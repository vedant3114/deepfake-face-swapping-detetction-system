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
import uuid
from PIL import Image
from model_arch import MultiModalDeepfakeDetector, Config

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

print(f"Using device: {DEVICE}")

# Initialize Model
model = MultiModalDeepfakeDetector().to(DEVICE)

# Load Weights
if os.path.exists(MODEL_PATH):
    print(f"Loading weights from {MODEL_PATH}...")
    try:
        # --- CRITICAL FIX 2: weights_only=False for older/custom checkpoints ---
        checkpoint = torch.load(MODEL_PATH, map_location=DEVICE, weights_only=False)
        
        if 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
        model.eval()
        print("Model Loaded Successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
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

# -- Helper 2: Video Preprocessing --
def preprocess_video(video_path):
    print(f"Processing video file: {video_path}")
    
    # --- Audio Extraction ---
    audio_tensor = None
    try:
        waveform, sample_rate = torchaudio.load(str(video_path))
        if sample_rate != config.AUDIO_SAMPLE_RATE:
            waveform = torchaudio.transforms.Resample(sample_rate, config.AUDIO_SAMPLE_RATE)(waveform)
        if waveform.shape[0] > 1: waveform = torch.mean(waveform, dim=0, keepdim=True)
        
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
            audio_segments.append(mel_spectrogram(segment).squeeze(0))
        audio_tensor = torch.stack(audio_segments)
    except Exception as e:
        print(f"Audio warning (using silence): {e}")
        audio_tensor = torch.zeros((config.SEQUENCE_LENGTH, config.AUDIO_N_MELS, 32))

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

if __name__ == "__main__":
    import uvicorn
    # Use port 8000 to match the Vue.js fetch request
    uvicorn.run(app, host="0.0.0.0", port=8000)