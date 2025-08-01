from abc import ABC, abstractmethod
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface.chat_models import ChatHuggingFace
from src.config import HF_API_TOKEN, HF_MODEL_NAME
from src.logger import get_logger

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
    def __init__(self, api_token=HF_API_TOKEN, model_name=HF_MODEL_NAME):
        if not api_token:
            raise ValueError("Hugging Face API token is required.")
        self.api_token = api_token
        self.model_name = model_name
        logger.info(f"Initialized HuggingFaceAPIProvider with model: {self.model_name}")

    def get_llm(self):
        """
        Returns the Hugging Face LLM endpoint.
        """
        logger.info("Creating Hugging Face LLM endpoint.")
        llm = HuggingFaceEndpoint(
            repo_id=self.model_name,
            huggingfacehub_api_token=self.api_token,
            temperature=0.1,
            max_new_tokens=512,
        )
        return ChatHuggingFace(llm=llm)

def get_llm_provider(provider_name="huggingface_api"):
    """
    Factory function to get an LLM provider.
    """
    if provider_name == "huggingface_api":
        return HuggingFaceAPIProvider()
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
