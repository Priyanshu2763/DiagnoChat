import pickle
import gzip
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

# Load trained Random Forest model
with gzip.open("C:/Users/Priyanshu Gupta/Desktop/DiagnoChat/disease_model.gz", "rb") as f:
    model = pickle.load(f)

# Load preprocessing objects
with open("C:/Users/Priyanshu Gupta/Desktop/DiagnoChat/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("C:/Users/Priyanshu Gupta/Desktop/DiagnoChat/pca_model.pkl", "rb") as f:
    pca = pickle.load(f)

with open("C:/Users/Priyanshu Gupta/Desktop/DiagnoChat/label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

# Initialize Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    input_symptoms = data.get("symptoms", [])

    # Create string for TF-IDF input
    symptom_text = " ".join(input_symptoms)

    # TF-IDF vectorization and PCA reduction
    tfidf_vector = vectorizer.transform([symptom_text])
    reduced_vector = pca.transform(tfidf_vector.toarray())

    # Predict top 5 probabilities
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
    app.run(debug=False, use_reloader=False)
