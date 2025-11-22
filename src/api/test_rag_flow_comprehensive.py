import requests
import json
import time
import os

API_URL = "http://localhost:8001"
CHAT_URL = f"{API_URL}/chat"
UPLOAD_URL = f"{API_URL}/upload"
GDRIVE_UPLOAD_URL = f"{API_URL}/upload/google-drive"

def print_separator(title):
    print(f"\n{'='*60}")
    print(f"TEST: {title}")
    print(f"{'='*60}")

def send_message(msg, session_id="test_session_1"):
    print(f"USER: {msg}")
    try:
        response = requests.post(
            CHAT_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"message": msg, "session_id": session_id})
        )
        if response.status_code == 200:
            result = response.json()
            print(f"BOT: {result['response'][:100]}..." if len(result['response']) > 100 else f"BOT: {result['response']}")
            return result
        else:
            print(f"ERROR: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return None

def upload_file(filename, content, mime_type="text/plain"):
    print(f"Uploading file: {filename}...")
    try:
        files = {'file': (filename, content, mime_type)}
        response = requests.post(UPLOAD_URL, files=files)
        if response.status_code == 200:
            print(f"SUCCESS: {response.json()}")
            return True
        else:
            print(f"ERROR: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return False

def upload_gdrive(file_id):
    print(f"Importing from Google Drive (ID: {file_id})...")
    try:
        response = requests.post(
            GDRIVE_UPLOAD_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps({"file_id": file_id})
        )
        if response.status_code == 200:
            print(f"SUCCESS: {response.json()}")
            return True
        else:
            print(f"ERROR: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return False

def run_tests():
    print("🚀 Starting Comprehensive RAG Flow Tests...")
    
    # Test 1: Health Check
    print_separator("Health Check")
    try:
        resp = requests.get(f"{API_URL}/health")
        print(f"Health Status: {resp.json()}")
    except Exception as e:
        print(f"Health Check Failed: {e}")
        return

    # Test 2: RAG Creation Workflow
    print_separator("RAG Creation Workflow")
    session_id = f"test_session_{int(time.time())}"
    
    # Step 1: Initiate
    send_message("Create a RAG for me", session_id)
    
    # Step 2: Name
    send_message("Engineering Docs", session_id)
    
    # Step 3: Multiple File Uploads
    print_separator("Multiple File Uploads")
    # Upload file 1
    upload_file("specs.txt", "System specifications v1.0")
    # Upload file 2
    upload_file("architecture.md", "# Architecture\n\nMicroservices based...")
    # Upload file 3 (Simulate re-uploading same name)
    upload_file("specs.txt", "System specifications v1.1 updated")
    
    # Confirm uploads in chat
    send_message("uploaded", session_id)
    
    # Step 4: Storage Name
    print_separator("Storage Configuration")
    send_message("eng_kb_v1", session_id)
    
    # Test 3: Google Drive Integration
    print_separator("Google Drive Integration")
    upload_gdrive("1A2B3C4D5E")
    
    # Test 4: General Chat (should use Gemma)
    print_separator("General Chat (NVIDIA Gemma)")
    send_message("What is the capital of France?", session_id)

    print("\n✅ All tests completed!")

if __name__ == "__main__":
    run_tests()
