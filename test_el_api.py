#!/usr/bin/env python3
from dotenv import load_dotenv
load_dotenv()
import os
import requests

api_key = os.getenv("ELEVENLABS_API_KEY")
print(f"Key: {api_key[:20]}...")

# Test 1: Get voices
print("\n1. Testing voices endpoint:")
response = requests.get("https://api.elevenlabs.io/v1/voices", headers={"xi-api-key": api_key}, timeout=5)
print(f"   Status: {response.status_code}")
print(f"   Response: {response.text[:100]}")

# Test 2: Generate speech with different model
print("\n2. Testing text-to-speech with multilingual model:")
payload = {
    "text": "Hello world",
    "model_id": "eleven_multilingual_v2"
}
response = requests.post(
    "https://api.elevenlabs.io/v1/text-to-speech/EXAVITQu4vr4xnSDxMaL",
    json=payload,
    headers={"xi-api-key": api_key},
    timeout=10
)
print(f"   Status: {response.status_code}")
if response.status_code != 200:
    print(f"   Error: {response.text[:300]}")
