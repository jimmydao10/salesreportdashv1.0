import pandas as pd
import plotly_express as plt
import streamlit as st
from streamlit_extras.stylable_container import stylable_container



st.set_page_config(
    "Sales Report Dashboard for Company XYZ",
    page_icon=":bar_chart",
    layout="wide",
)


# #CSS Styling for the background of the webpage
# pageBackground = """
# <style>
# [data-testid="stAppViewContainer"] {
# background-color: rgba(0, 0, 0, 0.4);
# }
# </style>
# """

# st.markdown(
# pageBackground,
# unsafe_allow_html=True
# )

# Read the excel file
df = pd.read_excel("SaleData.xlsx")


# Setting up the sidebar on the webpage

st.sidebar.header("Filter(s): ")

item = st.sidebar.multiselect(
    "Select the Item: ",
    options=df["Item"].unique(),
    default=df["Item"].unique()
)

salesMan = st.sidebar.multiselect(
    "Select the Sales Man(s): ",
    options=df["SalesMan"].unique(),
    default=df["SalesMan"].unique()
)

manager = st.sidebar.multiselect(
    "Select the Manager(s): ",
    options=df["Manager"].unique(),
    default=df["Manager"].unique()
)

dfSelection = df.query(
    "Item == @item & SalesMan == @salesMan & Manager == @manager"
)

# Error Checking if user left filters empty
if dfSelection.empty:
    st.write("Please select the filters!"),
    st.stop

# Header of page
st.title("📈 Sales Report Dashboard")

# ---Main KPIs---

# This KPI will be for total sales amount (USD)
totalSales = dfSelection["Sale_amt"].sum()

# This KPI will be for the average sales amount (USD)
averageSales = dfSelection["Sale_amt"].mean()

# This KPI will be for the total amount of Units Sold
totalUnits = dfSelection["Units"].sum()

# Further organizing the webpage/dashboard with dedicated columns for each KPI
LeftColumn, MiddleColumn, RightColumn = st.columns(3)
with LeftColumn:
    #CSS Styling for the KPIS
    with stylable_container(
        key = "TotalSalesKPI",
        css_styles = """
        {
            padding: 0.5em;
            background-color: #615EFF;
            box-shadow: 0 3px 10px rgb(0 0 0 / 1);
            text-align: center;
            display-inline: flex;
        }
        """

    ):
        st.subheader("Total Sales Amount (USD)")
        st.subheader(f"$ {totalSales:,}")
with MiddleColumn:
    #CSS Styling for the KPIS    
    with stylable_container(
        key = "AverageSalesKPI",
        css_styles = """
        {
            padding: 0.5em;
            background-color: #615EFF;
            box-shadow: 0 3px 10px rgb(0 0 0 / 1);
            text-align: center;
            display-inline: flex;
        }
        """

    ):
        st.subheader("Average Sales Amount (USD)")
        st.subheader(f"$ {averageSales:,.2f}")
with RightColumn:
    #CSS Styling for the KPIS
    with stylable_container(
        key = "UnitsSoldKPI",
        css_styles = """
        {
            padding: 0.5em;
            background-color: #615EFF;
            box-shadow: 0 3px 10px rgb(0 0 0 / 1);
            text-align: center;
            display-inline: flex;
        }
        """

    ):
        st.subheader("Total Units Sold")
        st.subheader(f"{totalUnits:,}")

# This will separate the KPIS from the Visualizations
st.markdown("---")




## -- Graph/Data Visualization Section

# Pie Chart for SalesMan and their sales amount (Indicating which Sales man performed best when it comes to selling)

SalesManBySalesAmt = dfSelection.groupby(by=["SalesMan"])[["Sale_amt"]].sum()

figurePie = plt.pie(
    SalesManBySalesAmt,
    values = "Sale_amt",
    names = SalesManBySalesAmt.index,
    hole = .3,
    title = "Sales Man by Sale Amount", 
    width = 400
)


# Bar Chart for Item and the amount of Units sold (Indicating which item sold best)

ItemByUnitsSold = dfSelection.groupby(by=["Item"])[["Units"]].sum()

figureBar = plt.bar(
    ItemByUnitsSold,
    x = "Units",
    y = ItemByUnitsSold.index,
    title = "Units Sold by Items",
    width = 400,
    template = "plotly"
)
    
# Possible  heatmap to show which region performed best?

RegionBySaleAmt = dfSelection.groupby(by=["Region"])[["Sale_amt"]].sum()

figureMap = plt.bar(
    RegionBySaleAmt,
    x = RegionBySaleAmt.index,
    y = "Sale_amt",
    title = "Sale Amount by Regions",
    width = 400,
    template = "plotly_dark",
)

# Possible pie chart for manager performance

ManagerBySaleAmt = dfSelection.groupby(by=["Manager"])[["Sale_amt"]].sum()

figurePieManager = plt.pie(
    ManagerBySaleAmt,
    values = "Sale_amt",
    names = ManagerBySaleAmt.index,
    hole = 0.3,
    title = "Manager(s) by Sales Amount",
    width = 400
)


# More KPIS

averageUnits = dfSelection["Units"].mean()

totalManagers = dfSelection["Manager"].unique()
totalManagersCount = len(totalManagers)

totalEmployees = dfSelection["SalesMan"].unique()
totalEmployeesCount = len(totalEmployees)




LeftColumn2, MiddleColumn2, RightColumn2 = st.columns(3)
with LeftColumn2:
    st.plotly_chart(figurePie)
with MiddleColumn2:
    st.plotly_chart(figureBar)
with RightColumn2:
    st.plotly_chart(figureMap)

LeftColumn3, MiddleColumn3, RightColumn3 = st.columns(3)
with LeftColumn3:
    st.plotly_chart(figurePieManager)
with MiddleColumn3:
    #CSS Styling for the KPIS
    with stylable_container(
        key = "ExtraKPIs",
        css_styles = """
        {
            padding: 0.5em;
            background-color: #615EFF;
            box-shadow: 0 3px 10px rgb(0 0 0 / 1);
            text-align: center;
            display-inline: flex;
        }
        """

    ):
        st.subheader("Average Units of Items: ")
        st.subheader(f"{averageUnits:,.2f}")
        st.markdown("--")
        st.subheader("Total Managers:")
        st.subheader(f"{totalManagersCount}")
        st.markdown("--")
        st.subheader("Total Employees:")
        st.subheader(f"{totalEmployeesCount}")
        



with st.expander("View Data Table"):
    st.dataframe(dfSelection)



