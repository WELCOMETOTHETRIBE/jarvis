#!/usr/bin/env python3
import os

# Load from .env file directly
env_path = '/Users/patrick/chat/jarvis-cli/.env'
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            if '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

import requests

hf_key = os.getenv("HUGGINGFACE_API_KEY")
print(f"HuggingFace Token: {hf_key[:20]}...")

# Test different approaches
print("\n=== Testing Different HF API Endpoints ===\n")

# Approach 1: Inference API (text generation)
print("1. Testing Inference API (text generation):")
headers = {"Authorization": f"Bearer {hf_key}"}
payload = {"inputs": "Hello world"}
try:
    response = requests.post(
        "https://api-inference.huggingface.co/models/gpt2",
        headers=headers,
        json=payload,
        timeout=10
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   Error: {e}")

# Approach 2: Check if token itself is valid (simple API call)
print("\n2. Testing Basic Auth with /user endpoint:")
try:
    response = requests.get(
        "https://huggingface.co/api/user",
        headers={"Authorization": f"Bearer {hf_key}"},
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text[:200]}")
except Exception as e:
    print(f"   Error: {e}")

# Approach 3: Check HF Hub Library
print("\n3. Testing with huggingface_hub library:")
try:
    from huggingface_hub import HfApi
    api = HfApi(token=hf_key)
    user = api.whoami()
    print(f"   ✅ SUCCESS! User: {user}")
except Exception as e:
    print(f"   Error: {str(e)[:200]}")

print("\n=== Diagnostics Complete ===")
