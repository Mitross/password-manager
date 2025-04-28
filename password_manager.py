import os
from cryptography.fernet import Fernet
import getpass 

class PasswordManager:
    def __init__(self):
        self.key_file = "secret.key"
        self.passwords_file = "passwords.enc"
        self.key = self.load_or_generate_key()
        self.cipher = Fernet(self.key)#func for encryption
        self.passwords = self.load_passwords()#[]

    def load_or_generate_key(self):
        #Load encryption key or generate a new one
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            return key

    def load_passwords(self):
        #Load and decrypt passwords from file
        if not os.path.exists(self.passwords_file):
            return {}
        
        with open(self.passwords_file, "rb") as f:
            encrypted_data = f.read()
        
        try:
            decrypted_data = self.cipher.decrypt(encrypted_data).decode()
            return eval(decrypted_data) 
        except:
            print("Password file corrupted or invalid key...")
            return {}

    def save_passwords(self):
        #Encrypt and save passwords to file
        with open(self.passwords_file, "wb") as f:
            encrypted_data = self.cipher.encrypt(str(self.passwords).encode())##Fernet(self.key).enc...
            f.write(encrypted_data)

    def add_password(self):
        #Add a new password entry
        website = input("Website: ").strip()
        username = input("Username/Email: ").strip()
        password = getpass.getpass("Password (leave empty => generate): ").strip()

        if not password:
            password = self.generate_password()
            print(f"generated Password: {password}")

        self.passwords[website] = {"username": username, "password": password}
        self.save_passwords()
        print("Password saved successfully")

    def view_password(self):
        #View a stored password
        website = input("Website: ").strip()
        
        if website in self.passwords:
            entry = self.passwords[website]
            print(f"\n{website}")
            print(f"Username: {entry['username']}")
            print(f"Password: {entry['password']}")
        else:
            print("No password found for this website")

    def delete_password(self):
        #Delete a password entry
        website = input("Website to delete: ").strip()
        
        if website in self.passwords:
            del self.passwords[website]
            self.save_passwords()
            print("Password deleted")
        else:
            print("No password found for this website")

    def generate_password(self, length=12):
        #Generate  random password
        import random
        import string
        
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(length))

    def run(self):
        
        while True:
            print("\nPassword Manager")
            print("1. Add Password")
            print("2. View Password")
            print("3. Delete Password")
            print("4. Exit")
            
            choice = input("Choose option (1-4): ")
            
            if choice == "1":
                self.add_password()
            elif choice == "2":
                self.view_password()
            elif choice == "3":
                self.delete_password()
            elif choice == "4":
                print("finale")
                break
            else:
                print("only 1-4 please try again")

if __name__ == "__main__":
    manager = PasswordManager()
    manager.run()