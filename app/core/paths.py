"""Path management"""

from pathlib import Path
from app.core.config import Config

class Paths:
    """Centralized path management"""

    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.root = self.config.root_path
        self.data = self.config.data_dir
        self.db = self.config.db_path
        self.sessions = self.data / "sessions"
        self.workspaces = self.root / "workspaces"
        self.kb = self.data / "kb"

        # Ensure directories exist
        for path in [self.data, self.sessions, self.workspaces, self.kb]:
            path.mkdir(exist_ok=True)