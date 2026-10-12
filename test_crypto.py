import pytest
from crypto_component import KostCryptoManager

def test_encryption_decryption_success():
    """Uji Positif 1: Memastikan enkripsi dan dekripsi data penyewa berhasil."""
    manager = KostCryptoManager()
    data = "Penyewa: Budi - Kamar 101 - NIK: 3171123456789000"
    
    encrypted = manager.encrypt_tenant_data(data)
    decrypted = manager.decrypt_tenant_data(encrypted["nonce"], encrypted["ciphertext"])
    
    assert decrypted == data

def test_password_hashing_success():
    """Uji Positif 2: Memastikan hashing password admin valid."""
    manager = KostCryptoManager()
    pwd = "KostRahasia123!"
    hashed = pwd_hash = manager.hash_admin_password(pwd)
    
    assert manager.verify_admin_password(pwd, hashed) is True

def test_password_verification_negative():
    """Uji Negatif: Memastikan verifikasi gagal jika password salah."""
    manager = KostCryptoManager()
    pwd = "KostRahasia123!"
    hashed = manager.hash_admin_password(pwd)
    
    assert manager.verify_admin_password("SalahPassword", hashed) is False

def test_decryption_tampered_ciphertext_boundary():
    """Uji Batas / Negatif: Memastikan dekripsi gagal jika ciphertext dimanipulasi."""
    manager = KostCryptoManager()
    data = "Data Pembayaran Kost"
    encrypted = manager.encrypt_tenant_data(data)
    
    # Memanipulasi byte terakhir ciphertext
    tampered_cipher = encrypted["ciphertext"][:-2] + "ff"
    
    with pytest.raises(Exception):
        manager.decrypt_tenant_data(encrypted["nonce"], tampered_cipher)