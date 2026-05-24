# 📊 MarketPulse 360 — End-to-End Data Analytics Project

> **Data Analytics portfolio project** · Python · PostgreSQL · dbt Core · Power BI · Streamlit

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?logo=postgresql)](https://postgresql.org)
[![dbt](https://img.shields.io/badge/dbt-Core-FF694B?logo=dbt)](https://getdbt.com)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi)](https://powerbi.microsoft.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit)](https://streamlit.io)

---

## 🎯 Project Overview

**Context:** Olist is a Brazilian e-commerce marketplace connecting thousands of sellers 
to customers across Brazil. The dataset contains 100K+ real transactions from 2016–2018, 
including orders, products, sellers, customers, payments, and reviews.

**Goal:** Act as a Data Analyst embedded in Olist's business team — transform raw 
transactional data into actionable insights across the full analytics pipeline:
ingestion → modeling → transformation → analysis → visualization → web app.

**What the analysis delivered:**
- 📦 **Business overview** — 13.28M BRL revenue, 96K orders, growth trends by category
- 👥 **Customer segmentation** — 93K customers clustered into 5 RFM segments (Champions, Loyal, At Risk...)
- 🛡️ **Fraud & anomaly detection** — 23,765 suspicious transactions flagged (21.4% of orders)
- 📈 **4 business recommendations** with quantified impact — up to +BRL 150K/year recoverable

**Dataset:** [Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) 
· 96K orders · 13.28M BRL revenue · 2016–2018


---

## 🏗️ Architecture

```
Raw CSV Data
     ↓
PostgreSQL (8 tables ingested)
     ↓
Star Schema (fact_orders + 3 dimensions)
     ↓
dbt Core (5 models: staging + mart)
     ↓
Python Analysis (EDA + RFM + Anomaly Detection)
     ↓
Power BI Dashboard (5 pages)
     ↓
Streamlit App (5 interactive pages)
```

---

## 📁 Project Structure

```
MarketPulse360/
├── data/
│   └── processed/          # Exported CSVs from PostgreSQL
├── dbt_project/            # dbt models
│   ├── models/
│   │   ├── staging/        # stg_orders, stg_customers, stg_order_items
│   │   └── marts/          # mart_revenue, mart_customer_value
│   └── dbt_project.yml
├── notebooks/
│   ├── 01_eda_kpis.ipynb          # Exploratory Data Analysis
│   ├── 02_customer_segmentation.ipynb  # RFM + KMeans clustering
│   └── 03_pricing_anomaly.ipynb   # Anomaly detection (23,765 flagged)
├── sql/                    # Star schema DDL
├── streamlit_app/
│   └── app.py             # Interactive web application
├── powerbi/
│   └── MarketPulse360.pbix # Power BI dashboard
└── requirements.txt
```

---

## 🔑 Key Results

| KPI | Value |
|-----|-------|
| Total Revenue | **13.28M BRL** |
| Total Orders | **96K** |
| Avg Order Value | **BRL 137.65** |
| Avg Review Score | **4.08 / 5** |
| Freight Ratio | **16.64%** |
| Anomalies Detected | **23,765 (21.4%)** |

---

## 📊 Day-by-Day Build Log

| Day | Task | Status |
|-----|------|--------|
| 1 | Project setup + PostgreSQL ingestion (8 tables) | ✅ |
| 2 | Star schema design (fact_orders 110K rows + 3 dims) | ✅ |
| 3 | dbt Core — 5 models, PASS=5 ERROR=0 | ✅ |
| 4 | Python notebooks — EDA, RFM segmentation, anomaly detection | ✅ |
| 5 | Power BI dashboard — 5 pages, dark theme | ✅ |
| 6 | Streamlit app — 5 interactive pages | ✅ |
| 7 | GitHub + README + LinkedIn | ✅ |

---

## 🧩 Tech Stack

| Layer | Tool |
|-------|------|
| Language | Python 3.11 |
| Database | PostgreSQL 18 |
| Transformation | dbt Core |
| Analysis | pandas, scikit-learn, matplotlib |
| BI Dashboard | Power BI Desktop |
| Web App | Streamlit + Plotly |
| Version Control | Git / GitHub |

---

## 🚀 Run Locally

> ⚠️ **Prerequisites:** PostgreSQL installed + Olist dataset loaded

```bash
# 1. Clone the repo
git clone https://github.com/Mohamed-Aziz-BELKAHLA/MarketPulse360.git
cd MarketPulse360

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Load the dataset into PostgreSQL
# - Create a database named: marketpulse360
# - Run the SQL scripts in /sql/ folder
# - Or run: python load_data.py

# 5. Configure the DB connection in streamlit_app/app.py
# Change this line:
# engine = create_engine("postgresql://postgres:YOUR_PASSWORD@localhost:5432/marketpulse360")

# 6. Run the Streamlit app
cd streamlit_app
streamlit run app.py
```

---

## 📈 Business Recommendations

Based on the analysis, 4 strategic initiatives were identified:

| Initiative | Finding | Action | Impact |
|-----------|---------|--------|--------|
| 💰 Pricing | bed_bath_table: 19.7% freight ratio | Renegotiate logistics or +8% reprice | **+BRL 150K/year** |
| 👥 Retention | 73% one-time buyers, 13,436 at risk | 15% discount re-engagement campaign | 13,436 customers |
| 🛡️ Risk | 23,765 anomalous transactions (21.4%) | Automated payment reconciliation | Critical |
| 🚀 Growth | Champions: BRL 245 avg/order (3.4×) | VIP loyalty program | 15,115 customers |

---

## 👤 Author

**Mohamed Aziz BELKAHLA**
- 🎓 Étudiant en Data / IA — Paris School of Technology & Business
- 💼 [LinkedIn](https://linkedin.com/in/mohamed-aziz-belkahla)
- 🐙 [GitHub](https://github.com/Mohamed-Aziz-BELKAHLA)

---
