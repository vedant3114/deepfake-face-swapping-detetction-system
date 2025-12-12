import os
import tempfile
from typing import Optional

import cv2
import numpy as np
try:
    import torch
    import torchvision.transforms as T
except Exception:
    # allow server to run without torch; ModelWrapper.load will raise if torch is required
    torch = None
    T = None


class ModelWrapper:
    def __init__(self, model_path: str, device: Optional[str] = None):
        self.model_path = model_path
        self.device = device
        self.model = None
        self.transform = None

    def load(self):
        if torch is None:
            raise RuntimeError("PyTorch is not installed in the environment. Install torch to load the model.")

        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        # set device default if not provided
        if not self.device:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # set up transforms lazily
        if T is None:
            raise RuntimeError("torchvision is not installed; install torchvision to enable image transforms.")

        self.transform = T.Compose([
            T.ToPILImage(),
            T.Resize((128, 128)),
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        # Load model. We try a few common loading patterns because .pth files vary.
        try:
            # common: saved state_dict or full model
            state = torch.load(self.model_path, map_location=self.device)
            if isinstance(state, dict) and 'state_dict' in state:
                # user should adapt model class to load state_dict; we assume full model saved
                self.model = state['state_dict']
            else:
                # if full model saved
                self.model = state
        except Exception:
            # last resort: load with torch.jit
            self.model = torch.jit.load(self.model_path, map_location=self.device)

        # If model is a dict or state_dict, try to find a model builder in backend.app.model_def
        if isinstance(self.model, dict):
            # Attempt to load model architecture from a user-supplied module
            try:
                # local import to avoid top-level dependency
                from . import model_def

                if not hasattr(model_def, 'build_model'):
                    raise RuntimeError('model_def.py must implement a build_model() function that returns an nn.Module')

                model = model_def.build_model()
                # The checkpoint might be a dict with nested 'state_dict' key
                state_dict = self.model
                if 'state_dict' in state_dict:
                    state_dict = state_dict['state_dict']

                # load state_dict into provided model
                model.load_state_dict(state_dict)
                self.model = model
            except Exception as e:
                raise RuntimeError(
                    "Loaded object is a state_dict. Provide a `backend/app/model_def.py` with a build_model() function to instantiate the model and load the checkpoint."
                ) from e

        self.model.to(self.device)
        self.model.eval()

    def _sample_frames(self, video_path: str, num_frames: int = 16):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError("Unable to open video file")

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        if frame_count <= 0:
            # fallback to reading sequentially
            frames = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
        else:
            indices = np.linspace(0, max(frame_count - 1, 0), num_frames, dtype=int)
            frames = []
            for idx in indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, int(idx))
                ret, frame = cap.read()
                if not ret:
                    continue
                frames.append(frame)

        cap.release()
        if len(frames) == 0:
            raise RuntimeError("No frames extracted from video")
        return frames

    def _preprocess_frames(self, frames):
        tensors = []
        for f in frames:
            # Convert BGR to RGB
            img = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
            t = self.transform(img)
            tensors.append(t)
        # shape: (num_frames, C, H, W)
        return torch.stack(tensors, dim=0)

    def predict_video(self, video_path: str, num_frames: int = 16):
        if self.model is None:
            raise RuntimeError("Model not loaded")

        frames = self._sample_frames(video_path, num_frames=num_frames)
        input_t = self._preprocess_frames(frames)

        # Build video and audio batches expected by the PinpointTransformer:
        # video: (B, T, C, H, W), audio: (B, T_a, num_mfcc)
        with torch.no_grad():
            # prepare video batch
            video_b = input_t.unsqueeze(0).to(self.device)  # (1, T, C, H, W)

            # try to build MFCC audio using torchaudio if available
            try:
                import torchaudio
                waveform, sr = torchaudio.load(video_path)
                mfcc_transform = torchaudio.transforms.MFCC(sample_rate=sr, n_mfcc=13)
                mfccs = mfcc_transform(waveform)
                # mfccs shape: (channels, n_mfcc, time) -> squeeze channel and transpose -> (time, n_mfcc)
                if mfccs.dim() == 3:
                    mfccs = mfccs.mean(dim=0)
                mfccs = mfccs.transpose(0, 1)
                audio_b = mfccs.unsqueeze(0).to(self.device)
            except Exception:
                # fallback: zeros tensor with a small temporal length
                num_mfcc = 13
                audio_len = max(16, int(video_b.shape[1]) * 2)
                audio_b = torch.zeros((1, audio_len, num_mfcc), device=self.device)

            # Run the model: it expects (video, audio, video_mask)
            outputs = self.model(video_b, audio_b, None)

            # outputs: (classification_logits, offset_logits, attention_map)
            cls_logits = outputs[0]
            if isinstance(cls_logits, torch.Tensor):
                prob = torch.sigmoid(cls_logits).squeeze().item()
                label = "DEEPFAKE" if prob >= 0.5 else "AUTHENTIC"
                return {"label": label, "score": float(prob)}
            else:
                return {"label": "AUTHENTIC", "score": 0.0}
