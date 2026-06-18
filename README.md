# 🤖 Phân Tích & Khuyến Nghị Ứng Dụng AI Agent Trong Ngành Khoa Học Máy Tính

## 📌 Tổng Quan Dự Án (Project Overview)

Dự án này được xây dựng trong khuôn khổ bài kiểm tra môn **Trực quan hóa dữ liệu (Data Visualization)**. Mục tiêu cốt lõi là chuyển đổi các tập dữ liệu khảo sát phức tạp về hành vi của người lao động và đánh giá của chuyên gia công nghệ thành một Dashboard tương tác trực quan trên nền tảng **Streamlit**.

Thông qua lăng kính của một Chuyên gia phân tích hệ thống, dự án phân tích sâu thực trạng ứng dụng AI trong Vòng đời phát triển phần mềm (SDLC), từ đó thiết lập **Ma trận chiến lược** nhằm khuyến nghị mô hình tái thiết kế quy trình nghiệp vụ (BPM) và kiểm soát rủi ro an toàn thông tin (Audit IT).

- **Sinh viên thực hiện:** Nguyễn Huy Gia Toàn
- **Chuyên ngành:** Hệ thống thông tin Chuyển đổi số (DTIS/MIS)
- **Công cụ phát triển:** Python, Streamlit, Pandas, Plotly Express

---

## 🗺️ Lộ Trình Triển Khai Bài Làm (Execution Roadmap)

[Bước 1: Tích hợp & Làm sạch dữ liệu (ETL)]
│
▼
[Bước 2: Mô hình hóa Trực quan bằng Streamlit & Plotly]
│
▼
[Bước 3: Trích xuất Insight Nghiệp vụ (BA/BPM)]
│
▼
[Bước 4: Thiết lập Khung Khuyến nghị Kiến trúc]

1. **Bước 1 (Data ETL):** Sử dụng `Pandas` lọc và chuẩn hóa dữ liệu từ các tập tin gốc, cô lập nhóm ngành Khoa học máy tính & IT. Thực hiện phép gộp quan hệ (Inner Join) dựa trên khóa `Task ID` để kết hợp mong muốn tự động hóa với năng lực thực tế của AI.
2. **Bước 2 (Data Visualization):** Phát triển giao diện Web Dashboard bằng `Streamlit`. Sử dụng `Plotly Express` dựng biểu đồ cột chồng 100% (100% Stacked Bar Chart) và biểu đồ phân tán (Scatter Plot) tương tác cao cấp.
3. **Bước 3 (Business Analytics):** Đọc hiểu dữ liệu trực quan để định vị các điểm nghẽn vận hành và phân nhóm tác vụ nghiệp vụ.
4. **Bước 4 (Solution Consulting):** Đóng gói báo cáo thành các giải pháp kiến trúc: Vận hành (Tactical), Quy trình (BPM Workflow), và Quản trị (Governance).

---

## 📊 Cấu Trúc Luồng Phân Tích & Insights Dữ Liệu

### 1. Tần suất Ứng dụng AI trong Vòng đời SDLC

- **Trực quan hóa:** Biểu đồ cột chồng 100% (100% Stacked Bar Chart).
- **Trục dữ liệu:** Trục Y phân loại các phân khúc tác vụ chuyên môn (_Lập trình, Xử lý dữ liệu, Thiết kế hệ thống_); Trục X biểu diễn tỷ lệ % tần suất phản hồi (_Daily, Weekly, Monthly, Never_).
- **Insight cốt lõi:** Dữ liệu cho thấy sự phân cực rất lớn. AI Agent đã cắm rễ sâu vào tác vụ thực thi kỹ thuật hàng ngày như **Lập trình (Coding)** và **Xử lý dữ liệu (Data Processing)**. Tuy nhiên, ở mảng tư duy kiến trúc vĩ mô như **Thiết kế hệ thống (System Design)**, tỷ lệ "Never" chiếm ưu thế, thiết lập ranh giới hiện tại của năng lực AI.

### 2. Ma trận Chiến lược Tự động hóa Quy trình (BPM Matrix)

- **Trực quan hóa:** Biểu đồ phân tán (Scatter Plot) chia 4 góc phần tư tại điểm mốc trung bình 3.0.
- **Trục dữ liệu:** Trục X (Năng lực AI thực tế theo chuyên gia); Trục Y (Mức độ mong muốn tự động hóa của kỹ sư).
- **Phân nhóm quyết định:**
  - **Quick Wins (Trên - Phải):** Năng lực AI cao + Kỹ sư muốn làm. Tập trung vào: Viết mã lặp lại, Kiểm thử tự động (QA/QC), Quét lỗi bảo mật định sẵn. -> _Khuyến nghị: Tự động hóa hoàn toàn._
  - **Điểm nghẽn (Trên - Trái):** Kỹ sư áp lực và muốn giao việc, nhưng AI chưa đủ năng lực (ví dụ: Quản lý dự án phức tạp). -> _Khuyến nghị: Cải tiến quy trình tổ chức, không ép dùng AI._
  - **Human Core (Dưới - Trái):** Con người làm chủ đạo do độ bất định (`Involved Uncertainty`) cao (ví dụ: Đánh giá đạo đức thuật toán, Phê duyệt kiến trúc lõi). -> _Khuyến nghị: Giữ nguyên nhân sự._

---

## 🎯 Khung Khuyến Nghị Chiến Lược Từ Chuyên Gia MIS

Dựa trên dữ liệu đã phân tích, mô hình chuyển đổi số được đề xuất theo 3 tầng chiến lược:

1. **Khuyến nghị Vận hành (Tactical):** Tích hợp trực tiếp các Agent tự động hóa nhóm tác vụ _Quick Wins_ vào luồng CI/CD và hệ thống quản lý mã nguồn mở (Git/GitHub) nhằm cắt bỏ thời gian chờ thủ công trong chu trình SDLC.
2. **Khuyến nghị Quy trình (BPM):** Thiết lập cơ chế **Human-in-the-loop (Con người kiểm soát ở giữa)** bắt buộc cho các quy trình thuộc vùng _Điểm nghẽn_ và _Human Core_. AI Agent chỉ đóng vai trò trợ lý tổng hợp thông tin, quyền duyệt cuối cùng thuộc về nhân sự cấp cao.
3. **Khuyến nghị Quản trị (Governance):** Xây dựng Khung kiểm toán IT định kỳ đối với sản phẩm đầu ra của AI Agent nhằm kiểm soát rủi ro ảo tưởng dữ liệu (Hallucination) và bảo mật an ninh hệ thống lõi.

---

## 💻 Hướng Dẫn Chạy Ứng Dụng (Installation & Run)

### Yêu cầu hệ thống

Đảm bảo máy tính của bạn đã cài đặt Python (phiên bản >= 3.8) và các file dữ liệu sau nằm chung thư mục dự án:

- `domain_worker_desires.csv`
- `expert_rated_technological_capability.csv`
- `domain_worker_metadata.csv`

### Các bước khởi chạy

1. Cài đặt các thư viện phụ thuộc bắt buộc:
   pip install streamlit pandas plotly openpyxl

2. Khởi chạy Dashboard trên môi trường Local:
   streamlit run app.py

3. Hệ thống sẽ kích hoạt giao diện Web tương tác tại địa chỉ mặc định: http://localhost:8501.
