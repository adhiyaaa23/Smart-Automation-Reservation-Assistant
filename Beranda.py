import streamlit as st
import time
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from utils import load_data, fmt_rupiah

st.set_page_config(
    page_title="Smart Automation Reservation Assistant · Mandala Rasa Restaurant Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False
if "show_admin_login" not in st.session_state:
    st.session_state.show_admin_login = False
# Admin password
ADMIN_PASSWORD = "admin123"

# ---------- Custom CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f1923 0%, #1a2a3a 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.07);
}
section[data-testid="stSidebar"] * {
    color: #e8dcc8 !important;
}

/* Main bg */
.main .block-container {
    background: #f7f3ee;
    padding: 2rem 2.5rem;
}

/* Hero */
.hero-wrap {
    background: linear-gradient(135deg, #0f1923 0%, #1a2a3a 50%, #2c3e50 100%);
    border-radius: 20px;
    padding: 60px 50px;
    color: #e8dcc8;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -40%;
    left: -20%;
    width: 60%;
    height: 200%;
    background: radial-gradient(ellipse, rgba(212,175,55,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    font-weight: 700;
    margin: 0 0 0.5rem;
    letter-spacing: -1px;
    color: #e8dcc8;
}
.hero-sub {
    font-size: 1.1rem;
    color: rgba(232,220,200,0.7);
    margin: 0 0 2rem;
    font-weight: 300;
}
.hero-badge {
    display: inline-block;
    background: rgba(212,175,55,0.2);
    border: 1px solid rgba(212,175,55,0.5);
    color: #d4af37;
    border-radius: 50px;
    padding: 6px 20px;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 1px;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
}

/* Nav cards */
.nav-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-top: 2rem;
}
.nav-card {
    background: white;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid rgba(0,0,0,0.06);
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    text-decoration: none;
    display: block;
}
.nav-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.1);
    border-color: #d4af37;
}
.nav-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}
.nav-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #0f1923;
    margin-bottom: 0.5rem;
}
.nav-desc {
    color: #666;
    font-size: 0.92rem;
    line-height: 1.6;
}

/* Stat mini */
.mini-stats {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
    flex-wrap: wrap;
}
.mini-stat {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 14px 20px;
    flex: 1;
    min-width: 140px;
    text-align: center;
}
.mini-stat-val {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #d4af37;
}
.mini-stat-lbl {
    font-size: 0.78rem;
    color: rgba(232,220,200,0.6);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 2px;
}

/* Admin login input styling */
.stTextInput > div > div > input {
    border-radius: 10px !important;
    border: 1.5px solid #e0d6c8 !important;
    font-size: 0.93rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #d4af37 !important;
    box-shadow: 0 0 0 3px rgba(212,175,55,0.12) !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar branding & Auth
with st.sidebar:
    st.markdown("### 🍽️ Smart Reservation")
    st.markdown("---")

    st.page_link("Beranda.py", label="🏠 Beranda")
    if st.session_state.admin_logged_in:
        st.page_link("pages/1_Dashboard_Analytics.py",    label="📊 Dashboard Analytics")
        st.page_link("pages/2_Reservation_Management.py", label="📋 Manajemen Reservasi")
    st.page_link("pages/3_AI_Assistant.py", label="🤖 AI Reservation Assistant")
    st.markdown("---")

    # Admin status indicator
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
    st.markdown("<small style='opacity:0.6'>v1.0 · AI Assistant · Gemini Powered</small>", unsafe_allow_html=True)

# ---- Admin button & login panel ----
st.markdown("""
<style>
.admin-topbar {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 0.5rem;
}
.admin-topbar .stButton > button {
    border-radius: 999px !important;
    background: linear-gradient(135deg, #d4af37, #f7e6a4) !important;
    color: #0f1923 !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 0.4rem 1.1rem !important;
    border: none !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.1) !important;
    white-space: nowrap !important;
}
.admin-topbar .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 14px rgba(0,0,0,0.15) !important;
}
.admin-login-panel {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="admin-topbar">', unsafe_allow_html=True)
if st.session_state.admin_logged_in:
    if st.button("🚪 Logout", key="top_logout_button"):
        st.session_state.admin_logged_in = False
        st.session_state.show_admin_login = False
        st.rerun()
else:
    if st.button("🔐 Admin Login", key="top_login_button"):
        st.session_state.show_admin_login = not st.session_state.show_admin_login
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.show_admin_login and not st.session_state.admin_logged_in:
    _, login_col, _ = st.columns([1, 2, 1])
    with login_col:
        st.markdown("##### 🔐 Login Admin")
        pwd = st.text_input("Password", type="password", placeholder="Masukkan password admin...", key="top_admin_pwd", label_visibility="collapsed")
        btn_cols = st.columns([3, 2])
        with btn_cols[0]:
            if st.button("Masuk sebagai Admin", key="top_login_submit", use_container_width=True):
                if pwd == ADMIN_PASSWORD:
                    with st.spinner("Memproses login admin..."):
                        time.sleep(0.5)
                        st.session_state.admin_logged_in = True
                        st.session_state.show_admin_login = False
                        st.rerun()
                else:
                    st.error("❌ Password salah!")
        with btn_cols[1]:
            if st.button("Batal", key="top_login_cancel", use_container_width=True):
                st.session_state.show_admin_login = False
                st.rerun()

# ---- Hero (admin only) ----
if st.session_state.admin_logged_in:
    _df_hero    = load_data()
    _total_rsv  = len(_df_hero)
    _total_rev  = _df_hero["Total Estimasi (IDR)"].sum()
    _avg_rating = _df_hero["Rating"].mean()
    _total_cust = _df_hero["Customer ID"].nunique()
    _completed  = int((_df_hero["Status Reservasi"] == "Completed").sum())

    st.markdown(f"""
<div class="hero-wrap">
    <div class="hero-badge" style="background: rgba(212,175,55,0.15); border-color: rgba(212,175,55,0.35); color: #d4af37;">✦ Mandala Rasa</div>
    <h1 class="hero-title">Mandala Rasa</h1>
    <p class="hero-sub">Platform Cerdas Manajemen Reservasi &amp; Analitik Bisnis Restoran</p>
    <p style="color: #d4af37; font-size: 0.9rem; font-weight: 600; margin-top: 0.5rem;">➤ 🔓 Mode Admin Aktif</p>
    <div class="mini-stats">
        <div class="mini-stat">
            <div class="mini-stat-val">{_total_rsv:,}</div>
            <div class="mini-stat-lbl">Total Reservasi</div>
        </div>
        <div class="mini-stat">
            <div class="mini-stat-val">{fmt_rupiah(_total_rev)}</div>
            <div class="mini-stat-lbl">Total Revenue</div>
        </div>
        <div class="mini-stat">
            <div class="mini-stat-val">{_avg_rating:.2f}</div>
            <div class="mini-stat-lbl">Avg Rating</div>
        </div>
        <div class="mini-stat">
            <div class="mini-stat-val">{_total_cust:,}</div>
            <div class="mini-stat-lbl">Total Pelanggan</div>
        </div>
        <div class="mini-stat">
            <div class="mini-stat-val">{_completed:,}</div>
            <div class="mini-stat-lbl">Completed</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- Nav Cards ----
if st.session_state.admin_logged_in:
    # Show all three cards for admin
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">📊</div>
            <div class="nav-title">Dashboard Analytics</div>
            <div class="nav-desc">Pantau KPI, tren reservasi, revenue, dan insight pelanggan secara real-time.</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/1_Dashboard_Analytics.py", label="→ Buka Dashboard", use_container_width=True)

    with col2:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">📋</div>
            <div class="nav-title">Manajemen Reservasi</div>
            <div class="nav-desc">Cari, filter, lihat detail, dan ekspor data reservasi pelanggan dengan mudah.</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/2_Reservation_Management.py", label="→ Kelola Reservasi", use_container_width=True)

    with col3:
        st.markdown("""
        <div class="nav-card">
            <div class="nav-icon">🤖</div>
            <div class="nav-title">AI Reservation Assistant</div>
            <div class="nav-desc">Chatbot AI berbasis Gemini untuk reservasi, cek status, dan info restoran.</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/3_AI_Assistant.py", label="→ Mulai Chat", use_container_width=True)
else:
    # Show elegant welcome hero for customer
    st.markdown("""
    <style>
    .welcome-hero {
        background: linear-gradient(135deg, #0f1923 0%, #1a2a3a 60%, #1e3a2f 100%);
        border-radius: 20px;
        padding: 56px 48px 48px;
        text-align: center;
        margin: 0.5rem 0 2rem;
        position: relative;
        overflow: hidden;
    }
    .welcome-hero::before {
        content: \'\';
        position: absolute;
        top: -30%;
        right: -10%;
        width: 50%;
        height: 180%;
        background: radial-gradient(ellipse, rgba(46,204,113,0.10) 0%, transparent 70%);
        pointer-events: none;
    }
    .welcome-hero::after {
        content: \'\';
        position: absolute;
        bottom: -20%;
        left: -10%;
        width: 40%;
        height: 140%;
        background: radial-gradient(ellipse, rgba(212,175,55,0.07) 0%, transparent 70%);
        pointer-events: none;
    }
    .welcome-badge {
        display: inline-block;
        background: rgba(46,204,113,0.15);
        border: 1px solid rgba(46,204,113,0.35);
        color: #2ecc71;
        border-radius: 50px;
        padding: 6px 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 1.4rem;
    }
    .welcome-title {
        font-family: \'Playfair Display\', serif;
        font-size: 2.6rem;
        font-weight: 700;
        color: #e8dcc8;
        margin: 0 0 0.6rem;
        letter-spacing: -0.5px;
        line-height: 1.2;
    }
    .welcome-title span { color: #d4af37; }
    .welcome-sub {
        color: rgba(232,220,200,0.65);
        font-size: 1.05rem;
        font-weight: 300;
        margin: 0 0 2rem;
        line-height: 1.7;
        max-width: 480px;
        display: inline-block;
    }
    .welcome-features {
        display: flex;
        justify-content: center;
        gap: 1rem;
        flex-wrap: wrap;
        margin-bottom: 2rem;
    }
    .welcome-feature-chip {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 50px;
        padding: 8px 18px;
        font-size: 0.83rem;
        color: rgba(232,220,200,0.8);
    }
    .welcome-cta-wrap {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 28px 32px;
        max-width: 420px;
        margin: 0 auto 0.5rem;
    }
    .welcome-cta-icon { font-size: 2.4rem; margin-bottom: 0.6rem; }
    .welcome-cta-title {
        font-family: \'Playfair Display\', serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #e8dcc8;
        margin-bottom: 0.4rem;
    }
    .welcome-cta-desc {
        color: rgba(232,220,200,0.55);
        font-size: 0.88rem;
        line-height: 1.6;
    }
    </style>
    <div class="welcome-hero">
        <div class="welcome-badge">✦ Selamat Datang</div>
        <h1 class="welcome-title">Nikmati Pengalaman Makan<br>di <span>Mandala Rasa</span></h1>
        <p class="welcome-sub">Reservasi meja dengan mudah, cepat, dan nyaman — langsung melalui asisten AI kami yang siap membantu 24/7.</p>
        <div class="welcome-features">
            <div class="welcome-feature-chip">⚡ Reservasi Instan</div>
            <div class="welcome-feature-chip">🤖 AI-Powered</div>
            <div class="welcome-feature-chip">📋 Cek Status Real-time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_center = st.columns([1, 1.4, 1])
    with col_center[1]:
        st.markdown("""
        <div style="
            background: white;
            border-radius: 16px;
            padding: 2rem 2rem 1.4rem;
            text-align: center;
            border: 1px solid rgba(0,0,0,0.07);
            box-shadow: 0 4px 20px rgba(0,0,0,0.07);
            margin-top: 0.5rem;
        ">
            <div style="font-size: 2.2rem; margin-bottom: 0.5rem;">🤖</div>
            <div style="font-family: 'Playfair Display', serif; font-size: 1.2rem; font-weight: 700; color: #0f1923; margin-bottom: 0.4rem;">SARA — AI Reservation Assistant</div>
            <div style="color: #777; font-size: 0.87rem; line-height: 1.6; margin-bottom: 1.3rem;">Buat reservasi, cek ketersediaan meja, atau tanyakan informasi restoran kepada asisten AI kami.</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/3_AI_Assistant.py", label="✦ Mulai Reservasi Sekarang", use_container_width=True)

st.markdown("---")
st.caption("© 2026 Smart Reservation Assistant · Kelompok 3 Hana Jatmiana · Dibuat dengan menggunakan Streamlit")
