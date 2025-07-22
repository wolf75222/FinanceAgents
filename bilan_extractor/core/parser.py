"""
Module for parsing and processing LLM output.

This module provides functions to parse and validate the output from the LLM.
It includes robust error handling to deal with various types of LLM responses,
including empty strings, non-JSON text, and JSON embedded in other text.
"""
import json
from typing import Dict, Any


def parse_llm_output(json_str: str) -> Dict[str, Any]:
    """
    Parse the JSON output from the LLM and convert it to a Python dictionary.
    
    Args:
        json_str: The JSON string output from the LLM
        
    Returns:
        A dictionary containing the extracted financial variables
        
    Raises:
        json.JSONDecodeError: If the JSON string is invalid and cannot be recovered
    """
    # Check if input is empty or whitespace-only
    if not json_str or json_str.isspace():
        # Return empty dictionary with expected keys
        return {
            "actif_total": None,
            "passif_total": None,
            "capitaux_propres": None,
            "résultat_net": None,
            "chiffre_affaires": None,
            "dettes": None
        }
    
    # Try to parse the JSON directly
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Try to extract JSON from the text
        # Look for dictionary-like patterns
        import re
        
        # Try to find content between curly braces
        dict_pattern = re.compile(r'\{.*\}', re.DOTALL)
        dict_match = dict_pattern.search(json_str)
        
        if dict_match:
            try:
                # Try to parse the extracted dictionary
                extracted_json = dict_match.group(0)
                return json.loads(extracted_json)
            except json.JSONDecodeError:
                # If still fails, continue to fallback
                pass
        
        # If all extraction attempts fail, return empty dictionary with expected keys
        return {
            "actif_total": None,
            "passif_total": None,
            "capitaux_propres": None,
            "résultat_net": None,
            "chiffre_affaires": None,
            "dettes": None
        }


def validate_financial_variables(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the financial variables extracted from the LLM.
    
    Args:
        data: The dictionary containing the extracted financial variables
        
    Returns:
        The validated dictionary with financial variables
    """
    expected_keys = [
        "actif_total", 
        "passif_total", 
        "capitaux_propres", 
        "résultat_net", 
        "chiffre_affaires", 
        "dettes"
    ]
    
    # Ensure all values are numeric
    for key, value in data.items():
        if key in expected_keys and value is not None:
            try:
                data[key] = float(value)
            except (ValueError, TypeError):
                # If conversion fails, keep the original value
                pass
    
    return data