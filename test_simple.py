# -*- coding: utf-8 -*-
import requests
import json
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8001"
SESSION_ID = "test_article21_final"

# Sample Constitution content about Article 21
constitution_content = """
ARTICLE 21: PROTECTION OF LIFE AND PERSONAL LIBERTY

The Supreme Court has expansively interpreted Article 21 through landmark cases:

1. Maneka Gandhi v. Union of India (1978): This case TRANSFORMED Article 21 from a narrow procedural guarantee to a substantive right. The Court held that "procedure established by law" must be just, fair, and reasonable.

2. TRANSFORMATION IMPACT:
   - Before: Article 21 was merely procedural
   - After: Article 21 became a source of numerous substantive rights including right to privacy, education, health, clean environment, and livelihood

3. The transformation occurred through judicial interpretation using the "golden triangle" of Articles 14, 19, and 21.
"""

print("Testing RAG with Article 21 content...")
print("=" * 60)

# Quick setup
requests.post(f"{BASE_URL}/chat", json={"message": "create a rag", "session_id": SESSION_ID})
requests.post(f"{BASE_URL}/chat", json={"message": "Formal", "session_id": SESSION_ID})
requests.post(f"{BASE_URL}/chat", json={"message": "Constitution Expert", "session_id": SESSION_ID})

# Upload
print("\nUploading document...")
files = {'file': ('article21.txt', constitution_content.encode('utf-8'), 'text/plain')}
data = {'session_id': SESSION_ID}
upload_resp = requests.post(f"{BASE_URL}/upload", files=files, data=data)
print(f"Upload: {upload_resp.json()['status']}")

# Complete RAG setup
requests.post(f"{BASE_URL}/chat", json={"message": "uploaded", "session_id": SESSION_ID})
requests.post(f"{BASE_URL}/chat", json={"message": "storage1", "session_id": SESSION_ID})

# Ask question
print("\nAsking question about Article 21 transformation...")
response = requests.post(f"{BASE_URL}/chat", json={
    "message": "How did Article 21 transform from procedural to substantive?",
    "session_id": SESSION_ID
})

result = response.json()
print("\n" + "=" * 60)
print("ANSWER:")
print("=" * 60)
print(result['response'])
print("\n" + "=" * 60)
print(f"Source: {result.get('citations', [{}])[0].get('source', 'Unknown')}")
print("=" * 60)

# Check if answer mentions Maneka Gandhi case
if "Maneka Gandhi" in result['response'] or "1978" in result['response']:
    print("\n✓ SUCCESS: Bot is using the uploaded document!")
else:
    print("\n✗ FAILED: Bot is NOT using the uploaded document")
