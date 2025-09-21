# test_api.py
import requests

url = "https://tb6thx4hctkh8-crewai--3000.prod1a.defang.dev/generate"
data = {"user_text": ""}

response = requests.get(url, json=data)
print("Status code:", response.status_code)
print("Response:", response.json())