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
        return {}
    
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
        
        # If all extraction attempts fail, return empty dictionary
        return {}


def validate_financial_variables(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the financial variables extracted from the LLM.
    
    Args:
        data: The dictionary containing the extracted financial variables
        
    Returns:
        The validated dictionary with financial variables
    """
    # Process each variable
    for var_name, var_data in list(data.items()):
        # Skip if not a dictionary
        if not isinstance(var_data, dict):
            continue
            
        # Handle new format with values list
        if "values" in var_data and isinstance(var_data["values"], list):
            # Validate each value in the list
            for i, value_data in enumerate(var_data["values"]):
                if isinstance(value_data, dict) and "value" in value_data:
                    try:
                        # Convert value to float
                        var_data["values"][i]["value"] = float(value_data["value"])
                    except (ValueError, TypeError):
                        # If conversion fails, remove this value
                        var_data["values"][i]["value"] = None
            
            # Remove values with None
            var_data["values"] = [v for v in var_data["values"] if v.get("value") is not None]
            
            # If no valid values, remove the variable
            if not var_data["values"]:
                del data[var_name]
        
        # Handle legacy format (direct value)
        elif "values" not in var_data:
            # Convert to new format
            value = None
            try:
                for key, val in var_data.items():
                    if key not in ["name", "code", "description"] and val is not None:
                        try:
                            value = float(val)
                            break
                        except (ValueError, TypeError):
                            pass
            except (ValueError, TypeError):
                pass
                
            if value is not None:
                # Create new format
                data[var_name] = {
                    "name": var_name,
                    "values": [{"value": value, "value_type": "unspecified", "year": None}]
                }
                # Copy other fields
                for key in ["code", "description"]:
                    if key in var_data:
                        data[var_name][key] = var_data[key]
            else:
                # No valid value, remove the variable
                del data[var_name]
    
    return data