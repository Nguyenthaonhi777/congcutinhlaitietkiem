import streamlit as st
import pandas as pd

# ==============================
# CẤU HÌNH TRANG
# ==============================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="wide"
)

# ==============================
# CSS
# ==============================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }

    .result-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f5f7fa;
        text-align: center;
        margin-bottom: 15px;
    }

    .result-title {
        font-size: 16px;
        color: #555;
        margin-bottom: 8px;
    }

    .result-value {
        font-size: 24px;
        font-weight: bold;
    }

    .formula-box {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# TIÊU ĐỀ
# ==============================
st.markdown(
    '<div class="main-title">💰 MÁY TÍNH LÃI TIỀN GỬI TIẾT KIỆM</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Tính lãi theo phương pháp lãi đơn và lãi kép'
    '</div>',
    unsafe_allow_html=True
)

# ==============================
# NHẬP DỮ LIỆU
# ==============================
st.header("📌 Thông tin tiền gửi")

col1, col2 = st.columns(2)

with col1:
    so_tien = st.number_input(
        "Số tiền gửi (VNĐ)",
        min_value=0.0,
        value=100_000_000.0,
        step=1_000_000.0,
        format="%.0f"
    )

    ky_han = st.number_input(
        "Kỳ hạn (tháng)",
        min_value=1,
        max_value=600,
        value=12,
        step=1
    )

    lai_suat = st.number_input(
        "Lãi suất (%/năm)",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1
    )

with col2:
    loai_lai = st.selectbox(
        "Phương pháp tính lãi",
        [
            "Lãi đơn",
            "Lãi kép"
        ]
    )

    hinh_thuc = st.selectbox(
        "Hình thức nhận lãi",
        [
            "Lãnh lãi hàng tháng",
            "Lãnh lãi hàng quý",
            "Lãnh lãi cuối kỳ"
        ]
    )

# ==============================
# NÚT TÍNH
# ==============================
st.divider()

tinh_lai = st.button(
    "🧮 TÍNH TIỀN LÃI",
    use_container_width=True
)

# ==============================
# HÀM ĐỊNH DẠNG TIỀN
# ==============================
def dinh_dang_tien(tien):
    return f"{tien:,.0f} VNĐ"


# ==============================
# TÍNH TOÁN
# ==============================
if tinh_lai:

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0.")
        st.stop()

    # Lãi suất dạng thập phân
    r = lai_suat / 100

    # Số tháng và số năm
    so_thang = ky_han
    so_nam = so_thang / 12

    # Xác định số kỳ nhận lãi
    if hinh_thuc == "Lãnh lãi hàng tháng":
        so_ky = so_thang
        thang_moi_ky = 1

    elif hinh_thuc == "Lãnh lãi hàng quý":
        so_ky = so_thang // 3

        # Nếu kỳ hạn không chia hết cho 3
        # thì vẫn tính phần thời gian còn lại
        if so_thang % 3 != 0:
            so_ky += 1

        thang_moi_ky = 3

    else:
        so_ky = 1
        thang_moi_ky = so_thang

    # ==========================================
    # LÃI ĐƠN
    # ==========================================
    if loai_lai == "Lãi đơn":

        tong_lai = so_tien * r * so_nam
        tong_tien = so_tien + tong_lai

        # Lãi định kỳ
        if hinh_thuc == "Lãnh lãi hàng tháng":
            lai_dinh_ky = so_tien * r / 12

        elif hinh_thuc == "Lãnh lãi hàng quý":
            lai_dinh_ky = so_tien * r / 4

        else:
            lai_dinh_ky = tong_lai

        # Tạo bảng chi tiết
        data = []

        for ky in range(1, so_ky + 1):

            if hinh_thuc == "Lãnh lãi hàng tháng":
                thoi_gian = ky
                lai_ky = so_tien * r / 12

            elif hinh_thuc == "Lãnh lãi hàng quý":
                thoi_gian = min(ky * 3, so_thang)
                thang_thuc_te = (
                    3 if ky * 3 <= so_thang
                    else so_thang - (ky - 1) * 3
                )
                lai_ky = so_tien * r * thang_thuc_te / 12

            else:
                thoi_gian = so_thang
                lai_ky = tong_lai

            data.append({
                "Kỳ": ky,
                "Thời gian (tháng)": thoi_gian,
                "Tiền gốc": dinh_dang_tien(so_tien),
                "Tiền lãi kỳ này": dinh_dang_tien(lai_ky),
                "Tổng lãi tích lũy": dinh_dang_tien(
                    sum(
                        row["lai"]
                        for row in [
                            {"lai": so_tien * r / 12}
                            for _ in range(
                                min(thoi_gian, so_thang)
                            )
                        ]
                    )
                    if hinh_thuc == "Lãnh lãi hàng tháng"
                    else lai_ky * ky
                )
            })

    # ==========================================
    # LÃI KÉP
    # ==========================================
    else:

        # Số lần nhập lãi vào gốc
        if hinh_thuc == "Lãnh lãi hàng tháng":
            n = so_thang
            lai_suat_ky = r / 12

        elif hinh_thuc == "Lãnh lãi hàng quý":
            n = so_thang / 3
            lai_suat_ky = r / 4

        else:
            n = 1
            lai_suat_ky = r * so_nam

        # Trường hợp cuối kỳ
        if hinh_thuc == "Lãnh lãi cuối kỳ":

            tong_tien = so_tien * (1 + r) ** so_nam
            tong_lai = tong_tien - so_tien
            lai_dinh_ky = tong_lai

            data = [{
                "Kỳ": 1,
                "Thời gian (tháng)": so_thang,
                "Tiền gốc": dinh_dang_tien(so_tien),
                "Tiền lãi kỳ này": dinh_dang_tien(tong_lai),
                "Tổng lãi tích lũy": dinh_dang_tien(tong_lai)
            }]

        else:

            # Tính từng kỳ
            tien_hien_tai = so_tien
            data = []

            for ky in range(1, int(n) + 1):

                tien_dau_ky = tien_hien_tai

                lai_ky = tien_dau_ky * lai_suat_ky

                tien_hien_tai += lai_ky

                data.append({
                    "Kỳ": ky,
                    "Thời gian (tháng)": (
                        ky if hinh_thuc == "Lãnh lãi hàng tháng"
                        else ky * 3
                    ),
                    "Tiền gốc đầu kỳ": dinh_dang_tien(tien_dau_ky),
                    "Tiền lãi kỳ này": dinh_dang_tien(lai_ky),
                    "Tổng tiền cuối kỳ": dinh_dang_tien(
                        tien_hien_tai
                    )
                })

            tong_tien = tien_hien_tai
            tong_lai = tong_tien - so_tien

            # Lãi định kỳ = lãi của kỳ đầu tiên
            lai_dinh_ky = data[0]["Tiền lãi kỳ này"]

    # ==============================
    # HIỂN THỊ KẾT QUẢ
    # ==============================
    st.success("✅ Tính toán hoàn tất!")

    st.header("📊 Kết quả")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">Tiền lãi định kỳ</div>
                <div class="result-value">
                    {
                        dinh_dang_tien(
                            lai_dinh_ky
                            if isinstance(lai_dinh_ky, (int, float))
                            else 0
                        )
                        if isinstance(lai_dinh_ky, (int, float))
                        else lai_dinh_ky
                    }
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">Tổng tiền lãi</div>
                <div class="result-value">
                    {dinh_dang_tien(tong_lai)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="result-box">
                <div class="result-title">Tổng gốc + lãi</div>
                <div class="result-value">
                    {dinh_dang_tien(tong_tien)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ==============================
    # THÔNG TIN TÓM TẮT
    # ==============================
    st.subheader("📋 Thông tin khoản tiền gửi")

    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

    with summary_col1:
        st.metric(
            "Số tiền gửi",
            dinh_dang_tien(so_tien)
        )

    with summary_col2:
        st.metric(
            "Kỳ hạn",
            f"{ky_han} tháng"
        )

    with summary_col3:
        st.metric(
            "Lãi suất",
            f"{lai_suat:.2f}%/năm"
        )

    with summary_col4:
        st.metric(
            "Phương pháp",
            loai_lai
        )

    # ==============================
    # BẢNG CHI TIẾT
    # ==============================
    st.subheader("📑 Chi tiết theo từng kỳ")

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # ==============================
    # CÔNG THỨC
    # ==============================
    st.subheader("📚 Công thức tính")

    if loai_lai == "Lãi đơn":

        st.markdown(
            """
            <div class="formula-box">
                <b>Lãi đơn:</b><br><br>
                Tiền lãi = Tiền gốc × Lãi suất × Thời gian<br><br>
                Tổng tiền = Tiền gốc + Tiền lãi
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="formula-box">
                <b>Lãi kép:</b><br><br>
                Tổng tiền = Tiền gốc × (1 + r)<sup>n</sup><br><br>
                Tiền lãi = Tổng tiền − Tiền gốc<br><br>
                Trong đó <b>r</b> là lãi suất của mỗi kỳ và
                <b>n</b> là số kỳ nhập lãi vào gốc.
            </div>
            """,
            unsafe_allow_html=True
        )

# ==============================
# CHÂN TRANG
# ==============================
st.divider()

st.caption(
    "💡 Công cụ mang tính chất tham khảo. "
    "Kết quả thực tế có thể khác tùy theo quy định tính lãi của từng ngân hàng."
)
