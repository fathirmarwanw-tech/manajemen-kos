# Diagram Aliran Data (DFD) & Trust Boundary — Manajemen Kost

## 1. Daftar Elemen DFD
* **External Entity (EE):**
  * `EE-01`: Penyewa Kost (Pengguna)
  * `EE-02`: Pengelola / Admin Kost
* **Process (P):**
  * `P-01`: Modul Autentikasi & Login (`bcrypt` verifikasi)
  * `P-02`: Modul Enkripsi/Dekripsi Data Penyewa (`AES-256-GCM`)
  * `P-03`: Modul Pencatatan Transaksi Keuangan
* **Data Store (DS):**
  * `DS-01`: Tabel Kredensial Pengguna (`AST-01`)
  * `DS-02`: Tabel Penyewa Terenkripsi (`AST-02`)
  * `DS-03`: Tabel Transaksi (`AST-03`)

## 2. Trust Boundaries (Batas Kepercayaan)
* **Trust Boundary 1 (TB-1):** Memisahkan lingkungan klien (browser pengguna/admin) dari jaringan publik/Web Server aplikasi.
* **Trust Boundary 2 (TB-2):** Memisahkan Web Server aplikasi dengan Database Internal tempat penyimpanan data sensitif (`AST-01`, `AST-02`).

## 3. Penanda Aset Kriptografi pada Aliran Data
* Aliran data input NIK/No. Telp dari `EE-02` menuju `P-02` diamankan dengan **AES-256-GCM** sebelum disimpan ke `DS-02`.
* Aliran verifikasi password dari `EE-01`/`EE-02` ke `P-01` diproses menggunakan **bcrypt**.