import os
import base64
import hashlib
import getpass
import cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_key(password):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'salt_',
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_data(data, key):
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(data.encode())
    return cipher_text

def decrypt_data(cipher_text, key):
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text)
    return plain_text.decode()

def generate_private_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return private_pem

def generate_public_key(private_key):
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_pem

def main():
    print("Data Encryption Utility")
    print("------------------------")
    
    password = getpass.getpass("Enter password: ")
    confirm_password = getpass.getpass("Confirm password: ")
    
    if password != confirm_password:
        print("Passwords do not match. Exiting.")
        return
    
    key = generate_key(password)
    print("Generated key:", key)
    
    data = input("Enter data to encrypt: ")
    cipher_text = encrypt_data(data, key)
    print("Encrypted data:", cipher_text)
    
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    
    with open("private_key.pem", "wb") as f:
        f.write(private_key)
    
    with open("public_key.pem", "wb") as f:
        f.write(public_key)
    
    print("Private key saved to private_key.pem")
    print("Public key saved to public_key.pem")
    
    print("Decrypted data:", decrypt_data(cipher_text, key))

if __name__ == "__main__":
    main()