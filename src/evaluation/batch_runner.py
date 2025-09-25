"""Embedding bake-off batch runner.

The runner executes the Phase 3c embedding evaluation sweep by iterating over
embedding models, chunking parameters, and retrieval settings. For each run it
collects retrieval and generation metrics and persists structured outputs for
later analysis.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Tuple

import yaml
from langchain_core.documents import Document
from langchain_text_splitters import TokenTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy

from src.evaluation.llm_judge import LLMJudge
from src.evaluation.model_provider import (
    ModelNotFoundError,
    ModelNotReadyError,
    get_llm_model_path,
    load_embedding_from_spec,
)
from src.rag.data_loader import load_servicenow_documents
from src.rag.llm_provider import get_llm_provider
from src.rag.logger import get_logger
from src.rag.rag_pipeline import create_rag_chain

logger = get_logger(__name__)


@dataclass
class QueryExample:
    query_id: str
    text: str


@dataclass
class Answer:
    query_id: str
    text: str


def load_jsonl(path: str) -> List[Dict[str, Any]]:
    with open(path, "r") as handle:
        return [json.loads(line) for line in handle]


def load_queries(path: str) -> List[QueryExample]:
    return [QueryExample(query_id=entry["id"], text=entry["text"]) for entry in load_jsonl(path)]


def load_answers(path: str) -> Dict[str, Answer]:
    answers = {}
    for entry in load_jsonl(path):
        answers[entry["id"]] = Answer(query_id=entry["id"], text=entry["text"])
    return answers


def load_qrels(path: str) -> Dict[str, List[str]]:
    mapping: Dict[str, List[str]] = {}
    with open(path, "r") as handle:
        for line in handle:
            query_id, _, doc_id, relevance = line.strip().split()
            if int(relevance) <= 0:
                continue
            mapping.setdefault(query_id, []).append(doc_id)
    return mapping


def load_corpus(markdown_dir: str, servicenow_jsonl: str | None) -> List[Document]:
    loader = DirectoryLoader(markdown_dir, glob="**/*.md", show_progress=True)
    documents = loader.load()
    if servicenow_jsonl:
        documents.extend(load_servicenow_documents(servicenow_jsonl))
    logger.info("Loaded %s source documents for evaluation", len(documents))
    return documents


def chunk_documents(documents: Iterable[Document], chunk_size: int, chunk_overlap: int) -> List[Document]:
    # Ensure list realization for stable ordering
    docs_list = list(documents)
    try:
        splitter = TokenTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            encoding_name="cl100k_base",
        )
    except ImportError:
        # Fallback if tiktoken is not installed
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    # Split while preserving each document's metadata
    chunks = splitter.split_documents(docs_list)

    # Build a stable per-document ID mapping to align with qrels-style IDs (doc1..docN)
    def doc_key(md: Dict[str, Any]) -> str:
        # Prefer filesystem source path for markdown docs; fall back to explicit 'id' or a hashable tuple
        return md.get("source") or md.get("id") or md.get("document_id") or "__unknown__"

    key_to_docid: Dict[str, str] = {}
    next_id = 1
    for d in docs_list:
        key = doc_key(getattr(d, "metadata", {}) or {})
        if key not in key_to_docid:
            key_to_docid[key] = f"doc{next_id}"
            next_id += 1

    # Assign chunk_id based on parent document key so all chunks of a document share the same id
    for chunk in chunks:
        chunk.metadata = dict(chunk.metadata)
        key = doc_key(chunk.metadata)
        # Unknowns (e.g., ServiceNow entries without a 'source') get unique IDs after known docs
        if key not in key_to_docid:
            key_to_docid[key] = f"doc{next_id}"
            next_id += 1
        chunk.metadata["chunk_id"] = key_to_docid[key]

    logger.info("Created %s chunks (chunk_size=%s, overlap=%s)", len(chunks), chunk_size, chunk_overlap)
    return chunks


def build_vector_store(chunks: List[Document], embedding_model) -> FAISS:
    return FAISS.from_documents(
        chunks,
        embedding_model,
        distance_strategy=DistanceStrategy.COSINE,
    )


def sanitize_name(name: str) -> str:
    return name.replace("/", "_").replace(" ", "-")


def recall_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    if not relevant:
        return 0.0
    relevant_set = set(relevant)
    retrieved_k = retrieved[:k]
    hits = sum(1 for doc_id in retrieved_k if doc_id in relevant_set)
    return hits / len(relevant_set)


def ndcg_at_k(retrieved: List[str], relevant: List[str], k: int) -> float:
    retrieved_k = retrieved[:k]
    if not retrieved_k or not relevant:
        return 0.0

    dcg = 0.0
    for idx, doc_id in enumerate(retrieved_k):
        rel = 1 if doc_id in relevant else 0
        if rel:
            dcg += (2**rel - 1) / math.log2(idx + 2)

    ideal_hits = min(len(relevant), k)
    if ideal_hits == 0:
        return 0.0
    idcg = sum((2**1 - 1) / math.log2(i + 2) for i in range(ideal_hits))
    if idcg == 0:
        return 0.0
    return dcg / idcg


class BatchRunner:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        dataset_cfg = config["dataset"]
        self.queries = load_queries(dataset_cfg["queries_path"])
        self.answers = load_answers(dataset_cfg["answers_path"])
        self.qrels = load_qrels(dataset_cfg["qrels_path"])
        self.corpus = load_corpus(
            dataset_cfg["document_source"]["markdown_dir"],
            dataset_cfg["document_source"].get("servicenow_jsonl"),
        )
        runtime_cfg = config.get("runtime", {})

        max_queries = runtime_cfg.get("max_queries")
        if max_queries is not None and max_queries > 0:
            original_count = len(self.queries)
            self.queries = self.queries[:max_queries]
            logger.info(
                "Limiting queries from %s to %s for this run", original_count, len(self.queries)
            )

        self.persist_responses = runtime_cfg.get("persist_responses", True)

        self.output_dir = config["experiment"]["output_dir"]
        self.per_run_metrics_path = os.path.join(
            self.output_dir, config["experiment"]["per_run_metrics_file"]
        )
        self.summary_path = os.path.join(
            self.output_dir, config["experiment"]["summary_file"]
        )
        self.detailed_dir = os.path.join(
            self.output_dir, config["experiment"].get("detailed_results_dir", "runs")
        )
        self.retrieval_k = config["frozen"]["metrics"]["retrieval_k"]
        self.generator_config = config["frozen"]["generator"]
        self.judge_config = config["judge"]
        self._generator_llm = None
        self._judge = None

        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.detailed_dir, exist_ok=True)

    def _get_generator_llm(self):
        if self._generator_llm is not None:
            return self._generator_llm
        provider_name = self.generator_config["provider"]
        model_path = get_llm_model_path(self.generator_config["llm_name"])
        temperature = self.generator_config.get("temperature", 0.0)
        max_new_tokens = self.generator_config.get("max_new_tokens", 256)
        # Increase context window to accommodate retrieved context + prompt + generation
        n_ctx = self.generator_config.get("n_ctx", 4096)
        n_batch = self.generator_config.get("n_batch", 512)
        self._generator_llm = get_llm_provider(
            provider_name,
            model_path=model_path,
            temperature=temperature,
            max_tokens=max_new_tokens,
            n_ctx=n_ctx,
            n_batch=n_batch,
        ).get_llm()
        return self._generator_llm

    def _get_judge(self) -> LLMJudge:
        if self._judge is not None:
            return self._judge
        provider = get_llm_provider(
            self.judge_config["provider"],
            model_path=get_llm_model_path(self.judge_config["llm_name"]),
            temperature=0.0,
            max_tokens=256,
            n_ctx=self.judge_config.get("n_ctx", 4096),
            n_batch=self.judge_config.get("n_batch", 512),
        )
        self._judge = LLMJudge(self.judge_config, provider)
        return self._judge

    def iter_runs(self):
        sweep_cfg = self.config["sweeps"]
        for embedding_spec, chunk_size, chunk_overlap, top_k in itertools.product(
            sweep_cfg["embedding_models"],
            sweep_cfg["chunk_size"],
            sweep_cfg["chunk_overlap"],
            sweep_cfg["top_k"],
        ):
            yield embedding_spec, chunk_size, chunk_overlap, top_k

    def run(self) -> Dict[str, Any]:
        logger.info("Starting embedding bake-off sweep")
        per_run_summary = []
        with open(self.per_run_metrics_path, "w") as metrics_stream:
            for embedding_spec, chunk_size, chunk_overlap, top_k in self.iter_runs():
                run_result = self._run_single(embedding_spec, chunk_size, chunk_overlap, top_k)
                metrics_stream.write(json.dumps(run_result) + "\n")
                per_run_summary.append(run_result)

        best = sorted(
            per_run_summary,
            key=lambda x: (x["metrics"]["recall@10"], x["metrics"]["ndcg@10"], x["metrics"]["faithfulness"]),
            reverse=True,
        )
        summary = {
            "total_runs": len(per_run_summary),
            "best_run_id": best[0]["run_id"] if best else None,
            "runs": per_run_summary,
        }
        with open(self.summary_path, "w") as summary_stream:
            json.dump(summary, summary_stream, indent=2)
        logger.info("Sweep complete. Results written to %s", self.summary_path)
        return summary

    def _run_single(
        self,
        embedding_spec: Dict[str, Any],
        chunk_size: int,
        chunk_overlap: int,
        top_k: int,
    ) -> Dict[str, Any]:
        run_id = f"{sanitize_name(embedding_spec['name'])}_cs{chunk_size}_co{chunk_overlap}_k{top_k}"
        logger.info("Running configuration %s", run_id)

        try:
            embedding_model = load_embedding_from_spec(embedding_spec)
        except (ModelNotFoundError, ModelNotReadyError) as exc:
            logger.error("Skipping %s: %s", run_id, exc)
            return {
                "run_id": run_id,
                "status": "skipped",
                "reason": str(exc),
            }

        chunks = chunk_documents(self.corpus, chunk_size, chunk_overlap)
        vector_store = build_vector_store(chunks, embedding_model)
        retriever = vector_store.as_retriever(search_kwargs={"k": top_k})

        rag_chain = create_rag_chain(
            llm=self._get_generator_llm(),
            retriever=retriever,
        )

        judge = self._get_judge()
        hallucination_threshold = self.judge_config.get("hallucination_threshold", 2)

        responses = []
        retrieval_scores: List[Tuple[str, List[str]]] = []
        judge_scores: List[int] = []
        hallucination_count = 0

        for query in self.queries:
            result = rag_chain.invoke(query.text)
            context_docs: List[Document] = result.get("context", [])
            doc_ids = [doc.metadata.get("chunk_id") for doc in context_docs]
            contexts = [doc.page_content for doc in context_docs]
            answer = result.get("answer", "")
            ground_truth = self.answers.get(query.query_id)
            judge_score, justification = judge.evaluate(
                question=query.text,
                answer=answer,
                ground_truth=ground_truth.text if ground_truth else "",
            )
            judge_scores.append(judge_score)
            if judge_score <= hallucination_threshold:
                hallucination_count += 1

            responses.append(
                {
                    "query_id": query.query_id,
                    "question": query.text,
                    "answer": answer,
                    "ground_truth": ground_truth.text if ground_truth else "",
                    "retrieved_doc_ids": doc_ids,
                    "retrieved_context": contexts,
                    "judge_score": judge_score,
                    "judge_justification": justification,
                }
            )
            retrieval_scores.append((query.query_id, doc_ids))

        metrics = self._compute_metrics(retrieval_scores, judge_scores, hallucination_count, len(responses))

        run_payload = {
            "run_id": run_id,
            "status": "completed",
            "configuration": {
                "embedding": embedding_spec,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
                "top_k": top_k,
            },
            "metrics": metrics,
        }

        run_dir = os.path.join(self.detailed_dir, run_id)
        os.makedirs(run_dir, exist_ok=True)

        if self.persist_responses:
            with open(os.path.join(run_dir, "responses.jsonl"), "w") as handle:
                for response in responses:
                    handle.write(json.dumps(response) + "\n")

        with open(os.path.join(run_dir, "metrics.json"), "w") as handle:
            json.dump(run_payload, handle, indent=2)

        logger.info("Finished run %s", run_id)
        return run_payload

    def _compute_metrics(
        self,
        retrieval_scores: List[Tuple[str, List[str]]],
        judge_scores: List[int],
        hallucination_count: int,
        total_examples: int,
    ) -> Dict[str, Any]:
        recall_total = 0.0
        ndcg_total = 0.0
        for query_id, doc_ids in retrieval_scores:
            relevant = self.qrels.get(query_id, [])
            recall_total += recall_at_k(doc_ids, relevant, self.retrieval_k)
            ndcg_total += ndcg_at_k(doc_ids, relevant, self.retrieval_k)

        examples = len(retrieval_scores)
        mean_recall = recall_total / examples if examples else 0.0
        mean_ndcg = ndcg_total / examples if examples else 0.0

        mean_judge = sum(judge_scores) / len(judge_scores) if judge_scores else 0.0
        faithfulness_threshold = self.judge_config.get("faithfulness_threshold", 4)
        faithful = sum(1 for score in judge_scores if score >= faithfulness_threshold)

        return {
            "recall@10": round(mean_recall, 4),
            "ndcg@10": round(mean_ndcg, 4),
            "faithfulness": round(faithful / total_examples if total_examples else 0.0, 4),
            "hallucination_rate": round(hallucination_count / total_examples if total_examples else 0.0, 4),
            "mean_judge_score": round(mean_judge, 4),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the embedding bake-off evaluation sweep.")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the Phase 3c embedding bake-off configuration file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with open(args.config, "r") as handle:
        config = yaml.safe_load(handle)
    runner = BatchRunner(config)
    runner.run()


if __name__ == "__main__":
    main()
