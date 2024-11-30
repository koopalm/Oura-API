# Oura Sleep Analysis

This project analyzes and visualizes sleep data from the Oura Ring. It compares weekday and weekend sleep metrics, such as deep sleep, REM sleep, sleep scores, and total sleep hours, over a specified date range.

## Features

- Fetches sleep data from the Oura API.
- Analyzes and compares sleep patterns on weekdays and weekends.
- Visualizes the comparisons in a single graph for clarity.
- Displays averages for all sleep metrics:
  - Deep Sleep (minutes)
  - REM Sleep (minutes)
  - Sleep Score (0-100)
  - Total Sleep Duration (hours)

## File Structure

- **`config.py`**: Stores the API token for accessing the Oura API.
- **`requirements.txt`**: Lists the Python dependencies for the project.
- **`sleep_analysis.py`**: The main script for data analysis and visualization.

## Requirements

To run this project, you need:

- Python 3.10 or higher
- An Oura API token

Install the required packages using:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/koopalm/Oura-API.git
   cd Oura-API
   ```
   
   ```bash
   cd Oura-API
   ```

2. Add your Oura API token to `config.py`:
   ```python
   API_TOKEN = "your_api_token_here"
   ```

3. Run the analysis:
   ```bash
   python sleep_analysis.py
   ```

4. The script will:
   - Fetch data for a date range.
   - Compute and display averages for weekdays and weekends.
   - Visualize the results in a single graph.

## Example Output

The script generates a bar chart comparing averages for weekdays and weekends, with metrics such as deep sleep and REM sleep duration, and sleep score points.

![image](https://github.com/user-attachments/assets/ae439c90-c5f3-4a87-9942-0111c7a87761)


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
