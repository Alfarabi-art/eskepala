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
# DATA MENU
# =========================
menu = [
    {
        "id": 1,
        "nama": "Es Kelapa + Gula",
        "harga": 4000,
        "gambar": "images/eskepalagula.jpg",
    },
    {
        "id": 2,
        "nama": "Es Kelapa + Gula + Susu",
        "harga": 5000,
        "gambar": "images/kelapasusu.jpg",
    },
    {
        "id": 3,
        "nama": "Kelapa Murni",
        "harga": 10000,
        "gambar": "images/kelapamurni.jpg",
    },
    {
        "id": 4,
        "nama": "Air Kelapa",
        "harga": 5000,
        "gambar": "images/airkelapa.jpg",
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
st.markdown("""
<style>

.main {
    background: linear-gradient(
        to bottom right,
        #dcfce7,
        #bbf7d0,
        #86efac
    );
}

.stButton button {
    background-color: #16a34a;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px;
    font-weight: bold;
}

.stButton button:hover {
    background-color: #15803d;
    color: white;
}

</style>
""", unsafe_allow_html=True)

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

                st.write(f"### {item['nama']}")
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

        # =====================
        # KEMBALIAN
        # =====================
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

                total_item = sum(
                    item["qty"]
                    for item
                    in st.session_state.keranjang
                )

                transaksi = {
                    "tanggal": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "total": total,
                    "metode": metode,
                    "jumlah_item": total_item,
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
                # STRUK TEXT
                # =====================
                struk = ""
                struk += "🥥 TOKO ES KELAPA\n"
                struk += "Fresh Coconut Drink\n"
                struk += "=" * 40 + "\n"
                struk += (
                    f"Tanggal : "
                    f"{transaksi['tanggal']}\n"
                )
                struk += "=" * 40 + "\n"

                # DETAIL ITEM
                for item in transaksi["detail"]:

                    subtotal = (
                        item["harga"]
                        * item["qty"]
                    )

                    struk += (
                        f"{item['nama']}\n"
                    )

                    kiri = (
                        f"{item['qty']} x "
                        f"Rp {item['harga']:,}"
                    )

                    kanan = (
                        f"Rp {subtotal:,}"
                    )

                    struk += (
                        f"{kiri:<25}"
                        f"{kanan:>15}\n"
                    )

                    struk += (
                        "-" * 40 + "\n"
                    )

                # TOTAL
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

                # TAMPILKAN STRUK
                st.code(struk)

                st.balloons()

                # KOSONGKAN KERANJANG
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

    total_item = sum(
        trx["jumlah_item"]
        for trx
        in st.session_state.riwayat_transaksi
    )

    col1, col2, col3 = st.columns(3)

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

    with col3:

        st.metric(
            "Item Terjual",
            total_item
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
            st.session_state
            .riwayat_transaksi
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

                st.write(
                    f"Jumlah Item : {trx['jumlah_item']}"
                )
