"""
LLM Initializer
Convenience functions for initializing LLM models in agents
"""

from typing import Optional, Dict, Any
from langchain_core.language_models.llms import LLM
from config.settings import settings
from .provider_factory import LLMProviderFactory


def get_llm_model(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    **kwargs
) -> LLM:
    """
    Get an LLM model instance with optional overrides.
    
    Uses settings as defaults but allows per-call overrides.
    
    Args:
        provider: LLM provider type (openai, anthropic, google, ollama)
        model: Model name to use
        temperature: Temperature for generation
        max_tokens: Maximum tokens to generate
        **kwargs: Additional provider-specific parameters
        
    Returns:
        LLM: A LangChain LLM instance
        
    Example:
        # Use default settings
        model = get_llm_model()
        
        # Override model
        model = get_llm_model(model="gpt-4")
        
        # Use different provider
        model = get_llm_model(provider="anthropic", model="claude-3-opus-20240229")
    """
    config = settings.get_llm_config()
    
    # Apply overrides
    if provider:
        config["provider"] = provider
    if model:
        config["model"] = model
    if temperature is not None:
        config["temperature"] = temperature
    if max_tokens is not None:
        config["max_tokens"] = max_tokens
    
    # Add any additional kwargs
    config.update(kwargs)
    
    # Create and return the provider's model
    llm_provider = LLMProviderFactory.from_config(config)
    return llm_provider.get_model()


def create_llm_provider(
    provider: Optional[str] = None,
    **kwargs
) -> LLM:
    """
    Create and set the current LLM provider.
    
    Args:
        provider: Provider type (uses settings default if not specified)
        **kwargs: Provider-specific configuration
        
    Returns:
        LLM: A LangChain LLM instance
    """
    config = settings.get_llm_config()
    
    if provider:
        config["provider"] = provider
    
    config.update(kwargs)
    
    llm_provider = LLMProviderFactory.from_config(config)
    LLMProviderFactory.set_current(llm_provider)
    
    return llm_provider.get_model()


def get_current_llm() -> LLM:
    """
    Get the current LLM provider's model.
    Falls back to creating one if not set.
    
    Returns:
        LLM: A LangChain LLM instance
    """
    try:
        provider = LLMProviderFactory.get_current()
        return provider.get_model()
    except RuntimeError:
        # No current provider, create one
        return create_llm_provider()


def validate_provider_config(provider_type: str) -> bool:
    """
    Validate that a provider has required configuration.
    
    Args:
        provider_type: Provider type to validate
        
    Returns:
        bool: True if configuration is valid
        
    Raises:
        ValueError: If required configuration is missing
    """
    config = settings.get_llm_config()
    config["provider"] = provider_type
    
    try:
        llm_provider = LLMProviderFactory.from_config(config)
        llm_provider.validate_config()
        return True
    except Exception as e:
        raise ValueError(f"Invalid configuration for {provider_type}: {str(e)}")


def list_available_providers() -> Dict[str, str]:
    """
    List all available LLM providers.
    
    Returns:
        Dict[str, str]: Provider names and descriptions
    """
    return LLMProviderFactory.get_available_providers()
