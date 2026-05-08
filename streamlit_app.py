import streamlit as st
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Kasir Es Kelapa",
    layout="wide"
)

# =========================
# VIDEO BACKGROUND URL
# =========================
bg_video_url = "https://raw.githubusercontent.com/Alfarabi-art/eskepala/refs/heads/main/bg.mp4"

# =========================
# DATA MENU
# =========================
menu = [
    {
        "id": 1,
        "nama": "Es Kelapa + Gula",
        "harga": 4000,
        "gambar": "https://i.postimg.cc/0Q0n0G7M/es-kelapa-gula.jpg",
    },
    {
        "id": 2,
        "nama": "Es Kelapa + Gula + Susu",
        "harga": 5000,
        "gambar": "https://i.postimg.cc/vmL1YBfN/es-kelapa-susu.jpg",
    },
    {
        "id": 3,
        "nama": "Kelapa Murni",
        "harga": 10000,
        "gambar": "https://i.postimg.cc/Z5W6tR6B/kelapa-murni.jpg",
    },
    {
        "id": 4,
        "nama": "Air Kelapa",
        "harga": 5000,
        "gambar": "https://i.postimg.cc/4dM3tM0r/air-kelapa.jpg",
    },
]

# =========================
# SESSION STATE
# =========================
if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

if "riwayat_transaksi" not in st.session_state:
    st.session_state.riwayat_transaksi = []

# =========================
# STYLE
# =========================
st.markdown(
    f"""
<style>

/* VIDEO BACKGROUND */
#bg-video {{
    position: fixed;
    right: 0;
    bottom: 0;
    min-width: 100%;
    min-height: 100%;
    object-fit: cover;
    z-index: -100;
    pointer-events: none;
    filter: brightness(0.6);
}}

/* VIDEO SUPPORT */
video {{
    object-fit: cover;
}}

/* OVERLAY */
.stApp {{
    background: rgba(0,0,0,0.35);
}}

/* TEXT */
h1, h2, h3, h4, h5, h6, p, label {{
    color: white !important;
}}

/* CARD */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.15);
    margin-bottom: 15px;
}}

/* BUTTON */
.stButton button {{
    background-color: #16a34a;
    color: white;
    border-radius: 12px;
    border: none;
    padding: 12px;
    font-weight: bold;
    width: 100%;
    font-size: 16px;
}}

.stButton button:hover {{
    background-color: #15803d;
    color: white;
}}

/* INPUT */
.stNumberInput input {{
    background-color: rgba(255,255,255,0.95);
    color: black;
    border-radius: 10px;
}}

.stSelectbox div[data-baseweb="select"] {{
    background-color: rgba(255,255,255,0.95);
    color: black;
    border-radius: 10px;
}}

/* STRUK */
.stCode {{
    border-radius: 20px !important;
    font-size: 16px !important;
    padding: 15px !important;
    background: white !important;
    color: black !important;
    overflow-x: auto;
}}

/* IMAGE */
img {{
    border-radius: 15px;
}}

/* MOBILE */
@media (max-width: 768px) {{

    h1 {{
        font-size: 28px !important;
        text-align: center;
    }}

    h2 {{
        font-size: 22px !important;
    }}

    h3 {{
        font-size: 20px !important;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        padding: 12px;
        border-radius: 18px;
    }}

    .stButton button {{
        font-size: 15px;
        padding: 12px;
    }}

    .stCode {{
        font-size: 13px !important;
        padding: 10px !important;
    }}

    img {{
        border-radius: 12px;
    }}
}}

@media (max-width: 480px) {{

    h1 {{
        font-size: 24px !important;
    }}

    .stButton button {{
        font-size: 14px;
    }}

    .stCode {{
        font-size: 12px !important;
    }}
}}

</style>

<video autoplay muted loop playsinline webkit-playsinline id="bg-video">
    <source src="{bg_video_url}" type="video/mp4">
</video>

""",
    unsafe_allow_html=True
)

# =========================
# TITLE
# =========================
st.title("🥥 Kasir Es Kelapa")

menu_tab, keuangan_tab = st.tabs(
    ["Kasir", "Keuangan"]
)

# =========================
# TAB KASIR
# =========================
with menu_tab:

    col1, col2 = st.columns(2)

    # =====================
    # MENU
    # =====================
    with col1:

        st.subheader("Menu")

        for item in menu:

            with st.container(border=True):

                st.image(
                    item["gambar"],
                    use_container_width=True
                )

                st.write(
                    f"### {item['nama']}"
                )

                st.write(
                    f"Rp {item['harga']:,}"
                )

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

                    found = False

                    for keranjang_item in st.session_state.keranjang:

                        if keranjang_item["nama"] == item["nama"]:

                            keranjang_item["qty"] += qty
                            found = True
                            break

                    if not found:

                        st.session_state.keranjang.append({
                            "nama": item["nama"],
                            "harga": item["harga"],
                            "qty": qty,
                        })

                    st.success(
                        f"{item['nama']} ditambahkan"
                    )

    # =====================
    # KERANJANG
    # =====================
    with col2:

        st.subheader("Keranjang")

        total = 0

        if len(st.session_state.keranjang) == 0:

            st.info("Belum ada pesanan")

        else:

            for item in st.session_state.keranjang:

                subtotal = (
                    item["harga"]
                    * item["qty"]
                )

                total += subtotal

                st.write(
                    f"### {item['nama']}"
                )

                st.write(
                    f"{item['qty']} x Rp {item['harga']:,}"
                )

                st.write(
                    f"Subtotal : Rp {subtotal:,}"
                )

                st.divider()

        st.write(
            f"## Total: Rp {total:,}"
        )

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
            min_value=0
        )

        kembalian = uang - total

        if uang > 0:

            if uang >= total:

                st.success(
                    f"Kembalian: Rp {kembalian:,}"
                )

            else:

                st.error(
                    "Uang pelanggan kurang"
                )

        # =====================
        # CETAK STRUK
        # =====================
        if st.button("Cetak Struk"):

            if total == 0:

                st.warning(
                    "Keranjang masih kosong"
                )

            elif uang < total:

                st.error(
                    "Pembayaran belum cukup"
                )

            else:

                transaksi = {
                    "tanggal": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "total": total,
                    "metode": metode,
                    "detail": (
                        st.session_state
                        .keranjang
                        .copy()
                    )
                }

                st.session_state.riwayat_transaksi.append(
                    transaksi
                )

                st.success(
                    "Struk berhasil dicetak"
                )

                # =====================
                # STRUK
                # =====================
                struk = ""

                for item in transaksi["detail"]:

                    subtotal = (
                        item["harga"]
                        * item["qty"]
                    )

                    kiri = (
                        f"{item['qty']} x "
                        f"Rp {item['harga']:,}"
                    )

                    kanan = (
                        f"Rp {subtotal:,}"
                    )

                    struk += (
                        f"{item['nama']}\n"
                    )

                    struk += (
                        f"{kiri:<25}"
                        f"{kanan:>15}\n"
                    )

                    struk += (
                        "-" * 40 + "\n"
                    )

                struk += (
                    f"{'TOTAL':<20}"
                    f": Rp {total:,}\n"
                )

                struk += (
                    f"{'PEMBAYARAN':<20}"
                    f": {metode}\n"
                )

                struk += (
                    f"{'TUNAI':<20}"
                    f": Rp {uang:,}\n"
                )

                struk += (
                    f"{'KEMBALIAN':<20}"
                    f": Rp {kembalian:,}\n"
                )

                struk += "=" * 40 + "\n"

                struk += (
                    "Terima Kasih 🙏\n"
                )

                struk += (
                    "Semoga harimu segar 🥥"
                )

                # =====================
                # TAMPILKAN STRUK
                # =====================
                with st.container(border=True):

                    st.code(
                        f"""
🥥 TOKO ES KELAPA
Fresh Coconut Drink

========================================

Tanggal : {transaksi['tanggal']}

========================================

{struk}
""",
                        language=None
                    )

                st.balloons()

                # =====================
                # RESET KERANJANG
                # =====================
                st.session_state.keranjang = []

# =========================
# TAB KEUANGAN
# =========================
with keuangan_tab:

    st.subheader("Laporan Keuangan")

    total_pemasukan = sum(
        trx["total"]
        for trx
        in st.session_state.riwayat_transaksi
    )

    total_transaksi = len(
        st.session_state.riwayat_transaksi
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Pemasukan",
            f"Rp {total_pemasukan:,}"
        )

    with col2:

        st.metric(
            "Jumlah Transaksi",
            total_transaksi
        )

    st.divider()

    if len(
        st.session_state.riwayat_transaksi
    ) == 0:

        st.info(
            "Belum ada transaksi"
        )

    else:

        for trx in reversed(
            st.session_state.riwayat_transaksi
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
