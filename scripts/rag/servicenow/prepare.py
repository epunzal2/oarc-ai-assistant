"""Prepare cleaned ServiceNow records as JSONL documents for embeddings."""

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
    """Combine cleaned ticket text fields and write LangChain-friendly JSONL."""

    try:
        with open(input_path, 'r') as f:
            raw_data = json.load(f)
    except FileNotFoundError:
        logging.error(f"Error: Input file not found at {input_path}")
        return
    except json.JSONDecodeError:
        logging.error(f"Error: Could not decode JSON from {input_path}")
        return

    if isinstance(raw_data, dict) and 'records' in raw_data:
        records = raw_data.get('records', [])
    elif isinstance(raw_data, list):
        records = raw_data
    elif isinstance(raw_data, dict):
        records = [raw_data]
    else:
        logging.warning(
            "Input JSON at %s did not match expected structure (dict/list); no data prepared.",
            input_path
        )
        records = []

    if not records:
        logging.warning(f"No records found in {input_path}. No output file will be generated.")
        return

    prepared_data = []
    for record in records:
        short_desc = record.get('short_description', '') or ''
        desc = record.get('description', '') or ''

        sections = []
        short_desc = short_desc.strip()
        desc = desc.strip()
        if short_desc:
            sections.append(f"Title: {short_desc}")
        if desc:
            sections.append(desc)

        for label, field in [('Comments', 'comments'),
                             ('Close Notes', 'close_notes'),
                             ('Work Notes', 'work_notes')]:
            value = (record.get(field) or '').strip()
            if value:
                sections.append(f"{label}: {value}")

        combined_text = '\n\n'.join(sections).strip()
        if not combined_text:
            logging.debug(
                "Skipping incident %s because no textual content remained after cleaning.",
                record.get('number', record.get('sys_id', 'UNKNOWN'))
            )
            continue

        metadata = {
            'incident_number': record.get('number', record.get('sys_id', 'N/A')),
            'state': record.get('state'),
            'priority': record.get('priority'),
            'impact': record.get('impact'),
            'urgency': record.get('urgency'),
            'contact_type': record.get('contact_type'),
            'knowledge': record.get('knowledge'),
            'opened_at': record.get('opened_at'),
            'closed_at': record.get('closed_at'),
            'sys_created_on': record.get('sys_created_on'),
            'sys_updated_on': record.get('sys_updated_on'),
            'category': record.get('category'),
            'subcategory': record.get('subcategory'),
            'service_offering': record.get('service_offering'),
            'business_service': record.get('business_service'),
            'location': record.get('location')
        }
        metadata = {k: v for k, v in metadata.items() if v not in (None, '', [])}

        prepared_data.append({
            'text': combined_text.strip(),
            'metadata': metadata
        })

    if not prepared_data:
        logging.warning(
            "No records from %s produced usable text. Output file will not be created.",
            input_path
        )
        return

    # Write to a JSONL file
    try:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        with open(output_path, 'w') as f:
            for item in prepared_data:
                f.write(json.dumps(item) + '\n')
        logging.info(f"Data successfully prepared for embedding and written to {output_path}")
    except IOError as e:
        logging.error(f"Error writing to output file {output_path}: {e}")


def main():
    """
    CLI entry point for preparing ServiceNow data for embeddings.
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
