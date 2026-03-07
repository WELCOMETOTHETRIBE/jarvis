"""Configuration management"""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel
import dotenv

dotenv.load_dotenv()

class Config(BaseModel):
    """Application configuration"""

    # API Keys
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    klingai_api_key: Optional[str] = os.getenv("KLINGAI_API_KEY")  # KlingAI service key

    # Paths
    root_path: Path = Path.cwd()
    data_dir: Path = Path("data")
    db_path: Path = Path("data/db/jarvis.db")

    # Defaults
    default_workspace: str = "general"
    default_model: str = "gpt-4"
    default_voice: str = "Sarah"

    def __init__(self, **data):
        super().__init__(**data)
        # Make paths absolute
        if not self.data_dir.is_absolute():
            self.data_dir = self.root_path / self.data_dir
        if not self.db_path.is_absolute():
            self.db_path = self.root_path / self.db_path

        # Ensure data directory exists
        self.data_dir.mkdir(exist_ok=True)
        self.db_path.parent.mkdir(exist_ok=True)
        
        # Load saved user preferences
        import json
        config_file = self.data_dir / "config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    if "default_voice" in user_config:
                        self.default_voice = user_config["default_voice"]
            except:
                pass  # Ignore config load errors