# 🛡️ B2B Trade Credit Risk & Collections Optimization Engine

An enterprise-grade Financial Intelligence platform designed for B2B (Business-to-Business) companies to manage supply chain trade credit, mitigate bad debt, and optimize outstanding Accounts Receivable (AR). 

Rather than standard descriptive tracking, this application couples an active **Prescriptive Decision Layer** with a dynamic **Recession Stress-Test Engine** to deliver predictive and actionable portfolio insights.

## 🚀 Live Application & Resources
* **Live Web App:** [Insert your Live Streamlit Cloud URL here]
* **Code Repository:** https://github.com/Simran-Padhi/b2b-trade-credit-risk-intelligence.git

## 🛠️ Tech Stack & Architecture
* **Core Language:** Python
* **Data Processing & Engineering:** Pandas (Multi-source relational joining, filtering, and structural merges)
* **Dynamic Visualizations:** Plotly Express (Multi-dimensional risk arrays & time-based distributions)
* **Frontend UI Framework:** Streamlit
* **UI/UX Wireframing:** Figma

## 💡 Key Architectural Features

### 1. Dynamic Recession Simulator (Sensitivity Analysis)
* Implements an interactive control slider that allows stakeholders to simulate systemic macroeconomic payment delays (0 to 50 days) across the customer portfolio.
* Features a reactive mathematical scoring engine that updates trust ratings and portfolio metrics instantly as payment intervals expand.

### 2. Contextual Sector Benchmarking (Data Integration)
* Executes a relational database join (`pd.merge`) to link internal company transaction histories with external macroeconomic industry standards (`industry_benchmarks.csv`).
* Effectively differentiates between widespread macroeconomic strain and isolated corporate failure by flagging **"Sector Laggards"**—companies whose individual delays drastically exceed their sector's baseline average.

### 3. Prescriptive Collection Engine
* Features an analytical decision-matrix layer that automatically translates real-time credit positions and market standings into discrete workflow tasks.
* Populates proactive automated alerts inside the operational tables:
  * `🚨 LEGAL: STOP SHIPMENTS` (Scores < 30)
  * `📞 CALL: REDUCE LIMIT` (Scores 30 - 59)
  * `📧 EMAIL: AUTO-REMINDER` (Scores 60 - 84)
  * `✅ APPROVE: INCREASE LIMIT` (Scores ≥ 85)

### 4. Cash Flow & Revenue Projection Chart
* Aggregates dynamic metrics across business sectors to output immediate cash allocation predictions. 
* Visualizes forward-looking portfolio performance to provide corporate treasurers with visible timeline estimates for invoice settlement.

## 📂 Project Structure
```text
├── app.py                  # Streamlit frontend dashboard layout & customized CSS styling
├── benchmark_engine.py     # Independent macro market intelligence data generator script
├── industry_benchmarks.csv # Macro market reference database file containing sector constraints
├── processed_risk_data.csv # Core ledger file containing synthetic B2B company trade histories
└── requirements.txt        # Production environment python software package dependencies
