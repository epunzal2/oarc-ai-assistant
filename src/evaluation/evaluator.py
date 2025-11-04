# src/evaluation/evaluator.py

import argparse
import json
from pathlib import Path

import yaml

from src.evaluation.llm_judge import LLMJudge
from src.rag import mlflow_tracker
from src.rag.llm_provider import get_llm_provider


def _hash_file(path: str) -> str:
    try:
        content = Path(path).read_text(encoding="utf-8")
    except Exception:
        return "unknown"
    return mlflow_tracker.hash_text(content)

def calculate_metrics(results, qrels):
    """
    Calculates retrieval metrics.
    """
    recall_at_5 = 0
    precision_at_5 = 0
    llm_judge_scores = []

    for result in results:
        query_id = result["query_id"]
        retrieved_docs = result["retrieved_docs"]
        relevant_docs = qrels.get(query_id, [])

        retrieved_set = set(retrieved_docs)
        relevant_set = set(relevant_docs)

        true_positives = len(retrieved_set.intersection(relevant_set))

        if "llm_judge_score" in result:
            llm_judge_scores.append(result["llm_judge_score"])

        if relevant_docs:
            recall_at_5 += true_positives / len(relevant_docs)
        
        if retrieved_docs:
            precision_at_5 += true_positives / len(retrieved_docs)

    return {
        "recall@5": recall_at_5 / len(results) if results else 0,
        "precision@5": precision_at_5 / len(results) if results else 0,
        "mean_llm_judge_score": sum(llm_judge_scores) / len(llm_judge_scores) if llm_judge_scores else 0,
    }

def load_qrels(qrels_path):
    """
    Loads qrels from a TSV file.
    """
    qrels = {}
    with open(qrels_path, "r") as f:
        for line in f:
            query_id, _, doc_id, _ = line.strip().split()
            if query_id not in qrels:
                qrels[query_id] = []
            qrels[query_id].append(doc_id)
    return qrels

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
        config = yaml.safe_load(f)

    llm_provider = get_llm_provider(config["llm_judge"]["llm_provider"])
    llm_judge = LLMJudge(config["llm_judge"], llm_provider)

    results = []
    with open(args.results_path, "r") as f:
        for line in f:
            result = json.loads(line)
            score, justification = llm_judge.evaluate(
                question=result["query"],
                answer=result["answer"],
                ground_truth=result["ground_truth"],
            )
            result["llm_judge_score"] = score
            result["llm_judge_justification"] = justification
            results.append(result)

    qrels = load_qrels(args.qrels_path)
    metrics = calculate_metrics(results, qrels)

    artifact_top_k = mlflow_tracker.config.MLFLOW.artifact_top_k
    sanitized_results = mlflow_tracker.sanitize_records(
        results,
        top_k=artifact_top_k,
        include_answer=True,
    )
    rag_provider = config.get("rag_pipeline", {}).get("llm_provider", "unknown")
    embedding_model = config.get("embedding_model", "unknown")
    corpus_hash = _hash_file(args.qrels_path)
    prompt_version = mlflow_tracker.hash_text(config.get("llm_judge", {}).get("prompt", ""))
    retriever_version = mlflow_tracker.hash_text(embedding_model)
    run_name = f"eval:{Path(args.results_path).stem}"
    tags = {
        "run_type": "evaluation",
        "provider": rag_provider,
        "model": embedding_model,
        "index_version": corpus_hash,
        "prompt_version": prompt_version,
        "retriever_version": retriever_version,
        "corpus_hash": corpus_hash,
    }
    with mlflow_tracker.start_run(run_name=run_name, tags=tags):
        mlflow_tracker.log_params(
            {
                "results_path": args.results_path,
                "qrels_path": args.qrels_path,
                "output_path": args.output_path,
                "num_results": len(results),
            }
        )
        mlflow_tracker.log_metrics(metrics)
        mlflow_tracker.log_jsonl(sanitized_results, "evaluation/responses.jsonl")
        mlflow_tracker.log_dict(metrics, "evaluation/metrics.json")
        prompt_template = config.get("llm_judge", {}).get("prompt")
        if prompt_template:
            mlflow_tracker.log_text(prompt_template, "evaluation/prompt_template.txt")
        retriever_config = {
            "embedding_model": embedding_model,
            "rag_pipeline": config.get("rag_pipeline", {}),
        }
        mlflow_tracker.log_dict(retriever_config, "evaluation/retriever_config.json")

    with open(args.output_path, "w") as f:
        json.dump(metrics, f, indent=4)

    print(f"Evaluation complete. Metrics saved to {args.output_path}")
    print(json.dumps(metrics, indent=4))

if __name__ == "__main__":
    main()
