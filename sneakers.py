import streamlit as st
from pytrends.request import TrendReq
import pandas as pd
from serpapi import GoogleSearch
from collections import Counter
from prophet import Prophet
import matplotlib.pyplot as plt
import time
import plotly.express as px
import random
from dotenv import load_dotenv

# Load environment variables
serpapi_key = "05c2966b0d626d9eea0e20490c92a911ffe65b0e589d905ae3ac06eb4513dadf"

# Sidebar Instructions
st.sidebar.title("👟 Sneaker Trend Analysis Dashboard")
with st.sidebar.expander("📋 Instructions"):
    st.markdown("""
    
    Here's how to use the app:
    
    - **Individual Trends**: Explore search trends for the top 5 trending sneaker brands.
    - **Compare Trends**: Select multiple brands to compare their search trends.
    - **Seasonal Trend Analysis**: Analyze seasonal trends for a selected brand using Prophet decomposition.
    - **Forecasting Future Trends**: Get predictions for future trends based on the historical data of a selected brand.
    
    Enjoy exploring the sneaker trend data! 🎉
    """)


@st.cache_data(ttl=3600)
def get_trending_sneakers_with_brands():
    params = {
        "q": "trending sneakers",
        "location": "United States",
        "api_key": serpapi_key,
        "tbm": "shop",
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    popular_brands = [
        "Nike", "Adidas", "New Balance", "Puma", "Reebok", "Vans", "Converse",
        "Under Armour", "Asics", "Saucony", "Hoka", "Jordans",
        "Yeezy", "Balenciaga", "Gucci", "Fila", "Sketchers", "Timberland", "On Cloud", "Alo", "alohas", "lululemon"
    ]

    brand_counts = Counter()
    if 'shopping_results' in results:
        for result in results['shopping_results']:
            sneaker_name = result.get('title', '').lower()
            for brand in popular_brands:
                if brand.lower() in sneaker_name:
                    brand_counts[brand] += 1
                    break
    return brand_counts

@st.cache_data(ttl=3600)
def fetch_trend_data(brand):
    pytrends = TrendReq(hl='en-US', tz=360)
    retries = 3
    delay = 10

    for attempt in range(retries):
        try:
            pytrends.build_payload([brand], cat=0, timeframe='today 12-m', geo='', gprop='')
            trend_data = pytrends.interest_over_time()
            if not trend_data.empty:
                return trend_data
        except Exception as e:
            if "429" in str(e):
                delay *= 2
                jitter = random.uniform(0, 5)
                time.sleep(delay + jitter)
            else:
                time.sleep(10)
    return pd.DataFrame()

# Fetch trending brands
brand_counts = get_trending_sneakers_with_brands()
top_brands = list(brand_counts.keys())[:5]

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Individual Trends", "Compare Trends", "Seasonal Trend Analysis", "Forecasting Future Trends"])

# Tab 1: Individual Trends
with tab1:
    st.subheader("Google Search Trends for Top 5 Brands")
    st.info("""
    **Description:**  
    In this tab, you can view individual search trends for the top 5 trending sneaker brands.  
    Explore the search interest over the past 12 months for each brand, visualized as an interactive line graph.
    """)
    st.sidebar.header("Top 5 Trending Sneaker Brands")
    
    trend_data_dict = {}
    for brand in top_brands:
        st.sidebar.write(f"{brand}")
        try:
            trend_data = fetch_trend_data(brand)
            if not trend_data.empty:
                trend_data_dict[brand] = trend_data
                fig = px.line(
                    trend_data,
                    x=trend_data.index,
                    y=brand,
                    title=f"Search Trend for {brand}",
                    labels={"x": "Date", "y": "Search Interest"}
                )
                fig.update_layout(yaxis_title="Search Interest")
                st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.write(f"Error fetching data for {brand}: {e}")

# Tab 2: Compare Trends
with tab2:
    st.subheader("Compare Search Trends for Multiple Brands")
    st.info("""
    **Description:**  
    This tab allows you to compare search trends for multiple sneaker brands.  
    Select the brands you want to compare from the dropdown menu to see how their search interest has evolved over time.
    """)

    selected_brands = st.multiselect("Select brands to compare:", top_brands, default=top_brands[:2])

    if selected_brands:
        fig = px.line(
            title="Comparison of Search Trends",
            labels={"x": "Date", "y": "Search Interest"}
        )
        for brand in selected_brands:
            if brand in trend_data_dict:
                trend_data = trend_data_dict[brand]
                fig.add_scatter(x=trend_data.index, y=trend_data[brand], mode='lines', name=brand)

        fig.update_layout(yaxis_title="Search Interest", xaxis_title="Date")
        st.plotly_chart(fig, use_container_width=True)

# Tab 3: Seasonal Trend Analysis
with tab3:
    st.subheader("Seasonal Trend Analysis")
    st.info("""
    **Description:**  
    Analyze the seasonal effects in search trends for a selected brand.  
    This analysis highlights recurring patterns in the search interest, such as yearly seasonality.
    """)
    selected_seasonal_brand = st.selectbox("Select a brand for seasonal analysis", top_brands)

    if selected_seasonal_brand and selected_seasonal_brand in trend_data_dict:
        trend_data = trend_data_dict[selected_seasonal_brand]
        df = trend_data[[selected_seasonal_brand]].reset_index()
        df.columns = ['ds', 'y']
        model = Prophet(yearly_seasonality=True, weekly_seasonality=True)
        model.fit(df)
        future = model.make_future_dataframe(periods=180)
        forecast = model.predict(future)
        yearly = forecast[['ds', 'yearly']]
        yearly_fig = px.line(yearly, x='ds', y='yearly', title=f"Yearly Seasonality for {selected_seasonal_brand}")
        yearly_fig.update_layout(xaxis_title="Date", yaxis_title="Yearly Seasonal Effect")
        st.plotly_chart(yearly_fig, use_container_width=True)

# Tab 4: Forecasting Future Trends
with tab4:
    
    
    st.info("""
    **Description:**  
    Predict future search interest trends for a selected brand using time series forecasting.  
    This tab provides insights into potential future popularity of the brand based on historical data.
    """)
    selected_brand = st.selectbox("Select a brand to forecast", top_brands)

    if selected_brand and selected_brand in trend_data_dict:
        st.subheader(f"Forecasting Future Trends for {selected_brand}")
        trend_data = trend_data_dict[selected_brand]
        df = trend_data[[selected_brand]].reset_index()
        df.columns = ['ds', 'y']
        model = Prophet()
        model.fit(df)
        future = model.make_future_dataframe(periods=180)
        forecast = model.predict(future)

        forecast_display = forecast.rename(columns={
            'ds': 'Date',
            'yhat': 'Predicted Value',
            'yhat_lower': 'Lower Bound (Confidence Interval)',
            'yhat_upper': 'Upper Bound (Confidence Interval)'
        })

        fig1 = model.plot(forecast)
        ax = fig1.gca()
        legend_labels = ["Actual Data", "Predicted Trend", "Confidence Interval"]
        ax.legend(legend_labels, loc='upper left', fontsize=10)
        st.pyplot(fig1)

        date_options = forecast['ds'].dt.strftime('%Y-%m-%d').tolist()
        selected_date = st.selectbox("Select a date to view the forecast:", date_options)
        selected_row = forecast_display[forecast_display['Date'].dt.strftime('%Y-%m-%d') == selected_date]

        if not selected_row.empty:
            st.write(selected_row[['Date', 'Predicted Value', 'Lower Bound (Confidence Interval)', 'Upper Bound (Confidence Interval)']])
        else:
            st.write("No data available for the selected date.")