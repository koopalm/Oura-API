import pandas as pd
import matplotlib.pyplot as plt
from config import API_TOKEN
import requests

# Constants
BASE_URL = "https://api.ouraring.com/v2/usercollection/daily_sleep"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

def fetch_sleep_data(start_date, end_date):
    """
    Fetch sleep data from the Oura API for the given date range.
    """
    params = {"start_date": start_date, "end_date": end_date}
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def process_sleep_data(raw_data):
    """
    Process raw sleep data into a DataFrame.
    """
    sleep_data = raw_data.get("data", [])
    records = []
    for item in sleep_data:
        records.append({
            "date": item["day"],
            "deep_sleep": item["contributors"]["deep_sleep"],
            "rem_sleep": item["contributors"]["rem_sleep"],
            "score": item["score"]
        })
    df = pd.DataFrame(records)
    df["date"] = pd.to_datetime(df["date"])
    df["day_of_week"] = df["date"].dt.day_name()
    return df

def analyze_weekday_vs_weekend(df):
    """
    Compare sleep stats between weekdays and weekends with date ranges.
    """
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 'Weekend' if x in ['Saturday', 'Sunday'] else 'Weekday')
    
    grouped = df.groupby('is_weekend').agg({
        'deep_sleep': 'mean',
        'rem_sleep': 'mean',
        'score': 'mean',
        'date': ['min', 'max']  # Adding min and max dates for range
    }).reset_index()
    
    # Flatten multi-level columns
    grouped.columns = ['is_weekend', 'deep_sleep (mean)', 'rem_sleep (mean)', 'score (mean)', 'start_date', 'end_date']
    
    # Add a date range column
    grouped['date_range'] = grouped['start_date'].dt.strftime('%Y-%m-%d') + ' to ' + grouped['end_date'].dt.strftime('%Y-%m-%d')
    grouped.drop(['start_date', 'end_date'], axis=1, inplace=True)

    return grouped

def plot_comparison(df):
    """
    Plot comparison of sleep stats between weekdays and weekends in a single graph.
    """
    metrics = ['deep_sleep (mean)', 'rem_sleep (mean)', 'score (mean)']
    x = range(len(df['is_weekend']))

    plt.figure(figsize=(10, 6))

    for i, metric in enumerate(metrics):
        plt.bar([pos + i * 0.25 for pos in x], df[metric], width=0.25, label=metric)

    plt.title('Comparison of Sleep Metrics Between Weekdays and Weekends')
    plt.ylabel('Average Values')
    plt.xlabel('Day Type')
    plt.xticks([pos + 0.25 for pos in x], df['is_weekend'])
    plt.legend()
    plt.tight_layout()
    plt.show()

def main():
    """
    Main function to fetch, process, analyze, and visualize sleep data.
    """
    start_date = "2024-10-31"
    end_date = "2024-11-30"
    print(f"Fetching sleep data from {start_date} to {end_date}...")
    
    raw_data = fetch_sleep_data(start_date, end_date)
    print("Processing sleep data...")
    df = process_sleep_data(raw_data)
    
    print("Analyzing weekday vs. weekend...")
    stats = analyze_weekday_vs_weekend(df)
    print(stats)

    print("Plotting comparison...")
    plot_comparison(stats)

if __name__ == "__main__":
    main()
