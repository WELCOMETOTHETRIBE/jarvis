"""Text-to-speech using OpenAI TTS"""

import httpx
from pathlib import Path
from typing import Optional
from app.core.config import Config
from app.core.paths import Paths

class TextToSpeech:
    """Convert text to speech using OpenAI TTS"""

    def __init__(self, config: Config, paths: Paths):
        self.config = config
        self.paths = paths
        self.api_key = config.openai_api_key
        self.base_url = "https://api.openai.com/v1"
        self.client = httpx.Client(
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=60.0
        )

    def generate_speech(
        self,
        text: str,
        voice: str = "alloy",
        model: str = "tts-1",
        output_path: Optional[Path] = None
    ) -> Path:
        """Generate speech from text"""

        if not self.api_key:
            raise ValueError("OpenAI API key not configured")

        if not output_path:
            audio_dir = self.paths.data / "audio"
            audio_dir.mkdir(exist_ok=True)
            import time
            output_path = audio_dir / f"tts_{int(time.time() * 1000000)}.mp3"

        payload = {
            "model": model,
            "input": text,
            "voice": voice
        }

        response = self.client.post(
            f"{self.base_url}/audio/speech",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()

        with open(output_path, 'wb') as f:
            f.write(response.content)

        return output_path

    def list_voices(self) -> dict:
        """List available voices from OpenAI TTS and ElevenLabs free tier"""
        return {
            "openai": ["alloy", "echo", "fable", "onyx", "nova", "shimmer"],
            "elevenlabs_free": [
                "Sarah",
                "Laura",
                "Charlie", 
                "George",
                "River",
                "Alice",
                "Matilda",
                "Jessica",
                "Bella"
            ]
        }