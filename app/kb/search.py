"""Knowledge base search"""

from typing import List, Optional
from app.core.models import KBResult
from app.core.paths import Paths

class KBSearch:
    """Knowledge base search functionality"""

    def __init__(self, paths: Paths):
        self.paths = paths

    def search(self, query: str, workspace: Optional[str] = None, limit: int = 10) -> List[KBResult]:
        """Search knowledge base"""
        # TODO: Implement proper search with embeddings/vector search
        # For now, return mock results
        return [
            KBResult(
                title="Sample Document",
                content=f"Mock result for query: {query}",
                source="sample.md",
                score=0.8
            )
        ]