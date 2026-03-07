#!/usr/bin/env python3
"""Interactive guide to fix failing APIs"""

import os
from dotenv import load_dotenv

print("\n" + "="*80)
print("🔧 JARVIS CLI - API FIX GUIDE")
print("="*80 + "\n")

print("Two APIs are reporting authentication errors (401).")
print("Follow the steps below to fix them:\n")

print("="*80)
print("❌ ISSUE #1: Replicate API (401 Unauthorized)")
print("="*80 + """

PROBLEM:
Your Replicate API key is invalid or expired. This prevents image generation
using Stable Diffusion models.

FIX STEPS:
1. Go to: https://replicate.com/account/api-tokens
2. Sign in with your Replicate account
3. Copy your API token (should start with 'r8_')
4. Open .env file and update:
   REPLICATE_API_KEY=your_copied_token_here
5. Save the file

VERIFY:
$ cd /Users/patrick/chat/jarvis-cli
$ ./venv/bin/python3 final_validation.py

You should see: ✅ WORKING for Replicate

COST: FREE ($40/month free credits)
MODELS: Stable Diffusion, image editing, variations
""")

print("\n" + "="*80)
print("❌ ISSUE #2: HuggingFace API (401 Invalid Credentials)")
print("="*80 + """

PROBLEM:
Your HuggingFace API key is invalid or has wrong permissions.
This prevents access to 1000+ ML models and inference.

FIX STEPS:
1. Go to: https://huggingface.co/settings/tokens
2. Sign in with your HuggingFace account
3. Delete the old/invalid token if it exists
4. Click "New token" button
5. Give it a name (e.g., "Jarvis CLI")
6. Select "Read" permission (that's all we need)
7. Copy the new token (starts with 'hf_')
8. Open .env file and update:
   HUGGINGFACE_API_KEY=your_new_token_here
9. Save the file

VERIFY:
$ cd /Users/patrick/chat/jarvis-cli
$ ./venv/bin/python3 final_validation.py

You should see: ✅ WORKING for HuggingFace

COST: FREE (unlimited inference API calls)
MODELS: 1000+ text, image, audio, video models
""")

print("\n" + "="*80)
print("✅ AFTER FIXING BOTH")
print("="*80 + """

Once you've updated both keys in .env:

1. Verify all APIs are working:
   $ ./venv/bin/python3 final_validation.py
   
2. This should show:
   ✅ WORKING: 9/9 APIs ready for production

3. You'll then have access to:
   ✅ ChatGPT-like conversations (3+ LLMs)
   ✅ Image generation (DALL-E 3 + 100+ Stable Diffusion models)
   ✅ Real-time web search
   ✅ Premium text-to-speech (100+ voices)
   ✅ ML model playground (HuggingFace)
   ✅ Code search (GitHub)
   ✅ More!

4. Start the web UI:
   $ ./venv/bin/python -m streamlit run web/app.py
""")

print("\n" + "="*80)
print("💡 QUICK FIX CHECKLIST")
print("="*80 + """

□ Visit https://replicate.com/account/api-tokens
□ Copy new Replicate token
□ Update .env: REPLICATE_API_KEY=...
□ Visit https://huggingface.co/settings/tokens
□ Create new HuggingFace token
□ Update .env: HUGGINGFACE_API_KEY=...
□ Run: ./venv/bin/python3 final_validation.py
□ Verify: See ✅ WORKING for all 9 APIs
□ Success! 🎉
""")

print("\n" + "="*80)
print("❓ STILL HAVING ISSUES?")
print("="*80 + """

API Key Format Checklist:
✓ Replicate keys start with: r8_
✓ HuggingFace keys start with: hf_
✓ No extra spaces before/after
✓ Correct copy/paste (check for typos)

Common Mistakes:
✗ Including spaces: " sk_abc..." 
✗ Partial copy: sk_abc (incomplete)
✗ Old/expired tokens (regenerate)
✗ Permissions too restrictive (set to "read")

If it still doesn't work:
1. Double-check key format
2. Regenerate key from provider dashboard
3. Make sure .env file was saved
4. Restart terminal and try again
""")

print("\n" + "="*80 + "\n")
