"""
Module for logging functionality.
"""
import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logger(
    name: str = "bilan_extractor",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    Set up and configure a logger.
    
    Args:
        name: Name of the logger
        level: Logging level (default: logging.INFO)
        log_file: Optional path to a log file
        console_output: Whether to output logs to the console
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Add file handler if log_file is provided
    if log_file:
        log_path = Path(log_file)
        # Create directory if it doesn't exist
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Add console handler if console_output is True
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger


# Default logger instance
logger = setup_logger()