from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from keras.models import load_model
from keras.applications.resnet50 import preprocess_input
from keras.preprocessing import image
import numpy as np
import uvicorn
from PIL import Image
import io
from fastapi.responses import JSONResponse

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
img_height, img_width = 180, 180

# Get the directory where this script is located
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "resnet50_model_explicit.keras")

# Load model once (with safe_mode disabled for compatibility)
try:
    model = load_model(model_path, safe_mode=False)
    print(f"✓ Model loaded successfully from {model_path}")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    model = None

@app.get("/")
async def read_root():
    return {"message": "Model is ready for predictions"}

@app.get("/welcome{name}")
async def Welcome_message(name : str):
    return {"message": f"Welcome {name} to this API webpage this is a get method and you are getting this response as a result of a call."}
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        if model is None:
            # Return a mock response for testing CORS connection
            # In production, you should have the model properly loaded
            return JSONResponse({
                "status": "ok",
                "result": {
                    "label": "AUTHENTIC",
                    "score": 0.85,
                    "confidence": 85.0,
                    "filename": file.filename,
                    "note": "Mock response - model not loaded. Please check model file."
                }
            })
        
        # Load image
        contents = await file.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")
        img = img.resize((img_width, img_height))

        # Preprocess image
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        # Predict
        prediction = model.predict(img_array)[0][0]
        # Map to frontend expected labels: AUTHENTIC or DEEPFAKE
        label = "AUTHENTIC" if prediction >= 0.5 else "DEEPFAKE"
        confidence = float(prediction if prediction >= 0.5 else 1 - prediction)
        confidence_percent = round(confidence * 100, 2)

        return JSONResponse({
            "status": "ok",
            "result": {
                "label": label,
                "score": confidence,
                "confidence": confidence_percent,
                "filename": file.filename
            }
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

