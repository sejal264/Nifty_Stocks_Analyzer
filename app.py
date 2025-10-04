import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("Stocks_2025.csv")

# Clean and preprocess
if 'Unnamed: 0' in df.columns:
    df = df.drop('Unnamed: 0', axis=1)

df['Date'] = pd.to_datetime(df['Date'])
df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()

# App Title
st.title("📈 Nifty Stock Analyzer")
st.markdown("Select a **Category** and **Stock** to visualize price trends along with SMA 50 & SMA 200.")

# Sidebar filters
categories = sorted(df['Category'].dropna().unique())
selected_category = st.sidebar.selectbox("Select Category", categories)

filtered_df = df[df['Category'] == selected_category]

stocks = sorted(filtered_df['Stock'].dropna().unique())
selected_stock = st.sidebar.selectbox("Select Stock", stocks)

# Filter final dataset
stock_df = filtered_df[filtered_df['Stock'] == selected_stock]

# Display basic info
st.subheader(f"Stock: {selected_stock} ({selected_category})")
st.write(f"Total Records: {len(stock_df)}")

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

sb.lineplot(x=stock_df['Date'], y=stock_df['Close'], label='Close Price', color='green', marker='o', ax=ax)
sb.lineplot(x=stock_df['Date'], y=stock_df['SMA_50'], label='SMA 50', color='blue', ax=ax)
sb.lineplot(x=stock_df['Date'], y=stock_df['SMA_200'], label='SMA 200', color='red', ax=ax)

plt.xticks(rotation=45)
plt.xlabel("Date")
plt.ylabel("Price")
plt.title(f"{selected_stock} Stock Trend with SMA 50 & 200")
plt.legend()
plt.tight_layout()

# Display chart in Streamlit
st.pyplot(fig)

# Optional: Show data table
if st.checkbox("Show Data Table"):
    st.dataframe(stock_df)
