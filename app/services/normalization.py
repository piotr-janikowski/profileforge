import re
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException


def normalize_name(name: str) -> str:
    """Collapses whitespace to single spaces and converts the name to title case."""
    cleaned = re.sub(r"\s+", " ", name.strip())
    return cleaned.title()

def split_full_name(name: str):
    """Splits a full name into first_name (all words except the last) and last_name (the last word). If only one word is given, first_name will be empty."""
    parts = name.split()

    first_name = " ".join(parts[:-1])
    last_name = parts[-1]

    return first_name, last_name


def normalize_age(age: str | None) -> int | None:
    """Converts age to an integer, returns None if missing or not a valid number"""
    if not age:
        return None

    try:
        return int(age.strip())
    except ValueError:
        return None


def normalize_phone(phone_number: str | None, default_region: str = "PL") -> str | None:
    """Formats a phone number to E.164 using default_region as a fallback country code; returns None if the number cannot be parsed or is invalid"""
    if not phone_number:
        return None

    try:
        parsed = phonenumbers.parse(phone_number, default_region)
    except NumberParseException:
        return None

    if not phonenumbers.is_valid_number(parsed):
        return None
    
    normalized_phone = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    return normalized_phone


def normalize_email(email: str | None) -> str | None:
    """Removes leading and trailing spaces and converts the email to lowercase."""
    if not email:
        return None
    
    return email.strip().lower()


def normalize_address(address: str | None) -> str | None:
    """Collapses whitespace to single spaces and returns None if the input is empty or missing"""
    if address is None:
        return None

    cleaned = re.sub(r"\s+", " ", address.strip())

    return cleaned if cleaned else None


def normalize_comment(comment: str | None) -> str | None:
    """Collapses whitespace to single spaces and returns None if the input is empty or missing"""
    if not comment:
        return None

    cleaned = re.sub(r"\s+", " ", comment.strip())
    return cleaned if cleaned else None