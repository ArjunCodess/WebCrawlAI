import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import time
from urllib.parse import urlparse

load_dotenv()

# ThorData proxy configuration
THORDATA_USERNAME = os.getenv("THORDATA_USERNAME")
THORDATA_PASSWORD = os.getenv("THORDATA_PASSWORD")
THORDATA_PROXY_SERVER = os.getenv("THORDATA_PROXY_SERVER")

def validate_proxy_config():
    """Validate that all required ThorData proxy configuration is present"""
    missing = []
    if not THORDATA_USERNAME:
        missing.append("THORDATA_USERNAME")
    if not THORDATA_PASSWORD:
        missing.append("THORDATA_PASSWORD")
    if not THORDATA_PROXY_SERVER:
        missing.append("THORDATA_PROXY_SERVER")
    
    if missing:
        raise ValueError(
            f"Missing required ThorData proxy configuration. Please set the following environment variables: {', '.join(missing)}"
        )

def get_proxies():
    """Create proxy configuration for ThorData residential proxy"""
    validate_proxy_config()
    return {
        "http": f"http://{THORDATA_USERNAME}:{THORDATA_PASSWORD}@{THORDATA_PROXY_SERVER}",
        "https": f"http://{THORDATA_USERNAME}:{THORDATA_PASSWORD}@{THORDATA_PROXY_SERVER}"
    }

def validate_url(url):
    """Validate that the URL is properly formatted"""
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise ValueError("Invalid URL: missing scheme or netloc")
        if result.scheme not in ['http', 'https']:
            raise ValueError(f"Invalid URL scheme: {result.scheme}. Only http and https are supported.")
        return True
    except Exception as e:
        raise ValueError(f"Invalid URL format: {str(e)}")

def scrape_website(website):
    """
    Scrape a website using ThorData residential proxy
    
    Args:
        website: URL of the website to scrape
        
    Returns:
        str: HTML content of the website
        
    Raises:
        ValueError: If URL is invalid or proxy configuration is missing
        Exception: If scraping fails after all retries
    """
    # Validate URL format
    validate_url(website)
    
    max_retries = 3
    retry_delay = 2
    
    proxies = get_proxies()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1} of {max_retries}")
            print(f"Connecting to {website} via ThorData residential proxy...")
            
            response = requests.get(
                website, 
                proxies=proxies, 
                headers=headers, 
                timeout=30,
                allow_redirects=True
            )
            response.raise_for_status()
            
            # Handle encoding properly
            if response.encoding is None or response.encoding == 'ISO-8859-1':
                response.encoding = response.apparent_encoding or 'utf-8'
            
            print("Page content retrieved successfully")
            html = response.text
            
            if html and len(html) > 0:
                return html
            else:
                raise Exception("Empty page content received")
                
        except requests.exceptions.ProxyError as e:
            error_msg = f"Proxy error during attempt {attempt + 1}: {str(e)}"
            print(error_msg)
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to scrape after {max_retries} attempts due to proxy error: {str(e)}")
        except requests.exceptions.Timeout as e:
            error_msg = f"Timeout error during attempt {attempt + 1}: {str(e)}"
            print(error_msg)
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to scrape after {max_retries} attempts due to timeout: {str(e)}")
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error during attempt {attempt + 1}: {e.response.status_code} - {str(e)}"
            print(error_msg)
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to scrape after {max_retries} attempts. HTTP {e.response.status_code}: {str(e)}")
        except requests.exceptions.RequestException as e:
            error_msg = f"Request error during attempt {attempt + 1}: {str(e)}"
            print(error_msg)
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to scrape after {max_retries} attempts: {str(e)}")
        except Exception as e:
            error_msg = f"Unexpected error during attempt {attempt + 1}: {str(e)}"
            print(error_msg)
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to scrape after {max_retries} attempts: {str(e)}")

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]