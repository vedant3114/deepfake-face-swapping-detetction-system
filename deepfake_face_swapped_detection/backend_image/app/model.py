import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model


class ModelWrapper:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.input_size = (128, 128)  # change only if your model needs it

    def load(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        self.model = load_model(self.model_path)
        print("Image model loaded successfully")

    def _preprocess_image(self, image_path: str):
        img = cv2.imread(image_path)
        if img is None:
            raise RuntimeError("Failed to read image")

        # BGR → RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Resize
        img = cv2.resize(img, self.input_size)

        # Normalize
        img = img.astype("float32") / 255.0

        # Add batch dimension
        img = np.expand_dims(img, axis=0)

        return img

    def predict_image(self, image_path: str):
        if self.model is None:
            raise RuntimeError("Model not loaded")

        img = self._preprocess_image(image_path)

        prediction = self.model.predict(img)

        # Support both (1,) and (1,1) outputs
        prob = float(prediction.reshape(-1)[0])
        label = "DEEPFAKE" if prob >= 0.5 else "AUTHENTIC"

        return {
            "label": label,
            "score": prob
        }
