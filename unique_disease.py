import pandas as pd
import os

# File name
csv_file = "Disease_Symptom_final.csv"

# Read CSV
df = pd.read_csv(csv_file)

# Extract unique diseases
unique_diseases = df['disease'].unique()

# Get directory of the CSV file
output_dir = os.path.dirname(os.path.abspath(csv_file))

# Output file path
output_file = os.path.join(output_dir, "unique_diseases.txt")

# Save unique diseases to txt file
with open(output_file, "w", encoding="utf-8") as f:
    for disease in unique_diseases:
        f.write(disease + "\n")

print(f"✅ Unique diseases saved to {output_file}")
print(f"Total unique diseases: {len(unique_diseases)}")
