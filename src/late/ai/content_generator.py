"""
Unified content generator that can use any provider.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from late.enums import CaptionTone, Platform

from .protocols import (
    AIProvider,
    GenerateRequest,
    GenerateResponse,
    StreamingAIProvider,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


class ContentGenerator:
    """
    Unified interface for content generation across providers.

    Provides a single API that can switch between providers seamlessly.

    Example:
        >>> from late.ai import ContentGenerator, GenerateRequest
        >>> from late import Platform, CaptionTone
        >>>
        >>> # Using OpenAI
        >>> generator = ContentGenerator(provider="openai", api_key="sk-...")
        >>>
        >>> response = generator.generate(
        ...     GenerateRequest(
        ...         prompt="Write a tweet about Python",
        ...         platform=Platform.TWITTER,
        ...         tone=CaptionTone.PROFESSIONAL,
        ...     )
        ... )
        >>> print(response.text)
        >>>
        >>> # Async streaming
        >>> async for chunk in generator.agenerate_stream(request):
        ...     print(chunk, end="")
    """

    _providers: dict[str, type] = {}

    def __init__(
        self,
        provider: str = "openai",
        **provider_kwargs: Any,
    ) -> None:
        """
        Initialize the content generator.

        Args:
            provider: Provider name ("openai", "anthropic")
            **provider_kwargs: Arguments passed to provider (api_key, model, etc.)
        """
        self._provider = self._create_provider(provider, **provider_kwargs)

    @classmethod
    def register_provider(cls, name: str, provider_class: type) -> None:
        """Register a custom provider."""
        cls._providers[name.lower()] = provider_class

    def _create_provider(self, name: str, **kwargs: Any) -> AIProvider:
        """Create a provider instance."""
        name_lower = name.lower()

        # Built-in providers
        if name_lower == "openai":
            from .providers.openai import OpenAIProvider

            return OpenAIProvider(**kwargs)

        # Custom providers
        if name_lower in self._providers:
            return self._providers[name_lower](**kwargs)

        available = ["openai"] + list(self._providers.keys())
        raise ValueError(f"Unknown provider: {name}. Available: {available}")

    @property
    def provider_name(self) -> str:
        """Get the current provider name."""
        return self._provider.name

    def generate(self, request: GenerateRequest) -> GenerateResponse:
        """Generate content using the configured provider."""
        return self._provider.generate(request)

    async def agenerate(self, request: GenerateRequest) -> GenerateResponse:
        """Generate content asynchronously."""
        return await self._provider.agenerate(request)

    async def agenerate_stream(self, request: GenerateRequest) -> AsyncIterator[str]:
        """Generate content as a stream."""
        if not isinstance(self._provider, StreamingAIProvider):
            raise NotImplementedError(
                f"Provider {self.provider_name} does not support streaming"
            )
        async for chunk in self._provider.agenerate_stream(request):
            yield chunk

    # Convenience methods
    def generate_post(
        self,
        topic: str,
        platform: Platform | str,
        *,
        tone: CaptionTone | str = CaptionTone.PROFESSIONAL,
        language: str = "en",
        **kwargs: Any,
    ) -> str:
        """
        Generate a social media post.

        Args:
            topic: What to write about
            platform: Target platform (twitter, linkedin, etc.)
            tone: Writing tone
            language: Output language

        Returns:
            Generated post content
        """
        request = GenerateRequest(
            prompt=f"Write a {platform} post about: {topic}",
            platform=platform,
            tone=tone,
            language=language,
            **kwargs,
        )
        return self.generate(request).text

    async def agenerate_post(
        self,
        topic: str,
        platform: Platform | str,
        *,
        tone: CaptionTone | str = CaptionTone.PROFESSIONAL,
        language: str = "en",
        **kwargs: Any,
    ) -> str:
        """Generate a social media post asynchronously."""
        request = GenerateRequest(
            prompt=f"Write a {platform} post about: {topic}",
            platform=platform,
            tone=tone,
            language=language,
            **kwargs,
        )
        response = await self.agenerate(request)
        return response.text
