import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
import time

load_dotenv()

# ThorData proxy configuration
THORDATA_USERNAME = os.getenv("THORDATA_USERNAME")
THORDATA_PASSWORD = os.getenv("THORDATA_PASSWORD")
THORDATA_PROXY_SERVER = os.getenv("THORDATA_PROXY_SERVER")

def get_proxies():
    """Create proxy configuration for ThorData residential proxy"""
    return {
        "http": f"http://{THORDATA_USERNAME}:{THORDATA_PASSWORD}@{THORDATA_PROXY_SERVER}",
        "https": f"https://{THORDATA_USERNAME}:{THORDATA_PASSWORD}@{THORDATA_PROXY_SERVER}"
    }

def scrape_website(website):
    max_retries = 3
    retry_delay = 2
    
    proxies = get_proxies()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1} of {max_retries}")
            print(f"Connecting to {website} via ThorData residential proxy...")
            
            response = requests.get(website, proxies=proxies, headers=headers, timeout=30)
            response.raise_for_status()
            
            print("Page content retrieved successfully")
            html = response.text
            
            if html and len(html) > 0:
                return html
            else:
                raise Exception("Empty page content received")
                
        except requests.exceptions.RequestException as e:
            print(f"Error during attempt {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise Exception(f"Failed to scrape after {max_retries} attempts: {str(e)}")
        except Exception as e:
            print(f"Error during attempt {attempt + 1}: {str(e)}")
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