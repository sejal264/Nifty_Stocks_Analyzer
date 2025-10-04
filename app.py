import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

# --- Load Data ---
df = pd.read_csv("Stocks_2025.csv")
df = df.drop('Unnamed: 0', axis=1)

# --- Ensure 'Date' column is parsed correctly ---
df["Date"] = pd.to_datetime(df["Date"], errors='coerce')  # Fix invalid date formats

# --- Drop rows where Date could not be parsed ---
df = df.dropna(subset=["Date"])

# --- Clean & calculate moving averages ---
df["SMA50"] = df["Close"].rolling(window=50, min_periods=1).mean()
df["SMA200"] = df["Close"].rolling(window=200, min_periods=1).mean()
df["Stock"] = df["Stock"].replace(" ", " ", regex=True)

# --- Streamlit UI ---
st.title("📈 Nifty Stocks Analysis Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("Filter Options")
categories = df["Category"].dropna().unique()
selected_category = st.sidebar.selectbox("Select Category", sorted(categories))

filtered_df = df[df["Category"] == selected_category]
stocks = filtered_df["Stock"].dropna().unique()
selected_stock = st.sidebar.selectbox("Select Stock", sorted(stocks))

# --- Filter Data ---
stock_data = filtered_df[filtered_df["Stock"] == selected_stock]

# --- Display Selected Info ---
st.write(f"### Showing data for *{selected_stock}* ({selected_category})")

# --- Plot ---
fig, ax = plt.subplots(figsize=(12, 6))
sb.lineplot(x=stock_data["Date"], y=stock_data["Close"], label="Close", color='g', marker='D', ax=ax)
sb.lineplot(x=stock_data["Date"], y=stock_data["SMA50"], label="SMA 50", color='orange', ax=ax)
sb.lineplot(x=stock_data["Date"], y=stock_data["SMA200"], label="SMA 200", color='red', ax=ax)

plt.xticks(rotation=45)
plt.title(f"{selected_stock} - Close Price with SMA50 & SMA200")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
st.pyplot(fig)

# --- Optional Data Table ---
with st.expander("🔍 View Raw Data"):
    st.dataframe(stock_data)
