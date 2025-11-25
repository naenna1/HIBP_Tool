# ============================
# api_client.py  (Anna)
# ============================
import requests
from dotenv import load_dotenv
from utils_and_tests import load_api_key_from_env
import os
load_dotenv()

BASE_URL = 'https://haveibeenpwned.com/api/v3'


class ApiError(Exception):
    """General error in HIBP API calls."""
    pass


class RateLimitError(ApiError):
    """Thrown when the API reports a rate limit."""
    pass

def _build_headers() -> dict[str, str]:
    """Builds the standard header for requests"""
    api_key = load_api_key_from_env()
    user_agent = os.getenv('HIBP_USER_AGENT', 'hibp-team-project/1.0 (student project)')


    return {
        'hibp-api-key': api_key,
        'user-agent': user_agent,
    }


def send_request(endpoint: str, params: dict | None = None) -> dict | list:
    """Central request function for the HIBP API."""
    url = f'{BASE_URL}{endpoint}'
    headers = _build_headers()
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
    except requests.RequestException as exc:
        raise ApiError(f'Network error during API call: {exc}') from exc

    if response.status_code == 200:
        try:
            return response.json()
        except ValueError as exc:
            raise ApiError('The API response is not valid JSON.') from exc

    if response.status_code == 404:
        # No error, just an empty list!
        return []

    if response.status_code == 429:
        raise RateLimitError('Rate limit reached. Please try again later. (HTTP 429)')

    raise ApiError(f'Error during API call: HTTP {response.status_code} - {response.text[:200]}')


def get_breached_account(email: str) -> list[dict]:
    """Raw data on breaches for an email address."""
    endpoint = f'/breachedaccount/{email}'
    params = {'truncateResponse': False}
    data = send_request(endpoint, params=params)
    return data if isinstance(data, list) else []


def get_paste_account(email: str) -> list[dict]:
    """Raw data on pastes for an email address."""
    endpoint = f'/pasteaccount/{email}'
    data = send_request(endpoint)
    return data if isinstance(data, list) else []


def get_all_breaches() -> list[dict]:
    """Raw data on all known breaches."""
    endpoint = '/breaches'
    data = send_request(endpoint)
    return data if isinstance(data, list) else []


def get_data_classes() -> list[str] | list[dict]:
    """Raw data of the data classes."""
    endpoint = '/dataclasses'
    data = send_request(endpoint)
    return data if isinstance(data, list) else []
