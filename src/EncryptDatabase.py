from typing import Tuple
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet, InvalidToken
import base64
import os
import getpass

class EncryptDatabase:
    def generate_key(self, password: bytes, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt_data(self, data: bytes) -> bytes:
        if self.key is None:
            raise ValueError("Key not loaded. Please load the password first.")
        data = data.encode('utf-8')
        cipher_suite = Fernet(self.key)
        encrypted_data = cipher_suite.encrypt(data)
        return encrypted_data

    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        if self.key is None:
            raise ValueError("Key not loaded. Please load the password first.")
        cipher_suite = Fernet(self.key)
        try:
            decrypted_data = cipher_suite.decrypt(encrypted_data)
            return decrypted_data
        except InvalidToken:
            return None

    def store_password(self, password: str) -> Tuple[bytes, bytes]:
        salt = os.urandom(16)
        self.key = self.generate_key(password.encode('utf-8'), salt)
        cipher_suite = Fernet(self.key)
        encrypted_password = cipher_suite.encrypt(password.encode('utf-8'))
        return (encrypted_password, salt)

    def load_password(self, encrypted_password_data: Tuple[bytes, bytes]) -> bool:
        password = self.request_password().encode('utf-8')
        stored_password = encrypted_password_data[0]
        salt = encrypted_password_data[1]
        self.key = self.generate_key(password, salt)
        cipher_suite = Fernet(self.key)
        if cipher_suite.decrypt(stored_password) == password:
            return True
        return False

    def create_password(self) -> str:
        while True:
            con1 = getpass.getpass('please enter a password for the drive:\n')
            con2 = getpass.getpass('please confirm the password:\n')

            if con1 == con2:
                return con1

    def request_password(self) -> str:
        return getpass.getpass('please enter the password for the drive:\n')