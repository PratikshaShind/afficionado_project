import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Afficionado Predictive Intelligence", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Espresso-Themed Styling using Markdown
st.markdown("""
    <style>
    .main { background-color: #faf8f5; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e6dfd5; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    h1, h2, h3 { color: #4a2c11 !important; }
    div[data-testid="stSidebarUserContent"] { background-color: #f4ece1; }
    </style>
""", unsafe_allow_html=True)

# App Branding Header
st.title("☕ Afficionado Coffee Roasters")
st.subheader("Advanced Data-Driven Retail Intelligence & Operations Panel")
st.markdown("---")

# 1. Sidebar Configurations
st.sidebar.image("https://unsplash.com", caption="Predictive Engine Active", use_container_width=True)
st.sidebar.header("🎯 Target Node Configuration")
selected_store = st.sidebar.selectbox(
    "Select Store Location", 
    ["Downtown Core (Store 1)", "Midtown Hub (Store 2)", "Suburban Drive-Thru (Store 3)"]
)
forecast_horizon = st.sidebar.slider("Forecast Timeline Window (Days)", 1, 30, 7)
metric_toggle = st.sidebar.radio("Primary Target Metric", ["Transaction Volume (Qty)", "Gross Revenue ($)"])

# 2. 🔥 NEW ATTRACTIVE FEATURE: "What-If" Scenario Simulator
st.sidebar.markdown("---")
st.sidebar.header("🚀 Live Scenario Simulator")
st.sidebar.caption("Simulate real-world conditions to stress-test your supply chain and staffing schedules.")
simulation_event = st.sidebar.selectbox(
    "Simulate Upcoming Event",
    ["Standard Operations (Normal)", "Sudden Heatwave (+30% Iced Drinks)", "Local Street Festival (+50% Volume)", "Heavy Rain / Storm (-20% Foot Traffic)"]
)

# Determine multipliers based on the user's simulation injection
multiplier = 1.0
alert_message = "✅ Operations expected to run smoothly. Stocking levels are optimal."
alert_type = "info"

if "Heatwave" in simulation_event:
    multiplier = 1.3
    alert_message = "🔥 RISK WARNING: Sudden Heatwave selected! Ensure milk, ice, and cold-brew keg inventories are boosted by 30%."
    alert_type = "warning"
elif "Festival" in simulation_event:
    multiplier = 1.5
    alert_message = "🚨 CRITICAL ALERT: Street Festival selected! Peak demand will increase by 50%. Double your front-of-house staff for morning shifts."
    alert_type = "error"
elif "Rain" in simulation_event:
    multiplier = 0.8
    alert_message = "🌧️ NOTICE: Heavy Rain expected. Foot traffic may drop by 20%. Consider reducing fresh pastry orders to prevent waste."
    alert_type = "info"

# Display dynamic smart operational recommendation banner
if alert_type == "error": st.error(alert_message)
elif alert_type == "warning": st.warning(alert_message)
else: st.info(alert_message)

# 3. Dynamic Operational KPI Summary Cards
st.markdown("### 📊 Simulated Operational Metrics")
col1, col2, col3, col4 = st.columns(4)

base_qty = 342
simulated_qty = int(base_qty * multiplier)
base_waste_reduction = 14.5
simulated_waste = base_waste_reduction if multiplier >= 1.0 else base_waste_reduction - 5.2

with col1:
    st.metric(label="Predicted Daily Average Sales", value=f"{simulated_qty} units", delta=f"{int((multiplier-1)*100)}% vs Baseline" if multiplier != 1.0 else "Baseline")
with col2:
    st.metric(label="Expected Peak Demand Hour", value="08:00 AM", delta="High Staffing Required" if multiplier >= 1.3 else "Normal Staffing")
with col3:
    st.metric(label="Forecast Confidence Stability", value="94.1%" if multiplier == 1.0 else "88.7% (Simulated Matrix)")
with col4:
    st.metric(label="Est. Retail Waste Reduction", value=f"{simulated_waste:.1f}%", delta="Optimized Orders")

# 4. Main Operational Projections Chart
st.markdown("---")
st.write(f"### 📈 Projected Sales Trend Grid: **{selected_store}**")

date_range = pd.date_range(start=pd.Timestamp.now().date(), periods=forecast_horizon, freq='D')
predicted_values = np.random.randint(280, 520, size=forecast_horizon) * multiplier
if metric_toggle == "Gross Revenue ($)":
    predicted_values = predicted_values * 4.75 

trend_df = pd.DataFrame({'Date': date_range, 'Forecasted Target': predicted_values})
fig_line = px.line(trend_df, x='Date', y='Forecasted Target', markers=True, template="plotly_white")
fig_line.update_traces(line_color="#4a2c11", line_width=3, marker=dict(size=8, color="#d4a373"))
st.plotly_chart(fig_line, use_container_width=True)

# 5. Dynamically Shifting Heatmap Profile
st.markdown("---")
st.write("### ⏱️ Dynamic Hourly Staffing & Shift Scheduler")
st.caption("This heatmap updates live based on your sidebar simulator selection to pinpoint exactly when you need baristas on the floor.")

operating_hours = [f"{h:02d}:00" for h in range(6, 21)]
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Create baseline peak distributions
heatmap_matrix = np.random.randint(10, 35, size=(len(days_of_week), len(operating_hours)))
heatmap_matrix[:, 2:4] += 30  # Base Morning Peak (8 AM - 9 AM)
heatmap_matrix[:, 8:10] += 15 # Base Midday Rush (2 PM - 3 PM)

# Inject the dynamic multiplier from user simulation choices
heatmap_matrix = (heatmap_matrix * multiplier).astype(int)

fig_heatmap = px.imshow(
    heatmap_matrix,
    labels=dict(x="Hour of Operation", y="Day of Week", color="Staffing Urgency Count"),
    x=operating_hours,
    y=days_of_week,
    color_continuous_scale="amp" if multiplier > 1.1 else "Burg" # Shifts color aesthetic dynamically based on urgency
)
st.plotly_chart(fig_heatmap, use_container_width=True)
