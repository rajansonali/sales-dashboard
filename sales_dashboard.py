import pandas as pd
import streamlit as st
import plotly.express as px

# Page settings
st.set_page_config(page_title="Sales Analytics Dashboard", layout="wide")
st.title("📊 Professional Sales Data Analytics Dashboard")

# Load dataset
df =pd.read_csv("Sample - Superstore.csv", encoding="latin1")


# Data Cleaning
df.columns = df.columns.str.strip()  # Remove extra spaces
df["Order Date"] = pd.to_datetime(df["Order Date"])
# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
region = st.sidebar.multiselect("Select Region:", df["Region"].unique())
category = st.sidebar.multiselect("Select Category:", df["Category"].unique())

# Apply filters
filtered_df = df.copy()
if region:
    filtered_df = filtered_df[filtered_df["Region"].isin(region)]
if category:
    filtered_df = filtered_df[filtered_df["Category"].isin(category)]

# --- KPI Metrics ---
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)
profit_margin = (total_profit / total_sales) * 100 if total_sales else 0
avg_order_value = total_sales / total_orders if total_orders else 0

# KPI Layout
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Total Sales", f"${total_sales:,.2f}")
kpi2.metric("Total Profit", f"${total_profit:,.2f}")
kpi3.metric("Total Orders", total_orders)
kpi4.metric("Profit Margin", f"{profit_margin:.2f}%")
kpi5.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.markdown("---")

# --- Charts ---
# Sales by Region
fig_region = px.bar(filtered_df.groupby("Region")["Sales"].sum().reset_index(),
                    x="Region", y="Sales", title="Sales by Region",
                    color="Sales", color_continuous_scale="Blues")
# Sales by Category
fig_category = px.pie(filtered_df, names="Category", values="Sales", title="Sales by Category")

# Monthly Sales Trend
monthly_sales = filtered_df.groupby(filtered_df["Order Date"].dt.to_period("M"))["Sales"].sum().reset_index()
monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)
fig_trend = px.line(monthly_sales, x="Order Date", y="Sales", title="Monthly Sales Trend", markers=True)

# Top 10 Products by Sales
top_products = filtered_df.groupby("Product Name")["Sales"].sum().nlargest(10).reset_index()
fig_top_products = px.bar(top_products, x="Sales", y="Product Name", orientation='h',
                          title="Top 10 Products by Sales", color="Sales", color_continuous_scale="Viridis")

# Profit by Category & Region (Heatmap)
heatmap_data = filtered_df.groupby(["Category", "Region"])["Profit"].sum().reset_index()
fig_heatmap = px.density_heatmap(heatmap_data, x="Region", y="Category", z="Profit",
                                 color_continuous_scale="RdBu", title="Profit by Category & Region")

# Layout in 2 rows
col1, col2 = st.columns(2)
col1.plotly_chart(fig_region, use_container_width=True)
col2.plotly_chart(fig_category, use_container_width=True)

col3, col4 = st.columns(2)
col3.plotly_chart(fig_trend, use_container_width=True)
col4.plotly_chart(fig_top_products, use_container_width=True)

st.plotly_chart(fig_heatmap, use_container_width=True)

