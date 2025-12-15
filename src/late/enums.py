"""
Enums for Late SDK.

These enums provide type-safe constants for common values used throughout the SDK.
They inherit from both `str` and `Enum`, so they serialize automatically to their
string values when used in API requests.

Example:
    >>> from late import Platform, PostStatus
    >>> Platform.TWITTER
    <Platform.TWITTER: 'twitter'>
    >>> Platform.TWITTER == "twitter"
    True
    >>> str(Platform.TWITTER)
    'twitter'
"""

from enum import Enum


class Platform(str, Enum):
    """
    Supported social media platforms.

    Example:
        >>> from late import Late, Platform
        >>> client = Late(api_key="...")
        >>> post = client.posts.create(
        ...     content="Hello!",
        ...     platforms=[{"platform": Platform.TWITTER, "accountId": "acc_123"}],
        ... )
    """

    TWITTER = "twitter"
    """Twitter/X"""

    INSTAGRAM = "instagram"
    """Instagram (feed posts, stories, reels)"""

    FACEBOOK = "facebook"
    """Facebook Pages"""

    LINKEDIN = "linkedin"
    """LinkedIn (personal profiles and company pages)"""

    TIKTOK = "tiktok"
    """TikTok"""

    YOUTUBE = "youtube"
    """YouTube (videos and shorts)"""

    PINTEREST = "pinterest"
    """Pinterest"""

    REDDIT = "reddit"
    """Reddit"""

    BLUESKY = "bluesky"
    """Bluesky"""

    THREADS = "threads"
    """Threads (Meta)"""

    GOOGLE_BUSINESS = "googlebusiness"
    """Google Business Profile"""


class PostStatus(str, Enum):
    """
    Post publication statuses.

    Example:
        >>> from late import Late, PostStatus
        >>> client = Late(api_key="...")
        >>> scheduled = client.posts.list(status=PostStatus.SCHEDULED)
        >>> failed = client.posts.list(status=PostStatus.FAILED)
    """

    DRAFT = "draft"
    """Saved but not scheduled for publishing"""

    SCHEDULED = "scheduled"
    """Scheduled for future publishing"""

    PUBLISHING = "publishing"
    """Currently being published to platforms"""

    PUBLISHED = "published"
    """Successfully published to all platforms"""

    FAILED = "failed"
    """Publishing failed on all platforms"""

    PARTIAL = "partial"
    """Publishing succeeded on some platforms but failed on others"""


class MediaType(str, Enum):
    """
    Media item types.

    Example:
        >>> from late import MediaType
        >>> media_item = {
        ...     "type": MediaType.VIDEO,
        ...     "url": "https://example.com/video.mp4",
        ... }
    """

    IMAGE = "image"
    """Static image (JPEG, PNG, WebP, etc.)"""

    VIDEO = "video"
    """Video file (MP4, MOV, etc.)"""

    GIF = "gif"
    """Animated GIF"""

    DOCUMENT = "document"
    """Document file (PDF for LinkedIn)"""


class Visibility(str, Enum):
    """
    Content visibility settings.

    Used primarily for YouTube videos and other platforms that support
    visibility controls.

    Example:
        >>> from late import Visibility
        >>> youtube_settings = {
        ...     "visibility": Visibility.UNLISTED,
        ... }
    """

    PUBLIC = "public"
    """Anyone can view the content"""

    PRIVATE = "private"
    """Only you and explicitly shared users can view"""

    UNLISTED = "unlisted"
    """Only people with the direct link can view"""


class InstagramContentType(str, Enum):
    """
    Instagram-specific content types.

    Example:
        >>> from late import InstagramContentType
        >>> instagram_settings = {
        ...     "contentType": InstagramContentType.STORY,
        ... }
    """

    STORY = "story"
    """Ephemeral story (disappears after 24 hours)"""


class FacebookContentType(str, Enum):
    """
    Facebook-specific content types.

    Example:
        >>> from late import FacebookContentType
        >>> facebook_settings = {
        ...     "contentType": FacebookContentType.STORY,
        ... }
    """

    STORY = "story"
    """Facebook Page Story (ephemeral, 24 hours)"""


class TikTokPrivacyLevel(str, Enum):
    """
    TikTok privacy levels.

    Note: Available options depend on the creator's account settings.
    Use the accounts API to get available options for each account.
    """

    PUBLIC_TO_EVERYONE = "PUBLIC_TO_EVERYONE"
    """Visible to everyone"""

    MUTUAL_FOLLOW_FRIENDS = "MUTUAL_FOLLOW_FRIENDS"
    """Visible only to mutual followers"""

    FOLLOWER_OF_CREATOR = "FOLLOWER_OF_CREATOR"
    """Visible only to followers"""

    SELF_ONLY = "SELF_ONLY"
    """Visible only to the creator"""


class TikTokCommercialContentType(str, Enum):
    """
    TikTok commercial content disclosure types.

    Required for brand partnerships and sponsored content.
    """

    NONE = "none"
    """Not commercial content"""

    BRAND_ORGANIC = "brand_organic"
    """Organic brand content"""

    BRAND_CONTENT = "brand_content"
    """Paid partnership / sponsored content"""


class TikTokMediaType(str, Enum):
    """
    TikTok media types.

    Usually auto-detected from media items, but can be overridden.
    """

    VIDEO = "video"
    """Video post"""

    PHOTO = "photo"
    """Photo carousel (up to 35 images)"""


class GoogleBusinessCTAType(str, Enum):
    """
    Google Business Profile call-to-action button types.

    Example:
        >>> from late import GoogleBusinessCTAType
        >>> cta = {
        ...     "type": GoogleBusinessCTAType.BOOK,
        ...     "url": "https://example.com/book",
        ... }
    """

    LEARN_MORE = "LEARN_MORE"
    """Link to more information"""

    BOOK = "BOOK"
    """Booking/reservation link"""

    ORDER = "ORDER"
    """Online ordering link"""

    SHOP = "SHOP"
    """E-commerce/shopping link"""

    SIGN_UP = "SIGN_UP"
    """Registration/signup link"""

    CALL = "CALL"
    """Phone call action"""


class DayOfWeek(int, Enum):
    """
    Days of the week for queue scheduling.

    Values follow the JavaScript/API convention where Sunday = 0.

    Example:
        >>> from late import DayOfWeek
        >>> slots = [
        ...     {"dayOfWeek": DayOfWeek.MONDAY, "time": "09:00"},
        ...     {"dayOfWeek": DayOfWeek.WEDNESDAY, "time": "14:00"},
        ... ]
    """

    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


class CaptionTone(str, Enum):
    """
    Tones for AI-generated captions.

    Example:
        >>> from late import Late, CaptionTone
        >>> client = Late(api_key="...")
        >>> result = client.tools.generate_caption(
        ...     image_url="https://example.com/image.jpg",
        ...     tone=CaptionTone.PROFESSIONAL,
        ... )
    """

    PROFESSIONAL = "professional"
    """Formal, business-appropriate tone"""

    CASUAL = "casual"
    """Relaxed, conversational tone"""

    HUMOROUS = "humorous"
    """Fun, witty, or playful tone"""

    INSPIRATIONAL = "inspirational"
    """Motivational, uplifting tone"""

    INFORMATIVE = "informative"
    """Educational, fact-focused tone"""
