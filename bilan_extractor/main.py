"""
Main entry point for the bilan_extractor application.
"""
import argparse
import json
import sys
from pathlib import Path

# Use absolute imports when run as a script, relative imports when imported as a module
if __name__ == "__main__":
    # When run as a script
    import os
    import sys
    # Add the parent directory to sys.path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from bilan_extractor.core.loader import load_bilan
    from bilan_extractor.core.converter import convert_to_markdown
    from bilan_extractor.core.parser import parse_llm_output, validate_financial_variables
    from bilan_extractor.models.variables import FinancialVariables
    from bilan_extractor.services.ollama_client import OllamaClient
    from bilan_extractor.services.docling_wrapper import DoclingWrapper
    from bilan_extractor.config.settings import get_config
    from bilan_extractor.utils.logger import setup_logger
else:
    # When imported as a module
    from .core.loader import load_bilan
    from .core.converter import convert_to_markdown
    from .core.parser import parse_llm_output, validate_financial_variables
    from .models.variables import FinancialVariables
    from .services.ollama_client import OllamaClient
    from .services.docling_wrapper import DoclingWrapper
    from .config.settings import get_config
    from .utils.logger import setup_logger


def main():
    """
    Main function for the bilan_extractor application.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Extract financial variables from financial statements.")
    parser.add_argument("filepath", help="Path to the financial statement file")
    parser.add_argument("--model", help="Ollama model to use", default=None)
    parser.add_argument("--output", help="Path to save the output JSON", default=None)
    parser.add_argument("--markdown", help="Path to save the intermediate Markdown", default=None)
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Set up logger
    log_level = "DEBUG" if args.verbose else "INFO"
    logger = setup_logger(level=log_level)
    
    # Get configuration
    config = get_config()
    
    try:
        # Check if file exists
        filepath = Path(args.filepath)
        if not filepath.exists():
            # Try to find the file at the root of the project
            project_root = Path(__file__).resolve().parent.parent
            filename = filepath.name
            alternative_path = project_root / filename
            
            if alternative_path.exists():
                logger.info(f"File not found at {filepath}, using file at {alternative_path} instead")
                filepath = alternative_path
            else:
                logger.error(f"File not found: {filepath}")
                sys.exit(1)
        
        logger.info(f"Processing file: {filepath}")
        
        # Convert to Markdown
        logger.info("Converting to Markdown...")
        docling = DoclingWrapper()
        
        if args.markdown:
            markdown_text = docling.parse_to_markdown(str(filepath), args.markdown)
            logger.info(f"Markdown saved to: {args.markdown}")
        else:
            markdown_text = docling.parse_to_markdown(str(filepath))
        
        # Extract variables using Ollama
        logger.info("Extracting financial variables...")
        ollama_client = OllamaClient(default_model=config["ollama"]["default_model"])
        model = args.model or config["ollama"]["default_model"]
        
        json_str = ollama_client.extract_financial_variables(markdown_text, model)
        
        # Parse and validate the output
        logger.info("Parsing and validating output...")
        data = parse_llm_output(json_str)
        variables = FinancialVariables.from_dict(data)
        
        # Output the result
        result = variables.to_dict()
        result_json = json.dumps(result, indent=2, ensure_ascii=False)
        
        if args.output:
            output_path = Path(args.output)
            # Create parent directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(result_json, encoding="utf-8")
            logger.info(f"Results saved to: {output_path}")
        
        print(result_json)
        logger.info("Processing completed successfully")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=args.verbose)
        sys.exit(1)


if __name__ == "__main__":
    main()