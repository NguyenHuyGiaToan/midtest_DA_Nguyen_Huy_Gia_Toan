import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================================
# 1. CẤU HÌNH TRANG DASHBOARD (PHẢI LÀ LỆNH STREAMLIT ĐẦU TIÊN)
# =====================================================================
st.set_page_config(
    page_title="AI Agent in Computer Science - Analytics Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# 2. HÀM TẢI VÀ TIỀN XỬ LÝ DỮ LIỆU (ĐẢM BẢO KHÔNG LỖI ĐỊNH DẠNG)
# =====================================================================
@st.cache_data
def load_and_process_data():
    # Đọc dữ liệu gốc từ các file CSV của người dùng
    desires = pd.read_csv('Dataset/domain_worker_desires.csv')
    experts = pd.read_csv('Dataset/expert_rated_technological_capability.csv')
    metadata = pd.read_csv('Dataset/domain_worker_metadata.csv')
    
    # Định nghĩa bộ từ khóa nhận diện nhóm ngành IT/CS
    it_keywords = ['computer', 'software', 'developer', 'programmer', 'network', 'data', 'information', 'system', 'web']
    
    # --- XỬ LÝ BIỂU ĐỒ 1: TẦN SUẤT ỨNG DỤNG AI TRONG SDLC ---
    metadata_it = metadata[metadata['Occupation (O*NET-SOC Title)'].str.lower().fillna('').apply(
        lambda occ: any(kw in occ for kw in it_keywords)
    )].copy()
    
    usage_cols = {
        'LLM Usage by Type - Coding': 'Lập trình (Coding)',
        'LLM Usage by Type - System Design': 'Thiết kế hệ thống (System Design)',
        'LLM Usage by Type - Data Processing': 'Xử lý dữ liệu (Data Processing)'
    }
    
    freq_order = ['Daily', 'Weekly', 'Monthly', 'Never']
    freq_list = []
    
    for col, task_name in usage_cols.items():
        if col in metadata_it.columns:
            counts = metadata_it[col].value_counts().reindex(freq_order, fill_value=0)
            total = counts.sum()
            for freq in freq_order:
                percentage = round((counts[freq] / total) * 100, 1) if total > 0 else 0
                freq_list.append({
                    'Tác vụ (SDLC)': task_name,
                    'Tần suất': freq,
                    'Tỷ lệ (%)': percentage
                })
                
    df_freq = pd.DataFrame(freq_list)
    
    # --- XỬ LÝ BIỂU ĐỒ 2: MA TRẬN CHIẾN LƯỢC TỰ ĐỘNG HÓA (BPM) ---
    all_occupations = desires['Occupation (O*NET-SOC Title)'].dropna().unique()
    it_roles = [role for role in all_occupations if any(kw in role.lower() for kw in it_keywords)]
    
    desires_it = desires[desires['Occupation (O*NET-SOC Title)'].isin(it_roles)]
    experts_it = experts[experts['Occupation (O*NET-SOC Title)'].isin(it_roles)]
    
    # Tính điểm trung bình theo Task ID
    avg_desire = desires_it.groupby(['Task ID', 'Task'])['Automation Desire Rating'].mean().reset_index()
    avg_capacity = experts_it.groupby('Task ID')['Automation Capacity Rating'].mean().reset_index()
    
    df_matrix = pd.merge(avg_desire, avg_capacity, on='Task ID', how='inner')
    
    # Định nghĩa quy luật phân chia ma trận quyết định theo nghiệp vụ (BPM)
    def classify_quadrant(row):
        if row['Automation Capacity Rating'] >= 3.0 and row['Automation Desire Rating'] >= 3.0:
            return 'Quick Wins (Ưu tiên triển khai)'
        elif row['Automation Capacity Rating'] < 3.0 and row['Automation Desire Rating'] >= 3.0:
            return 'Điểm nghẽn (Mong muốn cao, AI chưa tới)'
        elif row['Automation Capacity Rating'] >= 3.0 and row['Automation Desire Rating'] < 3.0:
            return 'Rào cản vận hành (AI mạnh, KS chưa muốn)'
        else:
            return 'Human Core (Con người chủ đạo)'
            
    df_matrix['Phân loại chiến lược'] = df_matrix.apply(classify_quadrant, axis=1)
    
    return df_freq, df_matrix

# Thực thi tải dữ liệu
try:
    df_freq, df_matrix = load_and_process_data()
except Exception as e:
    st.error(f"Lỗi khi đọc hoặc xử lý file dữ liệu hệ thống: {e}")
    st.stop()

# =====================================================================
# 3. THIẾT KẾ SIDEBAR (THÔNG TIN SINH VIÊN & ĐỊNH HƯỚNG GIẢI PHÁP)
# =====================================================================
st.sidebar.title("🎯 Định hình Giải pháp")
st.sidebar.info(
    "Hệ thống Dashboard hỗ trợ Phân tích và Khuyến nghị ứng dụng **AI Agent** trong ngành Khoa học Máy tính."
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Sinh viên thực hiện:** Nguyễn Huy Gia Toàn")
st.sidebar.markdown("**Chuyên ngành:** Hệ thống thông tin Chuyển đổi số (DTIS/MIS)")

# Giao diện chính tiêu đề bảng điều khiển
st.title("🤖 Dashboard Phân Tích & Khuyến Nghị Ứng Dụng AI Agent Trong Khoa Học Máy Tính")
st.markdown("---")

# =====================================================================
# 4. PHẦN 1: TẦN SUẤT ỨNG DỤNG AI TRONG SDLC (100% STACKED BAR CHART)
# =====================================================================
st.header("1. Thực trạng Tần suất Ứng dụng AI trong Vòng đời SDLC")

col1, col2 = st.columns([7, 3])

with col1:
    if not df_freq.empty:
        # Sử dụng thuộc tính chuẩn hóa của Plotly Express cho biểu đồ cột chồng
        fig_freq = px.bar(
            df_freq, 
            x="Tỷ lệ (%)", 
            y="Tác vụ (SDLC)", 
            color="Tần suất",
            orientation='h',
            color_discrete_map={'Daily': '#1a5276', 'Weekly': '#2980b9', 'Monthly': '#7fb3d5', 'Never': '#e5e7e9'},
            category_orders={"Tần suất": ['Daily', 'Weekly', 'Monthly', 'Never']},
            text="Tỷ lệ (%)"
        )
        # Định cấu hình nhãn nằm trong thanh biểu đồ và cập nhật trục tọa độ chính xác
        fig_freq.update_traces(textposition='inside', texttemplate='%{text}%')
        fig_freq.update_layout(
            barmode='stack', 
            xaxis=dict(range=[0, 100], title_text="Tỷ lệ phần trăm phản hồi (%)"),
            yaxis=dict(title_text="Phân khúc tác vụ chuyên môn"),
            legend_title_text="Mức độ thường xuyên",
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_freq, use_container_width=True)
    else:
        st.warning("Không có dữ liệu tần suất để hiển thị.")

with col2:
    st.subheader("💡 Insight Nghiệp vụ (BA)")
    st.markdown("""
    * **Sự phân cực luồng việc:** Sự bứt phá của AI Agent tập trung áp đảo ở khâu **Lập trình** và **Xử lý dữ liệu** với tần suất sử dụng Daily/Weekly vượt trội.
    * **Ranh giới năng lực:** Ở mảng **Thiết kế hệ thống (System Design)**, tỷ lệ *Never* cao hơn hẳn rõ rệt, chứng minh AI hiện tại đóng vai trò là trợ lý thực thi kỹ thuật, chưa thể thay thế tư duy kiến trúc vĩ mô.
    """)

st.markdown("---")

# =====================================================================
# 5. PHẦN 2: MA TRẬN ƯU TIÊN VÀ TÁI THIẾT KẾ QUY TRÌNH (BPM SCATTER)
# =====================================================================
st.header("2. Ma trận Chiến lược & Ưu tiên Tự động hóa Quy trình")

# Bộ lọc tương tác đa lựa chọn từ người dùng
all_quadrants = [
    'Quick Wins (Ưu tiên triển khai)', 
    'Điểm nghẽn (Mong muốn cao, AI chưa tới)', 
    'Rào cản vận hành (AI mạnh, KS chưa muốn)', 
    'Human Core (Con người chủ đạo)'
]

selected_quadrants = st.multiselect(
    "Lọc theo Phân loại Chiến lược vận hành:",
    options=all_quadrants,
    default=all_quadrants
)

# Lọc dữ liệu theo phân loại người dùng đã chọn
filtered_matrix = df_matrix[df_matrix['Phân loại chiến lược'].isin(selected_quadrants)]

col3, col4 = st.columns([7, 3])

with col3:
    if not filtered_matrix.empty:
        fig_scatter = px.scatter(
            filtered_matrix,
            x='Automation Capacity Rating',
            y='Automation Desire Rating',
            color='Phân loại chiến lược',
            hover_name='Task',
            color_discrete_map={
                'Quick Wins (Ưu tiên triển khai)': '#2ea44f',
                'Điểm nghẽn (Mong muốn cao, AI chưa tới)': '#f0883e',
                'Rào cản vận hành (AI mạnh, KS chưa muốn)': '#8a63d2',
                'Human Core (Con người chủ đạo)': '#6a737d'
            },
            labels={
                'Automation Capacity Rating': 'Năng lực AI thực tế (Chuyên gia đánh giá)',
                'Automation Desire Rating': 'Mức độ mong muốn tự động hóa (Kỹ sư đánh giá)'
            }
        )
        
        # Thiết lập đường chỉ giới phân chia 4 vùng chiến lược tại điểm mốc trung bình 3.0
        fig_scatter.add_shape(type="line", x0=3.0, y0=1.0, x1=3.0, y1=5.0, line=dict(color="Red", width=1.5, dash="dash"))
        fig_scatter.add_shape(type="line", x0=1.0, y0=3.0, x1=5.0, y1=3.0, line=dict(color="Red", width=1.5, dash="dash"))
        
        # Cập nhật kích thước điểm trực quan và giới hạn chuẩn của trục từ 1 đến 5
        fig_scatter.update_traces(marker=dict(size=12, opacity=0.8, line=dict(width=0.5, color='Black')))
        fig_scatter.update_layout(
            xaxis=dict(range=[0.8, 5.2]),
            yaxis=dict(range=[0.8, 5.2]),
            legend_title_text="Phân nhóm ma trận quyết định",
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Vui lòng chọn ít nhất một nhóm chiến lược từ bộ lọc phía trên để hiển thị biểu đồ.")

with col4:
    st.subheader("📋 Bản đồ Tác vụ Nghiệp vụ")
    st.write(f"Đang hiển thị **{len(filtered_matrix)}** tác vụ nghiệp vụ.")
    
    # Hiển thị dữ liệu dạng bảng có cấu trúc sạch đẹp, dễ theo dõi
    st.dataframe(
        filtered_matrix[['Task', 'Phân loại chiến lược']],
        column_config={
            "Task": "Mô tả Chi tiết Tác vụ", 
            "Phân loại chiến lược": "Nhóm Vận hành"
        },
        hide_index=True,
        use_container_width=True
    )

st.markdown("---")

# =====================================================================
# 6. PHẦN 3: KHUYẾN NGHỊ TƯ VẤN GIẢI PHÁP CHIẾN LƯỢC TỔNG THỂ
# =====================================================================
st.header("3. Khung Khuyến nghị Tích hợp Hệ thống từ Chuyên gia MIS")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 🛠️ 1. Khuyến nghị Vận hành (Tactical)")
    st.success("""
    **Tích hợp sâu vào luồng CI/CD & Git:**
    
    Triển khai ngay các AI Agent tự trị vào khâu tác vụ thuộc nhóm **Quick Wins**. Tự động hóa việc quét lỗi cú pháp mã nguồn, chạy Unit Test tự động và rà soát các lỗ hổng bảo mật cơ bản (Audit IT) ngay khi kỹ sư thực hiện đẩy mã (Push/Pull Request).
    """)

with c2:
    st.markdown("### 🔄 2. Khuyến nghị Quy trình (BPM)")
    st.warning("""
    **Thiết lập quy trình Human-in-the-loop:**
    
    Đối với các tác vụ thuộc nhóm **Điểm nghẽn** hệ thống, tuyệt đối không cấu hình cho AI Agent tự ra quyết định. Quy trình nghiệp vụ mới (TO-BE) phải bắt buộc có bước phê duyệt từ các Chuyên gia Kiến trúc hoặc Quản lý Dự án để kiểm soát độ bất định.
    """)

with c3:
    st.markdown("### ⚖️ 3. Khuyến nghị Quản trị (Governance)")
    st.info("""
    **Khung Kiểm toán mã nguồn & AI định kỳ:**
    
    Xây dựng các chốt kiểm soát an toàn thông tin để đánh giá định kỳ các sản phẩm đầu ra do AI Agent xử lý, phòng ngừa rủi ro ảo tưởng (Hallucination) hoặc vi phạm bản quyền thư viện mã nguồn mở.
    """)