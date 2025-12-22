import uuid
from pathlib import Path

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import aiofiles

from .model import ModelWrapper

ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "best_model.h5"

app = FastAPI(title="Deepfake Image Detection Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    global model_wrapper
    model_wrapper = None

    if MODEL_PATH.exists():
        try:
            model_wrapper = ModelWrapper(str(MODEL_PATH))
            model_wrapper.load()
            print("Image model loaded from", MODEL_PATH)
        except Exception as e:
            print("Failed to load image model:", e)
    else:
        print(f"Model not found at {MODEL_PATH}")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "model_loaded": MODEL_PATH.exists()
    }


@app.post("/predict-image")
async def predict_image(file: UploadFile = File(...)):
    if model_wrapper is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".jpg", ".jpeg", ".png"}:
        raise HTTPException(status_code=400, detail="Unsupported image type")

    tmp_dir = Path("./tmp_uploads")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    uid = uuid.uuid4().hex
    tmp_path = tmp_dir / f"upload_{uid}{suffix}"

    try:
        async with aiofiles.open(tmp_path, "wb") as out_file:
            while content := await file.read(1024 * 1024):
                await out_file.write(content)

        result = model_wrapper.predict_image(str(tmp_path))
        return {"status": "ok", "result": result}

    except Exception as e:
        return {"status": "error", "error": str(e)}

    finally:
        try:
            if tmp_path.exists():
                tmp_path.unlink()
        except Exception:
            pass
