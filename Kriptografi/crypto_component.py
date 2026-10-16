import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import bcrypt

class KostCryptoManager:
    def __init__(self, master_key: bytes = None):
        # Menggunakan CSPRNG untuk menghasilkan kunci master 256-bit jika tidak disediakan
        self.master_key = master_key if master_key else AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.master_key)

    def encrypt_tenant_data(self, plaintext_data: str) -> bytes:
        """Mengenkripsi data sensitif penyewa (NIK/No Telp) menggunakan AES-256-GCM"""
        nonce = os.urandom(12) # 12 bytes nonce untuk GCM menggunakan CSPRNG
        encrypted = self.aesgcm.encrypt(nonce, plaintext_data.encode('utf-8'), None)
        return nonce + encrypted # Gabungkan nonce dan ciphertext untuk penyimpanan

    def decrypt_tenant_data(self, encrypted_data: bytes) -> str:
        """Mendekripsi data kembali ke bentuk teks asli"""
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        decrypted = self.aesgcm.decrypt(nonce, ciphertext, None)
        return decrypted.decode('utf-8')

    @staticmethod
    def hash_password(password: str) -> bytes:
        """Melakukan hashing password menggunakan bcrypt dengan salt otomatis"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    @staticmethod
    def verify_password(password: str, hashed: bytes) -> bool:
        """Memverifikasi kecocokan password dengan hash bcrypt"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed)