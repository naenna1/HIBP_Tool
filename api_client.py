# ============================
# api_client.py  (Anna)
# ============================
import requests
from utils_and_tests import load_api_key_from_env
import os

BASE_URL = 'https://haveibeenpwned.com/api/v3'
print('Hallo :)')

class ApiError(Exception):
    """Allgemeiner Fehler bei HIBP-API-Aufrufen."""
    pass


class RateLimitError(ApiError):
    """Wird geworfen, wenn die API ein Rate-Limit meldet."""
    pass

def _build_headers() -> dict[str, str]:
    """Baut den Standard-Header für Anfragen"""
    return {
        'api_key': load_api_key_from_env(),
        'user_agent': os.getenv('HIBP_USER_AGENT', )
    }


def send_request(endpoint: str, params: dict | None = None) -> dict | list:
    """Zentrale Request-Funktion zur HIBP-API."""
    pass


def get_breached_account(email: str) -> list[dict]:
    """Rohdaten zu Breaches für eine E-Mail-Adresse."""
    pass


def get_paste_account(email: str) -> list[dict]:
    """Rohdaten zu Pastes für eine E-Mail-Adresse."""
    pass


def get_all_breaches() -> list[dict]:
    """Rohdaten aller bekannten Breaches."""
    pass


def get_data_classes() -> list[str] | list[dict]:
    """Rohdaten der Data Classes."""
    pass