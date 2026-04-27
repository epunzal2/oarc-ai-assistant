# src/evaluation/evaluator.py

import argparse
import json
import yaml
import pandas as pd
from src.evaluation.llm_judge import LLMJudge
from src.rag.llm_provider import get_llm_provider

mlflow = None


def _get_mlflow():
    global mlflow
    if mlflow is None:
        import mlflow as mlflow_module

        mlflow = mlflow_module
    return mlflow


def make_llm_judge_metric():
    mlflow_client = _get_mlflow()

    def llm_judge_metric(eval_df, builtin_metrics):
        llm_provider = get_llm_provider(config["llm_judge"]["llm_provider"])
        prompt = mlflow_client.get_prompt("llm_judge")
        llm_judge = LLMJudge({"prompt": prompt}, llm_provider)
        scores = []
        for index, row in eval_df.iterrows():
            score, justification = llm_judge.evaluate(
                question=row["query"],
                answer=row["answer"],
                ground_truth=row["ground_truth"],
            )
            scores.append(score)
        return pd.Series(scores, index=eval_df.index)

    return mlflow_client.metrics.make_metric(
        eval_fn=llm_judge_metric,
        greater_is_better=True,
        name="llm_judge_score",
    )

def main():
    """
    Main function to evaluate the results of a RAG pipeline run.
    """
    parser = argparse.ArgumentParser(description="Evaluate the results of a RAG pipeline run.")
    parser.add_argument("--results_path", type=str, required=True, help="Path to the results file in JSONL format.")
    parser.add_argument("--qrels_path", type=str, required=True, help="Path to the qrels file in TSV format.")
    parser.add_argument("--output_path", type=str, required=True, help="Path to save the evaluation metrics.")
    parser.add_argument("--config_path", type=str, default="configs/evaluation/default.yml", help="Path to the evaluation config file.")
    args = parser.parse_args()

    with open(args.config_path, "r") as f:
        global config
        config = yaml.safe_load(f)

    results_df = pd.read_json(args.results_path, lines=True)
    qrels_df = pd.read_csv(args.qrels_path, sep=" ", header=None, names=["query_id", "corpus_id", "score"])

    mlflow_client = _get_mlflow()
    with mlflow_client.start_run():
        mlflow_client.log_params(config)
        results = mlflow_client.evaluate(
            data=results_df,
            targets="ground_truth",
            predictions="answer",
            extra_metrics=[make_llm_judge_metric()],
            evaluators="default",
        )
        
        # Log the results to a file
        with open(args.output_path, "w") as f:
            json.dump(results.metrics, f, indent=4)

        print(f"Evaluation complete. Metrics saved to {args.output_path}")
        print(json.dumps(results.metrics, indent=4))

if __name__ == "__main__":
    main()
