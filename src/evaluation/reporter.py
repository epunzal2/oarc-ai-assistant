# src/evaluation/reporter.py

import argparse
import json

def generate_text_report(metrics):
    """
    Generates a simple text-based report.
    """
    report = "Evaluation Report\n"
    report += "=================\n\n"
    for key, value in metrics.items():
        report += f"{key}: {value:.4f}\n"
    return report

def main():
    """
    Main function to generate reports from evaluation results.
    """
    parser = argparse.ArgumentParser(description="Generate reports from evaluation results.")
    parser.add_argument("--metrics_path", type=str, required=True, help="Path to the evaluation metrics file in JSON format.")
    parser.add_argument("--output_path", type=str, required=True, help="Path to save the report.")
    args = parser.parse_args()

    with open(args.metrics_path, "r") as f:
        metrics = json.load(f)

    report = generate_text_report(metrics)

    with open(args.output_path, "w") as f:
        f.write(report)

    print(f"Report generated successfully. Saved to {args.output_path}")
    print("\n" + report)

if __name__ == "__main__":
    main()