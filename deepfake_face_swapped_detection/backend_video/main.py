from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
import torch.nn.functional as F
import torchaudio
from torchvision import transforms
import cv2
import numpy as np
import os
import shutil
import shutil as _shutil
import uuid
import gc
from PIL import Image
from model_arch import MultiModalDeepfakeDetector, Config

# -- MEMORY OPTIMIZATION: Reduce thread overhead for Render Free Tier --
torch.set_num_threads(1)
from downloader import download_video
from url_handler import detect_platform, is_supported_platform

from pydantic import BaseModel


class VideoURLRequest(BaseModel):
    url: str


# -- Force Audio Backend for Windows --
try:
    torchaudio.set_audio_backend("soundfile")
except:
    pass

app = FastAPI(title="Deepfake Detection API")

# --- CRITICAL FIX 1: Enable CORS ---
# This allows your Vue.js frontend running on a different port to contact this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL (e.g., ["http://localhost:5173"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -- Load Configuration and Model --
config = Config()
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
MODEL_PATH = "best_model.pth" 
HF_MODEL_URL = "https://huggingface.co/vedant3114/best_model_video/resolve/main/best_model.pth"

print(f"Using device: {DEVICE}")

# Initialize Model
model = MultiModalDeepfakeDetector().to(DEVICE)

# -- Helper: Download Model if Missing --
def download_model_if_missing():
    if not os.path.exists(MODEL_PATH):
        print(f"Model file {MODEL_PATH} not found. Downloading from Hugging Face...")
        print(f"URL: {HF_MODEL_URL}")
        try:
            import requests
            response = requests.get(HF_MODEL_URL, stream=True)
            response.raise_for_status()
            
            with open(MODEL_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print("✓ Model downloaded successfully!")
        except Exception as e:
            print(f"❌ Failed to download model: {e}")
            # We will attempt to load anyway, which will likely fail, but let the error propagate naturally below
            pass
    else:
        print(f"✓ Model file {MODEL_PATH} found locally.")

# Download model if needed
download_model_if_missing()

# Load Weights
if os.path.exists(MODEL_PATH):
    print(f"Loading weights from {MODEL_PATH}...")
    try:
        # --- CRITICAL FIX 2: weights_only=False for older/custom checkpoints ---
        # MEMORY FIX: Load to CPU explicitly to avoid any CUDA overhead allocation if not present
        checkpoint = torch.load(MODEL_PATH, map_location='cpu', weights_only=False)
        
        if 'model_state_dict' in checkpoint:
            state_dict = checkpoint['model_state_dict']
            del checkpoint # Free up the wrapper dict immediately
            gc.collect()
            model.load_state_dict(state_dict)
            del state_dict # Free up the state dict copy
        else:
            model.load_state_dict(checkpoint)
            del checkpoint
        
        gc.collect() # Force cleanup
        
        # --- CRITICAL: Force evaluation mode and disable gradients ---
        model.eval()
        for param in model.parameters():
            param.requires_grad = False
        
        print(f"Model Loaded Successfully! Memory usage optimized.")
    except Exception as e:
        print(f"Error loading model: {e}")
        # In production, we might want to crash if model fails, but for now print error
else:
    print(f"WARNING: Model file not found at {MODEL_PATH}. Inference will fail.")

# -- Helper 1: Image Preprocessing (Treats Image as Static Video) --
def preprocess_image_as_video(image_path):
    print(f"Processing image as static video: {image_path}")
    try:
        # 1. Load Image
        pil_image = Image.open(image_path).convert('RGB')
        
        # 2. Transform to Tensor [3, H, W]
        transform = transforms.Compose([
            transforms.Resize((config.IMG_SIZE, config.IMG_SIZE)), 
            transforms.ToTensor(), 
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        img_tensor = transform(pil_image)
        
        # 3. Repeat image to create a sequence: [Sequence_Length, 3, H, W]
        # This tricks the model into thinking it's a video where nothing moves.
        video_tensor = img_tensor.unsqueeze(0).repeat(config.SEQUENCE_LENGTH, 1, 1, 1)
        
        # 4. Create Dummy Silent Audio: [Sequence_Length, N_Mels, Time_Frames]
        audio_tensor = torch.zeros((config.SEQUENCE_LENGTH, config.AUDIO_N_MELS, 32))
        
        return audio_tensor, video_tensor
    except Exception as e:
        print(f"Image preprocessing error: {e}")
        return None, None

# -- Helper 2: Video Preprocessing with Enhanced Audio Handling --
def extract_audio_from_video(video_path, use_fallback=True):
    """
    Enhanced audio extraction with multiple fallback methods.
    Detects audio-video sync inconsistencies.
    """
    try:
        # Method 1: Try with torchaudio.load (fastest)
        try:
            waveform, sample_rate = torchaudio.load(str(video_path))
            return waveform, sample_rate, "torchaudio"
        except RuntimeError as e:
            if "TorchCodec" in str(e) and use_fallback:
                print(f"⚠️  TorchCodec not available, trying librosa fallback...")
                raise
            raise
            
    except Exception as e:
        # Method 2: Fallback using ffmpeg extraction
        try:
            import subprocess
            import io
            print(f"Using ffmpeg audio extraction...")

            # Check ffmpeg availability first to avoid WinError when it's missing
            if _shutil.which('ffmpeg') is None:
                print("ffmpeg not found on PATH; skipping ffmpeg audio extraction.")
                raise RuntimeError("ffmpeg not found")

            # Extract audio using ffmpeg
            cmd = [
                'ffmpeg', '-i', str(video_path),
                '-f', 'wav',
                '-acodec', 'pcm_s16le',
                '-ar', '16000',
                '-ac', '1',
                '-'
            ]

            result = subprocess.run(cmd, capture_output=True, timeout=30)
            if result.returncode == 0:
                # Load from bytes using scipy
                try:
                    from scipy.io import wavfile
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                        f.write(result.stdout)
                        temp_path = f.name

                    sample_rate, audio_data = wavfile.read(temp_path)
                    waveform = torch.from_numpy(audio_data.astype(np.float32) / 32768.0).unsqueeze(0)
                    os.remove(temp_path)
                    return waveform, sample_rate, "ffmpeg"
                except Exception:
                    pass
        except Exception as e2:
            print(f"ffmpeg extraction failed or skipped: {e2}")
        
        # Method 3: Return silence if audio extraction fails
        print(f"⚠️  Audio extraction failed ({str(e)[:50]}...). Using silent audio.")
        print("Note: This will affect consistency detection accuracy.")
        return None, None, "silence"


def preprocess_video(video_path):
    print(f"Processing video file: {video_path}")
    
    # --- Audio Extraction with Enhanced Error Handling ---
    audio_tensor = None
    try:
        waveform, sample_rate, extraction_method = extract_audio_from_video(video_path)
        
        if waveform is not None:
            print(f"✓ Audio extracted using: {extraction_method}")
            
            # Resample if needed
            if sample_rate != config.AUDIO_SAMPLE_RATE:
                resampler = torchaudio.transforms.Resample(sample_rate, config.AUDIO_SAMPLE_RATE)
                waveform = resampler(waveform)
            
            # Convert to mono
            if waveform.shape[0] > 1: 
                waveform = torch.mean(waveform, dim=0, keepdim=True)
            
            # Create mel spectrogram
            mel_spectrogram = torchaudio.transforms.MelSpectrogram(
                sample_rate=config.AUDIO_SAMPLE_RATE, n_fft=config.AUDIO_N_FFT, 
                n_mels=config.AUDIO_N_MELS, hop_length=512, power=2.0
            )
            
            segment_samples = int(config.AUDIO_SAMPLE_RATE * 1.0)
            audio_segments = []
            
            for i in range(config.SEQUENCE_LENGTH):
                start = i * segment_samples
                if start >= waveform.shape[1]:
                    segment = torch.zeros(1, segment_samples)
                else:
                    segment = waveform[:, start:start+segment_samples]
                
                if segment.shape[1] < segment_samples:
                    segment = F.pad(segment, (0, segment_samples - segment.shape[1]))
                
                mel_spec = mel_spectrogram(segment)
                audio_segments.append(mel_spec.squeeze(0))
            
            audio_tensor = torch.stack(audio_segments)
        else:
            raise Exception("Audio extraction returned None")
            
    except Exception as e:
        print(f"⚠️  Audio warning (using silence): {str(e)[:100]}")
        expected_time_dim = int(config.AUDIO_SAMPLE_RATE * 1.0 / 512) + 1
        audio_tensor = torch.zeros((config.SEQUENCE_LENGTH, config.AUDIO_N_MELS, expected_time_dim))

    # --- Video Extraction ---
    video_tensor = None
    try:
        cap = cv2.VideoCapture(str(video_path))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames < 1: return audio_tensor, None
        
        frame_indices = np.linspace(0, total_frames - 1, config.SEQUENCE_LENGTH, dtype=int)
        frames = []
        transform = transforms.Compose([
            transforms.ToPILImage(), 
            transforms.Resize((config.IMG_SIZE, config.IMG_SIZE)), 
            transforms.ToTensor(), 
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if ret:
                frames.append(transform(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            else:
                frames.append(torch.zeros(3, config.IMG_SIZE, config.IMG_SIZE))
        cap.release()
        video_tensor = torch.stack(frames)
    except Exception as e:
        print(f"Video error: {e}")
        return audio_tensor, None
        
    return audio_tensor, video_tensor

# -- API Endpoints --

@app.get("/")
def home():
    return {"status": "Deepfake Detection API is running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 1. Determine file type
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    temp_filename = f"temp_{uuid.uuid4()}{ext}"
    
    try:
        # 2. Save file
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 3. Choose Preprocessor based on extension
        if ext in ['.jpg', '.jpeg', '.png', '.webp']:
            audio, video = preprocess_image_as_video(temp_filename)
        else:
            audio, video = preprocess_video(temp_filename)
        
        if video is None:
            raise HTTPException(status_code=400, detail="Could not process file content.")

        # 4. Inference
        audio = audio.unsqueeze(0).to(DEVICE)
        video = video.unsqueeze(0).to(DEVICE)
        
        # --- CRITICAL: Ensure model is in eval mode and use no_grad context ---
        model.eval()
        with torch.no_grad():
            outputs = model(audio, video)
            logits = outputs['logits']
            confidence_scores = F.softmax(logits, dim=1)
            prediction_idx = torch.argmax(confidence_scores, dim=1).item()
            conf_score = confidence_scores[0, prediction_idx].item()

        label = "DEEPFAKE" if prediction_idx == 1 else "AUTHENTIC"
        
        return {
            "status": "ok",
            "result": {
                "label": label,
                "score": conf_score,
                "confidence": round(conf_score * 100, 2),
                "filename": filename
            }
        }

    except Exception as e:
        print(f"Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # 5. Clean up
        if os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
            except:
                pass

@app.post("/predict-video-url")
async def predict_video_url(payload: VideoURLRequest):
    """
    Predict deepfake from video URL (YouTube, Instagram, Facebook, TikTok, Twitter, Direct).
    
    Flow:
    1. Detect platform from URL
    2. Download video temporarily
    3. Run inference
    4. Clean up
    5. Return results with platform info
    """
    platform = detect_platform(payload.url)
    
    print(f"\n{'='*60}")
    print(f"URL Prediction Request")
    print(f"Platform: {platform}")
    print(f"URL: {payload.url[:80]}...")
    print(f"{'='*60}")

    if not is_supported_platform(platform):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported platform '{platform}'. Supported: YouTube, Instagram, Facebook, TikTok, Twitter, Direct URLs"
        )

    video_path = None
    try:
        # Download video
        print(f"Downloading video from {platform}...")
        video_path = download_video(payload.url, timeout=120)
        print(f"✓ Download complete: {video_path}")
        
        # Preprocess
        audio, video = preprocess_video(video_path)
        
        if video is None:
            raise HTTPException(status_code=400, detail="Could not process video content")
        
        # Inference
        audio = audio.unsqueeze(0).to(DEVICE)
        video = video.unsqueeze(0).to(DEVICE)
        
        model.eval()
        with torch.no_grad():
            outputs = model(audio, video)
            logits = outputs['logits']
            confidence_scores = F.softmax(logits, dim=1)
            prediction_idx = torch.argmax(confidence_scores, dim=1).item()
            conf_score = confidence_scores[0, prediction_idx].item()
            
            # Get consistency scores for explainability
            consistency_data = {
                'audio_consistency': outputs['consistency_scores']['audio_consistency'][0].item(),
                'video_consistency': outputs['consistency_scores']['video_consistency'][0].item(),
                'cross_modal_consistency': outputs['consistency_scores']['cross_modal_consistency'][0].item(),
            }
        
        label = "DEEPFAKE" if prediction_idx == 1 else "AUTHENTIC"
        
        print(f"✓ Inference complete")
        print(f"  Label: {label}")
        print(f"  Confidence: {conf_score:.4f}")
        print(f"{'='*60}\n")
        
        return {
            "status": "ok",
            "result": {
                "label": label,
                "score": round(conf_score, 4),
                "confidence": round(conf_score * 100, 2),
                "platform": platform,
                "consistency_scores": consistency_data,
                "source_url": payload.url[:50] + "..." if len(payload.url) > 50 else payload.url
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Prediction failed: {str(e)[:100]}"
        )
    
    finally:
        # Clean up
        if video_path and os.path.exists(video_path):
            try:
                os.remove(video_path)
                print(f"✓ Cleaned up: {video_path}")
            except Exception as e:
                print(f"⚠️  Could not clean up {video_path}: {e}")


@app.get("/supported-platforms")
async def get_supported_platforms():
    """
    Get list of supported platforms with metadata.
    Useful for frontend to display platform logos and info.
    """
    from url_handler import get_platform_info
    
    platforms = ["youtube", "instagram", "facebook", "tiktok", "twitter", "direct"]
    platform_info = {platform: get_platform_info(platform) for platform in platforms}
    
    return {
        "status": "ok",
        "platforms": platform_info
    }


@app.post("/predict-explain")
async def predict_with_explanation(file: UploadFile = File(...)):
    """
    Predict and provide detailed explainability analysis.
    Returns consistency scores, temporal analysis, and anomaly detection.
    """
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    temp_filename = f"temp_{uuid.uuid4()}{ext}"
    
    try:
        # Save and process
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        if ext in ['.jpg', '.jpeg', '.png', '.webp']:
            audio, video = preprocess_image_as_video(temp_filename)
        else:
            audio, video = preprocess_video(temp_filename)
        
        if video is None:
            raise HTTPException(status_code=400, detail="Could not process file")
        
        # Inference with features
        audio = audio.unsqueeze(0).to(DEVICE)
        video = video.unsqueeze(0).to(DEVICE)
        
        model.eval()
        with torch.no_grad():
            outputs = model(audio, video, return_features=True)
            logits = outputs['logits']
            confidence_scores = F.softmax(logits, dim=1)
            prediction_idx = torch.argmax(confidence_scores, dim=1).item()
            conf_score = confidence_scores[0, prediction_idx].item()
            
            # Extract temporal consistency
            audio_temporal = outputs['audio_temporal_consistency'].cpu().numpy()[0]
            video_temporal = outputs['video_temporal_consistency'].cpu().numpy()[0]
            
            consistency_scores = outputs['consistency_scores']
            
            # Detect anomalies
            threshold = 0.3
            audio_anomalies = np.where(audio_temporal < threshold)[0].tolist()
            video_anomalies = np.where(video_temporal < threshold)[0].tolist()
        
        label = "DEEPFAKE" if prediction_idx == 1 else "AUTHENTIC"
        
        return {
            "status": "ok",
            "prediction": {
                "label": label,
                "score": round(conf_score, 4),
                "confidence": round(conf_score * 100, 2),
            },
            "explainability": {
                "audio_temporal_consistency": audio_temporal.tolist(),
                "video_temporal_consistency": video_temporal.tolist(),
                "global_consistency": {
                    "audio": round(consistency_scores['audio_consistency'][0].item(), 4),
                    "video": round(consistency_scores['video_consistency'][0].item(), 4),
                    "cross_modal": round(consistency_scores['cross_modal_consistency'][0].item(), 4),
                },
                "anomalies_detected": {
                    "audio_inconsistencies": len(audio_anomalies),
                    "video_inconsistencies": len(video_anomalies),
                    "audio_anomaly_indices": audio_anomalies[:10],  # First 10
                    "video_anomaly_indices": video_anomalies[:10],
                    "severity": "HIGH" if len(audio_anomalies) > 5 or len(video_anomalies) > 5 else "MEDIUM" if len(audio_anomalies) > 0 or len(video_anomalies) > 0 else "LOW"
                },
                "sequence_length": len(audio_temporal),
                "analysis_type": "temporal_consistency_analysis"
            },
            "filename": filename
        }
    
    except Exception as e:
        print(f"Explainability Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(temp_filename):
            try:
                os.remove(temp_filename)
            except:
                pass


@app.post("/predict-url-explain")
async def predict_url_with_explanation(payload: VideoURLRequest):
    """
    Predict from URL with detailed explainability.
    Combines URL downloading with temporal analysis.
    """
    platform = detect_platform(payload.url)
    
    if not is_supported_platform(platform):
        raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform}")
    
    video_path = None
    try:
        video_path = download_video(payload.url, timeout=120)
        
        audio, video = preprocess_video(video_path)
        
        if video is None:
            raise HTTPException(status_code=400, detail="Could not process video")
        
        audio = audio.unsqueeze(0).to(DEVICE)
        video = video.unsqueeze(0).to(DEVICE)
        
        model.eval()
        with torch.no_grad():
            outputs = model(audio, video, return_features=True)
            logits = outputs['logits']
            confidence_scores = F.softmax(logits, dim=1)
            prediction_idx = torch.argmax(confidence_scores, dim=1).item()
            conf_score = confidence_scores[0, prediction_idx].item()
            
            audio_temporal = outputs['audio_temporal_consistency'].cpu().numpy()[0]
            video_temporal = outputs['video_temporal_consistency'].cpu().numpy()[0]
            consistency_scores = outputs['consistency_scores']
            
            threshold = 0.3
            audio_anomalies = np.where(audio_temporal < threshold)[0].tolist()
            video_anomalies = np.where(video_temporal < threshold)[0].tolist()
        
        label = "DEEPFAKE" if prediction_idx == 1 else "AUTHENTIC"
        
        return {
            "status": "ok",
            "prediction": {
                "label": label,
                "score": round(conf_score, 4),
                "confidence": round(conf_score * 100, 2),
                "platform": platform
            },
            "explainability": {
                "audio_temporal_consistency": audio_temporal.tolist(),
                "video_temporal_consistency": video_temporal.tolist(),
                "global_consistency": {
                    "audio": round(consistency_scores['audio_consistency'][0].item(), 4),
                    "video": round(consistency_scores['video_consistency'][0].item(), 4),
                    "cross_modal": round(consistency_scores['cross_modal_consistency'][0].item(), 4),
                },
                "anomalies_detected": {
                    "audio_inconsistencies": len(audio_anomalies),
                    "video_inconsistencies": len(video_anomalies),
                    "severity": "HIGH" if len(audio_anomalies) > 5 or len(video_anomalies) > 5 else "MEDIUM" if len(audio_anomalies) > 0 or len(video_anomalies) > 0 else "LOW"
                },
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if video_path and os.path.exists(video_path):
            try:
                os.remove(video_path)
            except:
                pass


if __name__ == "__main__":
    import uvicorn
    # Use config from env or default to 8000
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)