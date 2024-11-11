import instaloader
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from itertools import takewhile, dropwhile

# Create an instance of Instaloader
L = instaloader.Instaloader(download_pictures=False, download_comments=False, download_videos= False, compress_json= False)

L.login('flakocito','Flakocito123$')



# Section 1: Fetch Instagram Posts

def fetch_instagram_posts(hashtag, max_count=100):
    """
    Fetches posts from a specific Instagram hashtag.

    :param hashtag: The hashtag to search for (e.g., "fashion")
    :param max_count: Maximum number of posts to fetch
    :return: List of post details (likes, comments, date, etc.)
    """
    posts = []
    
    # Get the hashtag object
    for post in L.get_hashtag_posts(hashtag):
        if len(posts) >= max_count:
            break
        post_data = {
            'likes': post.likes,
            'comments': post.comments,
            'date': post.date_utc,
            'shortcode': post.shortcode,
        }
        posts.append(post_data)
    
    return posts

# Section 2: Analyze and Visualize Trendiness

def analyze_trendiness(posts):
    """
    Analyzes the trendiness of a hashtag based on the fetched posts.
    
    :param posts: List of post details fetched from Instagram
    :return: DataFrame containing analysis results
    """
    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(posts)

    # Calculate basic metrics
    avg_likes = df['likes'].mean()
    avg_comments = df['comments'].mean()
    total_posts = len(df)
    
    # Print basic analysis
    print(f"Average Likes: {avg_likes:.2f}")
    print(f"Average Comments: {avg_comments:.2f}")
    print(f"Total Posts Analyzed: {total_posts}")
    
    return df

def plot_trendiness(df, hashtag):
    """
    Plots the trendiness of the hashtag over time.
    
    :param df: DataFrame containing posts data
    :param hashtag: The hashtag being analyzed
    """
    plt.figure(figsize=(10, 6))
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['likes'].resample('D').mean().plot(label='Average Likes', legend=True)
    df['comments'].resample('D').mean().plot(label='Average Comments', legend=True)
    plt.title(f"Trendiness of #{hashtag} Over Time")
    plt.xlabel("Date")
    plt.ylabel("Average Engagement")
    plt.show()

# Main Execution: Fetch, Analyze, and Plot

if __name__ == "__main__":
    hashtag = "fashion"
    max_posts = 100
    fashion_posts = fetch_instagram_posts(hashtag, max_posts)
    trend_data = analyze_trendiness(fashion_posts)
    plot_trendiness(trend_data, hashtag)