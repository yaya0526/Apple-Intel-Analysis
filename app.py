import streamlit as st
import pandas as pd

st.title("Apple vs Intel Financial Analysis Dashboard")

# Load data
data = pd.read_csv("AAPL_INTC_quarterly.csv")
data['datadate'] = pd.to_datetime(data['datadate'])

# Split data
apple = data[data['tic'] == 'AAPL'].sort_values('datadate')
intel = data[data['tic'] == 'INTC'].sort_values('datadate')

# User selection
company = st.selectbox("Select Company", ["AAPL", "INTC"])
filtered = data[data['tic'] == company].sort_values('datadate')

# ---- Single Company Analysis ----
st.header(f"{company} Analysis")

st.subheader("Revenue Trend")
st.line_chart(filtered.set_index('datadate')['revtq'])

st.subheader("Net Income Trend")
st.line_chart(filtered.set_index('datadate')['niq'])

# Metrics
st.subheader("Key Metrics")
st.metric("Latest Revenue", f"{filtered['revtq'].iloc[-1]:,.0f}")
st.metric("Latest Net Income", f"{filtered['niq'].iloc[-1]:,.0f}")

# ---- Comparison Section ----
st.header("Company Comparison")

# Fix: align by quarter instead of exact date
data['quarter'] = data['datadate'].dt.to_period('Q')

comparison = data.pivot(index='quarter', columns='tic', values='revtq')

comparison = comparison.rename(columns={
    'AAPL': 'Apple',
    'INTC': 'Intel'
})

st.subheader("Revenue Comparison(Quarterly)")
st.line_chart(comparison)

# Growth rate (fixed alignment)
growth = comparison.pct_change()

st.subheader("Revenue Growth Rate（Quarterly)")
st.line_chart(growth)

comparison_ma = comparison.rolling(window=4).mean()

st.subheader("Revenue Comparison (Smoothed)")
st.line_chart(comparison_ma)
# ---- Investment Insight ----
st.header("Investment Insight")

if company == "AAPL":
    st.success("Apple is a strong long candidate due to stable growth and strong profitability.")
else:
    st.warning("Intel may be a short candidate due to declining performance and weaker financial trends.")

st.markdown("""
### Overall Conclusion

Apple demonstrates consistent revenue growth and strong profitability, making it a suitable long position.

Intel shows declining profitability and weaker financial performance, suggesting a potential short position.
""")