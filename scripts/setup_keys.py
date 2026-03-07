#!/usr/bin/env python3
"""Interactive API key setup wizard"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_service(name, url, instructions):
    print(f"📍 {name}")
    print(f"   URL: {url}")
    print(f"   Steps: {instructions}")
    print()

def main():
    load_dotenv()
    env_path = Path(".env")
    
    print_header("🚀 Jarvis CLI - API Key Setup Wizard")
    
    print("This will help you get all the free API keys.\n")
    print("Required (5 min total):")
    print("  1. Groq (free LLM)")
    print("  2. Tavily (web search)")
    print("  3. GitHub Token (code search)")
    print("\nOptional but recommended:")
    print("  4. Replicate (image gen)")
    print("  5. HuggingFace (ML models)")
    print("  6. Anthropic (better LLM)")
    print("  7. ElevenLabs (premium voices)\n")
    
    response = input("Ready to get started? (y/n): ").lower()
    if response != 'y':
        print("Exiting.")
        return
    
    # Groq
    print_header("Step 1: Groq API Key")
    print_service(
        "Groq (Ultra-fast LLM)",
        "https://console.groq.com/keys",
        "Sign up → Copy API key"
    )
    groq_key = input("Paste your Groq API key (or press Enter to skip): ").strip()
    
    # Tavily
    print_header("Step 2: Tavily API Key")
    print_service(
        "Tavily (Web Search)",
        "https://tavily.com",
        "Sign up → Dashboard → Copy API key"
    )
    tavily_key = input("Paste your Tavily API key (or press Enter to skip): ").strip()
    
    # GitHub
    print_header("Step 3: GitHub Token")
    print_service(
        "GitHub Token",
        "https://github.com/settings/tokens",
        "Generate new token (classic) → Check 'repo' and 'gist' → Copy"
    )
    github_key = input("Paste your GitHub token (or press Enter to skip): ").strip()
    
    # Replicate
    print_header("Step 4: Replicate API Key (Optional)")
    print_service(
        "Replicate (Image Generation)",
        "https://replicate.com",
        "Sign in with GitHub → Account → API tokens → Copy"
    )
    replicate_key = input("Paste your Replicate API key (or press Enter to skip): ").strip()
    
    # HuggingFace
    print_header("Step 5: HuggingFace API Key (Optional)")
    print_service(
        "HuggingFace (ML Models)",
        "https://huggingface.co/join",
        "Sign up → Settings → Access Tokens → Create new token"
    )
    hf_key = input("Paste your HuggingFace API key (or press Enter to skip): ").strip()
    
    # Anthropic
    print_header("Step 6: Anthropic API Key (Optional - $5 free credit)")
    print_service(
        "Anthropic Claude",
        "https://console.anthropic.com",
        "Sign up → Add payment method → Account → API keys"
    )
    anthropic_key = input("Paste your Anthropic API key (or press Enter to skip): ").strip()
    
    # ElevenLabs
    print_header("Step 7: ElevenLabs API Key (Optional)")
    print_service(
        "ElevenLabs (Premium TTS)",
        "https://elevenlabs.io",
        "Sign up → Account → API keys"
    )
    elevenlabs_key = input("Paste your ElevenLabs API key (or press Enter to skip): ").strip()
    
    # KlingAI
    print_header("Step 8: KlingAI API Key (Optional)")
    print_service(
        "KlingAI (Experimental AI)",
        "https://klingai.com",
        "Sign up → Dashboard → Copy API key"
    )
    klingai_key = input("Paste your KlingAI API key (or press Enter to skip): ").strip()
    
    # Write to .env
    print_header("💾 Saving to .env")
    
    env_content = []
    if env_path.exists():
        env_content = env_path.read_text().split('\n')
    
    # Update or add keys
    keys_to_add = {
        'GROQ_API_KEY': groq_key,
        'KLINGAI_API_KEY': klingai_key,
        'TAVILY_API_KEY': tavily_key,
        'GITHUB_TOKEN': github_key,
        'REPLICATE_API_KEY': replicate_key,
        'HUGGINGFACE_API_KEY': hf_key,
        'ANTHROPIC_API_KEY': anthropic_key,
        'ELEVENLABS_API_KEY': elevenlabs_key,
    }
    
    # Remove empty lines and old values
    new_content = []
    processed_keys = set()
    
    for line in env_content:
        key = line.split('=')[0] if '=' in line else None
        if key and key in keys_to_add:
            processed_keys.add(key)
            if keys_to_add[key]:
                new_content.append(f"{key}={keys_to_add[key]}")
        elif line.strip() and not line.startswith('#'):
            new_content.append(line)
    
    # Add missing keys
    for key, value in keys_to_add.items():
        if key not in processed_keys and value:
            new_content.append(f"{key}={value}")
    
    env_path.write_text('\n'.join(new_content))
    
    print("✅ Keys saved to .env\n")
    
    # Summary
    print_header("📊 Summary")
    for key, value in keys_to_add.items():
        if value:
            masked = value[:10] + "..." if len(value) > 10 else value
            print(f"  ✅ {key}: {masked}")
        else:
            print(f"  ⏭️  {key}: skipped")
    
    # Validate
    print_header("🔍 Validating keys")
    print("Run this to test all your keys:")
    print("\n  python scripts/validate_keys.py\n")
    
    response = input("Run validation now? (y/n): ").lower()
    if response == 'y':
        os.system("python scripts/validate_keys.py")

if __name__ == "__main__":
    main()
