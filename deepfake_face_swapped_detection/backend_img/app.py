from fastapi import FastAPI, File, UploadFile, HTTPException
from keras.models import load_model
from keras.applications.resnet50 import preprocess_input
from keras.preprocessing import image
import numpy as np
import uvicorn
from PIL import Image
import io
from fastapi.responses import JSONResponse

app = FastAPI()
img_height, img_width = 180, 180
# Load model once
model = load_model("resnet50_model_explicit.keras")

@app.get("/")
async def read_root():
    return {"message": "Model is ready for predictions"}

@app.get("/welcome{name}")
async def Welcome_message(name : str):
    return {"message": f"Welcome {name} to this API webpage this is a get method and you are getting this response as a result of a call."}
@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
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
        label = "Real" if prediction >= 0.5 else "Deepfake"
        confidence = float(prediction if prediction >= 0.5 else 1 - prediction)

        return JSONResponse({
            "label": label,
            "confidence": round(confidence, 4)
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# For local testing
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

