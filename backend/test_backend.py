import requests

url = "http://127.0.0.1:5000/webhook"
headers = {"Content-Type": "application/json"}
data = {"message": "Tell me about data types"}

response = requests.post(url, json=data, headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
