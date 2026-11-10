# Keputusan Desain dan Kriptografi — Manajemen Kost (v0.2)

Dokumen ini mencatat rincian kebutuhan keamanan, mekanisme kriptografi yang dipilih, serta alasan teknis di balik implementasi pada modul `KostCryptoManager`.

---

## 1. Perlindungan Data Sensitif Penyewa (Enkripsi Data)

- **Kebutuhan (Requirements):**
  Data pribadi penyewa seperti NIK (Nomor Induk Kependudukan) dan nomor telepon wajib dilindungi dari kerahasiaan (_confidentiality_) dan integritasnya (_integrity_) agar tidak bocor atau dimanipulasi secara ilegal di dalam database aplikasi Manajemen Kost.
- **Mekanisme (Mechanism):**
  - **Algoritma:** AES-256-GCM (_Authenticated Encryption with Associated Data_ / AEAD).
  - **Panjang Kunci:** 256-bit (32 byte) untuk memastikan tingkat keamanan simetris yang tinggi.
  - **Nonce / IV:** Menggunakan _Crypto-Secure Pseudo-Random Number Generator_ (`os.urandom(12)`) dengan panjang 12 byte yang unik untuk setiap proses enkripsi agar rentan terhadap serangan _replay_ terhindar.
  - **AAD (Additional Authenticated Data):** Diikat opsional ke konteks data (misal ID penyewa) guna mencegah pemindahan _ciphertext_ antar-record (_ciphertext shifting_).
  - **Auth Tag:** Tag autentikasi bawaan GCM untuk mendeteksi manipulasi data (_tampering_). Jika data rusak, sistem menerapkan prinsip **gagal tertutup (_fail-closed_)** dengan menolak proses dekripsi secara mutlak.
- **Alasan (Rationale):**
  AES-GCM dipilih karena merupakan standar industri modern yang menyediakan enkripsi dan validasi integritas sekaligus dalam satu operasi, mencegah serangan _bit-flipping_, dan efisien secara performa.

---

## 2. Penyimpanan Kata Sandi (_Password Hashing_)

- **Kebutuhan (Requirements):**
  Kredensial akun (password pemilik dan penyewa) tidak boleh disimpan dalam bentuk teks biasa (_plaintext_) atau _hash_ cepat yang mudah dibobol dengan _rainbow table_.
- **Mekanisme (Mechanism):**
  - Menggunakan pustaka **Bcrypt** dengan _salt_ otomatis yang dibangkitkan secara kriptografis pada setiap proses _hashing_.
- **Alasan (Rationale):**
  Bcrypt dirancang secara sengaja agar lambat secara komputasi (_adaptive cost factor_). Hal ini membuat upaya _brute-force_ atau _dictionary attack_ menjadi sangat mahal dan tidak efisien bagi penyerang jika database mengalami kebocoran.

---

## 3. Manajemen Kunci dan Keamanan Repositori

- **Kebutuhan (Requirements):**
  Kunci master enkripsi tidak boleh terekspos di dalam repositori publik GitHub guna menghindari kebocoran rahasia.
- **Mekanisme (Mechanism):**
  - Kunci master dibangkitkan dari luar kode sumber dan dimuat secara dinamis menggunakan _environment variables_ (`.env`).
  - File konfigurasi lokal yang berisi kunci rahasia secara tegas dimasukkan ke dalam `.gitignore`.
  - Seluruh data uji menggunakan data sintetis (_dummy data_), tanpa menyertakan data pribadi nyata atau _secrets_ asli.
