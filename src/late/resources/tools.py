"""
Tools resource for media download and utilities.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from late.models import (
    CaptionResponse,
    DownloadResponse,
    HashtagCheckResponse,
    TranscriptResponse,
)

from .base import BaseResource

if TYPE_CHECKING:
    from late.enums import CaptionTone


class ToolsResource(BaseResource[DownloadResponse]):
    """
    Resource for media download and utility tools.

    Rate limits by plan:
    - Build: 50/day
    - Accelerate: 500/day
    - Unlimited: unlimited

    Example:
        >>> from late import CaptionTone
        >>> client = Late(api_key="...")
        >>> # Download YouTube video
        >>> result = client.tools.youtube_download("https://youtube.com/watch?v=...")
        >>> # Generate AI caption
        >>> caption = client.tools.generate_caption(
        ...     image_url="https://example.com/image.jpg",
        ...     tone=CaptionTone.PROFESSIONAL,
        ... )
    """

    _BASE_PATH = "/v1/tools"

    # -------------------------------------------------------------------------
    # YouTube
    # -------------------------------------------------------------------------

    def youtube_download(
        self,
        url: str,
        *,
        format_id: str | None = None,
    ) -> DownloadResponse:
        """
        Download YouTube video or audio.

        Args:
            url: YouTube video URL
            format_id: Optional format ID for specific quality

        Returns:
            DownloadResponse with download information
        """
        params = self._build_params(url=url, format_id=format_id)
        data = self._client._get(self._path("youtube", "download"), params=params)
        return DownloadResponse.model_validate(data)

    def youtube_transcript(
        self,
        url: str,
        *,
        lang: str | None = None,
    ) -> TranscriptResponse:
        """
        Get YouTube video transcript.

        Args:
            url: YouTube video URL
            lang: Optional language code for transcript

        Returns:
            TranscriptResponse with transcript data
        """
        params = self._build_params(url=url, lang=lang)
        data = self._client._get(self._path("youtube", "transcript"), params=params)
        return TranscriptResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Instagram
    # -------------------------------------------------------------------------

    def instagram_download(self, url: str) -> DownloadResponse:
        """
        Download Instagram reel or post.

        Args:
            url: Instagram post/reel URL

        Returns:
            DownloadResponse with download information
        """
        data = self._client._get(
            self._path("instagram", "download"), params={"url": url}
        )
        return DownloadResponse.model_validate(data)

    def instagram_hashtag_check(self, hashtags: list[str]) -> HashtagCheckResponse:
        """
        Check Instagram hashtags for bans.

        Args:
            hashtags: List of hashtags to check

        Returns:
            HashtagCheckResponse with hashtag status information
        """
        data = self._client._post(
            self._path("instagram", "hashtag-checker"),
            data={"hashtags": hashtags},
        )
        return HashtagCheckResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # TikTok
    # -------------------------------------------------------------------------

    def tiktok_download(
        self,
        url: str,
        *,
        no_watermark: bool = True,
    ) -> DownloadResponse:
        """
        Download TikTok video.

        Args:
            url: TikTok video URL
            no_watermark: If True, download without watermark

        Returns:
            DownloadResponse with download information
        """
        params = {"url": url, "noWatermark": str(no_watermark).lower()}
        data = self._client._get(self._path("tiktok", "download"), params=params)
        return DownloadResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Twitter
    # -------------------------------------------------------------------------

    def twitter_download(self, url: str) -> DownloadResponse:
        """
        Download Twitter/X video.

        Args:
            url: Twitter/X video URL

        Returns:
            DownloadResponse with download information
        """
        data = self._client._get(self._path("twitter", "download"), params={"url": url})
        return DownloadResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Facebook
    # -------------------------------------------------------------------------

    def facebook_download(self, url: str) -> DownloadResponse:
        """
        Download Facebook video.

        Args:
            url: Facebook video URL

        Returns:
            DownloadResponse with download information
        """
        data = self._client._get(
            self._path("facebook", "download"), params={"url": url}
        )
        return DownloadResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # LinkedIn
    # -------------------------------------------------------------------------

    def linkedin_download(self, url: str) -> DownloadResponse:
        """
        Download LinkedIn video.

        Args:
            url: LinkedIn video URL

        Returns:
            DownloadResponse with download information
        """
        data = self._client._get(
            self._path("linkedin", "download"), params={"url": url}
        )
        return DownloadResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Bluesky
    # -------------------------------------------------------------------------

    def bluesky_download(self, url: str) -> DownloadResponse:
        """
        Download Bluesky video.

        Args:
            url: Bluesky video URL

        Returns:
            DownloadResponse with download information
        """
        data = self._client._get(self._path("bluesky", "download"), params={"url": url})
        return DownloadResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # AI Caption Generator
    # -------------------------------------------------------------------------

    def generate_caption(
        self,
        image_url: str,
        *,
        prompt: str | None = None,
        tone: CaptionTone | str | None = None,
    ) -> CaptionResponse:
        """
        Generate AI captions for an image.

        Args:
            image_url: URL of the image to analyze
            prompt: Optional custom prompt for generation
            tone: Optional tone (professional, casual, humorous, etc.)

        Returns:
            CaptionResponse with generated caption
        """
        payload = self._build_payload(
            image_url=image_url,
            prompt=prompt,
            tone=tone,
        )
        data = self._client._post(self._path("caption-generator"), data=payload)
        return CaptionResponse.model_validate(data)

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def ayoutube_download(
        self,
        url: str,
        *,
        format_id: str | None = None,
    ) -> DownloadResponse:
        """Download YouTube video asynchronously."""
        params = self._build_params(url=url, format_id=format_id)
        data = await self._client._aget(
            self._path("youtube", "download"), params=params
        )
        return DownloadResponse.model_validate(data)

    async def ayoutube_transcript(
        self,
        url: str,
        *,
        lang: str | None = None,
    ) -> TranscriptResponse:
        """Get YouTube transcript asynchronously."""
        params = self._build_params(url=url, lang=lang)
        data = await self._client._aget(
            self._path("youtube", "transcript"), params=params
        )
        return TranscriptResponse.model_validate(data)

    async def ainstagram_download(self, url: str) -> DownloadResponse:
        """Download Instagram content asynchronously."""
        data = await self._client._aget(
            self._path("instagram", "download"), params={"url": url}
        )
        return DownloadResponse.model_validate(data)

    async def ainstagram_hashtag_check(
        self, hashtags: list[str]
    ) -> HashtagCheckResponse:
        """Check Instagram hashtags asynchronously."""
        data = await self._client._apost(
            self._path("instagram", "hashtag-checker"),
            data={"hashtags": hashtags},
        )
        return HashtagCheckResponse.model_validate(data)

    async def atiktok_download(
        self,
        url: str,
        *,
        no_watermark: bool = True,
    ) -> DownloadResponse:
        """Download TikTok video asynchronously."""
        params = {"url": url, "noWatermark": str(no_watermark).lower()}
        data = await self._client._aget(self._path("tiktok", "download"), params=params)
        return DownloadResponse.model_validate(data)

    async def atwitter_download(self, url: str) -> DownloadResponse:
        """Download Twitter video asynchronously."""
        data = await self._client._aget(
            self._path("twitter", "download"), params={"url": url}
        )
        return DownloadResponse.model_validate(data)

    async def afacebook_download(self, url: str) -> DownloadResponse:
        """Download Facebook video asynchronously."""
        data = await self._client._aget(
            self._path("facebook", "download"), params={"url": url}
        )
        return DownloadResponse.model_validate(data)

    async def alinkedin_download(self, url: str) -> DownloadResponse:
        """Download LinkedIn video asynchronously."""
        data = await self._client._aget(
            self._path("linkedin", "download"), params={"url": url}
        )
        return DownloadResponse.model_validate(data)

    async def abluesky_download(self, url: str) -> DownloadResponse:
        """Download Bluesky video asynchronously."""
        data = await self._client._aget(
            self._path("bluesky", "download"), params={"url": url}
        )
        return DownloadResponse.model_validate(data)

    async def agenerate_caption(
        self,
        image_url: str,
        *,
        prompt: str | None = None,
        tone: CaptionTone | str | None = None,
    ) -> CaptionResponse:
        """Generate AI caption asynchronously."""
        payload = self._build_payload(
            image_url=image_url,
            prompt=prompt,
            tone=tone,
        )
        data = await self._client._apost(self._path("caption-generator"), data=payload)
        return CaptionResponse.model_validate(data)
