import pandas as pd
import csv
from argon2 import PasswordHasher  

class UserAuthentication:
    filepath = 'user_data.csv'
    def __init__(self):
        self.load_users()

    def load_users(self):
        try:
            self.users = pd.read_csv(self.filepath)
        except FileNotFoundError:
            print("User data file not found. Starting with an empty user database.")

    def register_user(self):
        try:
            user_auth_columns = ['Username', 'Password']
            username = input("Enter username:")
            password = input("Enter password: ")
            hash=PasswordHasher()
            hashed_password = hash.hash(password)
            filepath = 'user_data.csv'
            user_data = {'Username': username, 'Password': hashed_password}
            if username in self.users:
               return "Username already exists."
            with open(filepath,'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=user_auth_columns)
                writer.writerow(user_data)
                self.save_users()
            print(f"Expense added to CSV file: {user_data}")
            
        except Exception as e:
            print(f"An error occurred while registering the user: {e}")

    def authenticate_user(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        self.users = pd.read_csv(self.filepath)

       
        try:
            if username not in self.users['Username'].values:
                return "User not found."
            else:
                hashed_password = self.users.loc[self.users['Username'] == username, 'Password'].values
                hash=PasswordHasher()
                hash.verify(hashed_password[0], password)
                return "Authentication successful."
        except:
            return "Authentication failed."
        
    def save_users(self):
        try:
            self.users.to_csv(self.filepath, index=False)
        except Exception as e:
            print(f"An error occurred while saving the user data: {e}")
    def display_users(self):
        try:
            self.load_users()
            print(self.users)
        except Exception as e:
            print(f"An error occurred while displaying users: {e}")
    def start(self):
        
        while True:
            print("\n1. Register User\n2. Authenticate User\n3. Display Users\n4. Save Userss\n5. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                self.register_user()
            elif choice == '2':
                print(self.authenticate_user())
            elif choice == '3':
                self.display_users()
            elif choice == '4':
                self.save_users(self)
                print("Saved the users successfully..")
            elif choice == '5':
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please try again.")


def main():
    auth_system = UserAuthentication()
    auth_system.start()

if __name__ == "__main__":
    main()