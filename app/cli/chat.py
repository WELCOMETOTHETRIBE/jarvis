"""Chat commands"""

from rich.console import Console
from app.core.config import Config
from app.core.paths import Paths
from app.workspaces.manager import WorkspaceManager
from app.llm.openai_provider import OpenAIProvider

console = Console()

def chat_command():
    """Interactive chat session"""
    console.print("[bold green]Jarvis Chat[/bold green]")
    console.print("Type 'exit' to quit\n")

    config = Config()
    paths = Paths(config)
    workspace_manager = WorkspaceManager(paths)
    provider = OpenAIProvider(config)

    while True:
        try:
            user_input = console.input("[bold blue]You:[/bold blue] ")
            if user_input.lower() in ['exit', 'quit']:
                break

            # TODO: Implement full chat logic
            response = provider.generate_text(user_input)
            console.print(f"[bold red]Jarvis:[/bold red] {response}")

        except KeyboardInterrupt:
            break

    console.print("\nGoodbye!")

def ask_command(question: str):
    """Single question command"""
    config = Config()
    provider = OpenAIProvider(config)

    try:
        response = provider.generate_text(question)
        console.print(response)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")