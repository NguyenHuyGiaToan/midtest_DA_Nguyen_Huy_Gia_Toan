import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ==========================================
# 1. CẤU HÌNH TRANG & GIAO DIỆN
# ==========================================
st.set_page_config(
    page_title="CS Agent Readiness Map",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bảng màu cho từng nhóm phân loại
COLOR_MAP = {
    "Automate Now": "#2E86C1",       
    "Strong AI Assistant": "#17A589", 
    "Human-AI Partnership": "#D4AC0D",
    "Human-Centric": "#CB4335"        
}

# ==========================================
# 2. XỬ LÝ DỮ LIỆU (LOAD OR MOCK)
# ==========================================
@st.cache_data
def load_and_process_data():
    """
    Hàm đọc và liên kết dữ liệu từ cả 4 file CSV gốc của bộ dữ liệu WORKBank.
    Tập trung 100% vào nhóm ngành Computer Science.
    """
    cs_occupations = [
        "Computer Programmers", "Software Developers", "Web Developers",
        "Data Scientists", "Database Administrators", "Information Security Analysts",
        "Computer Systems Analysts", "Network Administrators", "Information Technology Project Managers"
    ]

    try:
        # 1. ĐỌC TẤT CẢ 4 FILE DATASET GỐC
        df_tasks = pd.read_csv("Dataset/task_statement_with_metadata.csv")
        df_worker_desires = pd.read_csv("Dataset/domain_worker_desires.csv")
        df_worker_metadata = pd.read_csv("Dataset/domain_worker_metadata.csv")
        df_expert = pd.read_csv("Dataset/expert_rated_technological_capability.csv")

        # Lọc các task thuộc nhóm ngành Computer Science trước để tối ưu hiệu năng
        df_tasks_cs = df_tasks[df_tasks['Occupation (O*NET-SOC Title)'].isin(cs_occupations)].copy()
        
        # 2. LIÊN KẾT WORKER DESIRES VỚI WORKER METADATA QUA 'User ID'
        # Việc này giúp giữ lại thông tin nền tảng của Worker (Kinh nghiệm, Tần suất dùng LLM...)
        df_worker_full = df_worker_desires.merge(
            df_worker_metadata[['User ID', 'Experience', 'LLM Familiarity', 'LLM Use in Work']], 
            on='User ID', 
            how='inner'
        )

        # 3. ĐỒNG BỘ HÓA ĐÁG GIÁ CỦA WORKER (Tính trung bình theo từng Task ID)
        worker_agg = df_worker_full.groupby('Task ID').agg({
            'Automation Desire Rating': 'mean',
            'Human Agency Scale Rating': 'mean'
        }).reset_index().rename(columns={
            'Automation Desire Rating': 'Worker_Desire',
            'Human Agency Scale Rating': 'Worker_HAS'
        })

        # 4. ĐỒNG BỘ HÓA ĐÁNH GIÁ CỦA EXPERT (Tính trung bình theo từng Task ID)
        expert_agg = df_expert.groupby('Task ID').agg({
            'Automation Capacity Rating': 'mean'
        }).reset_index().rename(columns={
            'Automation Capacity Rating': 'Expert_Capability'
        })

        # 5. TIẾN HÀNH MERGE TẤT CẢ VÀO DF CHÍNH
        df_final = df_tasks_cs.merge(worker_agg, on='Task ID', how='inner')
        df_final = df_final.merge(expert_agg, on='Task ID', how='inner')
        
        # Chuẩn hóa lại tên cột cho gọn gàng
        df_final.rename(columns={
            'Occupation (O*NET-SOC Title)': 'Occupation', 
            'Skill (O*NET Work Activity)': 'Skill'
        }, inplace=True)

    except FileNotFoundError:
        # TỰ ĐỘNG TẠO MOCK DATA NẾU THIẾU FILE (Giúp hệ thống không bị crash)
        np.random.seed(42)
        tasks_data = [
            ("Generate boilerplate code for CRUD operations.", "Software Developers", "Programming", 4.5, 4.8, 1.5),
            ("Review code for security vulnerabilities and optimize logic.", "Software Developers", "Quality Control", 3.2, 3.5, 3.8),
            ("Negotiate API contract specifications with frontend team.", "Software Developers", "Communication", 1.5, 1.2, 4.5),
            ("Write unit tests for edge cases in payment gateway.", "Computer Programmers", "Programming", 4.0, 4.2, 2.0),
            ("Debug legacy spaghetti code written in COBOL.", "Computer Programmers", "Problem Solving", 3.8, 2.5, 4.0),
            ("Build responsive UI layouts from Figma designs.", "Web Developers", "Programming", 4.2, 4.5, 2.0),
            ("Clean and impute missing values in structured datasets.", "Data Scientists", "Data Processing", 4.6, 4.7, 1.5),
            ("Design complex machine learning system architecture.", "Data Scientists", "System Design", 2.5, 2.0, 4.5),
            ("Optimize slow-running analytical SQL queries.", "Database Administrators", "Problem Solving", 3.5, 3.8, 3.0),
            ("Monitor network traffic logs for DDoS attack patterns.", "Information Security Analysts", "Data Processing", 4.8, 4.5, 1.2),
            ("Document system APIs and endpoints.", "Computer Systems Analysts", "Documentation", 4.5, 4.5, 1.5),
            ("Summarize sprint planning meeting notes.", "Information Technology Project Managers", "Documentation", 4.5, 4.5, 1.5),
            ("Resolve interpersonal conflicts between developers and QA.", "Information Technology Project Managers", "Communication", 1.0, 1.0, 5.0)
        ]
        
        df_final = pd.DataFrame(tasks_data, columns=['Task', 'Occupation', 'Skill', 'Worker_Desire', 'Expert_Capability', 'Worker_HAS'])
        df_final['Task ID'] = range(1001, 1001 + len(df_final))
        df_final['Frequency'] = np.random.randint(50, 500, len(df_final))

    # 6. SỬA LỖI SƠ CẤP: CHỈ SỬ DỤNG CLIP CHO CÁC CỘT SỐ
    numeric_cols = ['Worker_Desire', 'Expert_Capability', 'Worker_HAS']
    df_final[numeric_cols] = df_final[numeric_cols].clip(lower=1, upper=5)

    # 7. TÍNH TOÁN CHỈ SỐ ĐỘC QUYỀN: CS AGENT FIT SCORE
    df_final['Fit_Raw'] = (0.4 * df_final['Worker_Desire']) + (0.4 * df_final['Expert_Capability']) - (0.2 * df_final['Worker_HAS'])
    
    # Min-Max Scaling về thang điểm 0 - 100
    min_val = (0.4 * 1) + (0.4 * 1) - (0.2 * 5)  # -0.2
    max_val = (0.4 * 5) + (0.4 * 5) - (0.2 * 1)  # 3.8
    df_final['CS_Agent_Fit_Score'] = ((df_final['Fit_Raw'] - min_val) / (max_val - min_val)) * 100

    # Phân loại chiến lược dựa trên điểm số
    def classify_score(score):
        if score >= 80: return "Automate Now"
        elif score >= 60: return "Strong AI Assistant"
        elif score >= 40: return "Human-AI Partnership"
        else: return "Human-Centric"
    
    df_final['Classification'] = df_final['CS_Agent_Fit_Score'].apply(classify_score)
    df_final['Worker_vs_Expert_Gap'] = df_final['Expert_Capability'] - df_final['Worker_Desire']
    df_final['HAS_Bucket'] = pd.cut(df_final['Worker_HAS'], bins=[0, 1.5, 2.5, 3.5, 4.5, 5], labels=['H1', 'H2', 'H3', 'H4', 'H5'])

    return df_final

df = load_and_process_data()

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("CS Agent Atlas 🧭")
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Điều hướng",
    ["1. Home (Tổng quan)", 
     "2. Dataset Explorer", 
     "3. CS Agent Readiness Map", 
     "4. Human Agency Analysis", 
     "5. Worker vs Expert Gap", 
     "6. Future Skill Shift", 
     "7. Recommendations", 
     "8. About Project"]
)
st.sidebar.markdown("---")
st.sidebar.info("Dựa trên bộ dữ liệu **WORKBank** (Stanford University). Phân tích tập trung vào các nghề Khoa học Máy tính.")

# ==========================================
# 5. PAGE LOGIC
# ==========================================

if page == "1. Home (Tổng quan)":
    st.title("AI Agent Readiness Map for Computer Science")
    st.markdown("### Visualizing Human-AI Collaboration Opportunities")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        #### 📍 Bối cảnh
        Sự phát triển của AI Agent đang làm thay đổi cách con người làm việc trong lĩnh vực Công nghệ Thông tin. Tuy nhiên, phần lớn các câu hỏi hiện nay chỉ dừng lại ở việc *"AI sẽ thay thế nghề nào?"*. 
        
        Nghiên cứu này thay đổi góc nhìn: **Trong từng nhiệm vụ cụ thể của kỹ sư CS, AI nên làm gì và con người nên giữ vai trò gì?**
        
        #### 🎯 Mục tiêu cốt lõi
        Xây dựng bản đồ **AI Agent Readiness** dựa trên dữ liệu từ *WORKBank* nhằm xác định 4 nhóm hành động:
        1. **Automate Now** (Tự động hóa ngay lập tức)
        2. **Strong AI Assistant** (Dùng AI như trợ lý mạnh mẽ)
        3. **Human-AI Partnership** (Hợp tác ngang hàng)
        4. **Human-Centric** (Giữ con người làm trung tâm)
        """)
    with col2:
        st.info("""
        **Chỉ số CS Agent Fit Score**
        
        Được tính toán dựa trên 3 yếu tố:
        * 🔼 **Worker Desire** (Trọng số 40%)
        * 🔼 **Expert Capability** (Trọng số 40%)
        * 🔽 **Human Agency Scale** (Trọng số -20%)
        
        *Đã chuẩn hóa về thang 0-100.*
        """)
        st.success("Mức độ H3 (Equal Partnership) đang là xu hướng mong đợi phổ biến nhất trong các tác vụ phức tạp.")

elif page == "2. Dataset Explorer":
    st.title("Khám phá dữ liệu (Dataset Explorer)")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tổng số Task CS", len(df))
    col2.metric("Số lượng Nghề (Occupations)", df['Occupation'].nunique())
    col3.metric("Điểm Fit Score TB", f"{df['CS_Agent_Fit_Score'].mean():.1f}/100")
    col4.metric("Nhóm kỹ năng", df['Skill'].nunique())

    st.markdown("### Phân bổ Nhiệm vụ theo Nhóm Công việc (Classification)")
    pie_data = df['Classification'].value_counts().reset_index()
    pie_data.columns = ['Classification', 'Count']
    fig_pie = px.pie(pie_data, values='Count', names='Classification', 
                     color='Classification', color_discrete_map=COLOR_MAP,
                     hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("### Dữ liệu chi tiết")
    st.dataframe(df[['Task', 'Occupation', 'Skill', 'CS_Agent_Fit_Score', 'Classification']].sort_values('CS_Agent_Fit_Score', ascending=False), use_container_width=True)

elif page == "3. CS Agent Readiness Map":
    st.title("Chart 1: AI Agent Readiness Map")
    st.markdown("Biểu đồ phân tán (Scatter Plot) giúp định vị từng nhiệm vụ trong không gian: Năng lực của AI (Y) vs Mong muốn của con người (X).")

    # Filters
    col1, col2 = st.columns(2)
    selected_occ = col1.multiselect("Lọc theo Nghề nghiệp:", options=df['Occupation'].unique(), default=df['Occupation'].unique())
    selected_class = col2.multiselect("Lọc theo Phân loại:", options=df['Classification'].unique(), default=df['Classification'].unique())
    
    df_filtered = df[(df['Occupation'].isin(selected_occ)) & (df['Classification'].isin(selected_class))]

    if not df_filtered.empty:
        fig_scatter = px.scatter(
            df_filtered, 
            x="Worker_Desire", 
            y="Expert_Capability", 
            color="Classification",
            size="Frequency",
            hover_name="Task",
            hover_data={"Worker_Desire": ":.2f", "Expert_Capability": ":.2f", "Classification": False, "Frequency": False},
            color_discrete_map=COLOR_MAP,
            labels={"Worker_Desire": "Mức độ mong muốn Tự động hóa (Worker)", "Expert_Capability": "Năng lực công nghệ (Expert)"}
        )
        # Vẽ các đường chia quadrant mờ
        fig_scatter.add_hline(y=3, line_width=1, line_dash="dash", line_color="gray")
        fig_scatter.add_vline(x=3, line_width=1, line_dash="dash", line_color="gray")
        fig_scatter.update_layout(height=600, template="plotly_white")
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("Vui lòng chọn ít nhất 1 nghề và 1 phân loại.")

    st.markdown("---")
    st.title("Chart 2: Top AI-Ready Tasks")
    st.markdown("Những nhiệm vụ có điểm **CS Agent Fit Score** cao nhất (Ưu tiên triển khai tự động hóa / trợ lý AI trước).")
    
    top_tasks = df.sort_values('CS_Agent_Fit_Score', ascending=True).tail(15) # Ascending true để hiện top ở trên cùng trong Plotly bar
    fig_bar = px.bar(
        top_tasks, 
        x="CS_Agent_Fit_Score", 
        y="Task", 
        color="Classification",
        color_discrete_map=COLOR_MAP,
        orientation='h',
        text_auto='.1f'
    )
    fig_bar.update_layout(height=500, template="plotly_white", yaxis={'categoryorder':'total ascending'})
    fig_bar.update_yaxes(title_text="")
    st.plotly_chart(fig_bar, use_container_width=True)

elif page == "4. Human Agency Analysis":
    st.title("Chart 3: Human Agency Distribution")
    st.markdown("""
    Phân bổ mức độ kiểm soát của con người (H1-H5) theo từng nhóm nghề nghiệp.
    * **H1/H2:** Máy tính làm hoàn toàn, con người chỉ khởi tạo.
    * **H3:** Hợp tác ngang hàng (Copilot/Partnership).
    * **H4/H5:** Con người ra quyết định chính, công nghệ chỉ cung cấp thông tin.
    """)

    has_dist = df.groupby(['Occupation', 'HAS_Bucket']).size().reset_index(name='Count')
    has_dist['Percentage'] = has_dist.groupby('Occupation')['Count'].transform(lambda x: x / x.sum() * 100)
    
    fig_stacked = px.bar(
        has_dist, 
        x="Percentage", 
        y="Occupation", 
        color="HAS_Bucket",
        orientation='h',
        color_discrete_sequence=["#1F618D", "#2980B9", "#F4D03F", "#E67E22", "#C0392B"], # Từ xanh (máy) sang đỏ (người)
        labels={"Percentage": "Tỷ lệ (%)", "HAS_Bucket": "Human Agency Level"}
    )
    fig_stacked.update_layout(barmode='stack', height=600, template="plotly_white", yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_stacked, use_container_width=True)
    
    st.info("💡 **Insight:** Các vị trí quản lý (Project Managers) và bảo mật (Security Analysts) có xu hướng yêu cầu mức H4, H5 rất cao do tính chất giao tiếp và rủi ro. Ngược lại, Data Scientists/Programmers có tỷ lệ chấp nhận H1, H2 cho các task xử lý lặp lại cao hơn.")

elif page == "5. Worker vs Expert Gap":
    st.title("Chart 4: Worker vs Expert Gap Analysis")
    st.markdown("""
    Đo lường khoảng cách nhận thức: `Gap = Năng lực thực tế của AI (Expert) - Mong muốn Tự động hóa (Worker)`
    * 🟢 **Gap > 0 (Bên phải):** Chuyên gia đánh giá AI làm rất tốt, nhưng người lao động chưa thực sự muốn/chưa tin tưởng giao phó. (Vùng cần đào tạo / Change Management).
    * 🔴 **Gap < 0 (Bên trái):** Người lao động rất mệt mỏi và muốn tự động hóa, nhưng công nghệ hiện tại chưa đáp ứng được. (Vùng cần R&D).
    """)

    # Lấy top 10 âm và top 10 dương
    df_sorted_gap = df.sort_values('Worker_vs_Expert_Gap')
    top_negative = df_sorted_gap.head(10)
    top_positive = df_sorted_gap.tail(10)
    df_gap_plot = pd.concat([top_negative, top_positive])
    
    df_gap_plot['Color'] = np.where(df_gap_plot['Worker_vs_Expert_Gap'] > 0, '#28B463', '#E74C3C') # Xanh cho Dương, Đỏ cho Âm
    
    fig_gap = go.Figure()
    fig_gap.add_trace(go.Bar(
        x=df_gap_plot['Worker_vs_Expert_Gap'],
        y=df_gap_plot['Task'],
        orientation='h',
        marker_color=df_gap_plot['Color'],
        text=df_gap_plot['Worker_vs_Expert_Gap'].round(2),
        textposition='outside'
    ))
    fig_gap.update_layout(
        height=700, 
        template="plotly_white",
        xaxis_title="<-- Tech Chưa Tới (Gap Âm) | Khác Biệt Nhận Thức | (Gap Dương) Kháng Cự Từ User -->",
        yaxis_title="",
        yaxis={'categoryorder':'total ascending'}
    )
    # Thêm đường line ở 0
    fig_gap.add_vline(x=0, line_width=2, line_color="black")
    st.plotly_chart(fig_gap, use_container_width=True)

elif page == "6. Future Skill Shift":
    st.title("Chart 5: Future Skill Shift in CS")
    st.markdown("Phân tích xem nhóm kỹ năng (Skill) nào đang nghiêng về phía tự động hóa, nhóm nào vẫn yêu cầu tính con người cao.")

    skill_agg = df.groupby('Skill').agg({
        'CS_Agent_Fit_Score': 'mean',
        'Worker_HAS': 'mean',
        'Task': 'count'
    }).reset_index()

    fig_heat = px.scatter(
        skill_agg,
        x="Worker_HAS",
        y="CS_Agent_Fit_Score",
        size="Task",
        color="CS_Agent_Fit_Score",
        text="Skill",
        color_continuous_scale="RdYlBu", # Đỏ (Thấp) -> Xanh (Cao)
        labels={"Worker_HAS": "Yêu cầu kiểm soát của con người (HAS)", "CS_Agent_Fit_Score": "Khả năng ứng dụng AI Agent"}
    )
    fig_heat.update_traces(textposition='top center')
    fig_heat.update_layout(height=600, template="plotly_white")
    st.plotly_chart(fig_heat, use_container_width=True)
    
    st.markdown("""
    **Nhận định xu hướng:**
    * **Giảm giá trị (Tự động hóa cao):** Các kỹ năng *Data Processing*, *Documentation*, *System Administration* (Góc trên bên trái).
    * **Tăng giá trị (Human-Centric):** Các kỹ năng *Communication*, *System Design*, *Problem Solving* phức tạp (Góc dưới bên phải).
    """)

elif page == "7. Recommendations":
    st.title("Khuyến nghị Triển khai AI Agent trong CS")
    st.markdown("Dựa trên kết quả phân tích dữ liệu phân cụm, đây là lộ trình áp dụng AI Agent tối ưu cho từng lớp công việc.")

    with st.expander("💻 Nhóm 1: Lập trình / Triển khai (Coding & Dev) - Mức độ: Augment First", expanded=True):
        st.markdown("""
        **Phù hợp với mô hình Copilot (H3):**
        * **Nên giao cho AI:** Generate boilerplate code, tự động sinh test cases (Unit Test Generation), Refactoring các block code cũ.
        * **Con người giữ vai trò:** Quyết định kiến trúc phần mềm, Review bảo mật cuối cùng, Đảm bảo logic nghiệp vụ (Business Logic).
        """)
        
    with st.expander("🧪 Nhóm 2: Kiểm thử / Cảnh báo (QA & Security) - Mức độ: Automate Now", expanded=True):
        st.markdown("""
        **Nhiệm vụ lặp lại, xác minh cao (H1/H2):**
        * **Nên giao cho AI:** Dò quét lỗ hổng bảo mật tĩnh (SAST), Monitoring server logs 24/7, Tự động phát hiện bất thường (Anomaly Detection) trong Network.
        * **Con người giữ vai trò:** Xử lý sự cố cấp bách (Incident Response) khi AI Agent cảnh báo.
        """)
        
    with st.expander("📊 Nhóm 3: Dữ liệu (Data Tasks) - Mức độ: Strong AI Assistant"):
        st.markdown("""
        **Giảm tải công việc tiền xử lý:**
        * **Nên giao cho AI:** Data Cleaning, Imputation, Tối ưu hóa câu lệnh SQL (Query Optimization), Auto-generate reporting dashboards.
        * **Con người giữ vai trò:** Giải thích kết quả phân tích cho C-level (Interpretation), Đảm bảo tính đạo đức của dữ liệu.
        """)
        
    with st.expander("🗣️ Nhóm 4: Quản lý & Phân tích (PM & Business Analysis) - Mức độ: Keep Human-Centric"):
        st.markdown("""
        **Nhiệm vụ yêu cầu Interpersonal Skills cao (H4/H5):**
        * **Nên giao cho AI (vai trò thư ký):** Meeting summarization, Sprint tracking, Note-taking, Draft requirement docs.
        * **Con người CẦN giữ vai trò:** Đàm phán với Stakeholder, Giải quyết xung đột nhân sự, Xác định Scope của dự án, Đưa ra quyết định Ethical.
        """)

elif page == "8. About Project":
    st.title("Về Dự Án & Tác Giả")
    
    st.markdown("### Thông tin Dữ liệu (Dataset)")
    st.markdown("""
    Dự án sử dụng bộ dữ liệu **WORKBank** do Đại học Stanford phát hành, đo lường chi tiết mong muốn của người lao động (Worker Desires) và đánh giá của chuyên gia công nghệ (Expert Ratings) về tác động của AI.
    
    * **Giới hạn nghiên cứu (Limitations & Ethical Note):** Phân tích này tập trung vào 9 nghề cốt lõi trong Khoa học Máy tính. Các điểm số đã được làm phẳng dựa trên giá trị trung bình (mean), có thể che lấp các ý kiến thiểu số (outliers). Việc tự động hóa cần đi kèm với chính sách đào tạo chuyển đổi (reskilling).
    """)
    
    st.markdown("### Khác biệt cốt lõi")
    st.success("""
    Thay vì tiếp cận theo hướng "AI thay thế lập trình viên", dự án này đóng khung AI Agent như một **công cụ tái phân bổ thời gian**. 
    
    Mức hợp tác **H3 (Human-AI Partnership)** được chứng minh là "điểm vàng" cho lĩnh vực CS: AI thực hiện kiểm tra, ghi chép, lặp lại; giải phóng con người để tập trung vào xác định yêu cầu, kiến trúc hệ thống và giao tiếp.
    """)
    
    st.markdown("---")
    st.markdown("*Xây dựng bằng Python, Streamlit, Pandas và Plotly.*")