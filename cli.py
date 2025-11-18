### Imports : ###
#
#
#
#
#


### Menükörper ###
def print_menu():
    """Print the main menu to the console"""
    print("\n=== Have I Been Pwned – Checker ===")
    print("1: Check Email for breaches")
    print("2: Show Pastes for email")
    print("3: Show all breaches")
    print("4: Show the data classes")
    print("b: Get back")
    print("x: Finished program")


### Funktion des Menükörpers ###

def read_menu_choice():
    """Reads and validates the user´s menu choice"""
    choice = input("Please enter your choice: ").strip().lower()

    if choice in ["1", "2", "3", "4", "b", "x"]:
        return choice
    else:
        print("It´s not correct. Please try again.")
        return read_menu_choice()



### Funktion Email ###
def read_email_input():
    while True:
        email = input("\nPlease write your email or go back (b).").strip()

        if email.lower() == "b":
            return "b"

        if not email:
            print(format_warning("Input cannot be empty."))
            continue

        if not validate_email(email):
            print(format_warning("Invalid email address. Please try again."))
            continue

        return email



# Beide Funktionen in einer Schleife
def main():
    while True:
        print_menu()
        choice = read_menu_choice()

        if choice == "x":
            print("Thank you for using this program.")
            break

        # 1 – Check breaches
        if choice == "1":
            email = read_email_input()
            if email == "b":
                continue
            print(f"You have chosen {choice}. (Breaches for {email})")

        # 2 – Show pastes
        elif choice == "2":
            email = read_email_input()
            if email == "b":
                continue
            print(f"Pastes for {email}")

        # 3 – All breaches
        elif choice == "3":
            print("Showing all breaches...")

        # 4 – Data classes
        elif choice == "4":
            print("Showing data classes...")


# Programm starten
if ___name___=="___main___":
    main()





