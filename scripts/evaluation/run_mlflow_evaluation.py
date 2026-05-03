"""Run saved-result evaluation inside an explicit MLflow run."""

import argparse
import mlflow
from src.evaluation.evaluator import main as run_evaluation

def main():
    """Parse result/qrels paths, start MLflow, and delegate to evaluator."""

    parser = argparse.ArgumentParser(description="Run RAG pipeline evaluation with MLflow.")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/evaluation/default.yml",
        help="Path to the evaluation configuration file.",
    )
    parser.add_argument(
        "--results",
        type=str,
        required=True,
        help="Path to the results file in JSONL format.",
    )
    parser.add_argument(
        "--qrels",
        type=str,
        required=True,
        help="Path to the qrels file in TSV format.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to save the evaluation metrics.",
    )
    args = parser.parse_args()

    with mlflow.start_run():
        mlflow.log_param("config_path", args.config)
        mlflow.log_param("results_path", args.results)
        mlflow.log_param("qrels_path", args.qrels)
        mlflow.log_param("output_path", args.output)

        run_evaluation_args = [
            "--config_path",
            args.config,
            "--results_path",
            args.results,
            "--qrels_path",
            args.qrels,
            "--output_path",
            args.output,
        ]

        # This is a bit of a hack to run the evaluator script with arguments
        import sys
        original_argv = sys.argv
        sys.argv = [""] + run_evaluation_args
        run_evaluation()
        sys.argv = original_argv

if __name__ == "__main__":
    main()
