"""Basic tests"""

import pytest
from app.core.config import Config
from app.core.paths import Paths
from app.workspaces.manager import WorkspaceManager

def test_config():
    config = Config()
    assert config.data_dir.exists()

def test_paths():
    config = Config()
    paths = Paths(config)
    assert paths.data.exists()
    assert paths.workspaces.exists()

def test_workspace_manager():
    config = Config()
    paths = Paths(config)
    manager = WorkspaceManager(paths)
    workspaces = manager.list_workspaces()
    assert isinstance(workspaces, list)
    assert "general" in workspaces