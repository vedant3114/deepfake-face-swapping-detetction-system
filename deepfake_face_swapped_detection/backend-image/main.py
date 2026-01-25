import io
import os
import base64
from io import BytesIO
from contextlib import asynccontextmanager

import uvicorn
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras.applications.resnet50 import preprocess_input

# --- New Imports for URL Processing ---
from pydantic import BaseModel
from url_handler import detect_platform
from downloader import download_image

# -----------------------------
# Debug / Runtime Info
# -----------------------------
print("RUNNING FILE:", os.path.abspath(__file__))
print("TF VERSION:", tf.__version__)
print("TF PATH:", tf.__file__)
print("HAS tf.is_nan?", hasattr(tf, "is_nan"))

# -----------------------------
# Compatibility aliases (FIX)
# -----------------------------
# TF 2.20+ does not expose tf.is_nan / tf.is_inf at top-level.
# If any code (yours or imported) calls tf.is_nan, this prevents crashes.
if not hasattr(tf, "is_nan"):
    tf.is_nan = tf.math.is_nan  # type: ignore[attr-defined]
if not hasattr(tf, "is_inf"):
    tf.is_inf = tf.math.is_inf  # type: ignore[attr-defined]

# --- CONFIGURATION ---
MODEL_WEIGHTS_FILENAME = "resnet50_model.h5"
INPUT_SHAPE = (180, 180)

# Global variable to hold the loaded model
model = None


def get_gradcam_heatmap(img_array, model):
    """
    Computes Grad-CAM heatmap for explainability.
    """
    base_model = model.layers[0]          # ResNet50 base
    classifier_layers = model.layers[1:]  # GAP, Dense, Dropout, Dense

    with tf.GradientTape() as tape:
        inputs = tf.cast(img_array, tf.float32)
        feature_maps = base_model(inputs)
        tape.watch(feature_maps)

        x = feature_maps
        for layer in classifier_layers:
            x = layer(x)
        predictions = x
        score = predictions[0][0]

    grads = tape.gradient(score, feature_maps)
    if grads is None:
        # If no gradients, return zero heatmap
        return np.zeros((6, 6), dtype=np.float32)

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    feature_maps = feature_maps[0]
    heatmap = feature_maps @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0)

    # Use tf.math.* (correct) + alias above protects older calls elsewhere
    heatmap = tf.where(tf.math.is_nan(heatmap), 0.0, heatmap)
    heatmap = tf.where(tf.math.is_inf(heatmap), 0.0, heatmap)

    max_val = tf.math.reduce_max(heatmap)
    if max_val > 0:
        heatmap = heatmap / max_val

    return heatmap.numpy()


def explain_decision(heatmap):
    """Generates a text explanation based on heatmap focus areas."""
    h, w = heatmap.shape

    split_1 = h // 3
    split_2 = 2 * h // 3

    top_third = heatmap[:split_1, :]          # Eyes/Forehead
    mid_third = heatmap[split_1:split_2, :]   # Nose/Cheeks
    bot_third = heatmap[split_2:, :]          # Mouth/Chin

    scores = {
        "Eyes/Forehead": np.nanmean(top_third) if top_third.size > 0 else 0.0,
        "Nose/Cheeks": np.nanmean(mid_third) if mid_third.size > 0 else 0.0,
        "Mouth/Chin": np.nanmean(bot_third) if bot_third.size > 0 else 0.0
    }
    dominant_region = max(scores, key=scores.get)
    return dominant_region, scores


def generate_heatmap_image(img_array, heatmap):
    """Generates a base64 encoded heatmap overlay image."""
    import matplotlib.cm as cm

    # Original image
    img = keras_image.array_to_img(img_array[0])

    # Heatmap to color
    heatmap_uint8 = np.uint8(255 * heatmap)
    jet = cm.get_cmap("jet")
    jet_colors = jet(np.arange(256))[:, :3]
    jet_heatmap = jet_colors[heatmap_uint8]
    jet_heatmap = keras_image.array_to_img(jet_heatmap)
    jet_heatmap = jet_heatmap.resize((img.size[0], img.size[1]))
    jet_heatmap = keras_image.img_to_array(jet_heatmap)

    # Overlay
    superimposed = jet_heatmap * 0.4 + keras_image.img_to_array(img)
    superimposed = keras_image.array_to_img(superimposed)

    # To base64
    buffer = BytesIO()
    superimposed.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Loads the Keras model when the server starts.
    """
    global model
    try:
        print(f"🔄 Loading model weights from: {MODEL_WEIGHTS_FILENAME}...")

        base_model = ResNet50(weights="imagenet", include_top=False, input_shape=(180, 180, 3))
        base_model.trainable = False

        model = Sequential([
            base_model,
            GlobalAveragePooling2D(),
            Dense(384, activation="relu"),
            Dropout(0.5),
            Dense(1, activation="sigmoid"),
        ])

        model.load_weights(MODEL_WEIGHTS_FILENAME)
        print("✅ Model loaded successfully!")

    except Exception as e:
        print(f"❌ CRITICAL ERROR: Could not load model. {e}")
        print(f"Please ensure '{MODEL_WEIGHTS_FILENAME}' is a valid weights file in this directory.")

    yield
    model = None


# Initialize the App (debug=True to show full stack traces during development)
app = FastAPI(title="Deepfake Detection API", lifespan=lifespan, debug=True)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (can be restricted to specific URLs in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

class ImageURLRequest(BaseModel):
    url: str


def transform_image(image_bytes: bytes) -> np.ndarray:
    """
    Preprocesses the image to match the training pipeline exactly:
    1. Open image as RGB
    2. Resize to 180x180
    3. Convert to Array
    4. Apply ResNet50 'caffe' preprocessing (Zero-center, BGR conversion)
    """
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize(INPUT_SHAPE)

    img_array = keras_image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    return img_array


@app.post("/explain")
async def explain(file: UploadFile = File(...)):
    """
    Endpoint to explain the prediction with Grad-CAM heatmap and text explanation.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded. Check server logs.")

    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")

    try:
        contents = await file.read()
        processed_image = transform_image(contents)

        prediction = model.predict(processed_image)
        score = float(prediction[0][0])

        # NOTE: Verify your training label mapping.
        # Current logic assumes score>0.5 => Real. Adjust if your training was opposite.
        if score > 0.5:
            label = "Real"
            confidence = score
        else:
            label = "Deepfake"
            confidence = 1.0 - score

        heatmap = get_gradcam_heatmap(processed_image, model)
        dominant_region, region_scores = explain_decision(heatmap)
        heatmap_image = generate_heatmap_image(processed_image, heatmap)

        region_scores = {k: float(v) for k, v in region_scores.items()}

        explanation = (
            f"The model analyzed the image and found the highest activation in the {dominant_region} region. "
        )

        confidence_desc = "high" if confidence > 0.8 else "moderate" if confidence > 0.6 else "low"

        if label == "Deepfake":
            explanation += (
                f"With {confidence_desc} confidence ({confidence*100:.1f}%), this image is classified as a Deepfake. "
            )
            if dominant_region == "Eyes/Forehead":
                explanation += "The model detected potential artifacts in the eyes (e.g., irregular reflections, pupil shape) or hairline blending."
            elif dominant_region == "Nose/Cheeks":
                explanation += "The model focused on skin texture smoothing or unnatural shadowing around the nose and cheeks."
            elif dominant_region == "Mouth/Chin":
                explanation += "Irregularities in lip syncing, teeth alignment, or jawline blending were detected."
            else:
                explanation += "General synthetic patterns were observed."
        else:
            explanation += (
                f"With {confidence_desc} confidence ({confidence*100:.1f}%), this image is classified as Real. "
            )
            explanation += "The model detected natural skin textures, consistent lighting, and realistic facial features."

        return {
            "filename": file.filename,
            "prediction": label,
            "confidence_percentage": f"{confidence * 100:.2f}%",
            "raw_score": float(score),
            "dominant_focus_region": dominant_region,
            "region_scores": region_scores,
            "explanation": explanation,
            "heatmap_image_base64": heatmap_image,
        }

    except Exception as e:
        print(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/explain-url")
async def explain_url_endpoint(payload: ImageURLRequest):
    """
    Endpoint to explain the prediction from an Image URL.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded.")

    url = payload.url
    print(f"Received URL for analysis: {url}")
    
    # Detect platform (optional logging)
    platform = detect_platform(url)
    print(f"Detected platform: {platform}")

    temp_file_path = None
    try:
        # Download image
        temp_file_path = download_image(url, output_dir="tmp_downloads_images")
        
        if not temp_file_path or not os.path.exists(temp_file_path):
            raise HTTPException(status_code=400, detail="Failed to download image from URL.")

        # Read file contents
        with open(temp_file_path, "rb") as f:
            contents = f.read()

        # --- Re-use existing logic ---
        processed_image = transform_image(contents)

        prediction = model.predict(processed_image)
        score = float(prediction[0][0])

        if score > 0.5:
            label = "Real"
            confidence = score
        else:
            label = "Deepfake"
            confidence = 1.0 - score

        heatmap = get_gradcam_heatmap(processed_image, model)
        dominant_region, region_scores = explain_decision(heatmap)
        heatmap_image = generate_heatmap_image(processed_image, heatmap)

        region_scores = {k: float(v) for k, v in region_scores.items()}

        explanation = (
            f"The model analyzed the image and found the highest activation in the {dominant_region} region. "
        )
        confidence_desc = "high" if confidence > 0.8 else "moderate" if confidence > 0.6 else "low"

        if label == "Deepfake":
            explanation += (
                f"With {confidence_desc} confidence ({confidence*100:.1f}%), this image is classified as a Deepfake. "
            )
            # Add specific explanations based on region logic (simplified for brevity, works same as file upload)
            if dominant_region == "Eyes/Forehead":
                explanation += "The model detected potential artifacts in the eyes or hairline."
            elif dominant_region == "Nose/Cheeks":
                explanation += "The model focused on skin texture anomalies."
            elif dominant_region == "Mouth/Chin":
                explanation += "Irregularities in the mouth/chin area were detected."
            else:
                explanation += "General synthetic patterns were observed."
        else:
            explanation += (
                f"With {confidence_desc} confidence ({confidence*100:.1f}%), this image is classified as Real. "
            )
            explanation += "The model detected natural features."

        return {
            "filename": url,
            "prediction": label,
            "confidence_percentage": f"{confidence * 100:.2f}%",
            "raw_score": float(score),
            "dominant_focus_region": dominant_region,
            "region_scores": region_scores,
            "explanation": explanation,
            "heatmap_image_base64": heatmap_image,
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Error processing URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Clean up
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except:
                pass


@app.get("/")
def home():
    return {
        "message": "Deepfake Detection Backend is Running",
        "model_status": "Loaded" if model else "Not Loaded",
    }


if __name__ == "__main__":
    # Use port 8001 for image backend (video backend uses 8000)
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
