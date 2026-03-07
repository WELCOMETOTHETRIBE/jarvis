"""Workspace management"""

import yaml
from pathlib import Path
from typing import List, Optional
from app.core.models import WorkspaceConfig
from app.core.paths import Paths

class WorkspaceManager:
    """Manages workspaces"""

    def __init__(self, paths: Paths):
        self.paths = paths

    def list_workspaces(self) -> List[str]:
        """List available workspaces"""
        workspace_dir = self.paths.workspaces
        if not workspace_dir.exists():
            return []
        return [d.name for d in workspace_dir.iterdir() if d.is_dir()]

    def get_workspace(self, slug: str) -> Optional[WorkspaceConfig]:
        """Get workspace configuration"""
        config_path = self.paths.workspaces / slug / "workspace.yaml"
        if not config_path.exists():
            return None

        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)

        # Load system prompt
        system_path = self.paths.workspaces / slug / "system.md"
        system_prompt = ""
        if system_path.exists():
            with open(system_path, 'r') as f:
                system_prompt = f.read()

        data['system_prompt'] = system_prompt
        return WorkspaceConfig(**data)

    def create_workspace(self, config: WorkspaceConfig):
        """Create a new workspace"""
        workspace_dir = self.paths.workspaces / config.slug
        workspace_dir.mkdir(exist_ok=True)

        # Save config
        config_path = workspace_dir / "workspace.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(config.model_dump(exclude={'system_prompt'}), f)

        # Save system prompt
        if hasattr(config, 'system_prompt') and config.system_prompt:
            system_path = workspace_dir / "system.md"
            with open(system_path, 'w') as f:
                f.write(config.system_prompt)