#!/usr/bin/env python3
"""Test OpenAI API key validity"""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

def test_api_key():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ OPENAI_API_KEY not set or using placeholder")
        print("Please set a valid OpenAI API key in your .env file")
        return False

    client = httpx.Client(
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=10.0
    )

    try:
        # Test with a simple models list call
        response = client.get("https://api.openai.com/v1/models")
        if response.status_code == 200:
            print("✅ API key is valid!")
            return True
        elif response.status_code == 401:
            print("❌ API key is invalid (401 Unauthorized)")
            return False
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        return False

if __name__ == "__main__":
    test_api_key()