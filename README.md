# HIBP-Tool – Datenleck-Checker mit GUI und CLI

Ein Python-Tool zur Abfrage der [HaveIBeenPwned-API](https://haveibeenpwned.com/api). Prüft, ob E-Mail-Adressen in bekannten Datenleaks auftauchen und klassifiziert die Risiken der geleakten Daten.

## Features

- **Zwei Schnittstellen**: Interaktive GUI (Tkinter) und Command-Line-Interface (CLI)
- **Email-Validierung**: Regex-basierte Validierung mit Fehlerbehandlung
- **Risiko-Klassifizierung**: JSON-basierte Risk-Map ordnet geleakte Datentypen (Passwörter, Kreditkarten, Adressen etc.) in Risikostufen (high/medium/low)
- **Datenexport**: Ergebnisse in JSON und CSV speichern
- **Sichere API-Key-Verwaltung**: Laden aus Umgebungsvariablen via `.env`
- **Robuste Architektur**: Saubere Exception-Hierarchie, modulare Struktur, Unit-Tests

## Installation

### Voraussetzungen
- Python 3.8+
- API-Key von [HaveIBeenPwned](https://haveibeenpwned.com/api) (kostenlos, mit Registrierung)

### Setup

```bash
# Repository klonen oder Datei extrahieren
cd HIBP_Tool

# Virtual Environment erstellen (optional, empfohlen)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

# API-Key in .env speichern
echo "HIBP_API_KEY=dein_api_key_hier" > .env
```

## Verwendung

### CLI-Modus

```bash
python cli.py
```

Interaktive Eingabe:
1. Wähle eine Option (1-4)
2. Gib eine oder mehrere E-Mail-Adressen ein
3. Ergebnisse anschauen, speichern oder neu starten

**Optionen:**
- `1`: Breaches für eine E-Mail prüfen
- `2`: Pastes (Datensammlungen) abrufen
- `3`: Alle Breaches anzeigen
- `4`: Exit

### GUI-Modus

```bash
python gui.py
```

Öffnet ein Fenster mit:
- Eingabefeld für E-Mail-Adressen
- Ausgabebereich mit formatierter Anzeige
- Buttons für verschiedene Abfragen

## Projektstruktur

```
HIBP_Tool/
├── cli.py                      # CLI-Interface
├── gui.py                      # GUI mit Tkinter
├── data-processing.py          # Datenverarbeitung & API-Calls
├── ui_format.py                # Formatierung von Ausgaben
├── utils_and_tests.py          # Hilfsfunktionen & Tests
├── data_class_risk_map.json    # Risk-Klassifizierung für Datentypen
├── requirements.txt            # Dependencies
├── .env                        # API-Key (nicht ins Repo!)
└── .gitignore                  # Excludes .env
```

### Module

**data-processing.py**
- `Breach`, `Paste` Dataclasses
- API-Aufrufe (get_breaches, get_pastes)
- Gruppierung nach Jahr/Domain

**ui_format.py**
- Formatierung von Breach- und Paste-Listen
- Risiko-Summaries
- Warnungen und Info-Meldungen

**utils_and_tests.py**
- Email-Validierung (Regex)
- API-Key aus .env laden
- JSON/CSV-Export
- Unit-Tests

## Risk-Map

Die `data_class_risk_map.json` kategorisiert geleakte Datentypen:

```json
{
  "high": ["Passwords", "Credit cards", "Bank account numbers", ...],
  "medium": ["Email addresses", "Phone numbers", "Dates of birth", ...],
  "low": ["Usernames", "Account names", ...]
}
```

Jeder Breach zeigt an, welche Datentypen geleakt wurden und deren Risikostufe.

## Anforderungen (requirements.txt)

```
certifi==2025.11.12
charset-normalizer==3.4.4
idna==3.11
python-dotenv==1.2.1
requests==2.32.5
urllib3==2.5.0
```

## Beispiel-Output (CLI)

```
┌───────────────────────────────────────┐
│    HIBP – Datenleck-Checker           │
└───────────────────────────────────────┘

Breaches für: user@example.com

Breach #1: Adobe
  Domain: adobe.com
  Breached: 2013-10-04
  Geleakte Daten: Passwords, Email addresses, ...
  Risiko: HIGH

[weitere Breaches...]

Risiko-Summary:
  Gesamt Breaches: 5
  Risiko-Score: 78/100
```

## Testing

Unit-Tests für:
- Email-Validierung (gültig/ungültig)
- API-Key-Laden aus .env
- Serialisierung (Dataclass → JSON)

Testen:
```bash
python -m pytest utils_and_tests.py
```

## Lizenz

MIT (oder deine Lizenz hier)

## Disclaimer

Dieses Tool ist zu Informationszwecken gedacht. Nutze es verantwortungsvoll und nur für Adressen, die dir gehören oder für die du die Erlaubnis hast. HaveIBeenPwned-API hat Rate-Limits – achte darauf bei vielen Abfragen.

---

**Kontakt / Issues**: GitHub Issues oder Pull Requests willkommen!
