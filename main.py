from flask import Flask, request, jsonify
from google.cloud import storage
import tensorflow as tf
from PIL import Image
import numpy as np

app = Flask(__name__)
def load_model_from_gcs(bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.get_blob(blob_name)
    model_content = blob.download_as_bytes()
    model = tf.lite.Interpreter(model_content=model_content)
    model.allocate_tensors()
    return model


model_bucket_name = "dermatica"
model_blob_name = "model_final.tflite"
model = load_model_from_gcs(model_bucket_name, model_blob_name)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the image file from the request
        file = request.files['file']
        image = Image.open(file).convert('RGB')
        image = image.resize((224, 224))
        image = np.array(image)

        # Normalize the image
        image = (image / 255.0).astype(np.float32)

        # Make predictions
        input_details = model.get_input_details()
        output_details = model.get_output_details()
        model.set_tensor(input_details[0]['index'], image.reshape(1, 224, 224, 3))
        model.invoke()
        prediction = model.get_tensor(output_details[0]['index'])
        class_index = np.argmax(prediction, axis=1)[0]
        confidence = prediction[0][class_index]

        response = {
            "predicted_class": int(class_index),
            "confidence": float(confidence)
        }
        return jsonify(response)

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)