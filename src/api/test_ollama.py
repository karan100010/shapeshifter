import requests
import json

OLLAMA_URL = "http://localhost:11434"

def pull_model(model_name="llama3.2:1b"):
    """Pull a Llama model from Ollama"""
    print(f"📥 Pulling model: {model_name}")
    print("This may take a few minutes...")
    
    response = requests.post(
        f"{OLLAMA_URL}/api/pull",
        json={"name": model_name},
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            if "status" in data:
                print(f"Status: {data['status']}")
            if "completed" in data and "total" in data:
                progress = (data['completed'] / data['total']) * 100
                print(f"Progress: {progress:.1f}%")
    
    print("✅ Model pulled successfully!")

def test_model(model_name="llama3.2:1b", prompt="Hello! Tell me about yourself in one sentence."):
    """Test the Llama model with a simple prompt"""
    print(f"\n🧪 Testing model: {model_name}")
    print(f"Prompt: {prompt}")
    print("\nResponse:")
    
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(result.get("response", "No response"))
        print(f"\n✅ Model is working! (took {result.get('total_duration', 0) / 1e9:.2f}s)")
        return True
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        return False

def list_models():
    """List all installed models"""
    response = requests.get(f"{OLLAMA_URL}/api/tags")
    if response.status_code == 200:
        models = response.json().get("models", [])
        if models:
            print("\n📋 Installed models:")
            for model in models:
                print(f"  - {model['name']}")
        else:
            print("\n📋 No models installed")
        return models
    return []

if __name__ == "__main__":
    print("🚀 Ollama Model Manager\n")
    
    # Check current models
    models = list_models()
    
    # If no models, pull one
    if not models:
        pull_model("llama3.2:1b")
        models = list_models()
    
    # Test the first available model
    if models:
        model_name = models[0]['name']
        test_model(model_name)
    else:
        print("❌ No models available to test")
