# Backend for Deepfake Image Detector

This folder contains a FastAPI backend that loads a TensorFlow/Keras model and
exposes a `/predict` endpoint to accept uploaded images and return a
deepfake prediction.

Place your trained image model file at:

```
backend_image/models/my_model.h5

```

Run server:

```bash
# from backend_image folder (with venv active)
python3 -m uvicorn app.main:app --reload --port 8002

```

Usage (curl):
```bash
curl -F "file=@/path/to/image.jpg" http://localhost:8002/predict
```

API Endpoints:

- `GET /health` – check backend and model status
- `POST /predict` – upload an image for deepfake detection
