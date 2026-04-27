from auth import signup, login, verify_otp
from file_manager import create_file, access_file, share_file, view_metadata
from security import check_buffer, detect_malware

print("🔥 PROGRAM STARTED")

while True:
    print("\n===== Secure File System =====")
    print("1. Signup")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        u = input("Username: ")
        p = input("Password: ")
        signup(u, p)

    elif choice == "2":
        u = input("Username: ")
        p = input("Password: ")

        if login(u, p):
            if verify_otp():

                while True:
                    print("\n1. Create File\n2. Read File\n3. Share File\n4. View Metadata\n5. Logout")
                    ch = input("Choice: ")

                    # ✅ CREATE FILE
                    if ch == "1":
                        fname = input("Filename: ")
                        content = input("Content: ")

                        if check_buffer(content) and not detect_malware(content):
                            create_file(u, fname, content)

                    # ✅ READ FILE
                    elif ch == "2":
                        fname = input("Filename: ")
                        access_file(u, fname)

                    # 🔗 SHARE FILE
                    elif ch == "3":
                        fname = input("Filename: ")
                        target = input("Share with user: ")
                        share_file(u, fname, target)

                    # 📊 VIEW METADATA
                    elif ch == "4":
                        fname = input("Filename: ")
                        view_metadata(fname)

                    # 🚪 LOGOUT
                    elif ch == "5":
                        print("Logging out...")
                        break

                    else:
                        print("Invalid choice")

    elif choice == "3":
        print("Exiting...")
        break

    else:
        print("Invalid choice")