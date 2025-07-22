"""
Module for application configuration settings.
"""
import os
from pathlib import Path
from typing import Dict, Any


# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Ollama settings
OLLAMA_SETTINGS = {
    "default_model": os.environ.get("OLLAMA_MODEL", "gemma3"),
    "host": os.environ.get("OLLAMA_HOST", "http://localhost:11434"),
}

# Docling settings
DOCLING_SETTINGS = {
    "disable_ssl_verification": os.environ.get("DISABLE_SSL_VERIFICATION", "").lower() in ("1", "true", "yes"),
}

# Logging settings
LOGGING_SETTINGS = {
    "level": "INFO",
    "log_file": str(BASE_DIR / "logs" / "bilan_extractor.log"),
    "console_output": True,
}

# Create logs directory if it doesn't exist
(BASE_DIR / "logs").mkdir(exist_ok=True)


def get_config() -> Dict[str, Any]:
    """
    Get the complete configuration as a dictionary.
    
    Returns:
        A dictionary containing all configuration settings
    """
    return {
        "base_dir": str(BASE_DIR),
        "data_dir": str(DATA_DIR),
        "output_dir": str(OUTPUT_DIR),
        "ollama": OLLAMA_SETTINGS,
        "docling": DOCLING_SETTINGS,
        "logging": LOGGING_SETTINGS,
    }