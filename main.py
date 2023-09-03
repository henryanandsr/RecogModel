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
model_blob_name = "model_last.tflite"
model = load_model_from_gcs(model_bucket_name, model_blob_name)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the image file from the request
        file = request.files['file']
        img = Image.open(file).convert('RGB')
        img = img.resize((224, 224))
        
        # Preprocess the image
        input_details = model.get_input_details()
        output_details = model.get_output_details()
        
        print("Input details length:", len(input_details))
        print("Output details length:", len(output_details))
        print("Input details:", input_details)
        print("Output details:", output_details)
        
        if len(input_details) > 0 and len(output_details) > 0:
            quantization = input_details[0]['quantization']
            input_scale = quantization[0] if len(quantization) > 0 and quantization[0] != 0 else 1.0
            input_mean = quantization[1]
            input_std = quantization[2]
            input_data = np.array(img, dtype=np.float32) / input_scale
            input_data = (input_data - input_mean) / input_std
            input_data = np.expand_dims(input_data, axis=0)
            
            # Make predictions
            model.set_tensor(input_details[0]['index'], input_data)
            model.invoke()
            output_data = model.get_tensor(output_details[0]['index'])
            predicted_class = np.argmax(output_data)
            confidence = output_data[0][predicted_class]
            
            response = {
                "predicted_class": int(predicted_class),
                "confidence": float(confidence)
            }
            return jsonify(response)
        
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)