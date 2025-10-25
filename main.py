from flask import Flask, request, jsonify, send_from_directory, send_file
import json
from utils.scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from utils.parse import parse_with_gemini
import os

app = Flask(__name__, static_url_path='/static')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/scrape-and-parse', methods=['POST'])
def scrape_and_parse():
    data = request.get_json()
    url = data.get('url')
    parse_description = data.get('parse_description')
    
    if not url or not parse_description:
        return jsonify({'error': 'Both URL and parse_description are required'}), 400
    
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
    except Exception as e:
        print(f"Error in scrape_and_parse: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()