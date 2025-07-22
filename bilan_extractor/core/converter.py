"""
Module for converting PDF financial statement files to Markdown format.
"""
import subprocess
from pathlib import Path


def convert_to_markdown(filepath: str) -> str:
    """
    Convert a PDF financial statement file to Markdown format using docling.
    
    Args:
        filepath: Path to the PDF financial statement file
        
    Returns:
        The content of the file in Markdown format
        
    Raises:
        subprocess.CalledProcessError: If the docling command fails
    """
    result = subprocess.run(['docling', 'parse', filepath], capture_output=True, text=True, check=True)
    return result.stdout