import os
import re
import json
import csv
# Checks whether obj is a Dataclass instance and converts it to dict
from dataclasses import is_dataclass, asdict


# Generates email regex:
# - contains exactly one ‘@’
# - no spaces
# - anything before/after ‘@’ and at least one dot in the domain part

EMAIL_REGEX = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)

# 1. Function for checking email addresses.
#     Requirements:
#   - Must not be empty
#   - No leading/trailing spaces
#   - Rough structure: <something>@<something>.<tld>

def validate_email(email: str) -> bool:
# If email is not a string
    if not isinstance(email, str):
        return False
# Removes spaces at the beginning and end
    email = email.strip()
# Prüft, ob E-Mail leer
    if not email:
        return False
# Applies the regex from above
    return EMAIL_REGEX.match(email) is not None





# 2. Load API key from environment variables.
# var_name: Name of the environment variable, default is “HIBP_API_KEY”.
def load_api_key_from_env(var_name: str = "HIBP_API_KEY") -> str:
# Accesses the environment variable, returns None if it does not exist (instead of an error).
    value = os.getenv(var_name)
# Catches None and empty strings
    if not value:
# Error setting an API key
        raise RuntimeError(
            f"Environment variable '{var_name}' is not set "
            "or empty. Please enter a valid HIBP API key."
        )
    return value







# 3. Auxiliary function: Dataclasses → dict (preparation for json)
def _to_serializable(obj):
    if is_dataclass(obj):
        return asdict(obj)
    return obj





# 4. Save results as JSON.
def save_results_to_json(data, filepath: str) -> None:
# Check if data is a list
    if isinstance(data, list):
# List is converted to dict.
        processed = [_to_serializable(item) for item in data]
# If no list, pass single object
    else:
        processed = _to_serializable(data)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)





# 4.1 Ergebnisse als CSV speichern.
def save_results_to_csv(data, filepath: str) -> None:
    pass

