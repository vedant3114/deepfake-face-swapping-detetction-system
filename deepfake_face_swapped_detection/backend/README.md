# Backend for Deepfake Detector

This folder contains a FastAPI backend that loads a PyTorch model and exposes a `/predict` endpoint to accept uploaded videos and return a prediction.

Place your model file at:

```
backend/models/best_pinpoint_model_antisocial.pth
```

Setup (recommended in a virtualenv):

```powershell
# from repository root
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# install a specific torch wheel for your CUDA or cpu if needed, e.g.:
# pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

Run server:

```powershell
# from backend folder (with venv active)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Usage (curl):

```bash
curl -F "file=@/path/to/video.mp4" http://localhost:8000/predict
```

Notes and caveats:
- The repository doesn't know the exact model architecture that produced `best_pinpoint_model_antisocial.pth`.
- If your .pth contains only a `state_dict`, you must provide the model class and load the state_dict in `backend/app/model.py` (see `ModelWrapper.load`).
- The `ModelWrapper` samples frames from the video and averages per-frame outputs. Adjust `num_frames` and preprocessing to match your model.
