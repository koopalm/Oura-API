import requests
import matplotlib.pyplot as plt
from config import API_TOKEN


def fetch_sleep_data(start_date, end_date):
    """
    Fetch sleep data from the Oura API.
    """
    url = "https://api.ouraring.com/v2/usercollection/daily_sleep"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    params = {"start_date": start_date, "end_date": end_date}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data: {response.status_code} {response.text}")


def extract_deep_sleep(data):
    """
    Extract deep sleep data from the JSON response.
    """
    deep_sleep_data = []
    dates = []

    for item in data.get("data", []):
        dates.append(item["day"])
        deep_sleep_data.append(item["contributors"]["deep_sleep"])  # Already in minutes

    return dates, deep_sleep_data


def plot_comparison(dates_before, deep_sleep_before, dates_during, deep_sleep_during):
    """
    Plot comparison of deep sleep patterns before and during flu.
    """
    plt.figure(figsize=(12, 7))
    
    # Plot before flu
    plt.plot(dates_before, deep_sleep_before, marker="o", linestyle="-", color="blue", label="Before Flu")
    
    # Plot during flu
    plt.plot(dates_during, deep_sleep_during, marker="o", linestyle="-", color="green", label="During Flu")
    
    plt.xlabel("Date")
    plt.ylabel("Deep Sleep (minutes)")
    plt.title("Deep Sleep Patterns Before and During Flu")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.grid(True)
    plt.legend()
    
    # Save the plot to a file
    plt.savefig("deep_sleep_comparison.png")
    print("Plot saved as 'deep_sleep_comparison.png'.")
    
    # Show the plot without blocking
    plt.show(block=False)



def main():
    """
    Main function to compare deep sleep data before and during flu.
    """
    # Adjust these date ranges based on your experience
    before_flu_start_date = "2024-10-31"
    before_flu_end_date = "2024-11-10"
    during_flu_start_date = "2024-11-13"
    during_flu_end_date = "2024-11-30"

    print(f"Fetching data before flu from {before_flu_start_date} to {before_flu_end_date}...")
    before_flu_data = fetch_sleep_data(before_flu_start_date, before_flu_end_date)
    dates_before, deep_sleep_before = extract_deep_sleep(before_flu_data)

    print(f"Fetching data during flu from {during_flu_start_date} to {during_flu_end_date}...")
    during_flu_data = fetch_sleep_data(during_flu_start_date, during_flu_end_date)
    dates_during, deep_sleep_during = extract_deep_sleep(during_flu_data)

    # Display deep sleep comparison
    print("\nDeep Sleep Before Flu:")
    for date, deep_sleep in zip(dates_before, deep_sleep_before):
        print(f"Date: {date}, Deep Sleep: {deep_sleep} minutes")

    print("\nDeep Sleep During Flu:")
    for date, deep_sleep in zip(dates_during, deep_sleep_during):
        print(f"Date: {date}, Deep Sleep: {deep_sleep} minutes")

    # Plot comparison
    plot_comparison(dates_before, deep_sleep_before, dates_during, deep_sleep_during)


if __name__ == "__main__":
    main()
