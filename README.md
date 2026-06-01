# HIBP-Tool

Ein Python-API-Wrapper für die [Have I Been Pwned](https://haveibeenpwned.com/API/v3) API (v3). Prüft, ob E-Mail-Adressen in bekannten Datenlecks auftauchen, und bewertet das Risiko gewichtet.

## Stack

- Python 3.10+
- `requests` — HTTP-Requests an die HIBP API
- `dataclasses` — Datenmodelle für API-Antworten
- `python-dotenv` — API-Key-Management via `.env`

## Architektur

```
api_client.py        ← HIBP-API-Client: Request-Handling, Exception-Hierarchie
data_processing.py   ← Datenmodelle (dataclasses), gewichtetes Risiko-Scoring
utils_and_tests.py   ← Hilfsfunktionen, API-Key-Loader, Tests
.env.example         ← Vorlage für eigene .env (nie committen!)
```

## Setup

```bash
pip install -r requirements.txt

# .env anlegen (aus Vorlage):
cp .env.example .env
# eigenen HIBP API-Key unter https://haveibeenpwned.com/API/v3 besorgen
# und in .env eintragen: HIBP_API_KEY=<dein_key>
```

## Ausführen

```bash
python api_client.py
```

## Fehlerbehandlung

Benutzerdefinierte Exception-Hierarchie:

```
ApiError
└── RateLimitError   ← bei HTTP 429 (Rate Limit)
```

HTTP-Statuscodes werden auf sprechende Exceptions gemappt (200, 404, 429).

## Hinweis

Entstanden als Gruppenarbeit im Kurs Data Analytics (Nov 2025). Eigenanteil: `api_client.py` — API-Client-Design, Exception-Mapping, Header-Management.