from __future__ import annotations

_VIDEO_EXT = (".mp4", ".mov", ".avi", ".webm", ".m4v")
_IMAGE_EXT = (".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif", ".bmp", ".tiff")


def media_item(url: str) -> dict[str, str]:
    path = url.lower().split("?")[0]
    if path.endswith(_VIDEO_EXT):
        return {"type": "video", "url": url}
    if path.endswith(".gif"):
        return {"type": "gif", "url": url}
    if path.endswith(".pdf"):
        return {"type": "document", "url": url}
    if path.endswith(_IMAGE_EXT):
        return {"type": "image", "url": url}
    # Unknown extension (e.g. a Drive link): omit type so the API infers it (Drive links are rehosted first).
    return {"url": url}
