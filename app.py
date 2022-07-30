from tkinter import Y
import pandas as pd
import streamlit as st
import plotly.express as px

#PAGE CONGIGS

#emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Dashboard",
page_icon=":bar_chart:",
layout='wide',

)

#READING DATAFRAME
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        'supermarkt_sales.xlsx',
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000,

    )
    #Add hour column to df
    df["Hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()


#SIDEBAR

st.sidebar.header("Select your filters here: ")
city = st.sidebar.multiselect(
    "CITY:",
    options=df["City"].unique(),
    default=df["City"].unique(),
)

customer_type = st.sidebar.multiselect(
    "CUSTOMER:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique(),
)

gender = st.sidebar.multiselect(
    "GENDER:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique(),
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)


#MAIN PAGE

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

#KPI's

total_sales = int(df_selection['Total'].sum())
average_rating = round(df_selection["Rating"].mean(),1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sales_by_transaction = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US ${total_sales:,}")
with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"US ${average_rating:,}")
    st.subheader(star_rating)
with right_column:
    st.subheader("Sales by Transaction:")
    st.subheader(f'US ${average_sales_by_transaction:,}')

st.markdown("---")

#SALES BY PRODUCT LINE [BAR CHART]

sales_by_product_line = (
    df_selection.groupby("Product line").sum()[["Total"]].sort_values("Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x='Total',
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


# SALES BY HOUR
sales_by_hour = df_selection.groupby("Hour").sum()[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    y='Total',
    x=sales_by_hour.index,
    title="<b> Sales by Hour </b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)

fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(showgrid=False),
)

left_bar_column, right_bar_column = st.columns(2)
left_bar_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_bar_column.plotly_chart(fig_product_sales, use_container_width=True)


#Sales by Gender

sales_by_gender = df.groupby("Gender").sum()[["Total"]]

fig_pie_gender = px.pie(
    sales_by_gender,
    names=sales_by_gender.index,
    values='Total',
    title="<b> Sales by Gender </b>",
    )

st.plotly_chart(fig_pie_gender)

