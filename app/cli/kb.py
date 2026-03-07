"""KB commands"""

from rich.console import Console
from app.kb.search import KBSearch
from app.core.config import Config
from app.core.paths import Paths

console = Console()

def kb_search_command(query: str):
    """Search knowledge base"""
    config = Config()
    paths = Paths(config)
    kb_search = KBSearch(paths)

    results = kb_search.search(query)
    if results:
        for result in results:
            console.print(f"[bold]{result.title}[/bold] (Score: {result.score:.2f})")
            console.print(result.content)
            console.print()
    else:
        console.print("No results found")