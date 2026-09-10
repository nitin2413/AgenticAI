"""
Google Gemini LLM Provider
"""

from .base_provider import BaseLLMProvider
from langchain_google_genai import ChatGoogleGenerativeAI


class GoogleProvider(BaseLLMProvider):
    """
    Google Gemini LLM provider class.
    """

    def validate_config(self) -> bool:
        """Validate config parameters."""
        api_key = self.config.get("api_key") or self.config.get("google_api_key")
        if not api_key:
            raise ValueError("Missing Google Gemini API key")
        return True

    def get_model(self) -> ChatGoogleGenerativeAI:
        """Create and return the ChatGoogleGenerativeAI model instance."""
        if self._model is None:
            self.validate_config()
            api_key = self.config.get("api_key") or self.config.get("google_api_key")
            model_name = self.config.get("model", "gemini-pro")
            temperature = self.config.get("temperature", 0.7)
            max_tokens = self.config.get("max_tokens")

            # Setup ChatGoogleGenerativeAI
            self._model = ChatGoogleGenerativeAI(
                google_api_key=api_key,
                model=model_name,
                temperature=temperature,
                max_output_tokens=max_tokens,
            )
        return self._model
