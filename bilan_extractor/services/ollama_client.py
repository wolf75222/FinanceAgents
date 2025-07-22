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
    
    def extract_financial_variables(self, markdown_text: str, model: Optional[str] = None) -> str:
        """
        Extract financial variables from Markdown text using a local LLM via Ollama.
        
        Args:
            markdown_text: The financial statement in Markdown format
            model: The LLM model to use (defaults to the instance's default_model)
            
        Returns:
            The extracted variables as a JSON string
        """
        prompt = f"""Voici un bilan comptable au format Markdown :

{markdown_text}

Identifie et renvoie un dictionnaire Python avec les variables suivantes si elles sont présentes :
- actif_total
- passif_total
- capitaux_propres
- résultat_net
- chiffre_affaires
- dettes

Réponds uniquement avec un dictionnaire JSON parsable."""
        
        return self.chat(prompt, model)