import argparse

import yaml

from src.evaluation.batch_runner import BatchRunner

DEFAULT_CONFIG = "configs/evaluation/embedding_bakeoff.yml"

def main(config_path: str):
    """
    Main function to run the batch evaluation.

    Args:
        config_path (str): Path to the evaluation configuration file.
    """
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    batch_runner = BatchRunner(config)
    batch_runner.run()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run RAG pipeline evaluation.")
    parser.add_argument(
        "--config",
        type=str,
        default=DEFAULT_CONFIG,
        help=f"Path to the evaluation configuration file (default: {DEFAULT_CONFIG}).",
    )
    args = parser.parse_args()
    main(args.config)
