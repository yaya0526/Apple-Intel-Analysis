# 📊 Financial Analysis Dashboard (Streamlit)

## 📌 Project Overview
This project develops an **interactive financial analysis dashboard** using Streamlit to evaluate the performance of major technology firms.

The dashboard allows users to dynamically explore financial data across multiple companies and metrics, supporting data-driven investment insights.

---

## 🎯 Objectives
- Analyze firm performance using financial data from WRDS (Compustat Quarterly)
- Compare companies across multiple dimensions:
  - Growth (Revenue)
  - Profitability (Net Income)
  - Efficiency (ROA)
  - Earnings Quality (Profit Margin)
- Build an interactive tool for financial visualization and decision-making

---

## 🗂 Data Source
- **WRDS Compustat Quarterly (fundq)**
- Sample period: 2015–Present
- Firms included:
  - Apple (AAPL)
  - Intel (INTC)
  - Microsoft (MSFT)
  - NVIDIA (NVDA)
  - AMD (AMD)

---

## ⚙️ Features

### 🔹 Interactive Controls
- Select up to **3 companies**
- Select up to **3 financial metrics**
- Toggle between:
  - Single Company Analysis
  - Multi-company Comparison

---

### 🔹 Financial Metrics
- Revenue (Growth)
- Net Income (Profitability)
- Return on Assets (ROA)
- Profit Margin

---

### 🔹 Visualization
- Time-series line charts
- Multi-company comparison
- Dynamic updates based on user selection

---

### 🔹 Investment Ranking (Core Feature)
The dashboard includes a **multi-factor ranking system**:

- Uses the **latest available data**
- Applies **z-score standardization**:

  z = (x - mean) / std

- Computes a **Total Score**:

  Total Score = sum of standardized metrics

- Outputs:
  - Company ranking
  - Recommended **Long position**
  - Recommended **Short position**

---

## 🧠 Insights
The tool highlights:
- Strong performers (e.g., Apple, Microsoft)
- High-growth firms (e.g., NVIDIA)
- Weak or declining firms (e.g., Intel)

Insights are dynamically generated based on selected companies and metrics.

---

## ⚠️ Data Limitations
- Some firms (e.g., NVIDIA) may have **missing data for certain metrics**
- Forward-filling is applied for visualization purposes
- Rankings assume **equal weights across metrics**
- Results depend on selected metrics and companies

---

## 🚀 How to Run

### 1. Install dependencies
```bash
pip install streamlit pandas
