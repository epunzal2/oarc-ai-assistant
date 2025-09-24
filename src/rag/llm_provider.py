from abc import ABC, abstractmethod
from typing import Any, Dict

from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface.chat_models import ChatHuggingFace
from langchain_community.llms import LlamaCpp

from src.rag.config import HF_API_TOKEN, HF_MODEL_NAME, LLAMA_CPP_MODEL_PATH
from src.rag.logger import get_logger

logger = get_logger(__name__)


class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    """

    @abstractmethod
    def get_llm(self):
        pass


class HuggingFaceAPIProvider(LLMProvider):
    """
    LLM provider for the Hugging Face API.
    """

    def __init__(self, api_token=HF_API_TOKEN, model_name=HF_MODEL_NAME, **generation_kwargs):
        if not api_token:
            raise ValueError("Hugging Face API token is required.")
        self.api_token = api_token
        self.model_name = model_name
        self.generation_kwargs = {
            "temperature": 0.1,
            "max_new_tokens": 512,
        }
        self.generation_kwargs.update(generation_kwargs)
        logger.info(
            f"Initialized HuggingFaceAPIProvider with model: {self.model_name}"
        )

    def get_llm(self):
        """
        Returns the Hugging Face LLM endpoint.
        """
        logger.info("Creating Hugging Face LLM endpoint.")
        llm = HuggingFaceEndpoint(
            repo_id=self.model_name,
            huggingfacehub_api_token=self.api_token,
            **self.generation_kwargs,
        )
        return ChatHuggingFace(llm=llm)


class LlamaCPPProvider(LLMProvider):
    """
    LLM provider for a local Llama.cpp model.
    """

    def __init__(self, model_path=LLAMA_CPP_MODEL_PATH, **model_kwargs):
        self.model_path = model_path
        defaults: Dict[str, Any] = {
            "n_gpu_layers": -1,
            "n_batch": 512,
            "n_ctx": 2048,
            "f16_kv": True,
            "verbose": True,
        }
        defaults.update(model_kwargs)
        self.model_kwargs = defaults
        logger.info(
            "Initialized LlamaCPPProvider with model: %s", self.model_path
        )

    def get_llm(self):
        """
        Returns the Llama.cpp LLM instance.
        """
        logger.info("Creating Llama.cpp LLM instance.")
        llm = LlamaCpp(
            model_path=self.model_path,
            **self.model_kwargs,
        )
        return llm


def get_llm_provider(provider_name="llama_cpp", **kwargs):
    """
    Factory function to get an LLM provider.
    """
    if provider_name == "huggingface_api":
        return HuggingFaceAPIProvider(**kwargs)
    elif provider_name == "llama_cpp":
        return LlamaCPPProvider(**kwargs)
    # Add other providers here in the future
    else:
        raise ValueError(f"Unknown LLM provider: {provider_name}")

if __name__ == '__main__':
    # This is for testing the LLM provider
    try:
        provider = get_llm_provider()
        llm = provider.get_llm()
        logger.info("Successfully created LLM instance.")
        # You would need a prompt to invoke the LLM
        # from langchain_core.prompts import PromptTemplate
        #
        # template = "Question: {question}\\nAnswer: Let's think step by step."
        # prompt = PromptTemplate.from_template(template)
        # chain = prompt | llm
        # print(chain.invoke({"question": "What is the capital of France?"}))

    except ValueError as e:
        logger.error(e)
