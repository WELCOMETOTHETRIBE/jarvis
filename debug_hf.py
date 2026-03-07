#!/usr/bin/env python3
import os
import requests

# Load from .env
env_path = '/Users/patrick/chat/jarvis-cli/.env'
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ[key] = value

hf_token = os.getenv("HUGGINGFACE_API_KEY")

print("=" * 70)
print("🔍 HUGGINGFACE DEBUG")
print("=" * 70)

# 1. Check token format
print(f"\n1. TOKEN FORMAT CHECK:")
print(f"   Full token: {hf_token}")
print(f"   Length: {len(hf_token)}")
print(f"   Starts with 'hf_': {hf_token.startswith('hf_')}")
print(f"   Has spaces: {' ' in hf_token}")
print(f"   Has newlines: {chr(10) in hf_token}")

# 2. Test basic endpoints
print(f"\n2. TESTING ENDPOINTS:")

endpoints = [
    ("whoami", "https://huggingface.co/api/whoami"),
    ("user", "https://huggingface.co/api/user"),
    ("me", "https://huggingface.co/api/me"),
    ("v1/user/me", "https://huggingface.co/api/v1/user/me"),
]

for name, url in endpoints:
    headers = {"Authorization": f"Bearer {hf_token}"}
    try:
        resp = requests.get(url, headers=headers, timeout=3)
        print(f"   {name:20} -> {resp.status_code} - {resp.text[:80]}")
    except Exception as e:
        print(f"   {name:20} -> ERROR: {str(e)[:50]}")

# 3. Try different header formats
print(f"\n3. TESTING DIFFERENT HEADER FORMATS:")

header_formats = [
    ("Bearer", {"Authorization": f"Bearer {hf_token}"}),
    ("token", {"Authorization": f"token {hf_token}"}),
    ("Token", {"Authorization": f"Token {hf_token}"}),
    ("Private-Token", {"Private-Token": hf_token}),
    ("X-Token", {"X-Token": hf_token}),
]

url = "https://huggingface.co/api/whoami"
for name, headers in header_formats:
    try:
        resp = requests.get(url, headers=headers, timeout=3)
        print(f"   {name:20} -> {resp.status_code}")
    except Exception as e:
        print(f"   {name:20} -> ERROR")

# 4. Check if token is actually valid by checking user repos
print(f"\n4. TESTING INFERENCE API:")

inference_url = "https://api-inference.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {hf_token}"}
payload = {"inputs": "Hello"}

try:
    resp = requests.post(inference_url, headers=headers, json=payload, timeout=5)
    print(f"   Inference API Status: {resp.status_code}")
    print(f"   Response: {resp.text[:150]}")
except Exception as e:
    print(f"   Error: {e}")

# 5. Try router.huggingface.co (new endpoint)
print(f"\n5. TESTING NEW ROUTER ENDPOINT:")

router_url = "https://router.huggingface.co/models/gpt2"
headers = {"Authorization": f"Bearer {hf_token}"}
payload = {"inputs": "Hello"}

try:
    resp = requests.post(router_url, headers=headers, json=payload, timeout=5)
    print(f"   Router API Status: {resp.status_code}")
    print(f"   Response: {resp.text[:150]}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 70)
