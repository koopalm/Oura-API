import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime
from config import API_TOKEN

def fetch_sleep_data(start_date, end_date):
    url = "https://api.ouraring.com/v2/usercollection/daily_sleep"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params = {"start_date": start_date, "end_date": end_date}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()["data"]
    else:
        print(f"Error fetching data: {response.status_code}")
        return []

def process_sleep_data(data):
    processed_data = []
    for item in data:
        day = item["day"]
        score = item["score"]
        deep_sleep = item["contributors"]["deep_sleep"]  # Deep sleep in minutes
        rem_sleep = item["contributors"]["rem_sleep"]  # REM sleep in minutes
        total_sleep = item["contributors"]["total_sleep"]  # Total sleep in minutes
        processed_data.append({
            "date": day,
            "score": score,
            "deep_sleep_minutes": deep_sleep,
            "rem_sleep_minutes": rem_sleep,
            "total_sleep_minutes": total_sleep,
        })
    return pd.DataFrame(processed_data)

def analyze_weekday_vs_weekend(df):
    df["date"] = pd.to_datetime(df["date"])
    df["is_weekend"] = df["date"].dt.dayofweek >= 5  # Saturday and Sunday
    stats = df.groupby("is_weekend").mean().reset_index()
    stats["is_weekend"] = stats["is_weekend"].map({False: "Weekdays", True: "Weekends"})
    return stats

def plot_comparison(stats):
    plt.figure(figsize=(10, 6))
    x = stats["is_weekend"]
    plt.bar(x, stats["score"], alpha=0.7, label="Sleep Score")
    plt.bar(x, stats["deep_sleep_minutes"], alpha=0.7, label="Deep Sleep (min)")
    plt.bar(x, stats["rem_sleep_minutes"], alpha=0.7, label="REM Sleep (min)")
    plt.bar(x, stats["total_sleep_minutes"], alpha=0.7, label="Total Sleep (min)")

    plt.title("Comparison of Sleep Metrics: Weekdays vs Weekends")
    plt.xlabel("Days")
    plt.ylabel("Metrics")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

def main():
    start_date = "2024-10-31"
    end_date = "2024-11-30"

    print(f"Fetching sleep data from {start_date} to {end_date}...")
    sleep_data = fetch_sleep_data(start_date, end_date)

    print("Processing sleep data...")
    df = process_sleep_data(sleep_data)

    print("Analyzing weekday vs. weekend...")
    stats = analyze_weekday_vs_weekend(df)

    print("Plotting comparison...")
    plot_comparison(stats)

if __name__ == "__main__":
    main()
