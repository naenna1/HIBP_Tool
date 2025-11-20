### Imports : ###
from ui_format import format_warning
from utils_and_tests import validate_email


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

        if choice == "x":
            print("Thank you for using this program.")
            break

        if choice in ["1", "2"]:
            email = read_email_input()
            if email is None:
                continue

        if choice == "1":
            result = get_breached_account(email)
            print(result)

        elif choice == "2":
            result = get_paste_account(email)
            print(result)

        elif choice == "3":
            result = get_all_breaches()
            print(result)

        elif choice == "4":
            result = get_data_classes()
            print(result)


if __name__ == "__main__":
    main()





