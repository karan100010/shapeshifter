# Plugin System for Shapeshifter RAG

## Overview

The Shapeshifter plugin system provides a flexible architecture for extending the application with custom functionality without modifying core code.

## Features

- Modular plugin architecture
- Dynamic plugin loading and unloading
- Plugin lifecycle management
- Type-based plugin organization (retrieval, processing, generation)
- REST API for plugin management
- Configuration per plugin
- Plugin pipelines for chaining operations

## Plugin Types

### 1. Retrieval Plugins
Extend document retrieval capabilities with custom retrieval strategies.

**Base Class**: `RetrievalPlugin`

**Example Use Cases**:
- Custom search algorithms
- External data source integration
- Specialized domain-specific retrieval

### 2. Processing Plugins
Add custom document processing and transformation logic.

**Base Class**: `ProcessingPlugin`

**Example Use Cases**:
- Text cleaning and normalization
- Custom entity extraction
- Document format conversion
- Metadata enrichment

### 3. Generation Plugins
Implement custom response generation strategies.

**Base Class**: `GenerationPlugin`

**Example Use Cases**:
- Custom LLM integrations
- Template-based generation
- Domain-specific response formatting

## Creating a Plugin

### Step 1: Choose Base Class

```python
from src.plugins import RetrievalPlugin

class MyCustomPlugin(RetrievalPlugin):
    VERSION = "1.0.0"
    DESCRIPTION = "My custom retrieval plugin"
    AUTHOR = "Your Name"
```

### Step 2: Implement Required Methods

```python
def initialize(self) -> bool:
    """Initialize plugin resources"""
    self.logger.info("Initializing MyCustomPlugin")
    # Load models, connect to databases, etc.
    return True

def retrieve(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
    """Implement retrieval logic"""
    # Your custom retrieval code
    return results

def cleanup(self) -> None:
    """Cleanup resources"""
    # Close connections, free memory, etc.
    pass
```

### Step 3: Add Plugin to plugins/ Directory

Save your plugin file in the `plugins/` directory:
```
plugins/
  my_custom_plugin.py
```

### Step 4: Plugin Auto-Discovery

Plugins are automatically discovered on startup. You can also trigger reload:
```python
POST /plugins/reload
```

## Using Plugins

### Via Python API

```python
from src.plugins import PluginManager

# Initialize manager
manager = PluginManager(plugin_dir="plugins")

# Discover plugins
manager.discover_plugins()

# Execute single plugin
result = manager.execute_plugin("MyCustomPlugin", {
    "query": "search term",
    "top_k": 5
})

# Execute pipeline
result = manager.execute_pipeline(
    ["TextCleanerPlugin", "CustomRetrievalPlugin"],
    {"document": {"content": "text to process"}}
)
```

### Via REST API

#### List All Plugins
```bash
GET /plugins/
```

#### Get Plugin Details
```bash
GET /plugins/MyCustomPlugin
```

#### Execute Plugin
```bash
POST /plugins/execute
{
  "plugin_name": "MyCustomPlugin",
  "context": {
    "query": "search term",
    "top_k": 5
  }
}
```

#### Execute Pipeline
```bash
POST /plugins/pipeline
{
  "plugin_names": ["TextCleanerPlugin", "CustomRetrievalPlugin"],
  "context": {
    "document": {"content": "text"}
  }
}
```

#### Enable/Disable Plugin
```bash
PUT /plugins/MyCustomPlugin/enable
PUT /plugins/MyCustomPlugin/disable
```

#### Reload Plugins
```bash
POST /plugins/reload
```

## Example Plugins

### Custom Retrieval Plugin

See `plugins/custom_retrieval.py` for a complete example of keyword-based retrieval.

### Text Cleaner Plugin

See `plugins/text_cleaner.py` for a document processing example.

## Plugin Configuration

Plugins can accept configuration via the config dictionary:

```python
plugin = MyPlugin(config={
    "api_key": "...",
    "model_name": "...",
    "threshold": 0.5
})
```

Configuration can also be loaded from environment variables or config files.

## Plugin Lifecycle

1. **Discovery**: Plugins discovered from `plugins/` directory
2. **Instantiation**: Plugin class instantiated with configuration
3. **Initialization**: `initialize()` method called
4. **Registration**: Plugin registered in PluginManager
5. **Execution**: Plugin `execute()` method called on demand
6. **Cleanup**: `cleanup()` method called on shutdown or unload

## Best Practices

1. **Error Handling**: Implement robust error handling in all methods
2. **Logging**: Use `self.logger` for consistent logging
3. **Resource Management**: Clean up resources in `cleanup()`
4. **Configuration**: Use config dictionary for all configurable options
5. **Testing**: Write unit tests for your plugins
6. **Documentation**: Document plugin purpose, inputs, and outputs
7. **Versioning**: Use semantic versioning for your plugins

## Testing Plugins

Create tests for your plugins:

```python
import pytest
from plugins.my_custom_plugin import MyCustomPlugin

def test_plugin_initialization():
    plugin = MyCustomPlugin()
    assert plugin.initialize() == True

def test_plugin_execution():
    plugin = MyCustomPlugin()
    plugin.initialize()
    
    result = plugin.execute({"query": "test"})
    assert "results" in result
    
    plugin.cleanup()
```

## Troubleshooting

### Plugin Not Found
- Ensure plugin file is in `plugins/` directory
- Check plugin class inherits from correct base class
- Verify `initialize()` returns True
- Check logs for errors during discovery

### Plugin Execution Fails
- Check plugin is enabled: `plugin.enabled`
- Verify input context has required fields
- Check plugin logs for specific errors
- Test plugin independently before integration

### Performance Issues
- Profile plugin execution time
- Optimize resource-intensive operations
- Consider caching results
- Use async operations where appropriate

## Advanced Features

### Plugin Dependencies

Plugins can list dependencies:
```python
class MyPlugin(Plugin):
    DEPENDENCIES = ["numpy", "transformers"]
```

### Plugin Hooks

Plugins can register hooks for specific events:
```python
def on_document_upload(self, document):
    # Process new documents
    pass
```

### Plugin Pipelines

Chain multiple plugins:
```python
pipeline = ["CleanerPlugin", "ExtractorPlugin", "IndexerPlugin"]
manager.execute_pipeline(pipeline, context)
```

## API Reference

See [plugin_system.py](../src/plugins/plugin_system.py) for complete API documentation.

## Contributing

To contribute a plugin:
1. Create plugin following guidelines above
2. Add tests for your plugin
3. Document configuration options
4. Submit pull request with plugin in `plugins/` directory

## License

Plugin system is part of Shapeshifter RAG and follows the same license.
