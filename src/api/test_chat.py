import requests
import json

# Test the chat endpoint
url = "http://localhost:8001/chat"
headers = {"Content-Type": "application/json"}
payload = {"message": "Hello! What is artificial intelligence?"}

print("Testing NVIDIA Gemma API integration...")
print(f"Sending message: {payload['message']}")

response = requests.post(url, headers=headers, data=json.dumps(payload))

if response.status_code == 200:
    result = response.json()
    print("\n✅ Success!")
    print(f"Response: {result['response']}")
    print(f"Citations: {result.get('citations', [])}")
else:
    print(f"\n❌ Error: {response.status_code}")
    print(response.text)
