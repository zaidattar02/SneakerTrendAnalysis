# Import necessary libraries
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
from serpapi import GoogleSearch

# Initialize pytrends with the chosen settings
pytrends = TrendReq(hl='en-US', tz=360)

# Define keywords for fashion trends analysis
kw_list = ["fashion trends", "streetwear", "sustainable fashion"]

# Build the payload with the specified keywords and settings
pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m', geo='', gprop='')

# Get interest over time for the specified keywords
trend_data = pytrends.interest_over_time()

# Display the first few rows of the data
print(trend_data.head())

# Plot the search trends over time
plt.figure(figsize=(10, 6))
plt.plot(trend_data.index, trend_data['fashion trends'], label='Fashion Trends')
plt.plot(trend_data.index, trend_data['streetwear'], label='Streetwear')
plt.plot(trend_data.index, trend_data['sustainable fashion'], label='Sustainable Fashion')
plt.title('Google Search Trends Over Time')
plt.xlabel('Date')
plt.ylabel('Search Interest')
plt.legend()
plt.show()