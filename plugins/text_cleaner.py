"""
Example Document Processing Plugin

This demonstrates how to create a custom document processing plugin.
"""

from typing import Dict, Any
from src.plugins import ProcessingPlugin
import re


class TextCleanerPlugin(ProcessingPlugin):
    """Example plugin for cleaning and normalizing text"""
    
    VERSION = "1.0.0"
    DESCRIPTION = "Text cleaning and normalization plugin"
    AUTHOR = "Shapeshifter Team"
    
    def initialize(self) -> bool:
        """Initialize the plugin"""
        self.logger.info("Initializing TextCleanerPlugin")
        
        # Configuration options
        self.remove_special_chars = self.config.get("remove_special_chars", True)
        self.lowercase = self.config.get("lowercase", False)
        self.remove_extra_spaces = self.config.get("remove_extra_spaces", True)
        
        return True
    
    def process(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and normalize document text
        
        Args:
            document: Document to process
            
        Returns:
            Processed document
        """
        content = document.get("content", "")
        
        # Apply cleaning operations
        cleaned_content = content
        
        if self.remove_extra_spaces:
            # Remove extra whitespace
            cleaned_content = re.sub(r'\s+', ' ', cleaned_content)
            cleaned_content = cleaned_content.strip()
        
        if self.remove_special_chars:
            # Remove special characters except basic punctuation
            cleaned_content = re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', cleaned_content)
        
        if self.lowercase:
            cleaned_content = cleaned_content.lower()
        
        # Update document
        processed_doc = document.copy()
        processed_doc["content"] = cleaned_content
        processed_doc["metadata"] = processed_doc.get("metadata", {})
        processed_doc["metadata"]["processed_by"] = self.name
        processed_doc["metadata"]["original_length"] = len(content)
        processed_doc["metadata"]["cleaned_length"] = len(cleaned_content)
        
        return processed_doc
    
    def cleanup(self) -> None:
        """Cleanup resources"""
        self.logger.info("Cleaning up TextCleanerPlugin")
