# Changelog

All notable changes to the Late Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-01-16

### Added
- MCP (Model Context Protocol) server support for Claude Desktop integration
- HTTP server mode for MCP (`late-mcp-http`)
- AI content generation module with OpenAI and Anthropic support
- Pipelines for common workflows (CSV scheduler, cross-poster)
- Large file upload support via Vercel Blob
- Progress callbacks for file uploads
- Comprehensive test suite with pytest

### Changed
- Improved error handling with specialized exception classes
- Better async support throughout the SDK

## [1.1.0] - 2025-01-10

### Added
- Upload module with `SmartUploader` for automatic upload strategy selection
- Direct upload for files under 4MB
- Multipart upload support for large files
- `upload_bytes()` and `upload_large_bytes()` methods

## [1.0.0] - 2025-01-01

### Added
- Initial public release
- Full coverage of Late API endpoints
- Support for all 13 social media platforms: Instagram, TikTok, YouTube, LinkedIn, X/Twitter, Facebook, Pinterest, Threads, Bluesky, Reddit, Snapchat, Telegram, and Google Business Profile
- Async support with `alist()`, `acreate()`, etc.
- Type hints and Pydantic models
- Error handling with `LateAPIError`, `LateRateLimitError`, `LateValidationError`

### API Coverage
- Posts: create, list, get, update, delete, retry, bulk upload
- Accounts: list, get, follower stats
- Profiles: create, list, get, update, delete
- Analytics: get metrics, usage stats
- Account Groups: create, list, update, delete
- Queue: slots management, preview
- Webhooks: settings management, logs, testing
- API Keys: create, list, delete
- Media: upload, generate upload token
- Tools: downloads, hashtag checking, transcripts, AI caption generation
- Users: list, get
- Usage: stats
- Logs: list, get
- Connect: OAuth flows for all platforms
- Reddit: feed, search
- Invites: platform invites management
