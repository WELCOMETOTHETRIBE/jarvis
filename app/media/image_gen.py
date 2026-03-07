"""Image generation using OpenAI DALL-E"""

import httpx
import os
from pathlib import Path
from typing import Optional
from app.core.config import Config
from app.core.paths import Paths

class ImageGenerator:
    """Generate images using OpenAI DALL-E"""

    def __init__(self, config: Config, paths: Paths):
        self.config = config
        self.paths = paths
        self.api_key = config.openai_api_key
        self.base_url = "https://api.openai.com/v1"
        self.client = httpx.Client(
            headers={"Authorization": f"Bearer {self.api_key}"},
            timeout=60.0
        )

    def generate_image(
        self,
        prompt: str,
        model: str = "dall-e-3",
        size: str = "1024x1024",
        quality: str = "standard",
        output_path: Optional[Path] = None
    ) -> Path:
        """Generate an image from text prompt

        The `model` argument may be either the OpenAI model name (e.g. "dall-e-3")
        or the string "replicate". If "replicate" is selected the method will
        call the Replicate API instead of OpenAI.  We treat the value as a plain
        string for backwards compatibility with existing callers.
        """

        # allow callers to pass an enum value
        if not isinstance(model, str):
            model = str(model)

        # Replicate path -----------------------------------------------------
        if model.lower() == "replicate":
            # simple wrapper around Replicate predictions API
            api_key = os.getenv("REPLICATE_API_KEY")
            if not api_key:
                raise ValueError("Replicate API key not configured")

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                # wait synchronously up to 60 seconds
                "Prefer": "wait=60"
            }

            # determine version id dynamically to avoid 422 errors
            # query the model metadata and use its latest_version id
            try:
                info = httpx.get("https://api.replicate.com/v1/models/stability-ai/stable-diffusion",
                                  headers=headers,
                                  timeout=30.0)
                info.raise_for_status()
                version_id = info.json().get("latest_version", {}).get("id")
            except Exception as e:
                raise ValueError(f"Failed to query Replicate model info: {e}")

            if not version_id:
                raise ValueError("Could not determine a Replicate version id for stable-diffusion")

            payload = {
                "version": version_id,
                "input": {"prompt": prompt}
            }

            resp = httpx.post("https://api.replicate.com/v1/predictions",
                              json=payload,
                              headers=headers,
                              timeout=120.0)
            resp.raise_for_status()
            data = resp.json()

            # replicate returns output field which may be list or single url
            output_field = data.get("output")
            if not output_field:
                raise ValueError("No output from Replicate API")

            image_url = output_field[0] if isinstance(output_field, list) else output_field

            # download the image
            image_client = httpx.Client(timeout=120.0)
            image_response = image_client.get(image_url)
            image_response.raise_for_status()

            if not output_path:
                images_dir = self.paths.data / "images"
                images_dir.mkdir(exist_ok=True)
                import time
                output_path = images_dir / f"generated_{int(time.time() * 1000000)}.png"

            with open(output_path, 'wb') as f:
                f.write(image_response.content)

            return output_path

        # Default: OpenAI path ------------------------------------------------
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")

        payload = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "n": 1
        }

        response = self.client.post(f"{self.base_url}/images/generations", json=payload)
        response.raise_for_status()

        data = response.json()
        
        # Check if the response contains an error
        if "error" in data:
            raise ValueError(f"OpenAI API error: {data['error']['message']}")
        
        if "data" not in data or not data["data"]:
            raise ValueError("Invalid response from OpenAI API")
            
        image_url = data["data"][0]["url"]

        # Download the image immediately
        if not output_path:
            images_dir = self.paths.data / "images"
            images_dir.mkdir(exist_ok=True)
            import time
            output_path = images_dir / f"generated_{int(time.time() * 1000000)}.png"

        # Download and save immediately after getting the URL
        # Note: Image URLs from OpenAI are publicly accessible, so we don't need auth headers
        image_client = httpx.Client(timeout=60.0)
        image_response = image_client.get(image_url)
        image_response.raise_for_status()
        
        # Check if we got image data
        if not image_response.content:
            raise ValueError("Empty image data received")
            
        with open(output_path, 'wb') as f:
            f.write(image_response.content)

        return output_path

    def edit_image(
        self,
        image_path: Path,
        prompt: str,
        mask_path: Optional[Path] = None,
        model: str = "dall-e-2",
        output_path: Optional[Path] = None
    ) -> Path:
        """Edit an existing image"""

        if not self.api_key:
            raise ValueError("OpenAI API key not configured")

        if not output_path:
            images_dir = self.paths.data / "images"
            images_dir.mkdir(exist_ok=True)
            output_path = images_dir / f"edited_{image_path.stem}.png"

        # For editing, we need to upload the image first
        # This is a simplified version - full implementation would handle image uploads
        raise NotImplementedError("Image editing not yet implemented")

        return output_path