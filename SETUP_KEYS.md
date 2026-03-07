# Quick API Key Setup

Getting all the free API keys takes ~15 minutes. Here's how:

## Easiest Way: Interactive Setup

```bash
python scripts/setup_keys.py
```

This walks you through each signup, lets you paste keys, and validates them all.

## Or: Use the browser opener

```bash
bash scripts/signup.sh
```

This opens all signup pages in your browser (macOS/Linux).

## Manual Setup

If you prefer to do it yourself, here are all the links:

### Required (5 min)
1. **Groq** → https://console.groq.com/keys → copy `gsk_...`
1b. **KlingAI** → https://klingai.com → dashboard → copy API key
2. **Tavily** → https://tavily.com → dashboard → copy `tvly_...`
3. **GitHub** → https://github.com/settings/tokens → create token → copy `ghp_...`

### Optional (5 min)
4. **Replicate** → https://replicate.com → account → copy token
5. **HuggingFace** → https://huggingface.co/join → settings → copy token
6. **Anthropic** → https://console.anthropic.com → account → copy `sk-ant-...`
7. **ElevenLabs** → https://elevenlabs.io → account → copy token

## Paste into .env

```bash
GROQ_API_KEY=gsk_...
TAVILY_API_KEY=tvly_...
GITHUB_TOKEN=ghp_...
REPLICATE_API_KEY=...
HUGGINGFACE_API_KEY=hf_...
ANTHROPIC_API_KEY=sk-ant-...
ELEVENLABS_API_KEY=...
```

## Validate All Keys

```bash
python scripts/validate_keys.py
```

Shows which keys are working ✅ and which need fixing ❌
