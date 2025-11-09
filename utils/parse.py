import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash-lite')

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
    except (ValueError, json.JSONDecodeError):
        return text

def smart_merge_dicts(dicts):
    """
    Intelligently merge multiple dictionaries, prioritizing non-empty values.
    Later values only overwrite earlier ones if they're more complete.
    """
    merged = {}

    for obj in dicts:
        for key, value in obj.items():
            # If key doesn't exist yet, add it
            if key not in merged:
                merged[key] = value
                continue

            # Check if new value is "better" than existing value
            existing_value = merged[key]

            # Prioritize non-empty values over empty ones
            new_is_empty = value in [None, "", {}, []]
            existing_is_empty = existing_value in [None, "", {}, []]

            # If new value is empty but existing isn't, keep existing
            if new_is_empty and not existing_is_empty:
                continue

            # If existing is empty but new isn't, replace with new
            if existing_is_empty and not new_is_empty:
                merged[key] = value
                continue

            # If both are dicts, recursively merge them
            if isinstance(value, dict) and isinstance(existing_value, dict):
                merged[key] = smart_merge_dicts([existing_value, value])
                continue

            # If both are lists, combine them (removing duplicates)
            if isinstance(value, list) and isinstance(existing_value, list):
                merged[key] = existing_value + [v for v in value if v not in existing_value]
                continue

            # For other cases, prefer longer/more complete values
            if isinstance(value, str) and isinstance(existing_value, str):
                # Keep the longer string (likely more complete)
                if len(value) > len(existing_value):
                    merged[key] = value
            else:
                # Default: keep the new value
                merged[key] = value

    return merged

def parse_with_gemini(dom_chunks, parse_description):
    """
    Parse content chunks with AI, accumulating context across batches.
    Each batch sees the accumulated data from previous batches.
    """
    if not dom_chunks or len(dom_chunks) == 0:
        return '{}'
    
    initial_prompt_template = """
    Extract information from the following text content and return it as a CLEAN JSON object.

    Text content: {content}

    Instructions:
    1. Extract information matching this description: {description}
    2. Return ONLY a valid JSON object, no other text or markdown
    3. If no information is found, return an empty JSON object {{}}
    4. Ensure the JSON is properly formatted and valid
    5. DO NOT include any explanatory text, code blocks, or markdown - ONLY the JSON object
    """

    merge_prompt_template = """
    You are processing a webpage in chunks. You have already extracted some information from previous chunks.

    CURRENT ACCUMULATED DATA (from previous chunks):
    {accumulated_data}

    NEW CONTENT TO PROCESS (current chunk):
    {new_content}

    TASK:
    Extract information matching this description: {description}

    MERGE INSTRUCTIONS:
    1. Combine the accumulated data with any NEW information found in the current chunk
    2. If the new chunk provides MORE COMPLETE or MORE ACCURATE information for existing fields, UPDATE them
    3. If the new chunk adds NEW fields or information, ADD them
    4. If the new chunk has no relevant new information, keep the accumulated data as is
    5. Prioritize more complete, context-rich information over partial data
    6. Return the MERGED result as a valid JSON object
    7. DO NOT include any explanatory text, code blocks, or markdown - ONLY the JSON object
    """

    accumulated_result = None

    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            # First chunk: extract normally
            if accumulated_result is None:
                prompt = initial_prompt_template.format(
                    content=chunk,
                    description=parse_description
                )
                response = model.generate_content(prompt)
                if not response or not hasattr(response, 'text') or not response.text:
                    print(f"Warning: Empty or invalid response from Gemini API for chunk {i}")
                    continue
                result = clean_json_response(response.text.strip())

                if result and result != '{}':
                    accumulated_result = result
                    print(f"Parsed batch {i} of {len(dom_chunks)} (initial extraction)")
                else:
                    print(f"Parsed batch {i} of {len(dom_chunks)} (no data found)")

            # Subsequent chunks: merge with accumulated data
            else:
                prompt = merge_prompt_template.format(
                    accumulated_data=accumulated_result,
                    new_content=chunk,
                    description=parse_description
                )
                response = model.generate_content(prompt)
                if not response or not hasattr(response, 'text') or not response.text:
                    print(f"Warning: Empty or invalid response from Gemini API for chunk {i}")
                    continue
                result = clean_json_response(response.text.strip())

                if result and result != '{}':
                    accumulated_result = result
                    print(f"Parsed batch {i} of {len(dom_chunks)} (merged with previous data)")
                else:
                    print(f"Parsed batch {i} of {len(dom_chunks)} (keeping previous data)")

        except Exception as e:
            print(f"Error processing chunk {i}: {str(e)}")
            continue

    # Return the accumulated result or empty JSON object
    return accumulated_result if accumulated_result else '{}'