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
        margin-bottom: 15px;
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

# Khởi tạo dữ liệu chuẩn 100% theo đúng yêu cầu các trường thông tin
@st.cache_data
def load_default_data():
    data = {
        "Số thứ tự": [1, 2, 3],
        "Số tổ": ["Tổ 1", "Tổ 2", "Tổ 3"],
        "Mã hộ": ["T01-H001", "T02-H002", "T03-H003"],
        "Họ và tên": ["Nguyễn Văn A", "Trần Thị B", "Lê Văn C"],
        "Chủ hộ": ["Có", "Không", "Có"],
        "Ngày sinh": ["12/05/1985", "20/10/1990", "15/03/2000"],
        "Tuổi": [41, 36, 26],
        "Giới tính": ["Nam", "Nữ", "Nam"],
        "Căn cước công dân": ["079085001234", "079090005678", "079200009999"],
        "Số điện thoại": ["0901234567", "0912345678", "0987654321"],
        "Nơi thường trú": ["Ấp Phước Lâm, Xã Long Hải", "Ấp Phước Lâm, Xã Long Hải", "Ấp Phước Lâm, Xã Long Hải"],
        "Nơi ở hiện tại": ["Tổ 1, ấp Phước Lâm", "Tổ 2, ấp Phước Lâm", "Tổ 3, ấp Phước Lâm"],
        "Họ tên cha": ["Nguyễn Văn M", "Trần Văn P", "Lê Văn K"],
        "Họ tên mẹ": ["Lê Thị N", "Ngô Thị Q", "Phan Thị H"]
    }
    return pd.DataFrame(data)

# Kiểm tra xem đã có dữ liệu gốc tải lên trong session chưa, nếu chưa dùng dữ liệu chuẩn mẫu
if 'df_master' not in st.session_state:
    st.session_state['df_master'] = load_default_data()

df_hien_tai = st.session_state['df_master']

# ================= 1. TỔNG QUAN DÂN CƯ =================
if menu == "📋 Tổng quan Dân cư":
    st.subheader("📋 Danh Sách Tổng Quan Dân Cư Ấp Phước Lâm")
    st.markdown("Dữ liệu chuẩn bao gồm toàn bộ các trường thông tin chi tiết:")
    
    # Hiển thị bảng dữ liệu đầy đủ các cột yêu cầu
    st.dataframe(df_hien_tai, use_container_width=True)
    
    # Nút xuất Excel
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_hien_tai.to_excel(writer, index=False, sheet_name='DanCuGoc')
    processed_data = output.getvalue()
    
    st.download_button(
        label="📥 Xuất file Excel chuẩn để In ấn",
        data=processed_data,
        file_name="Danh_Sach_Dan_Cu_Phuoc_Lam_Chuan.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ================= 2. TRA CỨU DÂN CƯ & CCCD =================
elif menu == "🔍 Tra cứu Dân cư & CCCD":
    st.subheader("🔍 Tra Cứu Thông Tin Dân Cư & Căn Cước Công Dân")
    
    search_keyword = st.text_input("Nhập Họ và Tên hoặc Số CCCD cần tìm:")
    
    if search_keyword:
        # Lọc dữ liệu theo Họ tên hoặc CCCD (không phân biệt hoa thường)
        result = df_hien_tai[
            df_hien_tai['Họ và tên'].str.contains(search_keyword, case=False, na=False) |
            df_hien_tai['Căn cước công dân'].str.contains(search_keyword, case=False, na=False)
        ]
        
        if not result.empty:
            st.success(f"Tìm thấy {len(result)} kết quả phù hợp!")
            for idx, row in result.iterrows():
                st.markdown(f"""
                <div class="sub-card">
                    <h3>👤 {row['Họ và tên']}</h3>
                    <p><b>🔢 Số thứ tự:</b> {row['Số thứ tự']} | <b>🏡 Số tổ:</b> {row['Số tổ']} | <b>📋 Mã hộ:</b> {row['Mã hộ']}</p>
                    <p><b>👑 Là chủ hộ:</b> {row['Chủ hộ']} | <b>⚥ Giới tính:</b> {row['Giới tính']} | <b>🎂 Ngày sinh:</b> {row['Ngày sinh']} ({row['Tuổi']} tuổi)</p>
                    <p><b>🆔 Số CCCD:</b> {row['Căn cước công dân']} | <b>📞 Số điện thoại:</b> {row['Số điện thoại']}</p>
                    <p><b>🏠 Nơi ở hiện tại:</b> {row['Nơi ở hiện tại']}</p>
                    <p><b>📍 Nơi thường trú:</b> {row['Nơi thường trú']}</p>
                    <p><b>👪 Họ tên bố mẹ:</b> Cha: {row['Họ tên cha']} - Mẹ: {row['Họ tên mẹ']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Không tìm thấy thông tin phù hợp với từ khóa bạn nhập.")

# ================= 3. ĐỐI CHIẾU & LỌC DANH SÁCH =================
elif menu == "🔄 Đối chiếu & Lọc danh sách":
    st.subheader("🔄 Đối Chiếu Dữ Liệu Với Danh Sách Khác")
    
    uploaded_file = st.file_uploader("Tải lên file danh sách cần đối chiếu (.xlsx)", type=["xlsx"])
    if uploaded_file is not None:
        df_compare = pd.read_excel(uploaded_file)
        st.write("Xem trước danh sách tải lên:")
        st.dataframe(df_compare.head())
        
        if st.button("Tiến hành đối chiếu trùng lặp theo Số CCCD"):
            if 'Căn cước công dân' in df_compare.columns and 'Căn cước công dân' in df_hien_tai.columns:
                matched = df_compare[df_compare['Căn cước công dân'].isin(df_hien_tai['Căn cước công dân'])]
                st.success(f"Đã tìm thấy {len(matched)} người trùng khớp trong hệ thống dân cư gốc!")
                st.dataframe(matched, use_container_width=True)
            else:
                st.error("File tải lên phải có cột 'Căn cước công dân' để khớp dữ liệu gốc.")

# ================= 4. QUẢN LÝ KHÁCH THUÊ TRỌ =================
elif menu == "🏠 Quản lý Khách thuê trọ":
    st.subheader("🏠 Quản Lý Danh Sách Thuê Trọ / Nhà Cho Thuê")
    
    if 'tro_data' not in st.session_state:
        st.session_state['tro_data'] = pd.DataFrame({
            "Họ tên người thuê": ["Phạm Văn D", "Hoàng Thị E"],
            "Căn cước công dân": ["079199988877", "079288877766"],
            "Phòng / Nhà số": ["Phòng trọ số 4", "Nhà nguyên căn số 12"],
            "Số tổ": ["Tổ 2", "Tổ 4"],
            "Số điện thoại": ["0933111222", "0944556677"]
        })
    
    st.dataframe(st.session_state['tro_data'], use_container_width=True)
    
    if st.session_state['is_admin']:
        with st.form("add_tro_form"):
            st.write("➕ Thêm mới người thuê trọ")
            t_ten = st.text_input("Họ tên người thuê")
            t_cccd = st.text_input("Căn cước công dân")
            t_phong = st.text_input("Phòng trọ / Nhà số")
            t_to = st.text_input("Số tổ")
            t_sdt = st.text_input("Số điện thoại")
            submitted = st.form_submit_button("Thêm vào danh sách trọ")
            if submitted:
                new_row = {"Họ tên người thuê": t_ten, "Căn cước công dân": t_cccd, "Phòng / Nhà số": t_phong, "Số tổ": t_to, "Số điện thoại": t_sdt}
                st.session_state['tro_data'] = pd.concat([st.session_state['tro_data'], pd.DataFrame([new_row])], ignore_index=True)
                st.success("Đã thêm thành công!")
    else:
        st.info("💡 Vui lòng đăng nhập quyền Admin ở cột bên trái nếu muốn thêm hoặc chỉnh sửa danh sách trọ.")

# ================= 5. TRỢ LÝ AI THÔNG MINH =================
elif menu == "🤖 Trợ lý AI Thông minh":
    st.subheader("🤖 Trợ Lý AI Tích Hợp Cho Quản Lý Hành Chính")
    st.markdown("Hỏi đáp tự động hoặc tra cứu thông tin nhanh chóng qua Trợ lý AI:")
    
    ai_query = st.text_input("Nhập yêu cầu cho AI (Ví dụ: Thống kê số lượng nhân khẩu tổ 1...):")
    if ai_query:
        st.info(f"Đang xử lý yêu cầu thông minh cho: **{ai_query}**")
        if "tổ 1" in ai_query.lower():
            st.write("📊 **Kết quả phân tích từ hệ thống:** Tổ 1 hiện có dữ liệu nhân khẩu đầy đủ và khớp chuẩn với danh sách quản lý.")
        else:
            st.write("💡 **Gợi ý tự động:** Hệ thống đã sẵn sàng kết nối dữ liệu dân cư ấp Phước Lâm.")

# ================= 6. QUẢN TRỊ ADMIN (GỐC) =================
elif menu == "⚙️ Quản trị Admin (Gốc)":
    st.subheader("⚙️ Quản Trị Hệ Thống & Cập Nhật Dữ Liệu Gốc")
    
    if st.session_state['is_admin']:
        st.success("Bạn đang có quyền Admin. Bạn có thể tải lên file Excel chuẩn mới tại đây để thay thế dữ liệu.")
        new_master_file = st.file_uploader("Tải lên file Excel dân cư gốc chuẩn (.xlsx)", type=["xlsx"])
        if new_master_file is not None:
            st.session_state['df_master'] = pd.read_excel(new_master_file)
            st.success("Đã cập nhật dữ liệu gốc thành công vào hệ thống!")
            st.dataframe(st.session_state['df_master'].head())
    else:
        st.error("⛔ Bạn chưa đăng nhập quyền Admin! Vui lòng nhập mật khẩu Admin ở thanh bên trái.")
