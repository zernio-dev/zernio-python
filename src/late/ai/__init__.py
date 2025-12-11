"""
AI content generation abstraction.

Provides a provider-agnostic interface for content generation,
similar to Vercel AI SDK.
"""

from .content_generator import ContentGenerator
from .protocols import (
    AIProvider,
    GenerateRequest,
    GenerateResponse,
    StreamingAIProvider,
)
from .providers import OpenAIProvider

__all__ = [
    "AIProvider",
    "ContentGenerator",
    "GenerateRequest",
    "GenerateResponse",
    "OpenAIProvider",
    "StreamingAIProvider",
]
