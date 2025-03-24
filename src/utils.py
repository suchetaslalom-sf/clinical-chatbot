import logging
import re
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent injection attacks.
    
    Args:
        text: The input text to sanitize
        
    Returns:
        Sanitized text
    """
    # Remove any potentially harmful characters or sequences
    sanitized = re.sub(r'[^\w\s.,?!:;()\[\]{}\'"-]', '', text)
    return sanitized

def format_markdown_response(text: str) -> str:
    """
    Format the response text with proper markdown.
    
    Args:
        text: The response text to format
        
    Returns:
        Formatted markdown text
    """
    # Add some basic markdown formatting improvements
    
    # Ensure proper spacing for headers
    text = re.sub(r'(?<!\n)#', '\n#', text)
    
    # Ensure proper spacing after lists
    text = re.sub(r'(\n\d+\..+)(\n[^\d*-])', r'\1\n\2', text)
    
    # Ensure code blocks are properly formatted
    text = re.sub(r'```(\w+)?\n?', r'```\1\n', text)
    text = re.sub(r'\n?```', r'\n```', text)
    
    return text

def parse_medical_entities(text: str) -> List[Dict[str, Any]]:
    """
    Parse medical entities from text using regex patterns.
    This is a simple implementation - a more robust solution would use
    a medical NER model or medical knowledge base.
    
    Args:
        text: The text to parse for medical entities
        
    Returns:
        List of extracted medical entities
    """
    entities = []
    
    # Example patterns for medical entities
    patterns = {
        "medication": r'\b[A-Z][a-z]*(?:mab|nib|zumab|ximab|limus|prazole|sartan|statin)\b',
        "condition": r'\b(?:diabetes|hypertension|asthma|cancer|depression|anxiety)\b',
        "procedure": r'\b(?:surgery|biopsy|transplant|resection|angioplasty)\b'
    }
    
    for entity_type, pattern in patterns.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            entities.append({
                "type": entity_type,
                "text": match.group(0),
                "start": match.start(),
                "end": match.end()
            })
    
    return entities

def get_medical_disclaimer() -> str:
    """
    Return a standard medical disclaimer.
    
    Returns:
        Medical disclaimer text
    """
    return """
    **Medical Disclaimer**: The information provided is for informational purposes only and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
    """