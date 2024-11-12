# Sneaker Trend Analysis Dashboard 👟📈

Welcome to the Sneaker Trend Analysis Dashboard! This interactive web application allows users to explore, compare, and forecast trends for popular sneaker brands using real-time Google search data. It is designed to provide insightful visualizations and analysis, helping users stay ahead of the latest sneaker trends.

## 🚀 Features

- **Individual Brand Analysis**: View search interest trends for the top 5 trending sneaker brands, updated in real time using SerpAPI and Google Trends data.
- **Compare Trends**: Compare search trends across multiple sneaker brands to identify emerging patterns and brand performance.
- **Seasonal Trend Analysis**: Analyze yearly seasonality effects for a selected sneaker brand, visualizing how interest fluctuates throughout the year.
- **Future Trend Forecasting**: Leverage Prophet's time series forecasting to predict future search interest for a selected sneaker brand.
- **Interactive AI Assistant** (Optional): An AI chatbot feature (currently disabled) was designed to assist users by answering questions about the trends and insights displayed on the dashboard.

## 🔧 Technologies Used

- **Python**: Main programming language for the backend and data analysis.
- **Streamlit**: Frontend framework for building the interactive web application.
- **SerpAPI**: API used for fetching real-time search data for sneaker trends.
- **Google Trends API**: Provides data for search interest trends.
- **Prophet**: Time series forecasting library for predicting future trends.
- **Plotly**: For creating interactive visualizations.


## 🛠️ Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/zaidattar02/SneakerTrendAnalysis.git
   cd SneakerTrendAnalysis

   python3 -m venv venv

2. **Set Up Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

4. **Run App**:
   ```bash
   streamlit run sneakers.py

5. **Using the App**:
Navigate to http://localhost:8501 in your browser to explore the dashboard.


## 📝 Notes
- The SerpAPI key is included directly in the project for ease of use since it is free. This means you can start using the app without setting up your own API key.
- If you encounter rate limits from Google Trends, please wait a few moments and try again, as the app implements exponential backoff to handle these limits gracefully.


      
