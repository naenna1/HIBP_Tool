import os
import re
import json
import csv
# Prüft, ob obj eine Dataclass-Instanz ist und wandelt in dict um
from dataclasses import is_dataclass, asdict


# Erzeugt E-Mail-Regex:
# - enthält genau ein '@'
# - keine Leerzeichen
# - irgendwas vor/nach '@' und mindestens ein Punkt im Domain-Teil

EMAIL_REGEX = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)

# 1. Funktion zur Prüfung für E-Mail-Adressen.
#     Anforderungen:
#   - darf nicht leer sein
#   - keine führenden/trailing Spaces
#   - grobe Struktur: <irgendwas>@<irgendwas>.<tld>

def validate_email(email: str) -> bool:
# Wenn E-Mail kein string ist
    if not isinstance(email, str):
        return False
# Entfernt Leerzeichen am Anfang und Ende
    email = email.strip()
# Prüft, ob E-Mail leer
    if not email:
        return False
# Wendet regex von oben an
    return EMAIL_REGEX.match(email) is not None





# 2. API-Key aus Umgebungsvariablen laden.
# var_name: Name der Umgebungsvariable, standardmäßig "HIBP_API_KEY".
def load_api_key_from_env(var_name: str = "HIBP_API_KEY") -> str:
# Greift auf die Umgebungsvariable zu, gibt None zurück, wenn sie nicht existiert (statt Fehler).
    value = os.environ.get(var_name)
# Fängt None und leere Strings ab
    if not value:
# Fehler zum Setzen eines API-Keys
        raise RuntimeError(
            f"Environment variable '{var_name}' is not set "
            "or empty. Please enter a valid HIBP API key."
        )
    return value







# 3. Hilfsfunktion: Dataclasses → dict (Vorbereitung für json)
def _to_serializable(obj):
    if is_dataclass(obj):
        return asdict(obj)
    return obj





# 4. Ergebnisse als JSON speichern.
def save_results_to_json(data, filepath):
# Prüfen, ob data eine Liste ist.
    if isinstance(data, list):
# Liste wird in dict umgewandelt.
        processed = [_to_serializable(item) for item in data]
# Wenn keine Liste, Einzelobjekt übergeben
    else:
        processed = _to_serializable(data)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(processed, f, ensure_ascii=False, indent=2)





# 4.1 Ergebnisse als CSV speichern.
def save_results_to_csv(data, filepath: str) -> None:
        pass




# 5. Demo
if __name__ == "__main__":
# Es wird eine Liste E-Mails angelegt mit ein paar Testfällen.
    emails = [
        "test@example.com",
        "invalid-email",
        "no-at-sign.example.com",
        "spaces@trim.de",
        "also@not_valid",
        "",
    ]

    print("Quick demo check for validate_email:")
    for e in emails:
    # e!r zeigt den String mit Anführungszeichen.
    # :30 Platz auf 30 Zeichen auffüllen, damit die Ausgabe schön untereinander steht.
    # validate_email(e) Ruft die Funktion von oben auf → ergibt True oder False.
        print(f" {e!r:30} → {validate_email(e)}")