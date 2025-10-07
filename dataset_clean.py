import pandas as pd
import os

def one_hot_encode_symptoms(input_path: str, output_path: str):
    # Load dataset
    df = pd.read_csv(input_path)

    # Gather all symptom columns (everything except 'Disease')
    symptom_cols = [col for col in df.columns if col != "Disease"]

    # Flatten all symptoms into one list
    all_symptoms = set()
    for col in symptom_cols:
        all_symptoms.update(df[col].dropna().astype(str).str.strip().tolist())

    # Remove empty strings
    all_symptoms = {s for s in all_symptoms if s and s.lower() != "nan"}

    # Create new DataFrame with one-hot encoding
    encoded_rows = []
    for _, row in df.iterrows():
        disease = row["disease"]
        row_symptoms = set()
        for col in symptom_cols:
            val = str(row[col]).strip()
            if val and val.lower() != "nan":
                row_symptoms.add(val)

        # Build one-hot encoded dict
        encoded = {"disease": disease}
        for symptom in all_symptoms:
            encoded[symptom] = 1 if symptom in row_symptoms else 0

        encoded_rows.append(encoded)

    encoded_df = pd.DataFrame(encoded_rows)

    # Save encoded dataset
    encoded_df.to_csv(output_path, index=False)
    print(f"One-hot encoded file saved at: {output_path}")


if __name__ == "__main__":
    input_file = r"C:\Users\Priyanshu Gupta\Desktop\DiagnoChat\Disease_Symptom_final.csv"
    output_file = r"C:\Users\Priyanshu Gupta\Desktop\DiagnoChat\Disease_Symptom_final_encoded.csv"

    one_hot_encode_symptoms(input_file, output_file)
