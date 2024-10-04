import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency

# Set uniform style and color palette
sns.set(style='whitegrid')

# Load dataset
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/uray03/Submission_analisis_data_python/main/.ipynb_checkpoints/Dashboard/all_data.csv'
    return pd.read_csv(url)

all_df = load_data()

# Convert date columns to datetime
datetime_columns = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
for col in datetime_columns:
    all_df[col] = pd.to_datetime(all_df[col])

# Sidebar for date range selection
st.sidebar.title("Dicoding E-Commerce")
st.sidebar.image('https://raw.githubusercontent.com/miqbaljaffar/Submission-Analisis-Data/main/Dashboard/logo.png')

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()

start_date, end_date = st.sidebar.date_input(
    label="Date Range",
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Filter data based on date range
main_df = all_df[(all_df["order_approved_at"].dt.date >= start_date) & (all_df["order_approved_at"].dt.date <= end_date)]

# Dashboard title
st.title("Dashboard Analisis Data E-Commerce")

# E-commerce Income
st.header("E-commerce Income")
col1, col2 = st.columns(2)

with col1:
    total_spend = format_currency(main_df["payment_value"].sum(), "BRL", locale="pt_BR")
    st.markdown(f"Total Income: **{total_spend}**")

with col2:
    avg_spend = format_currency(main_df["payment_value"].mean(), "BRL", locale="pt_BR")
    st.markdown(f"Average Income: **{avg_spend}**")

# Monthly Income Chart
monthly_income = main_df.resample('M', on='order_approved_at')['payment_value'].sum().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(monthly_income['order_approved_at'], monthly_income['payment_value'], marker='o', linewidth=2, color="#FE0000")
ax.set_title("Monthly Total Income", fontsize=20, weight='bold')
ax.set_xlabel("Date", fontsize=14)
ax.set_ylabel("Total Income (BRL)", fontsize=14)
ax.tick_params(axis="x", rotation=45, labelsize=12)
ax.tick_params(axis="y", labelsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig)

# Most Sold Products
st.header("Produk yang Paling Sering Dibeli")
most_sold_products = main_df['product_id'].value_counts().head(10)
st.bar_chart(most_sold_products)

# Order Status Distribution
st.header("Distribusi Status Pesanan")
order_status_distribution = main_df['order_status'].value_counts()
st.bar_chart(order_status_distribution)

# Detailed Visualization of Order Status Distribution
st.subheader("Visualisasi Distribusi Status Pesanan")
fig, ax = plt.subplots(figsize=(12, 6))
order_status_distribution.plot(kind='bar', color=sns.color_palette('Set2'), ax=ax)
plt.title('Distribusi Status Pesanan', fontsize=18, weight='bold')
plt.xlabel('Status Pesanan', fontsize=14)
plt.ylabel('Jumlah Pesanan', fontsize=14)
plt.xticks(rotation=45, ha='right')
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)

# Add value labels on top of each bar
for i, v in enumerate(order_status_distribution):
    ax.text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=12)

plt.tight_layout()
st.pyplot(fig)

# Customer Distribution
st.header("Customer Distribution")
tab1, tab2 = st.tabs(["State", "Top 10 City"])

with tab1:
    state_distribution = main_df.groupby("customer_state")["customer_id"].nunique().sort_values(ascending=False)
    most_common_state = state_distribution.index[0]
    st.markdown(f"Most Common State: **{most_common_state}**")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=state_distribution.values, y=state_distribution.index, 
                palette=["#FF4500" if state == most_common_state else "#87CEFA" for state in state_distribution.index])
    ax.set_title("Customer Distribution by State", fontsize=18, weight='bold')
    ax.set_xlabel("Number of Customers", fontsize=14)
    ax.set_ylabel("State", fontsize=14)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    
    for i, v in enumerate(state_distribution.values):
        ax.text(v + 1, i, str(v), va='center', fontsize=12)
    
    plt.tight_layout()
    st.pyplot(fig)

with tab2:
    city_distribution = main_df.groupby("customer_city")["customer_id"].nunique().sort_values(ascending=False)
    top_10_cities = city_distribution.head(10)
    most_common_city = top_10_cities.index[0]
    st.markdown(f"Most Common City: **{most_common_city}**")
    
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.barplot(x=top_10_cities.values, y=top_10_cities.index, palette="coolwarm")
    ax.set_title("Top 10 Cities by Customer Count", fontsize=18, weight='bold')
    ax.set_xlabel("Number of Customers", fontsize=14)
    ax.set_ylabel("City", fontsize=14)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=12)
    
    for i, v in enumerate(top_10_cities.values):
        ax.text(v + 1, i, str(v), va='center', fontsize=12)
    
    plt.tight_layout()
    st.pyplot(fig)

# Footer
st.caption('Copyright (C) UrayHafizh 2024')