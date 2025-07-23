"""
Module for interacting with the Ollama API.
"""
import logging
import ollama
from typing import Dict, List, Any, Optional
from ollama._types import ResponseError

# Set up logger
logger = logging.getLogger("bilan_extractor")


class OllamaClient:
    """
    Client for interacting with the Ollama API.
    """
    
    def __init__(self, default_model: str = "gemma3"):
        """
        Initialize the Ollama client.
        
        Args:
            default_model: The default model to use for queries
        """
        self.default_model = default_model
    
    def chat(self, prompt: str, model: Optional[str] = None) -> str:
        """
        Send a chat message to the Ollama API and get the response.
        
        Args:
            prompt: The prompt to send to the model
            model: The model to use (defaults to the instance's default_model)
            
        Returns:
            The model's response as a string
        """
        model_to_use = model or self.default_model
        
        try:
            response = ollama.chat(
                model=model_to_use,
                messages=[{"role": "user", "content": prompt}]
            )
            return response['message']['content']
        except ResponseError as e:
            if "model not found" in str(e).lower() and model_to_use != self.default_model:
                logger.warning(f"Model '{model_to_use}' not found. Falling back to default model '{self.default_model}'")
                # Try again with the default model
                response = ollama.chat(
                    model=self.default_model,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response['message']['content']
            elif "model not found" in str(e).lower() and model_to_use == self.default_model:
                # If the default model is also not found, try with "gemma3"
                fallback_model = "gemma3"
                logger.warning(f"Default model '{self.default_model}' not found. Falling back to '{fallback_model}'")
                response = ollama.chat(
                    model=fallback_model,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response['message']['content']
            else:
                # Re-raise other errors
                raise
    
    def extract_financial_variables(self, markdown_text: str, model: Optional[str] = None, 
                                  year: Optional[int] = None, value_type: Optional[str] = None) -> str:
        """
        Extract financial variables from Markdown text using a local LLM via Ollama.
        
        Args:
            markdown_text: The financial statement in Markdown format
            model: The LLM model to use (defaults to the instance's default_model)
            year: The specific year to extract values for (optional)
            value_type: The type of value to extract (brut, net, amortissement) (optional)
            
        Returns:
            The extracted variables as a JSON string
        """
        # Load variable configuration
        import json
        from pathlib import Path
        
        config_path = Path(__file__).resolve().parent.parent / "config" / "variables.json"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            config = {"default_variables": [], "additional_variables": []}
        
        # Build the list of variables to extract
        variables_to_extract = []
        
        # Add default variables
        for var in config.get("default_variables", []):
            name = var.get("name")
            if name:
                variables_to_extract.append(f"- {name}")
        
        # Add additional variables
        for var in config.get("additional_variables", []):
            name = var.get("name")
            code = var.get("code")
            aliases = var.get("aliases", [])
            if name and (code or aliases):
                # Include the code and first alias in the prompt for better identification
                if code and aliases:
                    variables_to_extract.append(f"- {name} (code: {code}, aussi appelé: {aliases[0]})")
                elif code:
                    variables_to_extract.append(f"- {name} (code: {code})")
                elif aliases:
                    variables_to_extract.append(f"- {name} (aussi appelé: {aliases[0]})")
                else:
                    variables_to_extract.append(f"- {name}")
        
        # Build the value type instruction
        value_type_instruction = ""
        if value_type:
            if value_type.lower() == "brut":
                value_type_instruction = "Pour chaque variable, extrait la valeur brute (avant amortissements et provisions)."
            elif value_type.lower() == "net":
                value_type_instruction = "Pour chaque variable, extrait la valeur nette (après amortissements et provisions)."
            elif value_type.lower() in ["amortissement", "amortissements"]:
                value_type_instruction = "Pour chaque variable, extrait la valeur des amortissements et provisions."
            else:
                value_type_instruction = "Pour chaque variable, extrait les valeurs brutes, nettes et d'amortissements si disponibles."
        else:
            value_type_instruction = "Pour chaque variable, extrait les valeurs brutes, nettes et d'amortissements si disponibles."
        
        # Build the year instruction
        year_instruction = ""
        if year:
            year_instruction = f"Extrait les valeurs pour l'année {year}."
        
        # Build the prompt
        prompt = f"""Voici un bilan comptable au format Markdown :

{markdown_text}

Identifie et renvoie un dictionnaire Python avec les variables suivantes si elles sont présentes :
{chr(10).join(variables_to_extract)}

{value_type_instruction}
{year_instruction}

Pour chaque variable, renvoie un dictionnaire avec les clés suivantes :
- "name": le nom de la variable
- "code": le code comptable (si disponible)
- "values": une liste de dictionnaires avec les clés suivantes :
  - "value": la valeur numérique
  - "value_type": le type de valeur ("brut", "amortissement", "net")
  - "year": l'année (si disponible)

Exemple de format de réponse :
{{
  "actif_total": {{
    "name": "actif_total",
    "values": [
      {{
        "value": 1000000,
        "value_type": "brut",
        "year": 2023
      }},
      {{
        "value": 900000,
        "value_type": "net",
        "year": 2023
      }}
    ]
  }},
  "2154220_mat_ind_subv_bioclad_2012": {{
    "name": "2154220_mat_ind_subv_bioclad_2012",
    "code": "2154220",
    "values": [
      {{
        "value": 50000,
        "value_type": "brut",
        "year": 2023
      }},
      {{
        "value": 20000,
        "value_type": "amortissement",
        "year": 2023
      }},
      {{
        "value": 30000,
        "value_type": "net",
        "year": 2023
      }}
    ]
  }}
}}

Réponds uniquement avec un dictionnaire JSON parsable."""
        
        return self.chat(prompt, model)