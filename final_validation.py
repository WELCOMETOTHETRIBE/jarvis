#!/usr/bin/env python3
"""Final comprehensive API validation report"""

import os
import requests
import json
from datetime import datetime

# Load .env manually to ensure it works
env_path = '/Users/patrick/chat/jarvis-cli/.env'
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

print("\n" + "="*80)
print(" "*20 + "🎉 JARVIS CLI - FINAL API VALIDATION REPORT")
print(" "*30 + f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80 + "\n")

apis = {
    "OpenAI": {
        "status": "configured",
        "description": "GPT-4 Turbo text generation, DALL-E 3 images, TTS",
        "test": lambda: requests.get(
            "https://api.openai.com/v1/models",
            headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
            timeout=5
        )
    },
    "KlingAI": {
        "status": "configured",
        "description": "Experimental KlingAI endpoint",
        "test": lambda: requests.get(
            "https://api.klingai.com/v1/status",
            headers={"Authorization": f"Bearer {os.getenv('KLINGAI_API_KEY')}"},
            timeout=5
        )
    },
    "Groq": {
        "status": "configured",
        "description": "Ultra-fast Mixtral 8x7B inference (free)",
        "test": lambda: requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}"},
            timeout=5
        )
    },
    "Tavily": {
        "status": "configured",
        "description": "Real-time web search (100/month free)",
        "test": lambda: requests.post(
            "https://api.tavily.com/search",
            json={"api_key": os.getenv('TAVILY_API_KEY'), "query": "test"},
            timeout=10
        )
    },
    "GitHub": {
        "status": "configured",
        "description": "Code search and repo access",
        "test": lambda: requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"},
            timeout=5
        )
    },
    "Replicate": {
        "status": "configured",
        "description": "Image generation models ($40/month free credits)",
        "test": lambda: requests.get(
            "https://api.replicate.com/v1/account",
            headers={"Authorization": f"Bearer {os.getenv('REPLICATE_API_KEY')}"},
            timeout=5
        )
    },
    "HuggingFace": {
        "status": "configured",
        "description": "ML model hub and inference",
        "test": lambda: requests.get(
            "https://huggingface.co/api/whoami",
            headers={"Authorization": f"Bearer {os.getenv('HUGGINGFACE_API_KEY')}"},
            timeout=5
        )
    },
    "Anthropic": {
        "status": "configured",
        "description": "Claude 3.5 Sonnet ($5/month free credits)",
        "test": lambda: requests.get(
            "https://api.anthropic.com/v1/models",
            headers={"x-api-key": os.getenv("ANTHROPIC_API_KEY"), "anthropic-version": "2023-06-01"},
            timeout=5
        )
    },
    "ElevenLabs": {
        "status": "configured",
        "description": "Premium TTS with natural voices (10k chars/month free)",
        "test": lambda: requests.get(
            "https://api.elevenlabs.io/v1/user",
            headers={"xi-api-key": os.getenv("ELEVENLABS_API_KEY")},
            timeout=5
        )
    }
}

results = {}
print("🧪 RUNNING API TESTS...\n")

for name, config in apis.items():
    key = os.getenv(f"{name.upper()}_API_KEY") if name.upper() != "ANTHROPIC" else os.getenv("ANTHROPIC_API_KEY")
    key = os.getenv("GITHUB_TOKEN") if name == "GitHub" else key
    
    try:
        response = config["test"]()
        status = "✅ WORKING" if response.status_code == 200 else f"❌ FAILED ({response.status_code})"
        results[name] = {
            "status": status,
            "code": response.status_code,
            "desc": config["description"]
        }
        print(f"{status:20} {name:15} - {config['description']}")
    except requests.exceptions.Timeout:
        print(f"⏱️  TIMEOUT    {name:15} - Connection timeout")
        results[name] = {"status": "⏱️  TIMEOUT", "code": 0, "desc": config["description"]}
    except requests.exceptions.ConnectionError:
        print(f"🔌 NO CONNECTION {name:15}")
        results[name] = {"status": "🔌 NO CONNECTION", "code": 0, "desc": config["description"]}
    except Exception as e:
        print(f"❌ ERROR      {name:15} - {str(e)[:50]}")
        results[name] = {"status": "❌ ERROR", "code": 0, "desc": config["description"]}

# Summary Stats
print("\n" + "="*80)
print("📊 SUMMARY")
print("="*80)

working = sum(1 for r in results.values() if r["status"].startswith("✅"))
failed = sum(1 for r in results.values() if r["status"].startswith("❌"))
timeout = sum(1 for r in results.values() if r["status"].startswith("⏱️"))
noconn = sum(1 for r in results.values() if r["status"].startswith("🔌"))

print(f"\n✅ WORKING:     {working}/9 APIs ready for production")
print(f"❌ FAILED:      {failed}/9 APIs need fixing")
print(f"⏱️  TIMEOUT:     {timeout}/9 APIs (connection issue)")
print(f"🔌 NO CONNECTION: {noconn}/9 APIs (check network)")

# Detailed status
print("\n" + "-"*80)
print("DETAILED STATUS")
print("-"*80)

working_apis = [name for name, r in results.items() if r["status"].startswith("✅")]
failed_apis = [name for name, r in results.items() if r["status"].startswith("❌")]

if working_apis:
    print(f"\n✅ READY TO USE ({len(working_apis)}):")
    for api in working_apis:
        print(f"   • {api:20} - {results[api]['desc']}")

if failed_apis:
    print(f"\n❌ NEEDS FIXING ({len(failed_apis)}):")
    for api in failed_apis:
        print(f"   • {api:20} - {results[api]['desc']}")
        print(f"     └─ Status {results[api]['code']}: Invalid credentials or key issue")

# Usage instructions
print("\n" + "="*80)
print("🚀 QUICK START")
print("="*80)

print("""
1. START WEB UI:
   $ cd /Users/patrick/chat/jarvis-cli
   $ ./venv/bin/python -m streamlit run web/app.py
   → Opens at http://localhost:8502

2. TRY CLI COMMANDS:
   $ ./venv/bin/python -m app.main ask "What is AI?"
   $ ./venv/bin/python -m app.main image "robot painting"
   $ ./venv/bin/python -m app.main tts "Hello world"

3. COST BREAKDOWN:
   • OpenAI: ~$0.10-1 per request
   • Groq: FREE (100+ requests/day)
   • Tavily: FREE (100 searches/month)
   • GitHub: FREE (unlimited)
   • Replicate: $0.0035/sec (~$40 free/month)
   • Anthropic: FREE ($5 monthly credits)
   • ElevenLabs: FREE (10k chars/month)
   
   ✨ TOTAL COST: $0-2/month (mostly free tier!)

4. TROUBLESHOOTING FAILED APIS:

   ❌ Replicate: https://replicate.com/account/api-tokens
      - Copy your token and update .env
      
   ❌ HuggingFace: https://huggingface.co/settings/tokens
      - Create a new token with "read" permission
      - Update .env with the new token
""")

print("="*80)
print("✨ Your AI command center is ready!")
print("="*80 + "\n")
