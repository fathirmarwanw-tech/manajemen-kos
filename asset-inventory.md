```markdown
# Inventaris Aset — Aplikasi Manajemen Kost

| ID Aset | Nama Aset | Jenis Aset | Lokasi Penyimpanan | Mekanisme Perlindungan / Kriptografi |
|---------|-----------|------------|---------------------|-------------------------------------|
| AST-01 | Password Admin / Pengguna | Kredensial | Database (`users`) | Fungsi *hashing* satu arah menggunakan `bcrypt` dengan *salt* unik. |
| AST-02 | Data Pribadi Penyewa (NIK, No. Telp) | Data Pribadi | Database (`tenants`) | Enkripsi simetris blok **AES-256-GCM** dengan *nonce* CSPRNG. |
| AST-03 | Data Transaksi Pembayaran | Keuangan | Database (`payments`) | Validasi integritas basis data dan pembatasan otorisasi akses. |
| AST-04 | Token Sesi Pengguna | Sesi / Cookie | Memori Klien / Browser | Pembangkit acak aman menggunakan CSPRNG. |
| AST-05 | Kode Sumber Aplikasi | Intelektual | Repository GitHub | Kontrol akses cabang (*branch protection*) dan verifikasi commit. |