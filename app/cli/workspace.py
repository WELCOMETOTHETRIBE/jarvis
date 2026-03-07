"""Workspace commands"""

from rich.console import Console
from app.workspaces.manager import WorkspaceManager
from app.core.config import Config
from app.core.paths import Paths

console = Console()

def workspace_command(command: str, name: str = None):
    """Workspace management"""
    config = Config()
    paths = Paths(config)
    manager = WorkspaceManager(paths)

    if command == "list":
        workspaces = manager.list_workspaces()
        if workspaces:
            console.print("Available workspaces:")
            for ws in workspaces:
                console.print(f"  - {ws}")
        else:
            console.print("No workspaces found")

    elif command == "use" and name:
        workspace = manager.get_workspace(name)
        if workspace:
            console.print(f"Switched to workspace: {workspace.name}")
            # TODO: Set active workspace
        else:
            console.print(f"[red]Workspace '{name}' not found[/red]")

    else:
        console.print("Usage: jarvis workspace list | jarvis workspace use <name>")