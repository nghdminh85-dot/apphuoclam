import streamlit as st
import pandas as pd

# CẤU HÌNH TRANG VÀ GIAO DIỆN CHUYÊN NGHIỆP
st.set_page_config(
    page_title="Hệ thống Quản lý Dân cư & Đối soát - Ấp Phước Lâm",
    page_icon="🏛️",
    layout="wide"
)

# Giao diện CSS tùy chỉnh màu sắc sinh động, nổi bật và chuyên nghiệp
st.markdown("""
    <style>
        .stApp {
            background-color: #f4f7f6;
        }
        h1, h2, h3 {
            color: #1f4e78;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .main-header {
            background: linear-gradient(90deg, #1f4e78, #2e75b6);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 25px;
        }
        .stButton>button {
            background-color: #2e75b6;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            border: none;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #1f4e78;
        }
    </style>
""", unsafe_allow_html=True)

# TIÊU ĐỀ CHÍNH VỚI GIAO DIỆN ẤN TƯỢNG
st.markdown("""
    <div class="main-header">
        <h1>🏛️ HỆ THỐNG QUẢN LÝ DÂN CƯ & ĐỐI SOÁT</h1>
        <p style="font-size: 18px; margin: 0;">Ấp Phước Lâm - Tự động hóa 100% chuyên nghiệp</p>
    </div>
""", unsafe_allow_html=True)

# ----------------- HỆ THỐNG ĐĂNG NHẬP BẢO MẬT -----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.subheader("🔐 Đăng nhập hệ thống quản lý")
    role = st.selectbox("Chọn vai trò đăng nhập:", ["Thành viên (Tra cứu)", "Admin / Chủ quản lý (Toàn quyền)"])
    password = st.text_input("Nhập mật khẩu:", type="password")
    
    if st.button("Xác nhận đăng nhập"):
        if role == "Admin / Chủ quản lý (Toàn quyền)" and password == "admin123": # Mật khẩu admin mẫu, có thể đổi
            st.session_state.authenticated = True
            st.session_state.role = "admin"
            st.success("Đăng nhập thành công với quyền Admin!")
            st.rerun()
        elif role == "Thành viên (Tra cứu)" and password == "phuoclam123": # Mật khẩu thành viên mẫu
            st.session_state.authenticated = True
            st.session_state.role = "member"
            st.success("Đăng nhập thành công!")
            st.rerun()
        else:
            st.error("Mật khẩu không chính xác!")
    st.stop()

# Đăng xuất
if st.sidebar.button("Đăng xuất tài khoản"):
    st.session_state.authenticated = False
    st.rerun()

# ----------------- QUẢN LÝ FILE DỮ LIỆU GỐC (EXCEL) -----------------
st.sidebar.markdown("---")
st.sidebar.subheader("📂 Quản lý Dữ liệu Excel")

# Tải lên danh sách gốc (Chỉ Admin mới được thay đổi file gốc)
if st.session_state.role == "admin":
    uploaded_file = st.sidebar.file_uploader("Tải lên Danh sách dân cư gốc (.xlsx)", type=["xlsx", "xls"])
    if uploaded_file is not None:
        st.session_state.df_goc = pd.read_excel(uploaded_file)
        st.sidebar.success("Đã cập nhật danh sách gốc thành công!")
else:
    st.sidebar.info("Bạn đang ở chế độ Thành viên: Dữ liệu gốc được bảo vệ, không thể chỉnh sửa.")
    if "df_goc" not in st.session_state:
        st.session_state.df_goc = None

# Kiểm tra nếu chưa có dữ liệu
if "df_goc" not in st.session_state or st.session_state.df_goc is None:
    st.warning("⚠️ Vui lòng yêu cầu Admin tải lên file Excel dữ liệu dân cư gốc ở thanh bên trái để bắt đầu!")
    st.stop()

df = st.session_state.df_goc

# ----------------- HIỂN THỊ DANH SÁCH TỔNG QUAN KHI MỞ PHẦN MỀM -----------------
st.markdown("### 📋 Danh sách Tổng quan Dân cư")
st.dataframe(df, use_container_width=True)

st.markdown("---")

# ----------------- CÁC TÍNH NĂNG CHÍNH -----------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Tra cứu nhân khẩu & CCCD", 
    "🏠 Quản lý Nhà trọ / Thuê nhà", 
    "📊 Đối chiếu & Lọc danh sách", 
    "⚙️ Cài đặt & Quản trị"
])

# --- TAB 1: TRA CỨU CHI TIẾT DÂN CƯ & CCCD ---
with tab1:
    st.subheader("tra cứu thông tin chi tiết công dân")
    keyword = st.text_input("Nhập Họ tên hoặc Số Căn cước công dân (CCCD) cần tìm:")
    
    if keyword:
        # Lọc dữ liệu theo từ khóa
        mask = df.astype(str).apply(lambda x: x.str.contains(keyword, case=False, na=False)).any(axis=1)
        res = df[mask]
        
        if not res.empty:
            st.success(f"Tìm thấy {len(res)} kết quả phù hợp!")
            for idx, row in res.iterrows():
                with st.expander(f"Họ tên: {row.get('HoTen', 'N/A')} - CCCD: {row.get('SoCCCD', 'N/A')} (Bấm để xem chi tiết)"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**👤 Họ và tên:** {row.get('HoTen', 'N/A')}")
                        st.markdown(f"**📅 Ngày sinh:** {row.get('NgaySinh', 'N/A')}")
                        st.markdown(f"**🆔 Số Căn cước:** {row.get('SoCCCD', 'N/A')}")
                        st.markdown(f"**📞 Số điện thoại:** {row.get('SoDienThoai', 'N/A')}")
                        st.markdown(f"**🏠 Chỗ ở hiện tại:** {row.get('ChoO', 'N/A')}")
                    with col2:
                        st.markdown(f"**📍 Tổ dân cư số:** {row.get('ToDanCu', 'N/A')}")
                        st.markdown(f"**👨‍👩‍👧 Tổng số khẩu trong nhà:** {row.get('SoKhau', 'N/A')}")
                        st.markdown(f"**👥 Danh sách từng khẩu:** {row.get('ThanhVienKhau', 'N/A')}")
                        st.markdown(f"**👨‍👩‍👦 Họ tên Bố/Mẹ:** {row.get('BoMe', 'N/A')}")
        else:
            st.warning("Không tìm thấy thông tin phù hợp với từ khóa.")

# --- TAB 2: QUẢN LÝ NGƯỜI THUÊ TRỌ ---
with tab2:
    st.subheader("🏠 Quản lý danh sách người thuê trọ / thuê nhà")
    if "Tro" in df.columns or any("trọ" in str(c).lower() for c in df.columns):
        # Lọc các dòng có thông tin thuê trọ
        tro_df = df[df.astype(str).apply(lambda x: x.str.contains("trọ|thuê", case=False, na=False)).any(axis=1)]
        st.dataframe(tro_df, use_container_width=True)
    else:
        st.info("File Excel gốc cần có cột thông tin về 'Phòng trọ' hoặc 'Thuê nhà' để hệ thống tự động tổng hợp.")
        st.dataframe(df, use_container_width=True)

# --- TAB 3: ĐỐI CHUẾ VÀ LỌC DANH SÁCH ---
with tab3:
    st.subheader("📊 Đối chiếu & Lọc danh sách khác (Kiểm tra trùng lặp)")
    compare_file = st.file_uploader("Tải lên danh sách cần đối chiếu (.xlsx hoặc .csv)", type=["xlsx", "csv"])
    
    if compare_file is not None:
        if compare_file.name.endswith('.csv'):
            compare_df = pd.read_csv(compare_file)
        else:
            compare_df = pd.read_excel(compare_file)
            
        st.write("Dữ liệu danh sách cần kiểm tra:", compare_df.head())
        
        # Chọn cột để đối chiếu (ví dụ: Số CCCD hoặc Họ tên)
        col_to_check = st.selectbox("Chọn cột dùng để đối chiếu trùng lặp:", compare_df.columns)
        
        if st.button("Thực hiện đối chiếu tự động"):
            if col_to_check in df.columns:
                matched = compare_df[compare_df[col_to_check].isin(df[col_to_check])]
                st.warning(f"⚠️ Phát hiện {len(matched)} trường hợp trùng khớp với danh sách gốc:")
                st.dataframe(matched, use_container_width=True)
            else:
                st.error(f"Cột '{col_to_check}' không tồn tại trong danh sách gốc của ấp.")

# --- TAB 4: CÀI ĐẶT & QUẢN TRỊ ---
with tab4:
    st.subheader("⚙️ Cài đặt hệ thống")
    st.markdown("- **Trạng thái hệ thống:** Đang hoạt động ổn định tự động 100%.")
    st.markdown("- **Quyền hiện tại:** " + ("Admin (Toàn quyền)" if st.session_state.role == "admin" else "Thành viên (Chỉ tra cứu)"))
    st.info("Mọi thao tác chỉnh sửa dữ liệu gốc đều được kiểm soát chặt chẽ qua tài khoản Admin để đảm bảo an toàn thông tin.")
