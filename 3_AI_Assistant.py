import streamlit as st
import sys, os, json, re, base64
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import load_data, COMMON_CSS
from dotenv import load_dotenv

# ─────────────────── LOGO HELPER ───────────────────
def _load_logo_b64() -> str:
    """Load Sara_logo.png as base64 string for inline HTML embedding."""
    logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Sara_logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

LOGO_B64 = _load_logo_b64()
LOGO_IMG = (
    f'<img src="data:image/png;base64,{LOGO_B64}" '
    f'style="width:100%;height:100%;object-fit:cover;border-radius:50%;">'
    if LOGO_B64 else "🤖"
)

# Initialize session state
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

st.set_page_config(page_title="SARA - Smart AI Reservation Assistant",
                   page_icon="🤖", layout="wide")

# ─────────────────── CSS ───────────────────
st.markdown(COMMON_CSS, unsafe_allow_html=True)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

.main .block-container {
    padding: 1.5rem 2rem !important;
    background: #f4f0eb !important;
    max-width: 1400px !important;
}

/* ── Header ── */
.chat-header {
    background: linear-gradient(135deg, #0f1923 0%, #1c2e40 60%, #2c3e50 100%);
    border-radius: 16px;
    padding: 22px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    box-shadow: 0 6px 24px rgba(15,25,35,0.16);
}
.chat-header-text .badge {
    font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase;
    color: #d4af37; font-weight: 700; margin-bottom: 4px; display: block;
}
.chat-header-text h1 {
    font-family: 'Playfair Display', serif; font-size: 1.6rem;
    margin: 0 0 3px; color: #e8dcc8; line-height: 1.1;
}
.chat-header-text p { margin: 0; color: rgba(232,220,200,0.5); font-size: 0.82rem; }
.chat-header-icon {
    width: 54px; height: 54px; border-radius: 50%;
    background: rgba(212,175,55,0.15); border: 1.5px solid rgba(212,175,55,0.35);
    overflow: hidden; flex-shrink: 0;
}

/* ── Quick action pills ── */
.stButton > button {
    border-radius: 50px !important;
    border: 1.5px solid rgba(212,175,55,0.5) !important;
    background: white !important;
    color: #0f1923 !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    padding: 5px 8px !important;
    transition: all .18s !important;
}
.stButton > button:hover {
    background: #d4af37 !important;
    color: white !important;
    border-color: #d4af37 !important;
    box-shadow: 0 3px 12px rgba(212,175,55,0.3) !important;
}

/* ── Chat window ── */
.chat-window {
    background: white;
    border-radius: 16px;
    padding: 18px 16px;
    min-height: 380px;
    max-height: 480px;
    overflow-y: auto;
    box-shadow: 0 2px 14px rgba(0,0,0,0.06);
    border: 1px solid rgba(212,175,55,0.1);
    margin-bottom: 0.75rem;
    scroll-behavior: smooth;
}

/* ── Bubbles ── */
.bubble-wrap-user  { display:flex; justify-content:flex-end;  margin: 7px 0; }
.bubble-wrap-bot   { display:flex; justify-content:flex-start; margin: 7px 0; gap: 8px; align-items: flex-start; }

.bubble-user {
    background: linear-gradient(135deg, #0f1923, #1c2e40);
    color: #e8dcc8; border-radius: 16px 16px 4px 16px;
    padding: 9px 14px; max-width: 72%;
    font-size: 0.88rem; line-height: 1.6;
    box-shadow: 0 2px 10px rgba(15,25,35,0.15);
}
.bubble-user .sender {
    font-size:0.62rem; font-weight:700; letter-spacing:1px;
    text-transform:uppercase; color:rgba(232,220,200,0.45);
    margin-bottom:3px; text-align:right;
}
.bot-avatar {
    width: 32px; height: 32px; border-radius: 50%; flex-shrink: 0;
    background: linear-gradient(135deg, #d4af37, #f0d060);
    overflow: hidden; margin-top: 3px;
    box-shadow: 0 2px 6px rgba(212,175,55,0.25);
}
.bubble-bot {
    background: white; color: #1a1a2e;
    border-radius: 4px 16px 16px 16px;
    padding: 9px 14px; max-width: 75%;
    font-size: 0.88rem; line-height: 1.65;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border: 1px solid rgba(212,175,55,0.15);
}
.bubble-bot .sender {
    font-size:0.62rem; font-weight:700; letter-spacing:1px;
    text-transform:uppercase; color:#d4af37; margin-bottom:3px;
}

/* ── Input ── */
.stTextInput > div > div > input {
    border-radius: 50px !important;
    border: 1.5px solid rgba(212,175,55,0.3) !important;
    padding: 0.5rem 1.1rem !important;
    font-size: 0.9rem !important;
    background: white !important;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05) !important;
}
.stTextInput > div > div > input:focus {
    border-color: #d4af37 !important;
    box-shadow: 0 0 0 3px rgba(212,175,55,0.1) !important;
}

/* ── Info panel ── */
.info-card {
    background: white; border-radius: 12px;
    padding: 1rem 1.1rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border-top: 3px solid #d4af37;
    margin-bottom: 0.8rem;
}
.info-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 0.88rem; font-weight: 700;
    color: #0f1923; margin-bottom: 8px;
}
.example-item {
    background: #f7f3ee; border-radius: 7px;
    padding: 6px 9px; margin-bottom: 5px;
    font-size: 0.73rem; color: #555;
    border-left: 2px solid #d4af37;
}
.example-item b { color: #0f1923; display: block; margin-bottom: 1px; font-size: 0.73rem; }
.status-row { display:flex; align-items:center; gap:7px; margin-bottom:5px; }
.status-pill2 {
    border-radius:50px; padding:2px 9px;
    font-size:0.65rem; font-weight:700; color:white; white-space:nowrap;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────── SIDEBAR ───────────────────
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
""")
    st.markdown("---")
    st.markdown("<small style='opacity:.45'>v1.0 · AI Assistant · Gemini Powered</small>",
                unsafe_allow_html=True)

# ─────────────────── DATA & CONSTANTS ───────────────────
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

df_reservasi = load_data()

RESTAURANT_INFO = {
    "nama": "Mandala Rasa",
    "jam_operasional": "Senin–Minggu, 10:00–22:00 WIB",
    "area": ["Indoor", "Outdoor", "Garden", "Bar Area", "VIP Room", "Private Room"],
    "fasilitas": ["WiFi gratis", "Area parkir luas", "Smoking area terpisah",
                  "Live music Jumat–Sabtu mulai 19:00",
                  "Private room untuk acara eksklusif",
                  "Aksesibel untuk pengguna kursi roda"],
    "kebijakan": [
        "Reservasi dibuat min. 2 jam sebelum kedatangan",
        "Pembatalan gratis jika dilakukan H-1",
        "No-show 3x akan masuk daftar blacklist",
        "Deposit 50% untuk VIP Room & Private Room",
        "Hewan peliharaan tidak diizinkan masuk",
    ],
    "menu_unggulan": ["Sate Maranggi Spesial", "Nasi Goreng Wagyu",
                      "Premium Grill Platter", "Signature Mocktail"],
    "kapasitas": {"Indoor": 80, "Outdoor": 60, "Garden": 80,
                  "Bar Area": 40, "VIP Room": 60, "Private Room": 120},
}

SYSTEM_PROMPT = """Kamu adalah AI Reservation Assistant bernama "Sara" untuk restoran Mandala Rasa.
Kamu berbicara dalam Bahasa Indonesia yang ramah, hangat, dan profesional.

Tugas utamamu:
1. MEMBUAT RESERVASI — Kumpulkan: nama, jumlah orang, tanggal, waktu, area pilihan, occasion, special request. Konfirmasi semua detail sebelum memproses.
2. CEK RESERVASI — Minta nama lengkap atau ID reservasi, lalu tampilkan detail.
3. INFO RESTORAN — Jawab pertanyaan seputar jam operasional, area, fasilitas, kebijakan, menu.

Info Restoran Mandala Rasa:
- Jam: Senin–Minggu 10:00–22:00 WIB (tidak tutup hari libur nasional kecuali Lebaran)
- Area: Indoor (80 pax), Outdoor (60), Garden (80), Bar Area (40), VIP Room (60), Private Room (120)
- Fasilitas: WiFi gratis, Parkir luas, Smoking area, Live music Jum–Sab 19:00, Aksesibel kursi roda
- Kebijakan: Reservasi min 2 jam sebelumnya. Batal gratis H-1. No-show 3x → blacklist. Deposit 50% untuk VIP/Private.
- Menu andalan: Sate Maranggi Spesial, Nasi Goreng Wagyu, Premium Grill Platter, Signature Mocktail

Panduan menjawab:
- Gunakan emoji secukupnya agar pesan terasa hidup
- Jika ada info yang kurang untuk reservasi, tanya dengan sopan
- Berikan jawaban yang terstruktur dan mudah dibaca
- Akhiri setiap percakapan dengan tawaran bantuan lanjutan"""

# ─────────────────── TOOLS ───────────────────
def cek_reservasi_tool(query: str) -> dict:
    q = query.strip().lower()
    mask = (
        df_reservasi["Nama Customer"].str.lower().str.contains(q, na=False) |
        df_reservasi["Reservation ID"].str.lower().str.contains(q, na=False) |
        df_reservasi["Customer ID"].str.lower().str.contains(q, na=False)
    )
    result = df_reservasi[mask].head(3)
    if result.empty:
        return {"found": False}
    rows = []
    for _, r in result.iterrows():
        rows.append({
            "id": r["Reservation ID"], "nama": r["Nama Customer"],
            "tanggal": str(r["Tanggal"]), "waktu": str(r["Waktu Reservasi"]),
            "area": r["Area Meja"], "pax": int(r["Jumlah Orang"]),
            "status": r["Status Reservasi"], "occasion": r["Occasion"],
        })
    return {"found": True, "reservations": rows}

def buat_reservasi_tool(nama, pax, tanggal, waktu,
                        area="Indoor", occasion="Casual Dining",
                        special_request="Tidak ada"):
    import random
    new_id = f"RSV{random.randint(10000, 99999):05d}"
    return {
        "success": True, "reservation_id": new_id,
        "detail": {"nama": nama, "pax": pax, "tanggal": tanggal,
                   "waktu": waktu, "area": area, "occasion": occasion,
                   "special_request": special_request, "status": "Confirmed"},
    }

# ─────────────────── GEMINI CALL ───────────────────
def call_gemini(messages: list) -> str:
    import urllib.request, json as jm, traceback

    url = ("https://generativelanguage.googleapis.com/v1beta/"
           "models/gemini-2.5-flash:generateContent"
           f"?key={GEMINI_API_KEY}")

    # Build contents — filter out consecutive same-role messages
    contents = []
    for m in messages:
        role = "user" if m["role"] == "user" else "model"
        # Gemini requires alternating user/model; merge if same role
        if contents and contents[-1]["role"] == role:
            contents[-1]["parts"][0]["text"] += "\n" + m["content"]
        else:
            contents.append({"role": role, "parts": [{"text": m["content"]}]})

    # Must start with user turn
    if contents and contents[0]["role"] == "model":
        contents = contents[1:]

    payload = jm.dumps({
        "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
        "contents": contents,
        "generationConfig": {
            "temperature": 0.75,
            "maxOutputTokens": 1024,
            "topP": 0.9,
        }
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = jm.loads(resp.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        return f"⚠️ Gemini API error {e.code}: {body[:200]}"
    except Exception:
        return "⚠️ " + traceback.format_exc(limit=2)

# ─────────────────── HEURISTIC FALLBACK ───────────────────
def detect_intent(msg):
    m = msg.lower()
    if any(k in m for k in ["reservasi","pesan","booking","book","mau makan",
                             "ingin makan","duduk","meja"]):
        return "buat_reservasi"
    if any(k in m for k in ["cek","status","check","konfirmasi","lihat reservasi"]):
        return "cek_reservasi"
    if any(k in m for k in ["jam","buka","tutup","area","fasilitas","kebijakan",
                             "info","menu","parkir","wifi","kapasitas"]):
        return "info_restoran"
    if any(k in m for k in ["halo","hai","hello","hi","selamat","assalamualaikum",
                             "apa kabar","good morning","good evening"]):
        return "greeting"
    return "general"

def extract_params(msg):
    params = {}
    nm = re.search(r"(?:nama|atas nama|an\.?)\s+([A-Za-z][a-zA-Z\s]{2,30})",
                   msg, re.IGNORECASE)
    if nm: params["nama"] = nm.group(1).strip()
    px = re.search(r"(\d+)\s*(?:orang|pax|tamu|person|guests?)", msg, re.IGNORECASE)
    if px: params["pax"] = int(px.group(1))
    dt = re.search(r"(\d{1,2})[/\-](\d{1,2})(?:[/\-](\d{2,4}))?", msg)
    if dt:
        d,mo = dt.group(1), dt.group(2)
        yr = dt.group(3) or "2025"
        yr = yr if len(yr)==4 else "20"+yr
        params["tanggal"] = f"{yr}-{mo.zfill(2)}-{d.zfill(2)}"
    tm = re.search(r"(\d{1,2})[:\.](\d{2})\s*(?:WIB)?|pukul\s+(\d{1,2})[:\.]?(\d{0,2})",
                   msg, re.IGNORECASE)
    if tm:
        h = tm.group(3) or tm.group(1)
        mn = tm.group(4) or tm.group(2) or "00"
        params["waktu"] = f"{h.zfill(2)}:{mn.zfill(2)}"
    for a in RESTAURANT_INFO["area"]:
        if a.lower() in msg.lower(): params["area"] = a; break
    occ_map = {"birthday":"Birthday","ulang tahun":"Birthday",
               "anniversary":"Anniversary","bisnis":"Business Meeting",
               "meeting":"Business Meeting","rapat":"Business Meeting",
               "romantis":"Date Night","date":"Date Night",
               "keluarga":"Family Gathering","family":"Family Gathering",
               "arisan":"Arisan","wisuda":"Wisuda","lamaran":"Lamaran"}
    for k,v in occ_map.items():
        if k in msg.lower(): params["occasion"] = v; break
    return params

def heuristic_response(msg):
    intent = detect_intent(msg)
    params = extract_params(msg)

    if intent == "greeting":
        return ("Halo! Selamat datang di **Mandala Rasa** 🍽️\n\n"
                "Saya **Sara**, asisten reservasi Anda. Ada yang bisa saya bantu?\n\n"
                "• 🗓️ **Buat reservasi** meja\n"
                "• 🔍 **Cek status** reservasi\n"
                "• ℹ️ **Info restoran** (jam, area, fasilitas, kebijakan)")

    if intent == "cek_reservasi":
        q = re.sub(r"(cek|status|check|reservasi|detail|atas nama|nama)\s*",
                   "", msg, flags=re.IGNORECASE).strip()
        if not q or len(q) < 2:
            return "Silakan sebutkan **nama lengkap** atau **ID reservasi** Anda, ya! 😊\nContoh: *cek reservasi atas nama Budi*"
        result = cek_reservasi_tool(q)
        if not result["found"]:
            return (f"🔍 Maaf, reservasi atas nama/ID **\"{q}\"** tidak ditemukan.\n\n"
                    "Pastikan penulisan nama sudah benar, atau coba masukkan ID reservasi "
                    "yang tertera di konfirmasi (contoh: RSV00001).")
        rows = result["reservations"]
        resp = f"✅ Ditemukan **{len(rows)} reservasi**:\n\n"
        for r in rows:
            icons = {"Confirmed":"🟢","Completed":"🔵","Pending":"🟡",
                     "Cancelled":"🔴","No-show":"🟣"}
            ic = icons.get(r["status"], "⚪")
            resp += (f"**{r['id']}** · {r['nama']}\n"
                     f"📅 {r['tanggal']} pukul {r['waktu']} · 👥 {r['pax']} orang\n"
                     f"🪑 {r['area']} · 🎉 {r['occasion']}\n"
                     f"Status: {ic} **{r['status']}**\n\n")
        return resp.strip()

    if intent == "buat_reservasi":
        missing = []
        if "nama"    not in params: missing.append("nama Anda")
        if "pax"     not in params: missing.append("jumlah tamu")
        if "tanggal" not in params: missing.append("tanggal (format DD/MM)")
        if "waktu"   not in params: missing.append("waktu (contoh: 19:00)")
        if missing:
            return ("Saya siap membantu reservasi Anda! 🗓️\n\n"
                    "Mohon lengkapi informasi berikut:\n"
                    + "".join(f"• {m}\n" for m in missing)
                    + "\n💡 **Contoh:** *Reservasi atas nama Sinta, 4 orang, "
                      "20/07, jam 19:00, area Garden, untuk anniversary*")
        result = buat_reservasi_tool(**{k: params[k] for k in params if k in
                                        ["nama","pax","tanggal","waktu","area","occasion"]})
        d = result["detail"]
        return (f"🎉 **Reservasi berhasil dibuat!**\n\n"
                f"┌ ID Reservasi: **`{result['reservation_id']}`**\n"
                f"├ 👤 Nama: {d['nama']}\n"
                f"├ 👥 Tamu: {d['pax']} orang\n"
                f"├ 📅 Tanggal: {d['tanggal']} pukul {d['waktu']}\n"
                f"├ 🪑 Area: {d['area']}\n"
                f"├ 🎉 Occasion: {d['occasion']}\n"
                f"└ ✅ Status: **Confirmed**\n\n"
                "Simpan ID reservasi Anda. Konfirmasi akan dikirim via WhatsApp. "
                "Ada yang ingin ditambahkan? 😊")

    if intent == "info_restoran":
        m = msg.lower()
        info = RESTAURANT_INFO
        if any(k in m for k in ["jam","buka","tutup","operasional"]):
            return (f"🕐 **Jam Operasional Mandala Rasa:**\n\n"
                    f"**{info['jam_operasional']}**\n\n"
                    "Kami buka setiap hari, termasuk hari libur nasional "
                    "(kecuali Lebaran Hari H).")
        if any(k in m for k in ["area","meja","tempat","duduk","vip","private","kapasitas"]):
            areas = "\n".join(f"• **{a}** — kapasitas ±{info['kapasitas'].get(a,'?')} orang"
                              for a in info["area"])
            return f"🪑 **Area yang Tersedia di Mandala Rasa:**\n\n{areas}"
        if any(k in m for k in ["fasilitas","wifi","parkir","musik","aksesibel","smoking"]):
            fac = "\n".join(f"• {f}" for f in info["fasilitas"])
            return f"✨ **Fasilitas Mandala Rasa:**\n\n{fac}"
        if any(k in m for k in ["kebijakan","aturan","deposit","cancel","batal","no-show"]):
            pol = "\n".join(f"• {p}" for p in info["kebijakan"])
            return f"📜 **Kebijakan Reservasi:**\n\n{pol}"
        if any(k in m for k in ["menu","makanan","minuman","rekomendasi","recommend"]):
            men = "\n".join(f"• {m2}" for m2 in info["menu_unggulan"])
            return (f"🍽️ **Menu Andalan Mandala Rasa:**\n\n{men}\n\n"
                    "Untuk daftar menu lengkap, silakan kunjungi meja kami "
                    "atau minta dari staf saat kedatangan.")
        return (f"ℹ️ **Mandala Rasa — Info Singkat:**\n\n"
                f"🕐 **Jam:** {info['jam_operasional']}\n"
                f"🪑 **Area:** {', '.join(info['area'])}\n"
                f"✨ **Fasilitas:** WiFi · Parkir · Live Music (Jum-Sab)\n\n"
                "Tanya lebih lanjut tentang: *jam buka*, *area meja*, "
                "*fasilitas*, atau *kebijakan*?")

    return ("Hmm, saya belum sepenuhnya memahami permintaan Anda 😊\n\n"
            "Saya bisa membantu dengan:\n"
            "• 🗓️ **Buat reservasi** — *Reservasi 4 orang, 20 Juli, jam 19:00*\n"
            "• 🔍 **Cek reservasi** — *Cek reservasi atas nama Andi*\n"
            "• ℹ️ **Info restoran** — *Jam buka berapa? Ada WiFi?*\n\n"
            "Silakan coba lagi dengan kalimat yang lebih spesifik! 🙏")

# ─────────────────── SESSION STATE ───────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": ("Halo! Selamat datang di **Mandala Rasa** 🍽️\n\n"
                     "Saya **Sara**, asisten reservasi Anda. Saya siap membantu:\n\n"
                     "🗓️ **Buat reservasi** meja\n"
                     "🔍 **Cek status** reservasi Anda\n"
                     "ℹ️ **Info restoran** — jam, area, fasilitas & kebijakan\n\n"
                     "Apa yang bisa saya bantu hari ini? 😊")}
    ]

# ─────────────────── LAYOUT ───────────────────
col_main, col_info = st.columns([5, 2], gap="medium")

with col_main:
    # ── Header ──
    st.markdown(f"""
    <div class="chat-header">
      <div class="chat-header-text">
        <span class="badge">✦ AI Powered · Google Gemini</span>
        <h1>AI Reservation Assistant</h1>
        <p>Sara siap membantu reservasi, pengecekan status & info restoran</p>
      </div>
      <div class="chat-header-icon">{LOGO_IMG}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Quick actions ──
    qa_cols = st.columns(5)
    quick_actions = {
        "🗓️ Reservasi":   "Saya ingin membuat reservasi meja",
        "🔍 Cek Status":  "Cek status reservasi saya",
        "🕐 Jam Buka":    "Jam berapa restoran buka?",
        "🪑 Area Meja":   "Apa saja area meja yang tersedia?",
        "📜 Kebijakan":   "Apa kebijakan reservasi restoran?",
    }
    for col, (label, prompt) in zip(qa_cols, quick_actions.items()):
        with col:
            if st.button(label, use_container_width=True, key=f"qa_{label}"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.spinner("Sara sedang membalas..."):
                    reply = call_gemini(st.session_state.messages)
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.rerun()

    # ── Chat window ──
    chat_html = '<div class="chat-window" id="chat-window">'
    for msg in st.session_state.messages:
        raw = msg["content"]
        html_txt = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', raw)
        html_txt = re.sub(r'`(.+?)`', r'<code style="background:#f0e8d5;padding:2px 5px;border-radius:3px;font-size:0.83rem">\1</code>', html_txt)
        html_txt = html_txt.replace('\n', '<br>')
        if msg["role"] == "user":
            chat_html += f'<div class="bubble-wrap-user"><div class="bubble-user"><div class="sender">Anda</div>{html_txt}</div></div>'
        else:
            chat_html += f'<div class="bubble-wrap-bot"><div class="bot-avatar">{LOGO_IMG}</div><div class="bubble-bot"><div class="sender">Sara</div>{html_txt}</div></div>'
    chat_html += '</div><script>const cw=document.getElementById("chat-window");if(cw)cw.scrollTop=cw.scrollHeight;</script>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # ── Input bar ──
    inp_col, btn_col = st.columns([6, 1])
    with inp_col:
        user_input = st.text_input("msg", label_visibility="collapsed",
            placeholder="Ketik pesan... (contoh: Reservasi 4 orang besok jam 19:00)",
            key="chat_input")
    with btn_col:
        send = st.button("Kirim ✈️", use_container_width=True, key="send_btn")

    if send and user_input.strip():
        st.session_state.messages.append({"role": "user", "content": user_input.strip()})
        with st.spinner("Sara sedang membalas..."):
            reply = call_gemini(st.session_state.messages)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    # ── Reset ──
    if st.button("🗑️ Reset percakapan", key="clear_chat"):
        st.session_state.messages = [{"role": "assistant",
            "content": "Halo lagi! Saya **Sara**, asisten reservasi Mandala Rasa 🍽️\n\nPercakapan telah direset. Ada yang bisa saya bantu? 😊"}]
        st.rerun()

# ─────────────────── INFO PANEL ───────────────────
with col_info:
    # Sara badge
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0f1923,#1c2e40);border-radius:12px;
         padding:14px;text-align:center;margin-bottom:0.8rem;">
      <div style="width:44px;height:44px;border-radius:50%;margin:0 auto 7px;
           background:rgba(212,175,55,0.15);border:1.5px solid rgba(212,175,55,0.35);
           overflow:hidden;">{LOGO_IMG}</div>
      <div style="font-size:0.8rem;color:#e8dcc8;font-weight:700;">Sara</div>
      <div style="font-size:0.65rem;color:rgba(232,220,200,0.4);margin:2px 0 7px;">Gemini 2.5 Flash</div>
      <span style="background:rgba(46,204,113,0.18);border:1px solid rgba(46,204,113,0.35);
           border-radius:50px;padding:2px 10px;font-size:0.65rem;color:#2ecc71;font-weight:700;">
        ● ONLINE</span>
    </div>
    """, unsafe_allow_html=True)

    # Contoh perintah
    examples = [
        ("🗓️ Buat Reservasi", "Reservasi atas nama Sinta, 4 orang, 20/07, jam 19:00, Garden"),
        ("🔍 Cek by Nama",    "Cek reservasi atas nama Budi"),
        ("🔍 Cek by ID",      "Cek RSV00001"),
        ("🕐 Jam Buka",       "Jam berapa restoran buka?"),
        ("🪑 Area",           "Kapasitas VIP Room berapa?"),
        ("📜 Kebijakan",      "Cara membatalkan reservasi?"),
        ("✨ Fasilitas",      "Apakah ada live music?"),
        ("🎂 Spesial",        "Butuh dekorasi ulang tahun"),
    ]
    ex_html = '<div class="info-card"><div class="info-card-title">💬 Contoh Perintah</div>'
    for lbl, ex in examples:
        ex_html += f'<div class="example-item"><b>{lbl}</b><span style="color:#888;font-size:0.7rem"> — {ex}</span></div>'
    ex_html += '</div>'
    st.markdown(ex_html, unsafe_allow_html=True)

    # Status
    statuses = [("Confirmed","#2ecc71","Terkonfirmasi"),("Completed","#3498db","Selesai"),
                ("Pending","#f39c12","Menunggu"),("Cancelled","#e74c3c","Dibatalkan"),
                ("No-show","#9b59b6","Tidak hadir")]
    st_html = '<div class="info-card"><div class="info-card-title">📊 Status</div>'
    for s, c, l in statuses:
        st_html += f'<div class="status-row"><span class="status-pill2" style="background:{c}">{s}</span><span style="color:#555;font-size:0.77rem">{l}</span></div>'
    st_html += '</div>'
    st.markdown(st_html, unsafe_allow_html=True)

st.markdown("---")
st.caption("Sara adalah AI dan dapat membuat kesalahan. Harap periksa kembali Informasi Penting")
