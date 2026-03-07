"""ElevenLabs Text-to-Speech"""

import httpx
import os
from pathlib import Path
from typing import Optional
from app.core.config import Config
from app.core.paths import Paths

class ElevenLabsTTS:
    """Convert text to speech using ElevenLabs"""

    FREE_VOICES = {
        "Sarah": "EXAVITQu4vr4xnSDxMaL",
        "Laura": "FGY2WhTYpPnrIDTdsKH5",
        "Charlie": "IKne3meq5aSn9XLyUdCD",
        "George": "JBFqnCBsd6RMkjVDRZzb",
        "River": "SAz9YHcvj6GT2YYXdXww",
        "Alice": "Xb7hH8MSUJpSbSDYk0k2",
        "Matilda": "XrExE9yKIg1WjnnlVkGX",
        "Jessica": "cgSgspJ2msm6clMCkdW9",
        "Bella": "hpp4J3VqNfWAUOO0d1Us"
    }

    def __init__(self, config: Config, paths: Paths):
        self.config = config
        self.paths = paths
        
        # Get ElevenLabs API key from environment
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not configured in environment")
        
        self.base_url = "https://api.elevenlabs.io/v1"
        self.client = httpx.Client(
            headers={"xi-api-key": self.api_key},
            timeout=60.0
        )

    def generate_speech(
        self,
        text: str,
        voice: str = "Sarah",
        stability: float = 0.5,
        similarity_boost: float = 0.75,
        output_path: Optional[Path] = None
    ) -> Path:
        """Generate speech from text using ElevenLabs"""

        if not self.api_key:
            raise ValueError("ElevenLabs API key not configured")

        if voice not in self.FREE_VOICES:
            raise ValueError(f"Voice '{voice}' not found. Available: {', '.join(self.FREE_VOICES.keys())}")

        if not output_path:
            audio_dir = self.paths.data / "audio"
            audio_dir.mkdir(exist_ok=True)
            import time
            output_path = audio_dir / f"tts_el_{int(time.time() * 1000000)}.mp3"

        voice_id = self.FREE_VOICES[voice]
        
        # Use eleven_multilingual_v2 which is available on free tier
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost
            }
        }

        response = self.client.post(
            f"{self.base_url}/text-to-speech/{voice_id}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)

        return output_path

    @staticmethod
    def list_voices() -> list[str]:
        """List available ElevenLabs free voices"""
        return list(ElevenLabsTTS.FREE_VOICES.keys())
