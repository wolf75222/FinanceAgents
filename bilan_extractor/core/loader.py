"""
Module for loading financial statement files.
"""
from pathlib import Path


def load_bilan(filepath: str) -> str:
    """
    Load a financial statement file and return its content as text.
    
    Args:
        filepath: Path to the financial statement file
        
    Returns:
        The content of the file as a string
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Fichier non trouvé : {filepath}")
    return path.read_text(encoding="utf-8")