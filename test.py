import joblib
import numpy as np
import pandas as pd
import os
from symptom_extractor_hybrid import extract_symptoms

# Base directory
BASE_DIR = r"C:\Users\Priyanshu Gupta\Desktop\DiagnoChat"
valid_symptoms = joblib.load(os.path.join(BASE_DIR,"symptom_columns.pkl"))

# Load trained model
model = joblib.load(os.path.join(BASE_DIR, "disease_model.pkl"))

# Load symptom columns (order matters!)
symptom_columns = joblib.load(os.path.join(BASE_DIR, "symptom_columns.pkl"))






def predict_disease(user_symptoms, top_k=3):
    """
    Predict the top-k probable diseases based on user symptoms.
    Args:
        user_symptoms (list): List of symptoms (strings)
        top_k (int): Number of top predictions to return
    Returns:
        list of (disease, probability%)
    """
    # Initialize input vector with 0s
    input_vector = np.zeros(len(symptom_columns))

    # Track unknown symptoms
    unknown = []

    # Set 1 for symptoms present
    for symptom in user_symptoms:
        if symptom in symptom_columns:
            idx = symptom_columns.index(symptom)
            input_vector[idx] = 1
        else:
            unknown.append(symptom)

    # Wrap as DataFrame to preserve feature names (avoids sklearn warning)
    input_df = pd.DataFrame([input_vector], columns=symptom_columns)

    # Predict probabilities
    probas = model.predict_proba(input_df)[0]

    # Get top-k indices
    top_k_idx = probas.argsort()[-top_k:][::-1]

    # Collect top predictions
    results = [(model.classes_[i], round(probas[i] * 100, 2)) for i in top_k_idx]

    return results, unknown

# Load disease info dataset
disease_info = pd.read_csv(os.path.join(BASE_DIR, "disease_info.csv"))

def get_disease_details(disease_name):
    """
    Fetch details of a disease from the knowledge base.
    Args:
        disease_name (str): Name of the disease
    Returns:
        str: Formatted details
    """
    row = disease_info[disease_info['disease'].str.lower() == disease_name.lower()]
    if row.empty:
        return f"No information found for {disease_name}."

    row = row.iloc[0]  # get the first matching row

    # Format nicely
    details = (
        f"\n📌 Disease: {row['disease']}\n"
        f"📝 Definition: {row['definition']}\n"
        f"💊 Care: {row['care']}\n"
        f"⚠️ Warning: {row['warning']}\n"
        f"💉 Suggested Medications: {row['medications']}\n"
        f"🔍 Causes: {row['causes']}\n"
        f"🛡️ Prevention: {row['prevention']}\n"
        "\n⚠️ This information is for educational purposes only and is not a substitute for "
        "professional medical advice. Please consult a qualified diagnostician or healthcare "
        "provider for proper diagnosis and treatment."
    )
    return details


# ---------- Example usage ----------
if __name__ == "__main__":
    # user_input_symptoms = ["runny nose","stuffy nose", "sore throat", "sneezing", "mild fever","lauda"]
    user_input = "I have runny nose, cough and i am feeling feverish and sneezing"
    user_input_symptoms = extract_symptoms(user_input, valid_symptoms)
    

    results, unknown = predict_disease(user_input_symptoms, top_k=3)

    if unknown:
        print(f"⚠️ These symptoms are not in the dataset and were ignored: {unknown}")
    # Take the top predicted disease
    top_disease = results[0][0] 
    # Fetch details
    details = get_disease_details(top_disease)
    print("🔮 Possible Diseases:")
    for disease, score in results:
        print(f"- {disease} ({score}%)")
    print(details)
