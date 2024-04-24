import re


def extract_date_from_string(text):
    pattern = r"(\d{4}-\d{2}-\d{2}|\d{2}-\d{2}-\d{4}|\d{2}-\d{2}-\d{2})"
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return None
