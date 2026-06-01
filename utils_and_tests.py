import os
# Nur für den schnellen api_client-test


def load_api_key_from_env(var_name: str = "HIBP_API_KEY") -> str:
    """
    Lädt den API-Key aus den Umgebungsvariablen.
    Erwartet, dass z.B. in der .env steht:
        HIBP_API_KEY=dein_key
    """
    key = os.getenv(var_name)
    if not key:
        raise RuntimeError(f"API-Schlüssel fehlt: Umgebungsvariable {var_name} ist nicht gesetzt.")
    return key