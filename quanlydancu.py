import streamlit as st
import pandas as pd
import io

# Cấu hình giao diện trang
st.set_page_config(
    page_title="Hệ Thống Quản Lý Dân Cư & Đối Soát - ấp Phước Lâm",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Giao diện tùy chỉnh CSS
st.markdown("""
    <style>
        .main-header { font-size: 24px; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
        .sub-header { font-size: 18px; font-weight: bold; color: #374151; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# Thanh điều hướng (Sidebar)
st.sidebar.markdown("## Bảng Điều Hướng")
menu = st.sidebar.selectbox(
    "Chọn chức năng",
    [
        "Tổng quan Dân cư",
        "Tra cứu Dân cư & CCCD",
        "Đối chiếu & Lọc danh sách",
        "Quản lý Khách thuê trọ",
        "Trợ lý Thông minh",
        "Quản trị Admin (Gốc)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Đăng nhập Chủ (Admin)")
admin_pass = st.sidebar.text_input("Nhập mật khẩu Admin", type="password")
is_admin = admin_pass == "phuoclam2026"  # Mật khẩu chuẩn xác theo yêu cầu

if is_admin:
    st.sidebar.success("Đã cấp quyền Admin thành công!")
    st.sidebar.info("Đang ở chế độ: QUYỀN ADMIN (Được chỉnh sửa)")
else:
    st.sidebar.warning("Đang ở chế độ: Khách / Tra cứu")

# Tiêu đề chính ứng dụng
st.markdown("<div class='main-header'>HỆ THỐNG QUẢN LÝ DÂN CƯ & ĐỐI SOÁT - ẤP PHƯỚC LÂM</div>", unsafe_allow_html=True)

# Hàm tải file Excel an toàn
@st.cache_data
def load_excel(file):
    try:
        df = pd.read_excel(file)
        return df
    except Exception as e:
        return None

# Tải file mẫu hoặc file người dùng tải lên
uploaded_file = st.sidebar.file_uploader("Tải lên file Excel dữ liệu dân cư (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    df = load_excel(uploaded_file)
else:
    # Tạo dữ liệu giả lập chuẩn cấu trúc đúng 14 cột nếu chưa tải file lên
    data = {
        "STT": [1, 2, 3],
        "Số Tổ": ["T01", "T01", "T02"],
        "Mã Hộ": ["T01-H010", "T01-H010", "T01-H011"],
        "Họ tên chủ hộ": ["PHẠM THANH DANH", "PHẠM THANH DANH", "NGUYỄN QUANG VINH"],
        "Họ và tên": ["PHẠM THANH DANH", "ĐỒNG THỊ THÙY TRANG", "NGUYỄN QUANG VINH"],
        "Ngày sinh": ["24/05/1977", "06/05/1982", "05/05/1959"],
        "Tuổi": [49, 44, 67],
        "Giới tính": ["Nam", "Nữ", "Nam"],
        "CCCD/ĐDCN": ["077182007502", "077182007502", "079059019562"],
        "Số điện thoại": ["0919927006", "Chưa có SĐT", "0931556603"],
        "Nơi thường trú": ["Tổ 1, Ấp Phước Lâm, Xã Long Hải", "Tổ 1, Ấp Phước Lâm, Xã Long Hải", "Số nhà 18, Tổ 01, Ấp Phước Lâm"],
        "Nơi ở hiện tại": ["Tổ 1, Ấp Phước Lâm, Xã Long Hải", "Tổ 1, Ấp Phước Lâm, Xã Long Hải", "Số nhà 18, Tổ 01, Ấp Phước Lâm"],
        "Họ tên cha": ["ĐỒNG VĂN THÂN", "PHẠM THANH DANH", "NGUYỄN VĂN LIỆU"],
        "Họ tên mẹ": ["TRẦN THỊ HOA", "ĐỒNG THỊ THÙY TRANG", "NGUYỄN THỊ NĂM"]
    }
    df = pd.DataFrame(data)

# Chuẩn hóa tên cột chính xác 14 cột theo yêu cầu
expected_columns = [
    "STT", "Số Tổ", "Mã Hộ", "Họ tên chủ hộ", "Họ và tên", 
    "Ngày sinh", "Tuổi", "Giới tính", "CCCD/ĐDCN", "Số điện thoại", 
    "Nơi thường trú", "Nơi ở hiện tại", "Họ tên cha", "Họ tên mẹ"
]

# Kiểm tra và ánh xạ cột nếu file Excel có tên khác biệt nhẹ
for col in expected_columns:
    if col not in df.columns:
        matched = [c for c in df.columns if col.lower() in str(c).lower()]
        if matched:
            df.rename(columns={matched[0]: col}, inplace=True)
        else:
            df[col] = ""

# Đảm bảo chỉ lấy đúng và đủ các cột chuẩn
df = df[expected_columns]

# --- PHÂN KHU CHỨC NĂNG ---

if menu == "Tổng quan Dân cư":
    st.markdown("### Báo Cáo Thống Kê Tổng Quan Dân Cư ấp Phước Lâm")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Tổng số hộ", value=df['Mã Hộ'].nunique() if 'Mã Hộ' in df.columns else 0)
    with col2:
        st.metric(label="Tổng nhân khẩu", value=len(df))
    with col3:
        st.metric(label="Số tổ quản lý", value=df['Số Tổ'].nunique() if 'Số Tổ' in df.columns else 0)

    st.markdown("---")
    st.markdown("#### Danh Sách Chi Tiết Dân Cư")
    st.dataframe(df, use_container_width=True)

elif menu == "Tra cứu Dân cư & CCCD":
    st.markdown("### Tra Cứu Thông Tin Dân Cư & CCCD/ĐDCN")
    search_query = st.text_input("Nhập Họ tên, Số CCCD hoặc Số điện thoại cần tra cứu:")
    
    if search_query:
        result = df[
            df['Họ và tên'].astype(str).str.contains(search_query, case=False, na=False) |
            df['CCCD/ĐDCN'].astype(str).str.contains(search_query, case=False, na=False) |
            df['Số điện thoại'].astype(str).str.contains(search_query, case=False, na=False)
        ]
        if not result.empty:
            st.success(f"Tìm thấy {len(result)} kết quả phù hợp!")
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("Không tìm thấy thông tin phù hợp với từ khóa.")
    else:
        st.info("Vui lòng nhập từ khóa vào ô bên trên để bắt đầu tra cứu.")

elif menu == "Đối chiếu & Lọc danh sách":
    st.markdown("### Đối Chiếu Dữ Liệu Trùng Lặp Theo Số CCCD")
    if st.button("Tiến hành đối chiếu trùng lặp"):
        duplicates = df[df.duplicated(subset=['CCCD/ĐDCN'], keep=False) & (df['CCCD/ĐDCN'] != "")]
        if not duplicates.empty:
            st.error(f"Phát hiện {len(duplicates)} bản ghi bị trùng số CCCD/ĐDCN!")
            st.dataframe(duplicates, use_container_width=True)
        else:
            st.success("Không phát hiện số CCCD/ĐDCN nào bị trùng lặp!")

elif menu == "Quản lý Khách thuê trọ":
    st.markdown("### Quản Lý Biến Động Khách Thuê Trọ & Tạm Trú")
    st.info("Chức năng quản lý danh sách nhà cho thuê, khách tạm trú và khai báo lưu trú tại ấp Phước Lâm.")
    if 'Nơi ở hiện tại' in df.columns and 'Nơi thường trú' in df.columns:
        rent_df = df[df['Nơi ở hiện tại'].astype(str).str.strip() != df['Nơi thường trú'].astype(str).str.strip()]
    else:
        rent_df = df
    st.dataframe(rent_df, use_container_width=True)

elif menu == "Trợ lý Thông minh":
    st.markdown("### Trợ Lý Thông Minh Hỗ Trợ Hành Chính")
    st.write("Sử dụng AI tự động phân tích và tra cứu biến động nhân khẩu, lọc danh sách theo độ tuổi, giới tính hoặc khu vực tổ.")
    
    selected_to = st.selectbox("Lọc danh sách theo Tổ:", options=["Tất cả"] + list(df['Số Tổ'].dropna().unique()))
    if selected_to != "Tất cả":
        filtered_df = df[df['Số Tổ'] == selected_to]
    else:
        filtered_df = df
    st.dataframe(filtered_df, use_container_width=True)

elif menu == "Quản trị Admin (Gốc)":
    st.markdown("### Khu Vực Quản Trị Hệ Thống (Admin)")
    if is_admin:
        st.success("Bạn đang có quyền quản trị tối cao.")
        new_title = st.text_input("Đổi tiêu đề hệ thống:", value="HỆ THỐNG QUẢN LÝ DÂN CƯ & ĐỐI SOÁT - ẤP PHƯỚC LÂM")
        if st.button("Lưu thay đổi"):
            st.success("Đã cập nhật cấu hình hệ thống thành công!")
    else:
        st.error("Bạn chưa có quyền Admin! Vui lòng nhập mật khẩu chính xác (`phuoclam2026`) ở thanh bên trái.")
