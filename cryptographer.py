'''import random as r
import string

def key_generator():
    l = list(string.ascii_lowercase)
    num = list("1234567890")
    l1 = l.copy()
    num1 = num.copy()
    key = []
    cipher = {}

    n = 25
    for i in range(26):
        rint = r.randint(0,n)
        key.append(l[rint])
        l.pop(rint)
        n -= 1
    del l

    n1 = 9
    for i in range(10):
        rint = r.randint(0,n1)
        key.append(num[rint])
        num.pop(rint)
        n1 -= 1
    del num

    for i in range(26):
        k = l1[i]
        v = key[i]
        cipher[k] = v

    for i in range(10):
        k = num1[i]
        v = key[i+26]
        cipher[k] = v
    
    return cipher
 
def encrypter(s,cipher):
    s_iter = str(s)
    encrypted_message = ""
    for i in s_iter:
        if i.isalpha():
            if i.isupper():
                for k,v in dict(cipher).items():
                    if i.lower() == k:
                        encrypted_message += str(v).upper()
            else:
                for k,v in dict(cipher).items():
                    if i == k:
                        encrypted_message += v
        elif i.isdigit():
            for k,v in dict(cipher).items():
                    if i == k:
                        encrypted_message += str(v)
        else:
            encrypted_message += i
    return encrypted_message

def decrypter(s,cipher):
    s_iter = str(s)
    decrypted_message = ""
    for i in s_iter:
        if i.isalpha():
            if i.isupper():
                for k,v in dict(cipher).items():
                    if i.lower() == v:
                        decrypted_message += str(k).upper()
            else:
                for k,v in dict(cipher).items():
                    if i == v:
                        decrypted_message += k
        elif i.isdigit():
            for k,v in dict(cipher).items():
                    if i == v:
                        decrypted_message += str(k)
        else:
            decrypted_message += i
    return decrypted_message'''

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
