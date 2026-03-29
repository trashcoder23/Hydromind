"""
hydromind/ml/lstm_crash_predictor/export_onnx.py

Converts the trained Keras LSTM to ONNX format for Cloud Functions inference.
Input:  ml/lstm_crash_predictor/lstm_model.keras
Output: ml/models/model.onnx
"""

import os
import tf2onnx
import tensorflow as tf
import numpy as np

SCRIPT_DIR  = os.path.dirname(__file__)
MODEL_PATH  = os.path.join(SCRIPT_DIR, "lstm_model.keras")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "models", "model.onnx")

SEQUENCE_LEN = 288
N_FEATURES   = 4


def main():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Train the model first. Not found: {MODEL_PATH}")

    model = tf.keras.models.load_model(MODEL_PATH)
    print(f"Loaded model from {MODEL_PATH}")

    # Define input signature for ONNX export
    input_signature = [
        tf.TensorSpec(shape=(None, SEQUENCE_LEN, N_FEATURES), dtype=tf.float32, name="input")
    ]

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    model_proto, _ = tf2onnx.convert.from_keras(
        model,
        input_signature=input_signature,
        opset=13,
        output_path=OUTPUT_PATH,
    )

    print(f"ONNX model exported → {OUTPUT_PATH}")

    # Quick sanity check
    import onnxruntime as ort
    sess = ort.InferenceSession(OUTPUT_PATH)
    dummy = np.zeros((1, SEQUENCE_LEN, N_FEATURES), dtype=np.float32)
    result = sess.run(None, {"input": dummy})
    print(f"Sanity check — dummy input crash probability: {result[0][0][0]:.4f}")


if __name__ == "__main__":
    main()