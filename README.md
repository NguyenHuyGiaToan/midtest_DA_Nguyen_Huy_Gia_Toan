# 🗺️ CS Agent Map: AI Agent Readiness Map for Computer Science Occupations

> **A Human–AI Collaboration Perspective Using the WORKBank Dataset**

---

## 📌 1. Đặt Vấn Đề (Introduction & Context)

Sự bùng nổ của AI Agent đang tái định hình sâu sắc cấu trúc công việc trong lĩnh vực Khoa học Máy tính (Computer Science - CS). Tuy nhiên, phần lớn các báo cáo hiện nay đều tiếp cận theo hướng nhị phân chung chung: _"AI sẽ thay thế lập trình viên?"_ hay _"Công việc nào dễ bị tự động hóa nhất?"_.

Dự án này chuyển dịch góc nhìn sang hướng tiếp cận thực tế và sâu sắc hơn: **Không hỏi AI có thay thế con người hay không, mà hỏi trong từng nhiệm vụ (task-level) cụ thể của ngành CS, AI nên tham gia ở mức độ nào và con người nên giữ vai trò kiểm soát gì?**

Dựa trên bộ dữ liệu nghiên cứu **WORKBank** (Stanford University), dự án xây dựng một **Bản đồ mức độ sẵn sàng ứng dụng AI Agent (AI Agent Readiness Map)** dành riêng cho nhóm ngành Khoa học Máy tính. Từ đó, định hình một mô hình cộng tác tối ưu giữa Người và Máy (Human-AI Collaboration), giúp giải phóng kỹ sư khỏi các tác vụ lặp lại để tập trung vào các công việc mang lại giá trị chiến lược cao hơn.

---

## 🎯 2. Mục Tiêu & Câu Hỏi Nghiên Cứu

### Mục tiêu tổng quát

Phân tích, đánh giá và trực quan hóa mức độ sẵn sàng triển khai AI Agent trong các tác vụ ngành CS; xác định ranh giới tối ưu giữa tự động hóa hoàn toàn và tăng cường năng lực con người.

### Câu hỏi nghiên cứu (Research Questions)

- **RQ1:** Những nhiệm vụ nào trong lĩnh vực CS có mức độ sẵn sàng ứng dụng AI Agent cao nhất (_Automate Now_)?
- **RQ2:** Những nhiệm vụ nào vẫn bắt buộc giữ mức độ kiểm soát của con người cao (_Human-Centric_)?
- **RQ3:** Có tồn tại khoảng cách nhận thức (Gap) giữa mong muốn của người lao động (Worker Desires) và đánh giá của chuyên gia công nghệ (Expert Ratings) không?
- **RQ4:** Các kỹ năng cốt lõi (OOP, DB, System Design...) sẽ dịch chuyển như thế nào trong kỷ nguyên AI Agent?

---

## 📊 3. Đối Tượng & Phương Pháp Phân Tích

### Phạm vi dữ liệu (Scope)

Dự án lọc và tập trung phân tích sâu vào **9 nghề nghiệp cốt lõi** thuộc lĩnh vực Khoa học Máy tính trong WORKBank Dataset:

- **Nhóm Phát triển (Dev):** Software Developers, Computer Programmers, Web Developers.
- **Nhóm Dữ liệu (Data):** Data Scientists, Database Administrators.
- **Nhóm Hệ thống & Bảo mật (System & Cyber):** Computer Systems Analysts, Information Security Analysts, Network Administrators.
- **Nhóm Quản lý (Management):** Information Technology Project Managers.

### Chỉ số độc quyền: CS Agent Fit Score

Để lượng hóa chính xác, dự án tự thiết lập một chỉ số tổng hợp **CS Agent Fit Score (0 - 100)** được tính toán theo công thức có trọng số:

$$Fit\_Score = \left( 0.4 \times Automation\_Desire + 0.4 \times Expert\_Capability \right) - \left( 0.2 \times Human\_Agency \right)$$

_Sau đó, điểm số được chuẩn hóa về thang điểm 0–100 và phân cụm thành 4 vùng chiến lược:_

- **80 - 100 | Automate Now:** Tác vụ lặp lại cao, xác minh rõ ràng $\rightarrow$ Giao hoàn toàn cho AI Agent.
- **60 - 79 | Strong AI Assistant:** AI đóng vai trò trợ lý chủ lực, sinh mã và cấu trúc hóa thông tin.
- **40 - 59 | Human-AI Partnership (Mức H3):** Điểm vàng cộng tác ngang hàng (Copilot), AI và người cùng làm.
- **0 - 39 | Human-Centric:** Tác vụ mơ hồ, cần giao tiếp, kiến trúc hoặc ra quyết định đạo đức $\rightarrow$ Giữ con người ở trung tâm.

---

## 🛠️ 4. Kiến Trúc Ứng Dụng (Streamlit Dashboard Layout)

Ứng dụng tương tác được xây dựng bằng **Streamlit** và **Plotly** bao gồm 8 phân hệ trực quan hóa câu chuyện dữ liệu (Data Storytelling):

1. **Home (Tổng quan):** Giới thiệu bối cảnh, phương pháp luận và công thức chỉ số riêng.
2. **Dataset Explorer:** Thống kê mô tả toàn bộ số lượng task, phân bổ ngành nghề và tổng quan phân cụm.
3. **AI Readiness Map (Chart 1 & 2):** Biểu đồ bong bóng (Scatter Plot) định vị task trên 2 trục _Expert Capability_ vs _Worker Desire_, kết hợp biểu đồ cột ngang top 15 tác vụ sẵn sàng nhất.
4. **Human Agency Analysis (Chart 3):** Biểu đồ cột chồng (Stacked Bar) thể hiện tỷ lệ phân bổ các mức kiểm soát từ H1 đến H5 theo từng occupation.
5. **Worker vs Expert Gap (Chart 4):** Biểu đồ phân kỳ (Diverging Bar) đo lường sự lệch pha nhận thức giữa năng lực công nghệ thực tế và mong muốn của kỹ sư.
6. **Future Skill Shift (Chart 5):** Bản đồ định vị nhóm kỹ năng (Skill Heatmap) để dự đoán xu hướng dịch chuyển giá trị của nguồn nhân lực.
7. **Recommendations:** Lộ trình triển khai AI chi tiết cho 4 nhóm tác vụ cốt lõi (Coding, Testing, Data, PM).
8. **About Project:** Ghi chú học thuật, giới hạn nghiên cứu và thông tin bản quyền.

---

## 💡 5. Tóm Tắt Insight Cốt Lõi (Key Findings)

- **Điểm vàng H3 (Equal Partnership):** Trong lĩnh vực CS, mức độ cộng tác ngang hàng (H3) là vùng phổ biến nhất. Kỹ sư không muốn bị thay thế hoàn toàn, họ muốn AI giải phóng họ khỏi áp lực ghi chép/kiểm tra để tập trung vào tư duy kiến trúc.
- **Sự dịch chuyển giá trị kỹ năng:** Các tác vụ có tính xác minh cao, lặp lại nhiều như _Viết tài liệu hệ thống (Documentation)_, _Sinh mã boilerplate (Coding)_, và _Kiểm thử tự động (QA/Testing)_ dịch chuyển mạnh về vùng tự động hóa. Ngược lại, năng lực phán đoán kiến trúc, thấu cảm yêu cầu khách hàng (Business Analysis) và đàm phán stakeholder ngày càng tăng giá trị.
- **Xung đột nhận thức (Gap):** Phát hiện các vùng có khoảng cách lớn giữa đánh giá của chuyên gia AI và mong muốn thực tế của lập trình viên, chỉ ra những điểm nghẽn về mặt tâm lý an toàn việc làm hoặc giới hạn thực tế của công cụ.

---

## ⚠️ 6. Hạn Chế & Lưu Ý Đạo Đức (Limitations & Ethical Note)

- **Tính phẳng của dữ liệu:** Dự án sử dụng giá trị trung bình (mean) để tổng hợp ý kiến đánh giá, điều này có thể làm mờ đi các góc nhìn thiểu số đặc biệt của một số chuyên gia hoặc worker.
- **Khía cạnh Đạo đức:** Việc đẩy mạnh _Automate Now_ ở một số khâu (như tự động duyệt log, phân quyền) cần được kiểm soát chặt chẽ bằng cơ chế kiểm toán công nghệ (Audit IT) để tránh các lỗ hổng thiên kiến hoặc lỗi bảo mật tự động hệ thống.

---

## 🚀 7. Hướng Dẫn Chạy Ứng Dụng (Installation & Run)

**Bước 1: Clone kho lưu trữ này về máy**

```bash
git clone [https://github.com/NguyenHuyGiaToan/midtest_DA_Nguyen_Huy_Gia_Toan.git]


**Bước 2: Cài đặt các thư viện cần thiết**
pip install streamlit pandas numpy plotly

**Bước 3: Khởi chạy ứng dụng Streamlit**
streamlit run Maindashboard.py
```
