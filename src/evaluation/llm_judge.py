import json
from typing import Any, Dict, Tuple

from src.rag.llm_provider import LlmProvider


class LLMJudge:
    """
    A class to evaluate the quality of a generated answer using a language model.
    """

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
        """Loads the prompt template from the config."""
        # This will be expanded to load from a file or a more complex structure
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
        prompt = self.prompt_template.format(
            question=question, answer=answer, ground_truth=ground_truth
        )
        response = self.llm_provider.get_completion(prompt)

        try:
            # Assuming the LLM returns a JSON string with "score" and "justification"
            result = json.loads(response)
            score = int(result.get("score", 0))
            justification = result.get("justification", "")
            return score, justification
        except (json.JSONDecodeError, ValueError):
            # Handle cases where the LLM output is not as expected
            return 0, response
