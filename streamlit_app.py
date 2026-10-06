import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

st.bar_chart(df, x="Category", y="Sales")

st.dataframe(df.groupby("Category").sum())

st.bar_chart(
    df.groupby("Category", as_index=False).sum(),
    x="Category",
    y="Sales",
    color="#04f"
)

df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index("Order_Date", inplace=True)

sales_by_month = df.filter(items=["Sales"]).groupby(
    pd.Grouper(freq="ME")
).sum()

st.dataframe(sales_by_month)

st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")

st.write("### (1) Select a Category")

categories = sorted(df["Category"].dropna().unique())

selected_category = st.selectbox(
    "Category",
    categories
)

st.write("### (2) Select Sub_Category")

category_df = df[df["Category"] == selected_category]

sub_categories = sorted(
    category_df["Sub_Category"].dropna().unique()
)

selected_subcategories = st.multiselect(
    "Sub_Category",
    sub_categories,
    default=sub_categories
)

selected_df = category_df[
    category_df["Sub_Category"].isin(selected_subcategories)
]

st.write("### (3) Sales for Selected Sub_Category")

if len(selected_subcategories) > 0:

    sales_by_subcategory = (
        selected_df
        .groupby("Sub_Category")["Sales"]
        .sum()
        .reset_index()
    )

    st.line_chart(
        sales_by_subcategory,
        x="Sub_Category",
        y="Sales"
    )

else:
    st.warning("Please select at least one Sub_Category.")

st.write("### (4) Metrics for Selected Sub_Category")

if len(selected_subcategories) > 0:

    total_sales = selected_df["Sales"].sum()

    total_profit = selected_df["Profit"].sum()

    overall_profit_margin = (
        total_profit / total_sales * 100
        if total_sales != 0
        else 0
    )

    all_sales = df["Sales"].sum()

    all_profit = df["Profit"].sum()

    overall_average_profit_margin = (
        all_profit / all_sales * 100
        if all_sales != 0
        else 0
    )

    margin_difference = (
        overall_profit_margin -
        overall_average_profit_margin
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Sales",
        f"${total_sales:,.2f}"
    )

    col2.metric(
        "Total Profit",
        f"${total_profit:,.2f}"
    )

    col3.metric(
        "Overall Profit Margin",
        f"{overall_profit_margin:.2f}%",
        delta=f"{margin_difference:.2f} percentage points"
    )
