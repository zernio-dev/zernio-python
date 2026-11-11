# Changelog

All notable changes to the Late Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **`transport=` on `Late` / `Zernio`.** Pass an `httpx.BaseTransport` to reuse connections and TLS sessions across requests and clients. The caller owns it; the client never closes it. Without it nothing changes: a new connection per request.
- **Tool call telemetry on the hosted MCP server.** One JSON log line per tool call (tool, latency, outcome, hashed caller), and with `SENTRY_DSN` one Sentry transaction per tool call. `/health` reports the deployed commit.
- **Tool result size on the hosted MCP server.** `mcp_tool_call` gains `result_chars` and the Sentry transaction gains `mcp.tool.result.chars`, the characters of text a tool returned, so oversized results (one `ad_campaigns_get_ad_tree` call returned 284,873 characters) show per tool. Only the length is recorded, never the content.

### Fixed
- **Every MCP tool result was sent twice.** FastMCP derived a `{"result": string}` output schema from each tool's `-> str` return and repeated the whole text as `structuredContent`, so an 830,000-character result went out as about 1.66 MB, and ChatGPT shows both copies to the model. The main MCP server's 1,282 tools now return the text once, unchanged; the ChatGPT server keeps its real output schemas.
- **Every MCP tool call opened a new HTTPS connection to the Zernio API**, a TLS handshake and about 6 ms of CPU each, on the single server process that saturated on Nov 10. Tool calls now reuse a connection pool per worker thread. One pool shared by the 40 tool threads was slower than no pooling: httpcore scans every connection under one lock on each request. Measured over HTTPS against a stub API, 40 clients: 141 calls/s at 272 ms p50 before, 173/s at 220 ms after.
- **The hosted MCP server's memory kept growing until the next deploy.** Measured on Linux with a stub API: glibc kept freed memory from large API responses in per-thread arenas (829 MB against 303 MB with `MALLOC_ARENA_MAX=2`, now set in the Dockerfiles). Separately, FastMCP rebuilt `search_tools` and `call_tool` on every `tools/list` and every call to them, and `uncalled_for` kept each new function forever (about 3.6 MB per 1,000 `tools/list`). The transform now builds each tool once.
- **Ad updates reported a failure after 91 seconds while the update had worked, and each retry ran it again.** A `PUT` that took over 30 seconds was retried up to 3 times, so one call could update Meta several times and collect a 429 from the overlap. `PUT` and `PATCH` under `/v1/ads/` now use `publish_timeout` (300s) and are not retried on a timeout. `PUT` with `publishNow` gets the same treatment, so an update can no longer publish twice.
- **Ad creates could time out at 30 seconds while the ad was still being created, and a retry could create it twice.** A Meta video ad takes up to about 3 minutes, so the agent saw an error for an ad that then went live. `POST /v1/ads/create`, `/boost`, `/messaging`, `/call` and `/ctwa` now use `publish_timeout` (300s). The MCP tools for `create`, `messaging`, `call` and `ctwa` send an `Idempotency-Key` derived from their arguments, so an identical call within 24 hours returns the first ad. `boost` keeps the API's own duplicate check, which a key would turn off.
- **Other long POSTs still timed out at 30 seconds while the work finished on the server.** In a week 69% of ad video uploads, 25% of ad duplicates and 7% of post retries outlasted the default, so the caller saw an error for something that succeeded. `POST /v1/ads/videos`, `/v1/media/prepare`, `/v1/ads/{id}/duplicate`, `/v1/ads/ad-sets/{id}/duplicate`, `/v1/ads/campaigns/{id}/duplicate` and `/v1/posts/{id}/retry` now use `publish_timeout` (300s). `posts_retry_all_failed` stops after 5 minutes and says how many posts it did not attempt.
- **The hosted MCP server lost log lines to Railway's limit of 500 per second.** About 124,000 lines were dropped in 6 hours, `mcp_tool_call` included, every time a delayed log stream caught up. Access lines now appear only for 5xx, FastMCP's INFO lines are off, expected tool failures print no traceback, invalid-argument warnings no longer carry the customer's values, and the log thread writes at most 100 records per second. `mcp_tool_call` now has a `ts` field, so stream lag stays measurable. `--debug` keeps the full output.
- **A slow log stream could stop the hosted MCP server.** Log writes ran on the event loop, so a blocked stdout froze every request. They now go through a background thread and a bounded queue, and client disconnects are no longer logged as error tracebacks.
- **The hosted MCP server failed on workspaces with tens of thousands of accounts.** `accounts_list`, `profiles_list`, `_resolve_account` and the ChatGPT surface asked for every account or profile on each call, which the API cannot serialize at that size. They now request one bounded page with server-side filters and hand back a cursor, and a post with an `account_id` no longer lists accounts first: `POST /v1/posts` already rejects an id on another platform or outside the caller's scope.
- **The ChatGPT MCP server hid Threads accounts.** `_is_posting_account` dropped every platform ending in "ads" to keep ad connections out, and "threads" ends in "ads", so `list_social_accounts` omitted Threads accounts and `validate_post`, `schedule_post` and `publish_post_now` rejected their ids with "Unknown account id". Ad platforms are now an explicit list.
- **DELETE operations with a request body sent no body.** The generator emitted `_delete(path, params=...)` for every DELETE and dropped the body kwargs, so calls like `remove_campaign_assets(...)` reached the API empty and failed with `invalid_json_body`. DELETE methods now build the payload and send it as JSON (`_delete` / `_adelete` take `data`).
- **MCP tool parameters that take a list of objects (or an object) did not say which keys go inside.** `updates`, `campaigns` and similar were typed `list[dict[str, Any]]` with no keys, so agents had to guess. The parameter description now lists each key with its type, whether it is required and its description, one level of nested object keys included.
- **A POST that timed out client-side could be silently replayed, creating a duplicate live post.** `_request_with_retry` (and its async twin) retried every transient error identically, including `httpx.TimeoutException` on a POST. A timeout only means the client gave up waiting - the server may have finished the request anyway - so replaying it can create a second copy of whatever the first attempt already did. Hit in practice on a `publishNow` create: the server-side publish took 222s against `BaseClient.DEFAULT_TIMEOUT`'s 30s, httpx aborted while the server kept working, and the retry loop fired a second identical POST. The SDK sent no request id, so the server couldn't recognize the replay, and its content-hash dedup answered the replay with a 409 while the original request was still live - so the customer saw a failure for a post that had actually published, retried by hand with a one-character caption change to dodge the dedup, and ended up with two live posts. Two independent fixes: (1) every request now carries an `x-request-id` header, minted once per call and reused across retry attempts, so the server can recognize a replay when one does happen; (2) a POST that times out is no longer retried at all - it raises immediately with a message naming the duplicate-post risk, because the server's content-hash dedup can still race ahead of its idempotency check even with a matching request id. `publishNow` creates also get a much longer timeout (`publish_timeout`, default 300s, configurable on `Zernio(...)`) than the SDK default (`timeout`, default 30s), since a publish-now create runs the whole cross-platform publish synchronously inside the request. PUT, PATCH, and DELETE are unaffected - they're idempotent by contract and stay retryable on timeout. Known gaps, left alone here and tracked for follow-up: 5xx responses are never retried, and `PUT /v1/posts/{id}` with `publishNow` has the same synchronous-publish timeout exposure as create.
- **MCP `accounts_get_follower_stats` returned only the account name, dropping the follower count and daily series.** The shared `_format_response` helper pattern-matches on the response shape, and `FollowerStatsResponse` has an `accounts` attribute, so it fell into the generic account-list branch that prints only `- {platform}: {username}` and silently discarded `currentFollowers`, `growth`, and the daily `stats` series. Hit in practice by a developer pulling LinkedIn org follower stats (data was present server-side: latest count plus a week of daily snapshots), who saw only the account name come back through the tool. `_format_response` now checks for a `stats` attribute (unique to `FollowerStatsResponse` among all response models) BEFORE the generic `accounts` branch and returns the full `model_dump_json(by_alias=True, exclude_none=True)`, so the count, growth, and series reach the LLM losslessly. Fixed in both the emitted `generated_tools.py` and the `generate_mcp_tools.py` template so a future regen keeps it. Two regression tests added in `tests/test_integration.py`. (The related model gap, `FollowerStatsResponse` missing `stats`/`granularity`, was already corrected on `develop` by an earlier OpenAPI regen, so no model change was needed here.)

## [1.4.49]

### Fixed
- **1.4.48 was a regression: PATCH methods broke again.** The auto-regen workflow runs on `develop`, but the `_patch` / `_apatch` fix from 1.4.47 only landed on `main`. When `develop`'s next regen built 1.4.48 (against an updated OpenAPI spec that added `requestBody` blocks for `updateSequence` / `updateBroadcast`), it picked up `develop`'s **old** `base.py` without `_patch`, so any 1.4.48 customer who upgraded got `AttributeError` on every PATCH call again. 1.4.49 merges `develop` into `main` (keeping `main`'s `_patch` / `_apatch`) so the published wheel carries **both** fixes: the missing PATCH method **and** the new body kwargs on `update_sequence(...)` / `update_broadcast(...)`. Skip 1.4.48 — upgrade straight from 1.4.47 to 1.4.49.

## [1.4.47]

### Fixed
- **Every PATCH endpoint was broken end-to-end.** `BaseClient` exposed `_get`, `_post`, `_put`, `_delete` but never defined `_patch` (or its async counterpart `_apatch`), while the resource generator happily emitted `self._client._patch(...)` calls. Any call into a PATCH endpoint raised `AttributeError: 'Zernio' object has no attribute '_patch'` before a request was sent. Hit in practice on `contacts.update_contact` (caught when a customer tried to add a tag from the MCP), but the same bug took down `update_comment_automation`, `update_custom_field`, `update_lead_form`, `update_whats_app_template`, `update_whats_app_flow`, `update_discord_settings`, `update_google_business_place_action`, `edit_inbox_message`, `configure_tik_tok_ads_brand_identity`, `complete_telegram_connect`, `update_sequence`, and `update_broadcast` (sync + async = 26 methods total). `BaseClient` now defines `_patch` / `_apatch` mirroring `_put` / `_aput`, with a `params=` kwarg so the one query-only PATCH (`complete_telegram_connect`) keeps working. Regression test in `tests/test_patch_methods.py` exercises body-bearing and query-only PATCH through the resource layer against a mocked HTTP client, so future codegen drifts can't silently reintroduce this. (Originally targeted 1.4.6 on `main`; that tag had already been taken by an auto-regen on `develop`, so this fix ships as 1.4.47 after merging `develop` into `main`.)

## [1.4.5]

### Fixed
- **Optional scalar params no longer ship zero values to the API.** The MCP autogenerator was emitting `0` / `0.0` / `""` / `False` as defaults for optional scalars without OpenAPI-declared defaults, which the SDK's `_build_payload` couldn't filter (it only drops `None`). The literal `0.0` then tripped Zod's `z.number().positive().optional()` validators server-side, surfacing as `[400] Number must be greater than 0` even when the field was genuinely optional. Hit in practice on `ads_create_standalone_ad` for Google Search campaigns where `roas_average_floor` defaulted to `0.0` and was forwarded into the API. Optional scalars now default to `None` (typed as `T | None`) so unset fields are dropped before reaching the server. OpenAPI-declared defaults (e.g. `campaign_type="display"`, `gender="all"`) are still respected.
- **`LateAPIError` now surfaces field names and stable error codes.** The API returns `{error, type, code, param}` on validation failures but the SDK was reading `error_data.get("details")` (a key the API doesn't send), so `param` was always lost. The SDK now stores the full envelope in `details`, and `__str__` formats as `[400] {message} (field: {param}; code: {code})` when those are present. Direct fix for Hein's "the error doesn't identify the offending field" feedback.

## [1.4.2]

### Fixed
- Merged the multi-account routing fix (1.4.0, originally landed on `main`) and the array/object schema fix (1.4.1, also `main`) into the `develop` branch so the next OpenAPI auto-regen doesn't reintroduce the bugs. Develop now has both fixes applied on top of its accumulated auto-regen content (new endpoints up through v1.3.120). No new behavioural changes beyond 1.4.1.
- Generator now combines `develop`'s param/tool-name dedupe (prevents duplicate-kwarg SyntaxErrors and F811 lint failures) with `main`'s `$ref`/`allOf` schema resolution and `list[T]`/`dict[str, Any]` typing. With develop's newer OpenAPI spec, this means newer fields on `ads_create_standalone_ad` (`cities`, `regions`, `creatives`, `images`, `video`, `brand_identity`, `promoted_object`) are now properly typed alongside the original four (`keywords`, `countries`, `additional_headlines`, `additional_descriptions`).

## [1.4.1]

### Fixed
- **Autogenerated MCP tools no longer collapse `array` and `object` schemas to `str`.** Fields like `keywords`, `countries`, `additional_headlines`, `additional_descriptions` on `ads_create_standalone_ad` (and the equivalents across every autogenerated tool) were declared as `str` and forwarded straight into the SDK, which then rejected the request with `Expected array, received string`. They now use the correct Python types (`list[str] | None`, `list[dict[str, Any]] | None`, `dict[str, Any] | None`) so FastMCP advertises the right shape to LLMs and the SDK receives native containers.
- The generator now dereferences `$ref`, `allOf`, and same-type `oneOf`/`anyOf` wrappers when reading a schema's type. Without this, properties like `posts_create_post.tiktokSettings`, `posts_create_post.facebookSettings`, `posts_create_post.recycling`, and array-of-$ref fields like `createWhatsAppTemplate.components`, `createQueueSlot.slots`, `sendConversions.events`, `updateGoogleBusinessFoodMenus.menus`, and `sendPrivateReplyToComment.buttons` would still have leaked through as `str`.

## [1.4.0]

### Fixed
- **MCP multi-account routing (silent-wrong-account bug).** `posts_create`, `posts_publish_now`, `posts_cross_post`, and `accounts_get` previously fell back to the first matching account (`matching[0]`) when the user had more than one account on the requested platform. Agency / multi-client setups could see posts land on the wrong account with no warning. These tools now return an explicit error listing the candidate account IDs when the selection is ambiguous, and require the caller to disambiguate.

### Added
- `account_id` and `profile_id` parameters on `posts_create` and `posts_publish_now` for explicit target selection.
- `account_ids` (parallel to `platforms`) and `profile_id` parameters on `posts_cross_post`. Repeating a platform with different IDs is supported (e.g. cross-posting to two Twitter accounts in one call).
- `posts_create_post` exposed as an autogenerated tool alongside the simplified `posts_create`. It mirrors the full REST `createPost` surface (nested `platforms` array with `customContent`, `customMedia`, `scheduledFor`, `platformSpecificData`) for power users who need per-target customisation.
- Top-level multi-account workflow guidance in the MCP server instructions so LLMs learn the disambiguation flow once globally.
- Unit tests for the shared `_resolve_account` helper covering account-id, profile-id, ambiguous, and not-found paths.

## [Older Unreleased entries]

### Added
- MCP HTTP server now exposes the modern **Streamable HTTP** transport at `POST /mcp` (in addition to the existing SSE transport at `GET /sse`). Streamable HTTP is recommended for new clients (Claude Code, `mcp-remote`, etc.) because it is not affected by the idle-connection drops that affect long-lived SSE connections behind proxies.
- Streamable HTTP runs in stateless mode — each request is fully independent and authenticated separately via the `Authorization: Bearer` header.

### Changed
- Bumped minimum `mcp` SDK version to `>=1.8.0` (required for `StreamableHTTPSessionManager`).
- Server `transport` field in the root info endpoint now reports `"sse+streamable-http"`.

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
