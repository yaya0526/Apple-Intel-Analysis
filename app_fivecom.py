import streamlit as st
import pandas as pd

# =========================
# 页面设置
# =========================
st.set_page_config(page_title="Financial Analysis Dashboard", layout="wide")

st.title("📊 Financial Analysis of Technology Firms")

st.markdown("""
This dashboard analyzes the financial performance of major technology companies.

**Metrics include:**
- Growth (Revenue)
- Profitability (Net Income)
- Efficiency (ROA)
- Earnings Quality (Profit Margin)
""")

# =========================
# 读取数据
# =========================
data = pd.read_csv("multi_company_data.csv")

# 标准化公司代码（避免大小写/空格问题导致筛选为空）
data['tic'] = data['tic'].astype(str).str.upper().str.strip()

# 转换日期并排序
data['datadate'] = pd.to_datetime(data['datadate'])
data = data.sort_values('datadate')

# 计算指标
data['roa'] = data['niq'] / data['atq']
data['profit_margin'] = (data['niq'] / data['revtq']).clip(-0.5, 0.5)

# =========================
# Sidebar（交互区）
# =========================
st.sidebar.header("🔧 Controls")

# 多选公司
companies = st.sidebar.multiselect(
    "Select up to 3 companies",
    options=sorted(data['tic'].unique()),
    default=["AAPL", "INTC"]
)

if len(companies) > 3:
    st.sidebar.warning("Please select up to 3 companies.")
    companies = companies[:3]

# 指标多选（支持多个指标）
metrics = st.sidebar.multiselect(
    "Select Metrics",
    ["Revenue", "Net Income", "ROA", "Profit Margin"],
    default=["Revenue", "ROA"]
)

metric_map = {
    "Revenue": "revtq",
    "Net Income": "niq",
    "ROA": "roa",
    "Profit Margin": "profit_margin"
}

# 限制指标数量
if len(metrics) > 3:
    st.sidebar.warning("Please select up to 3 metrics.")
    metrics = metrics[:3]

# 模式选择
mode = st.sidebar.radio(
    "Select Mode",
    ["Single Company", "Comparison"]
)

 # 筛选数据
filtered = data[data['tic'].isin(companies)]

# 如果筛选后没有数据，提示用户
if filtered.empty:
    st.error("No data found for selected companies. Please check your data or selection.")
    st.stop()

# =========================
# 主图表区域
# =========================

st.subheader("📈 Financial Trends")

# -------- 单公司模式 --------
if mode == "Single Company":
    if len(companies) != 1:
        st.warning("Please select exactly ONE company for this mode.")
    else:
        company = companies[0]
        single = data[data['tic'] == company]

        for metric in metrics:
            st.markdown(f"### {company} - {metric} Trend")
            chart = single.set_index('datadate')[metric_map[metric]]
            st.line_chart(chart)

# -------- 对比模式 --------
elif mode == "Comparison":
    for metric in metrics:
        chart_data = filtered.pivot(
            index='datadate',
            columns='tic',
            values=metric_map[metric]
        )

        # 删除全是NaN的公司（避免空图）
        chart_data = chart_data.dropna(axis=1, thresh=3)
        chart_data = chart_data.fillna(method='ffill')

        st.markdown(f"### {metric} Comparison Across Firms")

        # 如果没有有效数据，提示
        if chart_data.shape[1] == 0:
            st.warning("No valid data available for selected companies and this metric.")
        else:
            st.line_chart(chart_data)

# =========================
# Insight（自动分析）
# =========================

st.subheader("🧠 Insight")

for metric in metrics:
    selected = ", ".join(companies)

    if metric == "Revenue":
        st.markdown(f"""
        **Revenue Analysis ({selected})**

        The selected companies show different growth patterns over time.

        Firms with a stronger upward trend indicate higher growth potential, 
        while flatter trends suggest slower expansion.

        Differences in volatility also reflect varying business dynamics across firms.
        """)

    elif metric == "Net Income":
        st.markdown(f"""
        **Profitability Analysis ({selected})**

        Net income trends indicate how consistently each firm generates profit.

        More stable patterns suggest stronger operational control, 
        while fluctuations may indicate business instability.
        """)

    elif metric == "ROA":
        st.markdown(f"""
        **Efficiency Analysis ({selected})**

        ROA reflects how effectively firms utilize assets.

        Higher and stable ROA suggests efficient operations, 
        while declining or volatile ROA indicates weaker performance.
        """)

    elif metric == "Profit Margin":
        st.markdown(f"""
        **Earnings Quality Analysis ({selected})**

        Profit margin shows how much profit is generated from revenue.

        Firms with higher and stable margins demonstrate stronger pricing power 
        and better cost control.
        """)
# =========================
# Investment Ranking（自动评分）
# =========================

st.subheader("🏆 Investment Ranking")

# 获取最新数据
latest = filtered.sort_values('datadate').groupby('tic').tail(1)

# 初始化评分表
score_df = latest[['tic']].copy()

# 标准化评分（z-score）
for metric in metrics:
    col = metric_map[metric]
    score_df[metric] = (latest[col] - latest[col].mean()) / latest[col].std()

# 计算总分
score_df['Total Score'] = score_df[metrics].sum(axis=1)

# 排序
ranking = score_df.sort_values('Total Score', ascending=False)

# 显示排名
st.dataframe(ranking.set_index('tic'))

# 推荐策略
best_company = ranking.iloc[0]['tic']
worst_company = ranking.iloc[-1]['tic']

st.success(f"Recommended Long: {best_company}")
st.error(f"Recommended Short: {worst_company}")

st.caption("Ranking is based on standardized scores of selected metrics.")

# =========================
# Conclusion
# =========================

st.subheader("🏆 Conclusion")

st.markdown("""
Apple consistently demonstrates strong performance across all dimensions.

Microsoft and NVIDIA also show competitive strength, while AMD presents growth potential.

Intel shows weaker growth and declining efficiency, indicating structural challenges.

**Suggested Strategy:**
- Long Apple  
- Short Intel  

This dashboard provides a scalable framework for evaluating firm performance.
""")