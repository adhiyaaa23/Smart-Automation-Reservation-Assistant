import streamlit as st
import pandas as pd
import sys, os
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, save_data, get_table_availability, fmt_rupiah, COMMON_CSS, STATUS_COLORS

# Initialize session state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

st.set_page_config(page_title="Manajemen Reservasi · Smart Reservation",
                   page_icon="📋", layout="wide")
st.markdown(COMMON_CSS, unsafe_allow_html=True)

# ✅ Authentication Check
if not st.session_state.admin_logged_in:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0f1923, #1a2a3a); border-radius: 16px; 
         padding: 60px 40px; text-align: center; color: #e8dcc8;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🔐</div>
        <h1 style="font-family: 'Playfair Display', serif; font-size: 2rem; margin: 0 0 10px;">Akses Terlarang</h1>
        <p style="color: rgba(232,220,200,0.8); margin: 0 0 20px;">Hanya admin restoran yang dapat mengakses manajemen reservasi.</p>
        <p style="color: #d4af37; font-weight: 600;">👤 Anda saat ini login sebagai: <strong>Pelanggan</strong></p>
        <hr style="border: 1px solid rgba(255,255,255,0.1); margin: 20px 0;">
        <p style="color: rgba(232,220,200,0.7); font-size: 0.9rem;">Silakan login sebagai admin melalui sidebar atau kembali ke beranda untuk menggunakan chatbot reservasi.</p>
    </div>
    """, unsafe_allow_html=True)

    # Tombol kembali ke beranda
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.page_link("Beranda.py", label="Kembali ke Beranda", icon="🏠", use_container_width=True)
    st.stop()

st.markdown("""
<style>
.main .block-container { background:#f4f0eb !important; padding:1.8rem 2.2rem !important; }

/* ── Header ── */
.page-header {
    background: linear-gradient(135deg,#0f1923 0%,#1c2e40 60%,#2c3e50 100%);
    border-radius:18px; padding:28px 36px; color:#e8dcc8;
    display:flex; justify-content:space-between; align-items:center;
    margin-bottom:1.4rem;
    box-shadow: 0 8px 32px rgba(15,25,35,0.18);
}
.page-header .badge { font-size:0.7rem; letter-spacing:2.5px; text-transform:uppercase;
    color:#d4af37; font-weight:700; margin-bottom:6px; display:block; }
.page-header h1 { font-family:'Playfair Display',serif; font-size:1.9rem;
    margin:0 0 4px; color:#e8dcc8; }
.page-header p  { margin:0; color:rgba(232,220,200,0.55); font-size:0.88rem; }
.page-header-icon { width:64px; height:64px; border-radius:50%;
    background:rgba(212,175,55,0.15); border:1.5px solid rgba(212,175,55,0.35);
    display:flex; align-items:center; justify-content:center; font-size:1.8rem; }

/* ── Filter card ── */
.filter-card {
    background:white; border-radius:14px; padding:1.4rem 1.8rem;
    box-shadow:0 2px 14px rgba(0,0,0,0.06); margin-bottom:1.2rem;
    border-top:3px solid #d4af37;
}

/* ── Table ── */
.tbl-wrap { border-radius:14px; overflow:hidden;
    box-shadow:0 2px 14px rgba(0,0,0,0.07); margin-bottom:1.2rem; }
.tbl-header {
    background:linear-gradient(135deg,#0f1923,#1a2a3a); color:#e8dcc8;
    padding:13px 18px; font-weight:600; font-size:0.82rem; letter-spacing:0.3px;
    display:grid; grid-template-columns:140px 1fr 110px 70px 130px 120px; gap:10px;
}
.tbl-row {
    background:white; border-bottom:1px solid #f0ebe3;
    padding:13px 18px; font-size:0.86rem; color:#333;
    display:grid; grid-template-columns:140px 1fr 110px 70px 130px 120px;
    gap:10px; align-items:center; transition:background .15s;
}
.tbl-row:hover { background:#fdf9f3; }
.tbl-row:last-child { border-bottom:none; }
.rsv-id-text { font-weight:700; color:#d4af37; font-size:0.8rem; }

/* ── Detail card ── */
.detail-card {
    background:white; border-radius:16px; padding:1.8rem 2.2rem;
    box-shadow:0 4px 24px rgba(0,0,0,0.08); border-left:5px solid #d4af37;
}
.detail-name { font-family:'Playfair Display',serif; font-size:1.5rem;
    font-weight:700; color:#0f1923; margin:6px 0; }
.detail-id   { font-size:0.78rem; color:#aaa; font-weight:600; letter-spacing:1px; }
.detail-contact { display:flex; gap:20px; flex-wrap:wrap;
    font-size:0.87rem; color:#555; margin-bottom:1rem; }
.detail-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:1rem; }
.detail-item { background:#f7f3ee; border-radius:10px; padding:11px 14px; }
.detail-lbl  { font-size:0.7rem; text-transform:uppercase; letter-spacing:0.8px;
    color:#999; margin-bottom:3px; font-weight:600; }
.detail-val  { font-size:0.93rem; font-weight:600; color:#0f1923; }
.status-pill { display:inline-block; border-radius:50px; padding:4px 14px;
    font-size:0.76rem; font-weight:700; color:white; margin-left:10px; }
.note-box { background:#fff8e1; border-radius:9px; padding:10px 14px;
    font-size:0.84rem; color:#795800; margin-top:12px;
    border-left:3px solid #f39c12; }
.revenue-val { color:#d4af37 !important; font-size:1.1rem !important;
    font-weight:700 !important; }

/* ── Pagination ── */
.stNumberInput { max-width:120px; }

/* Semua tombol di halaman ini */
.stButton > button {
    border-radius: 10px !important;
    border: 1.5px solid #e0d9ce !important;
    background: white !important;
    color: #4a3f2f !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
    padding: 7px 14px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    transition: all 0.15s ease !important;
    min-height: 38px !important;
}
.stButton > button:hover:not(:disabled) {
    border-color: #d4af37 !important;
    color: #0f1923 !important;
    background: #fdf9f0 !important;
    box-shadow: 0 3px 10px rgba(212,175,55,0.18) !important;
}
.stButton > button:disabled {
    background: #f5f3f0 !important;
    color: #bbb !important;
    border-color: #e8e3dc !important;
    box-shadow: none !important;
}
/* Halaman aktif (tombol disabled dengan bold label) tampak gold */
.stButton > button[disabled][data-active="true"],
.stButton > button:disabled:not([aria-label*="Prev"]):not([aria-label*="Next"]) {
    background: linear-gradient(135deg, #d4af37, #f1d166) !important;
    color: #0f1923 !important;
    border-color: #d4af37 !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

/* Kontainer pagination */
.pagination-wrap {
    background: white;
    border-radius: 12px;
    padding: 12px 18px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.06);
    border: 1px solid #ede8e0;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 1rem;
}
.page-info-badge {
    background: #f7f3ed;
    border: 1px solid #e0d9ce;
    border-radius: 8px;
    padding: 6px 16px;
    text-align: center;
    font-size: 0.85rem;
    color: #555;
    white-space: nowrap;
    line-height: 1.4;
}
.page-info-badge strong { color: #0f1923; font-size: 1rem; }
.page-info-badge .total-info { font-size: 0.75rem; color: #999; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown("### 🍽️ Smart Reservation")
    st.markdown("---")
    st.page_link("Beranda.py", label="🏠 Beranda")
    if st.session_state.admin_logged_in:
        st.page_link("pages/1_Dashboard_Analytics.py",    label="📊 Dashboard Analytics")
        st.page_link("pages/2_Reservation_Management.py", label="📋 Manajemen Reservasi")
    st.page_link("pages/3_AI_Assistant.py", label="🤖 AI Reservation Assistant")
    st.markdown("---")
    
    # Admin status in sidebar
    if st.session_state.admin_logged_in:
        st.markdown("""
        <div style="background: rgba(212,175,55,0.1); border: 1px solid rgba(212,175,55,0.3); 
             border-radius: 8px; padding: 10px; text-align: center; color: #d4af37; font-size: 0.85rem; font-weight: 600;">
        ✓ Admin Mode Active
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

    st.markdown("""
**📍 Mandala Rasa**

🕐 Senin–Minggu · 10:00–22:00

🪑 Indoor · Outdoor · Garden  
&nbsp;&nbsp;&nbsp;&nbsp;Bar · VIP Room · Private

📞 (0341) 123-456  
💬 WA: 0812-3456-7890
""", unsafe_allow_html=True)
    st.markdown("---")

# ── Load data ──
df_all = load_data()

# Pastikan kolom Tanggal Reservasi bertipe datetime
if not pd.api.types.is_datetime64_any_dtype(df_all["Tanggal Reservasi"]):
    df_all["Tanggal Reservasi"] = pd.to_datetime(df_all["Tanggal"], errors="coerce")

# ── Header ──
st.markdown("""
<div class="page-header">
  <div>
    <span class="badge">✦ Admin · Restaurant</span>
    <h1>Manajemen Reservasi</h1>
    <p>Cari, filter, lihat detail, dan ekspor data reservasi</p>
  </div>
  <div class="page-header-icon">📋</div>
</div>
""", unsafe_allow_html=True)

# ══════════════ FILTER ══════════════
st.markdown('<div class="section-title">🔍 Pencarian & Filter</div>', unsafe_allow_html=True)

with st.container():
    f1, f2, f3, f4, f5 = st.columns([2.2, 1.4, 1.4, 1.4, 1.4])
    with f1:
        search = st.text_input("🔎 Cari nama / ID Reservasi / ID Customer",
                               placeholder="Contoh: Andi, RSV00001, CUST001 ...")
    with f2:
        status_opts = ["Semua"] + sorted(df_all["Status Reservasi"].dropna().unique().tolist())
        status_sel  = st.selectbox("Status", status_opts)
    with f3:
        area_opts = ["Semua"] + sorted(df_all["Area Meja"].dropna().unique().tolist())
        area_sel  = st.selectbox("Area Meja", area_opts)
    with f4:
        ch_opts = ["Semua"] + sorted(df_all["Channel Booking"].dropna().unique().tolist())
        ch_sel  = st.selectbox("Channel", ch_opts)
    with f5:
        occ_opts = ["Semua"] + sorted(df_all["Occasion"].dropna().unique().tolist())
        occ_sel  = st.selectbox("Occasion", occ_opts)

    d1, d2 = st.columns(2)
    with d1:
        min_date = df_all["Tanggal Reservasi"].min().date()
        max_date = df_all["Tanggal Reservasi"].max().date()
        date_from = st.date_input("Dari Tanggal", value=min_date,
                                  min_value=min_date, max_value=max_date)
    with d2:
        date_to = st.date_input("Sampai Tanggal", value=max_date,
                                min_value=min_date, max_value=max_date)

# ── Apply filters ──
df = df_all.copy()

if search and search.strip():
    q = search.strip()
    mask = (
        df["Nama Customer"].astype(str).str.contains(q, case=False, na=False) |
        df["Reservation ID"].astype(str).str.contains(q, case=False, na=False) |
        df["Customer ID"].astype(str).str.contains(q, case=False, na=False)
    )
    df = df[mask]

if status_sel != "Semua": df = df[df["Status Reservasi"] == status_sel]
if area_sel   != "Semua": df = df[df["Area Meja"]        == area_sel]
if ch_sel     != "Semua": df = df[df["Channel Booking"]  == ch_sel]
if occ_sel    != "Semua": df = df[df["Occasion"]         == occ_sel]

df = df[
    (df["Tanggal Reservasi"].dt.date >= date_from) &
    (df["Tanggal Reservasi"].dt.date <= date_to)
]
df = df.reset_index(drop=True)

# ── Summary bar + Download ──
sc1, sc2 = st.columns([3, 1])
with sc1:
    total_rev_filt = df["Total Estimasi (IDR)"].sum()
    avg_pax = df["Jumlah Orang"].mean() if len(df) > 0 else 0
    st.markdown(
        f"Menampilkan **{len(df):,}** reservasi &nbsp;·&nbsp; "
        f"Total Revenue: **{fmt_rupiah(total_rev_filt)}** &nbsp;·&nbsp; "
        f"Avg Party Size: **{avg_pax:.1f} orang**",
        unsafe_allow_html=False
    )
with sc2:
    csv_cols = ["Reservation ID","Customer ID","Nama Customer","No. HP","Email",
                "Tanggal","Waktu Reservasi","Jumlah Orang","Area Meja","Tipe Meja",
                "Occasion","Special Request","Total Estimasi (IDR)","Metode Pembayaran",
                "Channel Booking","Status Reservasi","Rating","Catatan Staff"]
    # Hanya ambil kolom yang ada
    csv_cols = [c for c in csv_cols if c in df.columns]
    csv_data = df[csv_cols].to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", data=csv_data,
                       file_name="reservasi_export.csv",
                       mime="text/csv", use_container_width=True)

# ══════════════ TABLE ══════════════
st.markdown('<div class="section-title">📄 Daftar Reservasi</div>', unsafe_allow_html=True)

if df.empty:
    st.info("ℹ️ Tidak ada data yang cocok dengan filter yang dipilih.")
else:
    PAGE_SIZE   = 15
    total_pages = max(1, (len(df) - 1) // PAGE_SIZE + 1)
    if "reservation_page" not in st.session_state:
        st.session_state.reservation_page = 1
    if st.session_state.reservation_page > total_pages:
        st.session_state.reservation_page = total_pages

    cur  = st.session_state.reservation_page

    # ── Pagination: satu baris rapi ─────────────────────────────────────
    # Hitung window halaman (maks 5 tombol angka)
    WIN  = 5
    half = WIN // 2
    start_p = max(1, min(cur - half, total_pages - WIN + 1))
    end_p   = min(total_pages, start_p + WIN - 1)
    page_buttons = list(range(start_p, end_p + 1))

    # Kolom: Prev | angka-angka (maks 5) | info halaman | angka-angka lanjutan | Next
    # Layout: [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1]
    # Sederhana: Prev | ...5 tombol angka... | info | jump input | Next
    nav_cols = st.columns([1] + [0.7] * len(page_buttons) + [2.2, 1, 1])
    col_idx = 0

    with nav_cols[col_idx]:
        prev_clicked = st.button("← Prev", use_container_width=True,
                                 disabled=(cur <= 1), key="prev_page")
    col_idx += 1

    for pnum in page_buttons:
        with nav_cols[col_idx]:
            is_active = (pnum == cur)
            label = f"**{pnum}**" if is_active else str(pnum)
            if st.button(label, key=f"pjump_{pnum}", use_container_width=True,
                         disabled=is_active, help=f"Halaman {pnum}"):
                st.session_state.reservation_page = pnum
                st.rerun()
        col_idx += 1

    with nav_cols[col_idx]:
        st.markdown(
            f"<div class='page-info-badge'>"
            f"Hal <strong>{cur}</strong> / {total_pages}"
            f"<br><span class='total-info'>{len(df):,} reservasi</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    col_idx += 1

    with nav_cols[col_idx]:
        jump_to = st.number_input(
            "Ke halaman", min_value=1, max_value=total_pages,
            value=cur, step=1, key="jump_page_input",
            label_visibility="collapsed",
            help=f"Lompat ke halaman (1–{total_pages})"
        )
        if int(jump_to) != cur:
            st.session_state.reservation_page = int(jump_to)
            st.rerun()
    col_idx += 1

    with nav_cols[col_idx]:
        next_clicked = st.button("Next →", use_container_width=True,
                                 disabled=(cur >= total_pages), key="next_page")

    # ── Proses klik Prev / Next ──────────────────────────────────────────
    if prev_clicked:
        st.session_state.reservation_page = max(1, cur - 1); st.rerun()
    if next_clicked:
        st.session_state.reservation_page = min(total_pages, cur + 1); st.rerun()

    # Variabel dummy agar tidak ada NameError di bawah
    back5 = False
    fwd5  = False

    page_df = df.iloc[(st.session_state.reservation_page-1)*PAGE_SIZE : st.session_state.reservation_page*PAGE_SIZE]

    # Table header + rows
    st.markdown("""
    <div class="tbl-wrap">
      <div class="tbl-header">
        <span>ID Reservasi</span>
        <span>Nama Customer</span>
        <span>Tanggal</span>
        <span>Pax</span>
        <span>Area Meja</span>
        <span>Status</span>
      </div>""", unsafe_allow_html=True)

    rows_html = ""
    for _, row in page_df.iterrows():
        sc    = STATUS_COLORS.get(str(row.get("Status Reservasi","")), "#ccc")
        nama  = str(row.get("Nama Customer","—"))
        tgl   = str(row.get("Tanggal","—"))
        rsv   = str(row.get("Reservation ID","—"))
        area  = str(row.get("Area Meja","—"))
        stat  = str(row.get("Status Reservasi","—"))
        pax_v = row.get("Jumlah Orang", 0)
        pax   = int(pax_v) if pd.notna(pax_v) else "-"
        rows_html += f"""
      <div class="tbl-row">
        <span class="rsv-id-text">{rsv}</span>
        <span style="font-weight:600">{nama}</span>
        <span style="color:#666">{tgl}</span>
        <span>👥 {pax}</span>
        <span>{area}</span>
        <span><span style="background:{sc};color:white;border-radius:50px;
              padding:3px 10px;font-size:0.73rem;font-weight:700">{stat}</span></span>
      </div>"""
    st.markdown(rows_html + "</div>", unsafe_allow_html=True)

    # ══════════════ DETAIL VIEW ══════════════
    st.markdown('<div class="section-title">🔎 Detail Reservasi</div>', unsafe_allow_html=True)

    id_list = page_df["Reservation ID"].tolist()
    selected_id = st.selectbox("Pilih ID Reservasi:", id_list,
                               format_func=lambda x: f"{x}")

    if selected_id:
        rows_found = df[df["Reservation ID"] == selected_id]
        if not rows_found.empty:
            row = rows_found.iloc[0]
            sc  = STATUS_COLORS.get(str(row.get("Status Reservasi","")), "#aaa")

            # Safe getters
            def sv(col, default="—"):
                v = row.get(col, default)
                return default if pd.isna(v) or str(v) in ("nan","None","") else str(v)

            def iv(col, default=0):
                v = row.get(col, default)
                try: return int(float(v)) if pd.notna(v) else default
                except: return default

            rating_str  = f"⭐ {float(sv('Rating','')):.1f}" if sv("Rating") not in ["—","nan"] else "Belum ada rating"
            revenue_raw = row.get("Total Estimasi (IDR)", 0)
            revenue_str = fmt_rupiah(float(revenue_raw), short=False) if pd.notna(revenue_raw) else "—"
            catatan     = sv("Catatan Staff")
            special_req = sv("Special Request")
            if special_req in ["None","Tidak ada",""]: special_req = "Tidak ada"

            st.markdown(f"""
            <div class="detail-card">
              <div class="detail-id">{sv('Reservation ID')} &nbsp;·&nbsp; {sv('Customer ID')}</div>
              <div class="detail-name">
                {sv('Nama Customer')}
                <span class="status-pill" style="background:{sc}">{sv('Status Reservasi')}</span>
              </div>
              <div class="detail-contact">
                <span>📞 {sv('No. HP')}</span>
                <span>✉️ {sv('Email')}</span>
                <span>📅 {sv('Tanggal')} · {sv('Waktu Reservasi')}</span>
                <span>📱 {sv('Channel Booking')}</span>
              </div>
              <div class="detail-grid">
                <div class="detail-item">
                  <div class="detail-lbl">Area & Meja</div>
                  <div class="detail-val">🪑 {sv('Area Meja')} · {sv('Tipe Meja')} (No. {iv('Nomor Meja')})</div>
                </div>
                <div class="detail-item">
                  <div class="detail-lbl">Jumlah Tamu & Durasi</div>
                  <div class="detail-val">👥 {iv('Jumlah Orang')} orang · ⏱️ {iv('Durasi (menit)')} menit</div>
                </div>
                <div class="detail-item">
                  <div class="detail-lbl">Occasion</div>
                  <div class="detail-val">🎉 {sv('Occasion')}</div>
                </div>
                <div class="detail-item">
                  <div class="detail-lbl">Special Request</div>
                  <div class="detail-val">📝 {special_req}</div>
                </div>
                <div class="detail-item">
                  <div class="detail-lbl">Metode Pembayaran</div>
                  <div class="detail-val">💳 {sv('Metode Pembayaran')}</div>
                </div>
                <div class="detail-item">
                  <div class="detail-lbl">Rating Customer</div>
                  <div class="detail-val">{rating_str}</div>
                </div>
                <div class="detail-item" style="grid-column:span 2">
                  <div class="detail-lbl">Total Estimasi Revenue</div>
                  <div class="detail-val revenue-val">{revenue_str}</div>
                </div>
              </div>
              {"" if catatan == "—" else f'<div class="note-box">📌 <b>Catatan Staff:</b> {catatan}</div>'}
            </div>
            """, unsafe_allow_html=True)

# ══════════════ UPDATE STATUS ══════════════
st.markdown('<div class="section-title">🔄 Update Status Reservasi</div>', unsafe_allow_html=True)

st.markdown("""
<style>
/* ── Update Status Panel ── */
.update-panel {
    background: white;
    border-radius: 16px;
    padding: 1.8rem 2.2rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    border-top: 4px solid #d4af37;
    margin-bottom: 1.2rem;
}
.update-panel h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: #0f1923;
    margin: 0 0 1rem 0;
}
.conflict-box {
    background: #fff3cd;
    border: 1.5px solid #f0ad4e;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 0.85rem;
    color: #7a5800;
    margin-top: 10px;
}
.conflict-box b { color: #a06000; }
.success-box {
    background: #d4edda;
    border: 1.5px solid #28a745;
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 0.85rem;
    color: #155724;
    margin-top: 10px;
}
.info-row {
    display: flex; gap: 10px; flex-wrap: wrap;
    font-size: 0.83rem; color: #555;
    background: #f7f3ee;
    border-radius: 9px;
    padding: 10px 14px;
    margin-bottom: 1rem;
}
.info-row span { font-weight: 600; color: #0f1923; }
.table-avail-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
    gap: 8px;
    margin-top: 8px;
}
.table-chip {
    border-radius: 9px;
    padding: 6px 10px;
    font-size: 0.78rem;
    font-weight: 600;
    text-align: center;
}
.table-chip.busy   { background: #fde8e8; color: #c0392b; border: 1px solid #e8a9a9; }
.table-chip.free   { background: #e8fde8; color: #1a7a1a; border: 1px solid #a9e8a9; }
</style>
""", unsafe_allow_html=True)

# Inisialisasi session state untuk update
if "update_confirm" not in st.session_state:
    st.session_state.update_confirm = False
if "update_target_id" not in st.session_state:
    st.session_state.update_target_id = None
if "update_new_status" not in st.session_state:
    st.session_state.update_new_status = None
if "update_catatan" not in st.session_state:
    st.session_state.update_catatan = ""
if "update_success_msg" not in st.session_state:
    st.session_state.update_success_msg = ""

with st.container():
    # Pilih reservasi yang akan diupdate (dari semua data, bukan hanya halaman)
    all_ids = df_all["Reservation ID"].tolist()
    
    # Pilih dari filtered list jika ada, fallback ke semua data
    selectable_ids = df["Reservation ID"].tolist() if not df.empty else all_ids

    upd_col1, upd_col2 = st.columns([2, 1])
    with upd_col1:
        update_id = st.selectbox(
            "🎯 Pilih Reservasi untuk Diupdate",
            options=selectable_ids,
            key="update_select_id",
            help="Menampilkan reservasi sesuai filter aktif. Gunakan filter di atas untuk mempersempit pilihan."
        )
    with upd_col2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        quick_confirmed = st.button("🔍 Filter: Pending/Confirmed", use_container_width=True, key="quick_filter_btn")
    
    if quick_confirmed:
        # Set filter status ke Pending lalu rerun — shortcut untuk admin
        st.session_state["_quick_filter_pending"] = True
        st.rerun()

    if update_id:
        upd_row_matches = df_all[df_all["Reservation ID"] == update_id]
        if not upd_row_matches.empty:
            upd_row = upd_row_matches.iloc[0]

            current_status = str(upd_row.get("Status Reservasi", "—"))
            sc_current = STATUS_COLORS.get(current_status, "#aaa")
            tgl_val    = str(upd_row.get("Tanggal", "—"))
            waktu_val  = str(upd_row.get("Waktu Reservasi", "—"))
            nama_val   = str(upd_row.get("Nama Customer", "—"))
            meja_val   = f"Meja {int(upd_row.get('Nomor Meja', 0))} · {upd_row.get('Area Meja','—')} · {upd_row.get('Tipe Meja','—')}"
            durasi_val = int(upd_row.get("Durasi (menit)", 90))

            # Info baris ringkas
            st.markdown(f"""
            <div class="info-row">
                👤 <span>{nama_val}</span> &nbsp;|&nbsp;
                📅 <span>{tgl_val} · {waktu_val}</span> &nbsp;|&nbsp;
                🪑 <span>{meja_val}</span> &nbsp;|&nbsp;
                Status saat ini: <span style="background:{sc_current};color:white;border-radius:50px;padding:2px 10px;font-size:0.77rem;">{current_status}</span>
            </div>
            """, unsafe_allow_html=True)

            # Tentukan status yang tersedia (aturan transisi)
            STATUS_TRANSITIONS = {
                "Pending":   ["Confirmed", "Cancelled"],
                "Confirmed": ["Completed", "No-show", "Cancelled"],
                "Completed": [],
                "Cancelled": ["Pending"],   # Bisa reaktivasi
                "No-show":   ["Cancelled"],
            }
            allowed_next = STATUS_TRANSITIONS.get(current_status, [])

            if not allowed_next:
                st.markdown(f"""
                <div class="conflict-box">
                    ℹ️ Status <b>{current_status}</b> sudah final — tidak ada perubahan status yang bisa dilakukan.
                </div>
                """, unsafe_allow_html=True)
            else:
                upd_s1, upd_s2 = st.columns([1.5, 2])
                with upd_s1:
                    new_status = st.selectbox(
                        "🔄 Ubah Status Menjadi",
                        options=allowed_next,
                        key="new_status_select"
                    )
                with upd_s2:
                    catatan_input = st.text_input(
                        "📌 Catatan Staff (opsional)",
                        value="",
                        placeholder="Contoh: Tamu tiba terlambat, dipindah ke outdoor...",
                        key="catatan_update_input"
                    )

                # Cek konflik meja jika status diubah ke Confirmed
                conflict_info = []
                if new_status == "Confirmed":
                    busy_tables = get_table_availability(
                        df_all, tgl_val, waktu_val, durasi_val,
                        exclude_reservation_id=update_id
                    )
                    nomor_meja_target = upd_row.get("Nomor Meja")
                    conflict_info = [t for t in busy_tables
                                     if str(t.get("Nomor Meja")) == str(nomor_meja_target)]

                if conflict_info:
                    c = conflict_info[0]
                    st.markdown(f"""
                    <div class="conflict-box">
                        ⚠️ <b>Peringatan Konflik Meja!</b><br>
                        Meja <b>{nomor_meja_target}</b> ({upd_row.get('Area Meja','')}) 
                        sudah terpakai oleh reservasi <b>{c['Reservation ID']}</b> 
                        (Status: {c['Status']}) pada waktu yang sama 
                        (<b>{tgl_val} · {waktu_val}</b>).<br>
                        Pertimbangkan untuk memindah meja atau mengubah waktu terlebih dahulu.
                    </div>
                    """, unsafe_allow_html=True)

                    konflik_col1, konflik_col2 = st.columns(2)
                    with konflik_col1:
                        btn_tetap = st.button(
                            "⚠️ Tetap Konfirmasi (Override)",
                            use_container_width=True,
                            key="btn_override_confirm",
                            type="secondary"
                        )
                    with konflik_col2:
                        btn_batal_konflik = st.button(
                            "✖ Batalkan",
                            use_container_width=True,
                            key="btn_cancel_konflik"
                        )

                    if btn_tetap:
                        st.session_state.update_confirm   = True
                        st.session_state.update_target_id = update_id
                        st.session_state.update_new_status = new_status
                        st.session_state.update_catatan   = catatan_input
                        st.rerun()
                else:
                    btn_update = st.button(
                        f"✅ Update Status → {new_status}",
                        use_container_width=False,
                        type="primary",
                        key="btn_do_update"
                    )
                    if btn_update:
                        st.session_state.update_confirm   = True
                        st.session_state.update_target_id = update_id
                        st.session_state.update_new_status = new_status
                        st.session_state.update_catatan   = catatan_input
                        st.rerun()

# ── Eksekusi update setelah konfirmasi ──
if st.session_state.update_confirm and st.session_state.update_target_id:
    target_id  = st.session_state.update_target_id
    new_stat   = st.session_state.update_new_status
    new_cat    = st.session_state.update_catatan

    # Muat data segar (non-cached) langsung dari file
    import json as _json
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data.json"),
              "r", encoding="utf-8") as _f:
        raw = _json.load(_f)

    updated = 0
    for rec in raw:
        if rec.get("Reservation ID") == target_id:
            rec["Status Reservasi"] = new_stat
            if new_cat.strip():
                rec["Catatan Staff"] = new_cat.strip()
            updated += 1
            break

    if updated:
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data.json"),
                  "w", encoding="utf-8") as _f:
            _json.dump(raw, _f, ensure_ascii=False, indent=2)
        # Bersihkan cache agar load_data() kembali dengan data terbaru
        load_data.clear()
        st.session_state.update_success_msg = (
            f"✅ Status reservasi **{target_id}** berhasil diubah menjadi **{new_stat}**."
        )
    else:
        st.session_state.update_success_msg = f"⚠️ Reservasi {target_id} tidak ditemukan di database."

    # Reset confirm state
    st.session_state.update_confirm   = False
    st.session_state.update_target_id = None
    st.session_state.update_new_status = None
    st.session_state.update_catatan   = ""
    st.rerun()

# Tampilkan pesan sukses jika ada
if st.session_state.update_success_msg:
    msg = st.session_state.update_success_msg
    if msg.startswith("✅"):
        st.success(msg)
    else:
        st.warning(msg)
    # Auto-clear setelah ditampilkan
    st.session_state.update_success_msg = ""

# ══════════════ KETERSEDIAAN MEJA ══════════════
import datetime as _dt

st.markdown('<div class="section-title">🪑 Ketersediaan Meja</div>', unsafe_allow_html=True)

# CSS tambahan untuk section ketersediaan
st.markdown("""
<style>
/* ── Availability Section ── */
.avail-controls {
    background: white;
    border-radius: 14px;
    padding: 1.2rem 1.6rem;
    border: 1px solid rgba(0,0,0,0.07);
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    flex-wrap: wrap;
}
.avail-date-label {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #888;
    font-weight: 600;
    margin-bottom: 2px;
}
.avail-stat-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 1.2rem;
}
.avail-stat-card {
    border-radius: 12px;
    padding: 14px 16px;
    text-align: center;
    border: 1.5px solid transparent;
}
.avail-stat-card .stat-val {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
}
.avail-stat-card .stat-lbl {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
    opacity: 0.75;
}
.avail-stat-card.card-total { background: #f0f4ff; border-color: #c5d0f0; color: #1a2a6b; }
.avail-stat-card.card-busy  { background: #fde8e8; border-color: #e8a9a9; color: #c0392b; }
.avail-stat-card.card-free  { background: #e8fde8; border-color: #a9e8a9; color: #1a7a1a; }
.avail-stat-card.card-pct   { background: #fff8e1; border-color: #f0c030; color: #7a5800; }
.avail-note {
    border-radius: 9px;
    padding: 8px 14px;
    font-size: 0.8rem;
    color: #666;
    background: #f7f3ee;
    border: 1px solid #e0d6c8;
    margin-bottom: 1.2rem;
}
.area-section {
    background: white;
    border-radius: 14px;
    padding: 1.2rem 1.4rem 1rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
}
.area-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #0f1923;
    margin-bottom: 0.3rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.area-meta {
    font-size: 0.78rem;
    color: #999;
    margin-bottom: 0.8rem;
}
.area-stat-pill {
    display: inline-block;
    border-radius: 50px;
    padding: 2px 10px;
    font-size: 0.72rem;
    font-weight: 600;
    margin-left: 6px;
}
.table-avail-grid-new {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 8px;
}
.table-chip-v2 {
    border-radius: 10px;
    padding: 8px 10px;
    font-size: 0.78rem;
    font-weight: 600;
    text-align: center;
    cursor: default;
    transition: transform 0.15s ease;
    line-height: 1.4;
}
.table-chip-v2:hover { transform: translateY(-1px); }
.table-chip-v2.busy {
    background: #fde8e8;
    color: #c0392b;
    border: 1px solid #e8a9a9;
}
.table-chip-v2.free {
    background: #e8fde8;
    color: #1a7a1a;
    border: 1px solid #a9e8a9;
}
.chip-table-no { font-weight: 700; font-size: 0.82rem; }
.chip-detail   { font-size: 0.68rem; font-weight: 400; opacity: 0.85; margin-top: 2px; }
.legend-bar {
    display: flex;
    gap: 1.2rem;
    align-items: center;
    margin-bottom: 1rem;
    flex-wrap: wrap;
}
.legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 0.8rem;
    color: #555;
}
.legend-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}
</style>
""", unsafe_allow_html=True)

# ── Master table list per area (semua meja di restoran) ──
ALL_TABLES = {
    "Bar Area":     {29: "Bar Seat", 30: "Meja 2 Orang", 31: "Bar Seat", 32: "Bar Seat", 33: "Bar Seat"},
    "Garden":       {21: "Meja 8 Orang", 22: "Meja 4 Orang", 23: "Meja 6 Orang",
                     24: "Meja 6 Orang", 25: "Meja 6 Orang", 26: "Meja 6 Orang",
                     27: "Meja 4 Orang", 28: "Meja 4 Orang"},
    "Indoor":       {1: "Meja 6 Orang", 2: "Meja 4 Orang", 3: "Meja 2 Orang",
                     4: "Meja 2 Orang", 5: "Meja 4 Orang", 6: "Meja 2 Orang",
                     7: "Meja 4 Orang", 8: "Meja 2 Orang", 9: "Meja 4 Orang",
                     10: "Meja 6 Orang", 11: "Meja 4 Orang", 12: "Meja 4 Orang"},
    "Outdoor":      {13: "Meja 4 Orang", 14: "Meja 4 Orang", 15: "Meja 4 Orang",
                     16: "Meja 6 Orang", 17: "Meja 6 Orang", 18: "Meja 4 Orang",
                     19: "Meja 4 Orang", 20: "Meja 6 Orang"},
    "Private Room": {39: "Meja 10 Orang", 40: "Meja 15 Orang", 41: "Meja 20 Orang"},
    "VIP Room":     {34: "Meja 8 Orang", 35: "Meja 6 Orang", 36: "Meja 8 Orang",
                     37: "Meja 6 Orang", 38: "Meja 8 Orang"},
}

AREA_ICONS = {
    "Indoor": "🏠", "Outdoor": "🌿", "Garden": "🌺",
    "Bar Area": "🍸", "VIP Room": "⭐", "Private Room": "🔒",
}

# ── Kontrol: pilih tanggal ──
ctrl_col1, ctrl_col2 = st.columns([2, 1])
with ctrl_col1:
    st.markdown('<div class="avail-date-label">📅 Pilih Tanggal</div>', unsafe_allow_html=True)
    selected_date = st.date_input(
        "Pilih tanggal",
        value=_dt.date.today(),
        min_value=_dt.date(2026, 1, 1),
        max_value=_dt.date(2026, 12, 31),
        label_visibility="collapsed",
        key="avail_date_picker"
    )

with ctrl_col2:
    st.markdown('<div class="avail-date-label">⚡ Aksi Cepat</div>', unsafe_allow_html=True)
    jump_cols = st.columns(2)
    with jump_cols[0]:
        if st.button("Hari Ini", use_container_width=True, key="btn_jump_today"):
            st.session_state["avail_date_picker"] = _dt.date.today()
            st.rerun()
    with jump_cols[1]:
        if st.button("Besok", use_container_width=True, key="btn_jump_tomorrow"):
            st.session_state["avail_date_picker"] = _dt.date.today() + _dt.timedelta(days=1)
            st.rerun()

selected_date_str = selected_date.strftime("%Y-%m-%d")
is_today = (selected_date == _dt.date.today())
date_label = f"Hari Ini ({selected_date_str})" if is_today else selected_date_str

# ── Query reservasi aktif pada tanggal terpilih ──
active_on_date = df_all[
    (df_all["Tanggal"] == selected_date_str) &
    (df_all["Status Reservasi"].isin(["Pending", "Confirmed"]))
]

# Buat lookup: Nomor Meja → list reservasi aktif
busy_map: dict[int, list[dict]] = {}
for _, r in active_on_date.iterrows():
    mno = int(r.get("Nomor Meja", 0))
    if mno not in busy_map:
        busy_map[mno] = []
    busy_map[mno].append({
        "waktu":  str(r.get("Waktu Reservasi", "?")),
        "nama":   str(r.get("Nama Customer", "?"))[:12],
        "status": str(r.get("Status Reservasi", "?")),
    })

# ── Summary stat cards ──
total_all_tables = sum(len(t) for t in ALL_TABLES.values())
total_busy       = len(busy_map)
total_free       = total_all_tables - total_busy
pct_free         = round(total_free / total_all_tables * 100) if total_all_tables else 0

st.markdown(f"""
<div class="avail-stat-row">
    <div class="avail-stat-card card-total">
        <div class="stat-val">{total_all_tables}</div>
        <div class="stat-lbl">Total Meja</div>
    </div>
    <div class="avail-stat-card card-busy">
        <div class="stat-val">{total_busy}</div>
        <div class="stat-lbl">Terpakai</div>
    </div>
    <div class="avail-stat-card card-free">
        <div class="stat-val">{total_free}</div>
        <div class="stat-lbl">Tersedia</div>
    </div>
    <div class="avail-stat-card card-pct">
        <div class="stat-val">{pct_free}%</div>
        <div class="stat-lbl">Bebas</div>
    </div>
</div>
<div class="avail-note">
    📅 Tanggal: <b>{date_label}</b> &nbsp;·&nbsp;
    Status <b>Pending</b> &amp; <b>Confirmed</b> dihitung sebagai meja terpakai
</div>
""", unsafe_allow_html=True)

# ── Legend ──
col_leg1, col_leg2, _ = st.columns([1, 1.2, 4])
with col_leg1:
    st.markdown('<div style="display:flex;align-items:center;gap:7px;font-size:0.82rem;color:#555;">'
                '<div style="width:12px;height:12px;border-radius:50%;background:#2ecc71;flex-shrink:0;"></div>'
                ' Tersedia</div>', unsafe_allow_html=True)
with col_leg2:
    st.markdown('<div style="display:flex;align-items:center;gap:7px;font-size:0.82rem;color:#555;">'
                '<div style="width:12px;height:12px;border-radius:50%;background:#e74c3c;flex-shrink:0;"></div>'
                ' Terpakai (Confirmed / Pending)</div>', unsafe_allow_html=True)
st.markdown("<div style='margin-bottom:0.8rem;'></div>", unsafe_allow_html=True)

# ── Render per area menggunakan st.columns native ──
COLS_PER_ROW = 5

for area, tables in ALL_TABLES.items():
    icon      = AREA_ICONS.get(area, "🪑")
    busy_here = [no for no in tables if no in busy_map]
    free_here = [no for no in tables if no not in busy_map]
    total_here = len(tables)

    # Badge
    if not busy_here:
        badge = '<span style="background:#e8fde8;color:#1a7a1a;border:1px solid #a9e8a9;border-radius:50px;padding:2px 10px;font-size:0.72rem;font-weight:600;">✓ Semua bebas</span>'
    elif not free_here:
        badge = '<span style="background:#fde8e8;color:#c0392b;border:1px solid #e8a9a9;border-radius:50px;padding:2px 10px;font-size:0.72rem;font-weight:600;">✗ Penuh</span>'
    else:
        badge = (
            f'<span style="background:#e8fde8;color:#1a7a1a;border:1px solid #a9e8a9;border-radius:50px;padding:2px 10px;font-size:0.72rem;font-weight:600;">{len(free_here)} bebas</span>'
            f' &nbsp;<span style="background:#fde8e8;color:#c0392b;border:1px solid #e8a9a9;border-radius:50px;padding:2px 10px;font-size:0.72rem;font-weight:600;">{len(busy_here)} terpakai</span>'
        )

    # Header area — card tipis
    st.markdown(f"""
    <div style="background:white;border-radius:12px;padding:0.75rem 1.1rem 0.55rem;
                margin-bottom:0.5rem;border:1px solid rgba(0,0,0,0.07);
                box-shadow:0 1px 6px rgba(0,0,0,0.04);">
        <div style="font-family:'Playfair Display',serif;font-size:1rem;font-weight:700;
                    color:#0f1923;display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
            {icon} {area} &nbsp; {badge}
        </div>
        <div style="font-size:0.75rem;color:#aaa;margin-top:3px;">{total_here} meja</div>
    </div>
    """, unsafe_allow_html=True)

    # Chip grid pakai st.columns
    table_items = sorted(tables.items())
    for row_start in range(0, len(table_items), COLS_PER_ROW):
        row_items = table_items[row_start : row_start + COLS_PER_ROW]
        cols = st.columns(COLS_PER_ROW)
        for col_idx, (meja_no, tipe) in enumerate(row_items):
            with cols[col_idx]:
                if meja_no in busy_map:
                    slots    = busy_map[meja_no]
                    slot_txt = "<br>".join(
                        f"{s['waktu']} · {s['nama']}" for s in slots[:2]
                    )
                    if len(slots) > 2:
                        slot_txt += f"<br>+{len(slots)-2} lainnya"
                    st.markdown(f"""
                    <div style="background:#fde8e8;border:1.5px solid #e8a9a9;border-radius:10px;
                                padding:10px 8px;text-align:center;min-height:88px;
                                display:flex;flex-direction:column;justify-content:center;gap:3px;">
                        <div style="font-weight:700;font-size:0.8rem;color:#c0392b;">🪑 Meja {meja_no}</div>
                        <div style="font-size:0.68rem;color:#a93226;opacity:0.85;">{tipe}</div>
                        <div style="font-size:0.65rem;color:#c0392b;opacity:0.75;line-height:1.4;">{slot_txt}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background:#e8fde8;border:1.5px solid #a9e8a9;border-radius:10px;
                                padding:10px 8px;text-align:center;min-height:88px;
                                display:flex;flex-direction:column;justify-content:center;gap:3px;">
                        <div style="font-weight:700;font-size:0.8rem;color:#1a7a1a;">✓ Meja {meja_no}</div>
                        <div style="font-size:0.68rem;color:#1a7a1a;opacity:0.8;">{tipe}</div>
                        <div style="font-size:0.65rem;color:#1a7a1a;opacity:0.55;">Tersedia</div>
                    </div>
                    """, unsafe_allow_html=True)
        # Isi sisa kolom kosong di baris terakhir
        for empty_idx in range(len(row_items), COLS_PER_ROW):
            cols[empty_idx].empty()

    st.markdown("<div style='margin-bottom:1.2rem;'></div>", unsafe_allow_html=True)

st.markdown("---")
st.caption("Smart Reservation System · Manajemen Reservasi · Kelompok 3 Hana Jatmiana")
