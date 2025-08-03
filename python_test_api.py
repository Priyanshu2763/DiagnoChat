import time
import requests

# Wait to ensure Flask server is ready
time.sleep(3)

url = "http://127.0.0.1:5000/predict"
data = {
    "symptoms": ["nausea", "abdominal pain", "diarrhea"]
}







response = requests.post(url, json=data)
print("Response:", response.json())
