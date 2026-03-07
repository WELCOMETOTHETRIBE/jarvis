#!/usr/bin/env python3
"""Test if we can at least use HuggingFace without auth"""

import requests

print("\n" + "=" * 70)
print("Testing HuggingFace Public APIs (no auth needed)")
print("=" * 70)

# 1. List models (public)
print("\n1. Public Models API:")
try:
    resp = requests.get("https://huggingface.co/api/models?limit=5", timeout=5)
    print(f"   Status: {resp.status_code}")
    models = resp.json()
    print(f"   Found {len(models)} models")
    if models:
        print(f"   Example: {models[0].get('id')}")
except Exception as e:
    print(f"   Error: {e}")

# 2. Get info about a specific model
print("\n2. Specific Model Info:")
try:
    resp = requests.get("https://huggingface.co/api/models/gpt2", timeout=5)
    print(f"   Status: {resp.status_code}")
    if resp.status_code == 200:
        print(f"   Model: {resp.json().get('id')}")
except Exception as e:
    print(f"   Error: {e}")

# 3. List datasets (public)
print("\n3. Public Datasets API:")
try:
    resp = requests.get("https://huggingface.co/api/datasets?limit=5", timeout=5)
    print(f"   Status: {resp.status_code}")
    datasets = resp.json()
    print(f"   Found {len(datasets)} datasets")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 70)
print("CONCLUSION:")
print("=" * 70)
print("""
The token 'hf_<YOUR_TOKEN>' is being rejected.

Possible causes:
1. Token is revoked or expired on HuggingFace side
2. Token was generated but never used/activated
3. Account has restrictions
4. Token format is incorrect (though it looks correct)

NEXT STEPS:
1. Go to https://huggingface.co/settings/tokens
2. Delete the old token completely
3. Create a completely NEW token from scratch
4. Copy it immediately (don't wait)
5. Paste here to update .env

OR skip HuggingFace entirely - you have 7 working APIs already!
""")
print("=" * 70 + "\n")
