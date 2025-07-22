"""
Module for interacting with the docling library for PDF processing.
Uses docling.document_converter.DocumentConverter for PDF to Markdown conversion.
With fallback to PyPDF2 for direct text extraction if docling fails.

Supports disabling SSL verification for environments with SSL certificate issues.
"""
import logging
import os
import ssl
import urllib.request
from pathlib import Path
from typing import Optional

# Import settings to access configuration
from ..config import settings

# Configure SSL verification before importing docling
config = settings.get_config()
if config["docling"]["disable_ssl_verification"]:
    # Disable SSL certificate verification
    ssl._create_default_https_context = ssl._create_unverified_context
    os.environ["PYTHONHTTPSVERIFY"] = "0"
    # Disable SSL verification warnings
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    except ImportError:
        pass
    
    logger = logging.getLogger("bilan_extractor")
    logger.warning("SSL certificate verification is disabled. This is not recommended for production use.")

# Import docling for PDF to Markdown conversion
try:
    from docling.document_converter import DocumentConverter
    DOCLING_AVAILABLE = True
except ImportError:
    DOCLING_AVAILABLE = False
    logger = logging.getLogger("bilan_extractor")
    logger.warning("docling library not available. Will use PyPDF2 for text extraction.")

# Import PyPDF2 for fallback text extraction
import PyPDF2

# Set up logger
logger = logging.getLogger("bilan_extractor")


class DoclingWrapper:
    """
    Wrapper for the docling library for processing PDF files.
    Uses DocumentConverter for PDF to Markdown conversion.
    Falls back to PyPDF2 if docling fails.
    """
    
    @staticmethod
    def parse_to_markdown(filepath: str, output_file: Optional[str] = None) -> str:
        """
        Parse a PDF file to Markdown format using docling.DocumentConverter.
        Falls back to PyPDF2 if docling fails.
        
        Args:
            filepath: Path to the PDF file
            output_file: Optional path to save the Markdown output
            
        Returns:
            The Markdown content as a string
            
        Raises:
            FileNotFoundError: If the input file does not exist
        """
        input_path = Path(filepath)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {filepath}")
        
        # Check if docling should be disabled via environment variable
        if os.environ.get("DISABLE_DOCLING", "").lower() in ("1", "true", "yes"):
            logger.info("Docling is disabled by environment variable. Using PyPDF2 for text extraction.")
            return DoclingWrapper._extract_text_with_pypdf2(input_path, output_file)
        
        # Try to use docling if available
        if DOCLING_AVAILABLE:
            try:
                logger.info(f"Converting {input_path} to Markdown using docling.DocumentConverter")
                converter = DocumentConverter()
                result = converter.convert(str(input_path))
                markdown_text = result.document.export_to_markdown()
                
                # Save to file if requested
                if output_file:
                    output_path = Path(output_file)
                    output_path.write_text(markdown_text, encoding="utf-8")
                    logger.info(f"Saved Markdown to {output_path}")
                
                return markdown_text
            except Exception as e:
                logger.warning(f"Docling conversion failed: {e}. Falling back to PyPDF2 for text extraction.")
                return DoclingWrapper._extract_text_with_pypdf2(input_path, output_file)
        else:
            logger.warning("Docling library not available. Using PyPDF2 for text extraction.")
            return DoclingWrapper._extract_text_with_pypdf2(input_path, output_file)
    
    @staticmethod
    def _extract_text_with_pypdf2(input_path: Path, output_file: Optional[str] = None) -> str:
        """
        Extract text from PDF using PyPDF2 as a fallback method.
        
        Args:
            input_path: Path to the PDF file
            output_file: Optional path to save the Markdown output
            
        Returns:
            The extracted text formatted as Markdown
        """
        logger.info(f"Extracting text from {input_path} using PyPDF2")
        
        # Extract text using PyPDF2
        text_content = []
        try:
            with open(input_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    if text:
                        text_content.append(f"## Page {page_num + 1}\n\n{text}\n\n")
        except Exception as e:
            logger.error(f"Error extracting text with PyPDF2: {e}")
            # Return a minimal markdown with error information
            return f"# Error Processing PDF\n\nCould not extract text from {input_path}.\n\nError: {str(e)}"
        
        # Combine all text into a markdown document
        markdown_text = "# PDF Document\n\n" + "".join(text_content)
        
        # Save to file if requested
        if output_file:
            output_path = Path(output_file)
            output_path.write_text(markdown_text, encoding="utf-8")
            logger.info(f"Saved extracted text to {output_path}")
        
        return markdown_text