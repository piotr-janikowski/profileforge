import pytest
from app.services.normalization import (
    normalize_email,
    normalize_name,
    split_full_name,
    normalize_age,
    normalize_phone,
    normalize_address,
    normalize_comment,
)


@pytest.mark.parametrize(
    "raw_name, expected",
    [
        ("  jan kowalski  ", "Jan Kowalski"),
        ("JAN KOWALSKI", "Jan Kowalski"),
        ("jan    kowalski", "Jan Kowalski"),
        ("jan\tkowalski", "Jan Kowalski"),
        ("jan\nkowalski", "Jan Kowalski"),
        ("  JAN    KOWALSKI  ", "Jan Kowalski"),
        ("anna nowak", "Anna Nowak"),
        ("ANNA   NOWAK", "Anna Nowak"),
        ("", ""),
    ],
)
def test_normalize_name(raw_name, expected):
    # Act
    result = normalize_name(raw_name)

    # Assert
    assert result == expected


@pytest.mark.parametrize(
    "full_name, expected",
    [
        ("Jan Kowalski", ("Jan", "Kowalski")),
        ("Jan Piotr Kowalski", ("Jan Piotr", "Kowalski")),
        ("Anna Maria Nowak", ("Anna Maria", "Nowak")),
        ("Kowalski", ("", "Kowalski")),
        ("  Jan   Kowalski  ", ("Jan", "Kowalski")),
    ],
)
def test_split_full_name(full_name, expected):
    result = split_full_name(full_name)
    assert result == expected


@pytest.mark.parametrize(
    "raw_email, expected",
    [
        ("  USER@GMAIL.COM  ", "user@gmail.com"),
        ("User@Example.COM", "user@example.com"),
        ("user@gmail.com", "user@gmail.com"),
        ("   user@gmail.com   ", "user@gmail.com"),
        ("USER@EXAMPLE.COM", "user@example.com"),
        (None, None),
        ("", None),
        ("   ", None),
    ],
)
def test_normalize_email(raw_email, expected):
    result = normalize_email(raw_email)
    assert result == expected


@pytest.mark.parametrize(
    "raw_age, expected",
    [
        ("25", 25),
        (" 25 ", 25),
        ("0", 0),
        ("99", 99),
        (None, None),
        ("", None),
        ("   ", None),
        ("abc", None),
        ("25abc", None),
        ("20.5", None),
    ],
)
def test_normalize_age(raw_age, expected):
    result = normalize_age(raw_age)
    assert result == expected


@pytest.mark.parametrize(
    "phone_number, default_region, expected",
    [
        ("501234567", "PL", "+48501234567"),
        ("+48501234567", "PL", "+48501234567"),
        ("501 234 567", "PL", "+48501234567"),
        ("+49 151 23456789", "PL", "+4915123456789"),
        (None, "PL", None),
        ("", "PL", None),
        ("123", "PL", None),
        ("not a phone number", "PL", None),
    ],
)
def test_normalize_phone(phone_number, default_region, expected):
    result = normalize_phone(phone_number, default_region)
    assert result == expected


@pytest.mark.parametrize(
    "raw_address, expected",
    [
        ("123 Main Street", "123 Main Street"),
        ("  123 Main Street  ", "123 Main Street"),
        ("123    Main    Street", "123 Main Street"),
        ("123\tMain\tStreet", "123 Main Street"),
        ("123\nMain\nStreet", "123 Main Street"),
        ("  123   Main Street  ", "123 Main Street"),
        (None, None),
        ("", None),
        ("   ", None),
    ],
)
def test_normalize_address(raw_address, expected):
    result = normalize_address(raw_address)
    assert result == expected


@pytest.mark.parametrize(
    "raw_comment, expected",
    [
        ("This is a comment", "This is a comment"),
        ("  This is a comment  ", "This is a comment"),
        ("This    is    a comment", "This is a comment"),
        ("This\tis\ta\tcomment", "This is a comment"),
        ("This\nis\na\ncomment", "This is a comment"),
        ("  This   is a comment  ", "This is a comment"),
        (None, None),
        ("", None),
        ("   ", None),
    ],
)
def test_normalize_comment(raw_comment, expected):
    result = normalize_comment(raw_comment)
    assert result == expected