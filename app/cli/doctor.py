"""Doctor command for diagnostics"""

from rich.console import Console
from app.core.config import Config
from app.core.paths import Paths
from app.workspaces.manager import WorkspaceManager
import os

console = Console()

def doctor_command():
    """Run system diagnostics"""
    console.print("[bold green]Jarvis System Diagnostics[/bold green]\n")

    config = Config()
    paths = Paths(config)

    # Check API keys
    if config.openai_api_key:
        console.print("✅ OpenAI API key configured")
    else:
        console.print("❌ OpenAI API key not found")

    # KlingAI key (optional)
    if os.getenv("KLINGAI_API_KEY"):
        console.print("✅ KlingAI API key configured")


    # Check directories
    required_dirs = [
        paths.data,
        paths.db.parent,
        paths.sessions,
        paths.workspaces
    ]

    for dir_path in required_dirs:
        if dir_path.exists():
            console.print(f"✅ Directory exists: {dir_path}")
        else:
            console.print(f"❌ Missing directory: {dir_path}")

    # Check workspaces
    workspace_manager = WorkspaceManager(paths)
    workspaces = workspace_manager.list_workspaces()
    if workspaces:
        console.print(f"✅ Found {len(workspaces)} workspace(s): {', '.join(workspaces)}")
    else:
        console.print("❌ No workspaces found")

    console.print("\n[bold]System ready![/bold]")