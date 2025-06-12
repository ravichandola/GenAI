# app/utils.py
import requests
from bs4 import BeautifulSoup
import logging
from typing import Optional
import re
from urllib.parse import urlparse
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Remove empty lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return '\n'.join(lines)

def is_valid_url(url: str) -> bool:
    """Check if URL is valid and supported."""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except Exception:
        return False

def scrape_text_from_url(url: str) -> str:
    """
    Scrape and extract text content from a URL.
    
    Args:
        url (str): The URL to scrape
        
    Returns:
        str: Extracted and cleaned text content
        
    Raises:
        ValueError: If URL is invalid or content can't be accessed
        Exception: For other errors during scraping
    """
    try:
        if not is_valid_url(url):
            raise ValueError("Invalid URL format")
            
        logger.info(f"Scraping content from: {url}")
        
        # Add headers to mimic browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make request with timeout
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Check content type
        content_type = response.headers.get('content-type', '').lower()
        if 'text/html' not in content_type:
            raise ValueError(f"Unsupported content type: {content_type}")
            
        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Remove unwanted elements
        for element in soup(['script', 'style', 'noscript', 'header', 'footer', 'nav']):
            element.decompose()
            
        # Extract text from main content areas
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        if not main_content:
            raise ValueError("No main content found on page")
            
        # Get text and clean it
        text = main_content.get_text(separator='\n')
        cleaned_text = clean_text(text)
        
        if not cleaned_text:
            raise ValueError("No text content found after cleaning")
            
        logger.info(f"Successfully extracted {len(cleaned_text)} characters")
        return cleaned_text
        
    except RequestException as re:
        logger.error(f"Request failed: {str(re)}")
        raise ValueError(f"Failed to access URL: {str(re)}")
    except Exception as e:
        logger.error(f"Error scraping URL: {str(e)}", exc_info=True)
        raise Exception(f"Failed to scrape content: {str(e)}")
