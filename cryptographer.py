import os
import bcrypt

from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Load Fernet key
key = os.getenv("FERNET_KEY")

if not key:
    raise Exception("FERNET_KEY missing")

fernet = Fernet(key.encode())

# -------------------
# PASSWORD HASHING
# -------------------

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(
        password.encode(),
        salt
    )
    return hashed.decode()

def verify_password(password: str, stored_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        stored_hash.encode()
    )

# -------------------
# PERSONAL DATA ENCRYPTION
# -------------------

def encrypt_data(data: str) -> str:
    encrypted = fernet.encrypt(
        data.encode()
    )
    return encrypted.decode()

def decrypt_data(cipher_text: str) -> str:
    decrypted = fernet.decrypt(
        cipher_text.encode()
    )
    return decrypted.decode()
