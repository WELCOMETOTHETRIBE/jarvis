"""Tests for environment variable overrides in Config"""

import os
from pathlib import Path

import pytest

from app.core.config import Config


def test_env_overrides(tmp_path, monkeypatch):
    # simulate a different root and data directory
    monkeypatch.setenv("ROOT_PATH", str(tmp_path / "root"))
    monkeypatch.setenv("DATA_DIR", "mydata")
    monkeypatch.setenv("DB_PATH", "mydata/db/test.db")
    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@localhost/db")

    cfg = Config()

    # root_path should equal tmp_path/root
    assert cfg.root_path == tmp_path / "root"
    # data_dir should be derived from root unless absolute
    assert cfg.data_dir == cfg.root_path / "mydata"
    assert cfg.db_path == cfg.root_path / "mydata/db/test.db"
    assert cfg.database_url == "postgresql://user:pass@localhost/db"

    # ensure directories are created
    assert (cfg.data_dir).exists()
    assert (cfg.db_path.parent).exists()
