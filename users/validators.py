import re

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

PHONE_PATTERN = re.compile(r"^(8\d{10}|\+7\d{10})$")
GITHUB_HOST = "github.com"


def normalize_phone(phone: str) -> str:
    phone = phone.strip()
    if phone.startswith("8") and len(phone) == 11:
        return "+7" + phone[1:]
    return phone


def validate_phone(value: str) -> str:
    normalized = normalize_phone(value)
    if not PHONE_PATTERN.match(value) and not re.match(r"^\+7\d{10}$", normalized):
        raise ValidationError(
            "Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX"
        )
    return normalized


def validate_github_url(value: str) -> None:
    if not value:
        return
    validator = URLValidator()
    validator(value)
    if GITHUB_HOST not in value.lower():
        raise ValidationError("Ссылка должна вести на GitHub")
