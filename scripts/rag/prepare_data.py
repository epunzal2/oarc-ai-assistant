import os
import json
import csv
import re
from typing import List, Dict, Any

from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

def load_data(file_path: str) -> List[Dict[str, Any]]:
    """Loads ticket data from a JSON or CSV file."""
    if file_path.endswith('.json'):
        with open(file_path, 'r') as f:
            return json.load(f)
    elif file_path.endswith('.csv'):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            return [row for row in reader]
    else:
        raise ValueError("Unsupported file format. Please use JSON or CSV.")

def filter_tickets(tickets: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Filters out irrelevant tickets based on keywords."""
    irrelevant_keywords = ['account creation', 'password reset']
    relevant_tickets = []
    for ticket in tickets:
        # Assuming ticket content is in a 'description' field.
        description = ticket.get('description', '').lower()
        if not any(keyword in description for keyword in irrelevant_keywords):
            relevant_tickets.append(ticket)
    return relevant_tickets

def anonymize_pii(text: str) -> str:
    """
    Anonymizes Personally Identifiable Information (PII) in the text
    using Microsoft Presidio.
    """
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()

    # Analyze the text for PII entities.
    analyzer_results = analyzer.analyze(text=text, language='en')

    # Anonymize the detected entities.
    anonymized_text = anonymizer.anonymize(
        text=text,
        analyzer_results=analyzer_results
    )

    return anonymized_text.text

def format_for_rag(ticket: Dict[str, Any]) -> str:
    """Formats a ticket into a markdown document for the RAG pipeline."""
    # Customize this based on the actual ticket fields.
    title = ticket.get('short_description', 'No Title')
    description = ticket.get('description', 'No Description')
    resolution = ticket.get('resolution', 'No Resolution')

    # Anonymize content before formatting.
    description = anonymize_pii(description)
    resolution = anonymize_pii(resolution)

    markdown_content = f"# {title}\n\n"
    markdown_content += f"## Description\n\n{description}\n\n"
    markdown_content += f"## Resolution\n\n{resolution}\n"
    return markdown_content

def main():
    """Main function to process the ticket data."""
    # Create a dummy data file for testing.
    dummy_data = [
        {"short_description": "HPC job failing", "description": "My job on the cluster is failing. My username is testuser and my email is testuser@example.com.", "resolution": "Increased memory allocation for the job."},
        {"short_description": "Account creation request", "description": "Please create an account for newuser.", "resolution": "Account created."},
        {"short_description": "Software installation", "description": "Please install gromacs on the cluster. My IP is 192.168.1.1.", "resolution": "Gromacs has been installed."},
    ]
    dummy_file = 'dummy_tickets.json'
    with open(dummy_file, 'w') as f:
        json.dump(dummy_data, f)

    # Process the data.
    tickets = load_data(dummy_file)
    relevant_tickets = filter_tickets(tickets)

    output_dir = 'rag_documents'
    os.makedirs(output_dir, exist_ok=True)

    for i, ticket in enumerate(relevant_tickets):
        markdown_content = format_for_rag(ticket)
        output_file = os.path.join(output_dir, f'ticket_{i+1}.md')
        with open(output_file, 'w') as f:
            f.write(markdown_content)

    print(f"Processed {len(relevant_tickets)} tickets and saved them to '{output_dir}'.")

    # Clean up the dummy file.
    os.remove(dummy_file)

if __name__ == '__main__':
    main()