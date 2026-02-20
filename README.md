# Healthcare Fraud Analytics Dashboard

## Mô tả
Dự án phân tích gian lận và lãng phí trong Medicare Part D sử dụng AI để phát hiện các prescriber có rủi ro cao thông qua clustering và anomaly detection.

## Công nghệ sử dụng
- **Python**: Xử lý dữ liệu và AI models
- **Power BI**: Visualization dashboard
- **Machine Learning**: 
  - K-Means Clustering (4 clusters)
  - Isolation Forest (Anomaly Detection)

## Cấu trúc dự án
```
NhomE/
├── code.py                    # Script chính: AI segmentation & anomaly detection
├── archive/                   # Dữ liệu gốc (parquet files)
├── figure/                    # Hình ảnh và icons cho dashboard
├── Measures_KPI.xlsx         # Định nghĩa các KPI measures
├── Data_Columns.xlsx         # Định nghĩa các cột dữ liệu
└── segmentation_results.csv  # Kết quả phân tích (không commit do kích thước lớn)
```

## Quy trình xử lý
1. **Load & Aggregate**: Tổng hợp dữ liệu từ 3 năm (2018-2020) theo Prescriber NPI
2. **Feature Engineering**: Tính 5 đặc trưng phản ánh hành vi kê đơn
3. **AI Models**: 
   - K-Means clustering (4 nhóm)
   - Isolation Forest (phát hiện anomalies)
4. **Risk Scoring**: Tính điểm rủi ro tổng hợp

## Kết quả
- **Total Prescribers**: 1,163,372
- **High Risk Count**: 4,498 (0.4%)
- **Red Zone Prescribers**: 3,712 (0.32%) - chiếm 4.36% tổng chi phí

## Yêu cầu
- Python 3.7+
- pandas, numpy, scikit-learn

## Chạy script
```bash
python code.py
```

## Dashboard
File `Final.pbix` chứa Power BI dashboard với 6 pages:
1. Overview
2. Geographic Analysis
3. Drug Analysis
4. Prescriber Analysis
5. AI & Segmentation (Page này)
6. Provider Profile
