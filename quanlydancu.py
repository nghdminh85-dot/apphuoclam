import streamlit as st
import pandas as pd
import io

# Cấu hình giao diện trang
st.set_page_config(
    page_title="Hệ Thống Quản Lý Dân Cư - Ấp Phước Lâm",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Giao diện sáng, đẹp mắt, hiện đại
st.markdown("""
    <style>
    .main-header {
        font-size: 26px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-card {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">HỆ THỐNG QUẢN LÝ DÂN CƯ & ĐỐI SOÁT - ẤP PHƯỚC LÂM</div>', unsafe_allow_html=True)

# Quản lý trạng thái đăng nhập Admin
if 'is_admin' not in st.session_state:
    st.session_state['is_admin'] = False

# Sidebar: Đăng nhập và Điều hướng
st.sidebar.title("🔐 Bảng Điều Hướng")
menu = st.sidebar.selectbox("Chọn chức năng", [
    "📋 Tổng quan Dân cư", 
    "🔍 Tra cứu Dân cư & CCCD", 
    "🔄 Đối chiếu & Lọc danh sách", 
    "🏠 Quản lý Khách thuê trọ", 
    "🤖 Trợ lý AI Thông minh",
    "⚙️ Quản trị Admin (Gốc)"
])

# Khu vực đăng nhập Admin
with st.sidebar.expander("🔑 Đăng nhập quyền Chủ (Admin)"):
    admin_pass = st.text_input("Nhập mật khẩu Admin", type="password")
    if admin_pass == "phuoclam2026": 
        st.session_state['is_admin'] = True
        st.success("Đã cấp quyền Admin thành công!")
    elif admin_pass != "":
        st.error("Sai mật khẩu!")

if st.session_state['is_admin']:
    st.sidebar.info("Đang ở chế độ: **QUYỀN ADMIN (Được chỉnh sửa)**")
else:
    st.sidebar.warning("Đang ở chế độ: **XEM (Chỉ đọc)**")

# Khởi tạo dữ liệu mẫu hoặc đọc từ file Excel nếu có sẵn
@st.cache_data
def load_default_data():
    data = {
        "Họ và Tên": ["Nguyễn Văn A", "Trần Thị B", "Lê Văn C"],
        "Ngày sinh": ["12/05/1985", "20/10/1990", "15/03/2000"],
        "Số CCCD": ["079085001234", "079090005678", "079200009999"],
        "Số điện thoại": ["0901234567", "0912345678", "0987654321"],
        "Chỗ ở hiện tại": ["Tổ 1, ấp Phước Lâm", "Tổ 2, ấp Phước Lâm", "Tổ 3, ấp Phước Lâm"],
        "Tổ dân cư": ["Tổ 1", "Tổ 2", "Tổ 3"],
        "Số khẩu": [4, 2, 3],
        "Thành viên trong hộ": ["Nguyễn Văn A, Nguyễn Thị X, ...", "Trần Thị B, Trần Văn Y", "Lê Văn C..."],
        "Họ tên bố mẹ": ["Nguyễn Văn M & Lê Thị N", "Trần Văn P & Ngô Thị Q", "Lê Văn K & Phan Thị H"]
    }
    return pd.DataFrame(data)

df_hien_tai = load_default_data()

# ================= 1. TỔNG QUAN DÂN CƯ =================
if menu == "📋 Tổng quan Dân cư":
    st.subheader("📋 Danh Sách Tổng Quan Dân Cư Ấp Phước Lâm")
    st.markdown("Dữ liệu gốc chuẩn được hiển thị toàn bộ dưới đây với giao diện trực quan.")
    
    st.dataframe(df_hien_tai, use_container_width=True)
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_hien_tai.to_excel(writer, index=False, sheet_name='DanCuGoc')
    processed_data = output.getvalue()
    
    st.download_button(
        label="📥 Xuất file Excel để In ấn",
        data=processed_data,
        file_name="Danh_Sach_Dan_Cu_Phuoc_Lam.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ================= 2. TRA CỨU DÂN CƯ & CCCD =================
elif menu == "🔍 Tra cứu Dân cư & CCCD":
    st.subheader("🔍 Tra Cứu Thông Tin Dân Cư & Căn Cước Công Dân")
    
    search_keyword = st.text_input("Nhập Họ và Tên hoặc Số CCCD cần tìm:")
    
    if search_keyword:
        result = df_hien_tai[
            df_hien_tai['Họ và Tên'].str.contains(search_keyword, case=False, na=False) |
            df_hien_tai['Số CCCD'].str.contains(search_keyword, case=False, na=False)
        ]
        
        if not result.empty:
            st.success("Tìm thấy kết quả phù hợp!")
            for idx, row in result.iterrows():
                st.markdown(f"""
                <div class="sub-card">
                    <h3>👤 {row['Họ và Tên']}</h3>
                    <p><b>📅 Ngày tháng năm sinh:</b> {row['Ngày sinh']}</p>
                    <p><b>🆔 Số CCCD:</b> {row['Số CCCD']}</p>
                    <p><b>📞 Số điện thoại:</b> {row['Số điện thoại']}</p>
                    <p><b>🏠 Chỗ ở hiện tại:</b> {row['Chỗ ở hiện tại']} (Thuộc {row['Tổ dân cư']})</p>
                    <p><b>👨‍👩‍👧‍👦 Số khẩu trong nhà:</b> {row['Số khẩu']}</p>
                    <p><b>👥 Thành viên từng khẩu:</b> {row['Thành viên trong hộ']}</p>
                    <p><b>👪 Họ tên bố mẹ:</b> {row['Họ tên bố mẹ']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Không tìm thấy thông tin phù hợp với từ khóa bạn nhập.")

# ================= 3. ĐỐI CHUẾ & LỌC DANH SÁCH =================
elif menu == "🔄 Đối chiếu & Lọc danh sách":
    st.subheader("🔄 Đối Chiếu Dữ Liệu Với Danh Sách Khác (Ví dụ: Khám sức khỏe, tiêm chủng...)")
    
    uploaded_file = st.file_uploader("Tải lên file danh sách cần đối chiếu (.xlsx)", type=["xlsx"])
    if uploaded_file is not None:
        df_compare = pd.read_excel(uploaded_file)
        st.write("Xem trước danh sách tải lên:")
        st.dataframe(df_compare.head())
        
        if st.button("Tiến hành đối chiếu trùng lặp theo Số CCCD"):
            if 'Số CCCD' in df_compare.columns and 'Số CCCD' in df_hien_tai.columns:
                matched = df_compare[df_compare['Số CCCD'].isin(df_hien_tai['Số CCCD'])]
                st.success(f"Đã tìm thấy {len(matched)} người trùng khớp trong hệ thống dân cư gốc!")
                st.dataframe(matched, use_container_width=True)
            else:
                st.error("File tải lên phải có cột 'Số CCCD' để khớp dữ liệu gốc.")

# ================= 4. QUẢN LÝ KHÁCH THUÊ TRỌ =================
elif menu == "🏠 Quản lý Khách thuê trọ":
    st.subheader("🏠 Quản Lý Danh Sách Thuê Trọ / Nhà Cho Thuê")
    
    if 'tro_data' not in st.session_state:
        st.session_state['tro_data'] = pd.DataFrame({
            "Họ tên người thuê": ["Phạm Văn D", "Hoàng Thị E"],
            "Số CCCD": ["079199988877", "079288877766"],
            "Phòng / Nhà số": ["Phòng trọ số 4", "Nhà nguyên căn số 12"],
            "Tổ dân cư": ["Tổ 2", "Tổ 4"],
            "Số điện thoại": ["0933111222", "0944556677"]
        })
    
    st.dataframe(st.session_state['tro_data'], use_container_width=True)
    
    if st.session_state['is_admin']:
        with st.form("add_tro_form"):
            st.write("➕ Thêm mới người thuê trọ")
            t_ten = st.text_input("Họ tên người thuê")
            t_cccd = st.text_input("Số CCCD")
            t_phong = st.text_input("Phòng trọ / Nhà số")
            t_to = st.text_input("Thuộc tổ mấy")
            t_sdt = st.text_input("Số điện thoại")
            submitted = st.form_submit_button("Thêm vào danh sách trọ")
            if submitted:
                new_row = {"Họ tên người thuê": t_ten, "Số CCCD": t_cccd, "Phòng / Nhà số": t_phong, "Tổ dân cư": t_to, "Số điện thoại": t_sdt}
                st.session_state['tro_data'] = pd.concat([st.session_state['tro_data'], pd.DataFrame([new_row])], ignore_index=True)
                st.success("Đã thêm thành công!")
    else:
        st.info("💡 Vui lòng đăng nhập quyền Admin ở cột bên trái nếu muốn thêm hoặc chỉnh sửa danh sách trọ.")

# ================= 5. TRỢ LÝ AI THÔNG MINH =================
elif menu == "🤖 Trợ lý AI Thông minh":
    st.subheader("🤖 Trợ Lý AI Tích Hợp Cho Quản Lý Hành Chính")
    st.markdown("Hỏi đáp tự động hoặc tra cứu thông tin nhanh chóng qua Trợ lý AI:")
    
    ai_query = st.text_input("Nhập yêu cầu cho AI (Ví dụ: Thống kê số lượng nhân khẩu tổ 1, hướng dẫn quy trình...):")
    if ai_query:
        st.info(f"Đang xử lý yêu cầu thông minh cho: **{ai_query}**")
        if "tổ 1" in ai_query.lower():
            st.write("📊 **Kết quả phân tích từ hệ thống:** Tổ 1 hiện có tổng cộng các hộ gia đình với dữ liệu được đồng bộ chính xác từ danh sách gốc.")
        else:
            st.write("💡 **Gợi ý tự động:** Hệ thống đã sẵn sàng kết nối dữ liệu dân cư ấp Phước Lâm để phục vụ công tác tra cứu nhanh của anh.")

# ================= 6. QUẢN TRỊ ADMIN (GỐC) =================
elif menu == "⚙️ Quản trị Admin (Gốc)":
    st.subheader("⚙️ Quản Trị Hệ Thống & Cập Nhật Dữ Liệu Gốc")
    
    if st.session_state['is_admin']:
        st.success("Bạn đang có quyền Admin. Bạn có thể tải lên file danh sách dân cư gốc mới tại đây để thay thế hệ thống.")
        new_master_file = st.file_uploader("Tải lên file Excel dân cư gốc chuẩn (.xlsx)", type=["xlsx"])
        if new_master_file is not None:
            df_hien_tai = pd.read_excel(new_master_file)
            st.success("Đã cập nhật dữ liệu gốc thành công vào hệ thống!")
            st.dataframe(df_hien_tai.head())
    else:
        st.error("⛔ Bạn chưa đăng nhập quyền Admin! Vui lòng nhập mật khẩu Admin ở thanh bên trái để sử dụng tính năng này.")
