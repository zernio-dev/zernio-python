"""
Tools resource for media download and utilities.
"""

from __future__ import annotations

from typing import Any, Literal

from .base import BaseResource

Tone = Literal["professional", "casual", "humorous", "inspirational", "informative"]


class ToolsResource(BaseResource[Any]):
    """
    Resource for media download and utility tools.

    Rate limits by plan:
    - Build: 50/day
    - Accelerate: 500/day
    - Unlimited: unlimited

    Example:
        >>> client = Late(api_key="...")
        >>> # Download YouTube video
        >>> result = client.tools.youtube_download("https://youtube.com/watch?v=...")
        >>> # Generate AI caption
        >>> caption = client.tools.generate_caption(
        ...     image_url="https://example.com/image.jpg",
        ...     tone="professional",
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
    ) -> dict[str, Any]:
        """
        Download YouTube video or audio.

        Args:
            url: YouTube video URL
            format_id: Optional format ID for specific quality

        Returns:
            Dict with download information
        """
        params = self._build_params(url=url, format_id=format_id)
        return self._client._get(self._path("youtube", "download"), params=params)

    def youtube_transcript(
        self,
        url: str,
        *,
        lang: str | None = None,
    ) -> dict[str, Any]:
        """
        Get YouTube video transcript.

        Args:
            url: YouTube video URL
            lang: Optional language code for transcript

        Returns:
            Dict with transcript data
        """
        params = self._build_params(url=url, lang=lang)
        return self._client._get(self._path("youtube", "transcript"), params=params)

    # -------------------------------------------------------------------------
    # Instagram
    # -------------------------------------------------------------------------

    def instagram_download(self, url: str) -> dict[str, Any]:
        """
        Download Instagram reel or post.

        Args:
            url: Instagram post/reel URL

        Returns:
            Dict with download information
        """
        return self._client._get(self._path("instagram", "download"), params={"url": url})

    def instagram_hashtag_check(self, hashtags: list[str]) -> dict[str, Any]:
        """
        Check Instagram hashtags for bans.

        Args:
            hashtags: List of hashtags to check

        Returns:
            Dict with hashtag status information
        """
        return self._client._post(
            self._path("instagram", "hashtag-checker"),
            data={"hashtags": hashtags},
        )

    # -------------------------------------------------------------------------
    # TikTok
    # -------------------------------------------------------------------------

    def tiktok_download(
        self,
        url: str,
        *,
        no_watermark: bool = True,
    ) -> dict[str, Any]:
        """
        Download TikTok video.

        Args:
            url: TikTok video URL
            no_watermark: If True, download without watermark

        Returns:
            Dict with download information
        """
        params = {"url": url, "noWatermark": str(no_watermark).lower()}
        return self._client._get(self._path("tiktok", "download"), params=params)

    # -------------------------------------------------------------------------
    # Twitter
    # -------------------------------------------------------------------------

    def twitter_download(self, url: str) -> dict[str, Any]:
        """
        Download Twitter/X video.

        Args:
            url: Twitter/X video URL

        Returns:
            Dict with download information
        """
        return self._client._get(self._path("twitter", "download"), params={"url": url})

    # -------------------------------------------------------------------------
    # Facebook
    # -------------------------------------------------------------------------

    def facebook_download(self, url: str) -> dict[str, Any]:
        """
        Download Facebook video.

        Args:
            url: Facebook video URL

        Returns:
            Dict with download information
        """
        return self._client._get(self._path("facebook", "download"), params={"url": url})

    # -------------------------------------------------------------------------
    # LinkedIn
    # -------------------------------------------------------------------------

    def linkedin_download(self, url: str) -> dict[str, Any]:
        """
        Download LinkedIn video.

        Args:
            url: LinkedIn video URL

        Returns:
            Dict with download information
        """
        return self._client._get(self._path("linkedin", "download"), params={"url": url})

    # -------------------------------------------------------------------------
    # Bluesky
    # -------------------------------------------------------------------------

    def bluesky_download(self, url: str) -> dict[str, Any]:
        """
        Download Bluesky video.

        Args:
            url: Bluesky video URL

        Returns:
            Dict with download information
        """
        return self._client._get(self._path("bluesky", "download"), params={"url": url})

    # -------------------------------------------------------------------------
    # AI Caption Generator
    # -------------------------------------------------------------------------

    def generate_caption(
        self,
        image_url: str,
        *,
        prompt: str | None = None,
        tone: Tone | None = None,
    ) -> dict[str, Any]:
        """
        Generate AI captions for an image.

        Args:
            image_url: URL of the image to analyze
            prompt: Optional custom prompt for generation
            tone: Optional tone (professional, casual, humorous, etc.)

        Returns:
            Dict with generated caption(s)
        """
        payload = self._build_payload(
            image_url=image_url,
            prompt=prompt,
            tone=tone,
        )
        return self._client._post(self._path("caption-generator"), data=payload)

    # -------------------------------------------------------------------------
    # Async methods
    # -------------------------------------------------------------------------

    async def ayoutube_download(
        self,
        url: str,
        *,
        format_id: str | None = None,
    ) -> dict[str, Any]:
        """Download YouTube video asynchronously."""
        params = self._build_params(url=url, format_id=format_id)
        return await self._client._aget(self._path("youtube", "download"), params=params)

    async def ayoutube_transcript(
        self,
        url: str,
        *,
        lang: str | None = None,
    ) -> dict[str, Any]:
        """Get YouTube transcript asynchronously."""
        params = self._build_params(url=url, lang=lang)
        return await self._client._aget(self._path("youtube", "transcript"), params=params)

    async def ainstagram_download(self, url: str) -> dict[str, Any]:
        """Download Instagram content asynchronously."""
        return await self._client._aget(
            self._path("instagram", "download"), params={"url": url}
        )

    async def ainstagram_hashtag_check(self, hashtags: list[str]) -> dict[str, Any]:
        """Check Instagram hashtags asynchronously."""
        return await self._client._apost(
            self._path("instagram", "hashtag-checker"),
            data={"hashtags": hashtags},
        )

    async def atiktok_download(
        self,
        url: str,
        *,
        no_watermark: bool = True,
    ) -> dict[str, Any]:
        """Download TikTok video asynchronously."""
        params = {"url": url, "noWatermark": str(no_watermark).lower()}
        return await self._client._aget(self._path("tiktok", "download"), params=params)

    async def atwitter_download(self, url: str) -> dict[str, Any]:
        """Download Twitter video asynchronously."""
        return await self._client._aget(
            self._path("twitter", "download"), params={"url": url}
        )

    async def afacebook_download(self, url: str) -> dict[str, Any]:
        """Download Facebook video asynchronously."""
        return await self._client._aget(
            self._path("facebook", "download"), params={"url": url}
        )

    async def alinkedin_download(self, url: str) -> dict[str, Any]:
        """Download LinkedIn video asynchronously."""
        return await self._client._aget(
            self._path("linkedin", "download"), params={"url": url}
        )

    async def abluesky_download(self, url: str) -> dict[str, Any]:
        """Download Bluesky video asynchronously."""
        return await self._client._aget(
            self._path("bluesky", "download"), params={"url": url}
        )

    async def agenerate_caption(
        self,
        image_url: str,
        *,
        prompt: str | None = None,
        tone: Tone | None = None,
    ) -> dict[str, Any]:
        """Generate AI caption asynchronously."""
        payload = self._build_payload(
            image_url=image_url,
            prompt=prompt,
            tone=tone,
        )
        return await self._client._apost(self._path("caption-generator"), data=payload)
