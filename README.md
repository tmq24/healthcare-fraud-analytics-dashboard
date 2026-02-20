# Healthcare Fraud Analytics Dashboard

## Description
A comprehensive Medicare Part D fraud and waste analysis project using AI to detect high-risk prescribers through clustering and anomaly detection techniques.

## Technologies Used
- **Python**: Data processing and AI models
- **Power BI**: Interactive visualization dashboard
- **Machine Learning**: 
  - K-Means Clustering
  - Isolation Forest

## Processing Pipeline
1. **Load & Aggregate**: Aggregate data from 3 years (2018-2020) by Prescriber NPI
2. **Feature Engineering**: Calculate 5 features reflecting prescribing behavior
3. **AI Models**: 
   - K-Means clustering (4 groups)
   - Isolation Forest (anomaly detection)
4. **Risk Scoring**: Calculate composite risk score

## Key Results
- **Total Prescribers**: 1,163,372
- **High Risk Count**: 4,498 (0.4%)
- **Red Zone Prescribers**: 3,712 (0.32%) - accounting for 4.36% of total cost

## Dashboard Overview

The `Final.pbix` file contains a comprehensive Power BI dashboard with 6 pages:

### 1. Executive Overview
- Total Cost (3 Years): $369,187,519,900
- Total Claims: 3,647,086,261
- Total Prescribers: 1,163,372
- Financial and geographical insights with state-level cost distribution

### 2. Executive Overview: Financial & Geographical Insights
- Geographic cost distribution map (choropleth)
- Spending & price trends over 2018-2020
- Special group spending analysis (Top 5 specialties)
- Cost root cause analysis (hierarchical breakdown)

### 3. Cost & Brand Waste: Efficiency Analysis
- Brand Cost: $304,578,362,798 (82.5%)
- Brand Prescribing Rate: 18%
- Top 30 high-cost drugs analysis (scatter plot)
- Brand vs. Generic cost comparison
- Detailed drug cost analysis by specialty

### 4. Public Health Risk Monitor: Opioid & Antibiotic Safety
- Antibiotic Use Rate: 2.48% (Max threshold: 30%)
- Opioid Risk Rate: 4.63% (Max threshold: 20%)
- Average Claims Per Patient: 4 (Max threshold: 40)
- Opioid risk intensity by state (choropleth map)
- Top high-risk prescribers (100% opioid rate)
- Opioid risk evolution by specialty (2018-2020)

### 5. Elderly Safety Monitor
- High Fall Risk Claims: 52.28M
- Elderly Risk Score: 2.1% (Goal: 0.10)
- Antipsychotic Claims (>65yo): 10.02M
- Total Elderly Beneficiaries: 966.23K
- Risky drug mix for elderly (donut chart)
- Risk prescription by specialty (stacked bar chart)
- Detailed prescriber-level risk analysis table

### 6. AI & Segmentation: Advanced Anomaly Detection
- High Risk Count: 4,498
- Anomalies Detected: 708
- Cluster distribution by risk (scatter plot)
  - X-axis: Average Cost per Claim ($) - Log scale
  - Y-axis: Anomaly Score - 0 to 100
  - 4 clusters: Low Cost/Low Risk, Moderate/Stable, Behavioral Anomaly, High Cost/High Risk
- Cluster characteristics (radar chart)
- Top risk anomalies table with detailed prescriber information

### 7. Provider Search & Profile: Digital Dossier
- Individual prescriber search and analysis
- Provider identity and credentials
- Cost efficiency audit (Provider vs. Peers)
- Opioid safety audit (Provider vs. Peers)
- Prescription intensity audit
- Top 10 costly drugs prescribed
- Risk portfolio mix (donut chart)

## License
This project is for educational and research purposes.
