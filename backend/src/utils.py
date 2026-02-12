import re
import os

def clean_text(text):
    """
    Cleans extracted text by removing excess whitespace and junk characters.
    """
    if not text:
        return ""
    
    # 1. Basic whitespace normalization
    # Replace multiple spaces/newlines with single space
    # text = re.sub(r'\s+', ' ', text).strip() 
    # Actually, getting lines might be better for structure. 
    # Let's keep newlines but trim lines.
    
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    text = '\n'.join(cleaned_lines)
    
    return text

def save_to_file(text, output_path):
    """
    Saves text to a file.
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Successfully saved output to {output_path}")
    except Exception as e:
        print(f"Error saving file: {e}")
