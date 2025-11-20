# Formatierung für Breaches, Pastes, Warnungen und Infos

from textwrap import fill
from typing import List, Dict, Any

Breach = Dict[str, Any]
Paste = Dict[str, Any]
BreachSummary = Dict[str, Any]


# Einzelnen Breach formatiert darstellen

def format_breach(breach: Breach) -> str:

    name = breach.get("Name", "Unbekannt")
    domain = breach.get("Domain", "Keine Domain")
    date = breach.get("BreachDate", "N/A")
    desc = breach.get("Description", "Keine Beschreibung").strip()

    desc = fill(desc, width=70)

    return (
        f"\n{'_' * 60}\n"
        f"🔐 Datenleck: {name}\n"
        f"🌐 Domain:    {domain}\n"
        f"📅 Datum:     {date}\n"
        f"\n📝 Beschreibung:\n{desc}\n"
        f"{'_' * 60}"
    )


# Liste von Breaches formatiert darstellen

def format_breach_list(breaches: List[Breach]) -> str:
    if not breaches:
        return format_info("Keine Datenlecks gefunden.")

    return "\n".join(format_breach(b) for b in breaches)


# Liste von Pastes formatiert darstellen

def format_paste_list(pastes: List[Paste]) -> str:
    if not pastes:
        return format_info("Keine Pastes gefunden.")

    blocks = []
    for p in pastes:
        title = p.get("Title", "Kein Titel")
        source = p.get("Source", "N/A")
        date = p.get("Date", "N/A")

        block = (
            f"\n{'#' * 60}\n"
            f"📝 Paste-Eintrag\n"
            f"Titel:  {title}\n"
            f"Quelle: {source}\n"
            f"Datum:  {date}\n"
            f"{'_' * 60}"
        )
        blocks.append(block)

    return "\n".join(blocks)


# Breach Summary (Risiko-Score + Gesamtübersicht)

def format_breach_summary(summary: BreachSummary) -> str:

    total = summary.get("total_breaches", 0)
    risk = summary.get("risk_score", "N/A")

    return (
        f"\n{'_' * 60}\n"
        f"📊 BREACH-ÜBERSICHT\n"
        f"Anzahl Leaks: {total}\n"
        f"Risiko-Score: {risk} / 100\n"
        f"{'_' * 60}"
    )


# Warnung farblich hervorheben

def format_warning(message: str) -> str:
    return (
        f"\n{'-' * 60}\n"
        f"⚠️  WARNUNG:\n{message}\n"
        f"{'#' * 60}"
    )


# Info / normaler Hinweis

def format_info(message: str) -> str:
    return (
        f"\n{'-' * 60}\n"
        f"{message}\n"
        f"{'-' * 60}"
    )





#test
if __name__ == "__main__":
    test_breach = {
        "Name": "Adobe Leak",
        "Domain": "adobe.com",
        "BreachDate": "2019-10-04",
        "Description": "Passwort-Leak durch Sicherheitslücke."
    }

    print("\n--- Test: Einzelner Breach ---")
    print(format_breach(test_breach))

    print("\n--- Test: Warning ---")
    print(format_warning("Dies ist nur ein Test!"))

    print("\n--- Test: Info ---")
    print(format_info("Alles funktioniert erfolgreich!"))