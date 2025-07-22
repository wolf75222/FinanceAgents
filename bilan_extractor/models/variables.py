"""
Module defining data models for financial variables.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FinancialVariables:
    """
    Data class representing financial variables extracted from a financial statement.
    """
    actif_total: Optional[float] = None
    passif_total: Optional[float] = None
    capitaux_propres: Optional[float] = None
    resultat_net: Optional[float] = None
    chiffre_affaires: Optional[float] = None
    dettes: Optional[float] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'FinancialVariables':
        """
        Create a FinancialVariables instance from a dictionary.
        
        Args:
            data: Dictionary containing financial variables
            
        Returns:
            A FinancialVariables instance
        """
        # Handle potential key differences (accents, underscores, etc.)
        mapping = {
            'actif_total': ['actif_total', 'actiftotal', 'actif total'],
            'passif_total': ['passif_total', 'passiftotal', 'passif total'],
            'capitaux_propres': ['capitaux_propres', 'capitauxpropres', 'capitaux propres'],
            'resultat_net': ['résultat_net', 'resultat_net', 'résultatnet', 'resultatnet', 'résultat net', 'resultat net'],
            'chiffre_affaires': ['chiffre_affaires', 'chiffreaffaires', 'chiffre affaires', 'chiffre d\'affaires'],
            'dettes': ['dettes', 'dette']
        }
        
        result = {}
        for attr, keys in mapping.items():
            for key in keys:
                if key in data:
                    # Try to convert to float if it's not None
                    value = data[key]
                    if value is not None:
                        try:
                            value = float(value)
                        except (ValueError, TypeError):
                            pass
                    result[attr] = value
                    break
        
        return cls(**result)
    
    def to_dict(self) -> dict:
        """
        Convert the FinancialVariables instance to a dictionary.
        
        Returns:
            A dictionary representation of the financial variables
        """
        return {
            'actif_total': self.actif_total,
            'passif_total': self.passif_total,
            'capitaux_propres': self.capitaux_propres,
            'resultat_net': self.resultat_net,
            'chiffre_affaires': self.chiffre_affaires,
            'dettes': self.dettes
        }