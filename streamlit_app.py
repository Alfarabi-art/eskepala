import streamlit as st
from datetime import datetime

# =========================================
# CONFIG
# =========================================
st.set_page_config(
    page_title="Kasir Es Kelapa",
    layout="wide"
)

# =========================================
# VIDEO BACKGROUND
# =========================================
VIDEO_URL = "https://raw.githubusercontent.com/Alfarabi-art/eskepala/main/bg.mp4"

# =========================================
# CSS
# =========================================
st.markdown(f"""
<style>

/* =========================
VIDEO BACKGROUND
========================= */
.video-container {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: -100;
}}

.video-container video {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    filter: brightness(0.35);
}}

/* =========================
GLOBAL
========================= */
.stApp {{
    background: transparent;
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

h1, h2, h3, h4, h5, h6, p, label {{
    color: white !important;
}}

/* =========================
CARD
========================= */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.10);
    padding: 15px;
    margin-bottom: 15px;
}}

/* =========================
BUTTON
========================= */
.stButton button {{
    width: 100%;
    background: #16a34a;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px;
    font-weight: bold;
    font-size: 16px;
}}

.stButton button:hover {{
    background: #15803d;
    color: white;
}}

/* =========================
INPUT
========================= */
.stNumberInput input {{
    background: rgba(255,255,255,0.92);
    color: black;
    border-radius: 10px;
}}

.stSelectbox div[data-baseweb="select"] {{
    background: rgba(255,255,255,0.92);
    color: black;
    border-radius: 10px;
}}

/* =========================
STRUK
========================= */
.struk-box {{
    background: white;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    overflow: hidden;
}}

.struk-box * {{
    color: black !important;
    font-family: Arial, sans-serif;
}}

/* =========================
MOBILE
========================= */
@media (max-width: 768px) {{

    h1 {{
        font-size: 30px !important;
        text-align: center;
    }}

    .struk-box {{
        padding: 15px;
    }}

}}

</style>

<div class="video-container">
    <video autoplay muted loop playsinline>
        <source src="{VIDEO_URL}" type="video/mp4">
    </video>
</div>

""", unsafe_allow_html=True)

# =========================================
# DATA MENU
# =========================================
menu = [
    {
        "id": 1,
        "nama": "Es Kelapa + Gula",
        "harga": 4000,
        "gambar": "images/eskepalagula.jpg"
    },
    {
        "id": 2,
        "nama": "Es Kelapa + Gula + Susu",
        "harga": 5000,
        "gambar": "images/kelapasusu.jpg"
    },
    {
        "id": 3,
        "nama": "Kelapa Murni",
        "harga": 10000,
        "gambar": "images/kelapamurni.jpg"
    },
    {
        "id": 4,
        "nama": "Air Kelapa",
        "harga": 5000,
        "gambar": "images/airkelapa.jpg"
    }
]

# =========================================
# SESSION
# =========================================
if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

# =========================================
# TITLE
# =========================================
st.title("🥥 Kasir Es Kelapa")

tab1, tab2 = st.tabs(["Kasir", "Keuangan"])

# =========================================
# TAB KASIR
# =========================================
with tab1:

    col1, col2 = st.columns(2)

    # =====================================
    # MENU
    # =====================================
    with col1:

        st.subheader("Menu")

        for item in menu:

            with st.container(border=True):

                st.image(
                    item["gambar"],
                    use_container_width=True
                )

                st.write(f"## {item['nama']}")
                st.write(f"Rp {item['harga']:,}")

                qty = st.number_input(
                    f"Qty {item['nama']}",
                    min_value=1,
                    value=1,
                    key=f"qty_{item['id']}"
                )

                if st.button(
                    f"Tambah {item['nama']}",
                    key=f"btn_{item['id']}"
                ):

                    ditemukan = False

                    for k in st.session_state.keranjang:

                        if k["nama"] == item["nama"]:
                            k["qty"] += qty
                            ditemukan = True
                            break

                    if not ditemukan:
                        st.session_state.keranjang.append({
                            "nama": item["nama"],
                            "harga": item["harga"],
                            "qty": qty
                        })

                    st.success("Berhasil ditambahkan")

    # =====================================
    # KERANJANG
    # =====================================
    with col2:

        st.subheader("Keranjang")

        total = 0

        if len(st.session_state.keranjang) == 0:

            st.info("Belum ada pesanan")

        else:

            for item in st.session_state.keranjang:

                subtotal = item["harga"] * item["qty"]
                total += subtotal

                with st.container(border=True):

                    st.write(f"### {item['nama']}")
                    st.write(
                        f"{item['qty']} x Rp {item['harga']:,}"
                    )

                    st.write(
                        f"Subtotal : Rp {subtotal:,}"
                    )

        st.write(f"# Total: Rp {total:,}")

        metode = st.selectbox(
            "Metode Pembayaran",
            [
                "Cash",
                "QRIS",
                "Transfer Bank",
                "E-Wallet"
            ]
        )

        uang = st.number_input(
            "Jumlah uang diterima",
            min_value=0,
            value=0
        )

        kembalian = uang - total

        if uang > 0:

            if uang >= total:
                st.success(
                    f"Kembalian: Rp {kembalian:,}"
                )
            else:
                st.error("Uang kurang")

        # =====================================
        # CETAK STRUK
        # =====================================
        if st.button("Cetak Struk"):

            if total == 0:

                st.warning("Keranjang kosong")

            elif uang < total:

                st.error("Uang belum cukup")

            else:

                tanggal = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                st.success("Struk berhasil dicetak")

                struk_html = f"""
<div class="struk-box">

<div style="text-align:center;">

<h2 style="
margin:0;
font-size:28px;
">
🥥 TOKO ES KELAPA
</h2>

<div style="
color:#666;
font-size:14px;
margin-top:5px;
">
Fresh Coconut Drink
</div>

</div>

<hr style="margin:15px 0;">

<div style="
display:flex;
justify-content:space-between;
font-size:14px;
margin-bottom:15px;
">

<span>Tanggal</span>
<span>{tanggal}</span>

</div>

<hr style="margin:15px 0;">
"""

                for item in st.session_state.keranjang:

                    subtotal = (
                        item["harga"]
                        * item["qty"]
                    )

                    struk_html += f"""

<div style="
margin-bottom:18px;
padding-bottom:12px;
border-bottom:1px dashed #ccc;
">

<div style="
font-weight:bold;
font-size:16px;
margin-bottom:8px;
">
{item['nama']}
</div>

<div style="
display:flex;
justify-content:space-between;
font-size:15px;
">

<div>
{item['qty']} x Rp {item['harga']:,}
</div>

<div>
Rp {subtotal:,}
</div>

</div>

</div>
"""

                struk_html += f"""

<div style="margin-top:20px;">

<div style="
display:flex;
justify-content:space-between;
margin-bottom:10px;
font-size:16px;
">

<div><b>TOTAL</b></div>
<div><b>Rp {total:,}</b></div>

</div>

<div style="
display:flex;
justify-content:space-between;
margin-bottom:10px;
">

<div>PEMBAYARAN</div>
<div>{metode}</div>

</div>

<div style="
display:flex;
justify-content:space-between;
margin-bottom:10px;
">

<div>TUNAI</div>
<div>Rp {uang:,}</div>

</div>

<div style="
display:flex;
justify-content:space-between;
font-size:18px;
font-weight:bold;
color:green;
">

<div>KEMBALIAN</div>
<div>Rp {kembalian:,}</div>

</div>

</div>

<hr style="margin:20px 0;">

<div style="
text-align:center;
font-size:14px;
color:#666;
">

Terima Kasih 🙏 <br>
Semoga harimu segar 🥥

</div>

</div>
"""

                st.markdown(
                    struk_html,
                    unsafe_allow_html=True
                )

                st.session_state.riwayat.append({
                    "tanggal": tanggal,
                    "total": total,
                    "metode": metode
                })

                st.session_state.keranjang = []

# =========================================
# TAB KEUANGAN
# =========================================
with tab2:

    st.subheader("Laporan Keuangan")

    total_uang = sum(
        x["total"]
        for x
        in st.session_state.riwayat
    )

    jumlah = len(
        st.session_state.riwayat
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Pemasukan",
            f"Rp {total_uang:,}"
        )

    with col2:

        st.metric(
            "Jumlah Transaksi",
            jumlah
        )

    st.divider()

    if jumlah == 0:

        st.info("Belum ada transaksi")

    else:

        for trx in reversed(
            st.session_state.riwayat
        ):

            with st.container(border=True):

                st.write(
                    f"Tanggal : {trx['tanggal']}"
                )

                st.write(
                    f"Total : Rp {trx['total']:,}"
                )

                st.write(
                    f"Metode : {trx['metode']}"
                )
