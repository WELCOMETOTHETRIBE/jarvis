#!/usr/bin/env python3
"""Test all configured API keys"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

print("\n" + "="*70)
print("🔍 JARVIS CLI - API VALIDATION TEST")
print("="*70 + "\n")

results = {}

# Test 1: OpenAI
print("Testing OpenAI API...")
try:
    key = os.getenv("OPENAI_API_KEY")
    if not key or key == "your_openai_api_key_here":
        print("   ⚠️  OpenAI: MISSING KEY")
        results["OpenAI"] = "MISSING"
    else:
        print("   ✅ OpenAI: KEY CONFIGURED")
        results["OpenAI"] = "OK"
except Exception as e:
    print(f"   ❌ OpenAI: ERROR - {e}")
    results["OpenAI"] = "ERROR"

# Test 2: Groq
print("Testing Groq API...")
try:
    key = os.getenv("GROQ_API_KEY")
    if not key:
        print("   ❌ Groq: MISSING KEY")
        results["Groq"] = "MISSING"
    else:
        headers = {"Authorization": f"Bearer {key}"}
        response = requests.get("https://api.groq.com/openai/v1/models", headers=headers, timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Groq: WORKING ({len(response.json().get('data', []))} models)")
            results["Groq"] = "WORKING"
        else:
            print(f"   ❌ Groq: FAILED (Status {response.status_code})")
            results["Groq"] = "FAILED"
except Exception as e:
    print(f"   ❌ Groq: ERROR - {str(e)[:60]}")
    results["Groq"] = "ERROR"

# Test 2b: KlingAI
print("Testing KlingAI API...")
try:
    key = os.getenv("KLINGAI_API_KEY")
    if not key:
        print("   ⚠️  KlingAI: MISSING KEY")
        results["KlingAI"] = "MISSING"
    else:
        headers = {"Authorization": f"Bearer {key}"}
        response = requests.get("https://api.klingai.com/v1/status", headers=headers, timeout=5)
        if response.status_code == 200:
            print(f"   ✅ KlingAI: WORKING")
            results["KlingAI"] = "WORKING"
        else:
            print(f"   ❌ KlingAI: FAILED (Status {response.status_code})")
            results["KlingAI"] = "FAILED"
except Exception as e:
    print(f"   ❌ KlingAI: ERROR - {str(e)[:60]}")
    results["KlingAI"] = "ERROR"

# Test 3: Tavily
print("Testing Tavily Web Search...")
try:
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        print("   ❌ Tavily: MISSING KEY")
        results["Tavily"] = "MISSING"
    else:
        payload = {"api_key": key, "query": "AI"}
        response = requests.post("https://api.tavily.com/search", json=payload, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Tavily: WORKING")
            results["Tavily"] = "WORKING"
        else:
            print(f"   ❌ Tavily: FAILED (Status {response.status_code})")
            results["Tavily"] = "FAILED"
except Exception as e:
    print(f"   ❌ Tavily: ERROR - {str(e)[:60]}")
    results["Tavily"] = "ERROR"

# Test 4: GitHub
print("Testing GitHub API...")
try:
    key = os.getenv("GITHUB_TOKEN")
    if not key:
        print("   ❌ GitHub: MISSING KEY")
        results["GitHub"] = "MISSING"
    else:
        headers = {"Authorization": f"token {key}"}
        response = requests.get("https://api.github.com/user", headers=headers, timeout=5)
        if response.status_code == 200:
            user = response.json().get('login', 'unknown')
            print(f"   ✅ GitHub: WORKING (User: {user})")
            results["GitHub"] = "WORKING"
        else:
            print(f"   ❌ GitHub: FAILED (Status {response.status_code})")
            results["GitHub"] = "FAILED"
except Exception as e:
    print(f"   ❌ GitHub: ERROR - {str(e)[:60]}")
    results["GitHub"] = "ERROR"

# Test 5: Replicate
print("Testing Replicate API...")
try:
    key = os.getenv("REPLICATE_API_KEY")
    if not key:
        print("   ❌ Replicate: MISSING KEY")
        results["Replicate"] = "MISSING"
    else:
        headers = {"Authorization": f"Bearer {key}"}
        response = requests.get("https://api.replicate.com/v1/models", headers=headers, timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Replicate: WORKING")
            results["Replicate"] = "WORKING"
        else:
            print(f"   ❌ Replicate: FAILED (Status {response.status_code})")
            results["Replicate"] = "FAILED"
except Exception as e:
    print(f"   ❌ Replicate: ERROR - {str(e)[:60]}")
    results["Replicate"] = "ERROR"

# Test 6: HuggingFace
print("Testing HuggingFace API...")
try:
    key = os.getenv("HUGGINGFACE_API_KEY")
    if not key:
        print("   ❌ HuggingFace: MISSING KEY")
        results["HuggingFace"] = "MISSING"
    else:
        headers = {"Authorization": f"Bearer {key}"}
        response = requests.get("https://huggingface.co/api/whoami", headers=headers, timeout=5)
        if response.status_code == 200:
            user = response.json().get('name', 'unknown')
            print(f"   ✅ HuggingFace: WORKING (User: {user})")
            results["HuggingFace"] = "WORKING"
        else:
            print(f"   ❌ HuggingFace: FAILED (Status {response.status_code})")
            results["HuggingFace"] = "FAILED"
except Exception as e:
    print(f"   ❌ HuggingFace: ERROR - {str(e)[:60]}")
    results["HuggingFace"] = "ERROR"

# Test 7: Anthropic
print("Testing Anthropic Claude API...")
try:
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        print("   ❌ Anthropic: MISSING KEY")
        results["Anthropic"] = "MISSING"
    else:
        headers = {
            "x-api-key": key,
            "anthropic-version": "2023-06-01"
        }
        response = requests.get("https://api.anthropic.com/v1/models", headers=headers, timeout=5)
        if response.status_code == 200:
            print(f"   ✅ Anthropic: WORKING")
            results["Anthropic"] = "WORKING"
        else:
            print(f"   ❌ Anthropic: FAILED (Status {response.status_code})")
            results["Anthropic"] = "FAILED"
except Exception as e:
    print(f"   ❌ Anthropic: ERROR - {str(e)[:60]}")
    results["Anthropic"] = "ERROR"

# Test 8: ElevenLabs
print("Testing ElevenLabs TTS...")
try:
    key = os.getenv("ELEVENLABS_API_KEY")
    if not key:
        print("   ❌ ElevenLabs: MISSING KEY")
        results["ElevenLabs"] = "MISSING"
    else:
        headers = {"xi-api-key": key}
        response = requests.get("https://api.elevenlabs.io/v1/user", headers=headers, timeout=5)
        if response.status_code == 200:
            print(f"   ✅ ElevenLabs: WORKING")
            results["ElevenLabs"] = "WORKING"
        else:
            print(f"   ❌ ElevenLabs: FAILED (Status {response.status_code})")
            results["ElevenLabs"] = "FAILED"
except Exception as e:
    print(f"   ❌ ElevenLabs: ERROR - {str(e)[:60]}")
    results["ElevenLabs"] = "ERROR"

# Summary
print("\n" + "="*70)
print("📊 SUMMARY")
print("="*70)

working = sum(1 for v in results.values() if v == "WORKING")
failed = sum(1 for v in results.values() if v == "FAILED")
missing = sum(1 for v in results.values() if v == "MISSING")
errors = sum(1 for v in results.values() if v == "ERROR")

print(f"✅ Working: {working}/9")
print(f"❌ Failed: {failed}/9")
print(f"⚠️  Missing: {missing}/8")
print(f"🔴 Errors: {errors}/8")

print("\n" + "="*70)
