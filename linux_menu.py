import os

def show_menu():
    print("\n🛠️ Linux System Menu")
    print("1. Show system date")
    print("2. Show calendar")
    print("3. List users")
    print("4. Add a user")
    print("5. Delete a user")
    print("6. Check disk usage")
    print("7. Start Apache service")
    print("8. Stop Apache service")
    print("9. Exit")

def run_command(cmd):
    os.system(cmd)

def main():
    while True:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            run_command("date")
        elif choice == "2":
            run_command("cal")
        elif choice == "3":
            run_command("cut -d: -f1 /etc/passwd")
        elif choice == "4":
            user = input("Enter new username: ")
            run_command(f"sudo useradd {user}")
        elif choice == "5":
            user = input("Enter username to delete: ")
            run_command(f"sudo userdel {user}")
        elif choice == "6":
            run_command("df -h")
        elif choice == "7":
            run_command("sudo systemctl start apache2")
        elif choice == "8":
            run_command("sudo systemctl stop apache2")
        elif choice == "9":
            print("Exiting... 👋")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
