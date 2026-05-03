"""Register evaluation prompts in the configured MLflow Prompt Registry."""

import yaml
import mlflow

def main():
    """Read the default evaluation config and register the judge prompt."""

    with open("configs/evaluation/default.yml", "r") as f:
        config = yaml.safe_load(f)

    llm_judge_prompt = config["llm_judge"]["prompt"]

    mlflow.register_prompt(
        "llm_judge",
        llm_judge_prompt,
    )

    print("Prompts registered successfully.")

if __name__ == "__main__":
    main()
