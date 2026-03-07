# Quick API Key Signup Guide

Get all free API keys in ~10 minutes. Click each link, sign up, copy key, done!

## 🚀 Free APIs (No Credit Card)

### 1. **Groq** - Ultra-fast LLM (FREE)
**Time: 2 min**
- Visit: https://console.groq.com/keys
- Click "Sign in with Email" or "Continue with Google"
- Create account
- Copy your API key
- Paste into `.env`: `GROQ_API_KEY=gsk_xxxxx`

### 1b. **KlingAI** - Emerging AI platform (FREE beta)
**Time: 2 min**
- Visit: https://klingai.com
- Sign up with email
- Retrieve your API key from dashboard
- Paste into `.env`: `KLINGAI_API_KEY=xxxxx`

### 2. **Tavily** - Web Search (100/month FREE)
**Time: 2 min**
- Visit: https://tavily.com
- Click "Get Started"
- Sign up with email
- Go to dashboard
- Copy API key
- Paste into `.env`: `TAVILY_API_KEY=tvly_xxxxx`

### 3. **GitHub Token** - Code Search (Unlimited FREE)
**Time: 1 min**
- Visit: https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Name: "jarvis-cli"
- Select scopes: `repo`, `gist`, `read:public_repo`
- Generate & copy
- Paste into `.env`: `GITHUB_TOKEN=ghp_xxxxx`

### 4. **Replicate** - Image Generation ($40/month FREE credits)
**Time: 3 min**
- Visit: https://replicate.com
- Sign in with GitHub (use your account above)
- Go to Account > API tokens
- Copy API token
- Paste into `.env`: `REPLICATE_API_KEY=xxxxx`

### 5. **HuggingFace** - ML Models (FREE)
**Time: 2 min**
- Visit: https://huggingface.co/join
- Sign up with email
- Go to Settings > Access Tokens
- Create new token
- Paste into `.env`: `HUGGINGFACE_API_KEY=hf_xxxxx`

## 💳 Optional: One-time $5 Free Credit

### 6. **Anthropic Claude** - Better LLM ($5 free)
**Time: 3 min**
- Visit: https://console.anthropic.com
- Sign up with email
- Add payment method (won't charge)
- Go to Account > API keys
- Copy key
- Paste into `.env`: `ANTHROPIC_API_KEY=sk-ant-xxxxx`

### 7. **ElevenLabs** - Premium Voice (10k chars FREE/month)
**Time: 2 min**
- Visit: https://elevenlabs.io
- Sign up with email
- Go to Account > API keys
- Copy key
- Paste into `.env`: `ELEVENLABS_API_KEY=xxxxx`

## ⏱️ Total Time: ~15 minutes for all 7!

Once you have them all, just paste into `.env` and run:
```bash
./venv/bin/python scripts/validate_keys.py
```
