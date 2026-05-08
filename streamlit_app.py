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
    border-radius: 12px;
    border: none;
    padding: 10px;
    font-weight: bold;
}

.stButton button:hover {
    background-color: #15803d;
    color: white;
}

.struk-box{
    background:white;
    padding:25px;
    border-radius:20px;
    border:2px dashed #16a34a;
    box-shadow:0 4px 15px rgba(0,0,0,0.1);
    color:black;
    font-family:monospace;
}

.struk-title{
    text-align:center;
    font-size:30px;
    font-weight:bold;
    color:#16a34a;
}

.struk-sub{
    text-align:center;
    color:gray;
    margin-bottom:15px;
}

.struk-line{
    border-top:2px dashed #ccc;
    margin:15px 0;
}

.item-box{
    background:#f0fdf4;
    padding:12px;
    border-radius:12px;
    margin-bottom:10px;
}

.total-box{
    background:#dcfce7;
    padding:15px;
    border-radius:15px;
    margin-top:15px;
}

.kembalian{
    color:#16a34a;
    font-size:22px;
    font-weight:bold;
}

.footer{
    text-align:center;
    margin-top:20px;
    color:gray;
    font-size:14px;
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
                # STRUK MODERN
                # =====================

                struk_html = f"""
                <div class="struk-box">

                <div class="struk-title">
                🥥 TOKO ES KELAPA
                </div>

                <div class="struk-sub">
                Fresh Coconut Drink
                </div>

                <div class="struk-line"></div>

                <b>Tanggal :</b><br>
                {transaksi['tanggal']}

                <div class="struk-line"></div>
                """

                # =====================
                # DETAIL ITEM
                # =====================

                for item in transaksi["detail"]:

                    subtotal = (
                        item["harga"]
                        * item["qty"]
                    )

                    struk_html += f"""
                    <div class="item-box">

                    <b style="
                        font-size:18px;
                    ">
                        {item['nama']}
                    </b>

                    <table width="100%" style="
                        margin-top:8px;
                    ">

                    <tr>
                        <td>
                            {item['qty']} x Rp {item['harga']:,}
                        </td>

                        <td align="right">
                            Rp {subtotal:,}
                        </td>
                    </tr>

                    </table>

                    </div>
                    """

                # =====================
                # TOTAL
                # =====================

                struk_html += f"""

                <div class="total-box">

                <table width="100%" style="
                    line-height:2;
                    font-size:16px;
                ">

                <tr>
                    <td><b>TOTAL</b></td>
                    <td align="right">
                        Rp {total:,}
                    </td>
                </tr>

                <tr>
                    <td><b>PEMBAYARAN</b></td>
                    <td align="right">
                        {metode}
                    </td>
                </tr>

                <tr>
                    <td><b>TUNAI</b></td>
                    <td align="right">
                        Rp {uang:,}
                    </td>
                </tr>

                </table>

                <div style="
                    text-align:center;
                    margin-top:15px;
                ">
                    <div>
                        KEMBALIAN
                    </div>

                    <div class="kembalian">
                        Rp {kembalian:,}
                    </div>
                </div>

                </div>

                <div class="footer">
                🙏 Terima Kasih 🙏<br>
                Semoga harimu segar seperti kelapa 🥥
                </div>

                </div>
                """

                st.markdown(
                    struk_html,
                    unsafe_allow_html=True
                )

                st.balloons()

                # =====================
                # KOSONGKAN KERANJANG
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
