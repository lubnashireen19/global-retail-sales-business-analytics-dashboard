import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Global Retail Sales Business Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# Load data
df = pd.read_csv("superstore.csv")

# Convert dates
df['Order.Date'] = pd.to_datetime(df['Order.Date'])

# Sidebar
st.sidebar.header("Dashboard Filters")


region = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=[]
)

category = st.sidebar.multiselect(
    "Category",
    options=df["Category"].unique(),
    default=[]
)

segment = st.sidebar.multiselect(
    "Segment",
    options=df['Segment'].unique(),
    default=[]
)

filtered_df = df.copy()

if region:
    filtered_df = filtered_df[filtered_df['Region'].isin(region)]

if category:
    filtered_df = filtered_df[filtered_df['Category'].isin(category)]

if segment:
    filtered_df = filtered_df[filtered_df['Segment'].isin(segment)]


# KPIs
total_revenue = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df['Order.ID'].nunique()
total_customers = filtered_df['Customer.Name'].nunique()

# Title
st.title("📊 Global Retail Sales Business Analytics Dashboard")
st.write("Interactive business analytics dashboard for retail sales performance, profitability, and customer insights.")

# KPI cards
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Orders", total_orders)
col4.metric("Customers", total_customers)

# Charts
st.subheader("Monthly Sales Trend")
monthly_sales = filtered_df.groupby(filtered_df['Order.Date'].dt.to_period('M'))['Sales'].sum().reset_index()
monthly_sales['Order.Date'] = monthly_sales['Order.Date'].astype(str)

fig1 = px.line(monthly_sales, x='Order.Date', y='Sales')
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Region-wise Revenue")
fig2 = px.bar(filtered_df, x='Region', y='Sales', color='Region')
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Category-wise Profit")
fig3 = px.bar(filtered_df, x='Category', y='Profit', color='Category')
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Customer Segment Analysis")
fig4 = px.pie(filtered_df, names='Segment', values='Sales')
st.plotly_chart(fig4, use_container_width=True)

st.subheader("Shipping Mode Analysis")
fig5 = px.bar(filtered_df, x='Ship.Mode', y='Sales', color='Ship.Mode')
st.plotly_chart(fig5, use_container_width=True)


st.subheader("Top 10 Products by Sales")

top_products = filtered_df.groupby("Product.Name")["Sales"].sum().sort_values(ascending=False).head(10)

fig7 = px.bar(
    top_products,
    x=top_products.values,
    y=top_products.index,
    orientation="h",
    title="Top 10 Products by Sales"
)

fig7.update_layout(yaxis={'categoryorder':'total ascending'})

st.plotly_chart(fig7, use_container_width=True)
st.subheader("Monthly Profit Trend")

monthly_profit = filtered_df.groupby(filtered_df["Order.Date"].dt.to_period("M"))["Profit"].sum().reset_index()
monthly_profit["Order.Date"] = monthly_profit["Order.Date"].astype(str)

fig8 = px.line(
    monthly_profit,
    x="Order.Date",
    y="Profit",
    title="Monthly Profit Trend",
    markers=True
)

st.plotly_chart(fig8, use_container_width=True)

st.subheader("Download Filtered Data")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    "filtered_sales_data.csv",
    "text/csv"
)
st.markdown("---")
st.caption("Built by Lubna Shireen RS | Business Analytics | Python | SQL | Streamlit | Plotly")