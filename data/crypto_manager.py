import base64
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet

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

# Function to decrypt data using the key
def decrypt_data(key, encrypted_data):
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_data.encode()).decode()

# Function to retrieve encrypted data from environment variables
def retrieve_encrypted_data(key):
    encrypted_user = os.getenv("EMAIL_USER_CRYPT")
    encrypted_password = os.getenv("EMAIL_PASSWORD_CRYPT")

    if not encrypted_user or not encrypted_password:
        raise ValueError("User or password environment variables not found.")

    # Decrypt the data using the generated key
    user = decrypt_data(key, encrypted_user)
    password = decrypt_data(key, encrypted_password)
    return user, password

# Function to retrieve the salt from environment variables and convert it back to bytes
def retrieve_salt():
    salt_encrypted = os.getenv("EMAIL_SALT")

    if not salt_encrypted:
        raise ValueError("Salt environment variable not found.")

    # Decode the salt saved in base64
    salt = base64.urlsafe_b64decode(salt_encrypted)
    return salt