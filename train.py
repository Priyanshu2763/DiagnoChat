import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# ===============================
# 1. Load Dataset
# ===============================
data = pd.read_csv("C:/Users/Priyanshu Gupta/Desktop/DiagnoChat/Disease_Symptom_final_encoded.csv")

# Assuming 'Disease' column is the target
X = data.drop("disease", axis=1)   # Symptoms (features)
y = data["disease"]                # Disease labels

# ===============================
# 2. Train-Test Split
# ===============================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ===============================
# 3. Train Model (Random Forest)
# ===============================
model = RandomForestClassifier(
    n_estimators=200,      # number of trees
    max_depth=None,        # let it grow fully
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# ===============================
# 4. Evaluate
# ===============================
y_pred = model.predict(X_test)
print("✅ Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# ===============================
# 5. Save Model + Columns
# ===============================
# Save trained model
joblib.dump(model, "disease_model.pkl")

# Save feature (symptom) columns
joblib.dump(list(X.columns), "symptom_columns.pkl")

print("🎉 Model and columns saved: 'disease_model.pkl', 'symptom_columns.pkl'")
