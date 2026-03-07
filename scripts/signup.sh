#!/bin/bash
# Quick signup helper - opens all signup links

echo "🚀 Opening API signup pages..."
echo ""
echo "Follow these links and sign up (takes ~2 min each):"
echo ""

# macOS - opens links in browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "1️⃣  Opening Groq..."
    open "https://console.groq.com/keys"
    
    sleep 2
    echo "2️⃣  Opening Tavily..."
    open "https://tavily.com"
    
    sleep 2
    echo "3️⃣  Opening GitHub..."
    open "https://github.com/settings/tokens"
    
    sleep 2
    echo "4️⃣  Opening Replicate..."
    open "https://replicate.com"
    
    sleep 2
    echo "5️⃣  Opening HuggingFace..."
    open "https://huggingface.co/join"
    
    sleep 2
    echo "6️⃣  Opening KlingAI (optional)..."
    open "https://klingai.com"
    
    sleep 2
    echo "7️⃣  Opening Anthropic (optional)..."
    open "https://console.anthropic.com"
    
    sleep 2
    echo "8️⃣  Opening ElevenLabs (optional)..."
    open "https://elevenlabs.io"
else
    echo "📝 Copy and paste these links into your browser:"
    echo ""
    echo "1. https://console.groq.com/keys"
    echo "2. https://tavily.com"
    echo "3. https://github.com/settings/tokens"
    echo "4. https://replicate.com"
    echo "5. https://huggingface.co/join"
    echo "6. https://console.anthropic.com (optional)"
    echo "7. https://elevenlabs.io (optional)"
fi

echo ""
echo "After signing up, paste your keys into .env:"
echo ""
echo "  GROQ_API_KEY=gsk_..."
echo "  TAVILY_API_KEY=tvly_..."
echo "  GITHUB_TOKEN=ghp_..."
echo "  REPLICATE_API_KEY=..."
echo "  HUGGINGFACE_API_KEY=hf_..."
echo "  ANTHROPIC_API_KEY=sk-ant-... (optional)"
echo "  ELEVENLABS_API_KEY=... (optional)"
echo "  KLINGAI_API_KEY=... (optional)"
echo ""
echo "Then run:"
echo "  python scripts/validate_keys.py"
