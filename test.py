import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt 
import plotly.figure_factory as ff 
import numpy as np
from geopy.geocoders import Nominatim
import pydeck as pdk

st.set_page_config(layout='wide')

file1= 'dataset_final (1).csv'
file2= 'wwww.csv'

# Title
st.title("Company Revenue by Sector Visualizer")
st.caption("Unraveling India's startup Boom in AI and EV : Uncovering Market Trends,Dividing Factors and Creating an Interactive Dashboard for Insights")


data1 = pd.read_csv(file1, encoding='latin-1')
data2 = pd.read_csv(file2, encoding='latin-1')

if data1 is not None:
    # Display the raw data
    st.subheader("Raw Data")
    st.write(data1)

    # Create a bar chart for revenue by sector
    st.header("Revenue by Sector")
    st.caption("The distribution of income among various business sectors, providing valuable insights into which industries are driving the financial success of emerging companies.")
    fig = px.bar(data1, x="Sector", y="Revenue",width=1274)
    st.plotly_chart(fig)



st.header("Top 10 Performing Sectors Year by Year")
st.caption("This insightful analysis that tracks the ever-evolving landscape of industries, providing an annual snapshot of the ten sectors that exhibit the highest growth and success, offering valuable trends and business intelligence over time.")
top_10_sectors = data1.groupby(['Year', 'Sector'])['Revenue'].sum().reset_index()
top_10_sectors = top_10_sectors.groupby('Year').apply(lambda x: x.nlargest(10, 'Revenue')).reset_index(drop=True)

# Create a scatter chart to visualize the top 10 sectors year by year
fig = px.bar(top_10_sectors, x="Year", y="Revenue", color="Sector", labels={"Revenue": "Total Revenue"},width=1274)
st.plotly_chart(fig)


# Sort the data by revenue and select the top 100 companies
top_100_companies = data1.sort_values(by="Revenue", ascending=False).head(100)





# Streamlit app title
st.title("Company Revenue Over Time")
st.caption("this is a dynamic analysis that tracks the financial performance of businesses across different periods, providing insights into revenue trends and helping stakeholders make informed decisions based on historical financial data.")
x1 = data2["Year1"]
x2= data2["Year2"]
x3 = data2["Year3"]


hist_data = [x1,x2,x3]

group_labels = ["Revenue1","Revenue2","Revenue3"]
fig = ff.create_distplot(
    hist_data, group_labels , bin_size=[.1,.2,.3])

st.plotly_chart(fig,use_container_width=True)

#chart_data = pd.DataFrame(   
#    {       "col1": data1['Year'], 
#            "col2": data1['Revenue'],      
#            "col3": data1['Sector'], })
#st.line_chart(chart_data, x="col1", y="col2", color="col3")





# Group data by year and sector and count unique companies emerging each year
emerging_companies = data1.groupby(['Year', 'Sector'])['Company/Brand'].nunique().reset_index()

    # Create a line chart to visualize the number of emerging companies by sector over the years
st.header("Number of Companies Emerging in different Sectors Over the Years")
st.caption("It is a comprehensive study that maps the growth and evolution of industries, charting the rise of companies in each sector year by year, offering valuable insights into changing business landscapes and emerging market trends.")
fig = px.line(emerging_companies, x="Year", y="Company/Brand", color="Sector", labels={"Company": "Number of Companies"},width=1274)

st.plotly_chart(fig)



st.header("Amount invested in different sectors")
st.caption("It is a comprehensive overview of capital allocation across various industries, revealing the financial landscape and highlighting sectors attracting significant investments, offering key insights for strategic decision-making and market analysis.")
# Get the sector and investment amount columns from the data1 DataFrame
sector_column = data1['Sector']
investment_amount_column = data1['Amount($)']

# Create a pie chart
fig = px.pie(data1, values=investment_amount_column, names=sector_column, color=sector_column,height = 700,width=1274)

# Display the pie chart in Streamlit
st.plotly_chart(fig)



st.header("Revenue based on investment type")
st.caption("Revenue based on Investment Type delves into the correlation between the source of capital and a company's income, shedding light on how different investment types impact financial performance and offering valuable insights for investment strategy and decision-making.")

# Create a line chart of revenue vs. investment type
fig = px.line(
    data1,
    x="Stage",
    y="Revenue",
    color="Stage",
    width=1274
)

# Display the line chart in Streamlit
st.plotly_chart(fig)



st.header("Investment amount based on investment type")
st.caption("It offers a visual representation of how different types of investments contribute to the overall capital pool, providing a clear and intuitive way to understand the distribution of funds across investment categories.")
# Get the investment type and investment amount columns from the data1 DataFrame
investment_type_column = data1['Stage']
investment_amount_column = data1['Amount($)']

# Create a pie chart
fig = px.pie(data1, values=investment_amount_column, names=investment_type_column, color=investment_type_column, width=1274)

# Display the pie chart in Streamlit
st.plotly_chart(fig)





# Change the default matplotlib style to dark
plt.style.use("dark_background")

st.title("Sector Revenue Visualization")

# Create a dropdown widget to select a year
selected_year = st.selectbox("Select a Year", data1['Year'].unique())

# Filter the data based on the selected year
filtered_data = data1[data1['Year'] == selected_year]

# Group the data by sector and calculate the total revenue for each sector
sector_revenue = filtered_data.groupby('Sector')['Revenue'].sum()

# Create a bar plot chart
fig, ax = plt.subplots()
sector_revenue.plot(kind='bar', ax=ax)
ax.set_xlabel("Sector")
ax.set_ylabel("Total Revenue")
ax.set_title(f"Total Revenue by Sector in Year {selected_year}")
st.pyplot(fig)








st.title("3D Company Revenue Map")

# Create a PyDeck map using the given data
layer = pdk.Layer(
    'ScatterplotLayer',
    data=data1,
    get_position='[Longitude, Latitude, Revenue/5000]',  # Add revenue as a third dimension
    get_color='[200, 30, 0, 160]',
    get_radius=2000,
    pickable=True,
    extruded=True,
)

view_state = pdk.ViewState(
    latitude=data1['Latitude'].mean(),
    longitude=data1['Longitude'].mean(),
    zoom=4,
)

tooltip = {
    'html': '<b>Company:</b> {Company}<br /><b>Revenue:</b> {Revenue}',
}

# Create the PyDeck Deck
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip
)

# Display the map
st.pydeck_chart(deck)

    # Create a treemap for location-wise distribution
st.header("Location-Wise Distribution of Top 100 Companies")
st.caption("It offers a geographic perspective on business success, showcasing the regions where the top 100 companies are situated, revealing the geographical diversity of corporate excellence. This analysis aids in understanding the strategic placement of key players in the global business landscape.")
fig = px.treemap(top_100_companies, 
                     path=['HQ'],
                     values='Revenue',
                     color='Revenue',
                     color_continuous_scale='Viridis',
                     width=1274)

    # Display the treemap
st.plotly_chart(fig)