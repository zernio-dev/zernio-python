"""
Protocols (interfaces) for AI provider abstraction.
Inspired by Vercel AI SDK's provider pattern.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from late.enums import CaptionTone, Platform


@dataclass
class GenerateRequest:
    """Request for content generation."""

    prompt: str
    system: str | None = None
    max_tokens: int = 500
    temperature: float = 0.7
    platform: Platform | str | None = None
    tone: CaptionTone | str | None = None
    language: str = "en"
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class GenerateResponse:
    """Response from content generation."""

    text: str
    provider: str
    model: str
    usage: dict[str, int] | None = None
    finish_reason: str | None = None


@runtime_checkable
class AIProvider(Protocol):
    """Protocol for AI content generation providers."""

    @property
    def name(self) -> str:
        """Provider name."""
        ...

    @property
    def default_model(self) -> str:
        """Default model for this provider."""
        ...

    @abstractmethod
    def generate(self, request: GenerateRequest) -> GenerateResponse:
        """Generate content synchronously."""
        ...

    @abstractmethod
    async def agenerate(self, request: GenerateRequest) -> GenerateResponse:
        """Generate content asynchronously."""
        ...


@runtime_checkable
class StreamingAIProvider(Protocol):
    """Protocol for streaming content generation."""

    @abstractmethod
    async def agenerate_stream(self, request: GenerateRequest) -> AsyncIterator[str]:
        """Generate content as a stream."""
        ...
