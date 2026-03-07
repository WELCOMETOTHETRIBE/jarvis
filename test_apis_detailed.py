#!/usr/bin/env python3
"""Detailed test of problematic APIs"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*70)
print("🔧 DETAILED DIAGNOSTICS FOR FAILED APIs")
print("="*70 + "\n")

# Test Replicate in detail
print("1️⃣  REPLICATE DETAILED TEST")
print("-" * 70)
try:
    key = os.getenv("REPLICATE_API_KEY")
    print(f"Key present: {'Yes' if key else 'No'}")
    print(f"Key length: {len(key) if key else 0}")
    print(f"Key sample: {key[:20]}..." if key else "")
    
    headers = {"Authorization": f"Bearer {key}"}
    response = requests.get("https://api.replicate.com/v1/models", headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    # Try alternative Replicate endpoint
    print("\nTrying alternative endpoint...")
    response2 = requests.get("https://api.replicate.com/v1/account", headers=headers, timeout=5)
    print(f"Account Status: {response2.status_code}")
    print(f"Response: {response2.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test HuggingFace in detail
print("\n\n2️⃣  HUGGINGFACE DETAILED TEST")
print("-" * 70)
try:
    key = os.getenv("HUGGINGFACE_API_KEY")
    print(f"Key present: {'Yes' if key else 'No'}")
    print(f"Key length: {len(key) if key else 0}")
    print(f"Key sample: {key[:20]}..." if key else "")
    
    headers = {"Authorization": f"Bearer {key}"}
    response = requests.get("https://huggingface.co/api/whoami", headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:200]}")
    
    # Try listing models
    print("\nTrying to list models...")
    response2 = requests.get("https://huggingface.co/api/models", headers=headers, timeout=5)
    print(f"Models Status: {response2.status_code}")
    print(f"Response: {response2.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Test OpenAI with actual request
print("\n\n3️⃣  OPENAI ACTUAL CALL TEST")
print("-" * 70)
try:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    print(f"Key present: {'Yes' if openai.api_key else 'No'}")
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Say hello in one word"}],
        max_tokens=5
    )
    print(f"✅ OpenAI works!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ OpenAI failed: {e}")

print("\n" + "="*70)
