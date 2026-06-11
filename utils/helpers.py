import re

def format_currency(amount: float, currency_symbol: str = "$") -> str:
    """Format a float as a currency string."""
    try:
        return f"{currency_symbol}{float(amount):,.2f}"
    except (ValueError, TypeError):
        return f"{currency_symbol}0.00"

def extract_json_from_text(text: str) -> str:
    """Extract JSON string from Markdown code blocks if present."""
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if match:
        return match.group(1).strip()
    return text.strip()

def is_valid_email(email: str) -> bool:
    """Basic email format validation."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_strong_password(password: str) -> bool:
    """
    Check if password is strong.
    Requires at least 8 characters.
    """
    return len(password) >= 8
