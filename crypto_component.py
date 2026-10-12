import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import bcrypt

class KostCryptoManager:
    def __init__(self):
        # Menghasilkan kunci master 256-bit menggunakan CSPRNG untuk simulasi enkripsi data kost
        self.master_key = AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.master_key)

    def encrypt_tenant_data(self, plaintext: str) -> dict:
        """Mengenkripsi data pribadi penyewa kost menggunakan AES-256-GCM."""
        nonce = os.urandom(12)  # CSPRNG nonce
        ciphertext = self.aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
        return {
            "nonce": nonce.hex(),
            "ciphertext": ciphertext.hex()
        }

    def decrypt_tenant_data(self, nonce_hex: str, ciphertext_hex: str) -> str:
        """Mendekripsi kembali data penyewa kost."""
        nonce = bytes.fromhex(nonce_hex)
        ciphertext = bytes.fromhex(ciphertext_hex)
        plaintext_bytes = self.aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext_bytes.decode('utf-8')

    def hash_admin_password(self, password: str) -> str:
        """Mengamankan password admin kost menggunakan bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_admin_password(self, password: str, hashed: str) -> bool:
        """Memverifikasi password admin."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))