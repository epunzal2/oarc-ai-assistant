import yaml
import mlflow

def main():
    """
    Registers prompts with the MLflow Prompt Registry.
    """
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