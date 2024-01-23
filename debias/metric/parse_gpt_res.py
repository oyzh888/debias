import json

import pandas as pd

# Path to the CSV file - Replace with the actual path
from debias.consts import EXPORT_METRIC_CSV_PATH


def parse_json(json_string):
    """Safely parse a JSON string."""
    try:
        return json.loads(json_string.replace('\n', ''))
    except ValueError:
        return {}

def calculate_metrics(df):
    """Calculate aggregate metrics from the DataFrame."""
    df['parsed_result'] = df['result'].apply(parse_json)
    average_accuracy = df['parsed_result'].apply(lambda x: x.get('Accuracy', 0)).mean()
    average_keywords_matching = df['parsed_result'].apply(lambda x: x.get('Keywords Matching', 0)).mean()

    # Calculate average for each key in 'Music Metrics'
    music_metrics_keys = ['Human Likability', 'Creativity', 'Relevance', 'Coherence', 'Emotional Resonance', 'Cultural Appropriateness']
    music_metrics_averages = {key: df['parsed_result'].apply(lambda x: x.get('Music Metrics', {}).get(key, 0)).mean() for key in music_metrics_keys}

    return average_accuracy, average_keywords_matching, music_metrics_averages

def print_insights(average_accuracy, average_keywords_matching, music_metrics_averages):
    """Print the calculated insights."""
    print(f"Average Accuracy: {average_accuracy:.2f}")
    print(f"Average Keywords Matching: {average_keywords_matching:.2f}")
    print("Average Music Metrics:")
    for key, value in music_metrics_averages.items():
        print(f"  {key}: {value:.2f}")

def process_csv(file_path):
    """Process the CSV file and return a DataFrame."""
    return pd.read_csv(file_path)

def main():
    """Main function to execute the script."""
    df = process_csv(EXPORT_METRIC_CSV_PATH)
    average_accuracy, average_keywords_matching, music_metrics_averages = calculate_metrics(df)
    print_insights(average_accuracy, average_keywords_matching, music_metrics_averages)

if __name__ == '__main__':
    main()
