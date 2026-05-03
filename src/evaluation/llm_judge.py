"""LLM-as-judge helper used by evaluation sweeps and MLflow metrics."""

import json
import re
from typing import Any, Dict, Tuple

from src.rag.llm_provider import LlmProvider


class LLMJudge:
    """Evaluate generated answers against ground truth with a scoring LLM."""

    def __init__(self, config: Dict[str, Any], llm_provider: LlmProvider):
        """
        Initializes the LLMJudge.

        Args:
            config (Dict[str, Any]): The configuration for the LLM-as-Judge.
            llm_provider (LlmProvider): The language model provider.
        """
        self.config = config
        self.llm_provider = llm_provider
        self.prompt_template = self._load_prompt_template()

    def _load_prompt_template(self) -> str:
        """Load the prompt template string from the provided config."""

        return self.config.get(
            "prompt",
            "Evaluate the following answer on a scale of 1-5. Question: {question} Answer: {answer} Ground Truth: {ground_truth}",
        )

    def evaluate(
        self, question: str, answer: str, ground_truth: str
    ) -> Tuple[int, str]:
        """
        Evaluates the quality of a generated answer.

        Args:
            question (str): The question that was asked.
            answer (str): The generated answer.
            ground_truth (str): The ground-truth answer.

        Returns:
            Tuple[int, str]: A tuple containing the score (1-5) and a justification.
        """
        # Render prompt without invoking str.format on arbitrary JSON braces.
        # We only replace the three known placeholders.
        prompt = (
            self.prompt_template
            .replace("{question}", question)
            .replace("{answer}", answer)
            .replace("{ground_truth}", ground_truth)
        )
        response = self.llm_provider.get_completion(prompt)

        # Judge models sometimes wrap JSON in prose or code fences; keep parsing
        # tolerant while still returning a bounded numeric score.
        obj = None
        # 1) Direct JSON
        try:
            maybe = json.loads(response)
            if isinstance(maybe, dict):
                obj = maybe
        except Exception:
            pass

        # 2) Extract from ```json ... ``` code block
        if obj is None:
            m = re.search(r"```json\s*(.*?)\s*```", response, flags=re.DOTALL | re.IGNORECASE)
            if m:
                block = m.group(1)
                try:
                    obj = json.loads(block)
                except Exception:
                    obj = None

        # 3) Fallback: first {...} that parses
        if obj is None:
            start = response.find("{")
            end = response.rfind("}")
            if start != -1 and end != -1 and end > start:
                # Try progressively to parse shorter endings if large
                for r in range(end, start + 1, -1):
                    try:
                        obj = json.loads(response[start : r + 1])
                        if isinstance(obj, dict):
                            break
                    except Exception:
                        continue

        if isinstance(obj, dict):
            try:
                score = int(obj.get("score", 0))
            except Exception:
                score = 0
            # clamp 0..5
            score = max(0, min(5, score))
            justification = obj.get("justification", "")
            # Normalize justification to string
            if not isinstance(justification, str):
                justification = str(justification)
            return score, justification

        # Parsing failed; return raw response for visibility
        return 0, response
