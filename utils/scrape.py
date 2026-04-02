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

def has_proxy_config():
    """Check if ThorData proxy configuration is available"""
    return all([THORDATA_USERNAME, THORDATA_PASSWORD, THORDATA_PROXY_SERVER])

def get_proxies():
    """Create proxy configuration for ThorData residential proxy, or None if not configured"""
    if not has_proxy_config():
        return None
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

def _fetch(website, headers, proxies=None):
    """Make a single GET request, optionally through a proxy"""
    label = "via proxy" if proxies else "directly"
    print(f"  Connecting to {website} {label}...")

    response = requests.get(
        website,
        proxies=proxies,
        headers=headers,
        timeout=30,
        allow_redirects=True
    )
    response.raise_for_status()

    if response.encoding is None or response.encoding == 'ISO-8859-1':
        response.encoding = response.apparent_encoding or 'utf-8'

    html = response.text
    if not html:
        raise Exception("Empty page content received")

    print(f"  Page content retrieved successfully ({label})")
    return html

def scrape_website(website):
    """
    Scrape a website, trying ThorData proxy first and falling back to a direct request.

    Args:
        website: URL of the website to scrape

    Returns:
        str: HTML content of the website

    Raises:
        ValueError: If URL is invalid
        Exception: If scraping fails after all retries
    """
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

    last_error = None

    for attempt in range(max_retries):
        print(f"Attempt {attempt + 1} of {max_retries}")

        # --- try with proxy first (if configured) ---
        if proxies:
            try:
                return _fetch(website, headers, proxies=proxies)
            except (requests.exceptions.ProxyError, requests.exceptions.SSLError) as e:
                print(f"  Proxy/SSL error: {e}")
                print("  Falling back to direct request...")
            except requests.exceptions.Timeout as e:
                print(f"  Timeout via proxy: {e}")
                print("  Falling back to direct request...")
            except requests.exceptions.HTTPError as e:
                print(f"  HTTP {e.response.status_code} via proxy: {e}")
                print("  Falling back to direct request...")

        # --- fall back to direct request ---
        try:
            return _fetch(website, headers, proxies=None)
        except Exception as e:
            last_error = e
            print(f"  Direct request failed: {e}")

        if attempt < max_retries - 1:
            print(f"  Retrying in {retry_delay}s...")
            time.sleep(retry_delay)

    raise Exception(f"Failed to scrape after {max_retries} attempts: {last_error}")

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