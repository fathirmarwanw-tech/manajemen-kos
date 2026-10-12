# Aplikasi Web Manajemen Kost-Kostan (Modul Kriptografi)

## Deskripsi Produk
Aplikasi Web Manajemen Kost-Kostan adalah sistem operasional digital yang dirancang untuk mengelola data kamar, data penyewa, dan transaksi pembayaran secara terpusat. Untuk melindungi kerahasiaan data sensitif (seperti identitas dan kredensial pengguna) dari ancaman kebocoran, aplikasi ini dilengkapi dengan modul keamanan dan kriptografi modern berbasis pustaka standar industri.

## Tabel Kebutuhan Kriptografi

| No | Data Produk | Tujuan Keamanan (Security Goal) | Prioritas | Diturunkan Menjadi Komponen |
|---------------------------------------------|
| 1 | Password Pengguna / Admin | Confidentiality & Integrity (Mencegah pencurian kredensial via plaintext) | Tinggi (High) | Fungsi Hashing Satu Arah (`bcrypt`) |
| 2 | Data Pribadi Penyewa (NIK / No. Telepon) | Confidentiality (Melindungi data pribadi di database) | Tinggi (High) | Enkripsi Simetris Berbasis Blok (`AES-256-GCM` dengan CSPRNG) |
| 3 | Token Autentikasi / Sesi | Unpredictability & Authenticity (Mencegah pemalsuan token) | Sedang (Medium) | Pembangkit Bilangan Acak Aman (`CSPRNG` / `os.urandom`) |

## Rancangan Komponen Kriptografi
- **Masukan (Input):** Plaintext berupa data sensitif penyewa atau *password* teks biasa.
- **Proses:** 
  - *Hashing* menggunakan `bcrypt` untuk password.
  - *Enkripsi* menggunakan `AES-256-GCM` yang menyediakan enkripsi terautentikasi (kerahasiaan dan integritas sekaligus).
- **Keluaran (Output):** *Ciphertext* (termasuk *nonce/IV* dan *tag*) atau *hash string*.
- **Representasi Data:** Menggunakan format *hexadecimal* atau *Base64* untuk penyimpanan data biner hasil enkripsi ke dalam database.
- **Sumber Keacakan:** Menggunakan *Cryptographically Secure Pseudo-Random Number Generator* (CSPRNG) bawaan sistem/pustaka untuk menghasilkan *nonce* dan *salt* yang unik di setiap proses enkripsi.
- **Alasan Pemilihan Pustaka:** Menggunakan pustaka standar yang terpelihara dengan baik (`cryptography` dan `bcrypt` di Python) serta menghindari penggunaan sandi klasik yang sudah tidak aman.

## Cara Menjalankan
1. Clone repository ini ke komputer lokal.
2. Install dependensi yang dibutuhkan:
   ```bash
   pip install -r requirements.txt