"""
Module for extracting financial variables from Markdown text using LLM.
"""
import ollama


def extract_variables(markdown_text: str, model="gemma:3b") -> str:
    """
    Extract financial variables from Markdown text using a local LLM via Ollama.
    
    Args:
        markdown_text: The financial statement in Markdown format
        model: The LLM model to use (default: "gemma:3b")
        
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
    
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']