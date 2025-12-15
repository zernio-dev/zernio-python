"""
OpenAI provider implementation.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

from late.enums import Platform

from ..protocols import GenerateRequest, GenerateResponse

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


class OpenAIProvider:
    """
    OpenAI provider for content generation.

    Example:
        >>> provider = OpenAIProvider(api_key="sk-...")
        >>> response = provider.generate(
        ...     GenerateRequest(prompt="Write a tweet about Python")
        ... )
        >>> print(response.text)
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
        **kwargs: Any,
    ) -> None:
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self._api_key:
            raise ValueError(
                "OpenAI API key required. Set OPENAI_API_KEY or pass api_key."
            )

        self._model = model
        self._config = kwargs

        # Lazy import
        try:
            from openai import AsyncOpenAI, OpenAI

            self._client = OpenAI(api_key=self._api_key)
            self._async_client = AsyncOpenAI(api_key=self._api_key)
        except ImportError as e:
            raise ImportError(
                "openai package required. Install with: pip install 'late-sdk[ai]'"
            ) from e

    @property
    def name(self) -> str:
        return "openai"

    @property
    def model(self) -> str:
        """Current model being used."""
        return self._model

    @property
    def default_model(self) -> str:
        """Default model if none specified."""
        return "gpt-4o-mini"

    def _build_messages(self, request: GenerateRequest) -> list[dict[str, str]]:
        """Build messages for chat completion."""
        messages = []

        # System message
        system = request.system or self._build_system_prompt(request)
        if system:
            messages.append({"role": "system", "content": system})

        messages.append({"role": "user", "content": request.prompt})
        return messages

    def _build_system_prompt(self, request: GenerateRequest) -> str:
        """Build system prompt from request parameters."""
        parts = ["You are an expert social media content creator."]

        if request.platform:
            platform_guides: dict[Platform | str, str] = {
                Platform.TWITTER: "Keep it under 280 characters. Be concise and engaging.",
                Platform.LINKEDIN: "Be professional and insightful. Use paragraphs.",
                Platform.INSTAGRAM: "Be visual and use emojis. Include hashtag suggestions.",
                Platform.TIKTOK: "Be trendy and use Gen-Z language. Keep it fun.",
                Platform.FACEBOOK: "Be conversational and engaging.",
            }
            guide = platform_guides.get(request.platform, "")
            parts.append(f"Writing for {request.platform}. {guide}")

        if request.tone:
            parts.append(f"Use a {request.tone} tone.")

        if request.language != "en":
            parts.append(f"Write in {request.language}.")

        return " ".join(parts)

    def generate(self, request: GenerateRequest) -> GenerateResponse:
        """Generate content using OpenAI."""
        response = self._client.chat.completions.create(
            model=self._model,
            messages=self._build_messages(request),
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        choice = response.choices[0]
        return GenerateResponse(
            text=choice.message.content or "",
            provider=self.name,
            model=self._model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": (
                    response.usage.completion_tokens if response.usage else 0
                ),
            },
            finish_reason=choice.finish_reason,
        )

    async def agenerate(self, request: GenerateRequest) -> GenerateResponse:
        """Generate content asynchronously."""
        response = await self._async_client.chat.completions.create(
            model=self._model,
            messages=self._build_messages(request),
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        choice = response.choices[0]
        return GenerateResponse(
            text=choice.message.content or "",
            provider=self.name,
            model=self._model,
            usage={
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": (
                    response.usage.completion_tokens if response.usage else 0
                ),
            },
            finish_reason=choice.finish_reason,
        )

    async def agenerate_stream(self, request: GenerateRequest) -> AsyncIterator[str]:
        """Generate content as a stream."""
        stream = await self._async_client.chat.completions.create(
            model=self._model,
            messages=self._build_messages(request),
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
