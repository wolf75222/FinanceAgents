"""
Module defining data models for financial variables.
"""
import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Union


class ValueType(Enum):
    """Enum for different types of financial values."""
    BRUT = "brut"
    AMORTISSEMENT = "amortissement"
    NET = "net"
    UNSPECIFIED = "unspecified"


@dataclass
class FinancialValue:
    """
    Data class representing a financial value with its type and year.
    """
    value: float
    value_type: ValueType = ValueType.UNSPECIFIED
    year: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "value": self.value,
            "value_type": self.value_type.value,
            "year": self.year
        }


@dataclass
class FinancialVariable:
    """
    Data class representing a financial variable with its values.
    """
    name: str
    values: List[FinancialValue] = field(default_factory=list)
    code: Optional[str] = None
    description: Optional[str] = None
    
    def add_value(self, value: float, value_type: ValueType = ValueType.UNSPECIFIED, year: Optional[int] = None) -> None:
        """Add a value to this variable."""
        self.values.append(FinancialValue(value=value, value_type=value_type, year=year))
    
    def get_value(self, value_type: Optional[ValueType] = None, year: Optional[int] = None) -> Optional[float]:
        """Get a value matching the specified type and year."""
        for val in self.values:
            type_match = value_type is None or val.value_type == value_type
            year_match = year is None or val.year == year
            if type_match and year_match:
                return val.value
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        result = {
            "name": self.name,
            "values": [v.to_dict() for v in self.values]
        }
        if self.code:
            result["code"] = self.code
        if self.description:
            result["description"] = self.description
        return result


@dataclass
class FinancialVariables:
    """
    Data class representing financial variables extracted from a financial statement.
    """
    variables: Dict[str, FinancialVariable] = field(default_factory=dict)
    
    def add_variable(self, variable: FinancialVariable) -> None:
        """Add a variable to the collection."""
        self.variables[variable.name] = variable
    
    def get_variable(self, name: str) -> Optional[FinancialVariable]:
        """Get a variable by name."""
        return self.variables.get(name)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FinancialVariables':
        """
        Create a FinancialVariables instance from a dictionary.
        
        Args:
            data: Dictionary containing financial variables
            
        Returns:
            A FinancialVariables instance
        """
        # Load variable configuration
        config_path = Path(__file__).resolve().parent.parent / "config" / "variables.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {"default_variables": [], "additional_variables": []}
        
        # Create mapping of variable aliases to canonical names
        alias_mapping = {}
        for var_list in [config.get("default_variables", []), config.get("additional_variables", [])]:
            for var_config in var_list:
                name = var_config.get("name")
                if name:
                    for alias in var_config.get("aliases", []):
                        alias_mapping[alias.lower()] = name
                    # Also map the name itself
                    alias_mapping[name.lower()] = name
        
        # Create variable objects from configuration
        variables = {}
        for var_list in [config.get("default_variables", []), config.get("additional_variables", [])]:
            for var_config in var_list:
                name = var_config.get("name")
                if name:
                    variables[name] = FinancialVariable(
                        name=name,
                        code=var_config.get("code"),
                        description=var_config.get("description")
                    )
        
        # Process input data
        result = cls()
        
        # Handle legacy format (flat dictionary of values)
        for key, value in data.items():
            key_lower = key.lower()
            
            # Skip null values
            if value is None:
                continue
                
            # Try to convert to float
            try:
                float_value = float(value)
            except (ValueError, TypeError):
                continue
                
            # Find the canonical variable name
            var_name = alias_mapping.get(key_lower)
            if not var_name:
                # If not in our mapping, use the key as is
                var_name = key
                
            # Get or create the variable
            if var_name not in variables:
                variables[var_name] = FinancialVariable(name=var_name)
                
            # Add the value
            variables[var_name].add_value(float_value)
        
        # Handle new format (structured with value types and years)
        for var_name, var_data in data.items():
            if isinstance(var_data, dict) and "values" in var_data:
                # This is the new format with structured values
                if var_name not in variables:
                    variables[var_name] = FinancialVariable(
                        name=var_name,
                        code=var_data.get("code"),
                        description=var_data.get("description")
                    )
                
                for val_data in var_data["values"]:
                    if isinstance(val_data, dict) and "value" in val_data:
                        try:
                            float_value = float(val_data["value"])
                            value_type = ValueType(val_data.get("value_type", "unspecified"))
                            year = val_data.get("year")
                            variables[var_name].add_value(float_value, value_type, year)
                        except (ValueError, TypeError):
                            continue
        
        # Add all variables to the result
        for var in variables.values():
            result.add_variable(var)
            
        return result
    
    def to_dict(self) -> dict:
        """
        Convert the FinancialVariables instance to a dictionary.
        
        Returns:
            A dictionary representation of the financial variables
        """
        return {name: var.to_dict() for name, var in self.variables.items()}