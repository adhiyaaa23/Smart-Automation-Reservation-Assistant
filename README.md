# 🍽️ Mandala Rasa – Smart Reservation Dashboard

> **Capstone Project · CAMP Batch 4 · Kelompok 3 – Hana Jatmiana · 2026**

Platform manajemen reservasi restoran berbasis AI yang dibangun dengan **Streamlit** dan didukung oleh **Google Gemini 2.5 Flash**. Aplikasi ini menyediakan dua mode akses terpisah — **portal pelanggan** untuk reservasi via chatbot, dan **portal admin** dengan dashboard analitik bisnis secara penuh.

---

## 📸 Screenshots

### 1. Halaman Beranda – Mode Pelanggan
![Beranda](screenshots/01_beranda_pelanggan.png)

---

### 2. Halaman Beranda – Mode Admin (Setelah Login)
![Mode Admin](screenshots/02_beranda_admin.png)

---

### 3. Panel Login Admin
![Login Admin](screenshots/03_login_panel.png)

---

### 4. Dashboard Analytics – Overview KPI
![Overview KPI](screenshots/04_dashboard_kpi.png)

---

### 5. Dashboard Analytics – Grafik Reservasi & Revenue
![Grafik Reservasi & Revenue](screenshots/05_dashboard_charts.png)

---

### 6. Manajemen Reservasi – Filter & Tabel Data
![Filter dan Tabel](screenshots/06_manajemen_reservasi.png)

---

### 7. Manajemen Reservasi – Detail Reservasi
![Detail Reservasi](screenshots/07_detail_reservasi.png)

---

### 8. Ketersediaan Meja
![Ketersediaan Meja](screenshots/10_ketersediaan_meja.png)

---

### 9. AI Reservation Assistant – Tampilan Chat (Kosong)
![Tampilan Chat Awal](screenshots/08_sara_chat_kosong.png)

---

### 10. AI Reservation Assistant – Percakapan Aktif
![Percakapan 2 Arah](screenshots/09_sara_chat_aktif.png)

---

## 🗂️ Struktur Project

```
restaurant_dashboard/
├── Beranda.py                      # Entry point – landing page & login admin
├── utils.py                        # Data loader, helper format, save_data, get_table_availability
├── data.json                       # Dataset sintetis 3.000 reservasi
├── Sara_logo.png                   # Logo SARA untuk tampilan chat header
├── requirements.txt                # Dependensi Python
├── README.md                       # Dokumentasi ini
├── .env                            # API key (tidak di-commit ke Git)
├── .gitignore
├── .streamlit/
│   └── config.toml                 # Tema, warna primary, sidebar, server config
└── pages/
    ├── 1_Dashboard_Analytics.py    # Dashboard KPI & visualisasi Plotly (admin only)
    ├── 2_Reservation_Management.py # Manajemen, update status & detail reservasi (admin only)
    └── 3_AI_Assistant.py           # Chatbot SARA berbasis Gemini API (publik)
```

---

## 🚀 Cara Menjalankan

### 1. Clone / Download Project

```bash
git clone <repo-url>
cd restaurant_dashboard
```

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi API Key

Buat file `.env` di folder root project, lalu isi dengan API key Gemini kamu:

```env
GOOGLE_API_KEY="isi_dengan_api_key_gemini_kamu"
```

> Dapatkan API key gratis di [Google AI Studio](https://aistudio.google.com/app/apikey).

### 5. Jalankan Aplikasi

```bash
streamlit run Beranda.py
```

Akses di browser: **http://localhost:8501**

---

## 🔑 Sistem Login Admin

Aplikasi menggunakan sistem role-based access yang disimpan di `st.session_state`:

| State | Nilai Default | Keterangan |
|---|---|---|
| `admin_logged_in` | `False` | Status login admin saat ini |
| `show_admin_login` | `False` | Menampilkan/menyembunyikan panel login |

**Langkah login:**
1. Klik tombol **🔐 Admin Login** di pojok kanan atas halaman Beranda
2. Panel input password akan muncul di bawah tombol
3. Masukkan password lalu klik **Masuk sebagai Admin**

**Password default:** `admin123`

**Setelah login berhasil:**
- Tombol berubah menjadi **🚪 Logout**
- Hero badge berubah dari hijau **"Mode Pelanggan"** menjadi gold **"Mode Admin Aktif"**
- Tiga nav card muncul sekaligus: Dashboard Analytics, Manajemen Reservasi, AI Assistant
- Seluruh halaman admin dapat diakses

> ⚠️ Untuk production, ganti password default dan pertimbangkan menggunakan environment variable.

---

## 📊 Fitur Dashboard Analytics

Halaman ini **hanya dapat diakses oleh admin**. Seluruh chart menggunakan **Plotly** dengan styling konsisten (background putih, aksen gold). Jika diakses tanpa login, ditampilkan halaman *Akses Terlarang*.

### Filter Global
- **Filter Area Meja** – multiselect untuk menyaring seluruh visualisasi berdasarkan area

### Overview KPI

| KPI | Deskripsi |
|---|---|
| Total Reservasi | Jumlah seluruh reservasi di dataset |
| Total Revenue | Total estimasi pendapatan dalam IDR |
| Average Rating | Rata-rata rating pelanggan (skala 1–5) |
| Total Pelanggan Unik | Jumlah Customer ID yang berbeda |
| Completed | Jumlah reservasi berstatus Completed |
| Breakdown Status | Pill badge Confirmed / Pending / Cancelled / No-show |

### Reservation Analytics
- 📊 Tren Reservasi Bulanan (bar chart)
- 🥧 Distribusi Status Reservasi (pie chart)
- 📊 Distribusi Channel Booking (horizontal bar: Walk-in, Website, WhatsApp, Telepon, Instagram DM, Aplikasi Mobile)
- 🥧 Distribusi Area Meja (donut chart)
- 📊 Distribusi Occasion (bar chart)

### Revenue Analytics
- 💰 Revenue per Channel Booking (horizontal bar)
- 💰 Revenue per Area Meja (bar)
- 💰 Revenue per Occasion (pie)
- 📈 Tren Revenue Bulanan (line/bar)

### Customer Analytics
- 👥 Distribusi Jumlah Orang (party size)
- ⭐ Distribusi Rating
- 💳 Distribusi Metode Pembayaran (Cash, QRIS, GoPay, OVO, Dana, ShopeePay, Kartu Kredit, Transfer Bank)

---

## 📋 Fitur Manajemen Reservasi

Halaman ini **hanya dapat diakses oleh admin**.

### Filter & Pencarian
- 🔎 Cari berdasarkan nama pelanggan, Reservation ID, atau Customer ID
- Filter Status: Confirmed, Completed, Pending, Cancelled, No-show
- Filter Area Meja (Indoor, Outdoor, Garden, Bar Area, VIP Room, Private Room)
- Filter Channel Booking

### Tabel Data
- Menampilkan semua reservasi yang cocok dengan filter
- Pagination satu baris dengan navigasi halaman, tombol angka cepat, dan input lompat langsung ke halaman tertentu
- Tombol **⬇️ Download CSV** untuk mengekspor hasil filter ke file `reservasi_export.csv`

### Detail Reservasi
Panel detail yang muncul saat baris diklik, menampilkan:
- Nama lengkap pelanggan + No. HP + Email
- Reservation ID & Customer ID
- Area Meja, Tipe Meja, dan Nomor Meja
- Tanggal, Waktu Reservasi, dan Durasi (menit)
- Jumlah Orang, Occasion, dan Special Request
- Status Reservasi + Metode Pembayaran + Channel Booking
- Estimasi Budget/Orang & Total Estimasi (IDR)
- Rating & Catatan Staff

### Update Status Reservasi
Panel terpisah di bawah tabel untuk mengubah status reservasi secara langsung:
- Pilih Reservation ID (dari seluruh data atau hasil filter aktif)
- Pilih status baru (hanya transisi yang valid ditampilkan; status final seperti *Completed/Cancelled* dikunci)
- Tambahkan catatan opsional untuk staff
- **Conflict detection**: sistem otomatis memeriksa konflik meja apabila status diubah ke *Confirmed* (via `get_table_availability`)
- Perubahan langsung disimpan ke `data.json` melalui fungsi `save_data()`

### 🪑 Ketersediaan Meja *(dengan pemilih tanggal)*
Peta ketersediaan seluruh 41 meja restoran (6 area) dengan navigasi kalender:
- **Kalender interaktif** — pilih tanggal bebas untuk melihat ketersediaan, tidak terbatas hari ini
- Tombol aksi cepat **Hari Ini** dan **Besok** untuk navigasi cepat
- Setiap meja ditampilkan sebagai chip berwarna: 🟢 hijau = tersedia, 🔴 merah = terpakai
- Chip meja terpakai menampilkan waktu reservasi dan nama pelanggan (ringkas)
- **Summary bar** menunjukkan total meja terpakai, tersedia, dan persentase ketersediaan pada tanggal terpilih
- Badge ringkasan per area (misal: "3 bebas · 2 terpakai" atau "✓ Semua bebas" atau "✗ Penuh")
- Status **Pending** dan **Confirmed** dihitung sebagai meja terpakai

---

## 🤖 AI Reservation Assistant (SARA)

**SARA** (Smart Automation Reservation Assistant) adalah chatbot berbasis **Google Gemini 2.5 Flash** via REST API. Halaman ini dapat diakses oleh semua pengguna (pelanggan maupun admin).

### Fitur Utama
- **Reservasi baru** – membantu pelanggan membuat reservasi dengan mengumpulkan: nama, jumlah orang, tanggal, waktu, area, occasion, dan special request
- **Cek status reservasi** – mencari reservasi berdasarkan nama atau Reservation ID / Customer ID
- **Informasi restoran** – menjawab pertanyaan umum tentang jam buka, menu, fasilitas, lokasi, dsb.
- **Fallback heuristik** – jika API Gemini tidak tersedia, SARA tetap merespons dengan logika berbasis intent

### Tools Python (dipanggil dari dalam kode)

| Tool | Fungsi |
|---|---|
| `cek_reservasi_tool(query)` | Mencari reservasi di `data.json` berdasarkan nama, Reservation ID, atau Customer ID |
| `buat_reservasi_tool(...)` | Membuat entri reservasi baru (nama, pax, tanggal, waktu, area, occasion, special_request) |
| `detect_intent(msg)` | Mendeteksi intent: `buat_reservasi`, `cek_reservasi`, `info_restoran`, `greeting` |
| `extract_params(msg)` | Mengekstrak parameter reservasi dari teks natural language |
| `heuristic_response(msg)` | Fallback berbasis rule jika Gemini API tidak tersedia |

### Quick Action Buttons
Tombol shortcut di atas chat window:
- 📅 Buat Reservasi
- 🔍 Cek Status
- 🍽️ Info Restoran
- 📞 Hubungi Kami

### Info Restoran Mandala Rasa (built-in ke system prompt)

| Info | Detail |
|---|---|
| Jam Operasional | Senin–Minggu 10:00–22:00 WIB |
| Area | Indoor (80 pax), Outdoor (60), Garden (80), Bar Area (40), VIP Room (60), Private Room (120) |
| Fasilitas | WiFi gratis, parkir luas, smoking area, live music Jum–Sab 19:00, aksesibel kursi roda |
| Kebijakan | Reservasi min 2 jam sebelumnya, batal gratis H-1, deposit 50% untuk VIP/Private |
| Menu Andalan | Sate Maranggi Spesial, Nasi Goreng Wagyu, Premium Grill Platter, Signature Mocktail |

### Konfigurasi Model
```
Model    : gemini-2.5-flash
Endpoint : generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent
API Key  : dari environment variable GOOGLE_API_KEY
```

---

## 🗃️ Dataset

File `data.json` berisi **3.000 entri reservasi sintetis** dengan kolom lengkap:

| Kolom | Tipe | Keterangan |
|---|---|---|
| `Reservation ID` | String | ID unik reservasi (RSV00001 dst.) |
| `Customer ID` | String | ID unik pelanggan (CUST####) |
| `Nama Customer` | String | Nama lengkap pelanggan |
| `No. HP` | Number | Nomor handphone |
| `Email` | String | Email pelanggan |
| `Tanggal` / `Tanggal Reservasi` | Date | Tanggal reservasi (YYYY-MM-DD) |
| `Waktu Reservasi` | String | Waktu reservasi (HH:MM) |
| `Durasi (menit)` | Integer | Durasi booking meja |
| `Jumlah Orang` | Integer | Jumlah tamu (party size) |
| `Area Meja` | Categorical | Indoor / Outdoor / Garden / Bar Area / VIP Room / Private Room |
| `Tipe Meja` | String | Kapasitas meja (misal "Meja 6 Orang") |
| `Nomor Meja` | Integer | Nomor meja fisik |
| `Occasion` | Categorical | Anniversary / Birthday / Business Meeting / Casual Dining / dll. |
| `Special Request` | String / null | Permintaan khusus pelanggan |
| `Estimasi Budget/Orang (IDR)` | Number | Estimasi pengeluaran per orang |
| `Total Estimasi (IDR)` | Number | Total estimasi pendapatan |
| `Metode Pembayaran` | Categorical | Cash / QRIS / GoPay / OVO / Dana / ShopeePay / Kartu Kredit / Transfer Bank |
| `Channel Booking` | Categorical | Walk-in / Website / WhatsApp / Telepon / Instagram DM / Aplikasi Mobile |
| `Status Reservasi` | Categorical | Confirmed / Completed / Pending / Cancelled / No-show |
| `Rating` | Float / null | Rating kepuasan (1–5), null jika belum selesai |
| `Catatan Staff` | String / null | Catatan internal dari staff |
| `Bulan` | Integer | Bulan reservasi (1–12) |

---

## 🎨 Desain & UI/UX

### Color Palette

| Token | Hex | Penggunaan |
|---|---|---|
| Gold | `#d4af37` | Primary accent, border, badge, button |
| Dark Navy | `#0f1923` | Background sidebar, hero section, text utama |
| Cream | `#e8dcc8` | Text di atas background gelap |
| Light Cream | `#f7f3ee` | Background halaman utama |
| White | `#ffffff` | Card background, chat window |

### Status Colors

| Status | Warna |
|---|---|
| Confirmed | `#2ecc71` (hijau) |
| Completed | `#3498db` (biru) |
| Pending | `#f39c12` (oranye) |
| Cancelled | `#e74c3c` (merah) |
| No-show | `#9b59b6` (ungu) |

### Tipografi
- **Playfair Display** (serif) – heading, judul section, nilai KPI
- **DM Sans** (sans-serif) – body text, label, badge

### Komponen CSS Kustom
- `.kpi-card` – card KPI dengan border kiri berwarna aksen dan shadow
- `.section-title` – judul section dengan garis dekoratif gold
- `.nav-card` – card navigasi dengan hover effect (lift + border gold)
- `.hero-wrap` – hero banner dengan gradient gelap dan radial gold overlay
- `.mini-stat` – stat mini di hero section
- `.back-button` – tombol gradient gold untuk kembali ke beranda
- `.chat-header` – header banner chatbot SARA
- `.filter-card` – card filter di halaman manajemen reservasi
- `.detail-card` – card detail reservasi
- `.update-panel` – panel update status reservasi
- `.pagination-wrap` – kontainer navigasi halaman tabel

### Tema Streamlit (`.streamlit/config.toml`)
```toml
[theme]
base                     = "light"
primaryColor             = "#d4af37"
backgroundColor          = "#f7f3ee"
secondaryBackgroundColor = "#ffffff"
textColor                = "#0f1923"
font                     = "sans serif"

[server]
headless   = true
enableCORS = false

[client]
showSidebarNavigation = false
```

---

## 🛠️ Teknologi

| Layer | Stack |
|---|---|
| Framework | Streamlit ≥ 1.32.0 |
| Visualisasi | Plotly Express & Graph Objects ≥ 5.18.0 |
| Data Processing | Pandas ≥ 2.0.0, JSON built-in |
| AI / LLM | Google Generative AI ≥ 0.5.0 (Gemini 2.5 Flash via REST API) |
| Environment | python-dotenv ≥ 1.0.0 |
| Export | openpyxl ≥ 3.1.0 (support CSV download) |
| Deployment | Streamlit Community Cloud / Local |

---

## ⚙️ Konfigurasi Lanjutan

### Mengganti Password Admin
Di file `Beranda.py`, ubah baris berikut:
```python
ADMIN_PASSWORD = "admin123"
```
Untuk keamanan lebih, simpan sebagai environment variable:
```python
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
```

### Mengganti Dataset
Ganti file `data.json` di root folder. Pastikan kolom berikut tersedia:
`Reservation ID`, `Customer ID`, `Nama Customer`, `No. HP`, `Email`, `Tanggal`, `Waktu Reservasi`, `Durasi (menit)`, `Jumlah Orang`, `Area Meja`, `Tipe Meja`, `Nomor Meja`, `Occasion`, `Special Request`, `Estimasi Budget/Orang (IDR)`, `Total Estimasi (IDR)`, `Metode Pembayaran`, `Channel Booking`, `Status Reservasi`, `Rating`, `Catatan Staff`

### Deploy ke Streamlit Cloud
1. Push project ke GitHub (pastikan `.env` masuk `.gitignore`)
2. Buka [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Pilih repo dan set **Main file path**: `Beranda.py`
4. Tambahkan `GOOGLE_API_KEY` di menu **Secrets** (Settings → Secrets)

---

## 👥 Tim Pengembang

| Anggota | Peran |
|---|---|
| Achmad Raka Yuniar | Project Leader & Backend Developer |
| William Yonathan | AI Engineer |
| Milda Khaerunnisa | Data & Analytics Developer |
| Alfin Agustiar Pratama | Frontend & UI/UX Developer |
| Alfin Agustiar Pratama | QA & Integration Engineer |
| Muhammad Ad'hiya Hartono | Data Scientist & Deployment |

> Dibimbing oleh **Hana Jatmiana** – Mentor Kelompok 3, CAMP Batch 4

---

## 📄 Lisensi

Project ini dibuat sebagai capstone project untuk keperluan akademis dalam program **Data Science & Generative AI – CAMP Batch 4**. Tidak untuk distribusi komersial.

---

*© 2026 Smart Reservation Assistant · Kelompok 3 Hana Jatmiana · Dibuat dengan ❤️ menggunakan Streamlit*
