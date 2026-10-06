```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on July 14th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())

# Using as_index=False here preserves the Category as a column.
st.bar_chart(
    df.groupby("Category", as_index=False).sum(),
    x="Category",
    y="Sales",
    color="#04f"
)

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set it as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index("Order_Date", inplace=True)

# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=["Sales"]).groupby(
    pd.Grouper(freq="M")
).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")


# ==========================================================
# YOUR ADDITIONS
# ==========================================================

st.write("## Your additions")


# ==========================================================
# (1) Category dropdown
# ==========================================================

st.write("### (1) Select a Category")

categories = sorted(df["Category"].dropna().unique())

selected_category = st.selectbox(
    "Category",
    categories
)


# ==========================================================
# (2) Sub_Category multiselect based on selected Category
# ==========================================================

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


# Filter the data based on the selected Sub_Category values

selected_df = category_df[
    category_df["Sub_Category"].isin(selected_subcategories)
]


# ==========================================================
# (3) Line chart of Sales for selected Sub_Category
# ==========================================================

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


# ==========================================================
# (4) Three metrics
# ==========================================================

st.write("### (4) Metrics for Selected Sub_Category")

if len(selected_subcategories) > 0:

    total_sales = selected_df["Sales"].sum()

    total_profit = selected_df["Profit"].sum()

    overall_profit_margin = (
        total_profit / total_sales * 100
        if total_sales != 0
        else 0
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


    # ======================================================
    # (5) Delta for Overall Profit Margin
    # ======================================================

    # Calculate the overall profit margin for ALL products
    # across ALL categories

    all_sales = df["Sales"].sum()

    all_profit = df["Profit"].sum()

    overall_average_profit_margin = (
        all_profit / all_sales * 100
        if all_sales != 0
        else 0
    )

    # Difference between selected Sub_Category margin
    # and overall average margin

    margin_difference = (
        overall_profit_margin -
        overall_average_profit_margin
    )

    col3.metric(
        "Overall Profit Margin",
        f"{overall_profit_margin:.2f}%",
        delta=f"{margin_difference:.2f} percentage points"
    )
```
