import streamlit as st 
import pandas as pd 
from analytics import ECommerceAnalytics

st.set_page_config(page_title="E-Commerce Sales Analytics",page_icon="📊",layout="wide")

st.title("📊 E-Commerce Sales Analytics Dashboard")
st.markdown("An interactive dashboard for analyzing e-commerce sales data using Python, SQLite, and Pandas.")\

analytics=ECommerceAnalytics()
col1, col2 = st.columns(2)
with col1:
  st.subheader("🔥 Top 5 Best-Selling Products")
  top_products = analytics.get_top_selling_products(limit=5)
  st.dataframe(top_products,use_container_width=true)
  st.bar_chart(top_products.set_index("Description")["TotalQuantity"])

with col2:
    st.subheader("💰 Top 5 Spenders")
    top_spenders = analytics.get_top_spenders(limit=5)
    st.dataframe(top_spenders, use_container_width=True)

st.subheader("🌍 Top Countries by Revenue")
top_countries = analytics.get_top_countries_by_revenue(limit=5)
st.dataframe(top_countries, use_container_width=True)
st.bar_chart(top_countries.set_index("Country")["TotalSpent"])

st.subheader("📈 Monthly Revenue Trend")
monthly_rev = analytics.get_monthly_revenue()
st.line_chart(monthly_rev.set_index("Month")["TotalRevenue"])


