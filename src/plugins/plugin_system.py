"""
Plugin System for Shapeshifter RAG

This module provides a flexible plugin architecture for extending
the Shapeshifter application with custom functionality.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Type
import importlib
import inspect
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Plugin(ABC):
    """Base class for all plugins"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize plugin with configuration
        
        Args:
            config: Plugin-specific configuration dictionary
        """
        self.config = config or {}
        self.name = self.__class__.__name__
        self.enabled = True
        self.logger = logging.getLogger(f"plugin.{self.name}")
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the plugin
        
        Returns:
            True if initialization successful, False otherwise
        """
        pass
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute plugin functionality
        
        Args:
            context: Execution context with input data
            
        Returns:
            Result dictionary with output data
        """
        pass
    
    def cleanup(self) -> None:
        """Cleanup plugin resources"""
        pass
    
    @property
    def metadata(self) -> Dict[str, Any]:
        """
        Get plugin metadata
        
        Returns:
            Dictionary with plugin information
        """
        return {
            "name": self.name,
            "version": getattr(self, "VERSION", "1.0.0"),
            "description": getattr(self, "DESCRIPTION", ""),
            "author": getattr(self, "AUTHOR", ""),
            "enabled": self.enabled
        }


class RetrievalPlugin(Plugin):
    """Base class for retrieval plugins"""
    
    PLUGIN_TYPE = "retrieval"
    
    @abstractmethod
    def retrieve(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for query
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of retrieved documents
        """
        pass
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute retrieval"""
        query = context.get("query", "")
        top_k = context.get("top_k", 10)
        
        results = self.retrieve(query, top_k)
        
        return {
            "results": results,
            "count": len(results),
            "plugin": self.name
        }


class ProcessingPlugin(Plugin):
    """Base class for document processing plugins"""
    
    PLUGIN_TYPE = "processing"
    
    @abstractmethod
    def process(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a document
        
        Args:
            document: Document to process
            
        Returns:
            Processed document
        """
        pass
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute processing"""
        document = context.get("document", {})
        
        processed = self.process(document)
        
        return {
            "document": processed,
            "plugin": self.name
        }


class GenerationPlugin(Plugin):
    """Base class for generation plugins"""
    
    PLUGIN_TYPE = "generation"
    
    @abstractmethod
    def generate(self, prompt: str, context: List[str]) -> str:
        """
        Generate response
        
        Args:
            prompt: User prompt
            context: Context documents
            
        Returns:
            Generated response
        """
        pass
    
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute generation"""
        prompt = context.get("prompt", "")
        ctx = context.get("context", [])
        
        response = self.generate(prompt, ctx)
        
        return {
            "response": response,
            "plugin": self.name
        }


class PluginManager:
    """Manages plugin lifecycle and execution"""
    
    def __init__(self, plugin_dir: str = "plugins"):
        """
        Initialize plugin manager
        
        Args:
            plugin_dir: Directory containing plugins
        """
        self.plugin_dir = Path(plugin_dir)
        self.plugins: Dict[str, Plugin] = {}
        self.plugin_types: Dict[str, List[str]] = {}
        self.logger = logging.getLogger("PluginManager")
    
    def load_plugin(self, plugin_class: Type[Plugin], config: Dict[str, Any] = None) -> bool:
        """
        Load a plugin class
        
        Args:
            plugin_class: Plugin class to load
            config: Plugin configuration
            
        Returns:
            True if loaded successfully
        """
        try:
            # Instantiate plugin
            plugin = plugin_class(config)
            
            # Initialize plugin
            if not plugin.initialize():
                self.logger.error(f"Failed to initialize plugin: {plugin.name}")
                return False
            
            # Register plugin
            self.plugins[plugin.name] = plugin
            
            # Track by type
            plugin_type = getattr(plugin, "PLUGIN_TYPE", "general")
            if plugin_type not in self.plugin_types:
                self.plugin_types[plugin_type] = []
            self.plugin_types[plugin_type].append(plugin.name)
            
            self.logger.info(f"Loaded plugin: {plugin.name} (type: {plugin_type})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error loading plugin {plugin_class.__name__}: {e}")
            return False
    
    def discover_plugins(self) -> int:
        """
        Discover and load plugins from plugin directory
        
        Returns:
            Number of plugins loaded
        """
        if not self.plugin_dir.exists():
            self.logger.warning(f"Plugin directory not found: {self.plugin_dir}")
            return 0
        
        loaded_count = 0
        
        for plugin_file in self.plugin_dir.glob("*.py"):
            if plugin_file.name.startswith("_"):
                continue
            
            try:
                # Import module
                module_name = plugin_file.stem
                spec = importlib.util.spec_from_file_location(module_name, plugin_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find Plugin subclasses
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, Plugin) and obj != Plugin:
                        if self.load_plugin(obj):
                            loaded_count += 1
                            
            except Exception as e:
                self.logger.error(f"Error discovering plugins in {plugin_file}: {e}")
        
        self.logger.info(f"Discovered {loaded_count} plugins")
        return loaded_count
    
    def get_plugin(self, name: str) -> Optional[Plugin]:
        """Get plugin by name"""
        return self.plugins.get(name)
    
    def get_plugins_by_type(self, plugin_type: str) -> List[Plugin]:
        """Get all plugins of a specific type"""
        plugin_names = self.plugin_types.get(plugin_type, [])
        return [self.plugins[name] for name in plugin_names if name in self.plugins]
    
    def execute_plugin(self, name: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Execute a plugin
        
        Args:
            name: Plugin name
            context: Execution context
            
        Returns:
            Plugin execution result or None if failed
        """
        plugin = self.get_plugin(name)
        if not plugin:
            self.logger.error(f"Plugin not found: {name}")
            return None
        
        if not plugin.enabled:
            self.logger.warning(f"Plugin disabled: {name}")
            return None
        
        try:
            result = plugin.execute(context)
            return result
        except Exception as e:
            self.logger.error(f"Error executing plugin {name}: {e}")
            return None
    
    def execute_pipeline(self, plugin_names: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute multiple plugins in sequence
        
        Args:
            plugin_names: List of plugin names to execute
            context: Initial context
            
        Returns:
            Final context after all plugins
        """
        current_context = context.copy()
        results = []
        
        for name in plugin_names:
            result = self.execute_plugin(name, current_context)
            if result:
                results.append(result)
                # Update context with results
                current_context.update(result)
        
        return {
            "context": current_context,
            "pipeline_results": results
        }
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins with metadata"""
        return [plugin.metadata for plugin in self.plugins.values()]
    
    def enable_plugin(self, name: str) -> bool:
        """Enable a plugin"""
        plugin = self.get_plugin(name)
        if plugin:
            plugin.enabled = True
            self.logger.info(f"Enabled plugin: {name}")
            return True
        return False
    
    def disable_plugin(self, name: str) -> bool:
        """Disable a plugin"""
        plugin = self.get_plugin(name)
        if plugin:
            plugin.enabled = False
            self.logger.info(f"Disabled plugin: {name}")
            return True
        return False
    
    def unload_plugin(self, name: str) -> bool:
        """Unload a plugin"""
        plugin = self.get_plugin(name)
        if plugin:
            plugin.cleanup()
            del self.plugins[name]
            
            # Remove from type tracking
            for plugin_type, names in self.plugin_types.items():
                if name in names:
                    names.remove(name)
            
            self.logger.info(f"Unloaded plugin: {name}")
            return True
        return False
    
    def cleanup(self) -> None:
        """Cleanup all plugins"""
        for plugin in self.plugins.values():
            try:
                plugin.cleanup()
            except Exception as e:
                self.logger.error(f"Error cleaning up plugin {plugin.name}: {e}")
        
        self.plugins.clear()
        self.plugin_types.clear()
