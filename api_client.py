# ============================
# api_client.py  (Anna)
# ============================
import requests
from utils_and_tests import load_api_key_from_env
import os


BASE_URL = 'https://haveibeenpwned.com/api/v3'


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
        'user_agent': os.getenv('HIBP_USER_AGENT', 'hibp-team-project/1.0 (student project)')
    }


def send_request(endpoint: str, params: dict | None = None) -> dict | list:
    """Zentrale Request-Funktion zur HIBP-API."""
    url = BASE_URL + endpoint
    headers = _build_headers()
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
    except requests.RequestException as exc:
        raise ApiError(f'Netzwerkfehler beim API-Aufruf: {exc}') from exc

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError as exc:
            raise ApiError('Antwort der API ist kein gültiges JSON.') from exc

    if response.status_code == 404:
        # Kein Fehler, nur leere Liste!
        return []

    if response.status_code == 429:
        raise RateLimitError('Rate-Limit erreicht. Bitte später erneut versuchen. (HTTP 429)')

    raise ApiError(f'Fehler beim API-Aufruf: HTTP {response.status_code} - {response.text[:200]}')


def get_breached_account(email: str) -> list[dict]:
    """Rohdaten zu Breaches für eine E-Mail-Adresse."""
    endpoint = f'/breachedaccount/{email}'
    params = {'truncateResponse': False}
    data = send_request(endpoint, params=params)
    return data if isinstance(data, list) else []


def get_paste_account(email: str) -> list[dict]:
    """Rohdaten zu Pastes für eine E-Mail-Adresse."""
    endpoint = f'/pasteaccount/{email}'
    data = send_request(endpoint)
    return data if isinstance(data, list) else []


def get_all_breaches() -> list[dict]:
    """Rohdaten aller bekannten Breaches."""
    endpoint = '/breaches'
    data = send_request(endpoint)
    return data if isinstance(data, list) else []


def get_data_classes() -> list[str] | list[dict]:
    """Rohdaten der Data Classes."""
    endpoint = '/dataclasses'
    data = send_request(endpoint)
    return data if isinstance(data, list) else []

if __name__ == "__main__":
    print("Kleiner Selbsttest von api_client.py")

    try:
        breaches = get_all_breaches()
        print(f"API-Antworttyp: {type(breaches)}, Anzahl Einträge: {len(breaches)}")
    except RateLimitError as e:
        print("RateLimitError:", e)
    except ApiError as e:
        print("ApiError:", e)