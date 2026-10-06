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
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

st.write("## Your additions")
st.write("### (1) add a drop down for Category (https://docs.streamlit.io/library/api-reference/widgets/st.selectbox)")
st.write("### (2) add a multi-select for Sub_Category *in the selected Category (1)* (https://docs.streamlit.io/library/api-reference/widgets/st.multiselect)")
st.write("### (3) show a line chart of sales for the selected items in (2)")
st.write("### (4) show three metrics (https://docs.streamlit.io/library/api-reference/data/st.metric) for the selected items in (2): total sales, total profit, and overall profit margin (%)")
st.write("### (5) use the delta option in the overall profit margin metric to show the difference between the overall average profit margin (all products across all categories)")

```python
import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("your_data.csv")

st.title("Sales Dashboard")

# --------------------------------------------------
# 1. Category dropdown
# --------------------------------------------------

categories = sorted(df["Category"].dropna().unique())

selected_category = st.selectbox(
    "Select a Category",
    categories
)

# --------------------------------------------------
# 2. Sub_Category multiselect based on Category
# --------------------------------------------------

category_df = df[df["Category"] == selected_category]

sub_categories = sorted(
    category_df["Sub_Category"].dropna().unique()
)

selected_subcategories = st.multiselect(
    "Select Sub_Category",
    sub_categories,
    default=sub_categories
)

# --------------------------------------------------
# Filter data based on selections
# --------------------------------------------------

selected_df = category_df[
    category_df["Sub_Category"].isin(selected_subcategories)
]

# --------------------------------------------------
# 3. Line chart of Sales
# --------------------------------------------------

if len(selected_subcategories) > 0:

    sales_by_subcategory = (
        selected_df
        .groupby("Sub_Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    st.subheader("Sales by Selected Sub-Category")

    st.line_chart(sales_by_subcategory)

# --------------------------------------------------
# 4. Three metrics
# --------------------------------------------------

if len(selected_subcategories) > 0:

    total_sales = selected_df["Sales"].sum()
    total_profit = selected_df["Profit"].sum()

    overall_profit_margin = (
        total_profit / total_sales * 100
        if total_sales != 0
        else 0
    )

    # --------------------------------------------------
    # 5. Overall average profit margin
    #    across ALL products/categories
    # --------------------------------------------------

    all_sales = df["Sales"].sum()
    all_profit = df["Profit"].sum()

    overall_average_profit_margin = (
        all_profit / all_sales * 100
        if all_sales != 0
        else 0
    )

    # Difference between selected products and overall average
    margin_difference = (
        overall_profit_margin - overall_average_profit_margin
    )

    # Display metrics
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

else:
    st.warning("Please select at least one Sub_Category.")
```

