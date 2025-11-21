"""Plugin system for Shapeshifter RAG"""

from .plugin_system import (
    Plugin,
    RetrievalPlugin,
    ProcessingPlugin,
    GenerationPlugin,
    PluginManager
)

__all__ = [
    "Plugin",
    "RetrievalPlugin",
    "ProcessingPlugin",
    "GenerationPlugin",
    "PluginManager"
]
