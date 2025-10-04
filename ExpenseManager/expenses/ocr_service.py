import pytesseract
from PIL import Image
import re
from datetime import datetime

def extract_text_from_image(image_file):
    """
    Extracts text from an image file using pytesseract.
    """
    try:
        image = Image.open(image_file)
        text = pytesseract.image_to_string(image)
        return parse_ocr_text(text)
    except Exception as e:
        print(f"Error processing image: {e}")
        return {}

def parse_ocr_text(text):
    """
    Parses the extracted text to find relevant information like amount and date.
    """
    data = {
        'amount': find_amount(text),
        'date': find_date(text),
        'raw_text': text
    }
    return data

def find_amount(text):
    """
    Finds the total amount from the text using regular expressions.
    """
    # This regex looks for a line that starts with "Total" or "Amount" and captures the number that follows
    match = re.search(r'(?i)(?:total|amount)\s*[:\s]\s*\$?(\d+\.\d{2})', text)
    if match:
        return match.group(1)
    return None

def find_date(text):
    """
    Finds the date from the text using regular expressions.
    """
    # This regex looks for a date in the format YYYY-MM-DD, MM/DD/YYYY, or DD-MM-YYYY
    match = re.search(r'(\d{4}-\d{2}-\d{2})|(\d{2}/\d{2}/\d{4})|(\d{2}-\d{2}-\d{4})', text)
    if match:
        date_str = match.group(0)
        # Attempt to parse the date to a consistent format (YYYY-MM-DD)
        for fmt in ('%Y-%m-%d', '%m/%d/%Y', '%d-%m-%Y'):
            try:
                return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
            except ValueError:
                pass
    return None