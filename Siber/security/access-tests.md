# Dokumentasi Kontrol Akses, RBAC, dan Keamanan Kredensial — Manajemen Kost (sec-0.2)

Dokumen ini mendokumentasikan matriks kontrol akses berbasis peran (_Role-Based Access Control_ / RBAC), pengujian akses seimbang (positif dan negatif), serta mekanisme penyimpanan kata sandi yang aman untuk aplikasi **Manajemen Kost**.

---

## 1. Matriks Akses Per Peran (Role-Based Access Matrix)

| Sumber Daya / Fitur Sistem                | Peran: Admin  | Peran: Pemilik Kost  | Peran: Penyewa (Tenant)  |  Tamu (Unauthenticated)  |
| :---------------------------------------- | :-----------: | :------------------: | :----------------------: | :----------------------: |
| **Manajemen Konfigurasi Sistem Global**   | `Full Access` |     `No Access`      |       `No Access`        |       `No Access`        |
| **Kelola Data Seluruh Kamar & Properti**  | `Full Access` |    `Full Access`     | `Read-Only (Info Kamar)` | `Read-Only (Info Kamar)` |
| **Kelola Data Keuangan / Tagihan Global** | `Full Access` |    `Full Access`     | `Read (Tagihan Sendiri)` |       `No Access`        |
| **Profil & Data Pribadi Pengguna**        | `Full Access` | `Read/Write Sendiri` |   `Read/Write Sendiri`   |       `No Access`        |

---

## 2. Pengujian Akses Seimbang (Positive & Negative Access Tests)

Sesuai standar pengujian keamanan (_least privilege_), jumlah pengujian akses negatif (upaya akses tidak sah yang wajib ditolak oleh sistem) dirancang **seimbang** dengan pengujian positif.

### Skenario Uji Positif (Akses Sah yang Diizinkan)

- **Uji Positif 1: Admin Mengakses Panel Konfigurasi Sistem**
  - **Aktor:** Pengguna dengan peran `Admin`.
  - **Aksi:** Mengirim permintaan GET ke endpoint `/admin/settings`.
  - **Hasil Diharapkan:** Sistem memberikan akses dan merespon dengan status **HTTP 200 OK**.
  - **Hasil Aktual:** **PASSED** (Akses diberikan sesuai hak istimewa global).

- **Uji Positif 2: Pemilik Kost Mengelola Properti Sendiri**
  - **Aktor:** Pengguna dengan peran `Pemilik Kost`.
  - **Aksi:** Mengirim permintaan POST ke `/owner/properties/update`.
  - **Hasil Diharapkan:** Sistem memvalidasi kepemilikan properti dan merespon dengan **HTTP 200 OK** / _Redirect Success_.
  - **Hasil Aktual:** **PASSED** (Pemilik berhasil memperbarui data properti miliknya).

- **Uji Positif 3: Penyewa Membaca Tagihan Pribadi**
  - **Aktor:** Pengguna dengan peran `Penyewa` (ID sesi: `tenant_001`).
  - **Aksi:** Mengakses endpoint `/tenant/billing`.
  - **Hasil Diharapkan:** Sistem menampilkan data tagihan yang terikat pada ID `tenant_001` dengan **HTTP 200 OK**.
  - **Hasil Aktual:** **PASSED** (Data yang ditampilkan akurat sesuai konteks sesi login).

- **Uji Positif 4: Tamu Melihat Informasi Kamar Publik**
  - **Aktor:** Pengguna belum masuk (_Guest_).
  - **Aksi:** Mengakses halaman katalog kamar `/rooms/public`.
  - **Hasil Diharapkan:** Sistem menampilkan daftar kamar kosong dengan **HTTP 200 OK**.
  - **Hasil Aktual:** **PASSED** (Halaman publik dapat diakses tanpa autentikasi).

---

### Skenario Uji Negatif (Akses Tidak Sah yang Wajib Ditolak)

- **Uji Negatif 1: Penyewa Mencoba Mengakses Panel Admin (Privilege Escalation)**
  - **Aktor:** Pengguna dengan peran `Penyewa`.
  - **Aksi:** Mencoba mengakses endpoint `/admin/dashboard` secara langsung melalui URL.
  - **Hasil Diharapkan:** Sistem mendeteksi kekurangan hak istimewa dan menolak akses dengan **HTTP 403 Forbidden**.
  - **Hasil Aktual:** **PASSED** (Middleware otorisasi berhasil memblokir akses).

- **Uji Negatif 2: Pemilik Kost Mencoba Mengubah Pengaturan Sistem Global**
  - **Aktor:** Pengguna peran `Pemilik Kost`.
  - **Aksi:** Mengakses endpoint sistem global `/admin/system-config`.
  - **Hasil Diharapkan:** Sistem menolak permintaan karena berada di luar cakupan peran pemilik dengan **HTTP 403 Forbidden**.
  - **Hasil Aktual:** **PASSED** (Pemisahan peran (_segregation of duties_) berfungsi dengan baik).

- **Uji Negatif 3: Penyewa Memanipulasi ID untuk Melihat Tagihan Penyewa Lain (IDOR Test)**
  - **Aktor:** Pengguna `Penyewa` (ID sesi: `101`).
  - **Aksi:** Mengirim permintaan ke `/tenant/billing/102` (milik penyewa lain) dengan memanipulasi parameter URL.
  - **Hasil Diharapkan:** Sistem memvalidasi kepemilikan data (_authorization check_) dan menolak akses dengan **HTTP 403 Forbidden** atau **HTTP 404 Not Found**.
  - **Hasil Aktual:** **PASSED** (Serangan _Insecure Direct Object Reference_ berhasil dicegah).

- **Uji Negatif 4: Tamu Mengakses Dashboard Privat Tanpa Sesi**
  - **Aktor:** Pengguna belum masuk (_Guest_).
  - **Aksi:** Mengakses halaman privat `/dashboard`.
  - **Hasil Diharapkan:** Sistem menolak akses dan mengalihkan (_redirect_) ke halaman login atau mengembalikan **HTTP 401 Unauthorized**.
  - **Hasil Aktual:** **PASSED** (Sistem memaksa autentikasi sebelum akses diberikan).

---

## 3. Bukti Penyimpanan Kata Sandi dengan Fungsi Hash Lambat (Bcrypt)

Untuk mematuhi standar keamanan, sistem **tidak pernah** menyimpan kata sandi dalam bentuk _plaintext_ atau _hash_ cepat (seperti MD5/SHA256). Aplikasi menggunakan pustaka **Bcrypt** dengan _adaptive cost factor_ dan _salt_ otomatis.

### Cuplikan Implementasi Keamanan Kredensial (`crypto_component.py`):

```python
import bcrypt

class KostCryptoManager:
    @staticmethod
    def hash_password(password: str) -> bytes:
        """
        Melakukan hashing password menggunakan bcrypt.
        Menghasilkan salt otomatis secara kriptografis dan memperlambat komputasi
        untuk mencegah serangan brute-force / dictionary attack.
        """
        if not password:
            raise ValueError("Password tidak boleh kosong.")
        salt = bcrypt.gensalt(rounds=12)  # Cost factor standar industri
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    @staticmethod
    def verify_password(password: str, hashed: bytes) -> bool:
        """Memverifikasi kecocokan password secara aman dari timing attacks"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed)
        except Exception:
            return False
```
