import requests
import json

BASE_URL = "http://localhost:8001"
SESSION_ID = "test_article21_session"

# Sample Constitution content about Article 21
constitution_content = """
ARTICLE 21: PROTECTION OF LIFE AND PERSONAL LIBERTY

No person shall be deprived of his life or personal liberty except according to procedure established by law.

JUDICIAL INTERPRETATION AND EXPANSION:

The Supreme Court of India has expansively interpreted Article 21 to include numerous substantive rights beyond mere procedural guarantees:

1. RIGHT TO LIVE WITH HUMAN DIGNITY
   - Maneka Gandhi v. Union of India (1978): Transformed Article 21 from a narrow procedural guarantee to a substantive right
   - "Procedure established by law" must be just, fair, and reasonable
   - Life means more than mere animal existence

2. RIGHTS DERIVED FROM ARTICLE 21:
   - Right to privacy (Justice K.S. Puttaswamy v. Union of India, 2017)
   - Right to education (Unni Krishnan v. State of A.P., 1993)
   - Right to health and medical care
   - Right to clean environment
   - Right to speedy trial
   - Right to legal aid
   - Right to shelter
   - Right to livelihood

3. TRANSFORMATION MECHANISM:
   The Court has used the "golden triangle" of Articles 14, 19, and 21 to read substantive content into Article 21.
   The phrase "procedure established by law" has been interpreted to mean "due process of law" incorporating principles of natural justice.

4. IMPACT ON INDIAN CONSTITUTION:
   - Shifted from a rigid procedural framework to a flexible rights-based approach
   - Enabled judicial activism and PIL (Public Interest Litigation)
   - Made fundamental rights more enforceable and meaningful
   - Created a living constitution that adapts to societal needs
"""

print("=" * 80)
print("TESTING RAG CONTEXT WITH ARTICLE 21 CONTENT")
print("=" * 80)

# Step 1: Create RAG
print("\nStep 1: Starting RAG creation...")
response = requests.post(f"{BASE_URL}/chat", json={
    "message": "create a rag for me",
    "session_id": SESSION_ID
})
print(f"Response: {response.json()['response'][:100]}...")

# Step 2: Set personality
print("\nStep 2: Setting personality...")
response = requests.post(f"{BASE_URL}/chat", json={
    "message": "Formal and Academic",
    "session_id": SESSION_ID
})
print(f"Response: {response.json()['response'][:100]}...")

# Step 3: Name the RAG
print("\nStep 3: Naming RAG...")
response = requests.post(f"{BASE_URL}/chat", json={
    "message": "Constitution Expert",
    "session_id": SESSION_ID
})
print(f"Response: {response.json()['response'][:100]}...")

# Step 4: Upload file
print("\nStep 4: Uploading Constitution document...")
files = {'file': ('article21_analysis.txt', constitution_content, 'text/plain')}
data = {'session_id': SESSION_ID}
response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
print(f"Upload response: {response.json()}")

# Step 5: Confirm upload
print("\nStep 5: Confirming file upload...")
response = requests.post(f"{BASE_URL}/chat", json={
    "message": "uploaded",
    "session_id": SESSION_ID
})
print(f"Response: {response.json()['response'][:150]}...")

# Step 6: Set storage name
print("\nStep 6: Setting storage name...")
response = requests.post(f"{BASE_URL}/chat", json={
    "message": "constitution_storage_v1",
    "session_id": SESSION_ID
})
print(f"Response: {response.json()['response'][:150]}...")

# Step 7: Ask the question
print("\nStep 7: Asking the critical question...")
print("\nQuestion: How has the expansive interpretation of Article 21 transformed the Indian Constitution?")
response = requests.post(f"{BASE_URL}/chat", json={
    "message": "How has the expansive interpretation of Article 21 transformed the Indian Constitution from a narrow procedural guarantee to a broad source of substantive rights?",
    "session_id": SESSION_ID
})

result = response.json()
print("\n" + "=" * 80)
print("ANSWER:")
print("=" * 80)
print(result['response'])
print("\n" + "=" * 80)
print(f"Citations: {result.get('citations', [])}")
print("=" * 80)
