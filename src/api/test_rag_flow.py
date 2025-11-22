import requests
import json

API_URL = "http://localhost:8001/chat"

def send_message(msg):
    print(f"\n{'='*60}")
    print(f"USER: {msg}")
    print(f"{'='*60}")
    
    response = requests.post(
        API_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps({"message": msg})
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"BOT: {result['response']}\n")
        return result
    else:
        print(f"ERROR: {response.status_code} - {response.text}\n")
        return None

# Test the RAG creation flow
print("Testing RAG Creation Workflow...")

# Step 1: Initiate RAG creation
send_message("Create a RAG for me")

# Step 2: Provide RAG name
send_message("Product Documentation")

# Step 3: Confirm file upload
send_message("uploaded")

# Step 4: Provide storage name
send_message("docs_v1")

# Test general conversation (should use Gemma)
send_message("What is machine learning?")
