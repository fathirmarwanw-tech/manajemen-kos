import pytest
from crypto_component import KostCryptoManager

def test_aes_gcm_encryption_decryption():
    """Uji Positif: Memastikan enkripsi dan dekripsi data penyewa berjalan sukses"""
    manager = KostCryptoManager()
    sensitive_data = "NIK_3201123456780001_08123456789"
    
    encrypted = manager.encrypt_tenant_data(sensitive_data)
    decrypted = manager.decrypt_tenant_data(encrypted)
    
    assert decrypted == sensitive_data

def test_bcrypt_password_hashing():
    """Uji Positif: Memastikan hashing dan verifikasi password valid"""
    password = "KostAmanJaya2026!"
    hashed = KostCryptoManager.hash_password(password)
    
    assert KostCryptoManager.verify_password(password, hashed) is True
    assert KostCryptoManager.verify_password("PasswordSalah", hashed) is False

def test_decryption_tampered_ciphertext_boundary():
    """Uji Batas (Boundary Test): Memastikan dekripsi gagal jika ciphertext dimanipulasi (Integritas GCM)"""
    manager = KostCryptoManager()
    data = "DataRahasiaKamar101"
    
    encrypted = manager.encrypt_tenant_data(data)
    
    # Manipulasi byte terakhir dari ciphertext
    tampered_data = encrypted[:-1] + b'\x00'
    
    with pytest.raises(Exception):
        manager.decrypt_tenant_data(tampered_data)