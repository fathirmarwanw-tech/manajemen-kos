# Aplikasi Manajemen Kost Terintegrasi (Web, Kriptografi, & Keamanan Siber)

Aplikasi Web Manajemen Kost yang dirancang aman dengan perlindungan data berbasis kriptografi standar industri serta analisis pemodelan ancaman siber yang komprehensif.

## Tabel Kebutuhan Kriptografi
| No | Data / Aset | Tujuan Keamanan | Prioritas | Mekanisme / Pustaka |
|---------------------------------------------|
| 1 | Password Pengguna / Admin | Kerahasiaan (*Confidentiality*) | Tinggi | Hashing satu arah (`bcrypt` dengan *salt* unik) |
| 2 | Data Pribadi Penyewa (NIK) | Kerahasiaan & Integritas | Tinggi | Enkripsi simetris blok (`AES-256-GCM` dengan *nonce* CSPRNG) |
| 3 | Sesi Pengguna / Token | Keaslian (*Authenticity*) | Sedang | Pembangkit bilangan acak aman (`os.urandom` / CSPRNG) |

