# Imports:
from typing import List
from data_processing import Breach, Paste, BreachSummary
from colorama import Fore, Style, init
init(autoreset=True)

# formatiert einen Datenleakeintrag:
def format_breach(breach) -> str:
    return (
        f"{Fore.RED}---❌ Breach ❌---{Style.RESET_ALL}\n"
        f"Name: {breach.name}\n"
        f"Domain: {breach.domain}\n"
        f"Date: {breach.breach_date.isoformat() if breach.breach_date else 'N/A'}\n"
        f"Data exposed: {', '.join(breach.data_classes)}\n"
        f"Verified: {'Yes' if breach.is_verified else 'No'}\n"
    )

# formatiert eine Datenleakliste:
def format_breach_list(breaches: List[Breach]) -> str:
    if not breaches:
        return format_info("No breaches found.")

    return "\n".join(format_breach(b) for b in breaches)

# formatiert eine Liste von Paste (Pastebin= Eintrag, der Daten in die veröffentlicht wurden)
def format_paste_list(pastes: List[Paste]) -> str:
    if not pastes:
        return format_info("No pastes found.")
    result = []
    for paste in pastes:
        result.append(
            f"{Fore.BLUE}---📄 Paste 📄---{Style.RESET_ALL}\n"
            f"ID: {paste.id}\n"
            f"Source: {paste.source}\n" # Datenquelle
            f"Title: {paste.title}\n"
            f"Date: {paste.date or 'N/A'}\n"
        )
    return "\n".join(result)

# Zusammenfassung aller Breaches ( Verstößen)
def format_breach_summary(summary: BreachSummary) -> str:
    total = len(summary.breaches)
    risk = summary.risk_score

    return (
        f"{Fore.RED}---🛑 Breaches Overview 🛑---{Style.RESET_ALL}\n"
        f"Amount of Leaks: {total}\n"
        f"Risk-Score: {risk}%\n"
    )

# zeigt Warnungen an:
def format_warning(message: str) -> str:
    return f"{Fore.YELLOW} ⚠️ {message}{Style.RESET_ALL}"

# zeigt neutrale Hinweise an:
def format_info(message: str) -> str:
    return f"{Fore.BLUE} ℹ️ {message}{Style.RESET_ALL}"