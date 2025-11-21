"""
Plugin Management API Endpoints
"""

from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Any, List
from pydantic import BaseModel

from src.plugins import PluginManager

router = APIRouter(prefix="/plugins", tags=["plugins"])

# Global plugin manager instance
plugin_manager = PluginManager(plugin_dir="plugins")


class PluginExecuteRequest(BaseModel):
    """Request model for plugin execution"""
    plugin_name: str
    context: Dict[str, Any]


class PluginPipelineRequest(BaseModel):
    """Request model for plugin pipeline execution"""
    plugin_names: List[str]
    context: Dict[str, Any]


class PluginConfigRequest(BaseModel):
    """Request model for plugin configuration"""
    enabled: bool


@router.on_event("startup")
async def startup_plugins():
    """Load plugins on startup"""
    count = plugin_manager.discover_plugins()
    print(f"Loaded {count} plugins")


@router.on_event("shutdown")
async def shutdown_plugins():
    """Cleanup plugins on shutdown"""
    plugin_manager.cleanup()


@router.get("/")
async def list_plugins() -> List[Dict[str, Any]]:
    """
    List all available plugins
    
    Returns:
        List of plugin metadata
    """
    return plugin_manager.list_plugins()


@router.get("/{plugin_name}")
async def get_plugin(plugin_name: str) -> Dict[str, Any]:
    """
    Get information about a specific plugin
    
    Args:
        plugin_name: Name of the plugin
        
    Returns:
        Plugin metadata
        
    Raises:
        HTTPException: If plugin not found
    """
    plugin = plugin_manager.get_plugin(plugin_name)
    if not plugin:
        raise HTTPException(status_code=404, detail=f"Plugin not found: {plugin_name}")
    
    return plugin.metadata


@router.get("/type/{plugin_type}")
async def get_plugins_by_type(plugin_type: str) -> List[Dict[str, Any]]:
    """
    Get all plugins of a specific type
    
    Args:
        plugin_type: Type of plugins to retrieve
        
    Returns:
        List of plugin metadata
    """
    plugins = plugin_manager.get_plugins_by_type(plugin_type)
    return [p.metadata for p in plugins]


@router.post("/execute")
async def execute_plugin(request: PluginExecuteRequest) -> Dict[str, Any]:
    """
    Execute a single plugin
    
    Args:
        request: Plugin execution request
        
    Returns:
        Plugin execution result
        
    Raises:
        HTTPException: If plugin execution fails
    """
    result = plugin_manager.execute_plugin(request.plugin_name, request.context)
    if result is None:
        raise HTTPException(
            status_code=500,
            detail=f"Plugin execution failed: {request.plugin_name}"
        )
    
    return result


@router.post("/pipeline")
async def execute_pipeline(request: PluginPipelineRequest) -> Dict[str, Any]:
    """
    Execute a pipeline of plugins
    
    Args:
        request: Pipeline execution request
        
    Returns:
        Pipeline execution result
    """
    result = plugin_manager.execute_pipeline(request.plugin_names, request.context)
    return result


@router.put("/{plugin_name}/enable")
async def enable_plugin(plugin_name: str) -> Dict[str, str]:
    """
    Enable a plugin
    
    Args:
        plugin_name: Name of the plugin
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If plugin not found
    """
    success = plugin_manager.enable_plugin(plugin_name)
    if not success:
        raise HTTPException(status_code=404, detail=f"Plugin not found: {plugin_name}")
    
    return {"message": f"Plugin enabled: {plugin_name}"}


@router.put("/{plugin_name}/disable")
async def disable_plugin(plugin_name: str) -> Dict[str, str]:
    """
    Disable a plugin
    
    Args:
        plugin_name: Name of the plugin
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If plugin not found
    """
    success = plugin_manager.disable_plugin(plugin_name)
    if not success:
        raise HTTPException(status_code=404, detail=f"Plugin not found: {plugin_name}")
    
    return {"message": f"Plugin disabled: {plugin_name}"}


@router.delete("/{plugin_name}")
async def unload_plugin(plugin_name: str) -> Dict[str, str]:
    """
    Unload a plugin
    
    Args:
        plugin_name: Name of the plugin
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If plugin not found
    """
    success = plugin_manager.unload_plugin(plugin_name)
    if not success:
        raise HTTPException(status_code=404, detail=f"Plugin not found: {plugin_name}")
    
    return {"message": f"Plugin unloaded: {plugin_name}"}


@router.post("/reload")
async def reload_plugins() -> Dict[str, Any]:
    """
    Reload all plugins from plugin directory
    
    Returns:
        Number of plugins loaded
    """
    # Cleanup existing plugins
    plugin_manager.cleanup()
    
    # Discover and load plugins
    count = plugin_manager.discover_plugins()
    
    return {
        "message": "Plugins reloaded",
        "count": count,
        "plugins": plugin_manager.list_plugins()
    }
