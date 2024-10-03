import streamlit as st
import pandas as pd
from babel.numbers import format_currency
import ssl
import urllib.request

# Bypass SSL verification
ssl._create_default_https_context = ssl._create_unverified_context

# Load dataset
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/uray03/Submission_analisis_data_python/main/.ipynb_checkpoints/Dashboard/all_data.csv'
    try:
        with urllib.request.urlopen(url) as response:
            return pd.read_csv(response)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

all_df = load_data()

if all_df.empty:
    st.error("Failed to load data. Please check your internet connection and try again.")
    st.stop()

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
st.line_chart(monthly_income.set_index('order_approved_at'))

# Most Sold Products
st.header("Produk yang Paling Sering Dibeli")
most_sold_products = main_df['product_id'].value_counts().head(10)
st.bar_chart(most_sold_products)

# Order Status Distribution
st.header("Distribusi Status Pesanan")
order_status_distribution = main_df['order_status'].value_counts()
st.bar_chart(order_status_distribution)

# Customer Distribution
st.header("Customer Distribution")
tab1, tab2 = st.tabs(["State", "Top 10 City"])

with tab1:
    state_distribution = main_df.groupby("customer_state")["customer_id"].nunique().sort_values(ascending=False)
    most_common_state = state_distribution.index[0]
    st.markdown(f"Most Common State: **{most_common_state}**")
    st.bar_chart(state_distribution)

with tab2:
    city_distribution = main_df.groupby("customer_city")["customer_id"].nunique().sort_values(ascending=False)
    top_10_cities = city_distribution.head(10)
    most_common_city = top_10_cities.index[0]
    st.markdown(f"Most Common City: **{most_common_city}**")
    st.bar_chart(top_10_cities)

# Footer
st.caption('Copyright (C) 2024')