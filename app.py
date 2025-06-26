import pickle
import gzip
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
import os
import gdown

app = Flask(__name__)

# Set up file paths and download link
file_id = "15rT3yA0Qwm49XSBF2IjOkLkW9LrhbsgZ"  # your real file_id
model_path = "disease_model.gz"
model_url = f"https://drive.google.com/uc?id={file_id}"

# Flags
model = None
vectorizer = None
pca = None
le = None

# Load preprocessing files early (small files)
with open("tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("pca_model.pkl", "rb") as f:
    pca = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

def load_model():
    global model
    if model is None:
        if not os.path.exists(model_path):
            gdown.download(model_url, model_path, quiet=False)
        with gzip.open(model_path, "rb") as f:
            model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    load_model()
    data = request.get_json()
    input_symptoms = data.get("symptoms", [])

    symptom_text = " ".join(input_symptoms)
    tfidf_vector = vectorizer.transform([symptom_text])
    reduced_vector = pca.transform(tfidf_vector.toarray())

    probabilities = model.predict_proba(reduced_vector)[0]
    top_indices = np.argsort(probabilities)[-5:][::-1]

    top_predictions = []
    for idx in top_indices:
        disease = le.inverse_transform([model.classes_[idx]])[0]
        top_predictions.append({
            "disease": disease,
            "probability": round(float(probabilities[idx]), 4)
        })

    return jsonify({
        "predicted_disease": top_predictions[0]["disease"],
        "top_5_predictions": top_predictions
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
