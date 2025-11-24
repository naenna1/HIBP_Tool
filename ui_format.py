# Imports:
from typing import List
from data_processing import Breach, Paste, BreachSummary
from colorama import Fore, Style, init
init(autoreset=True)

# Formats a data leak entry:
def format_breach(breach) -> str:
    return (
        f"{Fore.RED}---❌ Breach ❌---{Style.RESET_ALL}\n"
        f"Name: {breach.name}\n"
        f"Domain: {breach.domain}\n"
        f"Date: {breach.breach_date.isoformat() if breach.breach_date else 'N/A'}\n"
        f"Data exposed: {', '.join(breach.data_classes)}\n"
        f"Verified: {'Yes' if breach.is_verified else 'No'}\n"
    )

# Formats a data leak list:
def format_breach_list(breaches: List[Breach]) -> str:
    if not breaches:
        return format_info("No breaches found.")

    return "\n".join(format_breach(b) for b in breaches)

# formats a list of pastes (Pastebin = online services developed for publishing text)
def format_paste_list(pastes: List[Paste]) -> str:
    if not pastes:
        return format_info("No pastes found.")
    result = []
    for paste in pastes:
        result.append(
            f"{Fore.BLUE}---📄 Paste 📄---{Style.RESET_ALL}\n"
            f"ID: {paste.id}\n"
            f"Source: {paste.source}\n"
            f"Title: {paste.title}\n"
            f"Date: {paste.date or 'N/A'}\n"
        )
    return "\n".join(result)

# Summary of all breaches
def format_breach_summary(summary: BreachSummary) -> str:
    total = len(summary.breaches)
    risk = summary.risk_score

    return (
        f"{Fore.RED}---🛑 Breaches Overview 🛑---{Style.RESET_ALL}\n"
        f"Amount of Leaks: {total}\n"
        f"Risk-Score: {risk}\n"
    )

# shows warnings:
def format_warning(message: str) -> str:
    return f"{Fore.YELLOW} ⚠️ {message}{Style.RESET_ALL}"

# shows hints:
def format_info(message: str) -> str:
    return f"{Fore.BLUE} ℹ️ {message}{Style.RESET_ALL}"