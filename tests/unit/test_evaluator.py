"""Tests for the MLflow custom LLM-judge metric wrapper."""

from unittest.mock import MagicMock, patch
import pandas as pd
from src.evaluation.evaluator import make_llm_judge_metric

@patch("src.evaluation.evaluator.get_llm_provider")
@patch("src.evaluation.evaluator.LLMJudge")
@patch("src.evaluation.evaluator.mlflow")
def test_make_llm_judge_metric(mock_mlflow, mock_llm_judge, mock_get_llm_provider):
    # Arrange
    mock_llm_provider = MagicMock()
    mock_get_llm_provider.return_value = mock_llm_provider

    mock_judge_instance = MagicMock()
    mock_judge_instance.evaluate.return_value = (5, "Great answer!")
    mock_llm_judge.return_value = mock_judge_instance

    # The actual make_metric returns a callable, so we mock it to return a lambda
    # that immediately calls the inner function (eval_fn) for testing purposes.
    mock_mlflow.metrics.make_metric.side_effect = lambda eval_fn, **kwargs: eval_fn

    eval_df = pd.DataFrame({
        "query": ["What is MLflow?"],
        "answer": ["MLflow is an open source platform for managing the end-to-end machine learning lifecycle."],
        "ground_truth": ["MLflow is a platform for the machine learning lifecycle."]
    })
    
    # This global is normally set in main(), so we set it here for the test
    from src.evaluation import evaluator
    evaluator.config = {
        "llm_judge": {
            "llm_provider": "test_provider"
        }
    }
    
    # Act
    llm_judge_metric_func = make_llm_judge_metric()
    result = llm_judge_metric_func(eval_df, {})

    # Assert
    assert result.iloc[0] == 5
    mock_get_llm_provider.assert_called_once_with("test_provider")
    mock_llm_judge.assert_called_once()
    mock_judge_instance.evaluate.assert_called_once()
