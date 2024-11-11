from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
from serpapi import GoogleSearch
from collections import Counter

def get_trending_sneakers_with_brands():
    # Initialize SerpAPI with your API key
    api_key = "05c2966b0d626d9eea0e20490c92a911ffe65b0e589d905ae3ac06eb4513dadf"
    
    # Set up parameters for a shopping search query
    params = {
        "q": "trending sneakers",
        "location": "United States",
        "api_key": api_key,
        "tbm": "shop",  # Set search type to "shopping"
    }

    # Fetch search results using SerpAPI
    search = GoogleSearch(params)
    results = search.get_dict()

    # Predefined list of popular sneaker brands
    popular_brands = [
        "Nike", "Adidas", "New Balance", "Puma", "Reebok", "Vans", "Converse", 
        "Under Armour", "Asics", "Saucony", "Hoka", "Jordan", 
        "Yeezy", "Balenciaga", "Gucci", "Fila", "Sketchers", "Timberland", "On Cloud", "Alo", "alohas", "lululemon"
    ]

    # Initialize a list to store sneaker names and a Counter for brands
    sneakers = []
    brand_counts = Counter()

    # Check if 'shopping_results' exists in the response
    if 'shopping_results' in results:
        # Extract sneaker names and potential brands from shopping results
        for result in results['shopping_results']:
            sneaker_name = result.get('title', '').lower()  # Convert to lowercase for easier matching

            # Check if any brand from the list is in the sneaker name
            for brand in popular_brands:
                if brand.lower() in sneaker_name:
                    brand_counts[brand] += 1  # Increment brand count
                    sneakers.append(sneaker_name)
                    break  # Stop checking once a brand is found to avoid double-counting

    return sneakers, brand_counts

# Example usage
trending_sneakers, brand_counts = get_trending_sneakers_with_brands()
# print("Trending Sneakers:", trending_sneakers)
# print("Brand Counts:", brand_counts)

pytrends = TrendReq(hl='en-US', tz=360)

# Example usage: Extracted brands from your previous code
brands = list(brand_counts.keys())  # Convert the extracted brands to a list

print(brands)

brands = brands[:5]

# Fetch Google Trends data for the extracted brands
if brands:
    pytrends.build_payload(brands, cat=0, timeframe='today 12-m', geo='', gprop='')
    
    # Get interest over time
    trend_data = pytrends.interest_over_time()

    print(trend_data.head())

    # Plot the data
    if not trend_data.empty:
        trend_data.plot(figsize=(10, 6))
        plt.title('Google Search Trends for Trending Sneaker Brands')
        plt.xlabel('Date')
        plt.ylabel('Search Interest')
        plt.show()
    else:
        print("No trend data available for the current keywords.")
else:
    print("No trending sneaker brands found.")

# Plot the most popular brands
# if brand_counts:
#     plt.figure(figsize=(10, 6))
#     plt.bar(brand_counts.keys(), brand_counts.values(), color='skyblue')
#     plt.title('Most Popular Sneaker Brands')
#     plt.xlabel('Brand')
#     plt.ylabel('Frequency')
#     plt.xticks(rotation=45)
#     plt.show()
# else:
#     print("No brand data available to plot.")
