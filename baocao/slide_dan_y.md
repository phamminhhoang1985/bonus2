# DÀN Ý SLIDE BÁO CÁO CUỐI KỲ (8 TRANG)
**Môn học:** DDM501 – AI trong sản xuất (DevOps, DataOps, MLOps)  
**Trường:** Đại học FPT (FPT University)  
**Đề tài:** Xây dựng hệ thống MLOps End-to-End: Phân loại chất lượng rượu vang, Giám sát Drift và Tự động Tái huấn luyện  

---

## SLIDE 1: TRANG TIÊU ĐỀ (TITLE SLIDE)
* **Tiêu đề chính:** BÁO CÁO CUỐI KỲ: HỆ THỐNG MLOPS END-TO-END
* **Tiêu đề phụ:** Phân loại chất lượng rượu vang với giám sát Data Drift và tự động tái huấn luyện mô hình
* **Môn học:** AI trong sản xuất: DevOps, DataOps, MLOps (Mã môn: DDM501)
* **Đơn vị:** Trường Đại học FPT (FPT University)
* **Giảng viên hướng dẫn:** Thầy Đông (dongnd)
* **Nhóm sinh viên thực hiện:**
  1. Phạm Minh Hoàng – MSSV: 25MS13285
  2. Nguyễn Công Trọng – MSSV: 25MS13297
  3. Ngô Minh Khôi – MSSV: 25MSA13236
* **Thời gian:** Tháng 10/2026

---

## SLIDE 2: ĐẶT VẤN ĐỀ & MỤC TIÊU DỰ ÁN
* **Bối cảnh & Thách thức:**
  * Hơn 80% mô hình ML không thể triển khai lên production hoặc bị suy giảm hiệu năng theo thời gian do "Hidden Technical Debt" và Data Drift.
  * Thiếu hụt quy trình tự động khép kín giữa Data Engineering, Huấn luyện, Triển khai và Giám sát.
* **Mục tiêu đề tài:**
  * Xây dựng kiến trúc MLOps microservices hoàn chỉnh dựa trên Docker.
  * Phục vụ dự đoán thời gian thực qua REST API với độ trễ thấp.
  * Thiết lập hệ thống theo dõi thí nghiệm và quản lý vòng đời mô hình (MLflow Model Registry).
  * Giám sát hệ thống (Prometheus/Grafana) và phát hiện biến động phân phối dữ liệu (Evidently AI).
  * Tự động hóa tái huấn luyện (Continuous Training) bằng Apache Airflow DAG khi xảy ra drift.
  * Đảm bảo chất lượng mã nguồn: Unit test đạt coverage $\ge 80\%$, CI/CD tự động.

---

## SLIDE 3: KIẾN TRÚC HỆ THỐNG TỔNG THỂ (SYSTEM ARCHITECTURE)
* **Mô hình kiến trúc Microservices (8 Docker Services):**
  * **API Serving:** FastAPI (Port 8000) – tiếp nhận request, dự đoán trực tiếp, xuất metrics.
  * **Model & Experiment Tracking:** MLflow Server (Port 5000) – lưu trữ metadata, artifact model.
  * **Workflow Orchestration:** Apache Airflow Webserver (8080) & Scheduler – điều phối pipeline 5 bước.
  * **Drift Monitoring:** Evidently AI (Port 8001) – phân tích thống kê so sánh reference vs current data.
  * **Observability:** Prometheus (Port 9090) – cào metrics, Grafana (Port 3000) – trực quan hóa dashboard.
  * **Database Backend:** PostgreSQL (Port 5432) – lưu trữ state cho Airflow và MLflow.
* **Sơ đồ luồng dữ liệu khép kín:**
  $$\text{User Request} \rightarrow \text{FastAPI} \xrightarrow{\text{Metrics}} \text{Prometheus} \rightarrow \text{Grafana}$$
  $$\text{Dữ liệu mới} \rightarrow \text{Evidently AI (Check Drift)} \xrightarrow{\text{Drift Trigger}} \text{Airflow DAG} \xrightarrow{\text{Retrain}} \text{MLflow Production}$$

---

## SLIDE 4: DỮ LIỆU & MÔ HÌNH HỌC MÁY (DATA & ML PIPELINE)
* **Bộ dữ liệu (Wine Quality Dataset):**
  * Nguồn: `sklearn.datasets.load_wine()` gồm 178 mẫu hóa nghiệm rượu vang vùng Piedmont, Ý.
  * Phân loại đa lớp (3 classes: Class 0, 1, 2) dựa trên 13 đặc trưng hóa học (Alcohol, Flavanoids, Color Intensity, Proline,...).
* **Mô hình học máy:**
  * Thuật toán: **Random Forest Classifier** (100 Decision Trees, `random_state=42`).
  * Lý do chọn: Ổn định, chống overfitting tốt, hỗ trợ trích xuất thuộc tính quan trọng (Feature Importance).
* **Cấu trúc Module Code (`src/`):**
  * `data_pipeline.py`: Ingestion, kiểm tra định dạng và chia tách train/test stratified (80/20).
  * `feature_engineering.py`: Chuẩn hóa dữ liệu bằng `StandardScaler`.
  * `train.py`: Huấn luyện mô hình, cross-validation 5-fold, log MLflow run.
  * `evaluate.py`: Tính toán bộ chỉ số Accuracy, Precision, Recall, F1-score, Confusion Matrix.
  * `explainability.py`: Giải thích mức độ quan trọng của đặc trưng (Feature Importances).

---

## SLIDE 5: GIÁM SÁT HỆ THỐNG & PHÁT HIỆN DATA DRIFT
* **Giám sát vận hành (Prometheus + Grafana):**
  * Bắt kịp thời gian thực: Requests per Second, Latency (P50, P95, P99), Error Rate (HTTP 4xx/5xx).
  * Phân phối dự đoán đầu ra của mô hình giữa 3 nhóm chất lượng rượu.
* **Cơ chế phát hiện Data Drift (Evidently AI):**
  * Đo lường sai khác phân phối dữ liệu thực nghiệm so với tập baseline ban đầu.
  * Ngưỡng kích hoạt cảnh báo: Tỷ lệ đặc trưng bị drift $\ge 30\%$.
* **Kịch bản mô phỏng kiểm thử Drift:**
  * **Giai đoạn 1 (Baseline):** Gửi 100 request bình thường $\rightarrow$ Trạng thái hệ thống an toàn.
  * **Giai đoạn 2 (Drift Simulation):** Gửi 250 request kèm nhiễu Gaussian ($\mu=0, \sigma=2.0$) $\rightarrow$ Evidently phát hiện drift vượt ngưỡng $\rightarrow$ Tự động gửi tín hiệu kích hoạt tái huấn luyện.

---

## SLIDE 6: ĐIỀU PHỐI TỰ ĐỘNG & CI/CD PIPELINE
* **Airflow DAG Tái huấn luyện (`ml_pipeline_dag` - 5 Tasks tuần tự):**
  1. `data_ingestion`: Nạp tập dữ liệu mới tích lũy.
  2. `data_cleaning`: Xử lý missing values, làm sạch nhiễu dữ liệu.
  3. `feature_engineering`: Chuẩn hóa scaling và fit transform tập đặc trưng.
  4. `model_training`: Huấn luyện lại Random Forest với dữ liệu cập nhật.
  5. `model_evaluation_and_registration`: Đánh giá ngưỡng chất lượng ($\text{Accuracy} \ge 85\%$) $\rightarrow$ Tự động promote lên **Production Stage** trên MLflow Model Registry.
* **Tự động hóa CI/CD (GitHub Actions):**
  * Tự động trigger khi có commit/PR vào nhánh `main` và `develop`.
  * Các bước: Lint code (flake8) $\rightarrow$ Chạy unit test & coverage report $\rightarrow$ Build Docker images.

---

## SLIDE 7: KẾT QUẢ THỰC NGHIỆM & ĐỐI CHIẾU TIÊU CHÍ
* **Chỉ số hiệu năng mô hình:**
  * Độ chính xác kiểm thử (Test Accuracy): **100%** (Precision: 1.0, Recall: 1.0, F1-Score: 1.0).
  * Kiểm định chéo (5-Fold Cross Validation): **97.9% $\pm$ 2.8%** (chứng minh tính tổng quát hóa cao, không overfit).
* **Chất lượng mã nguồn & Kiểm thử:**
  * **74/74 Test Cases PASSED** (Bao phủ API, Pipeline, Training, Evaluation, Explainability).
  * Code Coverage đạt **90%** (Vượt xa yêu cầu đề tài $\ge 80\%$).
* **Kiểm chứng Auto-Retraining:**
  * Kích hoạt thành công qua Airflow REST API khi có drift.
  * Cả 5 tasks trong DAG đều hoàn thành trạng thái **SUCCESS** trong $\approx 15$ giây.
  * Model Version mới tự động được promote lên Production không gây gián đoạn dịch vụ.

---

## SLIDE 8: KẾT LUẬN & HƯỚNG PHÁT TRIỂN TƯƠNG LAI
* **Tổng kết đề tài:**
  * Xây dựng thành công hệ thống MLOps khép kín (End-to-End) giải quyết bài toán Data Drift.
  * Đạt đầy đủ các chuẩn mực về kỹ thuật: CI/CD, Containerization, Orchestration, Observability và Test Coverage cao.
  * Giải quyết triệt để các bài toán thực tế: Xử lý tương thích phiên bản thư viện, tối ưu hóa lưu trữ artifact cục bộ.
* **Hướng phát triển tiếp theo:**
  * **Orchestration quy mô lớn:** Triển khai hạ tầng lên Kubernetes (K8s) với KServe / Seldon Core.
  * **Feature Store:** Tích hợp Feast để quản lý tập trung và chia sẻ features thời gian thực.
  * **Advanced Serving:** Áp dụng chiến lược A/B Testing hoặc Canary Deployment để so sánh model mới với model cũ trước khi chuyển đổi hoàn toàn.
* **Lời cảm ơn & Q&A:**
  * Lời cảm ơn Thầy giáo và Hội đồng đánh giá.
  * Sẵn sàng tiếp nhận câu hỏi thảo luận!
