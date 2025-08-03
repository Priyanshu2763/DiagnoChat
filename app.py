import pickle
import gzip
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
import os
import gdown

# --- Setup paths ---
MODEL_PATH = "disease_model.gz"
TFIDF_PATH = "tfidf_vectorizer.pkl"
PCA_PATH = "pca_model.pkl"
LABEL_ENCODER_PATH = "label_encoder.pkl"

# --- Google Drive file ID for the compressed model file ---
GDRIVE_FILE_ID = "15rT3yA0Qwm49XSBF2IjOkLkW9LrhbsgZ"  # Replace with yours if changed

# --- Download the model file if it's not present ---
if not os.path.exists(MODEL_PATH):
    print("⏬ Downloading model from Google Drive...")
    url = f"https://drive.google.com/uc?id={GDRIVE_FILE_ID}"
    gdown.download(url, MODEL_PATH, quiet=False)
else:
    print("✅ Model file already exists locally.")

# --- Load the model ---
with gzip.open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# --- Load preprocessing objects ---
with open(TFIDF_PATH, "rb") as f:
    vectorizer = pickle.load(f)

with open(PCA_PATH, "rb") as f:
    pca = pickle.load(f)

with open(LABEL_ENCODER_PATH, "rb") as f:
    le = pickle.load(f)

# --- Initialize Flask App ---
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_symptoms = data.get("symptoms", [])

    # Join symptoms into string
    symptom_text = " ".join(input_symptoms)

    # TF-IDF and PCA transformation
    tfidf_vector = vectorizer.transform([symptom_text])
    reduced_vector = pca.transform(tfidf_vector.toarray())

    # Predict and get top 5 diseases
    probabilities = model.predict_proba(reduced_vector)[0]
    top_indices = np.argsort(probabilities)[-5:][::-1]

    top_predictions = [
        {
            "disease": le.inverse_transform([model.classes_[idx]])[0],
            "probability": round(float(probabilities[idx]), 4)
        }
        for idx in top_indices
    ]

    return jsonify({
        "predicted_disease": top_predictions[0]["disease"],
        "top_5_predictions": top_predictions
    })

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)
