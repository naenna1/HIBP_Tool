### Imports : ###
from utils_and_tests import validate_email
from ui_format import (
    format_warning,
    format_info,
    format_breach_list,
    format_paste_list,
    format_breach_summary,
)
from api_client import (
    get_breached_account,
    get_paste_account,
    get_all_breaches,
    get_data_classes,
)
from data_processing import (
    parse_breach_list,
    parse_paste_list,
    build_breach_summary,
)
### Menükörper ###
def print_menu():
    """Print the main menu to the console"""
    print("\n=== Have I Been Pwned – Checker ===")
    print("1: Check Email for breaches")
    print("2: Show Pastes for email")
    print("3: Show all breaches")
    print("4: Show the data classes")
    print("x: Finished program")


### Funktion des Menükörpers ###

def read_menu_choice():
    """Reads and validates the user´s menu choice"""
    while True:
        choice = input("Please enter your choice: ").strip().lower()

        if choice in ["1", "2", "3", "4", "x"]:
            return choice

        print('Invalid choice. Please try again.')



### Funktion Email ###
def read_email_input():
    while True:
        email = input("\nPlease enter an email (or press Enter to cancel): ").strip().lower()

        if email == "":
            return None

        if not validate_email(email):
            print(format_warning("Invalid email address. Please try again."))
            continue

        return email


def main():
    while True:
        print_menu()
        choice = read_menu_choice()
        email = None # Eigentlich unnötig, aber sonst beschwert Linter sich :D

        if choice == "x":
            print("Thank you for using this program.")
            break

        if choice in ["1", "2"]:
            email = read_email_input()
            if email is None:
                # User hat mit Enter abgebrochen → zurück ins Menü
                continue

        if choice == "1":
            # Breaches holen → Dataclasses → Risk-Score → schön ausgeben
            raw = get_breached_account(email)
            breaches = parse_breach_list(raw)

            if not breaches:
                print(format_info("No breaches found for this email."))
            else:
                summary = build_breach_summary(breaches)
                print(format_breach_list(breaches))
                print(format_breach_summary(summary))

        elif choice == "2":
            # Pastes holen → Dataclasses → formatiert ausgeben
            raw = get_paste_account(email)
            pastes = parse_paste_list(raw)

            if not pastes:
                print(format_info("No pastes found for this email."))
            else:
                print(format_paste_list(pastes))

        elif choice == "3":
            # Alle Breaches → Dataclasses → kurze Übersicht
            raw = get_all_breaches()
            breaches = parse_breach_list(raw)

            if not breaches:
                print(format_info("No breaches returned by the API."))
            else:
                print(format_info(f"Total known breaches: {len(breaches)}"))
                print(format_breach_list(breaches[:10]))

        elif choice == "4":
            # Data Classes einfach auflisten
            data_classes = get_data_classes()

            if not data_classes:
                print(format_info("No data classes returned by the API."))
            else:
                print(format_info("Available data classes:"))
                for dc in data_classes:
                    print(f" - {dc}")


if __name__ == "__main__":
    main()





