import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-pro')

def clean_json_response(text):
    """Clean the response to extract only the JSON part"""
    # Remove markdown code blocks if present
    text = text.replace('```json', '').replace('```', '').strip()
    
    # Try to find JSON content between curly braces
    try:
        start = text.index('{')
        end = text.rindex('}') + 1
        json_str = text[start:end]
        
        # Parse and re-format JSON
        parsed_json = json.loads(json_str)
        return json.dumps(parsed_json, indent=2)
    except (ValueError, json.JSONDecodeError) as e:
        return text

def parse_with_gemini(dom_chunks, parse_description):
    prompt_template = """
    Extract information from the following text content and return it as a CLEAN JSON object.
    
    Text content: {content}
    
    Instructions:
    1. Extract information matching this description: {description}
    2. Return ONLY a valid JSON object, no other text or markdown
    3. If no information is found, return an empty JSON object {{}}
    4. Ensure the JSON is properly formatted and valid
    5. DO NOT include any explanatory text, code blocks, or markdown - ONLY the JSON object
    """
    
    parsed_results = []
    
    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            prompt = prompt_template.format(
                content=chunk,
                description=parse_description
            )
            
            response = model.generate_content(prompt)
            result = clean_json_response(response.text.strip())
            if result and result != '{}':
                parsed_results.append(result)
            print(f"Parsed batch: {i} of {len(dom_chunks)}")
        except Exception as e:
            print(f"Error processing chunk {i}: {str(e)}")
            continue
    
    # Combine results if multiple chunks produced output
    if len(parsed_results) > 1:
        try:
            # Parse all results into Python objects
            json_objects = [json.loads(result) for result in parsed_results]
            
            # Merge objects if they're dictionaries
            if all(isinstance(obj, dict) for obj in json_objects):
                merged = {}
                for obj in json_objects:
                    merged.update(obj)
                return json.dumps(merged, indent=2)
            
            # If they're lists or mixed, combine them
            return json.dumps(json_objects, indent=2)
        except json.JSONDecodeError:
            # If merging fails, return the first valid result
            return parsed_results[0]
    
    # Return the single result or empty JSON object
    return parsed_results[0] if parsed_results else '{}'