import os
from typing import Any, Dict

import yaml
from langchain_community.embeddings import HuggingFaceBgeEmbeddings, HuggingFaceEmbeddings


class ModelNotFoundError(ValueError):
    """Raised when a model is missing from the local registry."""


class ModelNotReadyError(FileNotFoundError):
    """Raised when a model is declared in the registry but not present on disk."""

def get_model_config():
    """Loads the model registry configuration."""
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'configs', 'models.yml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_embedding_model(model_name: str):
    """
    Loads an embedding model from the local registry.

    Args:
        model_name: The name of the model to load (e.g., "bge-large-en-v1.5").

    Returns:
        An instance of a LangChain embedding model.
    """
    config = get_model_config()
    model_info = next((m for m in config.get('embedding_models', []) if m['name'] == model_name), None)

    if not model_info:
        raise ModelNotFoundError(f"Model '{model_name}' not found in the registry.")

    local_path = model_info['local_dir']
    langchain_class_name = model_info['langchain_class']

    if not os.path.exists(local_path):
        raise ModelNotReadyError(
            f"Model directory not found at '{local_path}'. Please run the download script."
        )

    # Dynamically instantiate the correct LangChain class
    if langchain_class_name == "HuggingFaceBgeEmbeddings":
        model_cls = HuggingFaceBgeEmbeddings
    elif langchain_class_name == "HuggingFaceEmbeddings":
        model_cls = HuggingFaceEmbeddings
    else:
        raise ValueError(f"Unsupported LangChain class: {langchain_class_name}")

    # All sentence-transformer models expect the local path in `model_name`
    return model_cls(model_name=local_path)


def get_llm_model_path(llm_name: str) -> str:
    """Returns the absolute path to a locally managed LLM binary."""
    config = get_model_config()
    model_info = next((m for m in config.get("llms", []) if m["name"] == llm_name), None)
    if not model_info:
        raise ModelNotFoundError(f"LLM '{llm_name}' not found in the registry.")

    model_path = os.path.join(model_info["local_dir"], model_info["filename"])
    if not os.path.exists(model_path):
        raise ModelNotReadyError(
            f"LLM binary missing at '{model_path}'. Please run the download script."
        )
    return model_path


def load_embedding_from_spec(spec: Dict[str, Any]):
    """Loads an embedding model using an explicit spec entry.

    Specs can point at locally managed models (``source=registry``) or remote
    Hugging Face repos (``source=huggingface``).
    """

    source = spec.get("source", "registry")
    name = spec.get("name")
    if not name:
        raise ValueError("Embedding spec is missing 'name'.")

    if source == "registry":
        return get_embedding_model(name)

    if source == "huggingface":
        class_name = spec.get("langchain_class", "HuggingFaceEmbeddings")
        if class_name == "HuggingFaceBgeEmbeddings":
            return HuggingFaceBgeEmbeddings(model_name=name)
        if class_name == "HuggingFaceEmbeddings":
            return HuggingFaceEmbeddings(model_name=name)
        raise ValueError(f"Unsupported LangChain class for HF source: {class_name}")

    raise ValueError(f"Unsupported embedding source: {source}")

if __name__ == '__main__':
    # Example usage:
    try:
        print("Loading bge-large-en-v1.5...")
        bge_model = get_embedding_model("bge-large-en-v1.5")
        print("Model loaded:", bge_model)
        
        # You would need a sample text to test the embedding
        # query_result = bge_model.embed_query("This is a test document.")
        # print("Embedding successful.")

    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
