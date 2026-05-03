"""Clean and anonymize approved ServiceNow exports before embedding.

The script reads an operator-supplied JSON export, keeps only selected fields,
normalizes choice/boolean values, redacts common PII patterns, and writes a
cleaned JSON file under the requested output path.
"""

import json
import re
import os
import logging
import argparse
from datetime import datetime
from typing import Any, Dict

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


FIELDS_TO_KEEP = {
    'number',
    'sys_id',
    'short_description',
    'description',
    'comments',
    'close_notes',
    'work_notes',
    'contact_type',
    'category',
    'subcategory',
    'service_offering',
    'business_service',
    'state',
    'priority',
    'impact',
    'urgency',
    'knowledge',
    'opened_at',
    'closed_at',
    'sys_created_on',
    'sys_updated_on',
    'due_date',
    'sla_due',
    'reassignment_count',
    'sys_mod_count',
    'location'
}

BOOLEAN_FIELDS = {'knowledge'}

CHOICE_FIELD_LABELS: Dict[str, Dict[str, str]] = {
    'state': {
        '1': 'New',
        '2': 'In Progress',
        '3': 'On Hold',
        '4': 'Resolved',
        '5': 'Closed',
        '6': 'Cancelled',
        '7': 'Pending'
    },
    'priority': {
        '1': '1 - Critical',
        '2': '2 - High',
        '3': '3 - Moderate',
        '4': '4 - Low',
        '5': '5 - Planning'
    },
    'impact': {
        '1': '1 - High',
        '2': '2 - Medium',
        '3': '3 - Low'
    },
    'urgency': {
        '1': '1 - High',
        '2': '2 - Medium',
        '3': '3 - Low'
    },
    'contact_type': {
        'phone': 'Phone',
        'email': 'Email',
        'self-service': 'Self-service',
        'walk-in': 'Walk-in'
    }
}


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
    text = re.sub(r'\b[a-z]{2,3}\d{3,4}\b', '[USER]', text)  # e.g., rm1238, yw969, so398
    text = re.sub(r'\bpgarias\b', '[USER]', text)  # specific user from sample
    text = re.sub(r'\bthackray\b', '[USER]', text)  # specific user from sample

    # Generalize file paths
    text = re.sub(r'\/projects\/f_[a-z0-9]+_\d', '/projects/[USER_PROJECT]', text)

    # Generalize cluster hostnames
    text = re.sub(r'amarel\.rutgers\.edu', '[CLUSTER_HOSTNAME]', text)

    # Remove mailto anchors that often duplicate emails
    text = re.sub(r'<mailto:[^>]+>', '', text)

    # Remove or generalize URLs
    text = re.sub(r'https?:\/\/\S+', '[URL]', text)

    # Unescape common escaped characters
    text = text.replace('\\/', '/')

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

    # Remove common email header fragments
    text = re.sub(r'(?im)^received from:.*$', '', text)
    text = re.sub(r'(?im)^originally sent from:.*$', '', text)
    text = re.sub(r'(?im)^from:.*$', '', text)
    text = re.sub(r'(?im)^sent:.*$', '', text)
    text = re.sub(r'(?im)^to:.*$', '', text)
    text = re.sub(r'(?im)^subject:.*$', '', text)

    # Collapse repeated blank lines while retaining paragraph breaks
    lines = []
    for raw_line in text.splitlines():
        normalized_line = re.sub(r'\s+', ' ', raw_line).strip()
        if normalized_line:
            lines.append(normalized_line)

    signoff_prefixes = (
        'thanks',
        'thank you',
        'regards',
        'cheers',
        'sincerely',
        'best',
        'best regards'
    )
    while lines and any(lines[-1].lower().startswith(prefix) for prefix in signoff_prefixes):
        lines.pop()

    if lines and re.fullmatch(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', lines[-1]):
        lines[-1] = '[NAME]'

    text = '\n'.join(lines)

    # Normalize whitespace
    text = text.strip()

    return text


def normalize_boolean(value: Any) -> Any:
    """Normalize ServiceNow boolean strings while preserving unknown values."""

    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.lower()
        if lowered == 'true':
            return True
        if lowered == 'false':
            return False
    return value


def map_choice_value(field: str, value: Any) -> Any:
    """Map known ServiceNow choice codes to human-readable labels."""

    if not isinstance(value, str):
        return value
    mapping = CHOICE_FIELD_LABELS.get(field)
    if not mapping:
        return value
    key = value.strip()
    return mapping.get(key, mapping.get(key.lower(), value))


def should_keep_field(field: str) -> bool:
    """Return whether a ServiceNow field participates in the prepared corpus."""

    return field in FIELDS_TO_KEEP


def process_servicenow_data(input_path, output_path):
    """
    Reads ServiceNow data from JSON, anonymizes and cleans it, and writes the cleaned
    data to a new file wrapped in a ``records`` list.
    """
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
        possible_records = raw_data.get('records', [])
    elif isinstance(raw_data, list):
        possible_records = raw_data
    elif isinstance(raw_data, dict):
        possible_records = [raw_data]
    else:
        logging.warning(
            "Input JSON at %s did not match expected structure (dict/list); nothing to clean.",
            input_path
        )
        possible_records = []

    if not possible_records:
        logging.warning(f"No records found in {input_path}. Writing an empty records file.")
        anonymized_data = []
    else:
        anonymized_data = []
        for entry in possible_records:
            anonymized_entry = {}
            for key, value in entry.items():
                if not should_keep_field(key):
                    continue

                processed_value = value
                if key in ['short_description', 'comments', 'close_notes', 'work_notes']:
                    processed_value = anonymize_text(value)
                elif key == 'description':
                    anonymized_value = anonymize_text(value)
                    processed_value = clean_description(anonymized_value)
                elif key in BOOLEAN_FIELDS:
                    processed_value = normalize_boolean(value)

                processed_value = map_choice_value(key, processed_value)

                # Only add non-empty values to the cleaned entry
                if processed_value not in ("", None):
                    anonymized_entry[key] = processed_value
            anonymized_data.append(anonymized_entry)

    if anonymized_data:
        # Log the first cleaned entry for comparison, pretty-printed
        first_entry_json = json.dumps(anonymized_data[0], indent=2)
        logging.info(f"First cleaned entry for comparison:\n{first_entry_json}")

    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir) and output_dir:
        os.makedirs(output_dir)

    output_payload: Dict[str, Any] = {"records": anonymized_data}
    with open(output_path, 'w') as f:
        json.dump(output_payload, f, indent=2)

    logging.info(f"Anonymized data successfully written to {output_path}")


def main():
    """
    CLI entry point for cleaning ServiceNow incident data.
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
