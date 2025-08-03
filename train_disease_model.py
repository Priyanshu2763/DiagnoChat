import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
import pickle
import gzip

# Step 1: Load the dataset
df = pd.read_csv("/kaggle/input/disease-dataset-csv/disease_dataset.csv")
print("\u2705 Dataset Loaded. Shape:", df.shape)

# Drop rows with missing values
df.dropna(inplace=True)
print("\u2705 After dropping NaNs. Shape:", df.shape)

# Step 2: Combine symptoms into string (for TF-IDF)
# Convert binary symptom features into a string of active symptoms per row
def create_symptom_text(row):
    return " ".join([col for col in row.index if row[col] == 1])

symptom_columns = df.columns.drop("diseases")
df["symptom_text"] = df[symptom_columns].apply(create_symptom_text, axis=1)

# Step 3: Sample 50,000 rows
sampled_df = df.sample(n=50000, random_state=42)
X_text = sampled_df["symptom_text"]
y = sampled_df["diseases"]

# Step 4: TF-IDF Vectorization
vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(X_text)
print("\u2705 TF-IDF vectorized. Shape:", X_tfidf.shape)

# Step 5: PCA for dimensionality reduction
pca = PCA(n_components=100)
X_pca = pca.fit_transform(X_tfidf.toarray())
print("\u2705 PCA applied. Shape:", X_pca.shape)

# Step 6: Label encoding
y_encoder = LabelEncoder()
y_encoded = y_encoder.fit_transform(y)
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(y_encoder, f)
print("\u2705 LabelEncoder saved.")

# Step 7: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_pca, y_encoded, test_size=0.2, random_state=42)

# Step 8: Define hyperparameter grid
param_dist = {
    'n_estimators': [50, 100, 150],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['sqrt', 'log2', None]
}

# Step 9: RandomizedSearchCV
rfc = RandomForestClassifier(random_state=42, n_jobs=-1)
random_search = RandomizedSearchCV(
    estimator=rfc,
    param_distributions=param_dist,
    n_iter=10,
    cv=3,
    verbose=1,
    n_jobs=-1,
    random_state=42
)
random_search.fit(X_train, y_train)
model = random_search.best_estimator_

# Step 10: Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"🌟 Model Accuracy: {accuracy:.4f}")
print(f"📌 Best Params: {random_search.best_params_}")

# Save model and preprocessing tools
with gzip.open("disease_model.gz", "wb") as f:
    pickle.dump(model, f)

with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

with open("pca_model.pkl", "wb") as f:
    pickle.dump(pca, f)

print("\u2705 Files saved: 'disease_model.gz', 'tfidf_vectorizer.pkl', 'pca_model.pkl', 'label_encoder.pkl'")
