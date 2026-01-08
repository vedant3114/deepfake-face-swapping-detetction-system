import tensorflow as tf
from tensorflow.keras import layers, models, applications
from pathlib import Path

IMG_SIZE = (128, 128, 3)

def build_model():
    base_model = applications.EfficientNetB0(
        input_shape=IMG_SIZE,
        include_top=False,
        weights="imagenet"
    )

    base_model.trainable = False

    inputs = layers.Input(shape=IMG_SIZE)
    x = base_model(inputs, training=False)

    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.5)(x)

    outputs = layers.Dense(1, activation="sigmoid")(x)

    return models.Model(inputs, outputs)


def main():
    model = build_model()

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    model.summary()

    BASE_DIR = Path(__file__).resolve().parent
    MODEL_DIR = BASE_DIR / "models"
    MODEL_DIR.mkdir(exist_ok=True)

    model.save(MODEL_DIR / "my_model.h5")
    print("Model saved to", MODEL_DIR / "my_model.h5")


if __name__ == "__main__":
    main()
