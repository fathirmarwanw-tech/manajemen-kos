# Model Ancaman (Threat Model - STRIDE) — Manajemen Kost

| No | Kategori STRIDE | Elemen DFD | Aset Terdampak | Deskripsi Ancaman Spesifik pada Produk |
|----|-----------------|------------|----------------|-----------------------------------------|
| 1 | **S**poofing | `EE-02` -> `P-01` | `AST-04` (Sesi Admin) | Penyerang mencuri cookie sesi admin untuk membajak hak akses panel pengelolaan kamar kost. |
| 2 | **T**ampering | `DS-03` | `AST-03` (Transaksi) | Penyerang memanipulasi kolom nominal pembayaran di database untuk keuntungan pribadi. |
| 3 | **R**epudiation | `P-03` | `AST-03` (Log Transaksi) | Penyewa menyangkal telah melakukan transfer karena sistem tidak mencatat log waktu yang valid. |
| 4 | **I**nformation Disclosure | `DS-02` | `AST-02` (NIK Penyewa) | Penyerang membaca NIK dan nomor telepon penyewa dari database akibat tidak adanya enkripsi data. *(Dimitigasi dengan AES-256-GCM)* |
| 5 | **D**enial of Service | `P-02` | `AST-05` (Server) | Penyerang mengirimkan request pencarian kamar kos secara masif hingga server mengalami kehabisan sumber daya. |
| 6 | **E**levation of Privilege | `P-01` | `AST-01` (Akses Admin) | Penyewa biasa memanipulasi parameter API request untuk mengakses menu CRUD khusus admin kost. |
| 7 | **S**poofing | `EE-01` -> `P-01` | `AST-01` (Kredensial) | Penyerang membuat halaman tiruan (*phishing*) login kost untuk menjaring password penghuni. |
| 8 | **T**ampering | `EE-01` | `AST-02` (Input NIK) | Modul ekstensi browser jahat di sisi klien mengubah format data NIK sebelum dikirim ke server. |
| 9 | **I**nformation Disclosure | `P-01` | `AST-01` (Hash Password) | Pesan *error stack trace* backend terekspos ke publik dan membocorkan struktur skema database. |
| 10 | **R**epudiation | `P-02` | `AST-02` (Log Akses) | Admin menghapus data kontrak penyewa secara ilegal dan menyangkal perbuatannya karena ketiadaan *audit trail*. |