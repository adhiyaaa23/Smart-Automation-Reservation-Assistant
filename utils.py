"""
utils.py – shared data loader and helpers
"""
import pandas as pd
import streamlit as st
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_json(DATA_PATH)
    df["Tanggal Reservasi"] = pd.to_datetime(df["Tanggal"])
    df["Bulan"] = df["Tanggal Reservasi"].dt.month
    df["Nama Bulan"] = df["Tanggal Reservasi"].dt.strftime("%b")
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df["Total Estimasi (IDR)"] = pd.to_numeric(df["Total Estimasi (IDR)"], errors="coerce")
    return df

MONTH_MAP = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"Mei",6:"Jun",
             7:"Jul",8:"Agu",9:"Sep",10:"Okt",11:"Nov",12:"Des"}

def fmt_rupiah(value: float, short: bool = True) -> str:
    """
    Format angka rupiah secara adaptif:
      short=True  → label ringkas: "Rp 3,72 M" / "Rp 310 Jt" / "Rp 125 Rb"
      short=False → angka penuh:   "Rp 3.720.000.000"
    """
    if value is None or (hasattr(value, '__class__') and value.__class__.__name__ == 'float' and value != value):
        return "—"
    value = float(value)
    if not short:
        return "Rp " + f"{int(value):,}".replace(",", ".")
    if value >= 1_000_000_000:
        v = value / 1_000_000_000
        return f"Rp {v:.2f} M" if v < 10 else f"Rp {v:.1f} M"
    if value >= 1_000_000:
        return f"Rp {value/1_000_000:.1f} Jt"
    if value >= 1_000:
        return f"Rp {value/1_000:.0f} Rb"
    return f"Rp {int(value):,}"

STATUS_COLORS = {
    "Confirmed":  "#2ecc71",
    "Completed":  "#3498db",
    "Pending":    "#f39c12",
    "Cancelled":  "#e74c3c",
    "No-show":    "#9b59b6",
}

GOLD  = "#d4af37"
DARK  = "#0f1923"
CREAM = "#e8dcc8"

COMMON_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
section[data-testid="stSidebar"] {
    background: linear-gradient(160deg,#0f1923 0%,#1a2a3a 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.07);
}
section[data-testid="stSidebar"] * { color: #e8dcc8 !important; }
.main .block-container { background:#f7f3ee; padding:2rem 2.5rem; }

/* KPI Card */
.kpi-card {
    background: white;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    border-left: 4px solid var(--accent,#d4af37);
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}
.kpi-label { font-size:0.78rem; text-transform:uppercase; letter-spacing:1px;
             color:#888; font-weight:600; margin-bottom:4px; }
.kpi-value { font-family:'Playfair Display',serif; font-size:2rem;
             font-weight:700; color:#0f1923; line-height:1.1; }
.kpi-sub   { font-size:0.8rem; color:#aaa; margin-top:4px; }

/* Section title */
.section-title {
    font-family:'Playfair Display',serif;
    font-size:1.35rem; font-weight:700;
    color:#0f1923; margin:2rem 0 1rem;
    display:flex; align-items:center; gap:10px;
}
.section-title::after {
    content:''; flex:1; height:1px;
    background:linear-gradient(to right,#d4af37,transparent);
}

/* Badge */
.badge {
    display:inline-block; border-radius:50px;
    padding:3px 12px; font-size:0.78rem; font-weight:600;
}
.back-button-wrapper {
    display:flex; justify-content:center; margin-top:1.5rem;
}
.back-button {
    display:inline-flex; align-items:center; gap:0.75rem;
    padding:0.95rem 1.4rem; border-radius:999px;
    background: linear-gradient(135deg,#d4af37,#f7e6a4);
    color:#0f1923; text-decoration:none; font-weight:700;
    box-shadow:0 14px 32px rgba(212,175,55,0.18);
    transition:transform .18s ease, box-shadow .18s ease, opacity .18s ease;
}
.back-button:hover {
    transform:translateY(-2px);
    box-shadow:0 18px 38px rgba(212,175,55,0.22);
    opacity:0.98;
}
.back-button-icon {
    display:inline-flex; align-items:center; justify-content:center;
    width:2.2rem; height:2.2rem; border-radius:50%;
    background:rgba(15,25,35,0.08); color:#0f1923;
    font-size:1.05rem;
}
</style>
"""

import json

def save_data(df: pd.DataFrame) -> bool:
    """Simpan perubahan DataFrame kembali ke data.json."""
    try:
        # Hapus kolom turunan yang ditambahkan saat load
        cols_to_drop = [c for c in ["Tanggal Reservasi", "Bulan", "Nama Bulan"] if c in df.columns]
        df_save = df.drop(columns=cols_to_drop)
        records = df_save.to_dict(orient="records")
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2, default=str)
        # Bersihkan cache agar data terbaru dimuat ulang
        load_data.clear()
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


def get_table_availability(df: pd.DataFrame, tanggal: str, waktu: str,
                            durasi: int, exclude_reservation_id: str = None) -> list[dict]:
    """
    Kembalikan daftar nomor meja yang sedang terpakai pada tanggal+waktu tertentu.
    Digunakan untuk cek konflik sebelum mengkonfirmasi status reservasi.
    """
    from datetime import datetime, timedelta

    try:
        t_target = datetime.strptime(f"{tanggal} {waktu}", "%Y-%m-%d %H:%M")
    except Exception:
        return []

    busy = []
    for _, row in df.iterrows():
        if exclude_reservation_id and row.get("Reservation ID") == exclude_reservation_id:
            continue
        if str(row.get("Status Reservasi", "")) in ("Cancelled", "No-show", "Completed"):
            continue
        try:
            t_row = datetime.strptime(f"{row['Tanggal']} {row['Waktu Reservasi']}", "%Y-%m-%d %H:%M")
            dur_row = int(row.get("Durasi (menit)", 90))
            t_end_row = t_row + timedelta(minutes=dur_row)
            t_end_target = t_target + timedelta(minutes=durasi)

            # Cek overlap waktu
            if t_target < t_end_row and t_end_target > t_row:
                busy.append({
                    "Nomor Meja": row.get("Nomor Meja"),
                    "Area Meja": row.get("Area Meja"),
                    "Reservation ID": row.get("Reservation ID"),
                    "Status": row.get("Status Reservasi"),
                })
        except Exception:
            continue
    return busy
