import json
import os
import logging
import argparse
from datetime import datetime

# --- Logging Setup ---
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILENAME = os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}_preparation.log")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILENAME),
        logging.StreamHandler()
    ]
)

def prepare_for_embedding(input_path, output_path):
    """
    Reads cleaned ServiceNow data, combines relevant text fields for embedding,
    and saves the result to a JSONL file.
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
        logging.warning(f"No records found in {input_path}. No output file will be generated.")
        return

    prepared_data = []
    for record in records:
        short_desc = record.get('short_description', '')
        desc = record.get('description', '')

        # Combine the text fields
        # Using a clear separator can sometimes help the model distinguish between title and body
        combined_text = f"Title: {short_desc}\n\n{desc}"

        # Store the original incident number as metadata
        metadata = {
            'incident_number': record.get('number', record.get('sys_id', 'N/A'))
        }

        prepared_data.append({
            'text': combined_text.strip(),
            'metadata': metadata
        })

    # Write to a JSONL file
    try:
        with open(output_path, 'w') as f:
            for item in prepared_data:
                f.write(json.dumps(item) + '\n')
        logging.info(f"Data successfully prepared for embedding and written to {output_path}")
    except IOError as e:
        logging.error(f"Error writing to output file {output_path}: {e}")


def main():
    """
    Main function to parse arguments and run the data preparation process.
    """
    parser = argparse.ArgumentParser(description="Prepare ServiceNow data for embedding.")
    parser.add_argument(
        "--input-path",
        type=str,
        required=True,
        help="Path to the cleaned JSON file."
    )
    parser.add_argument(
        "--output-path",
        type=str,
        required=True,
        help="Path to save the prepared JSONL file."
    )
    args = parser.parse_args()

    prepare_for_embedding(args.input_path, args.output_path)

if __name__ == '__main__':
    main()