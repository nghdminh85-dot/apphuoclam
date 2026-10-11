import os
import re
import pandas as pd
import streamlit as st

# --- CẤU HÌNH TRANG & GIAO DIỆN CHUYÊN NGHIỆP ---
st.set_page_config(
    page_title="Hệ Thống Quản Lý Dân Cư & Đối Soát - Ấp Phước Lâm",
    page_icon="🏛️",
    layout="wide",
)
st.markdown("""
<style>
    /* Đổi màu nền chính của ứng dụng */
    .stApp {
        background-color: #f4f6f9;
    }
    /* Tùy chỉnh tiêu đề chính */
    h1 {
        color: #1f4e78;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Tùy chỉnh các nút bấm */
    .stButton>button {
        background-color: #0066cc;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #004999;
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)
# --- HỆ THỐNG BẢO MẬT BẰNG MẬT KHẨU ---
# Anh/chị có thể đổi mật khẩu ở đây (Ví dụ: "phuoclam2026")
MAT_KHAU_QUAN_TRI = "phuoclam2026"

def kiem_tra_dang_nhap():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
                <div style="background-color:white; padding:30px; border-radius:15px; border:1px solid #ddd; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align:center;">
                <h2 style="color:#007bff; margin-bottom:10px;">🔒 ĐĂNG NHẬP HỆ THỐNG</h2>
                <p style="color:#666; font-size:0.95rem;">Khu vực bảo mật dành riêng cho Cán bộ Quản lý Ấp Phước Lâm</p>
                </div>
            """, unsafe_allow_html=True)
            
            pwd = st.text_input("Nhập Mật khẩu quản trị:", type="password", placeholder="Nhập mật khẩu của bạn...")
            if st.button("🔑 Đăng nhập vào hệ thống", use_container_width=True):
                if pwd == MAT_KHAU_QUAN_TRI:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Mật khẩu không chính xác! Vui lòng thử lại.")
        return False
    return True

# Kiểm tra nếu chưa đăng nhập thì dừng lại ở màn hình khóa
if not kiem_tra_dang_nhap():
    st.stop()

# --- CSS TÙY CHỈNH GIAO DIỆN CAO CẤP ---
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #f0f2f6;
        border-right: 1px solid #e0e0e0;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.2rem;
        font-weight: bold;
        color: #007bff;
    }
</style>
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ CHÍNH ---
st.markdown("""
    <div style="background-color:#007bff;padding:15px;border-radius:10px;margin-bottom:20px">
    <h1 style="color:white;text-align:center;margin:0;font-size:1.8rem;">🏛️ PHẦN MỀM QUẢN LÝ DÂN CƯ & ĐỐI SOÁT - ẤP PHƯỚC LÂM</h1>
    <p style="color:white;text-align:center;margin:5px 0 0 0;font-size:1rem;">Hệ thống điều hành chuyên nghiệp độc quyền</p>
    </div>
    """, unsafe_allow_html=True)

# --- MENU CHỨC NĂNG ---
st.sidebar.markdown("<h3 style='color:#007bff; text-align:center;'>📋 THỰC ĐƠN</h3>", unsafe_allow_html=True)
menu = st.sidebar.radio(
    "",
    [
        "1. Tra cứu & Báo cáo Tổng quan",
        "2. Quản lý Thuê trọ & Biến động",
        "3. Đối soát Khám sức khỏe cả Xã",
        "4. Kiểm tra CCCD hàng loạt",
    ],
)

st.sidebar.markdown("---")
if st.sidebar.button("🔒 Đăng xuất tài khoản"):
    st.session_state.authenticated = False
    st.rerun()

# =============================================================================
# CHỨC NĂNG 1: TRA CỨU & DASHBOARD
# =============================================================================
if menu == "1. Tra cứu & Báo cáo Tổng quan":
    st.subheader("🔍 Tra cứu nhân khẩu & Tổng quan Dữ liệu ấp")
    with st.container():
        file_goc = st.file_uploader("Tải lên file Danh sách gốc Ấp Phước Lâm (.xlsx)", type=["xlsx", "xls"], key="goc1")
        if file_goc:
            df_goc = pd.read_excel(file_goc)
            total_ppl = len(df_goc)
            total_to = df_goc['Tổ'].nunique() if 'Tổ' in df_goc.columns else 0
            
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Tổng Dân số (Gốc)", f"{total_ppl:,}")
            with col2: st.metric("Số lượng Tổ dân cư", f"{total_to:,}")
            with col3: st.metric("Trạng thái", "Đã nạp dữ liệu")

    with st.container():
        if file_goc:
            tu_khoa = st.text_input("🔎 Nhập số CCCD, Họ tên hoặc Tổ dân cư để tra cứu nhanh:")
            if tu_khoa:
                mask = df_goc.astype(str).apply(lambda x: x.str.contains(tu_khoa, case=False)).any(axis=1)
                df_kq = df_goc[mask]
                st.success(f"✅ Tìm thấy **{len(df_kq)}** kết quả phù hợp:")
                st.dataframe(df_kq, use_container_width=True)
            else:
                st.dataframe(df_goc, use_container_width=True)

# =============================================================================
# CHỨC NĂNG 2: QUẢN LÝ THUÊ TRỌ
# =============================================================================
elif menu == "2. Quản lý Thuê trọ & Biến động":
    st.subheader("🏠 Quản lý Thuê trọ & Biến động Cư trú")
    with st.container():
        file_bv = st.file_uploader("Tải lên file dữ liệu nhân khẩu (.xlsx)", type=["xlsx", "xls"], key="bv")
    with st.container():
        if file_bv:
            df_bv = pd.read_excel(file_bv)
            cot_tinhtrang = st.selectbox("Chọn cột phân loại (Ghi chú/Tình trạng):", df_bv.columns)
            cac_tt = df_bv[cot_tinhtrang].dropna().unique().tolist()
            chon_tt = st.multiselect("Lọc theo Tình trạng cụ thể:", cac_tt, default=cac_tt)
            tu_khoa_tro = st.text_input("🔎 Tìm kiếm tên nhà trọ, chủ trọ hoặc địa chỉ:")
            
            df_hien_thị = df_bv[df_bv[cot_tinhtrang].isin(chon_tt)]
            if tu_khoa_tro:
                df_hien_thị = df_hien_thị[df_hien_thị.astype(str).apply(lambda x: x.str.contains(tu_khoa_tro, case=False)).any(axis=1)]
            st.dataframe(df_hien_thị, use_container_width=True)
            st.info(f"Hiển thị: **{len(df_hien_thị)}** nhân khẩu.")

# =============================================================================
# CHỨC NĂNG 3: ĐỐI SOÁT KHÁM SỨC KHỎE
# =============================================================================
elif menu == "3. Đối soát Khám sức khỏe cả Xã":
    st.subheader("🏥 Tách riêng dữ liệu Phước Lâm & Đối soát Khám sức khỏe")
    with st.container():
        col_f1, col_f2 = st.columns(2)
        with col_f1: file_goc = st.file_uploader("1. File Danh sách gốc Ấp Phước Lâm", type=["xlsx", "xls"], key="goc3")
        with col_f2: file_xa = st.file_uploader("2. File Danh sách tổng cả Xã gửi về", type=["xlsx", "xls"], key="xa")
    with st.container():
        if file_goc and file_xa:
            df_goc = pd.read_excel(file_goc)
            df_xa = pd.read_excel(file_xa)
            col_c1, col_c2 = st.columns(2)
            with col_c1: cot_cccd_goc = st.selectbox("Cột CCCD trong file Gốc Phước Lâm:", df_goc.columns)
            with col_c2: cot_cccd_xa = st.selectbox("Cột CCCD trong file Tổng của Xã:", df_xa.columns)
            
            if st.button("⚡ Tiến hành Tách dữ liệu & Đối soát"):
                df_goc["Check"] = df_goc[cot_cccd_goc].astype(str).str.strip().str.replace('.0', '', regex=False)
                df_xa["Check"] = df_xa[cot_cccd_xa].astype(str).str.strip().str.replace('.0', '', regex=False)
                df_phuoc_lam_trong_xa = df_xa[df_xa["Check"].isin(df_goc["Check"])].drop(columns=["Check"])
                df_chua_kham = df_goc[~df_goc["Check"].isin(df_xa["Check"])].drop(columns=["Check"])
                
                tab1, tab2 = st.tabs([f"✅ ĐÃ CÓ TÊN / ĐÃ KHÁM ({len(df_phuoc_lam_trong_xa)})", f"❌ CHƯA CÓ TÊN / CHƯA KHÁM ({len(df_chua_kham)})"])
                with tab1: st.dataframe(df_phuoc_lam_trong_xa, use_container_width=True)
                with tab2: st.dataframe(df_chua_kham, use_container_width=True)

# =============================================================================
# CHỨC NĂNG 4: KIỂM TRA CCCD HÀNG LOẠT
# =============================================================================
elif menu == "4. Kiểm tra CCCD hàng loạt":
    st.subheader("⚡ Kiểm tra nhanh hàng loạt số CCCD (100 - 1000 số)")
    with st.container():
        file_goc = st.file_uploader("1. Tải lên file Danh sách gốc Ấp Phước Lâm", type=["xlsx", "xls"], key="goc2")
        cot_cccd_goc = st.text_input("Tên cột CCCD trong file gốc:", value="CCCD")
        danh_sach_nhap = st.text_area("2. Dán danh sách số CCCD vào đây (Mỗi số 1 dòng hoặc cách nhau bằng dấu phẩy):", height=200)
    with st.container():
        if file_goc and danh_sach_nhap:
            if st.button("🚀 Bắt đầu quét và kiểm tra hàng loạt"):
                df_goc = pd.read_excel(file_goc)
                danh_sach_check = [str(x.strip()).replace('.0', '') for x in re.split(r",|\n|\s+", danh_sach_nhap) if x.strip()]
                df_goc["CCCD_Chuan"] = df_goc[cot_cccd_goc].astype(str).str.strip().str.replace('.0', '', regex=False)
                
                df_la_dan_pl = df_goc[df_goc["CCCD_Chuan"].isin(danh_sach_check)].drop(columns=["CCCD_Chuan"])
                cccd_co = df_la_dan_pl[cot_cccd_goc].astype(str).str.strip().str.replace('.0', '', regex=False).tolist()
                cccd_khong_phai = [c for c in danh_sach_check if c not in cccd_co]
                
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    st.success(f"✅ Thuộc dân cư Phước Lâm ({len(df_la_dan_pl)} người):")
                    st.dataframe(df_la_dan_pl, use_container_width=True)
                with col_res2:
                    if cccd_khong_phai:
                        st.warning(f"⚠️ Không thuộc Phước Lâm ({len(cccd_khong_phai)} số):")
                        st.write(cccd_khong_phai)
                    else:
                        st.success("🎉 Tất cả đều thuộc dân cư Phước Lâm!")
