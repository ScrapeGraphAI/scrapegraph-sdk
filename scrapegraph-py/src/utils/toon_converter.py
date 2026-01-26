"""
TOON format conversion utilities.

This module provides utilities to convert API responses to TOON format,
which reduces token usage by 30-60% compared to JSON.
"""
from typing import Any, Dict, Optional

try:
    from toon import encode as toon_encode
    TOON_AVAILABLE = True
except ImportError:
    TOON_AVAILABLE = False
    toon_encode = None


def convert_to_toon(data: Any, options: Optional[Dict[str, Any]] = None) -> str:
    """
    Convert data to TOON format.
    
    Args:
        data: Python dict or list to convert to TOON format
        options: Optional encoding options for TOON
            - delimiter: 'comma' (default), 'tab', or 'pipe'
            - indent: Number of spaces per level (default: 2)
            - key_folding: 'off' (default) or 'safe'
            - flatten_depth: Max depth for key folding (default: None)
    
    Returns:
        TOON formatted string
        
    Raises:
        ImportError: If toonify library is not installed
    """
    if not TOON_AVAILABLE or toon_encode is None:
        raise ImportError(
            "toonify library is not installed. "
            "Install it with: pip install toonify"
        )
    
    return toon_encode(data, options=options)


def process_response_with_toon(response: Dict[str, Any], return_toon: bool = False) -> Any:
    """
    Process API response and optionally convert to TOON format.
    
    Args:
        response: The API response dictionary
        return_toon: If True, convert the response to TOON format
        
    Returns:
        Either the original response dict or TOON formatted string
    """
    if not return_toon:
        return response
    
    # Convert the response to TOON format
    return convert_to_toon(response)

