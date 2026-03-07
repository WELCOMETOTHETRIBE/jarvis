#!/usr/bin/env python3
"""Comprehensive ElevenLabs API debugging"""

from dotenv import load_dotenv
load_dotenv()
import os
import requests

api_key = os.getenv("ELEVENLABS_API_KEY")
print("=" * 70)
print("🔍 ELEVENLABS API DEBUG")
print("=" * 70)

if not api_key:
    print("❌ No ELEVENLABS_API_KEY found in environment")
    exit(1)

print(f"\n✅ API Key found: {api_key[:15]}...")

# Test 1: User account info
print("\n" + "=" * 70)
print("1. USER ACCOUNT INFO")
print("=" * 70)
response = requests.get("https://api.elevenlabs.io/v1/user", headers={"xi-api-key": api_key}, timeout=5)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    user_info = response.json()
    print(f"  Subscription: {user_info.get('subscription', {}).get('tier', 'unknown')}")
    print(f"  Character limit: {user_info.get('subscription', {}).get('character_limit', 'unknown')}")
    print(f"  Characters used: {user_info.get('subscription', {}).get('character_count', 'unknown')}")
    print(f"  API key can use TTS: {user_info.get('subscription', {}).get('api_access', False)}")
else:
    print(f"  Error: {response.text[:200]}")

# Test 2: Get available voices and their details
print("\n" + "=" * 70)
print("2. AVAILABLE VOICES")
print("=" * 70)
response = requests.get("https://api.elevenlabs.io/v1/voices", headers={"xi-api-key": api_key}, timeout=5)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    voices = response.json().get("voices", [])
    print(f"  Total voices: {len(voices)}")
    if voices:
        voice = voices[0]
        print(f"\n  First voice (Sarah):")
        print(f"    Name: {voice.get('name')}")
        print(f"    Voice ID: {voice.get('voice_id')}")
        print(f"    Preview URL: {voice.get('preview_url', 'N/A')[:50]}")

# Test 3: Try different TTS models
print("\n" + "=" * 70)
print("3. TESTING DIFFERENT TTS MODELS")
print("=" * 70)

voice_id = "EXAVITQu4vr4xnSDxMaL"  # Sarah
models = [
    "eleven_monolingual_v1",
    "eleven_multilingual_v1", 
    "eleven_multilingual_v2",
    "eleven_turbo_v2"
]

for model in models:
    payload = {"text": "Hello", "model_id": model}
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        json=payload,
        headers={"xi-api-key": api_key, "Content-Type": "application/json"},
        timeout=10
    )
    print(f"  {model:25} -> {response.status_code}")
    if response.status_code != 200:
        error = response.json().get('detail', {})
        if isinstance(error, dict):
            print(f"      Error: {error.get('message', str(error))[:80]}")
        else:
            print(f"      Error: {str(error)[:80]}")

# Test 4: Test with minimal payload
print("\n" + "=" * 70)
print("4. TESTING MINIMAL PAYLOAD")
print("=" * 70)

payload = {"text": "Hi"}
response = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
    json=payload,
    headers={"xi-api-key": api_key},
    timeout=10
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print(f"✅ Success! Got {len(response.content)} bytes of audio")
else:
    print(f"Response: {response.text[:300]}")

# Test 5: Check subscription limits
print("\n" + "=" * 70)
print("5. SUBSCRIPTION CHECK")
print("=" * 70)
response = requests.get("https://api.elevenlabs.io/v1/subscription", headers={"xi-api-key": api_key}, timeout=5)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    sub = response.json()
    print(f"  Tier: {sub.get('tier', 'unknown')}")
    print(f"  Character limit: {sub.get('character_limit', 'N/A')}")
    print(f"  Characters used: {sub.get('character_count', 'N/A')}")
    print(f"  Can use API: {sub.get('can_use_professional_voices', 'N/A')}")
else:
    print(f"  Error: {response.text[:200]}")

print("\n" + "=" * 70)
print("💡 DIAGNOSIS")
print("=" * 70)
print("""
If you see 401 Unauthorized on TTS but 200 on /user endpoint:
  → Your API key may not have TTS access enabled
  → Check ElevenLabs account settings: Settings → API Access
  → Ensure "Text-to-Speech" is enabled for this API key

If you see 403 Forbidden:
  → Subscription might be expired or limited
  → Check billing: https://elevenlabs.io/subscription

If you see success (200) with binary audio:
  → ElevenLabs TTS is working! Update config and try again.
""")
print("=" * 70)
