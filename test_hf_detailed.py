#!/usr/bin/env python3
import os
import sys

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
print(f"Testing HuggingFace with key: {hf_key[:30]}...")
print(f"Key length: {len(hf_key)}")

# Test 1: whoami endpoint
headers = {"Authorization": f"Bearer {hf_key}"}
print("\n1. Testing /api/whoami endpoint:")
response = requests.get("https://huggingface.co/api/whoami", headers=headers, timeout=5)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.text[:300]}")

# Test 2: user endpoint
print("\n2. Testing /api/user endpoint:")
response = requests.get("https://huggingface.co/api/user", headers=headers, timeout=5)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.text[:300]}")

# Test 3: models endpoint (no auth needed)
print("\n3. Testing /api/models endpoint (public):")
response = requests.get("https://huggingface.co/api/models?limit=1", timeout=5)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.text[:150]}")

print("\n✅ DIAGNOSTICS COMPLETE")
