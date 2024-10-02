import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import winreg

# Function to generate a key from a password and salt
def generate_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

# Function to encrypt data with the key
def encrypt_data(key, text):
    cipher = Fernet(key)
    return cipher.encrypt(text.encode())

# Function to save encrypted data as environment variables in Windows registry
def save_to_env_variables(encrypted_user, encrypted_password, salt):
    try:
        # Open the registry key for user environment variables
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_SET_VALUE)

        # Set environment variables in the registry
        winreg.SetValueEx(registry_key, "EMAIL_USER_CRYPT", 0, winreg.REG_SZ, encrypted_user.decode())
        winreg.SetValueEx(registry_key, "EMAIL_PASSWORD_CRYPT", 0, winreg.REG_SZ, encrypted_password.decode())
        winreg.SetValueEx(registry_key, "EMAIL_SALT", 0, winreg.REG_SZ, base64.urlsafe_b64encode(salt).decode())

        # Close the registry key
        winreg.CloseKey(registry_key)

        # Notify the OS to apply the changes
        os.system("setx EMAIL_USER_CRYPT /M " + encrypted_user.decode())
        os.system("setx EMAIL_PASSWORD_CRYPT /M " + encrypted_password.decode())
        os.system("setx EMAIL_SALT /M " + base64.urlsafe_b64encode(salt).decode())

        print("Environment variables set successfully!")

    except Exception as e:
        print(f"Error setting environment variables: {e}")

def main():
    # Prompt the user for a password to generate the key
    password = input("Enter your password/key to encrypt the data: ")

    # Generate a random salt
    salt = os.urandom(16)

    # Generate the key from the password and salt
    key = generate_key(password, salt)

    # Prompt the user for the username and password to encrypt
    user = input("Enter the username: ")
    user_password = input("Enter the password: ")

    # Encrypt the username and password
    encrypted_user = encrypt_data(key, user)
    encrypted_password = encrypt_data(key, user_password)

    # Save the encrypted environment variables and the salt
    save_to_env_variables(encrypted_user, encrypted_password, salt)

if __name__ == "__main__":
    main()