"""Speech-to-text using OpenAI Whisper"""

import httpx
from pathlib import Path
from typing import Optional
from app.core.config import Config
from app.core.paths import Paths

class SpeechToText:
    """Convert speech to text using OpenAI Whisper"""

    def __init__(self, config: Config, paths: Paths):
        self.config = config
        self.paths = paths
        self.api_key = config.openai_api_key
        self.base_url = "https://api.openai.com/v1"
        self.client = httpx.Client(
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=60.0
        )

    def transcribe_audio(
        self,
        audio_path: Path,
        model: str = "whisper-1",
        language: Optional[str] = None,
        response_format: str = "text"
    ) -> str:
        """Transcribe audio file to text"""

        if not self.api_key:
            raise ValueError("OpenAI API key not configured")

        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        with open(audio_path, 'rb') as audio_file:
            files = {"file": (audio_path.name, audio_file, "audio/wav")}
            data = {
                "model": model,
                "response_format": response_format
            }

            if language:
                data["language"] = language

            response = self.client.post(
                f"{self.base_url}/audio/transcriptions",
                files=files,
                data=data
            )

        response.raise_for_status()
        return response.text.strip()

    def translate_audio(
        self,
        audio_path: Path,
        model: str = "whisper-1",
        response_format: str = "text"
    ) -> str:
        """Translate audio to English text"""

        if not self.api_key:
            raise ValueError("OpenAI API key not configured")

        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        with open(audio_path, 'rb') as audio_file:
            files = {"file": (audio_path.name, audio_file, "audio/wav")}
            data = {
                "model": model,
                "response_format": response_format
            }

            response = self.client.post(
                f"{self.base_url}/audio/translations",
                files=files,
                data=data
            )

        response.raise_for_status()
        return response.text.strip()