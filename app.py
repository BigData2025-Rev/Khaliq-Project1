import authentication
import admin 
import customer
from database import log_event

# Main Menu
def main():
    while True:
        print("\n--- Main Menu ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            user = authentication.login()
            if user:
                if user["role"] == "admin":
                    admin.admin_dashboard()
                elif user["role"] == "privileged_user":
                    admin.admin_dashboard()
                else:
                    customer.user_dashboard(user)
        elif choice == "2":
            authentication.register()
        elif choice == "3":
            log_event("Application exited.")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
