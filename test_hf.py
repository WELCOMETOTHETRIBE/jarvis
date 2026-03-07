import requests
import os

hf_key = os.environ.get("HUGGINGFACE_API_KEY", "not set")
print(f"HuggingFace Key: {hf_key[:20] if len(hf_key) > 20 else hf_key}...")

if hf_key != "not set":
    headers = {"Authorization": f"Bearer {hf_key}"}
    response = requests.get("https://huggingface.co/api/whoami", headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:300]}")
