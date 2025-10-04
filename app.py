import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ----------------------------------------
# 🧩 Load and preprocess dataset
# ----------------------------------------
try:
    df = pd.read_csv("Stocks_2025.csv")
except FileNotFoundError:
    st.error("❌ CSV file not found. Please check the file path: '../DataSets/Nifty/Stocks_2025.csv'")
    st.stop()

# Drop unwanted index column if present
if 'Unnamed: 0' in df.columns:
    df = df.drop('Unnamed: 0', axis=1)

# Ensure required columns exist
required_cols = {'Date', 'Close', 'Stock', 'Category'}
missing_cols = required_cols - set(df.columns)

if missing_cols:
    st.error(f"❌ Missing columns in dataset: {', '.join(missing_cols)}")
    st.stop()

# Safe Date parsing
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Date'])  # remove invalid dates

# Calculate SMAs
df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()

# ----------------------------------------
# 🧭 Streamlit UI
# ----------------------------------------
st.title("📈 Nifty Stock Analyzer")
st.markdown("Analyze **Nifty Stocks** interactively with 50-day and 200-day moving averages.")

# Sidebar filters
categories = sorted(df['Category'].dropna().unique())
selected_category = st.sidebar.selectbox("Select Category", categories)

filtered_df = df[df['Category'] == selected_category]

stocks = sorted(filtered_df['Stock'].dropna().unique())
selected_stock = st.sidebar.selectbox("Select Stock", stocks)

# Filter by stock
stock_df = filtered_df[filtered_df['Stock'] == selected_stock]

if stock_df.empty:
    st.warning("No data available for the selected stock.")
    st.stop()

# ----------------------------------------
# 📊 Plotly Chart
# ----------------------------------------
fig = go.Figure()

# Close price
fig.add_trace(go.Scatter(
    x=stock_df['Date'],
    y=stock_df['Close'],
    mode='lines+markers',
    name='Close Price',
    line=dict(color='green', width=2)
))

# SMA 50
fig.add_trace(go.Scatter(
    x=stock_df['Date'],
    y=stock_df['SMA_50'],
    mode='lines',
    name='SMA 50',
    line=dict(color='blue', dash='dot')
))

# SMA 200
fig.add_trace(go.Scatter(
    x=stock_df['Date'],
    y=stock_df['SMA_200'],
    mode='lines',
    name='SMA 200',
    line=dict(color='red', dash='dash')
))

# Layout
fig.update_layout(
    title=f"{selected_stock} Stock Trend ({selected_category})",
    xaxis_title="Date",
    yaxis_title="Price",
    hovermode="x unified",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

# Display chart
st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------
# 📋 Optional Data Table
# ----------------------------------------
with st.expander("🔍 View Raw Data"):
    st.dataframe(stock_df)

