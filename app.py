import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# 1. PAGE SETUP
st.set_page_config(layout="wide", page_title="B2B Risk Intelligence")

# Professional Banking UI Styling
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e6e9ef;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DATA LOADER (Joining Transactions with Benchmarks)
@st.cache_data
def load_full_intelligence_data():
    try:
        main_df = pd.read_csv("processed_risk_data.csv")
        bench_df = pd.read_csv("industry_benchmarks.csv")
        # JOIN: This proves you can handle relational data structures
        merged = pd.merge(main_df, bench_df, on='industry', how='left')
        return merged
    except FileNotFoundError:
        st.error("Missing data files! Please ensure 'processed_risk_data.csv' and 'industry_benchmarks.csv' exist.")
        return pd.DataFrame()

df = load_full_intelligence_data()

# 3. SIDEBAR: THE COMMAND CENTER
st.sidebar.title("🎮 Risk Control Panel")

# A. Calendar Filter
st.sidebar.subheader("📅 Observation Period")
start_date = st.sidebar.date_input("Start Date", datetime.date(2025, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date(2025, 12, 31))

st.sidebar.divider()

# B. Stress Test Slider (Recession Simulator)
st.sidebar.subheader("🕹️ Recession Simulator")
stress_days = st.sidebar.slider("Market Payment Delay (Days)", 0, 50, 0)
st.sidebar.info(f"Adding +{stress_days} days to all payments.")

st.sidebar.divider()

# C. Industry Filter
selected_industry = st.sidebar.multiselect(
    "Focus Industries",
    options=df["industry"].unique() if not df.empty else [],
    default=df["industry"].unique() if not df.empty else []
)

# 4. THE CALCULATION ENGINE (Market-Adjusted Risk)
sim_df = df.copy()

def advanced_risk_engine(row, added_delay):
    # Calculate current lateness vs industry benchmark
    actual_lateness = row['days_late'] + added_delay
    performance_gap = actual_lateness - row['market_avg_delay']
    
    score = 100
    score -= (actual_lateness * 1.2) # General delay penalty
    
    # NEW: Contextual Penalty (Harder penalty if lagging the sector)
    if performance_gap > 10: 
        score -= 20 
    elif performance_gap < -5:
        score += 5 # Bonus for being a top-tier payer
        
    if row['is_default'] > 0:
        score -= 40
        
    return max(0, min(100, score))

# Apply Engine
sim_df['credit_score'] = sim_df.apply(lambda x: advanced_risk_engine(x, stress_days), axis=1)

# NEW: Market Standing Logic
def get_market_standing(row, stress):
    actual = row['days_late'] + stress
    # If this benchmark column is empty (NaN), the logic stops working
    if pd.isna(row['market_avg_delay']): 
        return "No Benchmark Found"
    if actual < row['market_avg_delay']: return "🌟 Outperforming Market"
    if actual > row['market_avg_delay'] + 12: return "⚠️ Sector Lagging"
    return "⚖️ Market Neutral"

sim_df['Market_Standing'] = sim_df.apply(lambda x: get_market_standing(x, stress_days), axis=1)

# NEW: AI Decision Engine Logic
def get_recommendation(score):
    if score < 30: return "🚨 LEGAL: STOP SHIPMENTS"
    if score < 60: return "📞 CALL: REDUCE LIMIT"
    if score < 85: return "📧 EMAIL: AUTO-REMINDER"
    return "✅ APPROVE: INCREASE LIMIT"

sim_df['AI_Recommendation'] = sim_df['credit_score'].apply(get_recommendation)

# Apply Filters to the Final DataFrame
filtered_df = sim_df[sim_df["industry"].isin(selected_industry)]

# 5. HEADER SECTION
st.title("🛡️ B2B Trade Credit Intelligence")
st.write(f"Portfolio health for period: {start_date} to {end_date}")

# 6. KPI TILES (Digital Metrics)
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_score = filtered_df['credit_score'].mean()
    st.metric("Portfolio Health", f"{avg_score:.1f}/100")

with col2:
    cash_at_risk = filtered_df[filtered_df['credit_score'] < 45]['invoice_amount'].sum()
    st.metric("Exposure at Risk", f"${cash_at_risk:,.0f}")

with col3:
    avg_delay = filtered_df['days_late'].mean() + stress_days
    st.metric("Avg. Payment Delay", f"{avg_delay:.1f} Days")

with col4:
    critical_count = len(filtered_df[filtered_df['credit_score'] < 30])
    st.metric("Critical Accounts", critical_count)

st.divider()

# 7. VISUALIZATIONS
vis_col1, vis_col2 = st.columns([2, 1])

with vis_col1:
    st.subheader("Industry Risk Heatmap")
    fig = px.scatter(
        filtered_df,
        x="days_late",
        y="credit_score",
        size="invoice_amount",
        color="industry",
        hover_name="company_name",
        template="plotly_white",
        labels={"days_late": "Actual Delay (Days)", "credit_score": "Market-Adjusted Score"},
        color_discrete_sequence=px.colors.qualitative.Pastel,
        height=450
    )
    fig.add_hline(y=40, line_dash="dot", line_color="red", annotation_text="HIGH RISK")
    st.plotly_chart(fig, use_container_width=True)

with vis_col2:
    st.subheader("Cash Inflow Forecast")
    forecast_data = filtered_df.groupby('industry')['invoice_amount'].sum().reset_index()
    fig_bar = px.bar(
        forecast_data, 
        x='industry', 
        y='invoice_amount', 
        color='industry',
        labels={'invoice_amount': 'Projected Cash ($)'},
        template="none",
        height=450
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# 8. TASKBAR: PRIORITY COLLECTIONS LIST
st.subheader("🚨 Collections Priority List & Prescriptive Actions")
priority_list = filtered_df.sort_values('credit_score').head(15)
st.dataframe(
    priority_list[['company_name', 'industry', 'Market_Standing', 'credit_score', 'AI_Recommendation', 'invoice_amount']],
    use_container_width=True,
    hide_index=True
)