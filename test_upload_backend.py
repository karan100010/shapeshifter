import requests

# Test file upload with session_id
url = "http://localhost:8001/upload"

# Create a test text file
test_content = """
Article 14: Equality before law
The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India.

Article 19: Protection of certain rights regarding freedom of speech, etc.
All citizens shall have the right to freedom of speech and expression.
"""

files = {'file': ('test_constitution.txt', test_content, 'text/plain')}
data = {'session_id': 'test_session_123'}

print("📤 Uploading test file...")
response = requests.post(url, files=files, data=data)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")

# Now test chat with this session
chat_url = "http://localhost:8001/chat"
chat_payload = {
    "message": "What does Article 14 say?",
    "session_id": "test_session_123"
}

print("\n💬 Testing chat with uploaded context...")
chat_response = requests.post(chat_url, json=chat_payload)
print(f"Status Code: {chat_response.status_code}")
print(f"Response: {chat_response.json()}")
