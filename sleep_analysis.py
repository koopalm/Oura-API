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

def plot_comparisons(df):
    """
    Plot separate comparisons for deep sleep, REM sleep, and score metrics, displayed side by side.
    """
    metrics = ['deep_sleep (mean)', 'rem_sleep (mean)', 'score (mean)']
    titles = ['Deep Sleep', 'REM Sleep', 'Sleep Score']
    units = ['minutes', 'minutes', 'points']
    bar_width = 0.4
    x = range(len(df['is_weekend']))

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for i, (metric, title, unit) in enumerate(zip(metrics, titles, units)):
        ax = axes[i]
        bars = ax.bar(x, df[metric], width=bar_width, color=['skyblue', 'lightcoral'], label=metric)
        for bar, value in zip(bars, df[metric]):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                    f"{value:.1f} {unit}", ha="center", va="bottom", fontsize=10)
        ax.set_title(title, fontsize=14)
        ax.set_ylabel(f'Average {unit.title()}', fontsize=12)
        ax.set_xlabel('Day Type', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(df['is_weekend'], fontsize=12)

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

    print("Plotting comparisons...")
    plot_comparisons(stats)

if __name__ == "__main__":
    main()
