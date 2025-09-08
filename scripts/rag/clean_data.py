import json
import re
import os
import logging
import argparse
from datetime import datetime

# --- Logging Setup ---
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILENAME = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}_cleaning.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILENAME),
        logging.StreamHandler()
    ]
)


def anonymize_text(text):
    """
    Anonymizes PII in a given text string.
    """
    if not isinstance(text, str):
        return text

    # Replace email addresses
    text = re.sub(r'[\w\.-]+@[\w\.-]+', '[EMAIL]', text)

    # Replace full names (simple pattern, might need refinement)
    # This looks for Title Case words in sequence.
    text = re.sub(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', '[NAME]', text)

    # Replace usernames/NetIDs (patterns observed in sample data)
    text = re.sub(r'\b[a-z]{2,3}\d{3,4}\b', '[USER]', text) # e.g., rm1238, yw969, so398
    text = re.sub(r'\bpgarias\b', '[USER]', text) # specific user from sample
    text = re.sub(r'\bthackray\b', '[USER]', text) # specific user from sample

    # Generalize file paths
    text = re.sub(r'\/projects\/f_[a-z0-9]+_\d', '/projects/[USER_PROJECT]', text)

    # Generalize cluster hostnames
    text = re.sub(r'amarel\.rutgers\.edu', '[CLUSTER_HOSTNAME]', text)

    # Remove or generalize URLs
    text = re.sub(r'https?:\/\/\S+', '[URL]', text)

    return text

def clean_description(text):
    """
    Performs general cleaning on the description field.
    """
    if not isinstance(text, str):
        return text

    # Remove redundant "original account request" sections
    text = re.sub(r'#+\s*Below is the original account request\s*#+.*', '', text, flags=re.DOTALL)

    # Remove Smartsheet footers
    text = re.sub(r'You are receiving this email because.*', '', text, flags=re.DOTALL)
    text = re.sub(r'Powered by Smartsheet Inc\..*', '', text, flags=re.DOTALL)


    # Normalize whitespace
    text = ' '.join(text.split())

    return text

def process_servicenow_data(input_path, output_path):
    """
    Reads ServiceNow data from a JSON file with a 'records' key, 
    anonymizes and cleans it, and writes the cleaned data to a new file 
    with the same structure.
    """
    try:
        with open(input_path, 'r') as f:
            data = json.load(f)
        records = data.get('records', [])
    except FileNotFoundError:
        logging.error(f"Error: Input file not found at {input_path}")
        return
    except json.JSONDecodeError:
        logging.error(f"Error: Could not decode JSON from {input_path}")
        return

    if not records:
        logging.warning(f"No records found in {input_path}. Writing an empty records file.")
        anonymized_data = []
    else:
        anonymized_data = []
        for entry in records:
            anonymized_entry = {}
            for key, value in entry.items():
                processed_value = value
                if key in ['sys_updated_by', 'sys_created_by', 'short_description', 'watch_list']:
                    processed_value = anonymize_text(value)
                elif key == 'description':
                    anonymized_value = anonymize_text(value)
                    processed_value = clean_description(anonymized_value)

                # Only add non-empty values to the cleaned entry
                if processed_value != "":
                    anonymized_entry[key] = processed_value
            anonymized_data.append(anonymized_entry)

    if anonymized_data:
        # Log the first cleaned entry for comparison, pretty-printed
        first_entry_json = json.dumps(anonymized_data[0], indent=2)
        logging.info(f"First cleaned entry for comparison:\n{first_entry_json}")

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, 'w') as f:
        json.dump({"records": anonymized_data}, f, indent=2)

    logging.info(f"Anonymized data successfully written to {output_path}")

def main():
    """
    Main function to parse arguments and run the cleaning process.
    """
    parser = argparse.ArgumentParser(description="Clean ServiceNow data.")
    parser.add_argument(
        "--input-path",
        type=str,
        required=True,
        help="Path to the input JSON file."
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=True,
        help="Path to save the cleaned JSON file."
    )
    args = parser.parse_args()

    process_servicenow_data(args.input_path, args.output_path)

if __name__ == '__main__':
    main()