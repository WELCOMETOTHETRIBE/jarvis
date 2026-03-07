#!/usr/bin/env python3
"""Validate that all API keys are working"""

import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import httpx

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

class KeyValidator:
    def __init__(self):
        self.passed = []
        self.failed = []
    
    def test_groq(self):
        """Test Groq API key"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            self.failed.append("GROQ_API_KEY - not set")
            return
        
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = httpx.get(
                "https://api.groq.com/openai/v1/models",
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                self.passed.append("✅ GROQ_API_KEY - valid")
            else:
                self.failed.append(f"GROQ_API_KEY - invalid (status {response.status_code})")
        except Exception as e:
            self.failed.append(f"GROQ_API_KEY - error: {str(e)}")
    
    def test_tavily(self):
        """Test Tavily API key"""
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            self.failed.append("TAVILY_API_KEY - not set")
            return
        
        try:
            payload = {
                "api_key": api_key,
                "query": "test",
                "max_results": 1
            }
            response = httpx.post(
                "https://api.tavily.com/search",
                json=payload,
                timeout=5
            )
            if response.status_code == 200:
                self.passed.append("✅ TAVILY_API_KEY - valid")
            else:
                self.failed.append(f"TAVILY_API_KEY - invalid (status {response.status_code})")
        except Exception as e:
            self.failed.append(f"TAVILY_API_KEY - error: {str(e)}")
    
    def test_github(self):
        """Test GitHub token"""
        token = os.getenv("GITHUB_TOKEN")
        if not token:
            self.failed.append("GITHUB_TOKEN - not set")
            return
        
        try:
            headers = {"Authorization": f"token {token}"}
            response = httpx.get(
                "https://api.github.com/user",
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                user = response.json()
                self.passed.append(f"✅ GITHUB_TOKEN - valid (user: {user.get('login', 'unknown')})")
            else:
                self.failed.append(f"GITHUB_TOKEN - invalid (status {response.status_code})")
        except Exception as e:
            self.failed.append(f"GITHUB_TOKEN - error: {str(e)}")
    
    def test_replicate(self):
        """Test Replicate API key"""
        api_key = os.getenv("REPLICATE_API_KEY")
        if not api_key:
            self.failed.append("REPLICATE_API_KEY - not set")
            return
        
        try:
            headers = {"Authorization": f"Token {api_key}"}
            response = httpx.get(
                "https://api.replicate.com/v1/account",
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                self.passed.append("✅ REPLICATE_API_KEY - valid")
            else:
                self.failed.append(f"REPLICATE_API_KEY - invalid (status {response.status_code})")
        except Exception as e:
            self.failed.append(f"REPLICATE_API_KEY - error: {str(e)}")
    
    def test_huggingface(self):
        """Test HuggingFace API key"""
        api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            self.failed.append("HUGGINGFACE_API_KEY - not set")
            return
        
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = httpx.get(
                "https://huggingface.co/api/whoami",
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                self.passed.append("✅ HUGGINGFACE_API_KEY - valid")
            else:
                self.failed.append(f"HUGGINGFACE_API_KEY - invalid (status {response.status_code})")
        except Exception as e:
            self.failed.append(f"HUGGINGFACE_API_KEY - error: {str(e)}")
    
    def test_anthropic(self):
        """Test Anthropic API key"""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            return  # Optional
        
        try:
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            }
            response = httpx.get(
                "https://api.anthropic.com/v1/models",
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                self.passed.append("✅ ANTHROPIC_API_KEY - valid")
            else:
                self.failed.append(f"ANTHROPIC_API_KEY - invalid (status {response.status_code})")
        except Exception as e:
            self.failed.append(f"ANTHROPIC_API_KEY - error: {str(e)}")
    
    def test_elevenlabs(self):
        """Test ElevenLabs API key"""
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            return  # Optional
        
        try:
            headers = {"xi-api-key": api_key}
            response = httpx.get(
                "https://api.elevenlabs.io/v1/voices",
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                self.passed.append("✅ ELEVENLABS_API_KEY - valid")
            else:
                self.failed.append(f"ELEVENLABS_API_KEY - invalid (status {response.status_code})")
        except Exception as e:
            self.failed.append(f"ELEVENLABS_API_KEY - error: {str(e)}")
    
    def test_klingai(self):
        """Test KlingAI API key"""
        api_key = os.getenv("KLINGAI_API_KEY")
        if not api_key:
            return  # optional
        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = httpx.get(
                "https://api.klingai.com/v1/status",
                headers=headers,
                timeout=5
            )
            if response.status_code == 200:
                self.passed.append("✅ KLINGAI_API_KEY - valid")
            else:
                self.failed.append(f"KLINGAI_API_KEY - invalid (status {response.status_code})")
        except Exception as e:
            self.failed.append(f"KLINGAI_API_KEY - error: {str(e)}")
    
    def run_all(self):
        """Run all tests"""
        print("\n🔍 Validating API Keys...\n")
        
        self.test_groq()
        self.test_tavily()
        self.test_github()
        self.test_replicate()
        self.test_huggingface()
        self.test_anthropic()
        self.test_elevenlabs()
        self.test_klingai()
        self.test_huggingface()
        self.test_anthropic()
        self.test_elevenlabs()
        
        # Print results
        for msg in self.passed:
            print(msg)
        
        for msg in self.failed:
            print(f"❌ {msg}")
        
        # Summary
        print(f"\n{'='*50}")
        print(f"✅ Passed: {len(self.passed)}")
        print(f"❌ Failed: {len(self.failed)}")
        print(f"{'='*50}\n")
        
        return len(self.failed) == 0

if __name__ == "__main__":
    validator = KeyValidator()
    success = validator.run_all()
    sys.exit(0 if success else 1)
