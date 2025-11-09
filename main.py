from flask import Flask, request, jsonify, send_from_directory
import json
from utils.scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from utils.parse import parse_with_gemini
import os
from urllib.parse import urlparse

app = Flask(__name__, static_url_path='/static')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

def validate_request_data(data):
    """Validate the request data"""
    url = data.get('url')
    parse_description = data.get('parse_description')
    
    if not url:
        return None, 'URL is required'
    if not parse_description:
        return None, 'parse_description is required'
    
    # Validate URL format
    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return None, 'Invalid URL format'
        if parsed.scheme not in ['http', 'https']:
            return None, 'URL must use http or https protocol'
    except Exception as e:
        return None, f'Invalid URL: {str(e)}'
    
    return url, None

@app.route('/scrape-and-parse', methods=['POST'])
def scrape_and_parse():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    # Validate request data
    url, error = validate_request_data(data)
    if error:
        return jsonify({'error': error}), 400
    
    parse_description = data.get('parse_description')
    
    try:
        # Scrape the website
        dom_content = scrape_website(url)
        body_content = extract_body_content(dom_content)
        cleaned_content = clean_body_content(body_content)
        
        # Parse the content
        dom_chunks = split_dom_content(cleaned_content)
        result = parse_with_gemini(dom_chunks, parse_description)
        
        # Try to parse the result as JSON if it's a string
        try:
            if isinstance(result, str):
                result = json.loads(result)
        except json.JSONDecodeError:
            pass  # Keep the result as is if it's not valid JSON
        
        return jsonify({
            'success': True,
            'result': result
        })
    except ValueError as e:
        print(f"Validation error in scrape_and_parse: {str(e)}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Error in scrape_and_parse: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()