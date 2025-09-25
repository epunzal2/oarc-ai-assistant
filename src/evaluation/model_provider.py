import os
import glob
import logging
from typing import Any, Dict

import yaml
from langchain_huggingface import HuggingFaceBgeEmbeddings, HuggingFaceEmbeddings


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


def _locate_first_shard(local_dir: str, filename: str) -> str | None:
    """If the expected file is missing but shards exist, return the first shard.

    llama.cpp supports loading sharded GGUF by passing any shard path (usually
    the `-00001-of-000NN` file). Concatenating shards is incorrect for GGUF and
    will result in loader errors. This function returns the appropriate shard
    path so the runtime can load shards natively.
    """
    base, ext = os.path.splitext(filename)
    pattern = os.path.join(local_dir, f"{base}-*-of-*.{ext.lstrip('.')}")
    shards = sorted(glob.glob(pattern))
    if not shards:
        return None
    # Prefer the 00001 shard if present; otherwise pick the lexicographically first.
    for shard in shards:
        if "-00001-of-" in os.path.basename(shard):
            return shard
    return shards[0]


def get_llm_model_path(llm_name: str) -> str:
    """Returns the absolute path to a locally managed LLM binary.

    If the model file is sharded (downloaded as multiple `*-00001-of-*.gguf`),
    this function assembles the shards into the expected single file.
    """
    config = get_model_config()
    model_info = next((m for m in config.get("llms", []) if m["name"] == llm_name), None)
    if not model_info:
        raise ModelNotFoundError(f"LLM '{llm_name}' not found in the registry.")

    local_dir = model_info["local_dir"]
    filename = model_info["filename"]
    model_path = os.path.join(local_dir, filename)

    # Prefer native sharded loading if shards are present
    shard_path = _locate_first_shard(local_dir, filename)
    if shard_path and os.path.exists(shard_path):
        # If a non-sharded file with the target name also exists, warn users it may be a manual concatenation
        # which is not supported by llama.cpp for GGUF.
        if os.path.exists(model_path):
            logging.getLogger(__name__).warning(
                "Detected both '%s' and GGUF shards in '%s'. Using shards (%s). "
                "If '%s' was created by concatenating shards, please remove it to avoid loader errors.",
                os.path.basename(model_path), local_dir, os.path.basename(shard_path), os.path.basename(model_path)
            )
        logging.getLogger(__name__).info(
            "Using sharded GGUF; passing first shard to loader: %s", os.path.basename(shard_path)
        )
        return shard_path

    if os.path.exists(model_path):
        return model_path

    raise ModelNotReadyError(
        f"LLM binary missing at '{model_path}'. Please run the download script or "
        f"ensure shards are available in '{local_dir}'."
    )


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
