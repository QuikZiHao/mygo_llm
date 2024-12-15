import requests

url = "http://localhost:8000/v1/completions"
headers = {"Content-Type": "application/json"}
data = {
    "model": "/models/Llama-3.2-1B",  # Correct model path with the leading slash
    "prompt": "are you good?",
    "max_tokens": 2048
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
