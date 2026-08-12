"""
Auto-generated MCP tool handlers.

DO NOT EDIT - Run `python scripts/generate_mcp_tools.py` to regenerate.
"""

from __future__ import annotations

from typing import Any

from mcp.types import ToolAnnotations


def _enum_str(value: Any) -> str:
    """Extract string value from an enum or return as-is if already a string.

    The auto-generated models use plain Enum classes (Platform5, etc.) whose
    str() returns 'Platform5.TWITTER' instead of 'twitter'. This helper
    normalises any enum value to its underlying string.
    """
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if hasattr(value, "value"):
        return str(value.value)
    return str(value)


def _format_response(response: Any) -> str:
    """Format SDK response for MCP output."""
    if response is None:
        return "Success"
    if hasattr(response, "__dict__"):
        # Handle response objects
        if hasattr(response, "posts") and response.posts:
            posts = response.posts
            lines = [f"Found {len(posts)} post(s):"]
            for p in posts[:10]:
                content = str(getattr(p, "content", ""))[:50]
                status = _enum_str(getattr(p, "status", "unknown"))
                lines.append(f"- [{status}] {content}...")
            return "\n".join(lines)
        if hasattr(response, "accounts") and hasattr(response, "stats"):
            # Follower-stats: lossless structured output for the LLM. Must precede the
            # generic 'accounts' branch (which would print only 'platform: username' and
            # drop currentFollowers/growth and the daily series). 'stats' attr is unique
            # to FollowerStatsResponse, so no other tool's response matches.
            return response.model_dump_json(by_alias=True, exclude_none=True)
        if hasattr(response, "accounts") and response.accounts:
            accs = response.accounts
            lines = [f"Found {len(accs)} account(s):"]
            for a in accs[:10]:
                platform = _enum_str(getattr(a, "platform", "?"))
                username = getattr(a, "username", None) or getattr(
                    a, "displayName", "?"
                )
                lines.append(f"- {platform}: {username}")
            return "\n".join(lines)
        if hasattr(response, "profiles") and response.profiles:
            profiles = response.profiles
            lines = [f"Found {len(profiles)} profile(s):"]
            for p in profiles[:10]:
                name = getattr(p, "name", "Unnamed")
                lines.append(f"- {name}")
            return "\n".join(lines)
        if hasattr(response, "post") and response.post:
            p = response.post
            return f"Post ID: {getattr(p, 'field_id', 'N/A')}\nStatus: {_enum_str(getattr(p, 'status', 'N/A'))}"
        if hasattr(response, "profile") and response.profile:
            p = response.profile
            return f"Profile: {getattr(p, 'name', 'N/A')} (ID: {getattr(p, 'field_id', 'N/A')})"
    return str(response)


def register_generated_tools(mcp, _get_client):
    """Register all auto-generated tools with the MCP server."""

    # ACCOUNT_GROUPS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List groups",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def account_groups_list_account_groups() -> str:
        """List groups"""
        client = _get_client()
        try:
            response = client.account_groups.list_account_groups()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create group",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def account_groups_create_account_group(
        name: str, account_ids: list[str] | None, profile_id: str | None = None
    ) -> str:
        """Create group

            Args:
                name: (required)
                account_ids: (required)
                profile_id: Deprecated. Accepted for backward compatibility but ignored.
        Groups are no longer scoped to a single profile."""
        client = _get_client()
        try:
            response = client.account_groups.create_account_group(
                name=name, account_ids=account_ids, profile_id=profile_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update group",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def account_groups_update_account_group(
        group_id: str, name: str | None = None, account_ids: list[str] | None = None
    ) -> str:
        """Update group

        Args:
            group_id: (required)
            name
            account_ids"""
        client = _get_client()
        try:
            response = client.account_groups.update_account_group(
                group_id=group_id, name=name, account_ids=account_ids
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete group",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def account_groups_delete_account_group(group_id: str) -> str:
        """Delete group

        Args:
            group_id: (required)"""
        client = _get_client()
        try:
            response = client.account_groups.delete_account_group(group_id=group_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # ACCOUNT_SETTINGS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get FB persistent menu",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def account_settings_get_messenger_menu(account_id: str) -> str:
        """Get FB persistent menu

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.account_settings.get_messenger_menu(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Set FB persistent menu",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def account_settings_set_messenger_menu(
        account_id: str, persistent_menu: list[dict[str, Any]] | None
    ) -> str:
        """Set FB persistent menu

        Args:
            account_id: (required)
            persistent_menu: Persistent menu configuration array (Meta format) (required)"""
        client = _get_client()
        try:
            response = client.account_settings.set_messenger_menu(
                account_id=account_id, persistent_menu=persistent_menu
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete FB persistent menu",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def account_settings_delete_messenger_menu(account_id: str) -> str:
        """Delete FB persistent menu

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.account_settings.delete_messenger_menu(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get IG ice breakers",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def account_settings_get_instagram_ice_breakers(account_id: str) -> str:
        """Get IG ice breakers

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.account_settings.get_instagram_ice_breakers(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Set IG ice breakers",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def account_settings_set_instagram_ice_breakers(
        account_id: str, ice_breakers: list[dict[str, Any]] | None
    ) -> str:
        """Set IG ice breakers

        Args:
            account_id: (required)
            ice_breakers: (required)"""
        client = _get_client()
        try:
            response = client.account_settings.set_instagram_ice_breakers(
                account_id=account_id, ice_breakers=ice_breakers
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete IG ice breakers",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def account_settings_delete_instagram_ice_breakers(account_id: str) -> str:
        """Delete IG ice breakers

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.account_settings.delete_instagram_ice_breakers(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get TG bot commands",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def account_settings_get_telegram_commands(account_id: str) -> str:
        """Get TG bot commands

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.account_settings.get_telegram_commands(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Set TG bot commands",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def account_settings_set_telegram_commands(
        account_id: str, commands: list[dict[str, Any]] | None
    ) -> str:
        """Set TG bot commands

        Args:
            account_id: (required)
            commands: (required)"""
        client = _get_client()
        try:
            response = client.account_settings.set_telegram_commands(
                account_id=account_id, commands=commands
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete TG bot commands",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def account_settings_delete_telegram_commands(account_id: str) -> str:
        """Delete TG bot commands

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.account_settings.delete_telegram_commands(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # ACCOUNTS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List accounts",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_list_accounts(
        profile_id: str | None = None,
        platform: str | None = None,
        status: str | None = None,
        include_over_limit: bool = False,
        page: int | None = None,
        limit: int | None = None,
    ) -> str:
        """List accounts

        Args:
            profile_id: Filter accounts by profile ID. Must be a valid ObjectId.
            platform: Filter accounts by platform (e.g. "instagram", "twitter").
            status: Filter accounts by connection status. `connected` returns healthy accounts; `disconnected` returns accounts that need reconnection (per the same reconnection check surfaced in the dashboard). Omit to return accounts in any status. When combined with page/limit, pagination totals reflect the filtered result set.
            include_over_limit: When true, includes accounts from over-limit profiles.
            page: Page number (1-based). Must be provided together with limit to enable server-side pagination; sending only one of the two returns 400. Omit both for all accounts.
            limit: Page size. Must be provided together with page; sending only one of the two returns 400."""
        client = _get_client()
        try:
            response = client.accounts.list_accounts(
                profile_id=profile_id,
                platform=platform,
                status=status,
                include_over_limit=include_over_limit,
                page=page,
                limit=limit,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get follower stats",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_get_follower_stats(
        account_ids: str | None = None,
        profile_id: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        granularity: str = "daily",
    ) -> str:
        """Get follower stats

        Args:
            account_ids: Comma-separated list of account IDs (optional, defaults to all user's accounts)
            profile_id: Filter by profile ID
            from_date: Start date in YYYY-MM-DD format (defaults to 30 days ago)
            to_date: End date in YYYY-MM-DD format (defaults to today)
            granularity: Data aggregation level"""
        client = _get_client()
        try:
            response = client.accounts.get_follower_stats(
                account_ids=account_ids,
                profile_id=profile_id,
                from_date=from_date,
                to_date=to_date,
                granularity=granularity,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update account",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_update_account(
        account_id: str,
        username: str | None = None,
        display_name: str | None = None,
        x_capabilities: dict[str, Any] | None = None,
    ) -> str:
        """Update account

            Args:
                account_id: (required)
                username
                display_name
                x_capabilities: X/Twitter only. Per-account opt-in toggles for background API
        operations that incur X API pass-through costs. Each call is
        billed via Metronome at the X tier rate. Either field can be
        sent independently; omitted fields are unchanged."""
        client = _get_client()
        try:
            response = client.accounts.update_account(
                account_id=account_id,
                username=username,
                display_name=display_name,
                x_capabilities=x_capabilities,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Move account to another profile",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_move_account_to_profile(account_id: str, profile_id: str) -> str:
        """Move account to another profile

        Args:
            account_id: (required)
            profile_id: Target profile ID (must be a valid ObjectId and owned by the same user as the account). (required)"""
        client = _get_client()
        try:
            response = client.accounts.move_account_to_profile(
                account_id=account_id, profile_id=profile_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Disconnect account",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_delete_account(account_id: str) -> str:
        """Disconnect account

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.accounts.delete_account(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Check accounts health",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_get_all_accounts_health(
        profile_id: str | None = None,
        platform: str | None = None,
        status: str | None = None,
    ) -> str:
        """Check accounts health

        Args:
            profile_id: Filter by profile ID
            platform: Filter by platform
            status: Filter by health status"""
        client = _get_client()
        try:
            response = client.accounts.get_all_accounts_health(
                profile_id=profile_id, platform=platform, status=status
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Check account health",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_get_account_health(account_id: str) -> str:
        """Check account health

        Args:
            account_id: The account ID to check (required)"""
        client = _get_client()
        try:
            response = client.accounts.get_account_health(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Check whether an Instagram user follows the account",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_get_instagram_follow_status(
        account_id: str, user_id: str, refresh: bool | None = None
    ) -> str:
        """Check whether an Instagram user follows the account

        Args:
            account_id: Instagram account ID (required)
            user_id: Instagram-scoped user id (IGSID) from a webhook payload (required)
            refresh: Bypass the cache and re-query Meta"""
        client = _get_client()
        try:
            response = client.accounts.get_instagram_follow_status(
                account_id=account_id, user_id=user_id, refresh=refresh
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get TikTok creator info",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_get_tik_tok_creator_info(
        account_id: str, media_type: str = "video"
    ) -> str:
        """Get TikTok creator info

        Args:
            account_id: The TikTok account ID (required)
            media_type: The media type to get creator info for (affects available interaction settings)"""
        client = _get_client()
        try:
            response = client.accounts.get_tik_tok_creator_info(
                account_id=account_id, media_type=media_type
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get reviews",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_get_google_business_reviews(
        account_id: str,
        location_id: str | None = None,
        page_size: int = 50,
        page_token: str | None = None,
    ) -> str:
        """Get reviews

        Args:
            account_id: The Zernio account ID (from /v1/accounts) (required)
            location_id: Override which location to query. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs.
            page_size: Number of reviews to fetch per page (max 50)
            page_token: Pagination token from previous response"""
        client = _get_client()
        try:
            response = client.accounts.get_google_business_reviews(
                account_id=account_id,
                location_id=location_id,
                page_size=page_size,
                page_token=page_token,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get food menus",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_get_google_business_food_menus(
        account_id: str, location_id: str | None = None
    ) -> str:
        """Get food menus

        Args:
            account_id: The Zernio account ID (from /v1/accounts) (required)
            location_id: Override which location to query. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs."""
        client = _get_client()
        try:
            response = client.accounts.get_google_business_food_menus(
                account_id=account_id, location_id=location_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update food menus",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_update_google_business_food_menus(
        account_id: str,
        menus: list[dict[str, Any]] | None,
        location_id: str | None = None,
        update_mask: str | None = None,
    ) -> str:
        """Update food menus

        Args:
            account_id: The Zernio account ID (from /v1/accounts) (required)
            location_id: Override which location to target. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs.
            menus: Array of food menus to set (required)
            update_mask: Field mask for partial updates (e.g. "menus")"""
        client = _get_client()
        try:
            response = client.accounts.update_google_business_food_menus(
                account_id=account_id,
                location_id=location_id,
                menus=menus,
                update_mask=update_mask,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get location details",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_get_google_business_location_details(
        account_id: str, location_id: str | None = None, read_mask: str | None = None
    ) -> str:
        """Get location details

            Args:
                account_id: The Zernio account ID (from /v1/accounts) (required)
                location_id: Override which location to query. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs.
                read_mask: Comma-separated fields to return. Available: name, title, phoneNumbers, categories, storefrontAddress, websiteUri, regularHours, specialHours, serviceArea, serviceItems, profile, openInfo, metadata, moreHours.
        `title` and `metadata` are always included in the response so the `location` summary block can be populated, even if you omit them here.
        Note: `location` is a derived response field, not a Google readMask value, passing it returns 400."""
        client = _get_client()
        try:
            response = client.accounts.get_google_business_location_details(
                account_id=account_id, location_id=location_id, read_mask=read_mask
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update location details",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_update_google_business_location_details(
        account_id: str,
        update_mask: str,
        location_id: str | None = None,
        regular_hours: dict[str, Any] | None = None,
        special_hours: dict[str, Any] | None = None,
        profile: dict[str, Any] | None = None,
        website_uri: str | None = None,
        phone_numbers: dict[str, Any] | None = None,
        categories: dict[str, Any] | None = None,
        service_items: list[dict[str, Any]] | None = None,
    ) -> str:
        """Update location details

        Args:
            account_id: The Zernio account ID (from /v1/accounts) (required)
            location_id: Override which location to target. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs.
            update_mask: Required. Comma-separated fields to update (e.g. 'regularHours', 'specialHours', 'profile.description', 'categories', 'serviceItems'). Any valid Google Business Information API updateMask field is supported. (required)
            regular_hours
            special_hours
            profile
            website_uri
            phone_numbers
            categories: Primary and additional business categories. Use updateMask='categories' to update.
            service_items: Services offered by the business. Use updateMask='serviceItems' to update."""
        client = _get_client()
        try:
            response = client.accounts.update_google_business_location_details(
                account_id=account_id,
                location_id=location_id,
                update_mask=update_mask,
                regular_hours=regular_hours,
                special_hours=special_hours,
                profile=profile,
                website_uri=website_uri,
                phone_numbers=phone_numbers,
                categories=categories,
                service_items=service_items,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List media",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_list_google_business_media(
        account_id: str,
        location_id: str | None = None,
        page_size: int = 100,
        page_token: str | None = None,
    ) -> str:
        """List media

        Args:
            account_id: (required)
            location_id: Override which location to query. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs.
            page_size: Number of items to return (max 100)
            page_token: Pagination token from previous response"""
        client = _get_client()
        try:
            response = client.accounts.list_google_business_media(
                account_id=account_id,
                location_id=location_id,
                page_size=page_size,
                page_token=page_token,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Upload photo",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_create_google_business_media(
        account_id: str,
        source_url: str,
        location_id: str | None = None,
        media_format: str = "PHOTO",
        description: str | None = None,
        category: str | None = None,
    ) -> str:
        """Upload photo

        Args:
            account_id: (required)
            location_id: Override which location to target. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs.
            source_url: Publicly accessible image URL (required)
            media_format
            description: Photo description
            category: Where the photo appears on the listing"""
        client = _get_client()
        try:
            response = client.accounts.create_google_business_media(
                account_id=account_id,
                location_id=location_id,
                source_url=source_url,
                media_format=media_format,
                description=description,
                category=category,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete photo",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_delete_google_business_media(
        account_id: str, media_id: str, location_id: str | None = None
    ) -> str:
        """Delete photo

        Args:
            account_id: (required)
            location_id: Override which location to target. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs.
            media_id: The media item ID to delete (required)"""
        client = _get_client()
        try:
            response = client.accounts.delete_google_business_media(
                account_id=account_id, location_id=location_id, media_id=media_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get attribute metadata",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_get_gmb_attribute_metadata(
        account_id: str,
        location_id: str | None = None,
        category_name: str | None = None,
        region_code: str | None = None,
        language_code: str | None = None,
        page_size: int | None = None,
        page_token: str | None = None,
    ) -> str:
        """Get attribute metadata

        Args:
            account_id: (required)
            location_id: GBP location ID (e.g. "6257659026299438786"). If omitted, uses the account's stored selectedLocationId. Mutually exclusive with categoryName.
            category_name: Category resource name, must start with "categories/" (e.g. "categories/gcid:plumber"). Required together with regionCode. Mutually exclusive with locationId.
            region_code: BCP-47 region code (e.g. "US", "ES"). Required when categoryName is provided.
            language_code: BCP-47 language code for display names (e.g. "en", "es"). Optional when categoryName is provided. Omitted from the Google call when not supplied.
            page_size: Maximum number of attribute metadata items to return. Google defaults to 200.
            page_token: Pagination token from a previous response's nextPageToken field."""
        client = _get_client()
        try:
            response = client.accounts.get_gmb_attribute_metadata(
                account_id=account_id,
                location_id=location_id,
                category_name=category_name,
                region_code=region_code,
                language_code=language_code,
                page_size=page_size,
                page_token=page_token,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get attributes",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_get_google_business_attributes(
        account_id: str, location_id: str | None = None
    ) -> str:
        """Get attributes

        Args:
            account_id: (required)
            location_id: Override which location to query. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs."""
        client = _get_client()
        try:
            response = client.accounts.get_google_business_attributes(
                account_id=account_id, location_id=location_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update attributes",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_update_google_business_attributes(
        account_id: str,
        attributes: list[dict[str, Any]] | None,
        attribute_mask: str,
        location_id: str | None = None,
    ) -> str:
        """Update attributes

        Args:
            account_id: (required)
            location_id: Override which location to target. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs.
            attributes: (required)
            attribute_mask: Comma-separated attribute names to update (e.g. 'has_delivery,has_takeout') (required)"""
        client = _get_client()
        try:
            response = client.accounts.update_google_business_attributes(
                account_id=account_id,
                location_id=location_id,
                attributes=attributes,
                attribute_mask=attribute_mask,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List action links",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_list_google_business_place_actions(
        account_id: str,
        location_id: str | None = None,
        page_size: int = 100,
        page_token: str | None = None,
    ) -> str:
        """List action links

        Args:
            account_id: (required)
            location_id: Override which location to query. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs.
            page_size
            page_token"""
        client = _get_client()
        try:
            response = client.accounts.list_google_business_place_actions(
                account_id=account_id,
                location_id=location_id,
                page_size=page_size,
                page_token=page_token,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create action link",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_create_google_business_place_action(
        account_id: str,
        uri: str,
        place_action_type: str,
        location_id: str | None = None,
    ) -> str:
        """Create action link

        Args:
            account_id: (required)
            location_id: Override which location to target. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs.
            uri: The action URL (required)
            place_action_type: Type of action (required)"""
        client = _get_client()
        try:
            response = client.accounts.create_google_business_place_action(
                account_id=account_id,
                location_id=location_id,
                uri=uri,
                place_action_type=place_action_type,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete action link",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_delete_google_business_place_action(
        account_id: str, name: str, location_id: str | None = None
    ) -> str:
        """Delete action link

        Args:
            account_id: (required)
            location_id: Override which location to target. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs.
            name: The resource name of the place action link (e.g. locations/123/placeActionLinks/456) (required)"""
        client = _get_client()
        try:
            response = client.accounts.delete_google_business_place_action(
                account_id=account_id, location_id=location_id, name=name
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update action link",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_update_google_business_place_action(
        account_id: str,
        name: str,
        location_id: str | None = None,
        uri: str | None = None,
        place_action_type: str | None = None,
    ) -> str:
        """Update action link

        Args:
            account_id: (required)
            location_id: Override which location to target. If omitted, uses the account's selected location.
            name: Resource name of the place action link (e.g. locations/123/placeActionLinks/456) (required)
            uri: New action URL. At least one of uri or placeActionType is required (enforced server-side; not modeled as anyOf because required-only anyOf branches break SDK generators).
            place_action_type: New action type"""
        client = _get_client()
        try:
            response = client.accounts.update_google_business_place_action(
                account_id=account_id,
                location_id=location_id,
                name=name,
                uri=uri,
                place_action_type=place_action_type,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Batch get reviews",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_batch_get_google_business_reviews(
        account_id: str,
        location_names: list[str] | None,
        page_size: int = 50,
        page_token: str | None = None,
        order_by: str = "updateTime desc",
    ) -> str:
        """Batch get reviews

        Args:
            account_id: (required)
            location_names: Array of full location resource names (e.g. ['accounts/123/locations/456']). Max 50 per request (Google's batchGetReviews cap); chunk larger sets into multiple requests. (required)
            page_size: Number of reviews per page (max 50)
            page_token: Pagination token from previous response
            order_by: Sort order requested from Google. Defaults to 'updateTime desc' (newest first), which allows early-stopping pagination once results cross your date window."""
        client = _get_client()
        try:
            response = client.accounts.batch_get_google_business_reviews(
                account_id=account_id,
                location_names=location_names,
                page_size=page_size,
                page_token=page_token,
                order_by=order_by,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Reply to a review",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_reply_to_google_business_review(
        account_id: str, review_id: str, comment: str
    ) -> str:
        """Reply to a review

        Args:
            account_id: The Zernio account ID (from /v1/accounts) (required)
            review_id: The review ID portion (e.g. "AIe9_BGx1234567890"), not the full resource name (required)
            comment: The reply text to post on the review. Must be non-empty. (required)"""
        client = _get_client()
        try:
            response = client.accounts.reply_to_google_business_review(
                account_id=account_id, review_id=review_id, comment=comment
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete a review reply",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_delete_google_business_review_reply(
        account_id: str, review_id: str
    ) -> str:
        """Delete a review reply

        Args:
            account_id: The Zernio account ID (from /v1/accounts) (required)
            review_id: The review ID portion (e.g. "AIe9_BGx1234567890"), not the full resource name (required)"""
        client = _get_client()
        try:
            response = client.accounts.delete_google_business_review_reply(
                account_id=account_id, review_id=review_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Resolve LinkedIn mention",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_get_linked_in_mentions(
        account_id: str, url: str, display_name: str | None = None
    ) -> str:
        """Resolve LinkedIn mention

        Args:
            account_id: The LinkedIn account ID (required)
            url: LinkedIn profile URL, company URL, or vanity name. (required)
            display_name: Exact display name as shown on LinkedIn. Required for person mentions to be clickable. Optional for org mentions."""
        client = _get_client()
        try:
            response = client.accounts.get_linked_in_mentions(
                account_id=account_id, url=url, display_name=display_name
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get Slack account settings",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def accounts_get_slack_settings(account_id: str) -> str:
        """Get Slack account settings

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.accounts.get_slack_settings(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update Slack account settings",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_update_slack_settings(
        account_id: str,
        default_username: str | None = None,
        default_icon_url: str | None = None,
    ) -> str:
        """Update Slack account settings

        Args:
            account_id: (required)
            default_username: Author name shown on posts. Empty string clears it.
            default_icon_url: Author avatar image URL. Empty string clears it."""
        client = _get_client()
        try:
            response = client.accounts.update_slack_settings(
                account_id=account_id,
                default_username=default_username,
                default_icon_url=default_icon_url,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # AD_ACCOUNTS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List comments on an ad",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_get_ad_comments(
        ad_id: str,
        placement: str | None = None,
        limit: int = 25,
        cursor: str | None = None,
    ) -> str:
        """List comments on an ad

        Args:
            ad_id: Internal Zernio ad ID (ObjectId). (required)
            placement: Which side of the ad to return comments for. Omit to default to the Instagram side when present, else Facebook. Returns ad_not_commentable if the ad has no such placement.
            limit
            cursor: Pagination cursor from a previous response."""
        client = _get_client()
        try:
            response = client.ad_accounts.get_ad_comments(
                ad_id=ad_id, placement=placement, limit=limit, cursor=cursor
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List TikTok Business Centers",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_list_ads_business_centers(account_id: str) -> str:
        """List TikTok Business Centers

        Args:
            account_id: ID of the `tiktokads` (or parent `tiktok` posting) SocialAccount (required)"""
        client = _get_client()
        try:
            response = client.ad_accounts.list_ads_business_centers(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Ad account change / audit log",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_get_ads_activity_log(
        account_id: str,
        ad_account_id: str,
        since: str | None = None,
        until: str | None = None,
        object_id: str | None = None,
        limit: int = 50,
        after: str | None = None,
    ) -> str:
        """Ad account change / audit log

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)
            since: Start of range (YYYY-MM-DD).
            until: End of range (YYYY-MM-DD).
            object_id: Client-side filter to one Meta object id (campaign, ad set or ad).
            limit: Rows per page
            after: Cursor from paging.after of the previous page."""
        client = _get_client()
        try:
            response = client.ad_accounts.get_ads_activity_log(
                account_id=account_id,
                ad_account_id=ad_account_id,
                since=since,
                until=until,
                object_id=object_id,
                limit=limit,
                after=after,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="A/B tests and lift studies",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_list_ad_studies(
        account_id: str,
        ad_account_id: str,
        fields: str | None = None,
        limit: int = 25,
        after: str | None = None,
    ) -> str:
        """A/B tests and lift studies

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)
            fields: Comma-separated Graph field override (supports nested {} projections).
            limit: Rows per page
            after: Cursor from paging.after of the previous page."""
        client = _get_client()
        try:
            response = client.ad_accounts.list_ad_studies(
                account_id=account_id,
                ad_account_id=ad_account_id,
                fields=fields,
                limit=limit,
                after=after,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Businesses list",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_list_meta_businesses(
        account_id: str, limit: int = 25, after: str | None = None
    ) -> str:
        """Businesses list

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            limit: Rows per page
            after: Cursor from paging.after of the previous page."""
        client = _get_client()
        try:
            response = client.ad_accounts.list_meta_businesses(
                account_id=account_id, limit=limit, after=after
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Ad labels",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_list_ad_labels(
        account_id: str, ad_account_id: str, limit: int = 25, after: str | None = None
    ) -> str:
        """Ad labels

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)
            limit: Rows per page
            after: Cursor from paging.after of the previous page."""
        client = _get_client()
        try:
            response = client.ad_accounts.list_ad_labels(
                account_id=account_id,
                ad_account_id=ad_account_id,
                limit=limit,
                after=after,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="High demand periods / budget schedules",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_list_high_demand_periods(
        account_id: str,
        campaign_id: str | None = None,
        ad_set_id: str | None = None,
        limit: int = 25,
        after: str | None = None,
    ) -> str:
        """High demand periods / budget schedules

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            campaign_id: Platform campaign id. Exactly one of campaignId / adSetId.
            ad_set_id: Platform ad set id. Exactly one of campaignId / adSetId.
            limit: Rows per page
            after: Cursor from paging.after of the previous page."""
        client = _get_client()
        try:
            response = client.ad_accounts.list_high_demand_periods(
                account_id=account_id,
                campaign_id=campaign_id,
                ad_set_id=ad_set_id,
                limit=limit,
                after=after,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Schedule a budget increase",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_accounts_create_high_demand_period(
        account_id: str,
        budget_value: float,
        budget_value_type: str,
        time_start: int,
        time_end: int,
        campaign_id: str | None = None,
        ad_set_id: str | None = None,
        recurrence_type: str | None = None,
        currency: str | None = None,
    ) -> str:
        """Schedule a budget increase

        Args:
            account_id: Zernio SocialAccount id used to resolve the Meta token. (required)
            campaign_id: Platform campaign id. Exactly one of campaignId / adSetId.
            ad_set_id: Platform ad set id. Exactly one of campaignId / adSetId.
            budget_value: With ABSOLUTE, a budget in the ad account's currency in WHOLE units (50 = $50.00). With MULTIPLIER, a factor of the existing budget (2 = double it) and NOT a currency amount. (required)
            budget_value_type: (required)
            time_start: Unix seconds, on a 15-minute boundary (:00, :15, :30, :45). (required)
            time_end: Unix seconds, on a 15-minute boundary and after timeStart. (required)
            recurrence_type
            currency: Ad account currency, for the ABSOLUTE minor-unit conversion. Ignored for MULTIPLIER."""
        client = _get_client()
        try:
            response = client.ad_accounts.create_high_demand_period(
                account_id=account_id,
                campaign_id=campaign_id,
                ad_set_id=ad_set_id,
                budget_value=budget_value,
                budget_value_type=budget_value_type,
                time_start=time_start,
                time_end=time_end,
                recurrence_type=recurrence_type,
                currency=currency,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List value rule sets",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_list_value_rule_sets(
        account_id: str, ad_account_id: str, limit: int = 25, after: str | None = None
    ) -> str:
        """List value rule sets

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)
            limit: Rows per page
            after: Cursor from paging.after of the previous page. Meta does not document paging on this edge; `after` comes back null when it omits cursors."""
        client = _get_client()
        try:
            response = client.ad_accounts.list_value_rule_sets(
                account_id=account_id,
                ad_account_id=ad_account_id,
                limit=limit,
                after=after,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a value rule set",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_accounts_create_value_rule_set(
        account_id: str,
        ad_account_id: str,
        name: str,
        rules: list[dict[str, Any]] | None,
    ) -> str:
        """Create a value rule set

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)
            name: (required)
            rules: Evaluated in order; the first matching rule wins. (required)"""
        client = _get_client()
        try:
            response = client.ad_accounts.create_value_rule_set(
                account_id=account_id,
                ad_account_id=ad_account_id,
                name=name,
                rules=rules,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Read a value rule set",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_get_value_rule_set(value_rule_set_id: str, account_id: str) -> str:
        """Read a value rule set

        Args:
            value_rule_set_id: Platform value rule set id. (required)
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)"""
        client = _get_client()
        try:
            response = client.ad_accounts.get_value_rule_set(
                value_rule_set_id=value_rule_set_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Replace a value rule set",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_accounts_update_value_rule_set(
        value_rule_set_id: str,
        account_id: str,
        name: str,
        rules: list[dict[str, Any]] | None,
    ) -> str:
        """Replace a value rule set

        Args:
            value_rule_set_id: Platform value rule set id. (required)
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            name: Required: the update replaces the whole set. (required)
            rules: The COMPLETE rule list. Omitting a rule deletes it on Meta. (required)"""
        client = _get_client()
        try:
            response = client.ad_accounts.update_value_rule_set(
                value_rule_set_id=value_rule_set_id,
                account_id=account_id,
                name=name,
                rules=rules,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete a value rule set",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_accounts_delete_value_rule_set(
        value_rule_set_id: str, account_id: str
    ) -> str:
        """Delete a value rule set

        Args:
            value_rule_set_id: Platform value rule set id. (required)
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)"""
        client = _get_client()
        try:
            response = client.ad_accounts.delete_value_rule_set(
                value_rule_set_id=value_rule_set_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Ad account finances",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_get_ad_account_finance(account_id: str, ad_account_id: str) -> str:
        """Ad account finances

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)"""
        client = _get_client()
        try:
            response = client.ad_accounts.get_ad_account_finance(
                account_id=account_id, ad_account_id=ad_account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List ad accounts",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_list_ad_accounts(
        account_id: str, ad_account_id: str | None = None, limit: int | None = None
    ) -> str:
        """List ad accounts

        Args:
            account_id: Social account ID (required)
            ad_account_id: Filter response to a single platform ad account ID (e.g. `act_123` for Meta, advertiser_id for TikTok). Returns at most one item.
            limit: Clamp the returned `accounts[]` length. Useful for typeahead pickers on agency tokens with hundreds of advertisers."""
        client = _get_client()
        try:
            response = client.ad_accounts.list_ad_accounts(
                account_id=account_id, ad_account_id=ad_account_id, limit=limit
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update ad account settings",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_accounts_update_ad_account(
        account_id: str,
        ad_account_id: str,
        default_dsa_beneficiary: str,
        default_dsa_payor: str | None = None,
    ) -> str:
        """Update ad account settings

        Args:
            account_id: Social account ID (metaads, or a facebook/instagram posting account) (required)
            ad_account_id: Meta ad account ID (act_...) (required)
            default_dsa_beneficiary: Legal entity benefiting from ads on this ad account (required)
            default_dsa_payor: Legal entity paying for ads on this ad account. Defaults to defaultDsaBeneficiary when omitted."""
        client = _get_client()
        try:
            response = client.ad_accounts.update_ad_account(
                account_id=account_id,
                ad_account_id=ad_account_id,
                default_dsa_beneficiary=default_dsa_beneficiary,
                default_dsa_payor=default_dsa_payor,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get ad account DSA defaults",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_get_dsa_defaults(account_id: str, ad_account_id: str) -> str:
        """Get ad account DSA defaults

        Args:
            account_id: Social account ID (metaads, or a facebook/instagram posting account) (required)
            ad_account_id: Meta ad account ID (act_...) (required)"""
        client = _get_client()
        try:
            response = client.ad_accounts.get_dsa_defaults(
                account_id=account_id, ad_account_id=ad_account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List DSA beneficiary/payor suggestions",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_get_dsa_recommendations(account_id: str, ad_account_id: str) -> str:
        """List DSA beneficiary/payor suggestions

        Args:
            account_id: Social account ID (metaads, or a facebook/instagram posting account) (required)
            ad_account_id: Meta ad account ID (act_...) (required)"""
        client = _get_client()
        try:
            response = client.ad_accounts.get_dsa_recommendations(
                account_id=account_id, ad_account_id=ad_account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List custom conversions",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_accounts_list_custom_conversions(account_id: str, ad_account_id: str) -> str:
        """List custom conversions

        Args:
            account_id: Meta ads SocialAccount id. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)"""
        client = _get_client()
        try:
            response = client.ad_accounts.list_custom_conversions(
                account_id=account_id, ad_account_id=ad_account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create or reuse a custom conversion",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_accounts_create_custom_conversion(
        account_id: str,
        ad_account_id: str,
        name: str,
        pixel_id: str,
        custom_event_type: str,
        rule: dict[str, Any] | None,
    ) -> str:
        """Create or reuse a custom conversion

        Args:
            account_id: Meta ads SocialAccount id. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)
            name: Also the reuse key, together with pixelId. (required)
            pixel_id: Meta pixel id (event_source_id). From GET /v1/accounts/{accountId}/tracking-tags. (required)
            custom_event_type: Meta custom_event_type, e.g. LEAD, PURCHASE, OTHER. (required)
            rule: Meta conversion rule, forwarded verbatim. (required)"""
        client = _get_client()
        try:
            response = client.ad_accounts.create_custom_conversion(
                account_id=account_id,
                ad_account_id=ad_account_id,
                name=name,
                pixel_id=pixel_id,
                custom_event_type=custom_event_type,
                rule=rule,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # AD_AUDIENCES

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List custom audiences",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_audiences_list_ad_audiences(
        account_id: str,
        ad_account_id: str,
        platform: str | None = None,
        type: str | None = None,
    ) -> str:
        """List custom audiences

        Args:
            account_id: Social account ID (required)
            ad_account_id: Platform ad account ID (required)
            platform
            type: Filter to one audience type. `saved_targeting` returns stored TargetingSpec audiences; the other types return uploaded/derived audiences."""
        client = _get_client()
        try:
            response = client.ad_audiences.list_ad_audiences(
                account_id=account_id,
                ad_account_id=ad_account_id,
                platform=platform,
                type=type,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create custom audience",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_audiences_create_ad_audience() -> str:
        """Create custom audience"""
        client = _get_client()
        try:
            response = client.ad_audiences.create_ad_audience()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get audience details",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_audiences_get_ad_audience(audience_id: str) -> str:
        """Get audience details

        Args:
            audience_id: (required)"""
        client = _get_client()
        try:
            response = client.ad_audiences.get_ad_audience(audience_id=audience_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update an audience",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_audiences_update_ad_audience(
        audience_id: str,
        name: str | None = None,
        description: str | None = None,
        spec: dict[str, Any] | None = None,
    ) -> str:
        """Update an audience

        Args:
            audience_id: (required)
            name
            description
            spec: Full replacement for the stored targeting spec."""
        client = _get_client()
        try:
            response = client.ad_audiences.update_ad_audience(
                audience_id=audience_id, name=name, description=description, spec=spec
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete custom audience",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_audiences_delete_ad_audience(audience_id: str) -> str:
        """Delete custom audience

        Args:
            audience_id: (required)"""
        client = _get_client()
        try:
            response = client.ad_audiences.delete_ad_audience(audience_id=audience_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Add users to audience",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_audiences_add_users_to_ad_audience(
        audience_id: str, users: list[dict[str, Any]] | None
    ) -> str:
        """Add users to audience

        Args:
            audience_id: (required)
            users: (required)"""
        client = _get_client()
        try:
            response = client.ad_audiences.add_users_to_ad_audience(
                audience_id=audience_id, users=users
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # AD_CAMPAIGNS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List ads",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_campaigns_list_ads(
        page: int = 1,
        limit: int = 50,
        source: str = "all",
        status: str | None = None,
        platform: str | None = None,
        account_id: str | None = None,
        ad_account_id: str | None = None,
        page_id: str | None = None,
        profile_id: str | None = None,
        campaign_id: str | None = None,
        platform_ad_id: str | None = None,
        effective_object_story_id: str | None = None,
        effective_instagram_media_id: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> str:
        """List ads

        Args:
            page: Page number
            limit
            source: all (default) = Zernio-created + platform-discovered ads. zernio = restrict to Zernio-created only.
            status
            platform
            account_id: Social account ID
            ad_account_id: Platform ad account ID (e.g. act_123 for Meta). Mirrors the same filter on /v1/ads/campaigns and /v1/ads/tree.
            page_id: Meta only: Facebook Page ID. Returns only ads whose creative is backed by this Page (a Meta ad account serves ads for every Page in the Business Manager). Matches each ad's `creative.pageId`; ads with no page signal (rare IG-only creatives) never match. Mirrors the same filter on /v1/ads/campaigns and /v1/ads/tree.
            profile_id: Profile ID
            campaign_id: Platform campaign ID (filter ads within a campaign)
            platform_ad_id: Meta ad ID. Returns the ad with this platform-side ad ID.
            effective_object_story_id: Facebook `{pageId}_{postId}` of the post the ad's engagement lives on (Meta `effective_object_story_id`). Use to map a Business-Manager-visible post back to the Zernio ad.
            effective_instagram_media_id: Instagram media ID of the boosted post (Meta `effective_instagram_media_id`). Use to map a Business-Manager-visible IG post back to the Zernio ad.
            from_date: Start of metrics date range (YYYY-MM-DD). Defaults to 90 days ago.
            to_date: End of metrics date range (YYYY-MM-DD). Defaults to today. Max 730-day range."""
        client = _get_client()
        try:
            response = client.ad_campaigns.list_ads(
                page=page,
                limit=limit,
                source=source,
                status=status,
                platform=platform,
                account_id=account_id,
                ad_account_id=ad_account_id,
                page_id=page_id,
                profile_id=profile_id,
                campaign_id=campaign_id,
                platform_ad_id=platform_ad_id,
                effective_object_story_id=effective_object_story_id,
                effective_instagram_media_id=effective_instagram_media_id,
                from_date=from_date,
                to_date=to_date,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Search keywords",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_campaigns_list_ad_keywords(
        page: int = 1,
        limit: int = 50,
        account_id: str | None = None,
        ad_account_id: str | None = None,
        profile_id: str | None = None,
        campaign_id: str | None = None,
        ad_set_id: str | None = None,
        status: str | None = None,
        match_type: str | None = None,
        negative: bool | None = None,
        search: str | None = None,
    ) -> str:
        """List Search keywords

        Args:
            page: Page number
            limit
            account_id: Social account ID
            ad_account_id: Platform ad account ID (Google customer ID). Mirrors the same filter on /v1/ads.
            profile_id: Profile ID
            campaign_id: Platform campaign ID
            ad_set_id: Platform ad group ID (Google ad group)
            status: Keyword criterion status
            match_type
            negative: true = negative keywords only, false = positive only. Omit for both.
            search: Case-insensitive substring match on the keyword text"""
        client = _get_client()
        try:
            response = client.ad_campaigns.list_ad_keywords(
                page=page,
                limit=limit,
                account_id=account_id,
                ad_account_id=ad_account_id,
                profile_id=profile_id,
                campaign_id=campaign_id,
                ad_set_id=ad_set_id,
                status=status,
                match_type=match_type,
                negative=negative,
                search=search,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List campaigns",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_campaigns_list_ad_campaigns(
        include_empty: bool | None = None,
        page: int = 1,
        limit: int = 20,
        source: str = "all",
        platform: str | None = None,
        status: str | None = None,
        ad_account_id: str | None = None,
        page_id: str | None = None,
        account_id: str | None = None,
        profile_id: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        has_delivery: bool | None = None,
        min_spend: float | None = None,
    ) -> str:
        """List campaigns

        Args:
            include_empty: Meta only. Campaign reads aggregate over ad documents, so a campaign with ZERO ads is normally invisible here — the state the two-step create (campaign, then ads via `existingCampaignId`) leaves behind whenever Meta rejects the ad step. Set true to list those too, with `adCount: 0` and zeroed metrics. Requires `accountId` and `adAccountId`, since an empty campaign has no ad row to resolve a token or ad account from.
            page: Page number
            limit
            source: `all` (default) returns both Zernio-created ads and those discovered from the platform's ad manager — matches the web UI's default view. Pass `zernio` to restrict to isExternal=false only. Status is NOT filtered by default — use the `status` param for that.
            platform
            status: Filter by derived campaign status (post-aggregation)
            ad_account_id: Platform ad account ID (e.g. act_123 for Meta)
            page_id: Meta only: Facebook Page ID. Campaigns have no Page of their own, so this keeps campaigns having at least one ad backed by this Page, with adCount and metrics computed over those ads only. Mirrors the same filter on /v1/ads and /v1/ads/tree.
            account_id: Social account ID
            profile_id: Profile ID
            from_date: Start of metrics date range (YYYY-MM-DD, inclusive). Defaults to 90 days ago when both date params are omitted.
            to_date: End of metrics date range (YYYY-MM-DD, inclusive). Defaults to today. Max 730-day range.
            has_delivery: Return only campaigns that delivered between `fromDate` and `toDate` — spend above zero, or impressions served at zero spend. Unlike `status`, which reads a campaign's CURRENT state, this filters on what happened inside the window. Filters the campaign set itself, so `pagination.total` counts only matching campaigns. Mirrors the same filter on /v1/ads/tree.
            min_spend: Return only campaigns whose spend between `fromDate` and `toDate` reaches this amount, in each campaign's OWN currency (the `currency` field on the campaign). Implies `hasDelivery`; `minSpend=0` applies no filter. Mirrors the same filter on /v1/ads/tree."""
        client = _get_client()
        try:
            response = client.ad_campaigns.list_ad_campaigns(
                include_empty=include_empty,
                page=page,
                limit=limit,
                source=source,
                platform=platform,
                status=status,
                ad_account_id=ad_account_id,
                page_id=page_id,
                account_id=account_id,
                profile_id=profile_id,
                from_date=from_date,
                to_date=to_date,
                has_delivery=has_delivery,
                min_spend=min_spend,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a standalone campaign",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_create_ad_campaign(
        account_id: str,
        ad_account_id: str,
        name: str,
        goal: str,
        special_ad_categories: list[str] | None = None,
        budget_amount: float | None = None,
        budget_type: str | None = None,
        status: str = "PAUSED",
        bid_strategy: str | None = None,
        bid_amount: float | None = None,
        roas_average_floor: float | None = None,
    ) -> str:
        """Create a standalone campaign

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)
            name: (required)
            goal: Mapped to the ODAX objective (same mapping as POST /v1/ads/create). (required)
            special_ad_categories
            budget_amount: Campaign-level (CBO) budget in WHOLE currency units (USD: 50 = $50.00), NOT cents — Meta's own Marketing API takes this same number in minor units, so it is an easy and expensive mix-up. Requires budgetType.
            budget_type
            status
            bid_strategy: Campaign bid strategy. Meta stores `bid_strategy` alongside the budget, so this REQUIRES `budgetAmount` + `budgetType` on the same request; sending it without a campaign budget is a 400. A campaign carrying a strategy without its `bid_amount` makes every ad set created under it fail with an error that names the ad set (code 100, subcode 1815857), so the bad state is rejected up front rather than accepted. To bid at ad-set level, set the strategy there instead.
            bid_amount: Whole currency units (USD: 5 = $5.00). Required for LOWEST_COST_WITH_BID_CAP and COST_CAP; ignored otherwise. Validated here but NOT stored by Meta: the campaign object has no bid_amount field, only bid_strategy lives on it. The amount takes effect once an ad set joins this campaign (existingCampaignId on POST /v1/ads/create) and supplies its own bidAmount there.
            roas_average_floor: Decimal ROAS multiplier (2.0 = 2.0x). Required for LOWEST_COST_WITH_MIN_ROAS."""
        client = _get_client()
        try:
            response = client.ad_campaigns.create_ad_campaign(
                account_id=account_id,
                ad_account_id=ad_account_id,
                name=name,
                goal=goal,
                special_ad_categories=special_ad_categories,
                budget_amount=budget_amount,
                budget_type=budget_type,
                status=status,
                bid_strategy=bid_strategy,
                bid_amount=bid_amount,
                roas_average_floor=roas_average_floor,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Pause or resume a campaign",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_update_ad_campaign_status(
        campaign_id: str, status: str, platform: str
    ) -> str:
        """Pause or resume a campaign

        Args:
            campaign_id: Platform campaign ID (required)
            status: (required)
            platform: (required)"""
        client = _get_client()
        try:
            response = client.ad_campaigns.update_ad_campaign_status(
                campaign_id=campaign_id, status=status, platform=platform
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update a campaign",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_update_ad_campaign(
        campaign_id: str,
        platform: str,
        account_id: str | None = None,
        bid_strategy: str | None = None,
        bid_amount: float | None = None,
        roas_average_floor: float | None = None,
        budget: dict[str, Any] | None = None,
        name: str | None = None,
        platform_specific_data: dict[str, Any] | None = None,
    ) -> str:
        """Update a campaign

        Args:
            campaign_id: Platform campaign ID (required)
            platform: Required: platform campaign IDs are not globally unique. (required)
            account_id: **Meta only.** Zernio SocialAccount id owning the ad account. Needed only for an EMPTY campaign (zero ads); ignored otherwise.
            bid_strategy: **Meta + Google.** On Meta, the campaign default that ad sets inherit unless they override it. On Google, the campaign's own bidding strategy.
            bid_amount: **Google only.** Whole currency units (USD: 12 = $12.00). Max CPC for LOWEST_COST_WITH_BID_CAP, CPA target for COST_CAP; required for both.
            roas_average_floor: **Google only.** Decimal ROAS multiplier (2.0 = 2.0x), required for LOWEST_COST_WITH_MIN_ROAS.
            budget: **Meta only.** The CBO budget.
            name: **Meta only.** Rename the campaign.
            platform_specific_data: **Meta only.** Platform implied by the `platform` body param, same convention as POST /v1/ads/create."""
        client = _get_client()
        try:
            response = client.ad_campaigns.update_ad_campaign(
                campaign_id=campaign_id,
                platform=platform,
                account_id=account_id,
                bid_strategy=bid_strategy,
                bid_amount=bid_amount,
                roas_average_floor=roas_average_floor,
                budget=budget,
                name=name,
                platform_specific_data=platform_specific_data,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete a campaign",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_delete_ad_campaign(
        campaign_id: str, platform: str, account_id: str | None = None
    ) -> str:
        """Delete a campaign

        Args:
            campaign_id: Platform campaign ID (required)
            platform: (required)
            account_id: Zernio SocialAccount id owning the ad account. Required only to delete an EMPTY campaign (zero ads), which has no local Ad documents to resolve a token from."""
        client = _get_client()
        try:
            response = client.ad_campaigns.delete_ad_campaign(
                campaign_id=campaign_id, platform=platform, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Pause or resume many campaigns",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_bulk_update_ad_campaign_status(
        status: str, campaigns: list[dict[str, Any]] | None
    ) -> str:
        """Pause or resume many campaigns

        Args:
            status: (required)
            campaigns: (required)"""
        client = _get_client()
        try:
            response = client.ad_campaigns.bulk_update_ad_campaign_status(
                status=status, campaigns=campaigns
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Duplicate a campaign",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_duplicate_ad_campaign(
        campaign_id: str,
        platform: str,
        deep_copy: bool = True,
        status_option: str = "PAUSED",
        start_time: str | None = None,
        end_time: str | None = None,
        rename_strategy: str | None = None,
        rename_prefix: str | None = None,
        rename_suffix: str | None = None,
        sync_after: bool = True,
    ) -> str:
        """Duplicate a campaign

        Args:
            campaign_id: Source platform campaign ID (required)
            platform: (required)
            deep_copy: Copy child ad sets + ads + creatives + targeting
            status_option: ACTIVE = launch the clone immediately (spends the moment LinkedIn approves it). PAUSED = clone stays DRAFT, safe default. INHERITED_FROM_SOURCE = mirror each entity's source status per-entity. Duplicating an ACTIVE campaign this way starts a second front of spend.
            start_time: Reschedule the copied hierarchy's start time
            end_time
            rename_strategy
            rename_prefix
            rename_suffix
            sync_after: Trigger ads discovery on the owning account after the copy succeeds"""
        client = _get_client()
        try:
            response = client.ad_campaigns.duplicate_ad_campaign(
                campaign_id=campaign_id,
                platform=platform,
                deep_copy=deep_copy,
                status_option=status_option,
                start_time=start_time,
                end_time=end_time,
                rename_strategy=rename_strategy,
                rename_prefix=rename_prefix,
                rename_suffix=rename_suffix,
                sync_after=sync_after,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Duplicate an ad set",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_duplicate_ad_set(
        ad_set_id: str,
        platform: str,
        campaign_id: str | None = None,
        deep_copy: bool = True,
        status_option: str = "PAUSED",
        start_time: str | None = None,
        end_time: str | None = None,
        rename_strategy: str | None = None,
        rename_prefix: str | None = None,
        rename_suffix: str | None = None,
        sync_after: bool = True,
    ) -> str:
        """Duplicate an ad set

        Args:
            ad_set_id: Source platform ad set ID (required)
            platform: (required)
            campaign_id: Destination platform campaign id (defaults to the source's campaign)
            deep_copy: Copy child ads + creatives
            status_option
            start_time: Reschedule the copy's start time
            end_time
            rename_strategy
            rename_prefix
            rename_suffix
            sync_after"""
        client = _get_client()
        try:
            response = client.ad_campaigns.duplicate_ad_set(
                ad_set_id=ad_set_id,
                platform=platform,
                campaign_id=campaign_id,
                deep_copy=deep_copy,
                status_option=status_option,
                start_time=start_time,
                end_time=end_time,
                rename_strategy=rename_strategy,
                rename_prefix=rename_prefix,
                rename_suffix=rename_suffix,
                sync_after=sync_after,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Duplicate an ad",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_duplicate_ad(
        ad_id: str,
        ad_set_id: str | None = None,
        status_option: str = "PAUSED",
        rename_strategy: str | None = None,
        rename_prefix: str | None = None,
        rename_suffix: str | None = None,
        sync_after: bool = True,
    ) -> str:
        """Duplicate an ad

        Args:
            ad_id: Zernio ad ID or platform ad ID (required)
            ad_set_id: Destination platform ad set id (defaults to the source's ad set)
            status_option
            rename_strategy
            rename_prefix
            rename_suffix
            sync_after"""
        client = _get_client()
        try:
            response = client.ad_campaigns.duplicate_ad(
                ad_id=ad_id,
                ad_set_id=ad_set_id,
                status_option=status_option,
                rename_strategy=rename_strategy,
                rename_prefix=rename_prefix,
                rename_suffix=rename_suffix,
                sync_after=sync_after,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Live ad-set details incl. learning phase",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_campaigns_get_ad_set_details(
        ad_set_id: str, account_id: str, fields: str | None = None
    ) -> str:
        """Live ad-set details incl. learning phase

        Args:
            ad_set_id: Meta ad set id (platformAdSetId). (required)
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            fields: Comma-separated Graph field override (supports nested {} projections)."""
        client = _get_client()
        try:
            response = client.ad_campaigns.get_ad_set_details(
                ad_set_id=ad_set_id, account_id=account_id, fields=fields
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update an ad set",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_update_ad_set(
        ad_set_id: str,
        platform: str,
        budget: dict[str, Any] | None = None,
        status: str | None = None,
        name: str | None = None,
        bid_strategy: str | None = None,
        bid_amount: float | None = None,
        roas_average_floor: float | None = None,
        value_rule_set_id: str | None = None,
        value_rules_applied: bool | None = None,
        platform_specific_data: dict[str, Any] | None = None,
    ) -> str:
        """Update an ad set

            Args:
                ad_set_id: Platform ad set ID (required)
                platform: (required)
                budget: Omit if not updating budget
                status: Omit if not toggling delivery state
                name: Rename the ad set (Meta only; other platforms return 501). At least one of budget/status/bidStrategy/name is required.
                bid_strategy: Ad-set-level bid strategy. Overrides the campaign-level default.
        Supported on Meta (facebook, instagram), TikTok, and OpenAI. On TikTok the
        Meta-style enum is mapped to bid_type / bid_price / deep_bid_type
        automatically. On OpenAI, LOWEST_COST_WITH_BID_CAP and COST_CAP both map to
        the ad group's `bidding_config.max_bid_micros` (one knob covers both);
        LOWEST_COST_WITH_MIN_ROAS is rejected with 422 (OpenAI has no ROAS-based
        bidding). Other platforms (linkedin, pinterest, google, twitter) return 501
        Not Implemented when bidStrategy is set.
                bid_amount: Bid cap in WHOLE currency units (USD: 5 = $5.00; JPY: 100 = ¥100). Required when
        bidStrategy is LOWEST_COST_WITH_BID_CAP or COST_CAP. Internally converted to Meta's
        smallest-denomination integer, or (on OpenAI) to micros (× 1,000,000). Meta only:
        may be sent alone, WITHOUT bidStrategy, to update the cap amount on an ad set whose
        parent campaign is COST_CAP or LOWEST_COST_WITH_BID_CAP (the strategy is inherited
        from the campaign and is left untouched).
                roas_average_floor: Minimum ROAS as a decimal multiplier (2.0 = 2.0x). Required when bidStrategy is
        LOWEST_COST_WITH_MIN_ROAS. Sent to Meta as `bid_constraints.roas_average_floor` × 10000.
        Not supported on OpenAI (422).
                value_rule_set_id: Meta only (other platforms return 501). Value rule set to attach to this ad
        set, from `/v1/ads/value-rule-sets`. Sending a different id replaces the
        current association. To DETACH, send `valueRulesApplied: false` and omit
        this field.
                value_rules_applied: Meta only (other platforms return 501). `false` DETACHES the ad set's value
        rule set and must be sent WITHOUT `valueRuleSetId`; the combination returns
        400. `true` is optional when attaching, since attachment is driven by
        `valueRuleSetId`, and requires it to be present.
                platform_specific_data: Platform-specific post-launch delivery settings. The platform is implied by the
        `platform` body param. Meta only; other platforms return 400. Unknown keys are rejected."""
        client = _get_client()
        try:
            response = client.ad_campaigns.update_ad_set(
                ad_set_id=ad_set_id,
                platform=platform,
                budget=budget,
                status=status,
                name=name,
                bid_strategy=bid_strategy,
                bid_amount=bid_amount,
                roas_average_floor=roas_average_floor,
                value_rule_set_id=value_rule_set_id,
                value_rules_applied=value_rules_applied,
                platform_specific_data=platform_specific_data,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Pause or resume a single ad set",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_update_ad_set_status(
        ad_set_id: str, status: str, platform: str
    ) -> str:
        """Pause or resume a single ad set

        Args:
            ad_set_id: Platform ad set ID (required)
            status: (required)
            platform: (required)"""
        client = _get_client()
        try:
            response = client.ad_campaigns.update_ad_set_status(
                ad_set_id=ad_set_id, status=status, platform=platform
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get campaign tree",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_campaigns_get_ad_tree(
        page: int = 1,
        limit: int = 20,
        source: str = "all",
        platform: str | None = None,
        status: str | None = None,
        ad_account_id: str | None = None,
        page_id: str | None = None,
        account_id: str | None = None,
        profile_id: str | None = None,
        campaign_id: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        has_delivery: bool | None = None,
        min_spend: float | None = None,
        sort: str = "newest",
        time_increment: int | None = None,
        daily_level: str = "campaign",
    ) -> str:
        """Get campaign tree

        Args:
            page: Page number
            limit: Campaigns per page
            source: `all` (default) returns both Zernio-created ads and those discovered from the platform's ad manager — matches the web UI's default view. Pass `zernio` to restrict to isExternal=false only. Status is NOT filtered by default — use the `status` param for that.
            platform
            status: Filter by derived campaign status (post-aggregation)
            ad_account_id: Platform ad account ID
            page_id: Meta only: Facebook Page ID. Prunes the tree to ads whose creative is backed by this Page — campaigns and ad sets with no ad on the Page drop out, and rolled-up metrics cover only the Page's ads. Mirrors the same filter on /v1/ads and /v1/ads/campaigns.
            account_id: Social account ID
            profile_id: Profile ID
            campaign_id: Restrict the tree to a single campaign by its platform campaign id (the id the platform assigns, e.g. Meta's numeric campaign id). Filters the campaign set itself, so it works regardless of account size and pagination — pass this when you already hold a campaign id instead of paging the tree to find it. Mirrors the `campaignId` filter on GET /v1/ads.
            from_date: Start of the METRICS date range (YYYY-MM-DD). On its own it affects only the spend/impression numbers overlaid on each node, not which campaigns are returned — pass `hasDelivery` or `minSpend` to also filter the campaign set to this window. Defaults to 90 days ago.
            to_date: End of metrics date range (YYYY-MM-DD). Defaults to today. Max 730-day range.
            has_delivery: Return only campaigns that delivered between `fromDate` and `toDate` — spend above zero, or impressions served at zero spend. Unlike `status`, which reads a campaign's CURRENT state, this filters on what happened inside the window, so a campaign that spent then and is paused today is still returned. Filters the campaign set itself, so `pagination.total` counts only matching campaigns.
            min_spend: Return only campaigns whose spend between `fromDate` and `toDate` reaches this amount. Expressed in each campaign's OWN currency (the `currency` field on the campaign node): spend is stored per ad account in its native currency and one response can span several. Implies `hasDelivery`; `minSpend=0` applies no filter.
            sort: Campaign-level sort order. `newest` (default) / `oldest` order by the campaign's newest-ad createdAt. `spend_desc` / `spend_asc` order by aggregated spend in the requested date range; campaigns with no spend land at the end.
            time_increment: Set to `1` to also return a daily breakdown. Mirrors Meta Insights' `time_increment=1`: each node gains a `daily[]` array of per-day metrics (same fields as the aggregated `metrics`) alongside the range total, so you get per-entity daily trends in ONE call instead of calling the tree once per day. Only `1` (daily) is supported. The daily series covers the same date range and uses the same source data as `metrics`, except `reach` on Meta and TikTok: the range total is the platform's de-duplicated value, so daily reach does not sum to it. See `dailyLevel` to control which levels carry it.
            daily_level: Which tree levels get the `daily[]` series when `timeIncrement=1`. `campaign` (default) attaches it on campaign nodes only — the common per-campaign-trend case, and the smallest payload. `adset` adds it on ad sets too; `ad` adds it on every ad in `ads[]` as well (heaviest — a long range × up to 100 ads per ad set). Scope with `campaignId` to keep `ad`-level responses small. Ignored when `timeIncrement` is unset."""
        client = _get_client()
        try:
            response = client.ad_campaigns.get_ad_tree(
                page=page,
                limit=limit,
                source=source,
                platform=platform,
                status=status,
                ad_account_id=ad_account_id,
                page_id=page_id,
                account_id=account_id,
                profile_id=profile_id,
                campaign_id=campaign_id,
                from_date=from_date,
                to_date=to_date,
                has_delivery=has_delivery,
                min_spend=min_spend,
                sort=sort,
                time_increment=time_increment,
                daily_level=daily_level,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get daily account metrics",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_campaigns_get_ads_timeline(
        account_id: str,
        ad_account_id: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        platform: str | None = None,
    ) -> str:
        """Get daily account metrics

        Args:
            account_id: Social account ID. Sibling-expanded to its linked posting↔ads pair. (required)
            ad_account_id: Optional platform-native ad account ID (e.g. Meta `act_…`, TikTok advertiser ID). Use when the connection wraps multiple platform ad accounts and the chart should show one only. Note: rows ingested before 2026-05-13 don't carry this column; the recurring 7-day re-sync repopulates them naturally.
            from_date: Inclusive start of metrics range (YYYY-MM-DD). Defaults to 90 days ago.
            to_date: Inclusive end of metrics range (YYYY-MM-DD). Defaults to today. Max 730-day range.
            platform: Restrict to one platform."""
        client = _get_client()
        try:
            response = client.ad_campaigns.get_ads_timeline(
                account_id=account_id,
                ad_account_id=ad_account_id,
                from_date=from_date,
                to_date=to_date,
                platform=platform,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get ad details",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_campaigns_get_ad(ad_id: str) -> str:
        """Get ad details

           Args:
               ad_id: Zernio `_id` (hex), Meta `platformAdId` (numeric), or one of the creative's effective story/media IDs. See description for details.
        (required)"""
        client = _get_client()
        try:
            response = client.ad_campaigns.get_ad(ad_id=ad_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update ad",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_update_ad(
        ad_id: str,
        status: str | None = None,
        budget: dict[str, Any] | None = None,
        targeting: dict[str, Any] | None = None,
        creative: dict[str, Any] | None = None,
        name: str | None = None,
    ) -> str:
        """Update ad

            Args:
                ad_id: (required)
                status
                budget
                targeting: Meta + TikTok (demographics/interests) and Google (keyword edits only).
        Pinterest / X / LinkedIn return 501.
                creative: Replace the ad's creative. Meta + TikTok only.

        - **Meta**: requires `headline`, `body`, `callToAction`, `linkUrl`, `imageUrl`. The
          ad's existing creative is replaced via a new `/act_X/adcreatives` upload + ad
          update. The old creative is retained on the ad account for historical reporting.
        - **TikTok**: patch-style. Pass any subset; `headline` is ignored (TikTok creatives
          have no headline slot). `body` becomes the in-feed `ad_text`; `linkUrl` becomes
          `landing_page_url`; `videoUrl` triggers a fresh upload.
                name: Rename the ad. Now propagated to Meta (POST /{ad-id}); non-Meta platforms return 501."""
        client = _get_client()
        try:
            response = client.ad_campaigns.update_ad(
                ad_id=ad_id,
                status=status,
                budget=budget,
                targeting=targeting,
                creative=creative,
                name=name,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Cancel an ad",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_delete_ad(ad_id: str) -> str:
        """Cancel an ad

        Args:
            ad_id: (required)"""
        client = _get_client()
        try:
            response = client.ad_campaigns.delete_ad(ad_id=ad_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Pause or resume a single ad",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_update_ad_status(ad_id: str, status: str) -> str:
        """Pause or resume a single ad

        Args:
            ad_id: Zernio `_id` (hex), Meta `platformAdId` (numeric), or one of the creative's effective story/media IDs. (required)
            status: (required)"""
        client = _get_client()
        try:
            response = client.ad_campaigns.update_ad_status(ad_id=ad_id, status=status)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Boost post as ad",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_boost_post(
        account_id: str,
        ad_account_id: str,
        name: str,
        goal: str,
        post_id: str | None = None,
        platform_post_id: str | None = None,
        ad_set_id: str | None = None,
        budget: dict[str, Any] | None = None,
        instagram_account_id: str | None = None,
        destination_type: str | None = None,
        currency: str | None = None,
        schedule: dict[str, Any] | None = None,
        targeting: dict[str, Any] | None = None,
        raw_targeting: dict[str, Any] | None = None,
        bid_strategy: str | None = None,
        bid_amount: float | None = None,
        roas_average_floor: float | None = None,
        platform_specific_data: dict[str, Any] | None = None,
        tracking: dict[str, Any] | None = None,
        special_ad_categories: list[str] | None = None,
        special_ad_category_country: list[str] | None = None,
        link_url: str | None = None,
        call_to_action: str | None = None,
        spark_auth_code: str | None = None,
        dsa_beneficiary: str | None = None,
        dsa_payor: str | None = None,
        optimization_goal: str | None = None,
    ) -> str:
        """Boost post as ad

            Args:
                post_id: Zernio post ID (provide this or platformPostId)
                platform_post_id: Platform post ID (alternative to postId)
                account_id: Social account ID (required)
                ad_account_id: Platform ad account ID (required)
                name: (required)
                goal: Available goals vary by platform. Meta (Facebook/Instagram) and TikTok support all 7. LinkedIn supports all except app_promotion. Twitter/X supports engagement, traffic, awareness, video_views, app_promotion. Pinterest and Google Ads support only engagement, traffic, awareness, video_views. (required)
                ad_set_id: Meta only. Attach the boosted post to this existing ad set instead of creating a campaign. The ad set then owns budget, schedule and targeting; sending those too is a 400.
                budget: Required unless adSetId is set.
                instagram_account_id: Meta only. Instagram identity the ad runs AS (creative.instagram_user_id), overriding the account linked to the Page. Live-verified against a Page-post creative.
                destination_type: Meta only. Ad-set destination_type — where the click LANDS, as opposed to instagramAccountId which is who the ad runs as. Lead ads force ON_AD and ignore this.
                currency
                schedule
                targeting: Same geo/demographic fields as the `TargetingSpec` used by /v1/ads/create.
        Geo keys (`regions`/`cities`/`zips`/`metros`) resolve via
        GET /v1/ads/targeting/search?dimension=geo. City radius and lat/lng
        `customLocations` are Meta-only and preserve the boosted post's
        social proof (the ad references the existing post).
                raw_targeting: Meta only. A Meta-native targeting spec (e.g.
        `{ "geo_locations": { "cities": [{ "key": "...", "radius": 15, "distance_unit": "kilometer" }] } }`).
        Sent alone it is forwarded unchanged. Use for advanced fields the structured
        object does not expose (flexible_spec, excluded audiences, business places,
        user_os, wireless_carrier).

        Can be combined with `targeting`: rawTargeting is the BASE layer and the
        built camelCase spec is merged on top, key by key (camelCase wins on
        collision). The merge goes one level deep inside `geo_locations` and
        `excluded_geo_locations` (built sub-keys win; raw-only sub-keys such as
        `location_types` survive). Array values (`flexible_spec`, ...) are replaced
        as a whole key, never element-merged.

        When `rawTargeting` is present the `advantage_audience: 0` default that
        Zernio normally applies is no longer emitted, so it cannot clobber a
        `targeting_automation` sent in the raw spec. Meta requires
        `targeting_automation` on ad set creation, so include it in the raw spec,
        or send `targeting.advantage_audience` (0 or 1), which is merged over raw
        as `targeting_automation`.
                bid_strategy: Deprecated: send it inside `platformSpecificData` instead (Meta today; TikTok's nested shape is planned). The flat field keeps working during the deprecation window; sending both shapes returns a 400.

        Meta bid strategy applied to the ad set. On TikTok, mapped to
        `bid_type` / `bid_price` / `deep_bid_type` automatically.
                bid_amount: Deprecated: send it inside `platformSpecificData` instead (Meta today; TikTok's nested shape is planned). The flat field keeps working during the deprecation window; sending both shapes returns a 400.

        Bid cap in WHOLE currency units (USD: 5 = $5.00; JPY: 100 = ¥100). Required when
        `bidStrategy` is `LOWEST_COST_WITH_BID_CAP` or `COST_CAP`. Backward-compat: providing
        `bidAmount` without `bidStrategy` is treated as `LOWEST_COST_WITH_BID_CAP`.
                roas_average_floor: Deprecated: send it inside `platformSpecificData` instead (Meta today; TikTok's nested shape is planned). The flat field keeps working during the deprecation window; sending both shapes returns a 400.

        Minimum ROAS as a decimal multiplier (e.g. 2.0 = 2.0x ROAS). Required when
        `bidStrategy` is `LOWEST_COST_WITH_MIN_ROAS`. Sent to Meta as
        `bid_constraints.roas_average_floor` × 10000 (Meta uses fixed-point integers).
                platform_specific_data: Platform-specific options. The platform is derived from `accountId`;
        sending options for a different platform returns a 400. LinkedIn
        (campaign bidding and delivery controls) and Meta (the bid trio)
        have options today.

        **Meta**: `bidStrategy`, `bidAmount` and `roasAverageFloor` may be
        sent here instead of at the root — the preferred home going forward.
        Sending the bid fields in BOTH places returns a 400
        (`mutually_exclusive_fields`).
                tracking: Meta only. Tracking specs (pixel, URL tags).
                special_ad_categories: Meta only. Required for housing, employment, credit, or political ads.
                special_ad_category_country: Meta (metaads) only. 2-letter ISO country codes the special ad category applies to. Requires specialAdCategories to be set (400 otherwise).
                link_url: Destination URL for the CTA button. Send it together with `callToAction`.

        **Meta**: adds a top-level `call_to_action` to the post-reference creative.
        This is what gives a `traffic` boost a clickable destination without
        replacing the creative and losing the post's social proof. Ignored when
        `leadGenFormId` is set, which supplies its own destination. Live-verified
        against a Page-post creative.

        **TikTok**: maps to `landing_page_url` on the Spark Ad creative
        (`AdcreateCreatives.landing_page_url`); Spark Ads have no clickable
        destination without it.

        Ignored on LinkedIn / Pinterest / X / Google, which infer the destination
        from the boosted post.
                call_to_action: CTA button label. Send it together with `linkUrl` — a CTA without a
        destination produces a button that goes nowhere, so sending one alone is a 400.

        **Meta**: validated against the Meta CTA enum (same values as
        POST /v1/ads/create), e.g. `LEARN_MORE`, `SHOP_NOW`, `SIGN_UP`.

        **TikTok**: pass-through to `call_to_action` on the Spark Ad creative; the
        platform validates the value. See TikTok's "Enumeration - Call-to-Action".
                spark_auth_code: TikTok-only. Spark Code (creator's `auth_code`) authorizing cross-creator
        Spark Ads — the advertiser can boost a video owned by a DIFFERENT TikTok
        account. Without this, boosts are limited to videos owned by the same
        account running the ads (same-BC creators only). The creator generates the
        code in their TikTok app's Promote settings and shares it with the
        advertiser. Maps to `auth_code` on the creative entry of /v2/ad/create/.
                dsa_beneficiary: Legal entity that benefits from the ad. Required when targeting EU users
        (EU DSA, Article 26). Optional if the ad account has a default beneficiary:
        set it once via `PATCH /v1/ads/accounts` or in Meta Ads Manager, and Meta
        fills it in whenever the field is omitted.
                dsa_payor: Legal entity that pays for the ad. Can differ from `dsaBeneficiary`
        (for example, an agency paying for a client's ads). Same rules as
        `dsaBeneficiary`: required for EU targeting unless the ad account has
        a default payor.
                optimization_goal: Meta only. Explicit ad-set `optimization_goal` override. When omitted,
        defaults to the value derived from `goal`. The value must be compatible
        with the objective Meta derives from `goal`, not with the objective used
        by `POST /v1/ads/create` for the same `goal` name: boost maps `goal:
        "engagement"` to objective `OUTCOME_AWARENESS`, which accepts
        `REACH`, `IMPRESSIONS`, `AD_RECALL_LIFT`, or THRUPLAY-class values, and
        rejects `POST_ENGAGEMENT` (that value is only valid under
        `OUTCOME_ENGAGEMENT`, which create uses for the same goal name)."""
        client = _get_client()
        try:
            response = client.ad_campaigns.boost_post(
                post_id=post_id,
                platform_post_id=platform_post_id,
                account_id=account_id,
                ad_account_id=ad_account_id,
                name=name,
                goal=goal,
                ad_set_id=ad_set_id,
                budget=budget,
                instagram_account_id=instagram_account_id,
                destination_type=destination_type,
                currency=currency,
                schedule=schedule,
                targeting=targeting,
                raw_targeting=raw_targeting,
                bid_strategy=bid_strategy,
                bid_amount=bid_amount,
                roas_average_floor=roas_average_floor,
                platform_specific_data=platform_specific_data,
                tracking=tracking,
                special_ad_categories=special_ad_categories,
                special_ad_category_country=special_ad_category_country,
                link_url=link_url,
                call_to_action=call_to_action,
                spark_auth_code=spark_auth_code,
                dsa_beneficiary=dsa_beneficiary,
                dsa_payor=dsa_payor,
                optimization_goal=optimization_goal,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create standalone ad",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_create_standalone_ad(
        account_id: str,
        ad_account_id: str,
        name: str,
        campaign_name: str | None = None,
        ad_set_name: str | None = None,
        ad_name: str | None = None,
        tracking: dict[str, Any] | None = None,
        goal: str | None = None,
        optimization_goal: str | None = None,
        billing_event: str | None = None,
        buying_type: str | None = None,
        rf_prediction_id: str | None = None,
        creative_features: dict[str, Any] | None = None,
        multi_advertiser: str | None = None,
        validate_only: bool | None = None,
        budget_amount: float | None = None,
        budget_type: str | None = None,
        status: str | None = None,
        budget_level: str = "adset",
        currency: str | None = None,
        headline: str | None = None,
        long_headline: str | None = None,
        body: str | None = None,
        description: str | None = None,
        call_to_action: str | None = None,
        link_url: str | None = None,
        lead_gen_form_id: str | None = None,
        image_url: str | None = None,
        images: dict[str, Any] | None = None,
        video: dict[str, Any] | None = None,
        creatives: list[dict[str, Any]] | None = None,
        ad_set_id: str | None = None,
        existing_campaign_id: str | None = None,
        existing_creative_id: str | None = None,
        business_name: str | None = None,
        board_id: str | None = None,
        organization_id: str | None = None,
        targeting: dict[str, Any] | None = None,
        countries: list[str] | None = None,
        cities: list[dict[str, Any]] | None = None,
        regions: list[dict[str, Any]] | None = None,
        age_min: int | None = None,
        age_max: int | None = None,
        interests: list[dict[str, Any]] | None = None,
        zips: list[dict[str, Any]] | None = None,
        metros: list[dict[str, Any]] | None = None,
        custom_locations: list[dict[str, Any]] | None = None,
        behaviors: list[dict[str, Any]] | None = None,
        income_tier: str | None = None,
        languages: list[str] | None = None,
        placements: dict[str, Any] | None = None,
        saved_targeting_id: str | None = None,
        raw_targeting: dict[str, Any] | None = None,
        special_ad_categories: list[str] | None = None,
        special_ad_category_country: list[str] | None = None,
        end_date: str | None = None,
        start_date: str | None = None,
        instagram_account_id: str | None = None,
        dynamic_creative: dict[str, Any] | None = None,
        carousel_cards: list[dict[str, Any]] | None = None,
        default_locale: str | None = None,
        translations: list[dict[str, Any]] | None = None,
        placement_assets: dict[str, Any] | None = None,
        audience_id: str | None = None,
        campaign_type: str = "display",
        keywords: list[str] | None = None,
        negative_keywords: list[str] | None = None,
        additional_headlines: list[str] | None = None,
        additional_descriptions: list[str] | None = None,
        advantage_audience: int | None = None,
        attribution_spec: list[dict[str, Any]] | None = None,
        gender: str = "all",
        bid_strategy: str | None = None,
        bid_amount: float | None = None,
        roas_average_floor: float | None = None,
        value_rule_set_id: str | None = None,
        value_rules_applied: bool | None = None,
        platform_specific_data: dict[str, Any] | None = None,
        dsa_beneficiary: str | None = None,
        dsa_payor: str | None = None,
        brand_identity: dict[str, Any] | None = None,
        identity_type: str | None = None,
        smart_plus: bool | None = None,
        promoted_object: dict[str, Any] | None = None,
    ) -> str:
        """Create standalone ad

            Args:
                account_id: (required)
                ad_account_id: (required)
                name: (required)
                campaign_name: Meta only. Exact campaign name. Overrides the default `<name> - Campaign`.
                ad_set_name: Meta only. Exact ad set name. Overrides the default `<name> - Ad Set`. (For per-ad names on the multi-creative shape, set `name` on each `creatives[]` entry.)
                ad_name: Meta only. Exact ad name (the single-creative ad object's name). Overrides the default, which is `name`. (For per-ad names on the multi-creative shape, set `name` on each `creatives[]` entry instead.)
                tracking: Meta only. Attaches pixel measurement to the ad regardless of the optimization goal (the "Website events" tracking row in Ads Manager). `pixelId` becomes the ad's `tracking_specs` (offsite_conversion + fb_pixel); `urlTags` becomes the ad's `url_tags` (click-tracking query params). Applied on the legacy single-creative shape, every ad of the multi-creative shape, and the attach shape. NOTE: tracking lives on the AD object and is not inherited from the ad set, so pass it on EVERY attach call that should carry the pixel.
                goal: Required on legacy and multi-creative shapes; the attach shape inherits it from the ad set. Available goals vary by platform.

        **Meta**
        - `conversions`: OUTCOME_SALES. Requires `promotedObject.pixelId` and `promotedObject.customEventType` with a commerce event such as PURCHASE or START_TRIAL, or `promotedObject.customConversionId` to optimise against a Custom Conversion, or `customEventType: OTHER` + `customEventStr` to optimise against a pixel custom event.
        - `lead_conversion`: OUTCOME_LEADS optimizing website pixel leads. Same pixel and event fields, but with a leads-class event such as LEAD, SUBMIT_APPLICATION, SCHEDULE or CONTACT (or `promotedObject.customConversionId` to optimise against a Custom Conversion instead). Meta gates conversion events by objective, so leads-class events are rejected under `conversions`.
        - `lead_generation`: OUTCOME_LEADS with instant forms. Requires `leadGenFormId`. `promotedObject.pageId` is optional and auto-filled from the connected Page.
        - `app_promotion`: requires `promotedObject.applicationId` and `promotedObject.objectStoreUrl`.
        - `catalog_sales`: Advantage+ catalog ads, for example vehicle inventory. Requires `promotedObject.productSetId`, `promotedObject.pixelId` and `promotedObject.customEventType`. Builds a catalog TEMPLATE creative from the copy fields, which may carry template tags like {{product.name}} or {{vehicle.make}}. No imageUrl or video is sent; Meta renders the visuals per catalog item. Discover catalogs via GET /v1/ads/catalogs and product sets via GET /v1/ads/catalogs/{catalogId}/product-sets. Single shape only, no creatives[], adSetId, dynamicCreative or placementAssets.

        **TikTok**
        - `conversions`: website-conversion ad group. Requires `promotedObject.pixelId`, your TikTok Pixel ID. Accepts an optional `promotedObject.customEventType` with a TikTok optimization_event code your pixel tracks (newer pixels use e.g. SHOPPING for purchase events; legacy pixels use ON_WEB_ORDER, INITIATE_ORDER, ON_WEB_REGISTER or FORM). To inherit pixel and event from an existing ad group, pass `adSetId` instead.

        **LinkedIn**
        - `engagement`, `traffic`, `awareness` and `video_views` create standalone Direct Sponsored Content ads. `traffic` requires `linkUrl`; `video_views` requires `video`.
        - `job_applicants` requires a `platformSpecificData.jobs` creative.
        - For `lead_generation` or `conversions` on LinkedIn, or to promote an existing post, use POST /v1/ads/boost.

        **OpenAI Ads**
        - Only `traffic`, `awareness`, and `conversions` are supported (other goals return 400). Maps to OpenAI's `bidding_type` (clicks, impressions, conversions respectively). `conversions` requires an active conversion event setting on the account; create a tracking tag with `defaultEventType` via the tracking-tags API (`POST /v1/accounts/{accountId}/tracking-tags`), or configure a conversion event in OpenAI Ads Manager, or the request returns 422.
                optimization_goal: Meta only. Explicit ad-set `optimization_goal` (e.g. `LANDING_PAGE_VIEWS`, `LINK_CLICKS`, `REACH`, `IMPRESSIONS`, `OFFSITE_CONVERSIONS`, `THRUPLAY`, `LEAD_GENERATION`). Overrides the default derived from `goal` (e.g. `traffic` defaults to `LINK_CLICKS`). Forwarded verbatim to Meta, which validates compatibility with the campaign objective and rejects incompatible combinations.
                billing_event: Meta only. Explicit ad-set `billing_event`. Defaults to `IMPRESSIONS`. Forwarded verbatim to Meta, which validates compatibility with the optimization goal.
                buying_type: Meta only. RESERVED = Reach & Frequency: requires `rfPredictionId` (a RESERVED prediction from /v1/ads/rf-predictions + /reserve). Budget, schedule and pricing come from the reservation, so budgetAmount/budgetType are not required and bid fields are ignored. Only the plain single-ad shape (no creatives[], adSetId, existingCampaignId or dynamicCreative).
                rf_prediction_id: Meta only. The RESERVED prediction id the R&F ad set runs on (reserving mints a new id — pass that one). Requires buyingType RESERVED.
                creative_features: Meta only. Advantage+ creative enhancements: a partial map of Meta creative feature keys (snake_case, e.g. enhance_cta, image_brightness_and_contrast, text_optimizations) to enroll status, forwarded as degrees_of_freedom_spec.creative_features_spec. Meta validates the keys; unspecified features default to OPT_OUT. The legacy standard_enhancements bundle is deprecated by Meta and rejected.
                multi_advertiser: Meta only. Multi-advertiser ads: whether Meta may show this ad alongside other advertisers' in one unit. Meta auto-enrols since Aug 2024, so send OPT_OUT to leave. It is a top-level creative field, NOT a `creativeFeatures` key — Meta rejects it there.
                validate_only: Meta only, single standalone shape only (no creatives[], adSetId, or RESERVED). Dry-run: each node runs Meta's execution_options validate_only and NOTHING is created or persisted. Children need real parents, so a fresh tree validates the campaign + creative (the ad set needs its campaign to exist — pass existingCampaignId to validate it too; the ad itself is never validatable pre-create). A Meta validation failure returns the 400 verbatim; success returns 200 with per-node results instead of an ad.
                budget_amount: Budget in WHOLE currency units (USD: 50 = $50.00), NOT cents — Meta's own Marketing API takes this same number in minor units, so it is an easy and expensive mix-up. Required on legacy + multi-creative shapes. Inherited on attach. OpenAI Ads requires a $1 minimum (its budget is lifetime-only, see budgetType).
                budget_type: Required on legacy + multi-creative shapes. Inherited on attach. OpenAI Ads accepts lifetime only (no daily-budget concept on the platform); sending daily returns 422. OpenAI Ads lifetime budgets require `endDate` to give the lifetime cap a spend window.
                status: Meta and TikTok. Publish state of the created entities. Omitted or ACTIVE publishes live (default, back-compat); PAUSED creates them paused and skips activation, so you can review before they spend. On TikTok the whole campaign > ad group > ad hierarchy stays paused.
                budget_level: Meta only. Where the budget lives, which selects the Meta budget model:
          - `adset` (default): ABO (Ad-set Budget Optimization). The budget is set on the
            ad set. This is the back-compatible behaviour — omit this field to keep it.
          - `campaign`: CBO (Campaign Budget Optimization / Advantage Campaign Budget). The
            budget AND `bidStrategy` are set on the CAMPAIGN, and Meta distributes spend
            across ad sets automatically.
        Meta requires the budget at exactly one level, never both. Non-Meta platforms ignore
        this field. Ignored on the attach shape (`adSetId`), which inherits the existing budget.
                currency
                headline: Required for Meta, Google, Pinterest, LinkedIn, and OpenAI Ads on legacy + attach shapes (skip for multi-creative — use `creatives[].headline`). Ignored for TikTok and X/Twitter. Max: Meta=255, Google=30, Pinterest=100, LinkedIn=400, OpenAI=50 (min 3). On LinkedIn this is the ad's headline (the bold text on the creative); for traffic ads it's the link card title. On OpenAI Ads this is the chat card's title.
                long_headline: Google Display only — defaults to `headline` if omitted. On LinkedIn, reused as the optional secondary description text on traffic (link) ads; omitted if not provided.
                body: Required on legacy + attach shapes. For X/Twitter this is the tweet text (max 280 chars including a ~24-char URL when `linkUrl` is set). On LinkedIn this is the post commentary (the intro text shown above the ad). On OpenAI Ads this is the chat card's body text. Max: Google=90, Pinterest=500, OpenAI=100.
                description: Meta only (facebook/instagram). Link description — the secondary text shown below the headline (Meta's link_data.description; on video creatives mapped to video_data.link_description). When omitted, Meta auto-pulls the destination URL's OpenGraph description. Applies on legacy, attach, and placementAssets shapes; for multi-creative use creatives[].description (this field is the shared fallback). For multi-text variations use dynamicCreative.descriptions instead.
                call_to_action: Required on legacy + attach shapes for Meta. Honoured on TikTok (passes through to the Spark Ad creative's `call_to_action`) and on LinkedIn (the CTA button on the ad; defaults to LEARN_MORE when `linkUrl` is set). LinkedIn accepts: LEARN_MORE, SIGN_UP, DOWNLOAD, SUBSCRIBE, REGISTER, JOIN, ATTEND, REQUEST_DEMO, VIEW_QUOTE, APPLY, SEE_MORE, SHOP_NOW, BUY_NOW. Ignored by Google, Pinterest, and X/Twitter.
                link_url: Required on legacy + attach shapes (skip for multi-creative). On LinkedIn it's the ad's destination URL; required for `traffic` ads, optional for `engagement` / `awareness`. NOT required when `goal` is `lead_generation` (the ad opens a Lead Gen form instead of a destination). On LinkedIn, `imageUrl` + `linkUrl` publishes an ARTICLE-content creative; this is LinkedIn's article ad format, with the image as thumbnail and `longHeadline` as description. Required for OpenAI Ads (the chat card's target_url).
                lead_gen_form_id: Meta Lead Gen forms only (facebook/instagram). The leadgen_forms ID to attach to the ad's creative — create one via POST /v1/ads/lead-forms. REQUIRED when `goal` is `lead_generation`, and on every ATTACH (`adSetId`) call that targets a lead ad set (the form attaches per-ad; Meta rejects a formless ad in a lead ad set). Ignored otherwise. The ad set's promoted_object.page_id + LEAD_GENERATION optimization + destination_type ON_AD are derived automatically from the goal. Both `placementAssets` (per-placement creative) and `dynamicCreative` (multi-text / multi-asset pool, e.g. multiple headlines and primary texts) ARE supported on instant-form lead ads — the form is attached for you, and for `dynamicCreative` the ad set is created as a Dynamic Creative ad set automatically (Meta requires that for any multi-text feed; there is no non-DCO multi-text path). Send a single `imageUrls` (or `videoUrls`) entry plus your text variations to get Meta's "Multiple Text Options" behavior on a lead ad.
                image_url: Image creative for Meta/Google/Pinterest/LinkedIn on legacy + attach shapes (mutually exclusive with `video`). Required for LinkedIn ads unless `video` is set. Not required for Google Search campaigns. For TikTok, this field carries the VIDEO URL (the TikTok ads endpoint is video-only; the field retains the `imageUrl` name for cross-platform consistency). Ignored for X/Twitter. For Google Display, treated as the landscape image (alias of `images.landscape`); supply `images.square` alongside or the request is rejected. For LinkedIn the image is uploaded to LinkedIn under the authoring Company Page (see `organizationId`); recommended ratio 1.91:1 (e.g. 1200×627). Required for OpenAI Ads (uploaded as the chat card's image; OpenAI has no video ad format).
                images: Google Display (Responsive Display Ads) only. Google RDA requires both a landscape (1.91:1) and a square (1:1) marketing image; sending only one is rejected upstream as 'Too few.' (NOT_ENOUGH_*_MARKETING_IMAGE_ASSET). Supply both URLs here. Either this field or the legacy `imageUrl` can provide the landscape, but `square` has no legacy counterpart so it must be set here for Display.
                video: Meta (facebook, instagram) and LinkedIn. When set, creates a VIDEO ad on the legacy (or, for Meta, attach) shape. Mutually exclusive with `imageUrl`. For Meta multi-creative, set `video` per entry inside `creatives[]` instead. For LinkedIn the video is uploaded to LinkedIn under the authoring Company Page (see `organizationId`) and the campaign format is set to SINGLE_VIDEO; LinkedIn ignores `thumbnailUrl` (it auto-generates the poster frame) — supply MP4 H.264/AAC, 3s-30min, 75KB-500MB.
                creatives: Meta-only. When present, switches to the multi-creative shape:
        creates 1 campaign + 1 ad set + N ads (one per entry here).
        Top-level `headline` / `body` / `imageUrl` / `linkUrl` /
        `callToAction` are ignored in this mode. Mutually exclusive with `adSetId`.
                ad_set_id: When present, switches to the attach shape: adds
        one new ad to this existing ad set without creating a new
        campaign. Budget, targeting, goal, schedule, AND bid strategy
        are inherited from the ad set on Meta — passing `bidStrategy`
        in attach mode returns 400. To change an existing ad set's
        bid, use `PUT /v1/ads/ad-sets/{adSetId}`. Mutually exclusive
        with `creatives[]`.

        The attached ad takes the full single-creative surface:
        `headline`/`body`/`description`/`callToAction` plus either
        `imageUrl`/`video` OR `placementAssets` (its own per-placement
        Feed/Story assets), and `leadGenFormId` when the target is a
        lead ad set (the parent must be ON_AD — true for ad sets
        created via goal `lead_generation`; Meta rejects a formless ad
        there, so pass the form on EVERY attached ad). This is the way
        to build N full ads sharing one ad set: create the first ad
        via the normal shape, then attach the rest one call each.

        Supported on Meta (facebook, instagram), TikTok, and
        LinkedIn. On TikTok the `adSetId` is the ad group ID; the
        new ad inherits the ad group's bid + budget + targeting.
        On LinkedIn the `adSetId` is the LinkedIn Campaign ID
        (numeric); we attach a new Creative to that Campaign, so
        the Campaign's `platformSpecificData` bidding, targeting,
        budget and schedule are inherited (passing those fields
        returns 400).
                existing_campaign_id: Meta + LinkedIn. On Meta: add the new ad set under this
        EXISTING campaign instead of creating a new one
        (multi-ad-set audience testing). The new ad set's budget
        is matched to the campaign's mode automatically: for a
        CBO campaign (campaign-level budget) omit
        `budgetAmount`/`budgetType` — the campaign owns the
        budget; for an ABO campaign pass them (they go on the new
        ad set). On LinkedIn: create a new Campaign (and its
        Creative) under this EXISTING CampaignGroup. On failure
        only the entities we authored are cleaned up; the
        pre-existing parent is left untouched and is never
        (re)activated. Mutually exclusive with `adSetId` and
        `creatives[]`.
                existing_creative_id: Meta only. Reuse an EXISTING ad creative by id instead of
        building a new one from the copy/media fields (which are then
        ignored). Combine with `existingCampaignId` to build a
        multi-ad-set campaign that shares one creative. Mutually
        exclusive with `creatives[]`, `dynamicCreative`, and
        `placementAssets`. The creative id used is returned as
        `creativeId` on the create response.
                business_name: Google Display only
                board_id: Pinterest only. Board ID (auto-creates if not provided).
                organization_id: LinkedIn only. The Company Page that authors the Direct Sponsored Content ("dark") post backing the ad — accepts a numeric organization ID or a full `urn:li:organization:N` URN. Required unless the resolved `accountId` is a connected LinkedIn Company-Page account (defaults to that page) or the LinkedIn ad account is org-owned (defaults to the account's owning organization). The authenticated member must be an ADMINISTRATOR or DIRECT_SPONSORED_CONTENT_POSTER of this page (and the page must be associated with the ad account), or LinkedIn returns 403. Ignored by every other platform.
                targeting: Nested targeting object — the same TargetingSpec shape as `POST /v1/ads/boost`,
        `POST /v1/ads/targeting/reach-estimate`, and `saved_targeting` audiences. Merged
        UNDER the flat inline targeting fields below: `savedTargetingId` < `targeting` <
        flat fields (a flat field present on the body replaces the nested value entirely).
        Both forms are equivalent; use whichever your integration already builds.
                countries: ISO 3166-1 alpha-2 country codes (e.g. ['NL']). Defaults to ['US'] when no other geo targeting (flat or nested `targeting`) is provided. (LinkedIn and OpenAI Ads currently honour country-level targeting only; any other targeting field returns 400 for OpenAI Ads.)
                cities: City-level geo targeting (Meta and TikTok). Each city is targeted by the platform's opaque `key` (the city ID) which can be looked up via `GET /v1/ads/targeting/search?dimension=geo&q=<name>&countryCode=<ISO>`. Optional `radius` + `distance_unit` (Meta only) extend the targeting beyond the city limits (e.g. radius 25 km around the city center). Both must be set together, or both omitted (Meta defaults to ~16 km when omitted).

        On Meta, cannot overlap with the same country in `countries` (Meta returns a "locations overlap" error). Either drop the country or scope it to a different country. On TikTok, keys are numeric location ids and can be sent without `countries`.
                regions: Region-level (state/province) geo targeting (Meta and TikTok). Each region is targeted by the platform's opaque `key` (the region ID) which can be looked up via `GET /v1/ads/targeting/search?dimension=geo&q=<name>&countryCode=<ISO>`.
                age_min
                age_max
                interests: Interest objects from /v1/ads/interests. Each must include id and name.
                zips: Postal/ZIP geo targeting. `key` is the platform's postal location ID from /v1/ads/targeting/search?dimension=geo&geoType=zip. Supported on Meta, Google, TikTok, Pinterest, X.
                metros: DMA / metro-area geo targeting (Meta and TikTok). `key` is the platform's metro ID from /v1/ads/targeting/search?dimension=geo&geoType=metro (TikTok metros appear as type `metro`, e.g. the New York DMA).
                custom_locations: Point-radius (lat/lng) geo targeting. Meta only (custom_locations). Rejected on platforms without radius support.
                behaviors: Behaviour entities from /v1/ads/targeting/search?dimension=behavior. Supported on Meta and TikTok. Each must include id.
                income_tier: Normalized household-income tier. Meta and TikTok express all four; Google maps only
        `top_10`; rejected on LinkedIn, X, and Pinterest. On Meta, income targeting is incompatible
        with housing/employment/credit `specialAdCategories`.
                languages: Language codes restricting the audience by language. On Meta, ISO 639-1 codes (e.g. ['en'], ['de']); a bare code targets all regional variants ("en" = all English), or use a region-qualified code for a specific one ("en_GB", "pt_BR", "zh_TW"). Unknown codes are rejected. Other ad platforms use their own language-code systems.
                placements: Meta only. Manual ad placements. Omit for automatic placements (Meta's default,
        recommended for most cases — Meta optimises delivery across all eligible surfaces).
        When set, restricts delivery to the chosen surfaces, mapped onto the ad set's
        `targeting.{publisher_platforms, facebook_positions, instagram_positions,
        messenger_positions, audience_network_positions, threads_positions,
        whatsapp_positions, device_platforms}`. Enum membership is validated here; Meta
        additionally enforces co-selection rules (e.g. some positions require their parent
        publisher platform) and returns an actionable error which we surface. Non-Meta
        platforms reject this field.
                saved_targeting_id: ID of a `saved_targeting` audience (created via POST /v1/ads/audiences). When set, its stored
        TargetingSpec is expanded as the base targeting; inline fields on this body merge on top. Lets you
        reuse a named targeting preset without re-sending every field.
                raw_targeting: Meta only. A raw Meta-native targeting spec (snake_case: `geo_locations`, `age_min`,
        `excluded_custom_audiences`, `flexible_spec`, `targeting_automation`, `user_os`,
        `wireless_carrier`, business places, etc.) — exactly the shape `GET /v1/ads/{adId}` returns for
        external ads. Sent alone it reaches the ad set VERBATIM (the clone-a-campaign's-targeting-exactly
        path). Meta validates and surfaces any errors.

        Can be combined with the camelCase targeting fields (countries/regions/cities/interests/ageMin/...,
        `targeting`, `savedTargetingId`, `audienceId`): rawTargeting is the BASE layer and the built
        camelCase spec is merged on top, key by key, with the camelCase side winning on collision (the
        camelCase precedence chain stays `savedTargetingId` < `targeting` < flat fields). The merge goes
        one level deep inside `geo_locations` and `excluded_geo_locations`: built sub-keys win, raw-only
        sub-keys such as `location_types` survive alongside built `countries`. Array values
        (`flexible_spec`, ...) are replaced as a WHOLE key when the camelCase spec builds them, never
        element-merged. When rawTargeting is present the defaults the camelCase builder normally injects
        (US geo, `targeting_automation.advantage_audience: 0`) are suppressed, so raw's values are not
        clobbered — include `targeting_automation` in the raw spec (or send `advantageAudience`) as Meta
        requires it on create. If cloning an EU campaign, also pass `dsaBeneficiary` / `dsaPayor` (those
        are separate fields, not part of targeting).
                special_ad_categories: Meta only. Declares the ad's special category, required for housing, employment, credit, or
        political/social-issue ads (Meta enforces restricted targeting for these). Note: setting a special
        category disables income/zip targeting on Meta.
                special_ad_category_country: Meta (metaads) only. 2-letter ISO country codes the special ad category applies to. Requires
        specialAdCategories to be set (400 otherwise). Ignored when joining an existing campaign via
        existingCampaignId (the existing campaign's category/country already governs it).
                end_date: Required for lifetime budgets
                start_date: Meta only. Ad-set start time (ISO 8601, e.g. "2026-06-10T09:00:00Z"), mapped to the
        ad set's `start_time`. When omitted the ad starts delivering immediately. For lifetime
        budgets Meta also requires `endDate`. (Same `schedule.startDate` semantics already
        available on `POST /v1/ads/boost`.)
                instagram_account_id: Meta only. Override the Instagram account the ad is delivered as — pass an Instagram
        Business Account ID (e.g. 17841...), mapped to the creative's `instagram_user_id`.
        When omitted we auto-resolve the IG account linked to the connected Facebook Page
        (the existing default). Useful when a Page has more than one eligible IG account.
                dynamic_creative: Meta only. Dynamic Creative: supply a POOL of assets and Meta auto-combines and
        optimises them into the best-performing variations within a single ad (mapped to the
        creative's `asset_feed_spec`). When set, the top-level single-creative fields
        (`imageUrl`, `headline`, `body`, `linkUrl`, `callToAction`) are ignored. Mutually
        exclusive with the `creatives[]` multi-creative shape. Exactly ONE of `imageUrls` /
        `videoUrls` is required (Meta allows one ad format per asset feed; sending both →
        400). Meta limits: ≤10 images or ≤10 videos, ≤5 bodies / titles / descriptions.
                carousel_cards: Meta only. Hand-built carousel: 2-10 authored cards in DETERMINISTIC order, mapped to
        the creative's `link_data.child_attachments`. Unlike `dynamicCreative`,
        you control the card order and per-card copy/link. Requires top-level `body`,
        `linkUrl` and `callToAction`.
        Mutually exclusive with `imageUrl`/`video`, `creatives[]`, `dynamicCreative`,
        `placementAssets`, `existingCreativeId`, `adSetId`, `leadGenFormId` and goal
        `catalog_sales`.
                default_locale: Meta only. Language the top-level copy is written in (e.g. `en`, `pt_BR`), used by the `translations` default rule. Defaults to `en`. Meta rejects a language asset feed whose default rule carries no locales of its own. Must NOT also appear as an entry in `translations`.
                translations: Meta only. Multi-language ads (Dynamic Language Optimization): ONE ad carrying
        per-locale copy and, optionally, per-locale media — the "Languages" toggle in Ads
        Manager. Keeps social proof (likes/comments/shares) on a SINGLE post instead of
        splitting it across one ad per language.

        The ad's top-level copy is the DEFAULT shown to every locale you do NOT list,
        and it counts as one of the language variants.

        IMPORTANT, and the opposite of what you might expect: text does NOT inherit.
        Every entry must carry its own `headline`, `body` AND `description`, and all of
        them must be DISTINCT from each other and from the ad's top-level copy. Meta
        deduplicates identical strings inside the asset feed, so two locales sharing a
        string collapse into one asset and the create fails with a misleading "Too few
        ... texts provided in asset creation" (subcode 1885817) that names a field which
        is actually present. We validate this before calling Meta and return a 400
        naming the offending locale and field. `description` is therefore effectively
        required on the ad whenever `translations` is present, even though it is
        optional otherwise.

        Do NOT list `defaultLocale` inside `translations`: Meta rejects the duplicate
        with "The language asset feed includes an unsupported targeting field"
        (subcode 1885985).

        Media DOES inherit and is uploaded once when shared, and `linkUrl` inherits
        too: each locale may name its own landing page and unlisted locales fall back
        to the ad's top-level `linkUrl`. Note that Meta enforces
        Dynamic Creative image dimensions on language feeds, so an `imageUrl` that
        works on a normal ad may be rejected with "The following images have invalid
        dimensions for Dynamic Creative" (subcode 1885558). Video is not affected.

        Mutually exclusive with `dynamicCreative`, `placementAssets`, `carouselCards` and
        `existingCreativeId` — Meta allows one `asset_feed_spec` shape per creative.
                placement_assets: Meta only. Placement asset customization: pin a SPECIFIC asset (image OR video) to
        each placement group on a SINGLE ad (e.g. a 9:16 on Stories/Reels and a 4:5 on Feed).
        The same thing Meta Ads Manager produces with "different creative per placement",
        mapped to the creative's `asset_feed_spec` + `asset_customization_rules`. Deterministic
        pinning, NOT the auto-optimizing pool of `dynamicCreative` (mutually exclusive). Works
        on the legacy single shape AND the attach shape (`adSetId` + placementAssets adds one
        placement-customized ad to an existing ad set — the way to build N per-placement ads
        sharing one ad set: create the first normally, attach the rest). Cannot be combined
        with `creatives[]`. Shared copy (headline, body, link,
        CTA) comes from the top-level single-creative fields since only the asset varies by
        placement. Each rule's `placements` accepts the same fields as the top-level
        `placements` object; Meta enforces co-selection rules and returns an actionable error.

        Note on text rendering: Meta suppresses primary text and headline on fullscreen
        placements (Stories and Reels) in actual ad delivery; the fields are accepted and
        the ad publishes, but the copy is not shown to users. For visible copy on those
        placements, bake the text into the creative image or video itself.

        A block is all-image OR all-video, never mixed (Meta's asset_feed_spec carries one ad
        format). Image mode: `defaultImageUrl` + `rules[].imageUrl`. Video mode:
        `defaultVideoUrl` + `rules[].videoUrl` (optional `thumbnailUrl`/`defaultThumbnailUrl`
        posters; Meta auto-generates when omitted). Exactly one catch-all default is required.
                audience_id: Custom audience ID for targeting
                campaign_type: Google only
                keywords: Google Search only. BROAD-match keywords on the new ad group (first 20).
                negative_keywords: Google Search only; other platforms return 400. BROAD-match negative keywords on the new ad group. Editable later via PUT /v1/ads/{adId} targeting.negativeKeywords.
                additional_headlines: Google Search RSA only. Extra headlines.
                additional_descriptions: Google Search RSA only. Extra descriptions.
                advantage_audience: Meta only. Controls the Advantage audience feature (targeting_automation). 0 = disabled (default), 1 = enabled. Meta Marketing API requires this field on all ad set creation requests.
                attribution_spec: Meta only. Conversion attribution window for the ad set — maps 1:1 to Meta's
        ad-set `attribution_spec`. Only honored for conversion goals (`conversions`,
        `lead_generation`, `app_promotion`); ignored for awareness/traffic/engagement.
        Omit to use Meta's default (`7-day click` + `1-day view`). Meta enforces the
        valid combinations: `VIEW_THROUGH` only allows `windowDays: 1` (7d/28d view
        windows were removed Jan 2026); `ENGAGED_VIDEO_VIEW` only `1` and only alongside
        `VIEW_THROUGH: 1`; `CLICK_THROUGH: 28` only on certain objectives. Invalid combos
        surface as a Meta 400.
        Example: `[{ "eventType": "CLICK_THROUGH", "windowDays": 7 }, { "eventType": "VIEW_THROUGH", "windowDays": 1 }]`
                gender: Restrict the audience by gender. 'male' targets men only, 'female' targets women only, 'all' (default) targets everyone. Applied on Meta, TikTok and Pinterest. Ignored on Google, LinkedIn and X.
                bid_strategy: Deprecated: send it inside `platformSpecificData` instead (Meta today; TikTok's nested shape is planned). The flat field keeps working during the deprecation window; sending both shapes returns a 400.

        Meta bid strategy applied to the ad set.
                bid_amount: Deprecated: send it inside `platformSpecificData` instead (Meta today; TikTok's nested shape is planned). The flat field keeps working during the deprecation window; sending both shapes returns a 400.

        Bid cap in WHOLE currency units (USD: 5 = $5.00; JPY: 100 = ¥100). Required when
        `bidStrategy` is `LOWEST_COST_WITH_BID_CAP` or `COST_CAP`. Meta only: sending
        `bidAmount` WITHOUT `bidStrategy` requires `existingCampaignId` (400 otherwise),
        and sets the new ad set's cap under the joined campaign's COST_CAP /
        LOWEST_COST_WITH_BID_CAP parent. The strategy itself is inherited from the
        campaign. Restating bidStrategy here is accepted but has no effect on the ad set.

        Rejected with 400 in `adSetId` attach mode: that shape inherits its cap from
        the platform. Use `PUT /v1/ads/ad-sets/{adSetId}` there instead.
                roas_average_floor: Deprecated: send it inside `platformSpecificData` instead (Meta today; TikTok's nested shape is planned). The flat field keeps working during the deprecation window; sending both shapes returns a 400.

        Minimum ROAS as a decimal multiplier (e.g. 2.0 = 2.0x ROAS). Required when
        `bidStrategy` is `LOWEST_COST_WITH_MIN_ROAS`. Sending it without `bidStrategy`
        is a 400. Sent to Meta as
        `bid_constraints.roas_average_floor` × 10000. Known gap: a CBO campaign's
        ROAS floor lives on the campaign only (set via `POST /v1/ads/campaigns`);
        there is no supported way to set it while joining a CBO campaign here.
                value_rule_set_id: Meta only (facebook, instagram; other platforms return 400). Value rule set
        to attach to the new ad set, from `/v1/ads/value-rule-sets`. Attachment is
        driven by this id, so `valueRulesApplied` is optional alongside it.

        Rejected with 400 in `adSetId` attach mode: that shape inherits the existing
        ad set's attachment, so the field would be silently ignored. Use
        `PUT /v1/ads/ad-sets/{adSetId}` there instead.

        Ignored (stripped before the ad-set create) when `buyingType` is `RESERVED`:
        value rules only apply to auction ad sets on `LOWEST_COST_WITHOUT_CAP` or
        `COST_CAP`, and a Reach & Frequency reservation has no auction bid strategy.

        Read back with `GET /v1/ads/ad-sets/{adSetId}?fields=value_rule_set_id`; the
        attachment is not mirrored onto Zernio's ad documents.
                value_rules_applied: Meta only (facebook, instagram; other platforms return 400). Optional when
        attaching, and requires `valueRuleSetId`. `false` is REJECTED here with 400:
        a newly created ad set has nothing to detach, so detaching lives on
        `PUT /v1/ads/ad-sets/{adSetId}`.
                platform_specific_data: Platform-specific options. The platform is derived from `accountId`;
        sending options for a different platform returns a 400. LinkedIn
        (campaign bidding and delivery controls) and Meta (the bid trio)
        have options today.

        **Meta**: `bidStrategy`, `bidAmount` and `roasAverageFloor` may be
        sent here instead of at the root — the preferred home going forward.
        Sending the bid fields in BOTH places returns a 400
        (`mutually_exclusive_fields`), and sending any of them in
        `adSetId` attach mode is a 400 too (the ad set already has its bid).
                dsa_beneficiary: Legal entity that benefits from the ad. Required when targeting EU users
        (EU DSA, Article 26). Optional if the ad account has a default beneficiary:
        set it once via `PATCH /v1/ads/accounts` or in Meta Ads Manager, and Meta
        fills it in whenever the field is omitted.
                dsa_payor: Legal entity that pays for the ad. Can differ from `dsaBeneficiary`
        (for example, an agency paying for a client's ads). Same rules as
        `dsaBeneficiary`: required for EU targeting unless the ad account has
        a default payor.
                brand_identity: TikTok only. Synthetic Brand Identity used when the ad
        attributes to a CUSTOMIZED_USER (instead of a real TT_USER
        @username). Required on the FIRST CUSTOMIZED_USER ad on a
        `tiktokads` SocialAccount with no cached identity; omit on
        subsequent ads (the identity is cached on the account after
        first creation). Non-TikTok platforms ignore this field.

        Alternative: configure once via `PATCH /v1/connect/tiktok-ads`,
        then create ads without this field.
                identity_type: TikTok only. Forces the identity attribution on the ad:

          - `TT_USER`: the posting account's open_id (real @username
            branding). Requires a connected TikTok posting account
            on the same profile.
          - `CUSTOMIZED_USER`: synthetic Brand Identity (display
            name + avatar). Requires a configured Brand Identity
            (cached on the `tiktokads` SocialAccount via
            `PATCH /v1/connect/tiktok-ads`) or an inline
            `brandIdentity` to create one on the fly.

        When omitted, defaults to `TT_USER` if a posting account is
        connected on this profile, else `CUSTOMIZED_USER`. Spark
        Ads (`POST /v1/ads/boost`) always use `TT_USER` regardless
        of this field — TikTok requires the original organic
        post's author identity for Spark.
                smart_plus: TikTok only. Creates the ad as a TikTok Upgraded Smart+
        campaign: TikTok automates targeting, bidding and delivery. Supports goals
        `conversions` (Smart+ Web Conversions), `lead_generation` (Smart+ Lead
        Generation with a website form on `linkUrl`; TikTok Instant Forms not supported)
        and `app_promotion` (Smart+ App installs; the ad's destination is the app store,
        so `linkUrl` is not used). The web goals require `promotedObject.pixelId` AND
        `promotedObject.customEventType`; `app_promotion` requires
        `promotedObject.applicationId` instead.
        Targeting works like on any TikTok ad (defaults to `countries: ["US"]` when
        omitted); TikTok automates delivery within it.
        The budget lives on the Smart+ campaign (Campaign Budget Optimization); a `lifetime`
        budget additionally requires `endDate`. Cannot be combined with `adSetId`.
                promoted_object: What the ad optimises against. Behaviour depends on the platform.

        **Meta**: forwarded to the ad set's `promoted_object` (snake-cased).
        Required for goals whose ad-set optimization_goal points at a specific
        event/page/app (without it Meta rejects the ad-set create with
        `error_subcode: 1815430` "Please select a promoted object for your ad set"):
          - `goal: conversions` / `lead_conversion` (OFFSITE_CONVERSIONS): requires `pixelId` + `customEventType`, or `customConversionId` when optimising against a Custom Conversion (the conversion carries its own event definition). For a pixel CUSTOM event (one you named yourself in CAPI/Events Manager), send `customEventType: OTHER` + `customEventStr` with the event name.
          - `goal: app_promotion` (APP_INSTALLS): requires `applicationId` + `objectStoreUrl`
          - `goal: lead_generation` (LEAD_GENERATION): `pageId` is auto-filled from the connected Page when omitted

        Other Meta goals (engagement, traffic, awareness, video_views) ignore this field.

        **TikTok**: used by `goal: conversions` and the Smart+ goals (`smartPlus: true`).
          - `pixelId` maps to the ad group's `pixel_id`. Required: a TikTok website-conversion
            ad group without a pixel is rejected with `40002: Please select a pixel`.
          - `customEventType` maps to the ad group's `optimization_event` (the pixel event to
            optimise for). Optional on the regular conversions flow, required on Smart+.
            See the `customEventType` field below for the valid TikTok codes.
          - `applicationId` (Smart+ `goal: app_promotion` only) maps to the ad group's `app_id`:
            the App ID of an app registered on the TikTok Ads account (Assets → Events →
            App Events). Install optimization needs the app's MMP tracking configured.

        The remaining `promotedObject.*` fields are Meta-only. Platforms other than
        Meta and TikTok ignore `promotedObject` entirely."""
        client = _get_client()
        try:
            response = client.ad_campaigns.create_standalone_ad(
                account_id=account_id,
                ad_account_id=ad_account_id,
                name=name,
                campaign_name=campaign_name,
                ad_set_name=ad_set_name,
                ad_name=ad_name,
                tracking=tracking,
                goal=goal,
                optimization_goal=optimization_goal,
                billing_event=billing_event,
                buying_type=buying_type,
                rf_prediction_id=rf_prediction_id,
                creative_features=creative_features,
                multi_advertiser=multi_advertiser,
                validate_only=validate_only,
                budget_amount=budget_amount,
                budget_type=budget_type,
                status=status,
                budget_level=budget_level,
                currency=currency,
                headline=headline,
                long_headline=long_headline,
                body=body,
                description=description,
                call_to_action=call_to_action,
                link_url=link_url,
                lead_gen_form_id=lead_gen_form_id,
                image_url=image_url,
                images=images,
                video=video,
                creatives=creatives,
                ad_set_id=ad_set_id,
                existing_campaign_id=existing_campaign_id,
                existing_creative_id=existing_creative_id,
                business_name=business_name,
                board_id=board_id,
                organization_id=organization_id,
                targeting=targeting,
                countries=countries,
                cities=cities,
                regions=regions,
                age_min=age_min,
                age_max=age_max,
                interests=interests,
                zips=zips,
                metros=metros,
                custom_locations=custom_locations,
                behaviors=behaviors,
                income_tier=income_tier,
                languages=languages,
                placements=placements,
                saved_targeting_id=saved_targeting_id,
                raw_targeting=raw_targeting,
                special_ad_categories=special_ad_categories,
                special_ad_category_country=special_ad_category_country,
                end_date=end_date,
                start_date=start_date,
                instagram_account_id=instagram_account_id,
                dynamic_creative=dynamic_creative,
                carousel_cards=carousel_cards,
                default_locale=default_locale,
                translations=translations,
                placement_assets=placement_assets,
                audience_id=audience_id,
                campaign_type=campaign_type,
                keywords=keywords,
                negative_keywords=negative_keywords,
                additional_headlines=additional_headlines,
                additional_descriptions=additional_descriptions,
                advantage_audience=advantage_audience,
                attribution_spec=attribution_spec,
                gender=gender,
                bid_strategy=bid_strategy,
                bid_amount=bid_amount,
                roas_average_floor=roas_average_floor,
                value_rule_set_id=value_rule_set_id,
                value_rules_applied=value_rules_applied,
                platform_specific_data=platform_specific_data,
                dsa_beneficiary=dsa_beneficiary,
                dsa_payor=dsa_payor,
                brand_identity=brand_identity,
                identity_type=identity_type,
                smart_plus=smart_plus,
                promoted_object=promoted_object,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # AD_CREATIVES

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Render pre-create ad previews",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_creatives_generate_ad_previews(
        account_id: str,
        ad_account_id: str,
        formats: list[str] | None = None,
        existing_creative_id: str | None = None,
        creative_spec: dict[str, Any] | None = None,
    ) -> str:
        """Render pre-create ad previews

        Args:
            account_id: Zernio SocialAccount id used to resolve the Meta token. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)
            formats: Meta ad_format values, one preview per format. Defaults to [DESKTOP_FEED_STANDARD].
            existing_creative_id: Preview an existing ad-account creative by id. Mutually exclusive with creativeSpec.
            creative_spec: Raw Meta creative spec forwarded verbatim to /generatepreviews. Mutually exclusive with existingCreativeId."""
        client = _get_client()
        try:
            response = client.ad_creatives.generate_ad_previews(
                account_id=account_id,
                ad_account_id=ad_account_id,
                formats=formats,
                existing_creative_id=existing_creative_id,
                creative_spec=creative_spec,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Render previews of an existing ad",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_creatives_get_ad_previews(ad_id: str, formats: str | None = None) -> str:
        """Render previews of an existing ad

        Args:
            ad_id: Zernio ad id (24-char hex). (required)
            formats: Comma-separated Meta ad_format values (max 10), one preview per format. Defaults to DESKTOP_FEED_STANDARD."""
        client = _get_client()
        try:
            response = client.ad_creatives.get_ad_previews(ad_id=ad_id, formats=formats)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Creative library",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_creatives_list_ad_creatives(
        account_id: str,
        ad_account_id: str,
        fields: str | None = None,
        limit: int = 25,
        after: str | None = None,
    ) -> str:
        """Creative library

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)
            fields: Comma-separated Graph field override (supports nested {} projections).
            limit: Rows per page
            after: Cursor from paging.after of the previous page."""
        client = _get_client()
        try:
            response = client.ad_creatives.list_ad_creatives(
                account_id=account_id,
                ad_account_id=ad_account_id,
                fields=fields,
                limit=limit,
                after=after,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a standalone creative",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_creatives_create_ad_creative(
        account_id: str,
        ad_account_id: str,
        headline: str,
        body: str,
        link_url: str,
        description: str | None = None,
        call_to_action: str = "LEARN_MORE",
        image_url: str | None = None,
        image_hash: str | None = None,
        carousel_cards: list[dict[str, Any]] | None = None,
        url_tags: str | None = None,
        creative_features: dict[str, Any] | None = None,
        multi_advertiser: str | None = None,
    ) -> str:
        """Create a standalone creative

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token and Page. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)
            headline: (required)
            body: Primary text (required)
            description: Link description below the headline; omitted = Meta scrapes the destination's OG description.
            call_to_action: CTA type (same whitelist as POST /v1/ads/create).
            link_url: (required)
            image_url: Publicly reachable image; uploaded to the account's library server-side.
            image_hash: Existing library image hash (POST /v1/ads/images or GET /v1/ads/images).
            carousel_cards
            url_tags: Appended to every outbound URL (e.g. utm_source=fb).
            creative_features: Advantage+ creative enhancements: partial map of Meta creative feature keys (snake_case) to enroll status, forwarded as degrees_of_freedom_spec.creative_features_spec. Unspecified features default to OPT_OUT.
            multi_advertiser: Meta only. Multi-advertiser ads: whether Meta may show this ad alongside other advertisers' in one unit. Meta auto-enrols since Aug 2024, so send OPT_OUT to leave. It is a top-level creative field, NOT a `creativeFeatures` key — Meta rejects it there."""
        client = _get_client()
        try:
            response = client.ad_creatives.create_ad_creative(
                account_id=account_id,
                ad_account_id=ad_account_id,
                headline=headline,
                body=body,
                description=description,
                call_to_action=call_to_action,
                link_url=link_url,
                image_url=image_url,
                image_hash=image_hash,
                carousel_cards=carousel_cards,
                url_tags=url_tags,
                creative_features=creative_features,
                multi_advertiser=multi_advertiser,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Creative details",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_creatives_get_ad_creative(
        creative_id: str, account_id: str, fields: str | None = None
    ) -> str:
        """Creative details

        Args:
            creative_id: Platform creative id (required)
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            fields: Comma-separated Graph field override (supports nested {} projections)."""
        client = _get_client()
        try:
            response = client.ad_creatives.get_ad_creative(
                creative_id=creative_id, account_id=account_id, fields=fields
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Rename a creative",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_creatives_update_ad_creative(
        creative_id: str, account_id: str, name: str
    ) -> str:
        """Rename a creative

        Args:
            creative_id: Platform creative id (required)
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            name: (required)"""
        client = _get_client()
        try:
            response = client.ad_creatives.update_ad_creative(
                creative_id=creative_id, account_id=account_id, name=name
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete a creative",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_creatives_delete_ad_creative(creative_id: str, account_id: str) -> str:
        """Delete a creative

        Args:
            creative_id: Platform creative id (required)
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)"""
        client = _get_client()
        try:
            response = client.ad_creatives.delete_ad_creative(
                creative_id=creative_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Upload an ad image from base64",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_creatives_upload_ad_image(
        account_id: str,
        ad_account_id: str,
        image_base64: str,
        filename: str | None = None,
    ) -> str:
        """Upload an ad image from base64

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)
            image_base64: Raw base64 image bytes, or a full data URL (the data:image/...;base64, prefix is stripped). (required)
            filename: Optional filename shown in Meta's image library. Defaults to ad_image.jpg."""
        client = _get_client()
        try:
            response = client.ad_creatives.upload_ad_image(
                account_id=account_id,
                ad_account_id=ad_account_id,
                image_base64=image_base64,
                filename=filename,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Ad image library",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_creatives_list_ad_images(
        account_id: str,
        ad_account_id: str,
        fields: str | None = None,
        limit: int = 25,
        after: str | None = None,
    ) -> str:
        """Ad image library

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant) used to resolve the Meta token. (required)
            ad_account_id: Meta ad account id (act_<n>). (required)
            fields: Comma-separated Graph field override (supports nested {} projections).
            limit: Rows per page
            after: Cursor from paging.after of the previous page."""
        client = _get_client()
        try:
            response = client.ad_creatives.list_ad_images(
                account_id=account_id,
                ad_account_id=ad_account_id,
                fields=fields,
                limit=limit,
                after=after,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Meta product catalogs",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_creatives_list_ad_catalogs(account_id: str, ad_account_id: str) -> str:
        """List Meta product catalogs

        Args:
            account_id: A facebook, instagram, or metaads social account ID (required)
            ad_account_id: Meta ad account ID (act_...) (required)"""
        client = _get_client()
        try:
            response = client.ad_creatives.list_ad_catalogs(
                account_id=account_id, ad_account_id=ad_account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List a catalog's product sets",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_creatives_list_ad_catalog_product_sets(
        catalog_id: str, account_id: str
    ) -> str:
        """List a catalog's product sets

        Args:
            catalog_id: Meta product catalog ID (from GET /v1/ads/catalogs) (required)
            account_id: A facebook, instagram, or metaads social account ID (required)"""
        client = _get_client()
        try:
            response = client.ad_creatives.list_ad_catalog_product_sets(
                catalog_id=catalog_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # AD_INSIGHTS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Google Ads search terms report",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_insights_get_ads_search_terms(
        account_id: str,
        customer_id: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        campaign_id: str | None = None,
        ad_group_id: str | None = None,
        page_token: str | None = None,
    ) -> str:
        """Google Ads search terms report

        Args:
            account_id: Google ads SocialAccount id. (required)
            customer_id: Numeric Google Ads customer id (no dashes). Defaults to the account's connected customer.
            from_date: Defaults to 30 days ago.
            to_date: Defaults to today.
            campaign_id: Numeric Google campaign id filter.
            ad_group_id: Numeric Google ad group id filter.
            page_token: Cursor from paging.nextPageToken of the previous page."""
        client = _get_client()
        try:
            response = client.ad_insights.get_ads_search_terms(
                account_id=account_id,
                customer_id=customer_id,
                from_date=from_date,
                to_date=to_date,
                campaign_id=campaign_id,
                ad_group_id=ad_group_id,
                page_token=page_token,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Google Local Services Ads leads",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_insights_list_local_services_leads(
        account_id: str,
        customer_id: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        lead_type: str | None = None,
        lead_status: str | None = None,
        charged_only: bool | None = None,
        page_token: str | None = None,
    ) -> str:
        """Google Local Services Ads leads

        Args:
            account_id: Google ads SocialAccount id. (required)
            customer_id: Numeric Google Ads customer id (no dashes). Defaults to the account's connected customer.
            from_date: Leads created at/after this day.
            to_date: Leads created at/before this day.
            lead_type
            lead_status: Google LocalServicesLeadStatus enum value (e.g. NEW, BOOKED, WIPED_OUT).
            charged_only: true = only leads Google charged for.
            page_token: Cursor from paging.nextPageToken of the previous page."""
        client = _get_client()
        try:
            response = client.ad_insights.list_local_services_leads(
                account_id=account_id,
                customer_id=customer_id,
                from_date=from_date,
                to_date=to_date,
                lead_type=lead_type,
                lead_status=lead_status,
                charged_only=charged_only,
                page_token=page_token,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Conversations of a Local Services lead",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_insights_list_local_services_lead_conversations(
        lead_id: str,
        account_id: str,
        customer_id: str | None = None,
        page_token: str | None = None,
    ) -> str:
        """Conversations of a Local Services lead

        Args:
            lead_id: Numeric lead id from /v1/ads/local-services/leads. (required)
            account_id: Google ads SocialAccount id. (required)
            customer_id: Numeric Google Ads customer id (no dashes). Defaults to the account's connected customer.
            page_token: Cursor from paging.nextPageToken of the previous page."""
        client = _get_client()
        try:
            response = client.ad_insights.list_local_services_lead_conversations(
                lead_id=lead_id,
                account_id=account_id,
                customer_id=customer_id,
                page_token=page_token,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get campaign analytics",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_insights_get_campaign_analytics(
        campaign_id: str,
        platform: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        breakdowns: str | None = None,
    ) -> str:
        """Get campaign analytics

            Args:
                campaign_id: Platform campaign id (platformCampaignId). (required)
                platform: Disambiguate when the campaign id exists across platforms (e.g. facebook, instagram).
                from_date: Start of date range (YYYY-MM-DD). Defaults to 90 days ago.
                to_date: End of date range (YYYY-MM-DD). Defaults to today. Max 730-day range.
                breakdowns: Comma-separated breakdown dimensions.

        **Meta**: age, gender, country, publisher_platform, device_platform, region,
        platform_position, impression_device, video_asset, image_asset, body_asset, title_asset.

        **LinkedIn** (firmographics): job_title, job_function, seniority, industry,
        company, company_size, country, region. Rows carry the raw pivot `value`
        plus a resolved `name`. LinkedIn serves these aggregated over the whole
        range, delays the data 12-24h, and omits segments with fewer than 3 events."""
        client = _get_client()
        try:
            response = client.ad_insights.get_campaign_analytics(
                campaign_id=campaign_id,
                platform=platform,
                from_date=from_date,
                to_date=to_date,
                breakdowns=breakdowns,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Generate keyword ideas (Google Keyword Planner)",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_insights_generate_keyword_ideas(
        account_id: str,
        customer_id: str | None = None,
        seed_keywords: list[str] | None = None,
        seed_url: str | None = None,
        countries: list[str] | None = None,
        language_constant_id: str = "1000",
        network: str = "GOOGLE_SEARCH",
        include_adult_keywords: bool | None = None,
        page_size: int | None = None,
        page_token: str | None = None,
    ) -> str:
        """Generate keyword ideas (Google Keyword Planner)

        Args:
            account_id: Zernio googleads SocialAccount id. (required)
            customer_id: Numeric Google Ads customer id (no dashes); only needed when the connection has several accounts.
            seed_keywords: Seed terms. Provide these, seedUrl, or both.
            seed_url: Landing page to mine for ideas. Provide this, seedKeywords, or both.
            countries: ISO 3166-1 alpha-2 country codes. Omitted = worldwide.
            language_constant_id: Google languageConstant id (1000 = English).
            network
            include_adult_keywords
            page_size
            page_token: Cursor from paging.nextPageToken of the previous page."""
        client = _get_client()
        try:
            response = client.ad_insights.generate_keyword_ideas(
                account_id=account_id,
                customer_id=customer_id,
                seed_keywords=seed_keywords,
                seed_url=seed_url,
                countries=countries,
                language_constant_id=language_constant_id,
                network=network,
                include_adult_keywords=include_adult_keywords,
                page_size=page_size,
                page_token=page_token,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Historical keyword metrics (Google Keyword Planner)",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_insights_generate_keyword_historical_metrics(
        account_id: str,
        keywords: list[str] | None,
        customer_id: str | None = None,
        countries: list[str] | None = None,
        language_constant_id: str = "1000",
        network: str = "GOOGLE_SEARCH",
        include_adult_keywords: bool | None = None,
        include_average_cpc: bool | None = None,
    ) -> str:
        """Historical keyword metrics (Google Keyword Planner)

        Args:
            account_id: Zernio googleads SocialAccount id. (required)
            customer_id: Numeric Google Ads customer id (no dashes); only needed when the connection has several accounts.
            keywords: (required)
            countries: ISO 3166-1 alpha-2 country codes. Omitted = worldwide.
            language_constant_id: Google languageConstant id (1000 = English).
            network
            include_adult_keywords
            include_average_cpc: Adds averageCpcMicros to each row's keywordMetrics."""
        client = _get_client()
        try:
            response = client.ad_insights.generate_keyword_historical_metrics(
                account_id=account_id,
                customer_id=customer_id,
                keywords=keywords,
                countries=countries,
                language_constant_id=language_constant_id,
                network=network,
                include_adult_keywords=include_adult_keywords,
                include_average_cpc=include_average_cpc,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Flexible live insights query",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_insights_query_ad_insights(
        account_id: str,
        object_id: str | None = None,
        query: str | None = None,
        customer_id: str | None = None,
        page_token: str | None = None,
        level: str | None = None,
        fields: str | None = None,
        breakdowns: str | None = None,
        action_breakdowns: str | None = None,
        action_attribution_windows: str | None = None,
        action_report_time: str | None = None,
        use_unified_attribution_setting: bool | None = None,
        filtering: str | None = None,
        date_preset: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        time_increment: str | None = None,
        limit: int = 25,
        after: str | None = None,
    ) -> str:
        """Flexible live insights query

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant); its platform selects the Meta or Google contract. (required)
            object_id: Meta only (required there): insights node — act_<n>, campaign id, ad set id or ad id.
            query: Google only (required there): the GAQL SELECT statement to run.
            customer_id: Google only: numeric customer id (no dashes) when the connection has several Google Ads accounts.
            page_token: Google only: cursor from paging.nextPageToken of the previous page.
            level: Row granularity
            fields: Comma-separated Graph insights fields (e.g. spend,impressions,frequency,website_purchase_roas). Omitted = Meta's default set.
            breakdowns: Comma-separated Graph breakdowns (e.g. age,gender or publisher_platform).
            action_breakdowns: Comma-separated Graph action breakdowns. Segments the actions[] arrays in each row.
            action_attribution_windows: Comma-separated Meta attribution windows. Action values are returned keyed per window.
            action_report_time: When actions are counted: impression, conversion or mixed.
            use_unified_attribution_setting: Use the ad sets' own attribution settings for action counting.
            filtering: JSON array of Meta filter objects: [{"field", "operator", "value"}]. Applied server-side by Meta.
            date_preset: Meta date_preset (e.g. last_7d, last_30d, this_month). Mutually exclusive with fromDate/toDate.
            from_date: Start of range (YYYY-MM-DD); requires toDate.
            to_date: End of range (YYYY-MM-DD); requires fromDate.
            time_increment: Days per row (1-90), monthly, or all_days.
            limit: Rows per page
            after: Cursor from paging.after of the previous page."""
        client = _get_client()
        try:
            response = client.ad_insights.query_ad_insights(
                account_id=account_id,
                object_id=object_id,
                query=query,
                customer_id=customer_id,
                page_token=page_token,
                level=level,
                fields=fields,
                breakdowns=breakdowns,
                action_breakdowns=action_breakdowns,
                action_attribution_windows=action_attribution_windows,
                action_report_time=action_report_time,
                use_unified_attribution_setting=use_unified_attribution_setting,
                filtering=filtering,
                date_preset=date_preset,
                from_date=from_date,
                to_date=to_date,
                time_increment=time_increment,
                limit=limit,
                after=after,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Submit an async insights report run",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_insights_create_ad_insights_report(
        account_id: str,
        object_id: str,
        level: str | None = None,
        fields: str | None = None,
        breakdowns: str | None = None,
        action_breakdowns: str | None = None,
        action_attribution_windows: list[str] | None = None,
        action_report_time: str | None = None,
        use_unified_attribution_setting: bool | None = None,
        filtering: list[dict[str, Any]] | None = None,
        date_preset: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        time_increment: str | None = None,
    ) -> str:
        """Submit an async insights report run

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant). (required)
            object_id: Meta insights node: act_<n>, campaign id, ad set id or ad id. (required)
            level
            fields: Comma-separated Graph insights fields.
            breakdowns: Comma-separated Graph breakdowns.
            action_breakdowns: Comma-separated Graph action breakdowns (e.g. action_type,action_destination).
            action_attribution_windows: Meta attribution windows (e.g. ["7d_click", "1d_view"]). Action values are returned keyed per window.
            action_report_time: When actions are counted: impression, conversion or mixed.
            use_unified_attribution_setting: Use the ad sets' own attribution settings for action counting.
            filtering: Meta filter objects, applied server-side.
            date_preset: Mutually exclusive with fromDate/toDate.
            from_date
            to_date
            time_increment"""
        client = _get_client()
        try:
            response = client.ad_insights.create_ad_insights_report(
                account_id=account_id,
                object_id=object_id,
                level=level,
                fields=fields,
                breakdowns=breakdowns,
                action_breakdowns=action_breakdowns,
                action_attribution_windows=action_attribution_windows,
                action_report_time=action_report_time,
                use_unified_attribution_setting=use_unified_attribution_setting,
                filtering=filtering,
                date_preset=date_preset,
                from_date=from_date,
                to_date=to_date,
                time_increment=time_increment,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Poll an async insights report run",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_insights_get_ad_insights_report(
        report_run_id: str, account_id: str, limit: int = 25, after: str | None = None
    ) -> str:
        """Poll an async insights report run

        Args:
            report_run_id: (required)
            account_id: Zernio SocialAccount id used to resolve the Meta token (must be the same connection that created the run). (required)
            limit
            after"""
        client = _get_client()
        try:
            response = client.ad_insights.get_ad_insights_report(
                report_run_id=report_run_id,
                account_id=account_id,
                limit=limit,
                after=after,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get ad analytics",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_insights_get_ad_analytics(
        ad_id: str,
        from_date: str | None = None,
        to_date: str | None = None,
        breakdowns: str | None = None,
    ) -> str:
        """Get ad analytics

            Args:
                ad_id: (required)
                from_date: Start of date range (YYYY-MM-DD). Defaults to 90 days ago.
                to_date: End of date range (YYYY-MM-DD). Defaults to today. Max 730-day range.
                breakdowns: Comma-separated breakdown dimensions.

        **Meta**: age, gender, country, publisher_platform, device_platform, region.

        **TikTok**: gender, age, country_code, platform, ac, language.

        **LinkedIn** (firmographics): job_title, job_function, seniority, industry,
        company, company_size, country, region. Rows carry the raw pivot `value`
        plus a resolved `name`. LinkedIn serves these aggregated over the whole
        range, delays the data 12-24h, and omits segments with fewer than 3 events."""
        client = _get_client()
        try:
            response = client.ad_insights.get_ad_analytics(
                ad_id=ad_id, from_date=from_date, to_date=to_date, breakdowns=breakdowns
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # AD_TARGETING

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Search targeting interests",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_targeting_search_ad_interests(q: str, account_id: str) -> str:
        """Search targeting interests

        Args:
            q: Search query (required)
            account_id: Social account ID (required)"""
        client = _get_client()
        try:
            response = client.ad_targeting.search_ad_interests(
                q=q, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Search targeting options",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_targeting_search_ad_targeting(
        account_id: str,
        q: str,
        dimension: str = "interest",
        geo_type: str = "city",
        country_code: str | None = None,
        limit: int = 25,
    ) -> str:
        """Search targeting options

        Args:
            account_id: Social account ID (a connected account on the target ad platform). (required)
            q: Search query. For geo, the locality name only (no region/country suffix). (required)
            dimension: What to search. `geo` resolves locations (scope further with `geoType`), `interest`/`behavior` resolve audience entities, `income` resolves income-tier options. Defaults to `interest` for backward compatibility with the deprecated /v1/ads/interests alias.
            geo_type: Only used when `dimension=geo`. The kind of location to resolve. Defaults to `city`.
            country_code: ISO 3166-1 alpha-2 country code (e.g. NL) to scope a geo search.
            limit: Maximum results to return."""
        client = _get_client()
        try:
            response = client.ad_targeting.search_ad_targeting(
                account_id=account_id,
                q=q,
                dimension=dimension,
                geo_type=geo_type,
                country_code=country_code,
                limit=limit,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Estimate audience reach",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_targeting_estimate_ad_reach(
        account_id: str,
        ad_account_id: str,
        spec: dict[str, Any] | None,
        optimization_goal: str | None = None,
    ) -> str:
        """Estimate audience reach

            Args:
                account_id: Zernio social account ID on the target ad platform (the estimate runs against its platform). (required)
                ad_account_id: Required. The platform ad-account ID the reach call runs against (Meta act_..., LinkedIn numeric sponsoredAccount ID, Pinterest ad-account ID, X account ID) - every backing reach API is scoped to one ad account. Get it from GET /v1/ads/accounts. (required)
                spec: The targeting spec to estimate. Same shape used by POST /v1/ads/create. (required)
                optimization_goal: Optional. The optimization goal the estimate should assume (platform's
        own vocabulary, e.g. Meta `REACH`, `LINK_CLICKS`, `OFFSITE_CONVERSIONS`).
        Some platforms vary the estimate by goal; omit to use the platform default."""
        client = _get_client()
        try:
            response = client.ad_targeting.estimate_ad_reach(
                account_id=account_id,
                ad_account_id=ad_account_id,
                spec=spec,
                optimization_goal=optimization_goal,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Suggested bid and budget bounds",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_targeting_get_linked_in_bid_pricing(
        account_id: str,
        ad_account_id: str,
        spec: dict[str, Any] | None,
        campaign_type: str | None = None,
        bid_type: str | None = None,
        match_type: str | None = None,
        currency: str | None = None,
        objective_type: str | None = None,
        optimization_target_type: str | None = None,
        daily_budget: float | None = None,
    ) -> str:
        """Suggested bid and budget bounds

        Args:
            account_id: Zernio social account ID (LinkedIn). (required)
            ad_account_id: LinkedIn ad account ID (numeric). (required)
            spec: Same targeting spec used by POST /v1/ads/create. (required)
            campaign_type: Defaults to SPONSORED_UPDATES.
            bid_type: Defaults to CPM.
            match_type: Defaults to EXACT.
            currency: ISO 4217, defaults to USD.
            objective_type: LinkedIn objectiveType, e.g. WEBSITE_VISIT, LEAD_GENERATION, VIDEO_VIEW.
            optimization_target_type: LinkedIn optimizationTargetType, e.g. MAX_CLICK, MAX_IMPRESSION.
            daily_budget: Optional daily budget in whole account-currency units. LinkedIn refines the suggested bid to this budget."""
        client = _get_client()
        try:
            response = client.ad_targeting.get_linked_in_bid_pricing(
                account_id=account_id,
                ad_account_id=ad_account_id,
                spec=spec,
                campaign_type=campaign_type,
                bid_type=bid_type,
                match_type=match_type,
                currency=currency,
                objective_type=objective_type,
                optimization_target_type=optimization_target_type,
                daily_budget=daily_budget,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Impressions, clicks and spend forecast",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_targeting_get_linked_in_supply_forecast(
        account_id: str,
        ad_account_id: str,
        spec: dict[str, Any] | None,
        time_range_start: int,
        time_range_end: int,
        campaign_type: str | None = None,
        objective_type: str | None = None,
        optimization_target: str | None = None,
        daily_budget: float | None = None,
        total_budget: float | None = None,
        currency: str | None = None,
        competing_bid: dict[str, Any] | None = None,
        enable_audience_network: bool | None = None,
        enable_audience_expansion: bool | None = None,
        connected_television_only: bool | None = None,
    ) -> str:
        """Impressions, clicks and spend forecast

        Args:
            account_id: (required)
            ad_account_id: (required)
            spec: (required)
            campaign_type: Defaults to SPONSORED_UPDATES.
            time_range_start: Unix ms. Must be in the future. (required)
            time_range_end: Unix ms. Must be after start and within LinkedIn's max horizon. (required)
            objective_type
            optimization_target: When set, the forecast assumes auto-bidding. When unset, competingBid is required.
            daily_budget: Either dailyBudget or totalBudget is required.
            total_budget
            currency: ISO 4217, defaults to USD.
            competing_bid: Required for manual-bid forecasts (when optimizationTarget is not set).
            enable_audience_network: Defaults to false. Required true for connectedTelevisionOnly.
            enable_audience_expansion: Defaults to false.
            connected_television_only: Defaults to false."""
        client = _get_client()
        try:
            response = client.ad_targeting.get_linked_in_supply_forecast(
                account_id=account_id,
                ad_account_id=ad_account_id,
                spec=spec,
                campaign_type=campaign_type,
                time_range_start=time_range_start,
                time_range_end=time_range_end,
                objective_type=objective_type,
                optimization_target=optimization_target,
                daily_budget=daily_budget,
                total_budget=total_budget,
                currency=currency,
                competing_bid=competing_bid,
                enable_audience_network=enable_audience_network,
                enable_audience_expansion=enable_audience_expansion,
                connected_television_only=connected_television_only,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # ANALYTICS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get post analytics",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_analytics(
        post_id: str | None = None,
        platform: str | None = None,
        profile_id: str | None = None,
        account_id: str | None = None,
        source: str = "all",
        from_date: str | None = None,
        to_date: str | None = None,
        limit: int = 50,
        page: int = 1,
        sort_by: str = "date",
        order: str = "desc",
    ) -> str:
        """Get post analytics

        Args:
            post_id: Returns analytics for a single post. Accepts both Zernio Post IDs and External Post IDs. Zernio IDs are auto-resolved to External Post analytics.
            platform: Filter by platform (default "all")
            profile_id: Filter by profile ID (default "all")
            account_id: Filter by social account ID
            source: Filter by post source: late (posted via Zernio API), external (synced from platform), all (default)
            from_date: Inclusive lower bound (YYYY-MM-DD). Defaults to 90 days ago if omitted. Max range is 366 days.
            to_date: Inclusive upper bound (YYYY-MM-DD). Defaults to today if omitted.
            limit: Page size (default 50)
            page: Page number (default 1)
            sort_by: Sort by date, engagement, or a specific metric
            order: Sort order"""
        client = _get_client()
        try:
            response = client.analytics.get_analytics(
                post_id=post_id,
                platform=platform,
                profile_id=profile_id,
                account_id=account_id,
                source=source,
                from_date=from_date,
                to_date=to_date,
                limit=limit,
                page=page,
                sort_by=sort_by,
                order=order,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get YouTube channel insights",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_you_tube_channel_insights(
        account_id: str,
        metrics: str | None = None,
        since: str | None = None,
        until: str | None = None,
        metric_type: str = "total_value",
    ) -> str:
        """Get YouTube channel insights

            Args:
                account_id: The Zernio SocialAccount ID for the YouTube account. (required)
                metrics: Comma-separated list. Defaults to "views,estimatedMinutesWatched,subscribersGained,subscribersLost".

        Live YouTube Analytics v2 metrics:
          - views
          - estimatedMinutesWatched
          - averageViewDuration          (ratio - weighted mean computed across days)
          - subscribersGained
          - subscribersLost

        Zernio-synthesized from daily follower snapshots (cross-platform parity):
          - followers_gained
          - followers_lost
                since: Start date (YYYY-MM-DD). Defaults to 30 days ago.
                until: End date (YYYY-MM-DD). Defaults to today. YouTube Analytics has a 2-3 day delay,
        so the fetch is internally clamped to 3 days ago; any requested range extending
        beyond that returns zero values for the tail days. The response's dateRange.until
        field reflects your requested value.
                metric_type: "total_value" (default) returns aggregated totals.
        "time_series" returns per-day values in the "values" array."""
        client = _get_client()
        try:
            response = client.analytics.get_you_tube_channel_insights(
                account_id=account_id,
                metrics=metrics,
                since=since,
                until=until,
                metric_type=metric_type,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get LinkedIn org analytics",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_linked_in_org_aggregate_analytics(
        account_id: str,
        metrics: str | None = None,
        since: str | None = None,
        until: str | None = None,
        metric_type: str = "total_value",
    ) -> str:
        """Get LinkedIn org analytics

            Args:
                account_id: The Zernio SocialAccount ID for the LinkedIn organization account. (required)
                metrics: Comma-separated list. Defaults to
        "impressions,clicks,engagement_rate,organic_followers_gained,followers_gained,followers_lost".

        Share statistics (support both total_value and time_series):
          - impressions
          - unique_impressions
          - clicks
          - likes
          - comments
          - shares
          - engagement_rate       (0..1, LinkedIn-computed)

        Follower-gain statistics (support total_value and time_series):
          - organic_followers_gained   (per-day organic gains for time_series; sum of organic gains over the range for total_value)
          - paid_followers_gained      (per-day paid gains for time_series; sum of paid gains over the range for total_value)

        Page-view statistics (total_value ONLY - LinkedIn platform limit):
          - page_views_total
          - page_views_overview
          - page_views_careers
          - page_views_jobs
          - page_views_life

        Zernio-synthesized from daily follower snapshots:
          - followers_gained
          - followers_lost
                since: Start date (YYYY-MM-DD). Defaults to 30 days ago.
                until: End date (YYYY-MM-DD). Defaults to today.
                metric_type"""
        client = _get_client()
        try:
            response = client.analytics.get_linked_in_org_aggregate_analytics(
                account_id=account_id,
                metrics=metrics,
                since=since,
                until=until,
                metric_type=metric_type,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get TikTok account-level insights",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_tik_tok_account_insights(
        account_id: str,
        metrics: str | None = None,
        since: str | None = None,
        until: str | None = None,
        metric_type: str = "total_value",
    ) -> str:
        """Get TikTok account-level insights

            Args:
                account_id: The Zernio SocialAccount ID for the TikTok account. (required)
                metrics: Comma-separated list. Defaults to
        "follower_count,likes_count,video_count,followers_gained,followers_lost".

        Live from /v2/user/info/ (requires user.info.stats scope):
          - follower_count  (cumulative; time series joined from AccountStats)
          - following_count (cumulative; time series joined from AccountStats.metadata)
          - likes_count     (cumulative; time series joined from AccountStats.metadata)
          - video_count     (cumulative; time series joined from AccountStats.metadata)

        Zernio-synthesized:
          - followers_gained  (sum of positive daily follower deltas)
          - followers_lost    (sum of absolute negative daily deltas)
                since: Start date (YYYY-MM-DD). Defaults to 30 days ago.
                until: End date (YYYY-MM-DD). Defaults to today.
                metric_type: "total_value" returns the latest cumulative counter value.
        "time_series" returns daily values joined from AccountStats snapshots."""
        client = _get_client()
        try:
            response = client.analytics.get_tik_tok_account_insights(
                account_id=account_id,
                metrics=metrics,
                since=since,
                until=until,
                metric_type=metric_type,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get YouTube daily views",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_you_tube_daily_views(
        video_id: str,
        account_id: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        """Get YouTube daily views

            Args:
                video_id: The YouTube video ID (e.g., "dQw4w9WgXcQ") (required)
                account_id: The Zernio account ID for the YouTube account (required)
                start_date: Start date (YYYY-MM-DD). Defaults to 30 days ago.
                end_date: End date (YYYY-MM-DD). Defaults to 3 days ago, the newest fully finalized day
        (YouTube finalizes analytics with a ~3-day delay). An explicit endDate is honored
        up to today: days inside the delay window are provisional and may still be revised
        by YouTube (see provisionalSince in the response), and days YouTube has not
        processed yet are omitted from dailyViews."""
        client = _get_client()
        try:
            response = client.analytics.get_you_tube_daily_views(
                video_id=video_id,
                account_id=account_id,
                start_date=start_date,
                end_date=end_date,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get YouTube video retention curve",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_you_tube_video_retention(
        video_id: str,
        account_id: str,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        """Get YouTube video retention curve

            Args:
                video_id: The YouTube video ID (e.g., "dQw4w9WgXcQ") (required)
                account_id: The Zernio account ID for the YouTube account (required)
                start_date: Start date (YYYY-MM-DD). Defaults to the video's publish date (lifetime curve).
                end_date: End date (YYYY-MM-DD). Defaults to 3 days ago, the newest fully finalized day
        (YouTube finalizes analytics with a ~3-day delay). An explicit endDate is honored
        up to today: days inside the delay window are provisional and may still be revised
        by YouTube (see provisionalSince in the response)."""
        client = _get_client()
        try:
            response = client.analytics.get_you_tube_video_retention(
                video_id=video_id,
                account_id=account_id,
                start_date=start_date,
                end_date=end_date,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get Facebook Page insights",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_facebook_page_insights(
        account_id: str,
        metrics: str | None = None,
        since: str | None = None,
        until: str | None = None,
        metric_type: str = "total_value",
    ) -> str:
        """Get Facebook Page insights

            Args:
                account_id: The Zernio SocialAccount ID for the connected Facebook Page. (required)
                metrics: Comma-separated list of metrics. Defaults to
        "page_media_view,page_post_engagements,page_follows,followers_gained,followers_lost".

        Live Meta metrics (current names, post-Nov-2025):
          - page_media_view       (replaces deprecated page_impressions)
          - page_views_total
          - page_post_engagements
          - page_video_views
          - page_video_view_time
          - page_follows          (replaces deprecated page_fans)

        Zernio-synthesized from daily follower snapshots (filling the Nov-2025 gap
        left by the page_fan_adds / page_fan_removes deprecation):
          - followers_gained
          - followers_lost

        Monetization (opt-in, not in the defaults):
          - content_monetization_earnings
          - monetization_approximate_earnings

        Each monetization metric is fetched with its own separate Graph call, so requesting both
        adds two calls. Values are approximate and Meta restates them after the fact.

        content_monetization_earnings returns an object per day and always carries unit
        "micro_amount" plus an ISO 4217 "currency". monetization_approximate_earnings returns a bare
        number per day, so its unit is always "unspecified" and its "currency" is always null. The two
        are on different scales and are not comparable to each other. Both keep their daily "values"
        on every metricType and are never rescaled by Zernio.

        Earnings here are Page-level daily buckets and "total" is their sum. Meta does not
        document whether a bucket carries that day's earnings or a running total, and every
        Page measured so far earned exactly 0, so reconcile "total" against the Page's own Meta
        export before relying on it; the daily "values" are always returned for that purpose.
        Per-post lifetime earnings are served by GET /v1/analytics/facebook/post-earnings.

        A Page that is not enrolled in monetization, or that earned nothing, returns normal daily
        buckets of 0 in "metrics": Meta does not distinguish the two, so a 0 total here does NOT mean
        the Page is enrolled. "unavailableMetrics" covers the narrower case where Meta returned no
        bucket for the metric at all ("no_data") or rejected the request outright, and the metric is
        then omitted from "metrics" rather than reported as 0.
                since: Start date (YYYY-MM-DD). Defaults to 30 days ago.
                until: End date (YYYY-MM-DD). Defaults to today.
                metric_type: "total_value" (default) returns aggregated totals only.
        "time_series" returns daily values in the "values" array."""
        client = _get_client()
        try:
            response = client.analytics.get_facebook_page_insights(
                account_id=account_id,
                metrics=metrics,
                since=since,
                until=until,
                metric_type=metric_type,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get Facebook post monetization earnings",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_facebook_post_earnings(
        account_id: str, post_id: str, metrics: str | None = None
    ) -> str:
        """Get Facebook post monetization earnings

            Args:
                account_id: The Zernio SocialAccount ID for the connected Facebook Page. (required)
                post_id: The platform post ID, exactly as returned in platformAnalytics[].platformPostId by
        /v1/analytics: "{pageId}_{postId}", or the bare video ID for Reels.
         (required)
                metrics: Comma-separated list of monetization metrics. Defaults to both:
          - content_monetization_earnings
          - monetization_approximate_earnings

        content_monetization_earnings always carries unit "micro_amount" plus an ISO 4217
        "currency". monetization_approximate_earnings is always a bare number, so its unit is
        "unspecified" and its "currency" is null. The two are on different scales and are not
        comparable to each other. Any other metric name is rejected with 400."""
        client = _get_client()
        try:
            response = client.analytics.get_facebook_post_earnings(
                account_id=account_id, post_id=post_id, metrics=metrics
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get Instagram insights",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_instagram_account_insights(
        account_id: str,
        metrics: str | None = None,
        since: str | None = None,
        until: str | None = None,
        metric_type: str = "total_value",
        breakdown: str | None = None,
    ) -> str:
        """Get Instagram insights

            Args:
                account_id: The Zernio SocialAccount ID for the Instagram account (required)
                metrics: Comma-separated list of metrics. Defaults to "reach,views,accounts_engaged,total_interactions".
        Valid metrics: reach, views, accounts_engaged, total_interactions, comments, likes, saves, shares,
        replies, reposts, follows_and_unfollows, profile_links_taps.
        Note: only "reach" supports metricType=time_series. All other metrics (including
        follows_and_unfollows) are total_value only. This is an Instagram Graph API limitation,
        not a Zernio limitation - the IG API does not return time-series data for these metrics.
        For a daily running follower count, use /v1/analytics/instagram/follower-history instead.
                since: Start date (YYYY-MM-DD). Defaults to 30 days ago.
                until: End date (YYYY-MM-DD). Defaults to today.
                metric_type: "total_value" (default) returns aggregated totals and supports breakdowns.
        "time_series" returns daily values but only works with the "reach" metric.
                breakdown: Breakdown dimension (only valid with metricType=total_value).
        Valid values depend on the metric: media_product_type, follow_type, follower_type, contact_button_type."""
        client = _get_client()
        try:
            response = client.analytics.get_instagram_account_insights(
                account_id=account_id,
                metrics=metrics,
                since=since,
                until=until,
                metric_type=metric_type,
                breakdown=breakdown,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get Instagram follower history",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_instagram_follower_history(
        account_id: str,
        metrics: str | None = None,
        since: str | None = None,
        until: str | None = None,
        metric_type: str = "total_value",
    ) -> str:
        """Get Instagram follower history

            Args:
                account_id: The Zernio SocialAccount ID for the Instagram account. (required)
                metrics: Comma-separated list. Defaults to "follower_count,followers_gained,followers_lost".
          - follower_count   : per-day raw follower count
          - followers_gained : sum of positive daily deltas
          - followers_lost   : sum of absolute negative daily deltas
                since: Start date (YYYY-MM-DD). Defaults to 30 days ago.
                until: End date (YYYY-MM-DD). Defaults to today.
                metric_type: "total_value" returns aggregated totals (latest for follower_count, sum for gained/lost).
        "time_series" returns per-day values in the "values" array."""
        client = _get_client()
        try:
            response = client.analytics.get_instagram_follower_history(
                account_id=account_id,
                metrics=metrics,
                since=since,
                until=until,
                metric_type=metric_type,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get Instagram demographics",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_instagram_demographics(
        account_id: str,
        metric: str = "follower_demographics",
        breakdown: str | None = None,
        timeframe: str = "this_month",
    ) -> str:
        """Get Instagram demographics

            Args:
                account_id: The Zernio SocialAccount ID for the Instagram account (required)
                metric: "follower_demographics" for follower audience data, or "engaged_audience_demographics" for engaged viewers.
                breakdown: Comma-separated list of demographic dimensions: age, city, country, gender.
        Defaults to all four if omitted.
                timeframe: Time period for demographic data. Defaults to "this_month"."""
        client = _get_client()
        try:
            response = client.analytics.get_instagram_demographics(
                account_id=account_id,
                metric=metric,
                breakdown=breakdown,
                timeframe=timeframe,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get YouTube demographics",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_you_tube_demographics(
        account_id: str,
        video_id: str | None = None,
        breakdown: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        """Get YouTube demographics

            Args:
                account_id: The Zernio SocialAccount ID for the YouTube account (required)
                video_id: YouTube video ID. When provided, demographics are scoped to this single video
        (must belong to the connected channel; otherwise 404 video_not_found).
                breakdown: Comma-separated list of demographic dimensions: age, gender, country.
        Defaults to all three if omitted.
                start_date: Start date in YYYY-MM-DD format. Defaults to 90 days ago, or to the video's
        publish date (lifetime) when videoId is provided.
                end_date: End date (YYYY-MM-DD). Defaults to 3 days ago, the newest fully finalized day
        (YouTube finalizes analytics with a ~3-day delay). An explicit endDate is honored
        up to today: days inside the delay window are provisional and may still be revised
        by YouTube (see provisionalSince in the response)."""
        client = _get_client()
        try:
            response = client.analytics.get_you_tube_demographics(
                account_id=account_id,
                video_id=video_id,
                breakdown=breakdown,
                start_date=start_date,
                end_date=end_date,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get daily aggregated metrics",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_daily_metrics(
        platform: str | None = None,
        profile_id: str | None = None,
        account_id: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        source: str = "all",
        attribution: str = "publish",
    ) -> str:
        """Get daily aggregated metrics

            Args:
                platform: Filter by platform (e.g. "instagram", "tiktok"). Omit for all platforms.
                profile_id: Filter by profile ID. Omit for all profiles.
                account_id: Filter by social account ID
                from_date: Inclusive start date (ISO 8601). Defaults to 180 days ago.
                to_date: Inclusive end date (ISO 8601). Defaults to now.
                source: Filter by post origin. "late" for posts published via Zernio, "external" for posts imported from platforms.
                attribution: How each post's engagement is attributed to a day.
        "publish" (default) sums each post's lifetime total on its publish date.
        "received" buckets the per-day increase in engagement by the day it actually arrived (engagement-over-time), so engagement on older posts appears on the day it was gained rather than the post's publish date."""
        client = _get_client()
        try:
            response = client.analytics.get_daily_metrics(
                platform=platform,
                profile_id=profile_id,
                account_id=account_id,
                from_date=from_date,
                to_date=to_date,
                source=source,
                attribution=attribution,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get best times to post",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_best_time_to_post(
        platform: str | None = None,
        profile_id: str | None = None,
        account_id: str | None = None,
        source: str = "all",
    ) -> str:
        """Get best times to post

        Args:
            platform: Filter by platform (e.g. "instagram", "tiktok"). Omit for all platforms.
            profile_id: Filter by profile ID. Omit for all profiles.
            account_id: Filter by social account ID. Omit for all accounts.
            source: Filter by post origin. "late" for posts published via Zernio, "external" for posts imported from platforms."""
        client = _get_client()
        try:
            response = client.analytics.get_best_time_to_post(
                platform=platform,
                profile_id=profile_id,
                account_id=account_id,
                source=source,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get content performance decay",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_content_decay(
        platform: str | None = None,
        profile_id: str | None = None,
        account_id: str | None = None,
        source: str = "all",
    ) -> str:
        """Get content performance decay

        Args:
            platform: Filter by platform (e.g. "instagram", "tiktok"). Omit for all platforms.
            profile_id: Filter by profile ID. Omit for all profiles.
            account_id: Filter by social account ID. Omit for all accounts.
            source: Filter by post origin. "late" for posts published via Zernio, "external" for posts imported from platforms."""
        client = _get_client()
        try:
            response = client.analytics.get_content_decay(
                platform=platform,
                profile_id=profile_id,
                account_id=account_id,
                source=source,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get frequency vs engagement",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_posting_frequency(
        platform: str | None = None,
        profile_id: str | None = None,
        account_id: str | None = None,
        source: str = "all",
    ) -> str:
        """Get frequency vs engagement

        Args:
            platform: Filter by platform (e.g. "instagram", "tiktok"). Omit for all platforms.
            profile_id: Filter by profile ID. Omit for all profiles.
            account_id: Filter by social account ID. Omit for all accounts.
            source: Filter by post origin. "late" for posts published via Zernio, "external" for posts imported from platforms."""
        client = _get_client()
        try:
            response = client.analytics.get_posting_frequency(
                platform=platform,
                profile_id=profile_id,
                account_id=account_id,
                source=source,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get post analytics timeline",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_post_timeline(
        post_id: str, from_date: str | None = None, to_date: str | None = None
    ) -> str:
        """Get post analytics timeline

           Args:
               post_id: The post to fetch timeline for. Accepts an ExternalPost ID, a platformPostId, or a Zernio Post ID.
        (required)
               from_date: Start of date range (ISO 8601). Defaults to 90 days ago.
               to_date: End of date range (ISO 8601). Defaults to now."""
        client = _get_client()
        try:
            response = client.analytics.get_post_timeline(
                post_id=post_id, from_date=from_date, to_date=to_date
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get GBP performance metrics",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_google_business_performance(
        account_id: str,
        metrics: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        """Get GBP performance metrics

            Args:
                account_id: The Zernio SocialAccount ID for the Google Business Profile account. (required)
                metrics: Comma-separated metric names. Defaults to all available metrics.
        Valid values: BUSINESS_IMPRESSIONS_DESKTOP_MAPS, BUSINESS_IMPRESSIONS_DESKTOP_SEARCH,
        BUSINESS_IMPRESSIONS_MOBILE_MAPS, BUSINESS_IMPRESSIONS_MOBILE_SEARCH,
        BUSINESS_CONVERSATIONS, BUSINESS_DIRECTION_REQUESTS, CALL_CLICKS, WEBSITE_CLICKS,
        BUSINESS_BOOKINGS, BUSINESS_FOOD_ORDERS, BUSINESS_FOOD_MENU_CLICKS
                start_date: Start date (YYYY-MM-DD). Defaults to 30 days ago. Max 18 months back.
                end_date: End date (YYYY-MM-DD). Defaults to today."""
        client = _get_client()
        try:
            response = client.analytics.get_google_business_performance(
                account_id=account_id,
                metrics=metrics,
                start_date=start_date,
                end_date=end_date,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get GBP search keywords",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_google_business_search_keywords(
        account_id: str, start_month: str | None = None, end_month: str | None = None
    ) -> str:
        """Get GBP search keywords

        Args:
            account_id: The Zernio SocialAccount ID for the Google Business Profile account. (required)
            start_month: Start month (YYYY-MM). Defaults to 3 months ago.
            end_month: End month (YYYY-MM). Defaults to current month."""
        client = _get_client()
        try:
            response = client.analytics.get_google_business_search_keywords(
                account_id=account_id, start_month=start_month, end_month=end_month
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Sync an external post",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def analytics_sync_external_posts(
        account_id: str, url: str | None = None, post_id: str | None = None
    ) -> str:
        """Sync an external post

        Args:
            account_id: SocialAccount ID whose posts to sync. Must be connected to Zernio. (required)
            url: The post URL to locate. Optional. Provide `url` or `postId` to return a specific post; omit both to just refresh and return the account's recent posts.
            post_id: The platform post/media/video id to locate, as an alternative to `url`. Optional."""
        client = _get_client()
        try:
            response = client.analytics.sync_external_posts(
                account_id=account_id, url=url, post_id=post_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get LinkedIn aggregate stats",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_linked_in_aggregate_analytics(
        account_id: str,
        aggregation: str = "TOTAL",
        start_date: str | None = None,
        end_date: str | None = None,
        metrics: str | None = None,
    ) -> str:
        """Get LinkedIn aggregate stats

        Args:
            account_id: The ID of the LinkedIn personal account (required)
            aggregation: TOTAL (default, lifetime totals) or DAILY (time series). MEMBERS_REACHED not available with DAILY.
            start_date: Start date (YYYY-MM-DD). If omitted, returns lifetime analytics.
            end_date: End date (YYYY-MM-DD, exclusive). Defaults to today if omitted.
            metrics: Comma-separated metrics: IMPRESSION, MEMBERS_REACHED, REACTION, COMMENT, RESHARE, POST_SAVE, POST_SEND. Omit for all."""
        client = _get_client()
        try:
            response = client.analytics.get_linked_in_aggregate_analytics(
                account_id=account_id,
                aggregation=aggregation,
                start_date=start_date,
                end_date=end_date,
                metrics=metrics,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get LinkedIn post stats",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_linked_in_post_analytics(account_id: str, urn: str) -> str:
        """Get LinkedIn post stats

        Args:
            account_id: The ID of the LinkedIn account (required)
            urn: The LinkedIn post URN (required)"""
        client = _get_client()
        try:
            response = client.analytics.get_linked_in_post_analytics(
                account_id=account_id, urn=urn
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get LinkedIn post reactions",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_linked_in_post_reactions(
        account_id: str, urn: str, limit: int = 25, cursor: int = 0
    ) -> str:
        """Get LinkedIn post reactions

        Args:
            account_id: The ID of the LinkedIn organization account (required)
            urn: The LinkedIn post URN (required)
            limit: Maximum number of reactions to return per page
            cursor: Offset-based pagination start index"""
        client = _get_client()
        try:
            response = client.analytics.get_linked_in_post_reactions(
                account_id=account_id, urn=urn, limit=limit, cursor=cursor
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get Facebook post reactions",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def analytics_get_facebook_post_reactions(account_id: str, post_id: str) -> str:
        """Get Facebook post reactions

        Args:
            account_id: The ID of the Facebook Page account (required)
            post_id: The Facebook post ID (required)"""
        client = _get_client()
        try:
            response = client.analytics.get_facebook_post_reactions(
                account_id=account_id, post_id=post_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # API_KEYS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Verify credential",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def api_keys_verify_credential() -> str:
        """Verify credential"""
        client = _get_client()
        try:
            response = client.api_keys.verify_credential()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List keys",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def api_keys_list_api_keys() -> str:
        """List keys"""
        client = _get_client()
        try:
            response = client.api_keys.list_api_keys()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create key",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def api_keys_create_api_key(
        name: str,
        expires_in: int | None = None,
        scope: str = "full",
        profile_ids: list[str] | None = None,
        permission: str = "read-write",
        disabled_resource_groups: list[str] | None = None,
    ) -> str:
        """Create key

        Args:
            name: (required)
            expires_in: Days until expiry
            scope: 'full' grants access to all profiles (default), 'profiles' restricts to specific profiles
            profile_ids: Profile IDs this key can access. Required when scope is 'profiles'.
            permission: 'read-write' allows all operations (default), 'read' restricts to GET requests only
            disabled_resource_groups: Resource groups to DISABLE on this key (opt-out denylist). Omit for a legacy full-access key. A key with any group disabled mints with the zrk_ prefix, gets 403 with code=insufficient_permissions and required_group on operations in disabled groups (each operation's group is published as x-resource-group), and can never manage API keys, invites, or member identity. With 'messages' disabled, the key cannot read or send private messages through any API surface and cannot create or edit a webhook subscription broader than itself. Subscriptions that already exist are governed by their own `disabledResourceGroups`, not by this key's. OAuth connector tokens resolve against the same registry, but their groups are not settable yet."""
        client = _get_client()
        try:
            response = client.api_keys.create_api_key(
                name=name,
                expires_in=expires_in,
                scope=scope,
                profile_ids=profile_ids,
                permission=permission,
                disabled_resource_groups=disabled_resource_groups,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete key",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def api_keys_delete_api_key(key_id: str) -> str:
        """Delete key

        Args:
            key_id: (required)"""
        client = _get_client()
        try:
            response = client.api_keys.delete_api_key(key_id=key_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # BROADCASTS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List broadcasts",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def broadcasts_list_broadcasts(
        profile_id: str | None = None,
        status: str | None = None,
        platform: str | None = None,
        limit: int = 50,
        skip: int = 0,
    ) -> str:
        """List broadcasts

        Args:
            profile_id: Filter by profile. Omit to list across all profiles
            status
            platform
            limit
            skip"""
        client = _get_client()
        try:
            response = client.broadcasts.list_broadcasts(
                profile_id=profile_id,
                status=status,
                platform=platform,
                limit=limit,
                skip=skip,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create broadcast draft",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def broadcasts_create_broadcast(
        profile_id: str,
        account_id: str,
        platform: str,
        name: str,
        description: str | None = None,
        message: dict[str, Any] | None = None,
        template: dict[str, Any] | None = None,
        segment_filters: dict[str, Any] | None = None,
    ) -> str:
        """Create broadcast draft

        Args:
            profile_id: (required)
            account_id: (required)
            platform: (required)
            name: (required)
            description
            message
            template: WhatsApp template (required when platform is whatsapp)
            segment_filters"""
        client = _get_client()
        try:
            response = client.broadcasts.create_broadcast(
                profile_id=profile_id,
                account_id=account_id,
                platform=platform,
                name=name,
                description=description,
                message=message,
                template=template,
                segment_filters=segment_filters,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get broadcast details",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def broadcasts_get_broadcast(broadcast_id: str) -> str:
        """Get broadcast details

        Args:
            broadcast_id: (required)"""
        client = _get_client()
        try:
            response = client.broadcasts.get_broadcast(broadcast_id=broadcast_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update broadcast",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def broadcasts_update_broadcast(
        broadcast_id: str,
        name: str | None = None,
        description: str | None = None,
        message: dict[str, Any] | None = None,
        template: dict[str, Any] | None = None,
        segment_filters: dict[str, Any] | None = None,
    ) -> str:
        """Update broadcast

        Args:
            broadcast_id: (required)
            name
            description
            message: Generic message payload (used for non-WhatsApp platforms).
            template: WhatsApp template payload (used when platform is `whatsapp`).
            segment_filters: Recipient segment filters (tags, channels, subscription state)."""
        client = _get_client()
        try:
            response = client.broadcasts.update_broadcast(
                broadcast_id=broadcast_id,
                name=name,
                description=description,
                message=message,
                template=template,
                segment_filters=segment_filters,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete broadcast",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def broadcasts_delete_broadcast(broadcast_id: str) -> str:
        """Delete broadcast

        Args:
            broadcast_id: (required)"""
        client = _get_client()
        try:
            response = client.broadcasts.delete_broadcast(broadcast_id=broadcast_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Send broadcast now",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def broadcasts_send_broadcast(broadcast_id: str) -> str:
        """Send broadcast now

        Args:
            broadcast_id: (required)"""
        client = _get_client()
        try:
            response = client.broadcasts.send_broadcast(broadcast_id=broadcast_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Schedule broadcast for later",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def broadcasts_schedule_broadcast(broadcast_id: str, scheduled_at: str) -> str:
        """Schedule broadcast for later

        Args:
            broadcast_id: (required)
            scheduled_at: (required)"""
        client = _get_client()
        try:
            response = client.broadcasts.schedule_broadcast(
                broadcast_id=broadcast_id, scheduled_at=scheduled_at
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Cancel broadcast",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def broadcasts_cancel_broadcast(broadcast_id: str) -> str:
        """Cancel broadcast

        Args:
            broadcast_id: (required)"""
        client = _get_client()
        try:
            response = client.broadcasts.cancel_broadcast(broadcast_id=broadcast_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List broadcast recipients",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def broadcasts_list_broadcast_recipients(
        broadcast_id: str, status: str | None = None, limit: int = 50, skip: int = 0
    ) -> str:
        """List broadcast recipients

        Args:
            broadcast_id: (required)
            status
            limit
            skip"""
        client = _get_client()
        try:
            response = client.broadcasts.list_broadcast_recipients(
                broadcast_id=broadcast_id, status=status, limit=limit, skip=skip
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Add recipients to a broadcast",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def broadcasts_add_broadcast_recipients(
        broadcast_id: str,
        contact_ids: list[str] | None = None,
        phones: list[str] | None = None,
        use_segment: bool | None = None,
    ) -> str:
        """Add recipients to a broadcast

        Args:
            broadcast_id: (required)
            contact_ids: Specific contact IDs to add
            phones: Raw phone numbers (auto-creates contacts). Useful for WhatsApp/Telegram manual entry
            use_segment: Auto-populate from broadcast segment filters"""
        client = _get_client()
        try:
            response = client.broadcasts.add_broadcast_recipients(
                broadcast_id=broadcast_id,
                contact_ids=contact_ids,
                phones=phones,
                use_segment=use_segment,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # CALLS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List all calls (unified history)",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def calls_list_calls(
        channel: str | None = None,
        status: str | None = None,
        direction: str | None = None,
        number: str | None = None,
        search: str | None = None,
        before: str | None = None,
        limit: int = 50,
    ) -> str:
        """List all calls (unified history)

        Args:
            channel
            status
            direction
            number: Exact filter: calls involving this number (typically one of YOUR numbers, to scope history to a single line). E.164, leading + optional.
            search: Free-text match on the from/to numbers. Non-digits are stripped, so partial queries like `302` or `+1 302` work.
            before: Return calls with startedAt strictly before this instant (use the previous page's nextCursor).
            limit"""
        client = _get_client()
        try:
            response = client.calls.list_calls(
                channel=channel,
                status=status,
                direction=direction,
                number=number,
                search=search,
                before=before,
                limit=limit,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a call (any channel)",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def calls_get_call(id: str) -> str:
        """Get a call (any channel)

        Args:
            id: (required)"""
        client = _get_client()
        try:
            response = client.calls.get_call(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a call recording",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def calls_get_call_recording(id: str, as_: str | None = None) -> str:
        """Get a call recording

        Args:
            id: (required)
            as_: `json` returns `{ url }` instead of a 302 redirect."""
        client = _get_client()
        try:
            response = client.calls.get_call_recording(id=id, as_=as_)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # COMMENT_AUTOMATIONS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List comment-to-DM automations",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def comment_automations_list_comment_automations(
        profile_id: str | None = None,
    ) -> str:
        """List comment-to-DM automations

        Args:
            profile_id: Filter by profile. Omit to list across all profiles"""
        client = _get_client()
        try:
            response = client.comment_automations.list_comment_automations(
                profile_id=profile_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create comment-to-DM automation",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comment_automations_create_comment_automation(
        profile_id: str,
        account_id: str,
        name: str,
        dm_message: str,
        trigger: str = "comment",
        platform_post_id: str | None = None,
        post_id: str | None = None,
        post_title: str | None = None,
        keywords: list[str] | None = None,
        match_mode: str = "contains",
        exclude_keywords: list[str] | None = None,
        typo_tolerance: bool | None = None,
        buttons: list[dict[str, Any]] | None = None,
        template: dict[str, Any] | None = None,
        comment_reply: str | None = None,
        dm_message_variations: list[str] | None = None,
        comment_reply_variations: list[str] | None = None,
        link_tracking: bool = True,
        click_tag: str | None = None,
        dm_delay_seconds: int | None = None,
        comment_reply_delay_seconds: int | None = None,
        also_match_in_dms: bool = False,
        audience: dict[str, Any] | None = None,
        follow_gate: dict[str, Any] | None = None,
    ) -> str:
        """Create comment-to-DM automation

        Args:
            profile_id: (required)
            account_id: Instagram or Facebook account ID (required)
            trigger: What fires the automation. 'comment' (keyword comment on a post) or 'story_reply' (keyword reply to an Instagram story). For 'story_reply', platformPostId is the story media id (omit for any story).
            platform_post_id: Platform media/post ID (or story media id when trigger=story_reply). Omit for an account-wide (any-post / any-story) automation.
            post_id: Zernio post ID. Required only when also targeting a specific post via platformPostId.
            post_title: Post content snippet for display
            name: Automation label (required)
            keywords: Trigger keywords (empty = any comment triggers)
            match_mode: How a keyword is compared with the comment. 'contains' (default) matches anywhere, even inside another word (keyword 'app' fires on 'happy'). 'word' matches the keyword only as a standalone word. 'exact' requires the whole comment to be exactly the keyword.
            exclude_keywords: Comments containing one of these never trigger the automation, even when a trigger keyword also matches. Compared using the same matchMode.
            typo_tolerance: Only with matchMode=word: also fire on close misspellings of a keyword (one edit for 4-7 character keywords, two from 8 up). Keywords shorter than 4 characters are never fuzzy-matched.
            dm_message: DM text to send to commenter. Max 640 chars when buttons are set, otherwise ~1000. (required)
            buttons: Optional inline DM buttons (1-3). Phone buttons are Facebook-only. Omit or pass [] for a plain-text DM.
            template: Optional product card sent INSTEAD of the plain dmMessage bubble. Mutually exclusive with buttons. dmMessage stays required: it is what gets sent the moment the card is cleared.
            comment_reply: Optional public reply to the comment
            dm_message_variations: Optional alternate DM texts for random rotation. When set, each triggered comment sends one picked at random from [dmMessage, ...dmMessageVariations], so repeat commenters get slightly different DMs (helps avoid identical-message patterns). Up to 5. Buttons are attached to whichever text is picked, not varied.
            comment_reply_variations: Optional alternate public replies, rotated at random alongside commentReply (picked independently of the DM). Up to 5.
            link_tracking: Wrap link buttons in the DM in a tracked redirect so clicks are counted (Link Clicks / CTR). Pass false to send links exactly as written. Defaults to on.
            click_tag: Optional tag applied to a contact when they click a tracked link (requires linkTracking). Lets you segment clickers for broadcasts/sequences.
            dm_delay_seconds: Seconds to wait after the trigger before sending the DM. Omit or send 0 to reply immediately (the default). Max 86400 (24h). The trigger is still matched and deduplicated the moment the comment arrives, so a delay only moves when the response is sent.
            comment_reply_delay_seconds: Seconds to wait before posting the public comment reply. Omit or send 0 to post it right after the DM (the default). The reply never goes out before the DM, so a value below dmDelaySeconds is raised to it. Ignored when trigger=story_reply, which has no public reply.
            also_match_in_dms: Also fire these keywords on a plain inbound DM, so the automation answers people who message the keyword instead of commenting it. Requires at least one keyword (an empty keyword list means 'match anything', which would answer every inbound message) and is rejected on story_reply automations, which already trigger on DMs. Dedup is per door: a contact who already received the DM from their comment can still receive it from a DM.
            audience
            follow_gate"""
        client = _get_client()
        try:
            response = client.comment_automations.create_comment_automation(
                profile_id=profile_id,
                account_id=account_id,
                trigger=trigger,
                platform_post_id=platform_post_id,
                post_id=post_id,
                post_title=post_title,
                name=name,
                keywords=keywords,
                match_mode=match_mode,
                exclude_keywords=exclude_keywords,
                typo_tolerance=typo_tolerance,
                dm_message=dm_message,
                buttons=buttons,
                template=template,
                comment_reply=comment_reply,
                dm_message_variations=dm_message_variations,
                comment_reply_variations=comment_reply_variations,
                link_tracking=link_tracking,
                click_tag=click_tag,
                dm_delay_seconds=dm_delay_seconds,
                comment_reply_delay_seconds=comment_reply_delay_seconds,
                also_match_in_dms=also_match_in_dms,
                audience=audience,
                follow_gate=follow_gate,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get automation details",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def comment_automations_get_comment_automation(automation_id: str) -> str:
        """Get automation details

        Args:
            automation_id: (required)"""
        client = _get_client()
        try:
            response = client.comment_automations.get_comment_automation(
                automation_id=automation_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update automation settings",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comment_automations_update_comment_automation(
        automation_id: str,
        name: str | None = None,
        trigger: str | None = None,
        keywords: list[str] | None = None,
        match_mode: str | None = None,
        exclude_keywords: list[str] | None = None,
        typo_tolerance: bool | None = None,
        dm_message: str | None = None,
        buttons: list[dict[str, Any]] | None = None,
        template: str | None = None,
        comment_reply: str | None = None,
        dm_message_variations: list[str] | None = None,
        comment_reply_variations: list[str] | None = None,
        link_tracking: bool | None = None,
        click_tag: str | None = None,
        also_match_in_dms: bool | None = None,
        dm_delay_seconds: int | None = None,
        comment_reply_delay_seconds: int | None = None,
        audience: dict[str, Any] | None = None,
        follow_gate: dict[str, Any] | None = None,
        is_active: bool | None = None,
    ) -> str:
        """Update automation settings

        Args:
            automation_id: (required)
            name
            trigger: What fires the automation. Changing it detaches the automation from its bound post or story (a post id and a story id are different objects), unless this same request sets a new binding. 'story_reply' is Instagram only.
            keywords
            match_mode: How a keyword is compared with the comment. 'contains' (default) matches anywhere, even inside another word (keyword 'app' fires on 'happy'). 'word' matches the keyword only as a standalone word. 'exact' requires the whole comment to be exactly the keyword.
            exclude_keywords: Comments containing one of these never trigger the automation, even when a trigger keyword also matches. Compared using the same matchMode.
            typo_tolerance: Only with matchMode=word: also fire on close misspellings of a keyword (one edit for 4-7 character keywords, two from 8 up). Keywords shorter than 4 characters are never fuzzy-matched.
            dm_message
            buttons: Inline DM buttons (1-3). Pass [] to clear all buttons.
            template: Product card sent instead of the plain dmMessage bubble. Pass null to clear it and fall back to dmMessage. Mutually exclusive with buttons, including with the buttons already stored on the automation.
            comment_reply
            dm_message_variations: Alternate DM texts for random rotation (see create). Pass [] to clear.
            comment_reply_variations: Alternate public replies for random rotation. Pass [] to clear.
            link_tracking: Wrap link buttons in a tracked redirect to count clicks. Pass false to send links untouched.
            click_tag: Tag applied to a contact when they click a tracked link (requires linkTracking). Empty string clears it.
            also_match_in_dms: Also fire these keywords on a plain inbound DM. Enabling it requires the automation to end up with at least one keyword (this request's keywords if you send them, otherwise the stored ones) and is rejected on story_reply automations.
            dm_delay_seconds: Seconds to wait after the trigger before sending the DM. Send 0 to clear the delay and reply immediately.
            comment_reply_delay_seconds: Seconds to wait before posting the public comment reply. Send 0 to clear it. The reply never goes out before the DM.
            audience
            follow_gate
            is_active"""
        client = _get_client()
        try:
            response = client.comment_automations.update_comment_automation(
                automation_id=automation_id,
                name=name,
                trigger=trigger,
                keywords=keywords,
                match_mode=match_mode,
                exclude_keywords=exclude_keywords,
                typo_tolerance=typo_tolerance,
                dm_message=dm_message,
                buttons=buttons,
                template=template,
                comment_reply=comment_reply,
                dm_message_variations=dm_message_variations,
                comment_reply_variations=comment_reply_variations,
                link_tracking=link_tracking,
                click_tag=click_tag,
                also_match_in_dms=also_match_in_dms,
                dm_delay_seconds=dm_delay_seconds,
                comment_reply_delay_seconds=comment_reply_delay_seconds,
                audience=audience,
                follow_gate=follow_gate,
                is_active=is_active,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete automation",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comment_automations_delete_comment_automation(automation_id: str) -> str:
        """Delete automation

        Args:
            automation_id: (required)"""
        client = _get_client()
        try:
            response = client.comment_automations.delete_comment_automation(
                automation_id=automation_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List automation logs",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def comment_automations_list_comment_automation_logs(
        automation_id: str, status: str | None = None, limit: int = 50, skip: int = 0
    ) -> str:
        """List automation logs

        Args:
            automation_id: (required)
            status: Filter by result status
            limit
            skip"""
        client = _get_client()
        try:
            response = client.comment_automations.list_comment_automation_logs(
                automation_id=automation_id, status=status, limit=limit, skip=skip
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # COMMENTS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List commented posts",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def comments_list_inbox_comments(
        profile_id: str | None = None,
        platform: str | None = None,
        min_comments: int | None = None,
        since: str | None = None,
        sort_by: str = "date",
        sort_order: str = "desc",
        limit: int = 50,
        cursor: str | None = None,
        account_id: str | None = None,
    ) -> str:
        """List commented posts

        Args:
            profile_id: Filter by profile ID
            platform: Filter by platform. `metaads` is a synthetic value meaning the user's ads (boosted/dark posts) only; `facebook`/`instagram` return organic posts only.
            min_comments: Minimum comment count
            since: Posts created after this date
            sort_by: Sort field
            sort_order: Sort order
            limit
            cursor
            account_id: Filter by specific social account ID"""
        client = _get_client()
        try:
            response = client.comments.list_inbox_comments(
                profile_id=profile_id,
                platform=platform,
                min_comments=min_comments,
                since=since,
                sort_by=sort_by,
                sort_order=sort_order,
                limit=limit,
                cursor=cursor,
                account_id=account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get post comments",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def comments_get_inbox_post_comments(
        post_id: str,
        account_id: str,
        subreddit: str | None = None,
        limit: int = 25,
        cursor: str | None = None,
        comment_id: str | None = None,
    ) -> str:
        """Get post comments

        Args:
            post_id: Zernio post ID or platform-specific post ID. Zernio IDs are auto-resolved. LinkedIn third-party posts accept full activity URN or numeric ID. (required)
            account_id: (required)
            subreddit: (Reddit only) Subreddit name
            limit: Maximum number of comments to return
            cursor: Pagination cursor
            comment_id: (Reddit only) Get replies to a specific comment"""
        client = _get_client()
        try:
            response = client.comments.get_inbox_post_comments(
                post_id=post_id,
                account_id=account_id,
                subreddit=subreddit,
                limit=limit,
                cursor=cursor,
                comment_id=comment_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Reply to comment",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comments_reply_to_inbox_post(
        post_id: str,
        account_id: str,
        message: str,
        attachment_url: str | None = None,
        comment_id: str | None = None,
        parent_cid: str | None = None,
        root_uri: str | None = None,
        root_cid: str | None = None,
    ) -> str:
        """Reply to comment

        Args:
            post_id: Zernio post ID or platform-specific post ID. LinkedIn third-party posts accept full activity URN or numeric ID. (required)
            account_id: (required)
            message: (required)
            attachment_url: (Facebook only) URL of an image to attach, publishing a photo comment alongside the text. The URL must be publicly accessible so Meta can fetch it. Returns 400 for other platforms.
            comment_id: Reply to specific comment (optional)
            parent_cid: (Bluesky only) Parent content identifier
            root_uri: (Bluesky only) Root post URI
            root_cid: (Bluesky only) Root post CID"""
        client = _get_client()
        try:
            response = client.comments.reply_to_inbox_post(
                post_id=post_id,
                account_id=account_id,
                message=message,
                attachment_url=attachment_url,
                comment_id=comment_id,
                parent_cid=parent_cid,
                root_uri=root_uri,
                root_cid=root_cid,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete comment",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comments_delete_inbox_comment(
        post_id: str, account_id: str, comment_id: str
    ) -> str:
        """Delete comment

        Args:
            post_id: Zernio post ID or platform-specific post ID. LinkedIn third-party posts accept full activity URN or numeric ID. (required)
            account_id: (required)
            comment_id: (required)"""
        client = _get_client()
        try:
            response = client.comments.delete_inbox_comment(
                post_id=post_id, account_id=account_id, comment_id=comment_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Edit comment",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comments_edit_inbox_comment(
        post_id: str, comment_id: str, account_id: str, platform: str, content: str
    ) -> str:
        """Edit comment

        Args:
            post_id: (required)
            comment_id: (required)
            account_id: The social account ID (required)
            platform: Only Reddit supports editing a comment (required)
            content: The new comment body (required)"""
        client = _get_client()
        try:
            response = client.comments.edit_inbox_comment(
                post_id=post_id,
                comment_id=comment_id,
                account_id=account_id,
                platform=platform,
                content=content,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Set comment moderation status",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comments_set_comment_moderation(
        post_id: str,
        comment_id: str,
        account_id: str,
        platform: str,
        moderation_status: str,
        ban_author: bool | None = None,
    ) -> str:
        """Set comment moderation status

        Args:
            post_id: (required)
            comment_id: (required)
            account_id: The social account ID (required)
            platform: Only YouTube supports comment moderation (required)
            moderation_status: published approves the comment, rejected removes it, heldForReview returns it to the queue. (required)
            ban_author: Also ban the comment's author, auto-rejecting their future comments. Only valid when moderationStatus is "rejected"; any other pairing is a 400."""
        client = _get_client()
        try:
            response = client.comments.set_comment_moderation(
                post_id=post_id,
                comment_id=comment_id,
                account_id=account_id,
                platform=platform,
                moderation_status=moderation_status,
                ban_author=ban_author,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Hide comment",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comments_hide_inbox_comment(
        post_id: str, comment_id: str, account_id: str
    ) -> str:
        """Hide comment

        Args:
            post_id: (required)
            comment_id: (required)
            account_id: The social account ID (required)"""
        client = _get_client()
        try:
            response = client.comments.hide_inbox_comment(
                post_id=post_id, comment_id=comment_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Unhide comment",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comments_unhide_inbox_comment(
        post_id: str, comment_id: str, account_id: str
    ) -> str:
        """Unhide comment

        Args:
            post_id: (required)
            comment_id: (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.comments.unhide_inbox_comment(
                post_id=post_id, comment_id=comment_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Like comment",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comments_like_inbox_comment(
        post_id: str,
        comment_id: str,
        account_id: str,
        reaction_type: str | None = None,
        cid: str | None = None,
    ) -> str:
        """Like comment

        Args:
            post_id: (required)
            comment_id: (required)
            account_id: The social account ID (required)
            reaction_type: (LinkedIn only) Reaction to create. Defaults to LIKE; ignored on other platforms.
            cid: (Bluesky only) Content identifier for the comment"""
        client = _get_client()
        try:
            response = client.comments.like_inbox_comment(
                post_id=post_id,
                comment_id=comment_id,
                account_id=account_id,
                reaction_type=reaction_type,
                cid=cid,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Unlike comment",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comments_unlike_inbox_comment(
        post_id: str, comment_id: str, account_id: str, like_uri: str | None = None
    ) -> str:
        """Unlike comment

        Args:
            post_id: (required)
            comment_id: (required)
            account_id: (required)
            like_uri: (Bluesky only) The like URI returned when liking"""
        client = _get_client()
        try:
            response = client.comments.unlike_inbox_comment(
                post_id=post_id,
                comment_id=comment_id,
                account_id=account_id,
                like_uri=like_uri,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Like post",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comments_like_post(
        post_id: str,
        account_id: str,
        reaction_type: str | None = None,
        cid: str | None = None,
    ) -> str:
        """Like post

        Args:
            post_id: Zernio post ID or the platform's native post ID (required)
            account_id: The social account acting as the liker (required)
            reaction_type: (LinkedIn only) Reaction to create. Defaults to LIKE; ignored on other platforms.
            cid: (Bluesky only) Content identifier of the post"""
        client = _get_client()
        try:
            response = client.comments.like_post(
                post_id=post_id,
                account_id=account_id,
                reaction_type=reaction_type,
                cid=cid,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Unlike post",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comments_unlike_post(
        post_id: str, account_id: str, like_uri: str | None = None
    ) -> str:
        """Unlike post

        Args:
            post_id: Zernio post ID or the platform's native post ID (required)
            account_id: (required)
            like_uri: (Bluesky only) The like URI returned when liking"""
        client = _get_client()
        try:
            response = client.comments.unlike_post(
                post_id=post_id, account_id=account_id, like_uri=like_uri
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Send private reply",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def comments_send_private_reply_to_comment(
        post_id: str,
        comment_id: str,
        account_id: str,
        message: str,
        quick_replies: list[dict[str, Any]] | None = None,
        buttons: list[dict[str, Any]] | None = None,
    ) -> str:
        """Send private reply

            Args:
                post_id: The media/post ID (Instagram media ID or Facebook post ID) (required)
                comment_id: The comment ID to send a private reply to (required)
                account_id: The social account ID (Instagram or Facebook) (required)
                message: The message text to send as a private DM (required)
                quick_replies: Optional quick-reply chips appended to the message. Visible only in the
        Instagram and Messenger apps (not on web). Maximum 13 entries. Mutually
        exclusive with `buttons`. Note: chips do NOT render in the Instagram
        Message Requests folder where DMs from non-followers land — use `buttons`
        instead for cold reach.
                buttons: Optional 1-3 inline buttons rendered as part of the same message bubble
        via Meta's button_template. Visible in the Instagram Message Requests
        folder (unlike quick replies). Mutually exclusive with `quickReplies`."""
        client = _get_client()
        try:
            response = client.comments.send_private_reply_to_comment(
                post_id=post_id,
                comment_id=comment_id,
                account_id=account_id,
                message=message,
                quick_replies=quick_replies,
                buttons=buttons,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # CONNECT

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get OAuth connect URL",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_get_connect_url(
        platform: str,
        profile_id: str,
        redirect_url: str | None = None,
        headless: bool = False,
        login_method: str = "instagram_login",
    ) -> str:
        """Get OAuth connect URL

            Args:
                platform: Social media platform to connect (required)
                profile_id: Your Zernio profile ID (get from /v1/profiles). For WhatsApp, a Zernio-provisioned number can only be connected on the profile it was provisioned to; connecting from any other profile is rejected with a 409. (required)
                redirect_url: Your custom redirect URL after connection completes. Accepts an http(s) URL, a custom app scheme for mobile deeplinks (e.g. myapp://callback), or a relative path. Result params are appended with the URL API, so an existing query string is preserved. Standard mode appends connected={platform}&profileId=X&accountId=Y&username=Z. Headless mode appends OAuth data params for platforms requiring selection (e.g. LinkedIn orgs, Facebook pages). If no selection is needed, the account is created directly and the redirect includes accountId.
                headless: When true, the user is redirected to your redirect_url with raw OAuth data (code, state) instead of Zernio's default account selection UI. Use this to build a custom connect experience.
                login_method: Instagram only. Which of the two Instagram connection methods to use. Ignored for every other platform.

        `instagram_login` (the default, and what you get if you omit this): the Instagram Login dialog. The user authorizes their Instagram professional account directly, no Facebook Page required.

        `facebook_login`: the Facebook Login dialog, i.e. "Instagram API with Facebook Login". The user authorizes a Facebook Page that has a linked Instagram professional account, and every API call for that account then runs through the Page. Use this when the customer manages Instagram through a Page and expects the Facebook consent screen. Because the user has to pick which Page to connect, the callback continues at the account-selection step, `/v1/connect/instagram/select-account`.

        `facebook_login` supports `headless=true` like the other selection platforms: the callback redirects to your `redirect_url` with `profileId`, `tempToken`, `platform=instagram`, `step=select_account` and `connect_token`, which you pass into the select-account endpoints to finish. The default `instagram_login` has no selection step, so it connects the account directly."""
        client = _get_client()
        try:
            response = client.connect.get_connect_url(
                platform=platform,
                profile_id=profile_id,
                redirect_url=redirect_url,
                headless=headless,
                login_method=login_method,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Complete OAuth callback",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_handle_o_auth_callback(
        platform: str, code: str, state: str, profile_id: str
    ) -> str:
        """Complete OAuth callback

        Args:
            platform: (required)
            code: (required)
            state: (required)
            profile_id: (required)"""
        client = _get_client()
        try:
            response = client.connect.handle_o_auth_callback(
                platform=platform, code=code, state=state, profile_id=profile_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Connect ads for a platform",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_ads(
        platform: str,
        profile_id: str,
        account_id: str | None = None,
        redirect_url: str | None = None,
        headless: bool = False,
        force: bool = False,
        ad_account_id: str | None = None,
        ad_account_ids: list[str] | None = None,
    ) -> str:
        """Connect ads for a platform

            Args:
                platform: Platform to connect ads for. Only platforms with ads support are accepted. (required)
                profile_id: Your Zernio profile ID (required)
                account_id: Existing SocialAccount ID. Required for `twitter` (X Ads). Optional for `tiktok` —
        omit to enter ads-only mode (no TikTok posting account linked; ad creation uses
        a Brand Identity instead of a TT_USER). Ignored for same-token (`facebook`,
        `instagram`, `linkedin`, `pinterest`) and standalone (`googleads`) platforms.
                redirect_url: Custom redirect URL after OAuth completes (same-token platforms only). Accepts an http(s) URL, a custom app scheme for mobile deeplinks (e.g. myapp://callback), or a relative path.
                headless: Enable headless mode (same-token platforms only)
                force: Force a fresh OAuth even when an account already exists. Normally the
        endpoint returns `alreadyConnected: true` whenever a connected account
        is found, keying off its active state rather than token liveness.
        Set `force=true` to bypass that and always receivean `authUrl`.
        Completing the returned OAuth refreshes the stored token
        on the existing posting and ads accounts in place.
                ad_account_id: Scope ad sync to a single platform ad account. Without this param,
        sync covers every ad account the connected token can see. Supported
        on `facebook`/`instagram` (Meta, `act_<digits>`), `linkedin` (bare
        numeric sponsored-account id), `googleads` (bare customer id digits)
        and `twitter` (X Ads, base36 account id). `tiktok` scopes advertisers
        at OAuth and `pinterest` has no ads discovery, so both ignore it.
        Meta ids are additionally validated against the connected token;
        unreachable IDs return 400. Setting a scope also removes already
        synced ads from de-scoped ad accounts. For multiple accounts use
        `adAccountIds` instead.
                ad_account_ids: Scope ad sync to multiple platform ad accounts (same platform
        support and id shapes as `adAccountId`). Repeat the param
        (`?adAccountIds=act_1&adAccountIds=act_2`) or comma-separate
        (`?adAccountIds=act_1,act_2`). Persisted server-side; latest call
        wins, and de-scoped ad accounts have their synced ads removed.
        Omitting both `adAccountId` and `adAccountIds` keeps any previously
        persisted scope unchanged."""
        client = _get_client()
        try:
            response = client.connect.connect_ads(
                platform=platform,
                profile_id=profile_id,
                account_id=account_id,
                redirect_url=redirect_url,
                headless=headless,
                force=force,
                ad_account_id=ad_account_id,
                ad_account_ids=ad_account_ids,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Set TikTok brand identity",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_configure_tik_tok_ads_brand_identity(
        account_id: str, display_name: str, image_url: str
    ) -> str:
        """Set TikTok brand identity

        Args:
            account_id: SocialAccount ID of the `tiktokads` account. (required)
            display_name: Brand name shown above the ad on TikTok. (required)
            image_url: Public URL of a square brand image (≥98×98 px, JPG/PNG, max 5 MB). Used as the brand avatar on the ad. (required)"""
        client = _get_client()
        try:
            response = client.connect.configure_tik_tok_ads_brand_identity(
                account_id=account_id, display_name=display_name, image_url=image_url
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Facebook pages",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_list_facebook_pages(profile_id: str, temp_token: str) -> str:
        """List Facebook pages

        Args:
            profile_id: Profile ID from your connection flow (required)
            temp_token: Temporary Facebook access token from the OAuth callback redirect (required)"""
        client = _get_client()
        try:
            response = client.connect.list_facebook_pages(
                profile_id=profile_id, temp_token=temp_token
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Select Facebook page",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_select_facebook_page(
        profile_id: str,
        page_id: str,
        temp_token: str,
        user_profile: dict[str, Any] | None,
        redirect_url: str | None = None,
    ) -> str:
        """Select Facebook page

        Args:
            profile_id: Profile ID from your connection flow (required)
            page_id: The Facebook Page ID selected by the user (required)
            temp_token: Temporary Facebook access token from OAuth (required)
            user_profile: Decoded user profile object from the OAuth callback (required)
            redirect_url: Optional custom redirect URL to return to after selection"""
        client = _get_client()
        try:
            response = client.connect.select_facebook_page(
                profile_id=profile_id,
                page_id=page_id,
                temp_token=temp_token,
                user_profile=user_profile,
                redirect_url=redirect_url,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Pages with a linked Instagram account",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_list_instagram_pages(profile_id: str, temp_token: str) -> str:
        """List Pages with a linked Instagram account

        Args:
            profile_id: Profile ID from your connection flow (required)
            temp_token: Long-lived Facebook user access token from the OAuth callback redirect (required)"""
        client = _get_client()
        try:
            response = client.connect.list_instagram_pages(
                profile_id=profile_id, temp_token=temp_token
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Select the Page whose Instagram account to connect",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_select_instagram_account(
        profile_id: str, page_id: str, temp_token: str, redirect_url: str | None = None
    ) -> str:
        """Select the Page whose Instagram account to connect

        Args:
            profile_id: Profile ID from your connection flow (required)
            page_id: The Facebook Page ID selected by the user, from GET /v1/connect/instagram/select-account (required)
            temp_token: Long-lived Facebook user access token from the OAuth callback redirect (required)
            redirect_url: Optional custom redirect URL to return to after selection"""
        client = _get_client()
        try:
            response = client.connect.select_instagram_account(
                profile_id=profile_id,
                page_id=page_id,
                temp_token=temp_token,
                redirect_url=redirect_url,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List GBP locations",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_list_google_business_locations(
        profile_id: str | None = None,
        pending_data_token: str | None = None,
        temp_token: str | None = None,
        search: str | None = None,
        filter: str | None = None,
    ) -> str:
        """List GBP locations

        Args:
            profile_id: Profile ID from your connection flow. Required for auth validation when provided.
            pending_data_token: Token from the OAuth callback redirect. Preferred over tempToken because it preserves server-side token storage. One of pendingDataToken or tempToken is required.
            temp_token: Legacy. Direct Google access token. Use pendingDataToken instead when available.
            search: Free-text search on the business name, applied server-side by Google. Use this for accounts that own many locations (the response is bounded, see hasMore) so the user can find a specific location without loading the full list.
            filter: Raw Google Business Information API filter expression (advanced; takes precedence over search). Supports fields such as title, storeCode, storefront_address.postal_code, labels and categories, e.g. storeCode="LH279411". See Google's "Work with location data" guide."""
        client = _get_client()
        try:
            response = client.connect.list_google_business_locations(
                profile_id=profile_id,
                pending_data_token=pending_data_token,
                temp_token=temp_token,
                search=search,
                filter=filter,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Select GBP location",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_select_google_business_location(
        profile_id: str,
        location_id: str,
        pending_data_token: str,
        account_id: str | None = None,
        redirect_url: str | None = None,
    ) -> str:
        """Select GBP location

        Args:
            profile_id: Profile ID from your connection flow (required)
            location_id: The Google Business location ID selected by the user (required)
            account_id: Optional but recommended. The Google Business Account resource name ("accounts/123") that owns the selected location (returned per-location by GET /v1/connect/googlebusiness/locations). When provided, the location is resolved directly instead of by enumerating the account, which is required for accounts that own many locations. Omit only for small accounts.
            pending_data_token: Token from the OAuth callback redirect (pendingDataToken query param). Tokens and profile data are retrieved server-side from this token. (required)
            redirect_url: Optional custom redirect URL to return to after selection"""
        client = _get_client()
        try:
            response = client.connect.select_google_business_location(
                profile_id=profile_id,
                location_id=location_id,
                account_id=account_id,
                pending_data_token=pending_data_token,
                redirect_url=redirect_url,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get pending OAuth data",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_get_pending_o_auth_data(token: str) -> str:
        """Get pending OAuth data

        Args:
            token: The pending data token from the OAuth redirect URL (pendingDataToken parameter) (required)"""
        client = _get_client()
        try:
            response = client.connect.get_pending_o_auth_data(token=token)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List LinkedIn orgs",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_list_linked_in_organizations(temp_token: str, org_ids: str) -> str:
        """List LinkedIn orgs

        Args:
            temp_token: The temporary LinkedIn access token from the OAuth redirect (required)
            org_ids: Comma-separated list of organization IDs to fetch details for (max 100) (required)"""
        client = _get_client()
        try:
            response = client.connect.list_linked_in_organizations(
                temp_token=temp_token, org_ids=org_ids
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Select LinkedIn org",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_select_linked_in_organization(
        profile_id: str,
        temp_token: str,
        user_profile: dict[str, Any] | None,
        account_type: str,
        selected_organization: dict[str, Any] | None = None,
        redirect_url: str | None = None,
    ) -> str:
        """Select LinkedIn org

        Args:
            profile_id: (required)
            temp_token: (required)
            user_profile: (required)
            account_type: (required)
            selected_organization
            redirect_url"""
        client = _get_client()
        try:
            response = client.connect.select_linked_in_organization(
                profile_id=profile_id,
                temp_token=temp_token,
                user_profile=user_profile,
                account_type=account_type,
                selected_organization=selected_organization,
                redirect_url=redirect_url,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Pinterest boards",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_list_pinterest_boards_for_selection(
        profile_id: str, temp_token: str
    ) -> str:
        """List Pinterest boards

        Args:
            profile_id: Your Zernio profile ID (required)
            temp_token: Temporary Pinterest access token from the OAuth callback redirect (required)"""
        client = _get_client()
        try:
            response = client.connect.list_pinterest_boards_for_selection(
                profile_id=profile_id, temp_token=temp_token
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Select Pinterest board",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_select_pinterest_board(
        profile_id: str,
        board_id: str,
        temp_token: str,
        board_name: str | None = None,
        user_profile: dict[str, Any] | None = None,
        refresh_token: str | None = None,
        expires_in: int | None = None,
        redirect_url: str | None = None,
    ) -> str:
        """Select Pinterest board

        Args:
            profile_id: Your Zernio profile ID (required)
            board_id: The Pinterest Board ID selected by the user (required)
            board_name: The board name (for display purposes)
            temp_token: Temporary Pinterest access token from OAuth (required)
            user_profile: User profile data from OAuth redirect
            refresh_token: Pinterest refresh token (if available)
            expires_in: Token expiration time in seconds
            redirect_url: Custom redirect URL after connection completes"""
        client = _get_client()
        try:
            response = client.connect.select_pinterest_board(
                profile_id=profile_id,
                board_id=board_id,
                board_name=board_name,
                temp_token=temp_token,
                user_profile=user_profile,
                refresh_token=refresh_token,
                expires_in=expires_in,
                redirect_url=redirect_url,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Snapchat profiles",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_list_snapchat_profiles(profile_id: str, temp_token: str) -> str:
        """List Snapchat profiles

        Args:
            profile_id: Your Zernio profile ID (required)
            temp_token: Temporary Snapchat access token from the OAuth callback redirect (required)"""
        client = _get_client()
        try:
            response = client.connect.list_snapchat_profiles(
                profile_id=profile_id, temp_token=temp_token
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Select Snapchat profile",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_select_snapchat_profile(
        profile_id: str,
        selected_public_profile: dict[str, Any] | None,
        temp_token: str,
        user_profile: dict[str, Any] | None,
        refresh_token: str | None = None,
        expires_in: int | None = None,
        redirect_url: str | None = None,
    ) -> str:
        """Select Snapchat profile

        Args:
            profile_id: Your Zernio profile ID (required)
            selected_public_profile: The selected Snapchat Public Profile (required)
            temp_token: Temporary Snapchat access token from OAuth (required)
            user_profile: User profile data from OAuth redirect (required)
            refresh_token: Snapchat refresh token (if available)
            expires_in: Token expiration time in seconds
            redirect_url: Custom redirect URL after connection completes"""
        client = _get_client()
        try:
            response = client.connect.select_snapchat_profile(
                profile_id=profile_id,
                selected_public_profile=selected_public_profile,
                temp_token=temp_token,
                user_profile=user_profile,
                refresh_token=refresh_token,
                expires_in=expires_in,
                redirect_url=redirect_url,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Connect Bluesky account",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_bluesky_credentials(
        identifier: str, app_password: str, state: str, redirect_uri: str | None = None
    ) -> str:
        """Connect Bluesky account

        Args:
            identifier: Your Bluesky handle (e.g. user.bsky.social) or email address (required)
            app_password: App password generated from Bluesky Settings > App Passwords (required)
            state: Required state formatted as {userId}-{profileId}. Get userId from GET /v1/users and profileId from GET /v1/profiles. (required)
            redirect_uri: Optional URL to redirect to after successful connection"""
        client = _get_client()
        try:
            response = client.connect.connect_bluesky_credentials(
                identifier=identifier,
                app_password=app_password,
                state=state,
                redirect_uri=redirect_uri,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Connect an OpenAI Ads account",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_open_ai_ads_credentials(
        api_key: str,
        profile_id: str,
        state: str | None = None,
        redirect_uri: str | None = None,
    ) -> str:
        """Connect an OpenAI Ads account

        Args:
            api_key: API key from ChatGPT Ads Manager (Settings). Grants full read/write access on OpenAI's side; Zernio only ever reads with it. (required)
            profile_id: Your Zernio profile ID (required)
            state: Optional state passthrough for the connect flow.
            redirect_uri: Optional URL to redirect to after successful connection"""
        client = _get_client()
        try:
            response = client.connect.connect_open_ai_ads_credentials(
                api_key=api_key,
                profile_id=profile_id,
                state=state,
                redirect_uri=redirect_uri,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Connect WhatsApp via credentials",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_whats_app_credentials(
        profile_id: str,
        access_token: str,
        waba_id: str,
        phone_number_id: str,
        pin: str | None = None,
    ) -> str:
        """Connect WhatsApp via credentials

        Args:
            profile_id: Your Zernio profile ID (required)
            access_token: Permanent System User access token from Meta Business Suite (required)
            waba_id: WhatsApp Business Account ID from Meta (required)
            phone_number_id: Phone Number ID from Meta WhatsApp Manager (required)
            pin: The 6-digit two-step verification PIN set on the number. Required if you enabled two-step verification for it, otherwise Meta rejects the Cloud API registration with error 133005 and the number cannot send messages."""
        client = _get_client()
        try:
            response = client.connect.connect_whats_app_credentials(
                profile_id=profile_id,
                access_token=access_token,
                waba_id=waba_id,
                phone_number_id=phone_number_id,
                pin=pin,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List numbers for selection",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_list_whats_app_phone_numbers(profile_id: str, temp_token: str) -> str:
        """List numbers for selection

        Args:
            profile_id: The Zernio profile ID from the headless redirect (required)
            temp_token: The temporary access token from the headless redirect (required)"""
        client = _get_client()
        try:
            response = client.connect.list_whats_app_phone_numbers(
                profile_id=profile_id, temp_token=temp_token
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Complete number selection",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_complete_whats_app_phone_selection(
        profile_id: str,
        phone_number_id: str,
        waba_id: str,
        temp_token: str,
        user_profile: dict[str, Any] | None = None,
        redirect_url: str | None = None,
    ) -> str:
        """Complete number selection

        Args:
            profile_id: The Zernio profile ID (required)
            phone_number_id: The selected phone number ID (from listWhatsAppPhoneNumbers) (required)
            waba_id: The WABA ID containing the selected phone (required)
            temp_token: The temporary access token from the headless redirect (required)
            user_profile: Optional user profile data (passthrough)
            redirect_url: Optional URL to receive the post-connection redirect target"""
        client = _get_client()
        try:
            response = client.connect.complete_whats_app_phone_selection(
                profile_id=profile_id,
                phone_number_id=phone_number_id,
                waba_id=waba_id,
                temp_token=temp_token,
                user_profile=user_profile,
                redirect_url=redirect_url,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Generate Telegram code",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_get_telegram_connect_status(profile_id: str) -> str:
        """Generate Telegram code

        Args:
            profile_id: The profile ID to connect the Telegram account to (required)"""
        client = _get_client()
        try:
            response = client.connect.get_telegram_connect_status(profile_id=profile_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Connect Telegram directly",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_initiate_telegram_connect(chat_id: str, profile_id: str) -> str:
        """Connect Telegram directly

        Args:
            chat_id: The Telegram chat ID. Numeric ID (e.g. "-1001234567890") or username with @ prefix (e.g. "@mychannel"). (required)
            profile_id: The profile ID to connect the account to (required)"""
        client = _get_client()
        try:
            response = client.connect.initiate_telegram_connect(
                chat_id=chat_id, profile_id=profile_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Check Telegram status",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_complete_telegram_connect(code: str) -> str:
        """Check Telegram status

        Args:
            code: The access code to check status for (required)"""
        client = _get_client()
        try:
            response = client.connect.complete_telegram_connect(code=code)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Facebook pages",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_get_facebook_pages(account_id: str, refresh: bool | None = None) -> str:
        """List Facebook pages

        Args:
            account_id: (required)
            refresh: When true, bypasses the page cache and fetches fresh pages from Meta. Rate-limited server-side to 1 refresh per 60s. Pages no longer accessible to the connected account will be removed from the list on refresh."""
        client = _get_client()
        try:
            response = client.connect.get_facebook_pages(
                account_id=account_id, refresh=refresh
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update Facebook page",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_update_facebook_page(account_id: str, selected_page_id: str) -> str:
        """Update Facebook page

        Args:
            account_id: (required)
            selected_page_id: (required)"""
        client = _get_client()
        try:
            response = client.connect.update_facebook_page(
                account_id=account_id, selected_page_id=selected_page_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List LinkedIn orgs",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_get_linked_in_organizations(account_id: str) -> str:
        """List LinkedIn orgs

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.connect.get_linked_in_organizations(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Switch LinkedIn account type",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_update_linked_in_organization(
        account_id: str,
        account_type: str,
        selected_organization: dict[str, Any] | None = None,
    ) -> str:
        """Switch LinkedIn account type

        Args:
            account_id: (required)
            account_type: (required)
            selected_organization"""
        client = _get_client()
        try:
            response = client.connect.update_linked_in_organization(
                account_id=account_id,
                account_type=account_type,
                selected_organization=selected_organization,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Pinterest boards",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_get_pinterest_boards(account_id: str) -> str:
        """List Pinterest boards

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.connect.get_pinterest_boards(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Set default Pinterest board",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_update_pinterest_boards(
        account_id: str, default_board_id: str, default_board_name: str | None = None
    ) -> str:
        """Set default Pinterest board

        Args:
            account_id: (required)
            default_board_id: (required)
            default_board_name"""
        client = _get_client()
        try:
            response = client.connect.update_pinterest_boards(
                account_id=account_id,
                default_board_id=default_board_id,
                default_board_name=default_board_name,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create Pinterest board",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_create_pinterest_board(
        account_id: str,
        name: str,
        description: str | None = None,
        privacy: str = "PUBLIC",
    ) -> str:
        """Create Pinterest board

        Args:
            account_id: (required)
            name: Name of the board (required)
            description: Board description
            privacy: Board privacy setting"""
        client = _get_client()
        try:
            response = client.connect.create_pinterest_board(
                account_id=account_id,
                name=name,
                description=description,
                privacy=privacy,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List YouTube playlists",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_get_youtube_playlists(account_id: str) -> str:
        """List YouTube playlists

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.connect.get_youtube_playlists(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Set default YouTube playlist",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_update_youtube_default_playlist(
        account_id: str,
        default_playlist_id: str,
        default_playlist_name: str | None = None,
    ) -> str:
        """Set default YouTube playlist

        Args:
            account_id: (required)
            default_playlist_id: (required)
            default_playlist_name"""
        client = _get_client()
        try:
            response = client.connect.update_youtube_default_playlist(
                account_id=account_id,
                default_playlist_id=default_playlist_id,
                default_playlist_name=default_playlist_name,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List GBP locations",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_get_gmb_locations(
        account_id: str,
        search: str | None = None,
        filter: str | None = None,
        limit: int = 100,
    ) -> str:
        """List GBP locations

        Args:
            account_id: (required)
            search: Free-text search on the business name, applied server-side by Google. Use for accounts with many locations.
            filter: Raw Google Business Information API filter expression (advanced; takes precedence over search), e.g. storeCode="LH279411".
            limit: Max locations to return (default 100, max 500). Raise it to enumerate an account with more than 100 locations; for accounts with thousands, use search/filter instead."""
        client = _get_client()
        try:
            response = client.connect.get_gmb_locations(
                account_id=account_id, search=search, filter=filter, limit=limit
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update GBP location",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_update_gmb_location(
        account_id: str, selected_location_id: str, google_account_id: str | None = None
    ) -> str:
        """Update GBP location

        Args:
            account_id: (required)
            selected_location_id: (required)
            google_account_id: Optional but recommended. The Google Business Account resource name ("accounts/123") that owns the new location (from GET gmb-locations). When provided, the location is resolved directly instead of by enumerating the account, which is required for accounts with many locations. Named `googleAccountId` to disambiguate from the path `accountId` (the Zernio account). The legacy field name `accountId` is still accepted for backwards compatibility."""
        client = _get_client()
        try:
            response = client.connect.update_gmb_location(
                account_id=account_id,
                selected_location_id=selected_location_id,
                google_account_id=google_account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Assign GBP location to another profile",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_assign_google_business_location(
        account_id: str,
        profile_id: str,
        selected_location_id: str,
        google_account_id: str | None = None,
    ) -> str:
        """Assign GBP location to another profile

        Args:
            account_id: A source connected GBP account whose OAuth grant is reused. (required)
            profile_id: Target profile to connect the location onto. (required)
            selected_location_id: The Google Business location ID to assign (e.g. "locations/123"). (required)
            google_account_id: Optional but recommended. The Google Business Account resource name ("accounts/123") that owns the location (from GET gmb-locations). When provided the location is resolved directly instead of by enumerating the account, required for accounts with many locations."""
        client = _get_client()
        try:
            response = client.connect.assign_google_business_location(
                account_id=account_id,
                profile_id=profile_id,
                selected_location_id=selected_location_id,
                google_account_id=google_account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Reddit subreddits",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_get_reddit_subreddits(account_id: str) -> str:
        """List Reddit subreddits

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.connect.get_reddit_subreddits(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Set default subreddit",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_update_reddit_subreddits(
        account_id: str, default_subreddit: str
    ) -> str:
        """Set default subreddit

        Args:
            account_id: (required)
            default_subreddit: (required)"""
        client = _get_client()
        try:
            response = client.connect.update_reddit_subreddits(
                account_id=account_id, default_subreddit=default_subreddit
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get subreddit rules",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_get_subreddit_rules(account_id: str, subreddit: str) -> str:
        """Get subreddit rules

        Args:
            account_id: The ID of the Reddit account (required)
            subreddit: Subreddit name (without the "r/" prefix) (required)"""
        client = _get_client()
        try:
            response = client.connect.get_subreddit_rules(
                account_id=account_id, subreddit=subreddit
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Vote on a Reddit post or comment",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_vote_reddit_thing(
        account_id: str, thing_id: str, direction: int
    ) -> str:
        """Vote on a Reddit post or comment

           Args:
               account_id: The ID of the Reddit account casting the vote (required)
               thing_id: Reddit fullname of the target. Prefix "t3_" for a post and "t1_" for a comment. A bare id with no prefix is treated as a post ("t3_").
        (required)
               direction: 1 to upvote, -1 to downvote, 0 to clear an existing vote (required)"""
        client = _get_client()
        try:
            response = client.connect.vote_reddit_thing(
                account_id=account_id, thing_id=thing_id, direction=direction
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List subreddit flairs",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_get_reddit_flairs(account_id: str, subreddit: str) -> str:
        """List subreddit flairs

        Args:
            account_id: (required)
            subreddit: Subreddit name (without "r/" prefix) to fetch flairs for (required)"""
        client = _get_client()
        try:
            response = client.connect.get_reddit_flairs(
                account_id=account_id, subreddit=subreddit
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Set Reddit post flair",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_set_reddit_post_flair(
        account_id: str,
        subreddit: str,
        post_id: str,
        flair_template_id: str,
        text: str | None = None,
    ) -> str:
        """Set Reddit post flair

        Args:
            account_id: The ID of the Reddit account that owns the post (required)
            subreddit: Subreddit name (without the "r/" prefix) (required)
            post_id: Reddit post id, with or without the t3_ prefix (required)
            flair_template_id: Flair template id from the GET on this path (required)
            text: Optional override text, only for editable flair templates"""
        client = _get_client()
        try:
            response = client.connect.set_reddit_post_flair(
                account_id=account_id,
                subreddit=subreddit,
                post_id=post_id,
                flair_template_id=flair_template_id,
                text=text,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # CONNECTED_APPS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List connected apps",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connected_apps_list_connected_apps() -> str:
        """List connected apps"""
        client = _get_client()
        try:
            response = client.connected_apps.list_connected_apps()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Revoke connected app",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connected_apps_revoke_connected_app(client_id: str) -> str:
        """Revoke connected app

        Args:
            client_id: OAuth client id, as returned by GET /v1/me/connected-apps. (required)"""
        client = _get_client()
        try:
            response = client.connected_apps.revoke_connected_app(client_id=client_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # CONTACTS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List contacts",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def contacts_list_contacts(
        profile_id: str | None = None,
        account_id: str | None = None,
        search: str | None = None,
        tag: str | None = None,
        tags: str | None = None,
        platform: str | None = None,
        is_subscribed: str | None = None,
        limit: int = 50,
        skip: int = 0,
    ) -> str:
        """List contacts

        Args:
            profile_id: Filter by profile. Omit to list across all profiles. Matches the profile recorded on the contact itself, which is set when the contact is created and is independent of the profile its account currently belongs to. Filter by accountId to list a contact through its channel instead.
            account_id: Filter by the SocialAccount that owns the contact channel. Contacts are resolved through their channels, so the profileId contact filter is not applied while accountId is set. A profileId sent alongside is still access-checked and still scopes the returned filters.tags list.
            search: Case-insensitive substring match on the contact name, email and company. Phone numbers and other platform identifiers are not matched: they live on the contact channel, not on the contact. To reach a contact from an inbox webhook, use the conversation.contactId it already carries.
            tag
            tags: Comma-separated tags, matches contacts carrying any of them
            platform
            is_subscribed
            limit
            skip"""
        client = _get_client()
        try:
            response = client.contacts.list_contacts(
                profile_id=profile_id,
                account_id=account_id,
                search=search,
                tag=tag,
                tags=tags,
                platform=platform,
                is_subscribed=is_subscribed,
                limit=limit,
                skip=skip,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create contact",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def contacts_create_contact(
        profile_id: str,
        name: str,
        email: str | None = None,
        company: str | None = None,
        tags: list[str] | None = None,
        is_subscribed: bool = True,
        notes: str | None = None,
        account_id: str | None = None,
        platform: str | None = None,
        platform_identifier: str | None = None,
        display_identifier: str | None = None,
    ) -> str:
        """Create contact

        Args:
            profile_id: (required)
            name: (required)
            email
            company
            tags
            is_subscribed
            notes
            account_id: Optional. Creates a channel if provided with platform + platformIdentifier
            platform
            platform_identifier
            display_identifier"""
        client = _get_client()
        try:
            response = client.contacts.create_contact(
                profile_id=profile_id,
                name=name,
                email=email,
                company=company,
                tags=tags,
                is_subscribed=is_subscribed,
                notes=notes,
                account_id=account_id,
                platform=platform,
                platform_identifier=platform_identifier,
                display_identifier=display_identifier,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get contact",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def contacts_get_contact(contact_id: str) -> str:
        """Get contact

        Args:
            contact_id: (required)"""
        client = _get_client()
        try:
            response = client.contacts.get_contact(contact_id=contact_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update contact",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def contacts_update_contact(
        contact_id: str,
        name: str | None = None,
        email: str | None = None,
        company: str | None = None,
        avatar_url: str | None = None,
        tags: list[str] | None = None,
        is_subscribed: bool | None = None,
        is_blocked: bool | None = None,
        notes: str | None = None,
    ) -> str:
        """Update contact

        Args:
            contact_id: (required)
            name
            email
            company
            avatar_url
            tags
            is_subscribed
            is_blocked
            notes"""
        client = _get_client()
        try:
            response = client.contacts.update_contact(
                contact_id=contact_id,
                name=name,
                email=email,
                company=company,
                avatar_url=avatar_url,
                tags=tags,
                is_subscribed=is_subscribed,
                is_blocked=is_blocked,
                notes=notes,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete contact",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def contacts_delete_contact(contact_id: str) -> str:
        """Delete contact

        Args:
            contact_id: (required)"""
        client = _get_client()
        try:
            response = client.contacts.delete_contact(contact_id=contact_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List channels for a contact",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def contacts_get_contact_channels(contact_id: str) -> str:
        """List channels for a contact

        Args:
            contact_id: (required)"""
        client = _get_client()
        try:
            response = client.contacts.get_contact_channels(contact_id=contact_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Bulk create contacts",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def contacts_bulk_create_contacts(
        profile_id: str,
        contacts: list[dict[str, Any]] | None,
        account_id: str | None = None,
        platform: str | None = None,
    ) -> str:
        """Bulk create contacts

        Args:
            profile_id: (required)
            account_id: Required when contacts carry channel data (platformIdentifier or a row-level accountId). Omit for a plain CRM import with no channels.
            platform: Ignored when accountId is set: the platform is derived from the resolved account. Only relevant to disambiguate accountId lookup; a mismatch 404s.
            contacts: (required)"""
        client = _get_client()
        try:
            response = client.contacts.bulk_create_contacts(
                profile_id=profile_id,
                account_id=account_id,
                platform=platform,
                contacts=contacts,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # CONVERSIONS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get Event Match Quality",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def conversions_get_conversions_quality(
        account_id: str, destination_id: str
    ) -> str:
        """Get Event Match Quality

        Args:
            account_id: SocialAccount _id (must be a metaads account). (required)
            destination_id: Meta pixel/dataset ID. (required)"""
        client = _get_client()
        try:
            response = client.conversions.get_conversions_quality(
                account_id=account_id, destination_id=destination_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Send conversion events",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def conversions_send_conversions(
        account_id: str,
        destination_id: str,
        events: list[dict[str, Any]] | None,
        test_code: str | None = None,
        consent: dict[str, Any] | None = None,
    ) -> str:
        """Send conversion events

            Args:
                account_id: SocialAccount ID (metaads, googleads, linkedinads, tiktokads, or openaiads). (required)
                destination_id: Platform destination identifier. For Meta, the pixel/dataset
        ID. For Google, the conversion action resource name. For
        LinkedIn, the conversion rule ID or full
        `urn:lla:llaPartnerConversion:{id}` URN. For OpenAI Ads, the
        pixel wire id.
         (required)
                events: (required)
                test_code: Meta `test_event_code` passthrough. Ignored by Google, LinkedIn, and OpenAI Ads.
                consent: Batch-level user consent. Required by Google for EEA/UK
        events under the Feb 2026 restrictions. On Meta, any
        DENIED flag enables Limited Data Use on every event in
        the batch (data_processing_options ["LDU"] with
        geolocation, country 0 / state 0); GRANTED or absent
        consent sends events with Meta's default processing.
        Ignored by LinkedIn."""
        client = _get_client()
        try:
            response = client.conversions.send_conversions(
                account_id=account_id,
                destination_id=destination_id,
                events=events,
                test_code=test_code,
                consent=consent,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Adjust uploaded conversions",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def conversions_adjust_conversions(
        account_id: str, destination_id: str, adjustments: list[dict[str, Any]] | None
    ) -> str:
        """Adjust uploaded conversions

        Args:
            account_id: SocialAccount ID. Must be a `googleads` account. (required)
            destination_id: Conversion action resource name, e.g. `customers/1234567890/conversionActions/987654321`. (required)
            adjustments: (required)"""
        client = _get_client()
        try:
            response = client.conversions.adjust_conversions(
                account_id=account_id,
                destination_id=destination_id,
                adjustments=adjustments,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List conversion destinations",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def conversions_list_conversion_destinations(account_id: str) -> str:
        """List conversion destinations

        Args:
            account_id: SocialAccount ID (metaads, googleads, linkedinads, tiktokads, or openaiads). (required)"""
        client = _get_client()
        try:
            response = client.conversions.list_conversion_destinations(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a conversion destination",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def conversions_create_conversion_destination(
        account_id: str,
        ad_account_id: str,
        name: str,
        type: str,
        attribution_type: str | None = None,
        post_click_attribution_window_size: int | None = None,
        view_through_attribution_window_size: int | None = None,
        value_type: str | None = None,
        value: dict[str, Any] | None = None,
        auto_association_type: str = "ALL_CAMPAIGNS",
        counting_type: str | None = None,
        primary_for_goal: bool | None = None,
    ) -> str:
        """Create a conversion destination

            Args:
                account_id: SocialAccount ID (linkedinads or googleads). (required)
                ad_account_id: Ad account ID. For LinkedIn: numeric (e.g. "5123456") or
        full `urn:li:sponsoredAccount:{id}` URN. For Google: numeric
        customer ID (e.g. "1234567890") or `customers/{id}` form.
         (required)
                name: (required)
                type: Conversion type. For LinkedIn: a unified standard event name
        (e.g. "Purchase", "Lead", "AddToCart") or a LinkedIn rule
        type enum (e.g. "PURCHASE", "QUALIFIED_LEAD"). For Google:
        a unified standard event name (Purchase, Subscribe,
        CompleteRegistration, Lead, Schedule) or a Google
        ConversionActionCategory enum value directly (e.g.
        "PURCHASE", "SUBSCRIBE_PAID", "SIGNUP", "IMPORTED_LEAD",
        "BOOK_APPOINTMENT"). Unknown values pass through to the
        platform.
         (required)
                attribution_type: LinkedIn only.
                post_click_attribution_window_size: LinkedIn only. Default 30. 365 only allowed for LEAD,
        PURCHASE, ADD_TO_CART, QUALIFIED_LEAD, SUBMIT_APPLICATION
        rule types; the API rejects other combinations locally.
                view_through_attribution_window_size: LinkedIn only. Default 7. Same 365-day-window type
        restriction applies as `postClickAttributionWindowSize`.
                value_type: LinkedIn only. DYNAMIC (default) uses the per-event `value`
        from `sendConversions`. FIXED uses the rule's `value` field.
        NO_VALUE drops monetary value entirely.
                value: LinkedIn only. Static conversion value. Used when
        `valueType=FIXED`. The currency should match the ad
        account's currency.
                auto_association_type: LinkedIn only. Controls campaign association at rule-creation
        time:
        - ALL_CAMPAIGNS: associate the rule with every active,
          paused, and draft campaign in the ad account
        - OBJECTIVE_BASED: associate only campaigns whose
          objective matches the rule's type
        - NONE: don't auto-associate. Manage associations via
          the `/associations` endpoints below.
        Note: auto-association runs once at create time; new
        campaigns added after the rule still need explicit
        association.
                counting_type: Google Ads only. Whether to count multiple conversions from
        the same click (MANY_PER_CLICK) or at most one
        (ONE_PER_CLICK). Defaults to MANY_PER_CLICK if omitted.
                primary_for_goal: Google Ads only. When true, the conversion action is marked
        as primary and immediately influences Smart Bidding. Defaults
        to false (secondary, record-only) to avoid unintentionally
        steering the customer's campaigns on creation."""
        client = _get_client()
        try:
            response = client.conversions.create_conversion_destination(
                account_id=account_id,
                ad_account_id=ad_account_id,
                name=name,
                type=type,
                attribution_type=attribution_type,
                post_click_attribution_window_size=post_click_attribution_window_size,
                view_through_attribution_window_size=view_through_attribution_window_size,
                value_type=value_type,
                value=value,
                auto_association_type=auto_association_type,
                counting_type=counting_type,
                primary_for_goal=primary_for_goal,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a conversion destination",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def conversions_get_conversion_destination(
        account_id: str, destination_id: str, ad_account_id: str
    ) -> str:
        """Get a conversion destination

        Args:
            account_id: (required)
            destination_id: (required)
            ad_account_id: Numeric ID or full `urn:li:sponsoredAccount:{id}` URN. (required)"""
        client = _get_client()
        try:
            response = client.conversions.get_conversion_destination(
                account_id=account_id,
                destination_id=destination_id,
                ad_account_id=ad_account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update a conversion destination",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def conversions_update_conversion_destination(
        account_id: str,
        destination_id: str,
        ad_account_id: str,
        name: str | None = None,
        enabled: bool | None = None,
        attribution_type: str | None = None,
        post_click_attribution_window_size: int | None = None,
        view_through_attribution_window_size: int | None = None,
        value_type: str | None = None,
        value: dict[str, Any] | None = None,
    ) -> str:
        """Update a conversion destination

            Args:
                account_id: (required)
                destination_id: (required)
                ad_account_id: (required)
                name
                enabled: Setting `false` is equivalent to calling DELETE — the
        rule will appear as `inactive` afterwards.
                attribution_type
                post_click_attribution_window_size: 365 only allowed for LEAD, PURCHASE, ADD_TO_CART,
        QUALIFIED_LEAD, SUBMIT_APPLICATION rule types.
                view_through_attribution_window_size: 365 only allowed for LEAD, PURCHASE, ADD_TO_CART,
        QUALIFIED_LEAD, SUBMIT_APPLICATION rule types.
                value_type
                value: Used when `valueType=FIXED`."""
        client = _get_client()
        try:
            response = client.conversions.update_conversion_destination(
                account_id=account_id,
                destination_id=destination_id,
                ad_account_id=ad_account_id,
                name=name,
                enabled=enabled,
                attribution_type=attribution_type,
                post_click_attribution_window_size=post_click_attribution_window_size,
                view_through_attribution_window_size=view_through_attribution_window_size,
                value_type=value_type,
                value=value,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete a conversion destination",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def conversions_delete_conversion_destination(
        account_id: str, destination_id: str, ad_account_id: str | None = None
    ) -> str:
        """Delete a conversion destination

        Args:
            account_id: (required)
            destination_id: (required)
            ad_account_id: Required as query OR in JSON body."""
        client = _get_client()
        try:
            response = client.conversions.delete_conversion_destination(
                account_id=account_id,
                destination_id=destination_id,
                ad_account_id=ad_account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List associated campaigns",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def conversions_list_conversion_associations(
        account_id: str, destination_id: str, ad_account_id: str
    ) -> str:
        """List associated campaigns

        Args:
            account_id: (required)
            destination_id: (required)
            ad_account_id: (required)"""
        client = _get_client()
        try:
            response = client.conversions.list_conversion_associations(
                account_id=account_id,
                destination_id=destination_id,
                ad_account_id=ad_account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Associate campaigns",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def conversions_add_conversion_associations(
        account_id: str,
        destination_id: str,
        ad_account_id: str,
        campaign_ids: list[str] | None,
    ) -> str:
        """Associate campaigns

        Args:
            account_id: (required)
            destination_id: (required)
            ad_account_id: (required)
            campaign_ids: (required)"""
        client = _get_client()
        try:
            response = client.conversions.add_conversion_associations(
                account_id=account_id,
                destination_id=destination_id,
                ad_account_id=ad_account_id,
                campaign_ids=campaign_ids,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Remove associated campaigns",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def conversions_remove_conversion_associations(
        account_id: str, destination_id: str, ad_account_id: str, campaign_ids: str
    ) -> str:
        """Remove associated campaigns

        Args:
            account_id: (required)
            destination_id: (required)
            ad_account_id: (required)
            campaign_ids: Comma-separated list of campaign IDs. (required)"""
        client = _get_client()
        try:
            response = client.conversions.remove_conversion_associations(
                account_id=account_id,
                destination_id=destination_id,
                ad_account_id=ad_account_id,
                campaign_ids=campaign_ids,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get attribution metrics",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def conversions_get_conversion_metrics(
        account_id: str,
        destination_id: str,
        ad_account_id: str,
        start_date: str,
        end_date: str | None = None,
        granularity: str = "DAILY",
    ) -> str:
        """Get attribution metrics

        Args:
            account_id: (required)
            destination_id: (required)
            ad_account_id: (required)
            start_date: (required)
            end_date
            granularity"""
        client = _get_client()
        try:
            response = client.conversions.get_conversion_metrics(
                account_id=account_id,
                destination_id=destination_id,
                ad_account_id=ad_account_id,
                start_date=start_date,
                end_date=end_date,
                granularity=granularity,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # CUSTOM_FIELDS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Set custom field value",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def custom_fields_set_contact_field_value(
        contact_id: str, slug: str, value: str
    ) -> str:
        """Set custom field value

        Args:
            contact_id: (required)
            slug: (required)
            value: Field value (type depends on field definition) (required)"""
        client = _get_client()
        try:
            response = client.custom_fields.set_contact_field_value(
                contact_id=contact_id, slug=slug, value=value
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Clear custom field value",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def custom_fields_clear_contact_field_value(contact_id: str, slug: str) -> str:
        """Clear custom field value

        Args:
            contact_id: (required)
            slug: (required)"""
        client = _get_client()
        try:
            response = client.custom_fields.clear_contact_field_value(
                contact_id=contact_id, slug=slug
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List custom field definitions",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def custom_fields_list_custom_fields(profile_id: str | None = None) -> str:
        """List custom field definitions

        Args:
            profile_id: Filter by profile. Omit to list across all profiles"""
        client = _get_client()
        try:
            response = client.custom_fields.list_custom_fields(profile_id=profile_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create custom field",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def custom_fields_create_custom_field(
        profile_id: str,
        name: str,
        type: str,
        slug: str | None = None,
        options: list[str] | None = None,
    ) -> str:
        """Create custom field

        Args:
            profile_id: (required)
            name: (required)
            slug: Auto-generated from name if not provided
            type: (required)
            options: Required for select type"""
        client = _get_client()
        try:
            response = client.custom_fields.create_custom_field(
                profile_id=profile_id, name=name, slug=slug, type=type, options=options
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update custom field",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def custom_fields_update_custom_field(
        field_id: str, name: str | None = None, options: list[str] | None = None
    ) -> str:
        """Update custom field

        Args:
            field_id: (required)
            name
            options"""
        client = _get_client()
        try:
            response = client.custom_fields.update_custom_field(
                field_id=field_id, name=name, options=options
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete custom field",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def custom_fields_delete_custom_field(field_id: str) -> str:
        """Delete custom field

        Args:
            field_id: (required)"""
        client = _get_client()
        try:
            response = client.custom_fields.delete_custom_field(field_id=field_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # DISCORD

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get Discord account settings",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def discord_get_discord_settings(account_id: str) -> str:
        """Get Discord account settings

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.discord.get_discord_settings(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update Discord settings",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_update_discord_settings(
        account_id: str,
        webhook_username: str | None = None,
        webhook_avatar_url: str | None = None,
        channel_id: str | None = None,
    ) -> str:
        """Update Discord settings

        Args:
            account_id: (required)
            webhook_username: Custom display name for the webhook (1-80 chars). Empty string resets to default ("Zernio"). Cannot contain "clyde" or "discord".
            webhook_avatar_url: Custom avatar URL. Empty string resets to default bot avatar.
            channel_id: Switch to a different channel in the same guild. Must be a text (0), announcement (5), or forum (15) channel."""
        client = _get_client()
        try:
            response = client.discord.update_discord_settings(
                account_id=account_id,
                webhook_username=webhook_username,
                webhook_avatar_url=webhook_avatar_url,
                channel_id=channel_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Discord guild channels",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def discord_get_discord_channels(account_id: str) -> str:
        """List Discord guild channels

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.discord.get_discord_channels(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Send a Discord Direct Message",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_send_discord_direct_message(
        account_id: str,
        user_id: str,
        content: str | None = None,
        embeds: list[dict[str, Any]] | None = None,
        attachments: list[dict[str, Any]] | None = None,
        tts: bool | None = None,
    ) -> str:
        """Send a Discord Direct Message

        Args:
            account_id: SocialAccount _id of the connected Discord account the bot speaks as. Caller must own the account (directly or via team membership). (required)
            user_id: Discord snowflake ID of the recipient (15-21 digits). (required)
            content: Message text, up to 2,000 characters.
            embeds: Up to 10 Discord embeds. Same shape as channel-post embeds (title, description, color, fields, etc.). See DiscordPlatformData.embeds for the embed object schema.
            attachments: Up to 10 media attachments. Each is `{ type: image|video|gif|document, url, filename?, mimeType?, size? }`.
            tts: Send as text-to-speech message."""
        client = _get_client()
        try:
            response = client.discord.send_discord_direct_message(
                account_id=account_id,
                user_id=user_id,
                content=content,
                embeds=embeds,
                attachments=attachments,
                tts=tts,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Discord guild roles",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def discord_list_discord_guild_roles(guild_id: str, account_id: str) -> str:
        """List Discord guild roles

        Args:
            guild_id: Discord guild snowflake ID (required)
            account_id: SocialAccount _id of the Discord account bound to this guild (required)"""
        client = _get_client()
        try:
            response = client.discord.list_discord_guild_roles(
                guild_id=guild_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a Discord guild role",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_create_discord_guild_role(
        guild_id: str,
        account_id: str,
        name: str,
        color: int | None = None,
        hoist: bool | None = None,
        mentionable: bool | None = None,
        permissions: str | None = None,
    ) -> str:
        """Create a Discord guild role

        Args:
            guild_id: Discord guild snowflake ID (required)
            account_id: SocialAccount _id of the Discord account bound to this guild (required)
            name: (required)
            color: Decimal color (0 = no color). 0xFF0000 red is 16711680.
            hoist: Display members with this role separately in the member list
            mentionable: Allow anyone to @mention this role
            permissions: Permissions bitfield as a stringified integer"""
        client = _get_client()
        try:
            response = client.discord.create_discord_guild_role(
                guild_id=guild_id,
                account_id=account_id,
                name=name,
                color=color,
                hoist=hoist,
                mentionable=mentionable,
                permissions=permissions,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Edit a Discord guild role",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_edit_discord_guild_role(
        guild_id: str,
        role_id: str,
        account_id: str,
        name: str | None = None,
        color: int | None = None,
        hoist: bool | None = None,
        mentionable: bool | None = None,
        permissions: str | None = None,
    ) -> str:
        """Edit a Discord guild role

        Args:
            guild_id: Discord guild snowflake ID (required)
            role_id: Discord role snowflake ID (required)
            account_id: SocialAccount _id of the Discord account bound to this guild (required)
            name
            color
            hoist
            mentionable
            permissions: Permissions bitfield as a stringified integer"""
        client = _get_client()
        try:
            response = client.discord.edit_discord_guild_role(
                guild_id=guild_id,
                role_id=role_id,
                account_id=account_id,
                name=name,
                color=color,
                hoist=hoist,
                mentionable=mentionable,
                permissions=permissions,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete a Discord guild role",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_delete_discord_guild_role(
        guild_id: str, role_id: str, account_id: str
    ) -> str:
        """Delete a Discord guild role

        Args:
            guild_id: Discord guild snowflake ID (required)
            role_id: Discord role snowflake ID (required)
            account_id: SocialAccount _id of the Discord account bound to this guild (required)"""
        client = _get_client()
        try:
            response = client.discord.delete_discord_guild_role(
                guild_id=guild_id, role_id=role_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Discord guild members",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def discord_list_discord_guild_members(
        guild_id: str, account_id: str, limit: int = 100, after: str | None = None
    ) -> str:
        """List Discord guild members

        Args:
            guild_id: (required)
            account_id: (required)
            limit: Page size (1-1000).
            after: Snowflake of the last member from the previous page."""
        client = _get_client()
        try:
            response = client.discord.list_discord_guild_members(
                guild_id=guild_id, account_id=account_id, limit=limit, after=after
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Search Discord guild members",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def discord_search_discord_guild_members(
        guild_id: str, account_id: str, query: str, limit: int = 25
    ) -> str:
        """Search Discord guild members

        Args:
            guild_id: (required)
            account_id: (required)
            query: Username or nickname prefix to match. (required)
            limit"""
        client = _get_client()
        try:
            response = client.discord.search_discord_guild_members(
                guild_id=guild_id, account_id=account_id, query=query, limit=limit
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a Discord guild member",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def discord_get_discord_guild_member(
        guild_id: str, user_id: str, account_id: str
    ) -> str:
        """Get a Discord guild member

        Args:
            guild_id: (required)
            user_id: Discord user snowflake. (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.discord.get_discord_guild_member(
                guild_id=guild_id, user_id=user_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Assign a role to a guild member",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_add_discord_member_role(
        guild_id: str, user_id: str, role_id: str, account_id: str
    ) -> str:
        """Assign a role to a guild member

        Args:
            guild_id: (required)
            user_id: Discord user snowflake to assign the role to. (required)
            role_id: (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.discord.add_discord_member_role(
                guild_id=guild_id,
                user_id=user_id,
                role_id=role_id,
                account_id=account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Remove a role from a guild member",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_remove_discord_member_role(
        guild_id: str, user_id: str, role_id: str, account_id: str
    ) -> str:
        """Remove a role from a guild member

        Args:
            guild_id: (required)
            user_id: (required)
            role_id: (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.discord.remove_discord_member_role(
                guild_id=guild_id,
                user_id=user_id,
                role_id=role_id,
                account_id=account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete a Discord channel message",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_delete_discord_message(
        channel_id: str, message_id: str, account_id: str
    ) -> str:
        """Delete a Discord channel message

        Args:
            channel_id: Discord channel snowflake ID (required)
            message_id: Discord message snowflake ID (required)
            account_id: SocialAccount _id of the Discord account bound to this channel's guild (required)"""
        client = _get_client()
        try:
            response = client.discord.delete_discord_message(
                channel_id=channel_id, message_id=message_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Crosspost Discord message",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_crosspost_discord_message(
        channel_id: str, message_id: str, account_id: str
    ) -> str:
        """Crosspost Discord message

        Args:
            channel_id: Discord announcement channel snowflake ID (required)
            message_id: Discord message snowflake ID (required)
            account_id: SocialAccount _id of the Discord account bound to this channel's guild (required)"""
        client = _get_client()
        try:
            response = client.discord.crosspost_discord_message(
                channel_id=channel_id, message_id=message_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a Discord public thread",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_create_discord_thread(
        channel_id: str,
        account_id: str,
        name: str,
        message_id: str | None = None,
        auto_archive_duration: int | None = None,
    ) -> str:
        """Create a Discord public thread

        Args:
            channel_id: Discord channel snowflake ID (required)
            account_id: SocialAccount _id of the Discord account bound to this channel's guild (required)
            name: Thread name (required)
            message_id: Optional message snowflake to start the thread from. Omit for a standalone thread.
            auto_archive_duration: Minutes of inactivity before the thread auto-archives. Discord accepts only these four values."""
        client = _get_client()
        try:
            response = client.discord.create_discord_thread(
                channel_id=channel_id,
                account_id=account_id,
                name=name,
                message_id=message_id,
                auto_archive_duration=auto_archive_duration,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List pinned messages",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def discord_list_discord_pinned_messages(channel_id: str, account_id: str) -> str:
        """List pinned messages

        Args:
            channel_id: Discord channel snowflake. (required)
            account_id: SocialAccount _id of any Discord account in the same guild. (required)"""
        client = _get_client()
        try:
            response = client.discord.list_discord_pinned_messages(
                channel_id=channel_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Pin a Discord message",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_pin_discord_message(
        channel_id: str, message_id: str, account_id: str
    ) -> str:
        """Pin a Discord message

        Args:
            channel_id: (required)
            message_id: (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.discord.pin_discord_message(
                channel_id=channel_id, message_id=message_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Unpin a Discord message",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_unpin_discord_message(
        channel_id: str, message_id: str, account_id: str
    ) -> str:
        """Unpin a Discord message

        Args:
            channel_id: (required)
            message_id: (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.discord.unpin_discord_message(
                channel_id=channel_id, message_id=message_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Discord scheduled events",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def discord_list_discord_scheduled_events(
        guild_id: str, account_id: str, with_user_count: bool | None = None
    ) -> str:
        """List Discord scheduled events

        Args:
            guild_id: (required)
            account_id: (required)
            with_user_count: Include user_count on each event."""
        client = _get_client()
        try:
            response = client.discord.list_discord_scheduled_events(
                guild_id=guild_id,
                account_id=account_id,
                with_user_count=with_user_count,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a Discord scheduled event",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_create_discord_scheduled_event(
        guild_id: str,
        account_id: str,
        name: str,
        starts_at: str,
        entity: dict[str, Any] | None,
        description: str | None = None,
        image_data_uri: str | None = None,
    ) -> str:
        """Create a Discord scheduled event

        Args:
            guild_id: (required)
            account_id: (required)
            name: (required)
            description
            starts_at: ISO 8601 start time. Must be in the future. (required)
            entity: (required)
            image_data_uri: Optional cover image as a base64 data URI."""
        client = _get_client()
        try:
            response = client.discord.create_discord_scheduled_event(
                guild_id=guild_id,
                account_id=account_id,
                name=name,
                description=description,
                starts_at=starts_at,
                entity=entity,
                image_data_uri=image_data_uri,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a Discord scheduled event",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def discord_get_discord_scheduled_event(
        guild_id: str, event_id: str, account_id: str
    ) -> str:
        """Get a Discord scheduled event

        Args:
            guild_id: (required)
            event_id: (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.discord.get_discord_scheduled_event(
                guild_id=guild_id, event_id=event_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update a Discord scheduled event",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_update_discord_scheduled_event(
        guild_id: str,
        event_id: str,
        account_id: str,
        name: str | None = None,
        description: str | None = None,
        starts_at: str | None = None,
        ends_at: str | None = None,
        location: str | None = None,
        status: str | None = None,
        image_data_uri: str | None = None,
    ) -> str:
        """Update a Discord scheduled event

        Args:
            guild_id: (required)
            event_id: (required)
            account_id: (required)
            name
            description
            starts_at
            ends_at
            location: For external events.
            status: Status transition. Most common: 'cancelled' to cancel an event.
            image_data_uri"""
        client = _get_client()
        try:
            response = client.discord.update_discord_scheduled_event(
                guild_id=guild_id,
                event_id=event_id,
                account_id=account_id,
                name=name,
                description=description,
                starts_at=starts_at,
                ends_at=ends_at,
                location=location,
                status=status,
                image_data_uri=image_data_uri,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete a Discord scheduled event",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def discord_delete_discord_scheduled_event(
        guild_id: str, event_id: str, account_id: str
    ) -> str:
        """Delete a Discord scheduled event

        Args:
            guild_id: (required)
            event_id: (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.discord.delete_discord_scheduled_event(
                guild_id=guild_id, event_id=event_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # GMB_SERVICES

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get services",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def gmb_services_get_google_business_services(
        account_id: str, location_id: str | None = None
    ) -> str:
        """Get services

        Args:
            account_id: (required)
            location_id: Override which location to query. If omitted, uses the account's selected location."""
        client = _get_client()
        try:
            response = client.gmb_services.get_google_business_services(
                account_id=account_id, location_id=location_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Replace services",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def gmb_services_update_google_business_services(
        account_id: str,
        service_items: list[dict[str, Any]] | None,
        location_id: str | None = None,
    ) -> str:
        """Replace services

        Args:
            account_id: (required)
            location_id: Override which location to target. If omitted, uses the account's selected location.
            service_items: (required)"""
        client = _get_client()
        try:
            response = client.gmb_services.update_google_business_services(
                account_id=account_id,
                location_id=location_id,
                service_items=service_items,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # GMB_VERIFICATIONS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get verification state",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def gmb_verifications_get_google_business_verifications(
        account_id: str, location_id: str | None = None
    ) -> str:
        """Get verification state

        Args:
            account_id: The Zernio account ID (from /v1/accounts) (required)
            location_id: Override which location to query. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs."""
        client = _get_client()
        try:
            response = client.gmb_verifications.get_google_business_verifications(
                account_id=account_id, location_id=location_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Start a verification",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def gmb_verifications_start_google_business_verification(
        account_id: str,
        method: str,
        location_id: str | None = None,
        language_code: str | None = None,
        phone_number: str | None = None,
        email_address: str | None = None,
        mailer_contact: dict[str, Any] | None = None,
        context: dict[str, Any] | None = None,
    ) -> str:
        """Start a verification

        Args:
            account_id: The Zernio account ID (from /v1/accounts) (required)
            location_id: Override which location to target. If omitted, uses the account's selected location.
            method: The verification method. Selects which method-specific field below is required. (required)
            language_code
            phone_number: For PHONE_CALL / SMS.
            email_address: For EMAIL.
            mailer_contact: For ADDRESS (postcard) verification.
            context: ServiceBusinessContext (e.g. service address). Required for service-area businesses."""
        client = _get_client()
        try:
            response = client.gmb_verifications.start_google_business_verification(
                account_id=account_id,
                location_id=location_id,
                method=method,
                language_code=language_code,
                phone_number=phone_number,
                email_address=email_address,
                mailer_contact=mailer_contact,
                context=context,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Fetch verification options",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def gmb_verifications_fetch_google_business_verification_options(
        account_id: str,
        language_code: str,
        location_id: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> str:
        """Fetch verification options

        Args:
            account_id: The Zernio account ID (from /v1/accounts) (required)
            location_id: Override which location to query. If omitted, uses the account's selected location.
            language_code: (required)
            context: ServiceBusinessContext. Required for service-area businesses (must include the service address)."""
        client = _get_client()
        try:
            response = (
                client.gmb_verifications.fetch_google_business_verification_options(
                    account_id=account_id,
                    location_id=location_id,
                    language_code=language_code,
                    context=context,
                )
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Complete a verification",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def gmb_verifications_complete_google_business_verification(
        account_id: str, verification_id: str, pin: str, location_id: str | None = None
    ) -> str:
        """Complete a verification

        Args:
            account_id: The Zernio account ID (from /v1/accounts) (required)
            verification_id: The last segment of a verification `name` from GET /gmb-verifications. (required)
            location_id: Override which location to target. If omitted, uses the account's selected location.
            pin: The code Google sent to the business. (required)"""
        client = _get_client()
        try:
            response = client.gmb_verifications.complete_google_business_verification(
                account_id=account_id,
                verification_id=verification_id,
                location_id=location_id,
                pin=pin,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # INBOX_ANALYTICS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get inbox messaging volume",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def inbox_analytics_get_inbox_volume(
        from_date: str,
        to_date: str | None = None,
        profile_id: str | None = None,
        platform: str | None = None,
        account_id: str | None = None,
        source: str | None = None,
    ) -> str:
        """Get inbox messaging volume

        Args:
            from_date: Inclusive lower bound (YYYY-MM-DD). Required. (required)
            to_date: Inclusive upper bound (YYYY-MM-DD). Defaults to today.
            profile_id
            platform: Filter by single platform (facebook, instagram, twitter, etc.).
            account_id
            source: Filter by metadata.source lineage (human, workflow, sequence, broadcast, comment_automation, api, contact, platform)."""
        client = _get_client()
        try:
            response = client.inbox_analytics.get_inbox_volume(
                from_date=from_date,
                to_date=to_date,
                profile_id=profile_id,
                platform=platform,
                account_id=account_id,
                source=source,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get day × hour heatmap",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def inbox_analytics_get_inbox_heatmap(
        from_date: str,
        to_date: str | None = None,
        profile_id: str | None = None,
        platform: str | None = None,
        account_id: str | None = None,
        source: str | None = None,
        action: str | None = None,
    ) -> str:
        """Get day × hour heatmap

        Args:
            from_date: (required)
            to_date
            profile_id
            platform
            account_id
            source
            action: Narrow to a single event type. "all" or omitted means no filter."""
        client = _get_client()
        try:
            response = client.inbox_analytics.get_inbox_heatmap(
                from_date=from_date,
                to_date=to_date,
                profile_id=profile_id,
                platform=platform,
                account_id=account_id,
                source=source,
                action=action,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get inbox source breakdown",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def inbox_analytics_get_inbox_source_breakdown(
        from_date: str,
        to_date: str | None = None,
        profile_id: str | None = None,
        platform: str | None = None,
        account_id: str | None = None,
    ) -> str:
        """Get inbox source breakdown

        Args:
            from_date: (required)
            to_date
            profile_id
            platform
            account_id"""
        client = _get_client()
        try:
            response = client.inbox_analytics.get_inbox_source_breakdown(
                from_date=from_date,
                to_date=to_date,
                profile_id=profile_id,
                platform=platform,
                account_id=account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get inbox response-time stats",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def inbox_analytics_get_inbox_response_time(
        from_date: str,
        to_date: str | None = None,
        profile_id: str | None = None,
        platform: str | None = None,
        account_id: str | None = None,
    ) -> str:
        """Get inbox response-time stats

        Args:
            from_date: (required)
            to_date
            profile_id
            platform
            account_id"""
        client = _get_client()
        try:
            response = client.inbox_analytics.get_inbox_response_time(
                from_date=from_date,
                to_date=to_date,
                profile_id=profile_id,
                platform=platform,
                account_id=account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get top accounts by inbox volume",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def inbox_analytics_get_inbox_top_accounts(
        from_date: str,
        to_date: str | None = None,
        profile_id: str | None = None,
        platform: str | None = None,
        source: str | None = None,
        limit: int = 10,
    ) -> str:
        """Get top accounts by inbox volume

        Args:
            from_date: (required)
            to_date
            profile_id
            platform
            source
            limit: Cap on returned rows. Lower than the posting listing's 100 because each row triggers a SocialAccount Mongo lookup."""
        client = _get_client()
        try:
            response = client.inbox_analytics.get_inbox_top_accounts(
                from_date=from_date,
                to_date=to_date,
                profile_id=profile_id,
                platform=platform,
                source=source,
                limit=limit,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List conversation analytics",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def inbox_analytics_list_inbox_conversation_analytics(
        from_date: str,
        to_date: str | None = None,
        profile_id: str | None = None,
        platform: str | None = None,
        account_id: str | None = None,
        source: str | None = None,
        limit: int = 50,
        page: int = 1,
        sort_by: str = "lastMessageAt",
        order: str = "desc",
    ) -> str:
        """List conversation analytics

        Args:
            from_date: (required)
            to_date
            profile_id
            platform
            account_id
            source
            limit
            page
            sort_by
            order"""
        client = _get_client()
        try:
            response = client.inbox_analytics.list_inbox_conversation_analytics(
                from_date=from_date,
                to_date=to_date,
                profile_id=profile_id,
                platform=platform,
                account_id=account_id,
                source=source,
                limit=limit,
                page=page,
                sort_by=sort_by,
                order=order,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get conversation analytics",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def inbox_analytics_get_inbox_conversation_analytics(
        conversation_id: str, from_date: str, to_date: str | None = None
    ) -> str:
        """Get conversation analytics

        Args:
            conversation_id: Mongo _id or platformConversationId. (required)
            from_date: (required)
            to_date"""
        client = _get_client()
        try:
            response = client.inbox_analytics.get_inbox_conversation_analytics(
                conversation_id=conversation_id, from_date=from_date, to_date=to_date
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # INSTAGRAM

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List active Instagram stories",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def instagram_list_instagram_stories(account_id: str) -> str:
        """List active Instagram stories

        Args:
            account_id: The Instagram account ID (required)"""
        client = _get_client()
        try:
            response = client.instagram.list_instagram_stories(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get Instagram publishing limit",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def instagram_get_instagram_publishing_limit(account_id: str) -> str:
        """Get Instagram publishing limit

        Args:
            account_id: The ID of the Instagram account (required)"""
        client = _get_client()
        try:
            response = client.instagram.get_instagram_publishing_limit(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Search Instagram audio",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def instagram_search_instagram_audio(
        account_id: str, audio_type: str, q: str | None = None
    ) -> str:
        """Search Instagram audio

        Args:
            account_id: The ID of the Instagram account (required)
            audio_type: Catalog to search: licensed music or original sounds from Reels. (required)
            q: Search keywords. Omit to get the current trending list."""
        client = _get_client()
        try:
            response = client.instagram.search_instagram_audio(
                account_id=account_id, audio_type=audio_type, q=q
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get Instagram audio metadata",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def instagram_get_instagram_audio(account_id: str, audio_id: str) -> str:
        """Get Instagram audio metadata

        Args:
            account_id: The ID of the Instagram account (required)
            audio_id: Instagram audio asset ID (required)"""
        client = _get_client()
        try:
            response = client.instagram.get_instagram_audio(
                account_id=account_id, audio_id=audio_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get Instagram story insights",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def instagram_get_instagram_story_insights(account_id: str, story_id: str) -> str:
        """Get Instagram story insights

        Args:
            account_id: The Instagram account ID (required)
            story_id: The Instagram media ID of the story. (required)"""
        client = _get_client()
        try:
            response = client.instagram.get_instagram_story_insights(
                account_id=account_id, story_id=story_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # INVITES

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create invite token",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def invites_create_invite_token(
        scope: str,
        profile_ids: list[str] | None = None,
        role: str = "member",
        read_only: bool | None = None,
    ) -> str:
        """Create invite token

        Args:
            scope: 'all' grants access to all profiles, 'profiles' restricts to specific profiles (required)
            profile_ids: Required if scope is 'profiles'. Array of profile IDs to grant access to.
            role: Org role granted to the invitee. Defaults to 'member'. 'admin' can manage the team (invite/remove members, change roles and access) and billing, but not ownership transfer or account deletion. 'billing_admin' (displayed as Billing Manager) manages billing only. 'viewer' creates a read-only member who can view everything in their profile scope but cannot perform any content mutation (publish, edit, delete, connect accounts).
            read_only: Deprecated. Use role 'viewer' instead. When true, the invite is created with role 'viewer'. Cannot be combined with role 'billing_admin' or 'admin'."""
        client = _get_client()
        try:
            response = client.invites.create_invite_token(
                scope=scope, profile_ids=profile_ids, role=role, read_only=read_only
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # LEAD_GEN

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List submitted leads",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def lead_gen_list_leads(
        form_id: str | None = None,
        account_id: str | None = None,
        ad_account_id: str | None = None,
        limit: int = 25,
        since: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """List submitted leads

        Args:
            form_id: Filter to a single lead form.
            account_id: Filter to a single connected account. LinkedIn ads accounts switch to the live fetch.
            ad_account_id: LinkedIn only: the LinkedIn ad account id whose responses to read (owner-scoped finder).
            limit
            since: Unix seconds; only leads created at/after this timestamp.
            cursor: Keyset cursor from a previous response's pagination.cursor (Meta: AdLead id; LinkedIn: numeric start offset)."""
        client = _get_client()
        try:
            response = client.lead_gen.list_leads(
                form_id=form_id,
                account_id=account_id,
                ad_account_id=ad_account_id,
                limit=limit,
                since=since,
                cursor=cursor,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List lead forms",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def lead_gen_list_lead_forms(
        account_id: str,
        ad_account_id: str | None = None,
        limit: int = 25,
        cursor: str | None = None,
    ) -> str:
        """List lead forms

        Args:
            account_id: Connected facebook or linkedin ads account id. (required)
            ad_account_id: LinkedIn only: the LinkedIn ad account id (used to resolve the owning organization). Required for LinkedIn.
            limit
            cursor"""
        client = _get_client()
        try:
            response = client.lead_gen.list_lead_forms(
                account_id=account_id,
                ad_account_id=ad_account_id,
                limit=limit,
                cursor=cursor,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a lead form",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def lead_gen_create_lead_form(
        account_id: str,
        name: str,
        privacy_policy_url: str,
        questions: list[dict[str, Any]] | None = None,
        privacy_policy_link_text: str | None = None,
        follow_up_action_url: str | None = None,
        locale: str | None = None,
        thank_you_title: str | None = None,
        thank_you_body: str | None = None,
        thank_you_button_text: str | None = None,
        thank_you_button_type: str | None = None,
        thank_you_website_url: str | None = None,
        is_optimized_for_quality: bool | None = None,
        platform_specific_data: dict[str, Any] | None = None,
    ) -> str:
        """Create a lead form

        Args:
            account_id: (required)
            name: (required)
            questions: Deprecated (Meta legacy shape): use platformSpecificData.questions.
            privacy_policy_url: (required)
            privacy_policy_link_text: Deprecated: use platformSpecificData.privacyPolicyLinkText.
            follow_up_action_url: Deprecated: use platformSpecificData.followUpActionUrl.
            locale: Deprecated: use platformSpecificData.locale.
            thank_you_title: Deprecated: use platformSpecificData.thankYouTitle.
            thank_you_body: Deprecated: use platformSpecificData.thankYouBody.
            thank_you_button_text: Deprecated: use platformSpecificData.thankYouButtonText.
            thank_you_button_type: Deprecated: use platformSpecificData.thankYouButtonType.
            thank_you_website_url: Deprecated: use platformSpecificData.thankYouWebsiteUrl.
            is_optimized_for_quality: Deprecated: use platformSpecificData.isOptimizedForQuality.
            platform_specific_data: Form content; the shape is selected by the accountId's platform. Unknown fields are a 400 (strict-parsed)."""
        client = _get_client()
        try:
            response = client.lead_gen.create_lead_form(
                account_id=account_id,
                name=name,
                questions=questions,
                privacy_policy_url=privacy_policy_url,
                privacy_policy_link_text=privacy_policy_link_text,
                follow_up_action_url=follow_up_action_url,
                locale=locale,
                thank_you_title=thank_you_title,
                thank_you_body=thank_you_body,
                thank_you_button_text=thank_you_button_text,
                thank_you_button_type=thank_you_button_type,
                thank_you_website_url=thank_you_website_url,
                is_optimized_for_quality=is_optimized_for_quality,
                platform_specific_data=platform_specific_data,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a lead form",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def lead_gen_get_lead_form(form_id: str, account_id: str) -> str:
        """Get a lead form

        Args:
            form_id: Numeric form id (Meta leadgen_form id or LinkedIn leadForm id). (required)
            account_id: Connected facebook or linkedin ads account id (selects the platform). (required)"""
        client = _get_client()
        try:
            response = client.lead_gen.get_lead_form(
                form_id=form_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Archive a lead form",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def lead_gen_archive_lead_form(form_id: str, account_id: str) -> str:
        """Archive a lead form

        Args:
            form_id: Numeric form id (Meta leadgen_form id or LinkedIn leadForm id). (required)
            account_id: Connected facebook or linkedin ads account id (selects the platform). (required)"""
        client = _get_client()
        try:
            response = client.lead_gen.archive_lead_form(
                form_id=form_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List leads for a single form",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def lead_gen_list_form_leads(
        form_id: str,
        account_id: str,
        limit: int = 25,
        cursor: str | None = None,
        since: int | None = None,
    ) -> str:
        """List leads for a single form

        Args:
            form_id: (required)
            account_id: (required)
            limit
            cursor
            since: Unix seconds."""
        client = _get_client()
        try:
            response = client.lead_gen.list_form_leads(
                form_id=form_id,
                account_id=account_id,
                limit=limit,
                cursor=cursor,
                since=since,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a test lead",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def lead_gen_create_test_lead(
        form_id: str, account_id: str, field_data: list[dict[str, Any]] | None
    ) -> str:
        """Create a test lead

        Args:
            form_id: (required)
            account_id: (required)
            field_data: (required)"""
        client = _get_client()
        try:
            response = client.lead_gen.create_test_lead(
                form_id=form_id, account_id=account_id, field_data=field_data
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # LOGS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List activity logs",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def logs_list_logs(
        type: str = "publishing",
        status: str | None = None,
        platform: str | None = None,
        action: str | None = None,
        search: str | None = None,
        days: int = 90,
        limit: int = 50,
        skip: int = 0,
        account_id: str | None = None,
        event: str | None = None,
        request_id: str | None = None,
        from_: str | None = None,
        to: str | None = None,
        status_code: int | None = None,
        api_key_id: str | None = None,
        include_read_receipts: bool = False,
    ) -> str:
        """List activity logs

            Args:
                type: Log category to query. Use `all` for the unified view across every category,
        or `api_request` for your API request logs (method, path, status, latency).
                status: Filter by status
                platform: Filter by platform
                action: Filter by action (e.g., post.published, message.sent, account.connected, webhook.delivered)
                search: Free-text search across log fields
                days: Number of days to look back (max 90)
                limit: Maximum number of logs to return (max 100)
                skip: Number of logs to skip (for pagination)
                account_id: Filter by connected account ID
                event: Filter webhook logs by event (e.g. post.published, message.received)
                request_id: Correlation ID — returns every log spawned by a single API request
                from_: Precise start instant (ISO 8601); narrows within the day range
                to: Precise end instant (ISO 8601)
                status_code: Filter by exact HTTP status code (api_request logs)
                api_key_id: Filter by the API key that made the request (api_request logs)
                include_read_receipts: Include message.read / message.delivered events (hidden by default for messaging logs)"""
        client = _get_client()
        try:
            response = client.logs.list_logs(
                type=type,
                status=status,
                platform=platform,
                action=action,
                search=search,
                days=days,
                limit=limit,
                skip=skip,
                account_id=account_id,
                event=event,
                request_id=request_id,
                from_=from_,
                to=to,
                status_code=status_code,
                api_key_id=api_key_id,
                include_read_receipts=include_read_receipts,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # MEDIA

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get upload URL",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def media_get_media_presigned_url(
        filename: str, content_type: str, size: int | None = None
    ) -> str:
        """Get upload URL

        Args:
            filename: Name of the file to upload (required)
            content_type: MIME type of the file (required)
            size: Optional file size in bytes for pre-validation (max 5GB)"""
        client = _get_client()
        try:
            response = client.media.get_media_presigned_url(
                filename=filename, content_type=content_type, size=size
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # MENTIONS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List mentions",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def mentions_list_inbox_mentions(
        account_id: str | None = None,
        profile_id: str | None = None,
        sort_order: str = "desc",
        limit: int = 25,
        cursor: str | None = None,
    ) -> str:
        """List mentions

        Args:
            account_id: Filter by social account ID
            profile_id: Filter by profile ID
            sort_order: Sort order by publishedAt
            limit
            cursor: Cursor for pagination (ID of the last item from the previous page)"""
        client = _get_client()
        try:
            response = client.mentions.list_inbox_mentions(
                account_id=account_id,
                profile_id=profile_id,
                sort_order=sort_order,
                limit=limit,
                cursor=cursor,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Reply to a mention",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def mentions_reply_to_mention(
        account_id: str, media_id: str, message: str, comment_id: str | None = None
    ) -> str:
        """Reply to a mention

        Args:
            account_id: The Instagram social account ID (required)
            media_id: The ID of the media the account was mentioned in (required)
            comment_id: The mentioning comment's ID. Omit for a caption mention.
            message: The reply text (required)"""
        client = _get_client()
        try:
            response = client.mentions.reply_to_mention(
                account_id=account_id,
                media_id=media_id,
                comment_id=comment_id,
                message=message,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # MESSAGES

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List conversations",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def messages_list_inbox_conversations(
        profile_id: str | None = None,
        platform: str | None = None,
        status: str | None = None,
        sort_order: str = "desc",
        limit: int = 50,
        cursor: str | None = None,
        account_id: str | None = None,
    ) -> str:
        """List conversations

        Args:
            profile_id: Filter by profile ID
            platform: Filter by platform
            status: Filter by conversation status
            sort_order: Sort order by updated time
            limit: Maximum number of conversations to return
            cursor: Pagination cursor for next page
            account_id: Filter by specific social account ID"""
        client = _get_client()
        try:
            response = client.messages.list_inbox_conversations(
                profile_id=profile_id,
                platform=platform,
                status=status,
                sort_order=sort_order,
                limit=limit,
                cursor=cursor,
                account_id=account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create conversation",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def messages_create_inbox_conversation(
        account_id: str,
        participant_id: str | None = None,
        participant_username: str | None = None,
        message: str | None = None,
        skip_dm_check: bool = False,
        template_name: str | None = None,
        category: str | None = None,
        template_language: str | None = None,
        template_params: list[str] | None = None,
        header_media: dict[str, Any] | None = None,
    ) -> str:
        """Create conversation

        Args:
            account_id: The social account ID to send from (required)
            participant_id: Recipient identifier. For X this is the numeric user ID; for WhatsApp and SMS, the recipient phone number in international format (digits, country code included); for Slack, the workspace member id (e.g. U01ABCDEF). Provide either this or participantUsername.
            participant_username: Recipient handle/username — an X or Bluesky handle (with or without @) or a Reddit username (with or without u/). Resolved via lookup. Provide either this or participantId.
            message: Text content of the message. At least one of message, attachment, or (for WhatsApp) templateName is required. Required when category is set (a Direct Send utility message is a text message).
            skip_dm_check: X/Twitter only. Skip the receives_your_dm eligibility check before sending. Use if you have already verified the recipient accepts DMs.
            template_name: WhatsApp only. Name of the approved template to start the conversation with. Required for WhatsApp unless category is used instead (Direct Send). Cannot be combined with category.
            category: WhatsApp only (Meta Direct Send). Combined with message and without templateName, starts the conversation with a business-initiated UTILITY message and no pre-approved template; Meta matches or auto-creates a template asynchronously. The WhatsApp Business Account must be eligible for Direct Send, otherwise the send fails with an error telling you to use an approved message template instead. Cannot be combined with templateName (templates are already categorized at creation). Utility messages only; marketing content is not allowed under this category. Accepted on the JSON body only, not on multipart requests.
            template_language: WhatsApp only. Template language code (e.g. en_US).
            template_params: WhatsApp only. Template variable values as one flat array, in the order the variables appear across the whole template: text-header variables first, then body variables, then one value per dynamic URL button (in button order). Works with positional placeholders ({{1}}, {{2}}, ...) and with named placeholders ({{name}}, {{company}} - how Meta Business Manager creates templates), where values fill the named slots in order of appearance. Example - a body with {{1}}, {{2}} plus a URL button https://example.com/{{1}} takes three values: [body1, body2, buttonSuffix]. Media headers (image, video, document) are filled automatically from the approved template and take no value here (use headerMedia to override the header asset per send).
            header_media: WhatsApp only. Overrides a media-header template's header asset for THIS send, so a template with an image/video/document header can carry a different asset per message (e.g. each recipient their own invoice PDF). Without it, the template's approved sample asset is sent. Provide exactly one of link or id."""
        client = _get_client()
        try:
            response = client.messages.create_inbox_conversation(
                account_id=account_id,
                participant_id=participant_id,
                participant_username=participant_username,
                message=message,
                skip_dm_check=skip_dm_check,
                template_name=template_name,
                category=category,
                template_language=template_language,
                template_params=template_params,
                header_media=header_media,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Search conversations",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def messages_search_inbox_conversations(
        query: str,
        direction: str | None = None,
        profile_id: str | None = None,
        platform: str | None = None,
        account_id: str | None = None,
        limit: int = 20,
        cursor: str | None = None,
    ) -> str:
        """Search conversations

        Args:
            query: Text to search for, in message content and in the contact's name, username, or phone number (required)
            direction: Only match messages sent to you (incoming) or by you (outgoing). Contact-identity matching is not applied when this is set.
            profile_id: Filter by profile ID
            platform: Filter by platform (searchable platforms only)
            account_id: Filter by specific social account ID
            limit: Maximum number of conversations to return
            cursor: Pagination cursor for next page"""
        client = _get_client()
        try:
            response = client.messages.search_inbox_conversations(
                query=query,
                direction=direction,
                profile_id=profile_id,
                platform=platform,
                account_id=account_id,
                limit=limit,
                cursor=cursor,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get conversation",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def messages_get_inbox_conversation(conversation_id: str, account_id: str) -> str:
        """Get conversation

        Args:
            conversation_id: The conversation ID (id field from list conversations endpoint). This is the platform-specific conversation identifier, not an internal database ID. (required)
            account_id: The social account ID (required)"""
        client = _get_client()
        try:
            response = client.messages.get_inbox_conversation(
                conversation_id=conversation_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update conversation status",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def messages_update_inbox_conversation(
        conversation_id: str, account_id: str, status: str
    ) -> str:
        """Update conversation status

        Args:
            conversation_id: The conversation ID (id field from list conversations endpoint). This is the platform-specific conversation identifier, not an internal database ID. (required)
            account_id: Social account ID (required)
            status: (required)"""
        client = _get_client()
        try:
            response = client.messages.update_inbox_conversation(
                conversation_id=conversation_id, account_id=account_id, status=status
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List messages",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def messages_get_inbox_conversation_messages(
        conversation_id: str,
        account_id: str,
        limit: int = 100,
        cursor: str | None = None,
        sort_order: str = "asc",
    ) -> str:
        """List messages

            Args:
                conversation_id: The conversation ID (id field from list conversations endpoint). This is the platform-specific conversation identifier, not an internal database ID. (required)
                account_id: Social account ID (required)
                limit: Number of messages to return per page. Default 100, max 100.
                cursor: Opaque pagination cursor. Pass `pagination.nextCursor` from a prior response.
                sort_order: Order of returned messages. Default `asc` (oldest first, chat style).
        Twitter, Instagram, Telegram, WhatsApp and Reddit honor this order
        across cursor pages. For Facebook and Bluesky, only intra-page
        ordering is affected — pages always walk newest→oldest. See
        `sortOrderApplied` in the response."""
        client = _get_client()
        try:
            response = client.messages.get_inbox_conversation_messages(
                conversation_id=conversation_id,
                account_id=account_id,
                limit=limit,
                cursor=cursor,
                sort_order=sort_order,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Send message",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def messages_send_inbox_message(
        conversation_id: str,
        account_id: str,
        message: str | None = None,
        attachment_url: str | None = None,
        category: str | None = None,
        attachment_type: str | None = None,
        attachment_name: str | None = None,
        voice_note: bool | None = None,
        quick_replies: list[dict[str, Any]] | None = None,
        buttons: list[dict[str, Any]] | None = None,
        template: dict[str, Any] | None = None,
        interactive: dict[str, Any] | None = None,
        reply_markup: dict[str, Any] | None = None,
        messaging_type: str | None = None,
        message_tag: str | None = None,
        reply_to: str | None = None,
        location: dict[str, Any] | None = None,
        contacts: list[dict[str, Any]] | None = None,
    ) -> str:
        """Send message

            Args:
                conversation_id: Opaque conversation identifier, accepted verbatim from the list endpoint or from the conversationId on inbox webhooks. Format not to be assumed. (required)
                account_id: Social account ID (required)
                message: Message text
                attachment_url: URL of the attachment to send (image, video, audio, or file). The URL must be publicly accessible. For binary file uploads, use multipart/form-data instead. On WhatsApp, combining an image, video, or file with `buttons` renders the media as the header of one interactive reply-button message; audio cannot be combined with buttons.
                category: WhatsApp only (Meta Direct Send). Sends this message as a business-initiated UTILITY message without an approved template, for example outside the 24-hour customer service window; Meta matches or auto-creates a template asynchronously. The WhatsApp Business Account must be eligible for Direct Send, otherwise the send fails with an error telling you to use an approved message template instead. Supported only for text messages (link preview ok) and interactive messages (reply buttons, CTA URL buttons, voice-call button, header of text/image/video/document). Cannot be combined with template, attachments, location, or contacts. Utility messages only; marketing content is not allowed under this category. Accepted on the JSON body only, not on multipart requests.
                attachment_type: Type of attachment. Defaults to file if not specified.
                attachment_name: WhatsApp only. Display name for a document sent via attachmentUrl with attachmentType: file (e.g. "Report.pdf"). Maps to the recipient's file name; without it WhatsApp derives the name from the URL and shows "Untitled". Ignored for image/video/audio and for binary uploads (which use the uploaded file's name).
                voice_note: WhatsApp only. When `true` on an audio attachment, the message is sent
        as a voice message (PTT) — the recipient sees the waveform + voice-note
        UI instead of a basic audio attachment. The audio file MUST be `.ogg`
        encoded with the OPUS codec (mono) per Meta's voice-message contract;
        other formats are rejected by WhatsApp. Ignored for non-audio attachments.
                quick_replies: Quick reply buttons. Mutually exclusive with buttons. Max 13 items.
                buttons: Action buttons. Mutually exclusive with quickReplies. Max 3 items.

        Instagram / Facebook: also mutually exclusive with `template`.
        A Meta message carries one body shape, so sending both is a 400
        rather than a silent drop of the buttons.

        WhatsApp: buttons always render as interactive reply buttons.
        Only `title` and `payload` are used — `type`, `url`, and `phone`
        are ignored (WhatsApp has no URL/phone button in this field; use
        the `interactive` field with `type: cta_url` for a link button).
        `payload` becomes the button reply ID delivered on the
        `message.received` webhook when the user taps. To send a simple
        reply-button message, provide `title` + `payload` and set
        `type: postback`, e.g.
        `{ "type": "postback", "title": "Yes", "payload": "yes" }`.

        Combine `buttons` with `attachmentUrl` and `attachmentType`
        `image`, `video`, or `file` to render one WhatsApp message with
        a media header, body text, and reply buttons. Audio is not a
        supported interactive header and returns 400 when combined
        with buttons.
                template: Platform-dependent template payload. Ignored on Telegram.

        Instagram / Facebook: a generic template (carousel). Set `type: generic`
        and provide up to 10 `elements`, each with a `title` (required) and
        optional `subtitle`, `imageUrl`, and `buttons`. Mutually exclusive with
        the top-level `buttons` field (sending both is a 400); put the card's
        buttons on its `elements` instead.

        WhatsApp: sends an approved WhatsApp template message, the only message
        type WhatsApp accepts when the 24-hour customer-service window is closed.
        Provide exactly one element carrying the template reference:
        `{ "elements": [{ "name": "order_update", "language": "en_US", "components": [...] }] }`
        (`type` is ignored on WhatsApp). `components` is optional and is forwarded
        unchanged as the `template.components` array of Meta's Cloud API send
        payload; use it to fill body/header variables and button parameters, e.g.
        `[{ "type": "body", "parameters": [{ "type": "text", "text": "John" }] }]`.
        Templates with media headers (image, video, document) must include the
        header component with its media link here at send time. To send a template
        to a phone number with no existing conversation, or to have media headers
        filled in automatically from the template definition, use the
        create-conversation endpoint (POST /v1/inbox/conversations) instead.
                interactive: WhatsApp-only. Rich interactive payload for list messages, CTA URL
        buttons, Flow prompts, location requests, voice-call buttons, and
        commerce messages (single product, product list, catalog, and
        carousel). When set, takes priority over `buttons` and
        `quickReplies`. The shape mirrors Meta's Cloud API `interactive`
        object verbatim, so any payload that works against Meta directly
        will also work here.

        Use `buttons` / `quickReplies` for simple button replies
        (WhatsApp's `interactive.type: "button"`): the abstraction caps at
        3 buttons and handles the auto-conversion for you. Use this field
        only for the types listed in the enum below.

        All interactive messages are session messages: they can only be
        sent inside the 24-hour customer service window opened by the
        user's last inbound message.

        Commerce types (`product`, `product_list`, `catalog_message`, and
        product carousels) require a Meta catalog connected to the
        WhatsApp Business Account in Commerce Manager. Media carousels
        (image/video cards) do not need a catalog.

        For `product`, `body` is optional (WhatsApp renders the product
        card itself) and `header` is not allowed (the product image is
        the header). For `product_list`, a `header` with `type: "text"`
        is required. For `carousel`, top-level `header`/`footer` are not
        supported; media goes on each card instead.

        For `voice_call`, the message renders WhatsApp's native call
        button; tapping it starts a voice call to your business number.
        Requires WhatsApp Business Calling to be enabled on the sending
        number. The optional `parameters.payload` string is echoed back on
        the `calls` webhook (as `cta_payload`) for attribution.

        For `location_request_message`, `action` may be omitted (we default
        it to `{ "name": "send_location" }`). WhatsApp renders a localized
        "Send location" button; the user's reply arrives as a regular
        location message in the conversation.

        For `request_contact_info`, `action` may be omitted (we default it
        to `{ "name": "request_contact_info" }`). WhatsApp renders a
        localized share button that cannot be relabelled, so put the reason
        for asking in `body.text`: this is a consent prompt, and a bare
        request converts badly. The reply arrives as an inbound `contacts`
        message with `metadata.contactsOrigin` set to `contact_request`,
        and we fold the shared number back into the contact automatically.
        A `contacts` message with origin `other` is a card the user picked
        from their address book and is NOT proof of their own number.

        For `catalog_message`, `action` may also be omitted (we default it
        to `{ "name": "catalog_message" }`).

        Tap events come back via the `message.received` webhook with
        `metadata.interactiveType` set to `list_reply` or `nfm_reply`.
        Carts submitted from commerce messages arrive as `metadata.order`;
        product inquiries arrive as `metadata.referredProduct`.
                reply_markup: Telegram-native keyboard markup. Ignored on other platforms.
                messaging_type: Facebook messaging type. Required when using messageTag.
                message_tag: Facebook message tag for messaging outside 24h window. Requires messagingType MESSAGE_TAG. Instagram only supports HUMAN_AGENT.
                reply_to: Platform message ID to quote-reply to. For WhatsApp, pass the wamid; for Telegram, the Telegram message ID (both available in message.platformMessageId from webhooks or the list-messages endpoint). On Slack it threads the reply (thread_ts) instead of quoting. Silently ignored on platforms without send-side reply support, including Instagram and Facebook Messenger (Meta's Send API rejects reply_to on Instagram and does not expose it on Messenger).
                location: WhatsApp-only. Send a location pin.
                contacts: WhatsApp-only. Send one or more contact cards."""
        client = _get_client()
        try:
            response = client.messages.send_inbox_message(
                conversation_id=conversation_id,
                account_id=account_id,
                message=message,
                attachment_url=attachment_url,
                category=category,
                attachment_type=attachment_type,
                attachment_name=attachment_name,
                voice_note=voice_note,
                quick_replies=quick_replies,
                buttons=buttons,
                template=template,
                interactive=interactive,
                reply_markup=reply_markup,
                messaging_type=messaging_type,
                message_tag=message_tag,
                reply_to=reply_to,
                location=location,
                contacts=contacts,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Edit message",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def messages_edit_inbox_message(
        conversation_id: str,
        message_id: str,
        account_id: str,
        text: str | None = None,
        reply_markup: dict[str, Any] | None = None,
    ) -> str:
        """Edit message

        Args:
            conversation_id: The conversation ID (required)
            message_id: The Telegram message ID to edit (required)
            account_id: Social account ID (required)
            text: New message text
            reply_markup: New inline keyboard markup"""
        client = _get_client()
        try:
            response = client.messages.edit_inbox_message(
                conversation_id=conversation_id,
                message_id=message_id,
                account_id=account_id,
                text=text,
                reply_markup=reply_markup,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete message",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def messages_delete_inbox_message(
        conversation_id: str, message_id: str, account_id: str
    ) -> str:
        """Delete message

        Args:
            conversation_id: The conversation ID (required)
            message_id: The platform message ID to delete (required)
            account_id: Social account ID (required)"""
        client = _get_client()
        try:
            response = client.messages.delete_inbox_message(
                conversation_id=conversation_id,
                message_id=message_id,
                account_id=account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Send typing indicator",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def messages_send_typing_indicator(conversation_id: str, account_id: str) -> str:
        """Send typing indicator

        Args:
            conversation_id: The conversation ID (required)
            account_id: Social account ID (required)"""
        client = _get_client()
        try:
            response = client.messages.send_typing_indicator(
                conversation_id=conversation_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Mark a conversation as read",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def messages_mark_conversation_read(conversation_id: str, account_id: str) -> str:
        """Mark a conversation as read

        Args:
            conversation_id: The conversation ID (required)
            account_id: Social account ID (required)"""
        client = _get_client()
        try:
            response = client.messages.mark_conversation_read(
                conversation_id=conversation_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Add reaction",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def messages_add_message_reaction(
        conversation_id: str, message_id: str, account_id: str, emoji: str
    ) -> str:
        """Add reaction

        Args:
            conversation_id: The conversation ID (required)
            message_id: The platform message ID to react to (required)
            account_id: Social account ID (required)
            emoji: Emoji character (e.g. "👍", "❤️") (required)"""
        client = _get_client()
        try:
            response = client.messages.add_message_reaction(
                conversation_id=conversation_id,
                message_id=message_id,
                account_id=account_id,
                emoji=emoji,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Remove reaction",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def messages_remove_message_reaction(
        conversation_id: str, message_id: str, account_id: str
    ) -> str:
        """Remove reaction

        Args:
            conversation_id: The conversation ID (required)
            message_id: The platform message ID (required)
            account_id: Social account ID (required)"""
        client = _get_client()
        try:
            response = client.messages.remove_message_reaction(
                conversation_id=conversation_id,
                message_id=message_id,
                account_id=account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Upload media file",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def messages_upload_media_direct() -> str:
        """Upload media file"""
        client = _get_client()
        try:
            response = client.messages.upload_media_direct()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Resolve message attachment",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def messages_get_message_attachment(
        conversation_id: str,
        message_id: str,
        index: int,
        account_id: str,
        format: str = "redirect",
    ) -> str:
        """Resolve message attachment

        Args:
            conversation_id: The conversation ID (Zernio id or platform conversation id) (required)
            message_id: The message id as returned by the list-messages endpoint (the platform message id) (required)
            index: Zero-based position of the attachment in the message's attachments array (required)
            account_id: Social account ID (required)
            format: `redirect` (default) answers 302 to the media; `json` returns the url in the body"""
        client = _get_client()
        try:
            response = client.messages.get_message_attachment(
                conversation_id=conversation_id,
                message_id=message_id,
                index=index,
                account_id=account_id,
                format=format,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # MESSAGING_ADS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create click-to-message ad (WhatsApp / Messenger / Instagram Direct)",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def messaging_ads_create_messaging_ad() -> str:
        """Create click-to-message ad (WhatsApp / Messenger / Instagram Direct)"""
        client = _get_client()
        try:
            response = client.messaging_ads.create_messaging_ad()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create Click-to-Call ad",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def messaging_ads_create_call_ad() -> str:
        """Create Click-to-Call ad"""
        client = _get_client()
        try:
            response = client.messaging_ads.create_call_ad()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create Click-to-WhatsApp ad (deprecated)",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def messaging_ads_create_ctwa_ad() -> str:
        """Create Click-to-WhatsApp ad (deprecated)"""
        client = _get_client()
        try:
            response = client.messaging_ads.create_ctwa_ad()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # PHONE_NUMBERS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List phone numbers",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def phone_numbers_list_phone_numbers(
        status: str | None = None, profile_id: str | None = None
    ) -> str:
        """List phone numbers

            Args:
                status: Filter by status (by default excludes released numbers). NOTE:
        `status=pending_regulatory` returns the "provisioning" view — numbers
        still in review PLUS recently-declined (last 30 days) ones, so a
        failed registration surfaces (with `regulatoryDeclineReason`) instead
        of silently disappearing. Declined numbers can be re-submitted via
        POST /v1/phone-numbers/{id}/remediate. `verifying` is the
        short-lived state after the number is provisioned on our side while
        WhatsApp confirms the activation code; the number is not billed until
        it reaches `active`.
                profile_id: Filter by profile"""
        client = _get_client()
        try:
            response = client.phone_numbers.list_phone_numbers(
                status=status, profile_id=profile_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get phone number",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def phone_numbers_get_phone_number(id: str) -> str:
        """Get phone number

        Args:
            id: Phone number record ID (required)"""
        client = _get_client()
        try:
            response = client.phone_numbers.get_phone_number(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Release phone number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_release_phone_number(id: str) -> str:
        """Release phone number

        Args:
            id: Phone number record ID (required)"""
        client = _get_client()
        try:
            response = client.phone_numbers.release_phone_number(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Purchase phone number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_purchase_phone_number(
        profile_id: str,
        country: str = "US",
        number_type: str | None = None,
        area_code: str | None = None,
        connect_whatsapp: bool = True,
        wants_sms: bool = False,
        wants_whatsapp: bool = False,
        purchase_intent_id: str | None = None,
        allow_multiple: bool = False,
    ) -> str:
        """Purchase phone number

           Args:
               profile_id: Preferred profile for the number. One number = one profile, so when the requested profile already holds a number the API assigns the next free profile instead (or creates one) and returns the actual assignment in `profileId` on the response.
        (required)
               country: ISO 3166-1 alpha-2 country for the number (default US). International numbers require usage-based billing. Tier 3/4 countries return 202 { status: "kyc_required", kycUrl } — the customer must complete KYC at that URL before the number is ordered. See GET /v1/phone-numbers/countries.
               number_type: Which of the country's offered number types to order (see `types[]` on GET /v1/phone-numbers/countries). Omitted = the country's default type, which is always the WhatsApp-safe choice. Capabilities, price, and KYC requirements are per (country, type): toll_free can never connect WhatsApp (400 when combined with connectWhatsapp:true), and wantsSms:true requires an SMS-capable type.
               area_code: Area code (national destination code, e.g. 11 for Sao Paulo) the number must be in. Hard constraint: when the area has no deliverable inventory the purchase fails with 409 code AREA_CODE_UNAVAILABLE instead of assigning a number from another area, and later replacements stay in this area too. Omit for any area. Get live options from GET /v1/phone-numbers/availability (areaOptions).
               connect_whatsapp: A phone number is the unit; WhatsApp is one optional feature. Pass false to buy a STANDALONE number (Calls/SMS only): provisioning skips the Meta pre-verify/OTP steps and the number activates immediately. Omitted defaults to the WhatsApp provisioning path. WhatsApp can be connected to a standalone number later from the connect flow.
               wants_sms: SMS capability is per-number, not per-country. Pass true to provision from the SMS-capable inventory pool so the number can actually text (see also GET /v1/phone-numbers/available with sms=true, and smsAvailable on GET /v1/phone-numbers/countries).
               wants_whatsapp: Declare WhatsApp intent on a STANDALONE purchase (connectWhatsapp:false). The number still activates and bills immediately, but if WhatsApp's buy-time check rejects the assigned number, it is automatically swapped for a WhatsApp-eligible one during the purchase instead of being delivered with WhatsApp unavailable. Ignored on the WhatsApp provisioning path (connectWhatsapp omitted or true), which always delivers a WhatsApp-verified number.
               purchase_intent_id: Optional idempotency key. Send the same value when retrying a purchase: if a number was already bought under this key, the API returns { status: "already_purchased", numberId, phoneNumber, profileId } instead of provisioning a second number. Generate a fresh key for each genuinely new purchase.
               allow_multiple: Any second purchase within 10 minutes of a previous one is rejected with 409 code PURCHASE_VELOCITY as duplicate protection. Pass true to confirm the additional purchase is intentional (e.g. bulk provisioning)."""
        client = _get_client()
        try:
            response = client.phone_numbers.purchase_phone_number(
                profile_id=profile_id,
                country=country,
                number_type=number_type,
                area_code=area_code,
                connect_whatsapp=connect_whatsapp,
                wants_sms=wants_sms,
                wants_whatsapp=wants_whatsapp,
                purchase_intent_id=purchase_intent_id,
                allow_multiple=allow_multiple,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List offerable number countries",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def phone_numbers_list_phone_number_countries() -> str:
        """List offerable number countries"""
        client = _get_client()
        try:
            response = client.phone_numbers.list_phone_number_countries()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Search available numbers",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def phone_numbers_search_available_phone_numbers(
        country: str = "US",
        type: str | None = None,
        prefix: str | None = None,
        locality: str | None = None,
        contains: str | None = None,
        sms: bool | None = None,
        limit: int = 20,
    ) -> str:
        """Search available numbers

        Args:
            country
            type: Number type; defaults to the country's WhatsApp-safe type
            prefix: Area code
            locality: City
            contains: Pattern to match within the number
            sms: true narrows the pool to SMS-capable numbers. Each result still carries its full `features` list for per-number capability badging.
            limit"""
        client = _get_client()
        try:
            response = client.phone_numbers.search_available_phone_numbers(
                country=country,
                type=type,
                prefix=prefix,
                locality=locality,
                contains=contains,
                sms=sms,
                limit=limit,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Check country availability",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def phone_numbers_check_phone_number_availability(
        country: str, number_type: str | None = None, sms: bool | None = None
    ) -> str:
        """Check country availability

        Args:
            country: ISO-2 country code. (required)
            number_type: Check a specific offered type (stock and address constraints are per type). Omitted = the country's default type.
            sms: Pass true when the buyer wants SMS: availability, areas, and areaOptions then describe the SMS-capable pool (an SMS purchase orders from it), not the wider voice-only pool."""
        client = _get_client()
        try:
            response = client.phone_numbers.check_phone_number_availability(
                country=country, number_type=number_type, sms=sms
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get KYC form spec",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def phone_numbers_get_phone_number_kyc_form(
        country: str, number_type: str | None = None
    ) -> str:
        """Get KYC form spec

        Args:
            country: (required)
            number_type: Requirements and reuse eligibility are per (country, type). Omitted = the country's default type. Pass the same value on the POST."""
        client = _get_client()
        try:
            response = client.phone_numbers.get_phone_number_kyc_form(
                country=country, number_type=number_type
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Submit KYC",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_submit_phone_number_kyc(
        profile_id: str,
        country: str,
        submission_id: str | None = None,
        quantity: int = 1,
        reuse: bool | None = None,
        reuse_option_id: str | None = None,
        reuse_from: str | None = None,
        area_code: str | None = None,
        end_user_first_name: str | None = None,
        end_user_last_name: str | None = None,
        values: dict[str, Any] | None = None,
        documents: list[dict[str, Any]] | None = None,
        address: dict[str, Any] | None = None,
    ) -> str:
        """Submit KYC

        Args:
            profile_id: (required)
            country: (required)
            submission_id: Idempotency token for this submission attempt. A retry/double-submit with the same token returns the same number; omit and each call creates a new number.
            quantity: Provision several same-country numbers from one submission (1-5). The single verification covers all of them; each number is billed only when it activates. Numbers that fail to order are skipped (best-effort). With `areaCode`, a quantity above that area's live stock is rejected with a 400.
            reuse: Reuse a prior approved verification for this country (skips document/field collection; places the order immediately).
            reuse_option_id: Which reusable verification to use (GET reusable.options[].id). The unambiguous selection key. Omitted = the approved default. No match = 409.
            reuse_from: Legacy fallback for `reuseOptionId`: the source phone number (GET reusable.options[].fromPhoneNumber). Ambiguous when a number labels two verifications — prefer `reuseOptionId`. Omitted = the approved default. No match = 409.
            area_code: Area code (NDC) the number must be in. Hard constraint: an empty area pool fails with 409 code AREA_CODE_UNAVAILABLE instead of ordering from another area. Omit for any area. Options come from GET /v1/phone-numbers/availability (areaOptions); the purchase 202 kycUrl echoes the areaCode picked at purchase time so it can be passed here.
            end_user_first_name: End user's legal first name. Required when the country has an action/ID-verification (Onfido) requirement.
            end_user_last_name: End user's legal last name. Same condition as endUserFirstName.
            values: requirementId → textual value
            documents: One per document requirement. Each is EITHER inline base64 OR a `documentId` returned by POST /v1/phone-numbers/kyc/upload-document (use the upload endpoint for large files to stay under the request-size limit).
            address"""
        client = _get_client()
        try:
            response = client.phone_numbers.submit_phone_number_kyc(
                profile_id=profile_id,
                country=country,
                submission_id=submission_id,
                quantity=quantity,
                reuse=reuse,
                reuse_option_id=reuse_option_id,
                reuse_from=reuse_from,
                area_code=area_code,
                end_user_first_name=end_user_first_name,
                end_user_last_name=end_user_last_name,
                values=values,
                documents=documents,
                address=address,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="View a KYC document on file",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def phone_numbers_view_phone_number_kyc_document(document_id: str) -> str:
        """View a KYC document on file

        Args:
            document_id: The Telnyx document id (from `reusable.options[].details[].documentId`). (required)"""
        client = _get_client()
        try:
            response = client.phone_numbers.view_phone_number_kyc_document(
                document_id=document_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Upload a KYC document",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_upload_phone_number_kyc_document() -> str:
        """Upload a KYC document"""
        client = _get_client()
        try:
            response = client.phone_numbers.upload_phone_number_kyc_document()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Pre-validate KYC address",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_validate_phone_number_kyc_address(
        country: str,
        street_address: str,
        locality: str,
        postal_code: str,
        administrative_area: str | None = None,
    ) -> str:
        """Pre-validate KYC address

        Args:
            country: ISO 3166-1 alpha-2 country code. (required)
            street_address: (required)
            locality: City / town. (required)
            administrative_area: State / province / region. When omitted, the pre-check is skipped (the final submit still validates).
            postal_code: (required)"""
        client = _get_client()
        try:
            response = client.phone_numbers.validate_phone_number_kyc_address(
                country=country,
                street_address=street_address,
                locality=locality,
                administrative_area=administrative_area,
                postal_code=postal_code,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a hosted KYC link",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_create_phone_number_kyc_link(
        profile_id: str,
        country: str,
        area_code: str | None = None,
        branding: dict[str, Any] | None = None,
        redirect_url: str | None = None,
    ) -> str:
        """Create a hosted KYC link

            Args:
                profile_id: (required)
                country: ISO 3166-1 alpha-2 country code (must be a regulated/KYC country). (required)
                area_code: Area code (NDC) the eventual number must be in. Hard constraint carried by the link; the end customer filling the form makes no area choice. Options come from GET /v1/phone-numbers/availability (areaOptions).
                branding: Optional white-label of the hosted page the end customer sees.
                redirect_url: Where to send the end customer's browser after a successful
        submit. On completion Zernio appends `kyc=submitted` and
        `country=<ISO-2>` as query params. When omitted, the hosted
        page shows a built-in confirmation screen instead."""
        client = _get_client()
        try:
            response = client.phone_numbers.create_phone_number_kyc_link(
                profile_id=profile_id,
                country=country,
                area_code=area_code,
                branding=branding,
                redirect_url=redirect_url,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Port numbers in",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_create_phone_number_port_in(
        phone_numbers: list[str] | None,
        end_user: dict[str, Any] | None,
        loa_document_id: str,
        invoice_document_id: str,
        foc_datetime_requested: str | None = None,
        customer_reference: str | None = None,
        port_type: str = "full",
        requirements: list[dict[str, Any]] | None = None,
    ) -> str:
        """Port numbers in

            Args:
                phone_numbers: E.164 numbers to port in. (required)
                end_user: End-user / current-carrier account info that authorizes the port. The
        losing carrier matches every field against its records and rejects the
        whole port on a mismatch — enter values exactly as they appear on the
        carrier bill.
         (required)
                loa_document_id: Document id from POST /v1/phone-numbers/port-in/documents (kind=loa). (required)
                invoice_document_id: Document id from POST /v1/phone-numbers/port-in/documents (kind=invoice). (required)
                foc_datetime_requested: Requested port date; the carrier confirms the actual FOC later. US/CA default is one week out (shifted off weekends); international orders are scheduled into the carrier's next allowed porting window at or after this date.
                customer_reference
                port_type: Whether the losing account ports all its numbers (full) or keeps some (partial).
                requirements: Country-specific requirement values for international ports (from GET /v1/phone-numbers/port-in/requirements). Not needed for US/CA. The LOA and invoice requirements are satisfied automatically by loaDocumentId/invoiceDocumentId, and address-type requirements by the endUser service address."""
        client = _get_client()
        try:
            response = client.phone_numbers.create_phone_number_port_in(
                phone_numbers=phone_numbers,
                end_user=end_user,
                loa_document_id=loa_document_id,
                invoice_document_id=invoice_document_id,
                foc_datetime_requested=foc_datetime_requested,
                customer_reference=customer_reference,
                port_type=port_type,
                requirements=requirements,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List port-in orders",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def phone_numbers_list_phone_number_port_ins() -> str:
        """List port-in orders"""
        client = _get_client()
        try:
            response = client.phone_numbers.list_phone_number_port_ins()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Check portability",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_check_phone_number_portability(
        phone_numbers: list[str] | None,
    ) -> str:
        """Check portability

        Args:
            phone_numbers: E.164 numbers to check, e.g. +13035550000. (required)"""
        client = _get_client()
        try:
            response = client.phone_numbers.check_phone_number_portability(
                phone_numbers=phone_numbers
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Upload a porting document",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_upload_phone_number_port_in_document() -> str:
        """Upload a porting document"""
        client = _get_client()
        try:
            response = client.phone_numbers.upload_phone_number_port_in_document()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Country porting requirements",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def phone_numbers_get_phone_number_port_in_requirements(
        country: str, number_type: str = "local"
    ) -> str:
        """Country porting requirements

        Args:
            country: ISO country of the numbers being ported (a supported port-in country). (required)
            number_type: The portability check's phoneNumberType — requirements differ by type."""
        client = _get_client()
        try:
            response = client.phone_numbers.get_phone_number_port_in_requirements(
                country=country, number_type=number_type
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="A port-in order's pending requirements",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def phone_numbers_get_phone_number_port_in_order_requirements(id: str) -> str:
        """A port-in order's pending requirements

        Args:
            id: Porting order ID (from the port-in list). (required)"""
        client = _get_client()
        try:
            response = client.phone_numbers.get_phone_number_port_in_order_requirements(
                id=id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Cancel a port-in",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_cancel_phone_number_port_in(id: str) -> str:
        """Cancel a port-in

        Args:
            id: Porting order ID (from the port-in list). (required)"""
        client = _get_client()
        try:
            response = client.phone_numbers.cancel_phone_number_port_in(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Pre-review a KYC packet",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_review_phone_number_kyc_packet(
        country: str,
        number_type: str,
        docs: list[dict[str, Any]] | None,
        values: dict[str, Any] | None = None,
        address: dict[str, Any] | None = None,
    ) -> str:
        """Pre-review a KYC packet

        Args:
            country: (required)
            number_type: (required)
            values: requirementId to declared textual value.
            address: Declared address (street_address, locality, ...), so a mismatched proof-of-address can be flagged.
            docs: (required)"""
        client = _get_client()
        try:
            response = client.phone_numbers.review_phone_number_kyc_packet(
                country=country,
                number_type=number_type,
                values=values,
                address=address,
                docs=docs,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get declined requirements",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def phone_numbers_get_phone_number_remediation(id: str) -> str:
        """Get declined requirements

        Args:
            id: Phone number record ID. (required)"""
        client = _get_client()
        try:
            response = client.phone_numbers.get_phone_number_remediation(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Resubmit a declined number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_remediate_phone_number(
        id: str,
        values: dict[str, Any] | None = None,
        documents: list[dict[str, Any]] | None = None,
        address: dict[str, Any] | None = None,
    ) -> str:
        """Resubmit a declined number

        Args:
            id: (required)
            values
            documents
            address: Same shape as the KYC submit address."""
        client = _get_client()
        try:
            response = client.phone_numbers.remediate_phone_number(
                id=id, values=values, documents=documents, address=address
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Reply to the regulatory reviewer",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_reply_to_phone_number_reviewer(
        id: str,
        text: str | None = None,
        attachments: list[dict[str, Any]] | None = None,
    ) -> str:
        """Reply to the regulatory reviewer

        Args:
            id: (required)
            text: The reply message to the reviewer.
            attachments: Files (PDF/JPG/PNG/WEBP, max 10 MB each) whose links are added to the reply."""
        client = _get_client()
        try:
            response = client.phone_numbers.reply_to_phone_number_reviewer(
                id=id, text=text, attachments=attachments
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Respond to the regulatory reviewer (message + corrections)",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def phone_numbers_respond_to_phone_number_reviewer(
        id: str,
        message: str | None = None,
        documents: list[dict[str, Any]] | None = None,
        address: dict[str, Any] | None = None,
        entity_type: str | None = None,
        attachments: list[dict[str, Any]] | None = None,
    ) -> str:
        """Respond to the regulatory reviewer (message + corrections)

        Args:
            id: (required)
            message: Your message to the reviewer.
            documents: Corrected requirement documents, each keyed to its requirement.
            address: A corrected address record, keyed to its requirement.
            entity_type
            attachments: Loose files (PDF/JPG/PNG/WEBP, max 10 MB each) whose links are added to your message."""
        client = _get_client()
        try:
            response = client.phone_numbers.respond_to_phone_number_reviewer(
                id=id,
                message=message,
                documents=documents,
                address=address,
                entity_type=entity_type,
                attachments=attachments,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # POSTS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List posts",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def posts_list_posts(
        page: int = 1,
        limit: int = 10,
        source: str = "zernio",
        status: str | None = None,
        platform: str | None = None,
        profile_id: str | None = None,
        created_by: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        include_hidden: bool = False,
        search: str | None = None,
        sort_by: str = "scheduled-desc",
        account_id: str | None = None,
    ) -> str:
        """List posts

        Args:
            page: Page number
            limit: Page size. Values above the maximum return 400 rather than being clamped.
            source: Which collection to read. `zernio` (default) returns posts authored through Zernio. `external` returns posts synced from the platform (existing/historical posts that were published outside Zernio). Combine with `accountId` and paginate via `page`/`limit` to walk the full synced history (we keep up to the last ~12 months per account).
            status
            platform
            profile_id: Filter posts to a specific profile (24-char hex ObjectId). Omit it, or send `all` or an empty value, to list posts across every profile.
            created_by: Filter posts to those created by a specific team user (24-char hex ObjectId).
            date_from: Zero-padded YYYY-MM-DD, or a full ISO 8601 datetime. An empty value means no date filter; any other malformed value returns 400.
            date_to: Zero-padded YYYY-MM-DD, or a full ISO 8601 datetime. An empty value means no date filter; any other malformed value returns 400.
            include_hidden
            search: Search posts by text content.
            sort_by: Sort order for results.
            account_id: Filter posts to those published via a specific social account (24-char hex ObjectId)."""
        client = _get_client()
        try:
            response = client.posts.list_posts(
                page=page,
                limit=limit,
                source=source,
                status=status,
                platform=platform,
                profile_id=profile_id,
                created_by=created_by,
                date_from=date_from,
                date_to=date_to,
                include_hidden=include_hidden,
                search=search,
                sort_by=sort_by,
                account_id=account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create post",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def posts_create_post(
        title: str | None = None,
        content: str | None = None,
        media_items: list[dict[str, Any]] | None = None,
        platforms: list[dict[str, Any]] | None = None,
        scheduled_for: str | None = None,
        publish_now: bool = False,
        is_draft: bool = False,
        timezone: str = "UTC",
        tags: list[str] | None = None,
        hashtags: list[str] | None = None,
        mentions: list[str] | None = None,
        crossposting_enabled: bool = True,
        metadata: dict[str, Any] | None = None,
        tiktok_settings: dict[str, Any] | None = None,
        facebook_settings: dict[str, Any] | None = None,
        recycling: dict[str, Any] | None = None,
        queued_from_profile: str | None = None,
        queue_id: str | None = None,
    ) -> str:
        """Create post

            Args:
                title
                content: Post caption/text. Optional when media is attached or all platforms have customContent. Required for text-only posts.
                media_items
                platforms: Target platforms and accounts for this post. Required for non-draft posts (returns 400 if empty). Drafts can omit platforms.
                scheduled_for
                publish_now
                is_draft: When true, saves the post as a draft. When none of scheduledFor, publishNow, or queuedFromProfile are provided, the post defaults to draft automatically.
                timezone
                tags: Tags/keywords. YouTube constraints: each tag max 100 chars, combined max 500 chars, duplicates auto-removed.
                hashtags
                mentions: Stored for reference only. This field does NOT automatically create @mentions when publishing. For LinkedIn @mentions, use the /v1/accounts/{accountId}/linkedin-mentions endpoint to resolve profile URLs to URNs, then embed the returned mentionFormat directly in the post content field.
                crossposting_enabled
                metadata
                tiktok_settings: Root-level TikTok settings applied to the TikTok platforms sent in the same request. Merged into each platform's platformSpecificData, with platform-specific settings taking precedence.
                facebook_settings: Root-level Facebook settings applied to the Facebook platforms sent in the same request. Merged into each platform's platformSpecificData.facebookSettings, with platform-specific settings taking precedence.
                recycling
                queued_from_profile: Profile ID to schedule via queue. When provided without scheduledFor, the post is auto-assigned to the next available slot. Do not call /v1/queue/next-slot and use that time in scheduledFor, as that bypasses queue locking.
                queue_id: Specific queue ID to use when scheduling via queue.
        Only used when queuedFromProfile is also provided.
        If omitted, uses the profile's default queue."""
        client = _get_client()
        try:
            response = client.posts.create_post(
                title=title,
                content=content,
                media_items=media_items,
                platforms=platforms,
                scheduled_for=scheduled_for,
                publish_now=publish_now,
                is_draft=is_draft,
                timezone=timezone,
                tags=tags,
                hashtags=hashtags,
                mentions=mentions,
                crossposting_enabled=crossposting_enabled,
                metadata=metadata,
                tiktok_settings=tiktok_settings,
                facebook_settings=facebook_settings,
                recycling=recycling,
                queued_from_profile=queued_from_profile,
                queue_id=queue_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get post",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def posts_get_post(post_id: str) -> str:
        """Get post

        Args:
            post_id: (required)"""
        client = _get_client()
        try:
            response = client.posts.get_post(post_id=post_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update post",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def posts_update_post(
        post_id: str,
        title: str | None = None,
        content: str | None = None,
        media_items: list[dict[str, Any]] | None = None,
        platforms: list[dict[str, Any]] | None = None,
        scheduled_for: str | None = None,
        publish_now: bool = False,
        is_draft: bool | None = None,
        timezone: str | None = None,
        visibility: str | None = None,
        tags: list[str] | None = None,
        hashtags: list[str] | None = None,
        mentions: list[str] | None = None,
        crossposting_enabled: bool | None = None,
        metadata: dict[str, Any] | None = None,
        queued_from_profile: str | None = None,
        queue_id: str | None = None,
        tiktok_settings: dict[str, Any] | None = None,
        facebook_settings: dict[str, Any] | None = None,
        recycling: dict[str, Any] | None = None,
    ) -> str:
        """Update post

        Args:
            post_id: (required)
            title
            content
            media_items
            platforms: Target platforms and accounts for this post. Each item must include platform and accountId.
            scheduled_for
            publish_now
            is_draft: When omitted, the post keeps its current draft status. Send `false` to promote a draft to scheduled (combined with `scheduledFor`, `publishNow`, or a queue).
            timezone
            visibility
            tags
            hashtags
            mentions
            crossposting_enabled
            metadata
            queued_from_profile: Profile ID to schedule via queue.
            queue_id: Specific queue ID to use when scheduling via queue.
            tiktok_settings: Root-level TikTok settings applied to the TikTok platforms sent in the same request. Merged into each platform's platformSpecificData, with platform-specific settings taking precedence. Returns 400 if sent without a platforms array.
            facebook_settings: Root-level Facebook settings applied to the Facebook platforms sent in the same request. Merged into each platform's platformSpecificData.facebookSettings, with platform-specific settings taking precedence. Returns 400 if sent without a platforms array.
            recycling"""
        client = _get_client()
        try:
            response = client.posts.update_post(
                post_id=post_id,
                title=title,
                content=content,
                media_items=media_items,
                platforms=platforms,
                scheduled_for=scheduled_for,
                publish_now=publish_now,
                is_draft=is_draft,
                timezone=timezone,
                visibility=visibility,
                tags=tags,
                hashtags=hashtags,
                mentions=mentions,
                crossposting_enabled=crossposting_enabled,
                metadata=metadata,
                queued_from_profile=queued_from_profile,
                queue_id=queue_id,
                tiktok_settings=tiktok_settings,
                facebook_settings=facebook_settings,
                recycling=recycling,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete post",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def posts_delete_post(post_id: str) -> str:
        """Delete post

        Args:
            post_id: (required)"""
        client = _get_client()
        try:
            response = client.posts.delete_post(post_id=post_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Bulk upload from CSV",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def posts_bulk_upload_posts(dry_run: bool = False) -> str:
        """Bulk upload from CSV

        Args:
            dry_run"""
        client = _get_client()
        try:
            response = client.posts.bulk_upload_posts(dry_run=dry_run)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Unpublish post",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def posts_unpublish_post(post_id: str, platform: str) -> str:
        """Unpublish post

        Args:
            post_id: (required)
            platform: The platform to delete the post from (required)"""
        client = _get_client()
        try:
            response = client.posts.unpublish_post(post_id=post_id, platform=platform)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Edit published post",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def posts_edit_post(post_id: str, platform: str, content: str) -> str:
        """Edit published post

        Args:
            post_id: (required)
            platform: The platform to edit the post on. (required)
            content: The new post text content (required)"""
        client = _get_client()
        try:
            response = client.posts.edit_post(
                post_id=post_id, platform=platform, content=content
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update post metadata",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def posts_update_post_metadata(
        post_id: str,
        platform: str,
        video_id: str | None = None,
        account_id: str | None = None,
        title: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        category_id: str | None = None,
        privacy_status: str | None = None,
        thumbnail_url: str | None = None,
        made_for_kids: bool | None = None,
        contains_synthetic_media: bool | None = None,
        playlist_id: str | None = None,
    ) -> str:
        """Update post metadata

        Args:
            post_id: Zernio post ID, or "_" when using direct video ID mode (required)
            platform: The platform to update metadata on (required)
            video_id: YouTube video ID (required for direct mode, ignored for post-based mode)
            account_id: Zernio social account ID (required for direct mode, ignored for post-based mode)
            title: New video title (max 100 characters for YouTube)
            description: New video description
            tags: Array of keyword tags (max 500 characters combined for YouTube)
            category_id: YouTube video category ID
            privacy_status: Video privacy setting
            thumbnail_url: Public URL of a custom thumbnail image (JPEG, PNG, or GIF, max 2 MB, recommended 1280x720). Works on any video you own, including existing videos not published through Zernio. The channel must be verified (phone verification) to set custom thumbnails.
            made_for_kids: COPPA compliance flag. Set true for child-directed content (restricts comments, notifications, ad targeting).
            contains_synthetic_media: AI-generated content disclosure. Set true if the video contains synthetic content that could be mistaken for real. YouTube may add a label.
            playlist_id: YouTube playlist ID to add the video to (e.g. 'PLxxxxxxxxxxxxx'). Use GET /v1/accounts/{id}/youtube-playlists to list available playlists. Only playlists owned by the channel are supported."""
        client = _get_client()
        try:
            response = client.posts.update_post_metadata(
                post_id=post_id,
                platform=platform,
                video_id=video_id,
                account_id=account_id,
                title=title,
                description=description,
                tags=tags,
                category_id=category_id,
                privacy_status=privacy_status,
                thumbnail_url=thumbnail_url,
                made_for_kids=made_for_kids,
                contains_synthetic_media=contains_synthetic_media,
                playlist_id=playlist_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # PROFILES

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List profiles",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def profiles_list_profiles(
        include_over_limit: bool = False,
        name: str | None = None,
        limit: int | None = None,
        skip: int | None = None,
    ) -> str:
        """List profiles

        Args:
            include_over_limit: When true, includes over-limit profiles (marked with isOverLimit: true).
            name: Exact-match filter on the profile name. Useful to recover a profile id after an ambiguous create (timeout followed by a 409 on retry).
            limit: Page size. When limit or skip is present, the response includes total and skip (and echoes limit).
            skip: Number of profiles to skip, applied after sorting and filtering."""
        client = _get_client()
        try:
            response = client.profiles.list_profiles(
                include_over_limit=include_over_limit, name=name, limit=limit, skip=skip
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create profile",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def profiles_create_profile(
        name: str, description: str | None = None, color: str | None = None
    ) -> str:
        """Create profile

        Args:
            name: (required)
            description
            color"""
        client = _get_client()
        try:
            response = client.profiles.create_profile(
                name=name, description=description, color=color
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get profile",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def profiles_get_profile(profile_id: str) -> str:
        """Get profile

        Args:
            profile_id: (required)"""
        client = _get_client()
        try:
            response = client.profiles.get_profile(profile_id=profile_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update profile",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def profiles_update_profile(
        profile_id: str,
        name: str | None = None,
        description: str | None = None,
        color: str | None = None,
        is_default: bool | None = None,
    ) -> str:
        """Update profile

        Args:
            profile_id: (required)
            name
            description
            color
            is_default"""
        client = _get_client()
        try:
            response = client.profiles.update_profile(
                profile_id=profile_id,
                name=name,
                description=description,
                color=color,
                is_default=is_default,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete profile",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def profiles_delete_profile(profile_id: str) -> str:
        """Delete profile

        Args:
            profile_id: (required)"""
        client = _get_client()
        try:
            response = client.profiles.delete_profile(profile_id=profile_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # QUEUE

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List schedules",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def queue_list_queue_slots(
        profile_id: str, queue_id: str | None = None, all: str | None = None
    ) -> str:
        """List schedules

        Args:
            profile_id: Profile ID to get queues for (required)
            queue_id: Specific queue ID to retrieve (optional)
            all: Set to 'true' to list all queues for the profile"""
        client = _get_client()
        try:
            response = client.queue.list_queue_slots(
                profile_id=profile_id, queue_id=queue_id, all=all
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create schedule",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def queue_create_queue_slot(
        profile_id: str,
        name: str,
        timezone: str,
        slots: list[dict[str, Any]] | None,
        active: bool = True,
    ) -> str:
        """Create schedule

        Args:
            profile_id: Profile ID (required)
            name: Queue name (e.g., Evening Posts) (required)
            timezone: IANA timezone (required)
            slots: (required)
            active"""
        client = _get_client()
        try:
            response = client.queue.create_queue_slot(
                profile_id=profile_id,
                name=name,
                timezone=timezone,
                slots=slots,
                active=active,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update schedule",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def queue_update_queue_slot(
        profile_id: str,
        timezone: str,
        slots: list[dict[str, Any]] | None,
        queue_id: str | None = None,
        name: str | None = None,
        active: bool = True,
        set_as_default: bool | None = None,
        reshuffle_existing: bool = False,
    ) -> str:
        """Update schedule

        Args:
            profile_id: (required)
            queue_id: Queue ID to update (optional)
            name: Queue name
            timezone: (required)
            slots: (required)
            active
            set_as_default: Make this queue the default
            reshuffle_existing: Whether to reschedule existing queued posts to match new slots"""
        client = _get_client()
        try:
            response = client.queue.update_queue_slot(
                profile_id=profile_id,
                queue_id=queue_id,
                name=name,
                timezone=timezone,
                slots=slots,
                active=active,
                set_as_default=set_as_default,
                reshuffle_existing=reshuffle_existing,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete schedule",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def queue_delete_queue_slot(profile_id: str, queue_id: str | None = None) -> str:
        """Delete schedule

        Args:
            profile_id: (required)
            queue_id: Queue ID to delete. Omit to delete all queues for the profile"""
        client = _get_client()
        try:
            response = client.queue.delete_queue_slot(
                profile_id=profile_id, queue_id=queue_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Preview upcoming slots",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def queue_preview_queue(
        profile_id: str, queue_id: str | None = None, count: int = 20
    ) -> str:
        """Preview upcoming slots

        Args:
            profile_id: (required)
            queue_id: Filter by specific queue ID. Omit to use the default queue.
            count"""
        client = _get_client()
        try:
            response = client.queue.preview_queue(
                profile_id=profile_id, queue_id=queue_id, count=count
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get next available slot",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def queue_get_next_queue_slot(profile_id: str, queue_id: str | None = None) -> str:
        """Get next available slot

        Args:
            profile_id: (required)
            queue_id: Specific queue ID (optional, defaults to profile's default queue)"""
        client = _get_client()
        try:
            response = client.queue.get_next_queue_slot(
                profile_id=profile_id, queue_id=queue_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # REACH_AND_FREQUENCY

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a Reach & Frequency prediction",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def reach_and_frequency_create_rf_prediction(
        account_id: str,
        ad_account_id: str,
        start_date: str,
        end_date: str,
        budget_amount: float | None = None,
        reach: int | None = None,
        frequency_cap: int | None = None,
        targeting: dict[str, Any] | None = None,
        placements: dict[str, Any] | None = None,
    ) -> str:
        """Create a Reach & Frequency prediction

        Args:
            account_id: Zernio SocialAccount id (posting or ads variant). (required)
            ad_account_id: Meta ad account id (act_<n>). (required)
            budget_amount: Whole currency units. Exactly one of budgetAmount / reach.
            reach: Target unique reach. Exactly one of budgetAmount / reach.
            start_date: Campaign window start (must be in the future). (required)
            end_date: (required)
            frequency_cap: Max impressions per person over the window.
            targeting: Canonical camelCase TargetingSpec (same shape as /v1/ads/create's `targeting`). Defaults to countries: [US].
            placements: Meta placements object (same shape as /v1/ads/create's `placements`)."""
        client = _get_client()
        try:
            response = client.reach_and_frequency.create_rf_prediction(
                account_id=account_id,
                ad_account_id=ad_account_id,
                budget_amount=budget_amount,
                reach=reach,
                start_date=start_date,
                end_date=end_date,
                frequency_cap=frequency_cap,
                targeting=targeting,
                placements=placements,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Read a Reach & Frequency prediction",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def reach_and_frequency_get_rf_prediction(
        prediction_id: str, account_id: str, ad_account_id: str
    ) -> str:
        """Read a Reach & Frequency prediction

        Args:
            prediction_id: (required)
            account_id: (required)
            ad_account_id: (required)"""
        client = _get_client()
        try:
            response = client.reach_and_frequency.get_rf_prediction(
                prediction_id=prediction_id,
                account_id=account_id,
                ad_account_id=ad_account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Cancel a Reach & Frequency reservation",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def reach_and_frequency_cancel_rf_reservation(
        prediction_id: str, account_id: str, ad_account_id: str
    ) -> str:
        """Cancel a Reach & Frequency reservation

        Args:
            prediction_id: (required)
            account_id: (required)
            ad_account_id: (required)"""
        client = _get_client()
        try:
            response = client.reach_and_frequency.cancel_rf_reservation(
                prediction_id=prediction_id,
                account_id=account_id,
                ad_account_id=ad_account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Reserve a Reach & Frequency prediction",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def reach_and_frequency_reserve_rf_prediction(
        prediction_id: str, account_id: str, ad_account_id: str
    ) -> str:
        """Reserve a Reach & Frequency prediction

        Args:
            prediction_id: (required)
            account_id: (required)
            ad_account_id: (required)"""
        client = _get_client()
        try:
            response = client.reach_and_frequency.reserve_rf_prediction(
                prediction_id=prediction_id,
                account_id=account_id,
                ad_account_id=ad_account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # REDDIT

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Search posts",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def reddit_search_reddit(
        account_id: str,
        q: str,
        subreddit: str | None = None,
        restrict_sr: str | None = None,
        sort: str = "new",
        limit: int = 25,
        after: str | None = None,
    ) -> str:
        """Search posts

        Args:
            account_id: (required)
            subreddit
            q: (required)
            restrict_sr
            sort
            limit
            after"""
        client = _get_client()
        try:
            response = client.reddit.search_reddit(
                account_id=account_id,
                subreddit=subreddit,
                q=q,
                restrict_sr=restrict_sr,
                sort=sort,
                limit=limit,
                after=after,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get subreddit feed",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def reddit_get_reddit_feed(
        account_id: str,
        subreddit: str | None = None,
        sort: str = "hot",
        limit: int = 25,
        after: str | None = None,
        t: str | None = None,
    ) -> str:
        """Get subreddit feed

        Args:
            account_id: (required)
            subreddit
            sort
            limit
            after
            t"""
        client = _get_client()
        try:
            response = client.reddit.get_reddit_feed(
                account_id=account_id,
                subreddit=subreddit,
                sort=sort,
                limit=limit,
                after=after,
                t=t,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # REVIEWS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List reviews",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def reviews_list_inbox_reviews(
        profile_id: str | None = None,
        platform: str | None = None,
        min_rating: int | None = None,
        max_rating: int | None = None,
        has_reply: bool | None = None,
        sort_by: str = "date",
        sort_order: str = "desc",
        limit: int = 25,
        cursor: str | None = None,
        account_id: str | None = None,
    ) -> str:
        """List reviews

        Args:
            profile_id
            platform
            min_rating
            max_rating
            has_reply: Filter by reply status
            sort_by
            sort_order
            limit
            cursor
            account_id: Filter by specific social account ID"""
        client = _get_client()
        try:
            response = client.reviews.list_inbox_reviews(
                profile_id=profile_id,
                platform=platform,
                min_rating=min_rating,
                max_rating=max_rating,
                has_reply=has_reply,
                sort_by=sort_by,
                sort_order=sort_order,
                limit=limit,
                cursor=cursor,
                account_id=account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Reply to review",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def reviews_reply_to_inbox_review(
        review_id: str, account_id: str, message: str
    ) -> str:
        """Reply to review

        Args:
            review_id: Review ID (URL-encoded for Google Business) (required)
            account_id: (required)
            message: (required)"""
        client = _get_client()
        try:
            response = client.reviews.reply_to_inbox_review(
                review_id=review_id, account_id=account_id, message=message
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete review reply",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def reviews_delete_inbox_review_reply(review_id: str, account_id: str) -> str:
        """Delete review reply

        Args:
            review_id: (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.reviews.delete_inbox_review_reply(
                review_id=review_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # SEQUENCES

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List sequences",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def sequences_list_sequences(
        profile_id: str | None = None,
        status: str | None = None,
        limit: int = 50,
        skip: int = 0,
    ) -> str:
        """List sequences

        Args:
            profile_id: Filter by profile. Omit to list across all profiles
            status
            limit
            skip"""
        client = _get_client()
        try:
            response = client.sequences.list_sequences(
                profile_id=profile_id, status=status, limit=limit, skip=skip
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create sequence",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sequences_create_sequence(
        profile_id: str,
        account_id: str,
        platform: str,
        name: str,
        description: str | None = None,
        steps: list[dict[str, Any]] | None = None,
        exit_on_reply: bool = True,
        exit_on_unsubscribe: bool = True,
    ) -> str:
        """Create sequence

        Args:
            profile_id: (required)
            account_id: (required)
            platform: (required)
            name: (required)
            description
            steps
            exit_on_reply
            exit_on_unsubscribe"""
        client = _get_client()
        try:
            response = client.sequences.create_sequence(
                profile_id=profile_id,
                account_id=account_id,
                platform=platform,
                name=name,
                description=description,
                steps=steps,
                exit_on_reply=exit_on_reply,
                exit_on_unsubscribe=exit_on_unsubscribe,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get sequence with steps",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def sequences_get_sequence(sequence_id: str) -> str:
        """Get sequence with steps

        Args:
            sequence_id: (required)"""
        client = _get_client()
        try:
            response = client.sequences.get_sequence(sequence_id=sequence_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update sequence",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sequences_update_sequence(
        sequence_id: str,
        name: str | None = None,
        description: str | None = None,
        steps: list[dict[str, Any]] | None = None,
        exit_on_reply: bool | None = None,
        exit_on_unsubscribe: bool | None = None,
    ) -> str:
        """Update sequence

        Args:
            sequence_id: (required)
            name
            description
            steps: Replace the full step list. Only allowed while the sequence is draft or paused.
            exit_on_reply
            exit_on_unsubscribe"""
        client = _get_client()
        try:
            response = client.sequences.update_sequence(
                sequence_id=sequence_id,
                name=name,
                description=description,
                steps=steps,
                exit_on_reply=exit_on_reply,
                exit_on_unsubscribe=exit_on_unsubscribe,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete sequence",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sequences_delete_sequence(sequence_id: str) -> str:
        """Delete sequence

        Args:
            sequence_id: (required)"""
        client = _get_client()
        try:
            response = client.sequences.delete_sequence(sequence_id=sequence_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Activate sequence",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sequences_activate_sequence(sequence_id: str) -> str:
        """Activate sequence

        Args:
            sequence_id: (required)"""
        client = _get_client()
        try:
            response = client.sequences.activate_sequence(sequence_id=sequence_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Pause sequence",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sequences_pause_sequence(sequence_id: str) -> str:
        """Pause sequence

        Args:
            sequence_id: (required)"""
        client = _get_client()
        try:
            response = client.sequences.pause_sequence(sequence_id=sequence_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Enroll contacts in a sequence",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sequences_enroll_contacts(
        sequence_id: str,
        contact_ids: list[str] | None,
        channel_ids: list[str] | None = None,
    ) -> str:
        """Enroll contacts in a sequence

        Args:
            sequence_id: (required)
            contact_ids: (required)
            channel_ids: Optional. Auto-detected if not provided."""
        client = _get_client()
        try:
            response = client.sequences.enroll_contacts(
                sequence_id=sequence_id,
                contact_ids=contact_ids,
                channel_ids=channel_ids,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Unenroll contact",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sequences_unenroll_contact(sequence_id: str, contact_id: str) -> str:
        """Unenroll contact

        Args:
            sequence_id: (required)
            contact_id: (required)"""
        client = _get_client()
        try:
            response = client.sequences.unenroll_contact(
                sequence_id=sequence_id, contact_id=contact_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List enrollments for a sequence",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def sequences_list_sequence_enrollments(
        sequence_id: str, status: str | None = None, limit: int = 50, skip: int = 0
    ) -> str:
        """List enrollments for a sequence

        Args:
            sequence_id: (required)
            status
            limit
            skip"""
        client = _get_client()
        try:
            response = client.sequences.list_sequence_enrollments(
                sequence_id=sequence_id, status=status, limit=limit, skip=skip
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # SLACK

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Slack workspace members",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def slack_list_slack_members(
        account_id: str, query: str | None = None, limit: int = 50
    ) -> str:
        """List Slack workspace members

        Args:
            account_id: (required)
            query: Case-insensitive filter over display name and handle.
            limit"""
        client = _get_client()
        try:
            response = client.slack.list_slack_members(
                account_id=account_id, query=query, limit=limit
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # SMS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Send an SMS/MMS",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_send_sms(
        from_: str,
        to: str,
        text: str | None = None,
        media_urls: list[str] | None = None,
        send_at: str | None = None,
    ) -> str:
        """Send an SMS/MMS

        Args:
            from_: One of your SMS-enabled numbers (E.164; formatting is normalized). (required)
            to: Recipient number (E.164). (required)
            text: Message body. Required unless `mediaUrls` is set. Max 10 SMS segments (1530 GSM-7 or 670 unicode characters).
            media_urls: Public media URLs to attach (sends as MMS). Max 10.
            send_at: Optional. Schedule the send for a future time (ISO 8601 with offset, e.g. `2026-08-01T12:00:00Z`). Must be in the future. The message is queued and the `message.delivered` webhook fires when it actually sends."""
        client = _get_client()
        try:
            response = client.sms.send_sms(
                from_=from_, to=to, text=text, media_urls=media_urls, send_at=send_at
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Look up carrier + line type",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def sms_lookup_sms_number(number: str) -> str:
        """Look up carrier + line type

        Args:
            number: Number to look up (E.164; formatting is normalized). (required)"""
        client = _get_client()
        try:
            response = client.sms.lookup_sms_number(number=number)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List SMS opt-outs",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def sms_list_sms_opt_outs(format: str = "json", limit: int = 500) -> str:
        """List SMS opt-outs

        Args:
            format
            limit"""
        client = _get_client()
        try:
            response = client.sms.list_sms_opt_outs(format=format, limit=limit)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create an alphanumeric sender ID",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_create_sms_sender_id(sender_id: str) -> str:
        """Create an alphanumeric sender ID

        Args:
            sender_id: The sender ID recipients will see (3-11 letters/digits/spaces, at least one letter, no leading/trailing space). (required)"""
        client = _get_client()
        try:
            response = client.sms.create_sms_sender_id(sender_id=sender_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List alphanumeric sender IDs",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def sms_list_sms_sender_ids() -> str:
        """List alphanumeric sender IDs"""
        client = _get_client()
        try:
            response = client.sms.list_sms_sender_ids()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Request a higher sender ID daily limit",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_request_sms_sender_id_limit_increase(
        requested_cap: int, reason: str
    ) -> str:
        """Request a higher sender ID daily limit

        Args:
            requested_cap: Desired daily message cap. Must exceed the current cap. (required)
            reason: Use case and audience (what you send, to whom, opt-in status). (required)"""
        client = _get_client()
        try:
            response = client.sms.request_sms_sender_id_limit_increase(
                requested_cap=requested_cap, reason=reason
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete an alphanumeric sender ID",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_delete_sms_sender_id(id: str) -> str:
        """Delete an alphanumeric sender ID

        Args:
            id: Sender ID resource id. (required)"""
        client = _get_client()
        try:
            response = client.sms.delete_sms_sender_id(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Start a carrier registration",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_start_sms_registration(
        registration_type: str,
        phone_numbers: list[str] | None = None,
        brand: dict[str, Any] | None = None,
        campaign: dict[str, Any] | None = None,
        messaging_brand_name: str | None = None,
        wizard_values: dict[str, Any] | None = None,
        resubmit_request_id: str | None = None,
        toll_free: dict[str, Any] | None = None,
    ) -> str:
        """Start a carrier registration

            Args:
                registration_type: (required)
                phone_numbers: Your numbers this registration covers. When omitted or empty on a 10DLC registration, defaults to your active SMS-enabled US local numbers not already covered by another registration.
                brand: Required for 10DLC. The legal entity behind the traffic (TCR brand).
                campaign: Required for 10DLC. What you'll send and how recipients opt in/out.
        The opt-in/opt-out/help auto-responses (`optinMessage`,
        `optoutMessage`, `helpMessage`) are optional: when omitted, a
        compliant, brand-named template with the carrier-required
        disclosures is generated for you. If you do send them, they must
        name the registered brand and carry the disclosures — submissions
        that don't are rewritten to the compliant template before the
        campaign is filed.
                messaging_brand_name: DBA / trade name used to brand message content (samples and auto-replies) when it differs from the legal name, e.g. a sole proprietor texting under a business name. The legal `brand.displayName` is still what the carrier vets.
                wizard_values: Raw dashboard-wizard answers, stored only to prefill edit-and-resubmit. API integrators can omit.
                resubmit_request_id: Resubmit a registration that was returned for changes — updates it in place instead of creating a new one.
                toll_free: Required for toll_free."""
        client = _get_client()
        try:
            response = client.sms.start_sms_registration(
                registration_type=registration_type,
                phone_numbers=phone_numbers,
                brand=brand,
                campaign=campaign,
                messaging_brand_name=messaging_brand_name,
                wizard_values=wizard_values,
                resubmit_request_id=resubmit_request_id,
                toll_free=toll_free,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List carrier registrations",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def sms_list_sms_registrations(include_deactivated: bool | None = None) -> str:
        """List carrier registrations

        Args:
            include_deactivated: Deactivated (terminated) registrations are hidden by default — pass true to include them."""
        client = _get_client()
        try:
            response = client.sms.list_sms_registrations(
                include_deactivated=include_deactivated
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Pre-check a carrier registration",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_preflight_sms_registration(
        registration_type: str,
        brand: dict[str, Any] | None,
        campaign: dict[str, Any] | None,
        phone_numbers: list[str] | None = None,
        messaging_brand_name: str | None = None,
    ) -> str:
        """Pre-check a carrier registration

        Args:
            registration_type: (required)
            phone_numbers
            brand: Same shape as the registration `brand`. (required)
            campaign: Same shape as the registration `campaign`. (required)
            messaging_brand_name"""
        client = _get_client()
        try:
            response = client.sms.preflight_sms_registration(
                registration_type=registration_type,
                phone_numbers=phone_numbers,
                brand=brand,
                campaign=campaign,
                messaging_brand_name=messaging_brand_name,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Deactivate a brand/campaign registration",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_deactivate_sms_registration(id: str) -> str:
        """Deactivate a brand/campaign registration

        Args:
            id: (required)"""
        client = _get_client()
        try:
            response = client.sms.deactivate_sms_registration(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a carrier registration",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def sms_get_sms_registration(id: str) -> str:
        """Get a carrier registration

        Args:
            id: (required)"""
        client = _get_client()
        try:
            response = client.sms.get_sms_registration(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Submit the sole-prop OTP",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_verify_sms_registration_otp(id: str, otp_pin: str) -> str:
        """Submit the sole-prop OTP

        Args:
            id: (required)
            otp_pin: (required)"""
        client = _get_client()
        try:
            response = client.sms.verify_sms_registration_otp(id=id, otp_pin=otp_pin)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Re-send the sole-prop OTP",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_resend_sms_registration_otp(id: str) -> str:
        """Re-send the sole-prop OTP

        Args:
            id: (required)"""
        client = _get_client()
        try:
            response = client.sms.resend_sms_registration_otp(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Appeal a rejected campaign",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_appeal_sms_registration(
        id: str,
        appeal_reason: str,
        message_flow: str | None = None,
        sample1: str | None = None,
        sample2: str | None = None,
    ) -> str:
        """Appeal a rejected campaign

        Args:
            id: (required)
            appeal_reason: Goes verbatim to the carrier reviewer — address the decline reason directly. (required)
            message_flow: Corrected opt-in flow; include a link to the opt-in page/form.
            sample1
            sample2"""
        client = _get_client()
        try:
            response = client.sms.appeal_sms_registration(
                id=id,
                appeal_reason=appeal_reason,
                message_flow=message_flow,
                sample1=sample1,
                sample2=sample2,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Reply to a change request",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_respond_to_sms_registration_review(
        id: str, note: str | None = None, files: list[str] | None = None
    ) -> str:
        """Reply to a change request

        Args:
            id: (required)
            note: Answer for the reviewer. Required when no files are sent.
            files: Hosted document URLs returned by POST /v1/sms/opt-in-proof."""
        client = _get_client()
        try:
            response = client.sms.respond_to_sms_registration_review(
                id=id, note=note, files=files
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Upload opt-in form proof",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_upload_sms_opt_in_proof_file() -> str:
        """Upload opt-in form proof"""
        client = _get_client()
        try:
            response = client.sms.upload_sms_opt_in_proof_file()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Upload opt-in form proof for an appeal",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_upload_sms_opt_in_proof(id: str) -> str:
        """Upload opt-in form proof for an appeal

        Args:
            id: (required)"""
        client = _get_client()
        try:
            response = client.sms.upload_sms_opt_in_proof(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a registration share link",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_share_sms_registration(number_id: str) -> str:
        """Create a registration share link

        Args:
            number_id: Your phone number's ID (from GET /v1/phone-numbers). (required)"""
        client = _get_client()
        try:
            response = client.sms.share_sms_registration(number_id=number_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Enable SMS on a number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_enable_sms_on_number(id: str) -> str:
        """Enable SMS on a number

        Args:
            id: Phone number record ID (from GET /v1/phone-numbers). (required)"""
        client = _get_client()
        try:
            response = client.sms.enable_sms_on_number(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Disable SMS on a number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_disable_sms_on_number(id: str) -> str:
        """Disable SMS on a number

        Args:
            id: (required)"""
        client = _get_client()
        try:
            response = client.sms.disable_sms_on_number(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Add number to SMS registration",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def sms_reuse_sms_registration_for_number(id: str) -> str:
        """Add number to SMS registration

        Args:
            id: (required)"""
        client = _get_client()
        try:
            response = client.sms.reuse_sms_registration_for_number(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # TRACKING_TAGS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get ad tracking tags",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def tracking_tags_get_ad_tracking_tags(ad_id: str) -> str:
        """Get ad tracking tags

        Args:
            ad_id: Ad id (hex _id, platformAdId, or effective story/media id). (required)"""
        client = _get_client()
        try:
            response = client.tracking_tags.get_ad_tracking_tags(ad_id=ad_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Set ad tracking tags",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def tracking_tags_update_ad_tracking_tags(
        ad_id: str,
        url_tags: list[dict[str, Any]] | None = None,
        creative: dict[str, Any] | None = None,
        tracking_url_template: str | None = None,
        final_url_suffix: str | None = None,
        dynamic_value_parameters: dict[str, Any] | None = None,
        custom_value_parameters: dict[str, Any] | None = None,
    ) -> str:
        """Set ad tracking tags

        Args:
            ad_id: (required)
            url_tags: Meta only. Click-URL params appended to a freshly-rebuilt creative. Meta dynamic macros ({{ad.id}}, {{campaign.id}}, {{placement}}, ...) are sent through unescaped so Meta expands them; every other character is percent-encoded.
            creative: Meta only. OPTIONAL — omit to preserve the existing creative verbatim (default). Provide it only to rebuild the creative explicitly, or for creatives whose object_story_spec Meta strips.
            tracking_url_template: Google only. Full tracking template (must contain {lpurl}).
            final_url_suffix: Google only. Parse-only key=value params.
            dynamic_value_parameters: LinkedIn only. key -> dynamic value enum (CAMPAIGN_ID, CAMPAIGN_NAME, CREATIVE_ID, ...).
            custom_value_parameters: LinkedIn only. key -> static value."""
        client = _get_client()
        try:
            response = client.tracking_tags.update_ad_tracking_tags(
                ad_id=ad_id,
                url_tags=url_tags,
                creative=creative,
                tracking_url_template=tracking_url_template,
                final_url_suffix=final_url_suffix,
                dynamic_value_parameters=dynamic_value_parameters,
                custom_value_parameters=custom_value_parameters,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List tracking tags",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def tracking_tags_list_tracking_tags(
        account_id: str, ad_account_id: str | None = None
    ) -> str:
        """List tracking tags

        Args:
            account_id: Ads SocialAccount id (platform `metaads` or `openaiads`). (required)
            ad_account_id: Optional, Meta only. Scope to one ad account, e.g. `act_123456789`. Ignored for OpenAI Ads."""
        client = _get_client()
        try:
            response = client.tracking_tags.list_tracking_tags(
                account_id=account_id, ad_account_id=ad_account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a tracking tag",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def tracking_tags_create_tracking_tag(
        account_id: str, ad_account_id: str, name: str
    ) -> str:
        """Create a tracking tag

        Args:
            account_id: Ads SocialAccount id (platform `metaads` or `openaiads`). (required)
            ad_account_id: Meta ad account id, e.g. `act_123456789`. Required by this endpoint but ignored for OpenAI Ads. (required)
            name: (required)"""
        client = _get_client()
        try:
            response = client.tracking_tags.create_tracking_tag(
                account_id=account_id, ad_account_id=ad_account_id, name=name
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a tracking tag",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def tracking_tags_get_tracking_tag(account_id: str, tag_id: str) -> str:
        """Get a tracking tag

        Args:
            account_id: (required)
            tag_id: Pixel id. (required)"""
        client = _get_client()
        try:
            response = client.tracking_tags.get_tracking_tag(
                account_id=account_id, tag_id=tag_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update a tracking tag",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def tracking_tags_update_tracking_tag(
        account_id: str,
        tag_id: str,
        name: str | None = None,
        enable_automatic_matching: bool | None = None,
        automatic_matching_fields: list[str] | None = None,
        first_party_cookie_status: str | None = None,
        data_use_setting: str | None = None,
    ) -> str:
        """Update a tracking tag

            Args:
                account_id: (required)
                tag_id: Pixel id. (required)
                name
                enable_automatic_matching: Meta Advanced Matching toggle (`enable_automatic_matching`).
                automatic_matching_fields: Which user fields Advanced Matching may collect. Meta's
        terse codes: em=email, ph=phone, fn=first name, ln=last
        name, ge=gender, db=date of birth, ct=city, st=state,
        zp=zip.
                first_party_cookie_status
                data_use_setting"""
        client = _get_client()
        try:
            response = client.tracking_tags.update_tracking_tag(
                account_id=account_id,
                tag_id=tag_id,
                name=name,
                enable_automatic_matching=enable_automatic_matching,
                automatic_matching_fields=automatic_matching_fields,
                first_party_cookie_status=first_party_cookie_status,
                data_use_setting=data_use_setting,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List accounts it is shared with",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def tracking_tags_list_tracking_tag_shared_accounts(
        account_id: str, tag_id: str
    ) -> str:
        """List accounts it is shared with

        Args:
            account_id: (required)
            tag_id: Pixel id. (required)"""
        client = _get_client()
        try:
            response = client.tracking_tags.list_tracking_tag_shared_accounts(
                account_id=account_id, tag_id=tag_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Share with an ad account",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def tracking_tags_add_tracking_tag_shared_account(
        account_id: str, tag_id: str, ad_account_id: str
    ) -> str:
        """Share with an ad account

        Args:
            account_id: (required)
            tag_id: Pixel id. (required)
            ad_account_id: Ad account to share with, e.g. `act_123456789`. (required)"""
        client = _get_client()
        try:
            response = client.tracking_tags.add_tracking_tag_shared_account(
                account_id=account_id, tag_id=tag_id, ad_account_id=ad_account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Stop sharing with an account",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def tracking_tags_remove_tracking_tag_shared_account(
        account_id: str, tag_id: str, ad_account_id: str | None = None
    ) -> str:
        """Stop sharing with an account

        Args:
            account_id: (required)
            tag_id: Pixel id. (required)
            ad_account_id: Ad account to unshare, e.g. `act_123456789`. May also be sent in the JSON body."""
        client = _get_client()
        try:
            response = client.tracking_tags.remove_tracking_tag_shared_account(
                account_id=account_id, tag_id=tag_id, ad_account_id=ad_account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get aggregated event stats",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def tracking_tags_get_tracking_tag_stats(
        account_id: str,
        tag_id: str,
        aggregation: str = "event",
        start_time: int | None = None,
        end_time: int | None = None,
    ) -> str:
        """Get aggregated event stats

        Args:
            account_id: (required)
            tag_id: Pixel id. (required)
            aggregation: Aggregation dimension. Defaults to `event`.
            start_time: Unix seconds lower bound.
            end_time: Unix seconds upper bound."""
        client = _get_client()
        try:
            response = client.tracking_tags.get_tracking_tag_stats(
                account_id=account_id,
                tag_id=tag_id,
                aggregation=aggregation,
                start_time=start_time,
                end_time=end_time,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # TWITTER_ENGAGEMENT

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Retweet a post",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def twitter_engagement_retweet_post(account_id: str, tweet_id: str) -> str:
        """Retweet a post

        Args:
            account_id: The social account ID (required)
            tweet_id: The ID of the tweet to retweet (required)"""
        client = _get_client()
        try:
            response = client.twitter_engagement.retweet_post(
                account_id=account_id, tweet_id=tweet_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Undo retweet",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def twitter_engagement_undo_retweet(account_id: str, tweet_id: str) -> str:
        """Undo retweet

        Args:
            account_id: (required)
            tweet_id: The ID of the original tweet to un-retweet (required)"""
        client = _get_client()
        try:
            response = client.twitter_engagement.undo_retweet(
                account_id=account_id, tweet_id=tweet_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Bookmark a tweet",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def twitter_engagement_bookmark_post(account_id: str, tweet_id: str) -> str:
        """Bookmark a tweet

        Args:
            account_id: The social account ID (required)
            tweet_id: The ID of the tweet to bookmark (required)"""
        client = _get_client()
        try:
            response = client.twitter_engagement.bookmark_post(
                account_id=account_id, tweet_id=tweet_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Remove bookmark",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def twitter_engagement_remove_bookmark(account_id: str, tweet_id: str) -> str:
        """Remove bookmark

        Args:
            account_id: (required)
            tweet_id: The ID of the tweet to unbookmark (required)"""
        client = _get_client()
        try:
            response = client.twitter_engagement.remove_bookmark(
                account_id=account_id, tweet_id=tweet_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Follow a user",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def twitter_engagement_follow_user(account_id: str, target_user_id: str) -> str:
        """Follow a user

        Args:
            account_id: The social account ID (required)
            target_user_id: The Twitter ID of the user to follow (required)"""
        client = _get_client()
        try:
            response = client.twitter_engagement.follow_user(
                account_id=account_id, target_user_id=target_user_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Unfollow a user",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def twitter_engagement_unfollow_user(account_id: str, target_user_id: str) -> str:
        """Unfollow a user

        Args:
            account_id: (required)
            target_user_id: The Twitter ID of the user to unfollow (required)"""
        client = _get_client()
        try:
            response = client.twitter_engagement.unfollow_user(
                account_id=account_id, target_user_id=target_user_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Search recent tweets",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def twitter_engagement_search_tweets(
        account_id: str,
        query: str,
        limit: int = 10,
        since_id: str | None = None,
        until_id: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        cursor: str | None = None,
        sort_order: str = "recency",
    ) -> str:
        """Search recent tweets

        Args:
            account_id: The social account ID (required)
            query: X search query, max 512 characters. Operators are passed through unchanged; X rejects malformed queries with a 400. (required)
            limit: Results per page. X requires a minimum of 10; values below 10 are rejected.
            since_id: Only return tweets with an ID greater than (more recent than) this numeric tweet ID. Non-numeric values are rejected with 400.
            until_id: Only return tweets with an ID less than (older than) this numeric tweet ID. Non-numeric values are rejected with 400.
            start_time: Oldest UTC timestamp (ISO 8601, inclusive), within the last 7 days
            end_time: Newest UTC timestamp (ISO 8601, exclusive), within the last 7 days
            cursor: Pagination cursor from a previous response
            sort_order"""
        client = _get_client()
        try:
            response = client.twitter_engagement.search_tweets(
                account_id=account_id,
                query=query,
                limit=limit,
                since_id=since_id,
                until_id=until_id,
                start_time=start_time,
                end_time=end_time,
                cursor=cursor,
                sort_order=sort_order,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Look up a tweet",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def twitter_engagement_get_tweet(account_id: str, id: str) -> str:
        """Look up a tweet

        Args:
            account_id: The social account ID whose X token is used for the lookup (required)
            id: Numeric tweet ID or a tweet URL (e.g. https://x.com/user/status/123...) (required)"""
        client = _get_client()
        try:
            response = client.twitter_engagement.get_tweet(account_id=account_id, id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # USAGE

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Account billing snapshot (plan, cycle, balance, caps, status)",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def usage_get_billing() -> str:
        """Account billing snapshot (plan, cycle, balance, caps, status)"""
        client = _get_client()
        try:
            response = client.usage.get_billing()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get X/Twitter API pricing table",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def usage_get_x_api_pricing() -> str:
        """Get X/Twitter API pricing table"""
        client = _get_client()
        try:
            response = client.usage.get_x_api_pricing()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Usage snapshot (default) or billed-spend metering (with params)",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def usage_get_usage(
        reconcile: bool | None = None,
        range: str = "cycle",
        from_: str | None = None,
        to: str | None = None,
        granularity: str = "day",
    ) -> str:
        """Usage snapshot (default) or billed-spend metering (with params)

            Args:
                reconcile: Snapshot mode only. For Stripe subscription users, `true` forces a
        subscription reconciliation pass even when cached plan data looks
        complete.
                range: Window to report. `cycle` / `prev-cycle` resolve to the customer's
        real billing-period bounds (falling back to a trailing 30 days when
        no invoice exists yet); `7d`…`12mo` are trailing windows; `custom`
        uses `from` / `to`.
                from_: Inclusive start (UTC date). Required when `range=custom`.
                to: Inclusive end (UTC date). Required when `range=custom`. Max span 366 days.
                granularity: Bucketing of the `days` series: `day` (one row per UTC day),
        `month` (one row per calendar month, dated to the 1st), or `total`
        (no series — read `totals`). Does not affect `totals`."""
        client = _get_client()
        try:
            response = client.usage.get_usage(
                reconcile=reconcile,
                range=range,
                from_=from_,
                to=to,
                granularity=granularity,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get plan and usage snapshot (plan, limits, payment status)",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def usage_get_usage_stats(reconcile: bool | None = None) -> str:
        """Get plan and usage snapshot (plan, limits, payment status)

            Args:
                reconcile: For Stripe subscription users, `true` forces a subscription
        reconciliation pass even when cached plan data looks complete.
        Omit the parameter, or pass `false`, to use the default
        first-time-only reconciliation behavior. Invalid boolean values are
        rejected."""
        client = _get_client()
        try:
            response = client.usage.get_usage_stats(reconcile=reconcile)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Calling usage and cost",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def usage_get_calls_usage(
        since: str | None = None,
        until: str | None = None,
        channel: str | None = None,
        number: str | None = None,
        group_by: str | None = None,
    ) -> str:
        """Calling usage and cost

        Args:
            since: Start of the window (inclusive). Default 30 days before `until`.
            until: End of the window (exclusive). Default now.
            channel
            number: Scope to calls involving this number (typically one of YOUR numbers). E.164, leading + optional.
            group_by"""
        client = _get_client()
        try:
            response = client.usage.get_calls_usage(
                since=since,
                until=until,
                channel=channel,
                number=number,
                group_by=group_by,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="SMS usage (volumes)",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def usage_get_sms_usage(
        since: str | None = None,
        until: str | None = None,
        number: str | None = None,
        group_by: str | None = None,
    ) -> str:
        """SMS usage (volumes)

        Args:
            since: Start of the window (inclusive). Default 30 days before `until`.
            until: End of the window (exclusive). Default now.
            number: Scope to one of YOUR SMS-enabled numbers (E.164, leading + optional).
            group_by"""
        client = _get_client()
        try:
            response = client.usage.get_sms_usage(
                since=since, until=until, number=number, group_by=group_by
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # USERS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List users",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def users_list_users() -> str:
        """List users"""
        client = _get_client()
        try:
            response = client.users.list_users()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get user",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def users_get_user(user_id: str) -> str:
        """Get user

        Args:
            user_id: (required)"""
        client = _get_client()
        try:
            response = client.users.get_user(user_id=user_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # VALIDATE

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Validate character count",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def validate_post_length(text: str) -> str:
        """Validate character count

        Args:
            text: The post text to check (required)"""
        client = _get_client()
        try:
            response = client.validate.validate_post_length(text=text)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Validate post content",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def validate_post(
        platforms: list[dict[str, Any]] | None,
        content: str | None = None,
        media_items: list[dict[str, Any]] | None = None,
    ) -> str:
        """Validate post content

        Args:
            content: Post text content
            platforms: Target platforms (same format as POST /v1/posts) (required)
            media_items: Root media items shared across platforms"""
        client = _get_client()
        try:
            response = client.validate.validate_post(
                content=content, platforms=platforms, media_items=media_items
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Validate media URL",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def validate_media(url: str) -> str:
        """Validate media URL

        Args:
            url: Public media URL to validate (required)"""
        client = _get_client()
        try:
            response = client.validate.validate_media(url=url)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Check subreddit existence",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def validate_subreddit(name: str, account_id: str | None = None) -> str:
        """Check subreddit existence

        Args:
            name: Subreddit name (with or without "r/" prefix) (required)
            account_id: Reddit social account ID for authenticated lookup (recommended for reliable results)"""
        client = _get_client()
        try:
            response = client.validate.validate_subreddit(
                name=name, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # VERIFY

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Send a verification code",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def verify_create_verification(
        channel: str,
        to: str,
        from_: str | None = None,
        brand_name: str | None = None,
        code_length: int = 6,
        ttl_minutes: int = 10,
    ) -> str:
        """Send a verification code

        Args:
            channel: SMS-only for now. (required)
            to: E.164 phone number. (required)
            from_: The SMS-enabled number on your account to send from. Defaults to your only SMS number.
            brand_name: Your app or business name, rendered in the message. Defaults to your account name. Letters, numbers, and basic punctuation only.
            code_length
            ttl_minutes"""
        client = _get_client()
        try:
            response = client.verify.create_verification(
                channel=channel,
                to=to,
                from_=from_,
                brand_name=brand_name,
                code_length=code_length,
                ttl_minutes=ttl_minutes,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a verification",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def verify_get_verification(verification_id: str) -> str:
        """Get a verification

        Args:
            verification_id: (required)"""
        client = _get_client()
        try:
            response = client.verify.get_verification(verification_id=verification_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Check a verification code",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def verify_check_verification(verification_id: str, code: str) -> str:
        """Check a verification code

        Args:
            verification_id: (required)
            code: (required)"""
        client = _get_client()
        try:
            response = client.verify.check_verification(
                verification_id=verification_id, code=code
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # VOICE

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Place an outbound phone call",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def voice_create_voice_call(
        to: str,
        from_number: str | None = None,
        forward_to: str | None = None,
        greeting: str | None = None,
        record_override: bool | None = None,
        transcribe_override: bool | None = None,
        transcription_language: str | None = None,
        amd: bool | None = None,
        voicemail_drop_message: str | None = None,
    ) -> str:
        """Place an outbound phone call

        Args:
            to: Destination to dial, E.164 with leading +. (required)
            from_number: Which of your voice-enabled numbers to dial from. Optional when you have exactly one.
            forward_to: Per-call agent override (tel:+E164, sip:..., or wss://...); defaults to the number's stored forward destination.
            greeting: Spoken to the callee when they answer, before the bridge.
            record_override: Per-call recording toggle; defaults to the number's setting.
            transcribe_override: Per-call transcription toggle; defaults to the number's setting.
            transcription_language: 'auto' derives from the callee's country; 'en'/'es' force it.
            amd: Answering-machine detection; defers the bridge until human vs machine is known.
            voicemail_drop_message: Spoken to a detected machine, then hang up (implies `amd`). For outbound voicemail drops."""
        client = _get_client()
        try:
            response = client.voice.create_voice_call(
                to=to,
                from_number=from_number,
                forward_to=forward_to,
                greeting=greeting,
                record_override=record_override,
                transcribe_override=transcribe_override,
                transcription_language=transcription_language,
                amd=amd,
                voicemail_drop_message=voicemail_drop_message,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List phone calls",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def voice_list_voice_calls(
        status: str | None = None,
        direction: str | None = None,
        number: str | None = None,
        before: str | None = None,
        limit: int = 50,
    ) -> str:
        """List phone calls

        Args:
            status
            direction
            number: Exact filter: calls involving this number (typically one of your DIDs). E.164, leading + optional.
            before
            limit"""
        client = _get_client()
        try:
            response = client.voice.list_voice_calls(
                status=status,
                direction=direction,
                number=number,
                before=before,
                limit=limit,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a phone call",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def voice_get_voice_call(id: str) -> str:
        """Get a phone call

        Args:
            id: (required)"""
        client = _get_client()
        try:
            response = client.voice.get_voice_call(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Hang up a live call",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def voice_end_voice_call(id: str) -> str:
        """Hang up a live call

        Args:
            id: (required)"""
        client = _get_client()
        try:
            response = client.voice.end_voice_call(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a call recording",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def voice_get_voice_call_recording(id: str, as_: str | None = None) -> str:
        """Get a call recording

        Args:
            id: (required)
            as_: `json` returns `{ url }` instead of a 302 redirect."""
        client = _get_client()
        try:
            response = client.voice.get_voice_call_recording(id=id, as_=as_)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Blind-transfer a live call",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def voice_transfer_voice_call(id: str, to: str) -> str:
        """Blind-transfer a live call

        Args:
            id: (required)
            to: +E164 phone number (tel: prefix optional) or a sip: URI. wss:// is not a valid transfer target. (required)"""
        client = _get_client()
        try:
            response = client.voice.transfer_voice_call(id=id, to=to)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Estimate call cost",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def voice_get_voice_call_estimate(
        to: str,
        minutes: int = 1,
        recording: bool | None = None,
        transcription: bool | None = None,
    ) -> str:
        """Estimate call cost

        Args:
            to: Destination number, E.164 (leading + optional). (required)
            minutes
            recording
            transcription"""
        client = _get_client()
        try:
            response = client.voice.get_voice_call_estimate(
                to=to, minutes=minutes, recording=recording, transcription=transcription
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Mint a browser softphone session",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def voice_create_voice_web_session() -> str:
        """Mint a browser softphone session"""
        client = _get_client()
        try:
            response = client.voice.create_voice_web_session()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Dial from the browser softphone",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def voice_dial_voice_web_call(
        to: str,
        credential_id: str,
        from_number: str | None = None,
        record_override: bool | None = None,
    ) -> str:
        """Dial from the browser softphone

        Args:
            to: The number to call, E.164 with leading +. (required)
            credential_id: The WebRTC credential id returned by POST /v1/voice/calls/web (the registered browser). (required)
            from_number: Which of your voice-enabled numbers to call from (optional when you have one).
            record_override"""
        client = _get_client()
        try:
            response = client.voice.dial_voice_web_call(
                to=to,
                credential_id=credential_id,
                from_number=from_number,
                record_override=record_override,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Enable phone calling on a number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def voice_enable_voice_on_number(
        id: str,
        forward_to: str | None = None,
        recording_enabled: bool | None = None,
        transcription_enabled: bool | None = None,
        transcription_language: str | None = None,
        voicemail_enabled: bool | None = None,
        voicemail_greeting: str | None = None,
        business_hours_enabled: bool | None = None,
        business_hours_timezone: str | None = None,
        business_hours: list[dict[str, Any]] | None = None,
        blocked_callers: list[str] | None = None,
        forward_caller_id: str | None = None,
        ivr_enabled: bool | None = None,
        ivr_prompt: str | None = None,
        ivr_options: list[dict[str, Any]] | None = None,
    ) -> str:
        """Enable phone calling on a number

        Args:
            id: Phone number record ID (from GET /v1/phone-numbers). (required)
            forward_to: tel:+E164, sip:..., or wss://... destination for inbound calls. Empty string clears the forward (outbound-only); omitted preserves the current one.
            recording_enabled
            transcription_enabled
            transcription_language
            voicemail_enabled: Voicemail is taken when there's no live destination. Default on.
            voicemail_greeting: Custom spoken greeting; empty string restores the default.
            business_hours_enabled: Outside the windows, inbound skips the forward and goes to voicemail. Off = 24/7.
            business_hours_timezone: IANA timezone the windows are evaluated in.
            business_hours
            blocked_callers: E.164 numbers rejected before answer. Replaces the whole list; bare 10-digit values are normalized as US numbers.
            forward_caller_id: Caller ID on the forwarded leg: your number (`business`) or the original caller's (`caller`).
            ivr_enabled: IVR menu (supersedes the plain forward within business hours).
            ivr_prompt
            ivr_options"""
        client = _get_client()
        try:
            response = client.voice.enable_voice_on_number(
                id=id,
                forward_to=forward_to,
                recording_enabled=recording_enabled,
                transcription_enabled=transcription_enabled,
                transcription_language=transcription_language,
                voicemail_enabled=voicemail_enabled,
                voicemail_greeting=voicemail_greeting,
                business_hours_enabled=business_hours_enabled,
                business_hours_timezone=business_hours_timezone,
                business_hours=business_hours,
                blocked_callers=blocked_callers,
                forward_caller_id=forward_caller_id,
                ivr_enabled=ivr_enabled,
                ivr_prompt=ivr_prompt,
                ivr_options=ivr_options,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Disable phone calling on a number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def voice_disable_voice_on_number(id: str) -> str:
        """Disable phone calling on a number

        Args:
            id: (required)"""
        client = _get_client()
        try:
            response = client.voice.disable_voice_on_number(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # WEBHOOKS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List webhooks",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def webhooks_get_webhook_settings() -> str:
        """List webhooks"""
        client = _get_client()
        try:
            response = client.webhooks.get_webhook_settings()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create webhook",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def webhooks_create_webhook_settings(
        name: str,
        url: str,
        events: list[str] | None,
        secret: str | None = None,
        is_active: bool = True,
        custom_headers: dict[str, Any] | None = None,
        disabled_resource_groups: list[str] | None = None,
    ) -> str:
        """Create webhook

        Args:
            name: Webhook name (1-50 characters) (required)
            url: Webhook endpoint URL (must be a valid URL, whitespace trimmed) (required)
            secret: Secret key for HMAC-SHA256 signature verification
            events: Events to subscribe to (at least one required) (required)
            is_active: Enable or disable webhook delivery. Defaults to `true` when omitted.
            custom_headers: Custom headers to include in webhook requests
            disabled_resource_groups: Resource groups this subscription does not receive (opt-out denylist). Omit or send an empty array to receive every event in `events`. Listing a group here drops its events before delivery and on every replay path. Set at creation it applies to everything this subscription ever receives; changed later via PUT it applies to events emitted after the change, with a five-minute tail for events already queued (see that operation). When the caller is a restricted (zrk_) key, that key's own disabled groups are unioned into whatever you send here, so a restricted key can never create a subscription wider than itself."""
        client = _get_client()
        try:
            response = client.webhooks.create_webhook_settings(
                name=name,
                url=url,
                secret=secret,
                events=events,
                is_active=is_active,
                custom_headers=custom_headers,
                disabled_resource_groups=disabled_resource_groups,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update webhook",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def webhooks_update_webhook_settings(
        id: str,
        name: str | None = None,
        url: str | None = None,
        secret: str | None = None,
        events: list[str] | None = None,
        is_active: bool | None = None,
        custom_headers: dict[str, Any] | None = None,
        disabled_resource_groups: list[str] | None = None,
    ) -> str:
        """Update webhook

        Args:
            id: Webhook ID to update (required) (required)
            name: Webhook name (1-50 characters). Must be non-empty if provided.
            url: Webhook endpoint URL (must be a valid URL, whitespace trimmed). Must be a valid URL if provided.
            secret: Secret key for HMAC-SHA256 signature verification
            events: Events to subscribe to. Must contain at least one event if provided.
            is_active: Enable or disable webhook delivery
            custom_headers: Custom headers to include in webhook requests
            disabled_resource_groups: Replaces the subscription's denylist. Send an empty array to clear it and receive every event in `events` again. Omitting the field leaves the current denylist untouched. Applies to events emitted after the update; already-queued events can still deliver for up to five minutes after they were enqueued. When the caller is a restricted (zrk_) key, that key's own disabled groups are unioned back in either way, so a restricted key can neither clear nor widen a subscription past its own groups."""
        client = _get_client()
        try:
            response = client.webhooks.update_webhook_settings(
                id=id,
                name=name,
                url=url,
                secret=secret,
                events=events,
                is_active=is_active,
                custom_headers=custom_headers,
                disabled_resource_groups=disabled_resource_groups,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete webhook",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def webhooks_delete_webhook_settings(id: str) -> str:
        """Delete webhook

        Args:
            id: Webhook ID to delete (required)"""
        client = _get_client()
        try:
            response = client.webhooks.delete_webhook_settings(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List webhook delivery logs",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def webhooks_get_webhook_logs(
        limit: int = 50,
        skip: int = 0,
        status: str | None = None,
        event: str | None = None,
        webhook_id: str | None = None,
        event_id: str | None = None,
    ) -> str:
        """List webhook delivery logs

        Args:
            limit: Maximum number of logs to return
            skip: Number of logs to skip (offset-based pagination)
            status: Filter by delivery outcome
            event: Filter by event type (e.g. post.published)
            webhook_id: Filter by webhook configuration ID
            event_id: Filter by stable webhook event ID"""
        client = _get_client()
        try:
            response = client.webhooks.get_webhook_logs(
                limit=limit,
                skip=skip,
                status=status,
                event=event,
                webhook_id=webhook_id,
                event_id=event_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Send test webhook",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def webhooks_test_webhook(webhook_id: str) -> str:
        """Send test webhook

        Args:
            webhook_id: ID of the webhook to test (required)"""
        client = _get_client()
        try:
            response = client.webhooks.test_webhook(webhook_id=webhook_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # WHATSAPP

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Register a connected WhatsApp number on the Cloud API",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_register_whats_app_number(
        account_id: str, pin: str | None = None
    ) -> str:
        """Register a connected WhatsApp number on the Cloud API

        Args:
            account_id: The WhatsApp account ID (required)
            pin: The 6-digit two-step verification PIN set on the number. Omit it only if the number has no PIN of its own."""
        client = _get_client()
        try:
            response = client.whatsapp.register_whats_app_number(
                account_id=account_id, pin=pin
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Download WhatsApp media",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_get_whats_app_media(media_id: str, account_id: str) -> str:
        """Download WhatsApp media

        Args:
            media_id: The media id from `attachments[].payload.id`. (required)
            account_id: The WhatsApp account that received the media. (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_media(
                media_id=media_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List templates",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_get_whats_app_templates(account_id: str) -> str:
        """List templates

        Args:
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_templates(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create template",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_create_whats_app_template(
        account_id: str,
        name: str,
        category: str,
        language: str,
        parameter_format: str | None = None,
        components: list[dict[str, Any]] | None = None,
        library_template_name: str | None = None,
        library_template_body_inputs: dict[str, Any] | None = None,
        library_template_button_inputs: list[dict[str, Any]] | None = None,
    ) -> str:
        """Create template

            Args:
                account_id: WhatsApp social account ID (required)
                name: Template name (lowercase, letters/numbers/underscores, must start with a letter) (required)
                category: Template category (required)
                language: Template language code (e.g., en_US) (required)
                parameter_format: Variable style: POSITIONAL ({{1}}, the default) or NAMED ({{customer_name}}). Named templates provide examples via body_text_named_params / header_text_named_params. Inferred as NAMED when omitted but a named-params example is present.
                components: Template components (header, body, footer, buttons, carousel, limited_time_offer). Required for custom templates, omit when using library_template_name.
                library_template_name: Name of a pre-built template from Meta's template library (e.g., "appointment_reminder",
        "auto_pay_reminder_1", "address_update"). When provided, the template is pre-approved
        by Meta with no review wait. Omit components when using this field.
                library_template_body_inputs: Optional body customizations for library templates. Available options depend on the
        template (e.g., add_contact_number, add_learn_more_link, add_security_recommendation,
        add_track_package_link, code_expiration_minutes).
                library_template_button_inputs: Optional button customizations for library templates. Each item specifies button type
        and configuration (e.g., URL, phone number, quick reply)."""
        client = _get_client()
        try:
            response = client.whatsapp.create_whats_app_template(
                account_id=account_id,
                name=name,
                category=category,
                language=language,
                parameter_format=parameter_format,
                components=components,
                library_template_name=library_template_name,
                library_template_body_inputs=library_template_body_inputs,
                library_template_button_inputs=library_template_button_inputs,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get template",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_get_whats_app_template(template_name: str, account_id: str) -> str:
        """Get template

        Args:
            template_name: Template name (required)
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_template(
                template_name=template_name, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update template",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_update_whats_app_template(
        template_name: str, account_id: str, components: list[dict[str, Any]] | None
    ) -> str:
        """Update template

        Args:
            template_name: Template name (required)
            account_id: WhatsApp social account ID (required)
            components: Updated template components (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.update_whats_app_template(
                template_name=template_name,
                account_id=account_id,
                components=components,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete template",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_delete_whats_app_template(template_name: str, account_id: str) -> str:
        """Delete template

        Args:
            template_name: Template name (required)
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.delete_whats_app_template(
                template_name=template_name, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get business profile",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_get_whats_app_business_profile(account_id: str) -> str:
        """Get business profile

        Args:
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_business_profile(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update business profile",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_update_whats_app_business_profile(
        account_id: str,
        about: str | None = None,
        address: str | None = None,
        description: str | None = None,
        email: str | None = None,
        websites: list[str] | None = None,
        vertical: str | None = None,
        profile_picture_handle: str | None = None,
    ) -> str:
        """Update business profile

        Args:
            account_id: WhatsApp social account ID (required)
            about: Short business description (max 139 characters)
            address: Business address
            description: Full business description (max 512 characters)
            email: Business email
            websites: Business websites (max 2)
            vertical: Business category (e.g., RETAIL, ENTERTAINMENT, etc.)
            profile_picture_handle: Handle from resumable upload for profile picture"""
        client = _get_client()
        try:
            response = client.whatsapp.update_whats_app_business_profile(
                account_id=account_id,
                about=about,
                address=address,
                description=description,
                email=email,
                websites=websites,
                vertical=vertical,
                profile_picture_handle=profile_picture_handle,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Upload profile picture",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_upload_whats_app_profile_photo(account_id: str, url: str) -> str:
        """Upload profile picture

        Args:
            account_id: WhatsApp social account ID (required)
            url: Publicly reachable https URL of the image (JPEG or PNG, max 5MB, recommended 640x640). Fetched server-side; must resolve directly without redirects. (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.upload_whats_app_profile_photo(
                account_id=account_id, url=url
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get display name status",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_get_whats_app_display_name(account_id: str) -> str:
        """Get display name status

        Args:
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_display_name(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Request display name change",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_update_whats_app_display_name(
        account_id: str, display_name: str
    ) -> str:
        """Request display name change

        Args:
            account_id: WhatsApp social account ID (required)
            display_name: New display name (must follow WhatsApp naming guidelines) (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.update_whats_app_display_name(
                account_id=account_id, display_name=display_name
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get business username",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_get_whatsapp_business_username(account_id: str) -> str:
        """Get business username

        Args:
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whatsapp_business_username(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Set business username",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_set_whatsapp_business_username(
        account_id: str, username: str, transfer_action: str = "none"
    ) -> str:
        """Set business username

           Args:
               account_id: WhatsApp social account ID (required)
               username: Desired username. Letters, digits, period, and underscore only. Must contain at least one letter. No leading, trailing, or consecutive periods. No www prefix. No domain TLD suffix.
        (required)
               transfer_action: Pass `force_transfer` to request a transfer if the username is held by another account"""
        client = _get_client()
        try:
            response = client.whatsapp.set_whatsapp_business_username(
                account_id=account_id,
                username=username,
                transfer_action=transfer_action,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete business username",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_delete_whatsapp_business_username(account_id: str) -> str:
        """Delete business username

        Args:
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.delete_whatsapp_business_username(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get username suggestions",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_get_whatsapp_business_username_suggestions(account_id: str) -> str:
        """Get username suggestions

        Args:
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whatsapp_business_username_suggestions(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Check if a user is blocked",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_get_whats_app_block_status(account_id: str, user: str) -> str:
        """Check if a user is blocked

        Args:
            account_id: (required)
            user: Consumer wa_id or E.164 phone (leading + optional) (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_block_status(
                account_id=account_id, user=user
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List blocked users",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_get_whats_app_blocked_users(
        account_id: str, limit: int | None = None, after: str | None = None
    ) -> str:
        """List blocked users

        Args:
            account_id: WhatsApp social account ID (required)
            limit: Page size.
            after: Cursor from a previous response's `nextCursor`."""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_blocked_users(
                account_id=account_id, limit=limit, after=after
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Block users",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_block_whats_app_users(account_id: str, users: list[str] | None) -> str:
        """Block users

        Args:
            account_id: WhatsApp social account ID (required)
            users: Phone numbers (E.164, e.g. "+16505551234") or WhatsApp user IDs to block. (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.block_whats_app_users(
                account_id=account_id, users=users
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Unblock users",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_unblock_whats_app_users(
        account_id: str, users: list[str] | None
    ) -> str:
        """Unblock users

        Args:
            account_id: WhatsApp social account ID (required)
            users: Phone numbers (E.164) or WhatsApp user IDs to unblock. (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.unblock_whats_app_users(
                account_id=account_id, users=users
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get CTWA conversions dataset",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_get_whats_app_dataset(account_id: str) -> str:
        """Get CTWA conversions dataset

        Args:
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_dataset(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Provision CTWA dataset",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_create_whats_app_dataset(account_id: str) -> str:
        """Provision CTWA dataset

        Args:
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.create_whats_app_dataset(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List active groups",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_list_whats_app_group_chats(
        account_id: str, limit: int = 25, after: str | None = None
    ) -> str:
        """List active groups

        Args:
            account_id: WhatsApp social account ID (required)
            limit: Max groups to return
            after: Pagination cursor"""
        client = _get_client()
        try:
            response = client.whatsapp.list_whats_app_group_chats(
                account_id=account_id, limit=limit, after=after
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create group",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_create_whats_app_group_chat(
        account_id: str,
        subject: str,
        description: str | None = None,
        join_approval_mode: str | None = None,
    ) -> str:
        """Create group

        Args:
            account_id: WhatsApp social account ID (required)
            subject: Group name (max 128 characters) (required)
            description: Group description (max 2048 characters)
            join_approval_mode: Whether users need approval to join via invite link"""
        client = _get_client()
        try:
            response = client.whatsapp.create_whats_app_group_chat(
                account_id=account_id,
                subject=subject,
                description=description,
                join_approval_mode=join_approval_mode,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get group info",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_get_whats_app_group_chat(group_id: str, account_id: str) -> str:
        """Get group info

        Args:
            group_id: Group ID (required)
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_group_chat(
                group_id=group_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update group settings",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_update_whats_app_group_chat(
        group_id: str,
        account_id: str,
        subject: str | None = None,
        description: str | None = None,
        join_approval_mode: str | None = None,
    ) -> str:
        """Update group settings

        Args:
            group_id: Group ID (required)
            account_id: WhatsApp social account ID (required)
            subject
            description
            join_approval_mode"""
        client = _get_client()
        try:
            response = client.whatsapp.update_whats_app_group_chat(
                group_id=group_id,
                account_id=account_id,
                subject=subject,
                description=description,
                join_approval_mode=join_approval_mode,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete group",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_delete_whats_app_group_chat(group_id: str, account_id: str) -> str:
        """Delete group

        Args:
            group_id: Group ID (required)
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.delete_whats_app_group_chat(
                group_id=group_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Add participants",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_add_whats_app_group_participants(
        group_id: str, account_id: str, phone_numbers: list[str] | None
    ) -> str:
        """Add participants

        Args:
            group_id: Group ID (required)
            account_id: WhatsApp social account ID (required)
            phone_numbers: Phone numbers in E.164 format (max 8) (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.add_whats_app_group_participants(
                group_id=group_id, account_id=account_id, phone_numbers=phone_numbers
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Remove participants",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_remove_whats_app_group_participants(
        group_id: str, account_id: str, phone_numbers: list[str] | None
    ) -> str:
        """Remove participants

        Args:
            group_id: Group ID (required)
            account_id: WhatsApp social account ID (required)
            phone_numbers: Phone numbers to remove (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.remove_whats_app_group_participants(
                group_id=group_id, account_id=account_id, phone_numbers=phone_numbers
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create invite link",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_create_whats_app_group_invite_link(
        group_id: str, account_id: str
    ) -> str:
        """Create invite link

        Args:
            group_id: Group ID (required)
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.create_whats_app_group_invite_link(
                group_id=group_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List join requests",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_list_whats_app_group_join_requests(
        group_id: str, account_id: str
    ) -> str:
        """List join requests

        Args:
            group_id: Group ID (required)
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.list_whats_app_group_join_requests(
                group_id=group_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Approve join requests",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_approve_whats_app_group_join_requests(
        group_id: str, account_id: str, phone_numbers: list[str] | None
    ) -> str:
        """Approve join requests

        Args:
            group_id: Group ID (required)
            account_id: WhatsApp social account ID (required)
            phone_numbers: Phone numbers to approve (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.approve_whats_app_group_join_requests(
                group_id=group_id, account_id=account_id, phone_numbers=phone_numbers
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Reject join requests",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_reject_whats_app_group_join_requests(
        group_id: str, account_id: str, phone_numbers: list[str] | None
    ) -> str:
        """Reject join requests

        Args:
            group_id: Group ID (required)
            account_id: WhatsApp social account ID (required)
            phone_numbers: Phone numbers to reject (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.reject_whats_app_group_join_requests(
                group_id=group_id, account_id=account_id, phone_numbers=phone_numbers
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List conversion events",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_list_whats_app_conversions(account_id: str, limit: int = 50) -> str:
        """List conversion events

        Args:
            account_id: WhatsApp social account ID (required)
            limit: Max events to return (1-200, default 50)."""
        client = _get_client()
        try:
            response = client.whatsapp.list_whats_app_conversions(
                account_id=account_id, limit=limit
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Send WhatsApp conversion event",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_send_whats_app_conversion(
        account_id: str,
        event_name: str,
        event_id: str,
        event_time: float | None = None,
        conversation_id: str | None = None,
        phone_e164: str | None = None,
        value: float | None = None,
        currency: str | None = None,
        content_ids: list[str] | None = None,
        email: str | None = None,
        external_id: str | None = None,
        test_code: str | None = None,
    ) -> str:
        """Send WhatsApp conversion event

            Args:
                account_id: WhatsApp SocialAccount ID. (required)
                event_name: Live-verified allowlist of event names accepted by Meta's
        CAPI for Business Messaging (Graph API v25.0). Other
        standard pixel events including `Lead`,
        `CompleteRegistration`, `Subscribe`, `Schedule`, `Contact`,
        `StartTrial`, `AddPaymentInfo`, `Search`, and
        `SubmitApplication` are rejected with subcode 2804066
        ("Messaging Event Invalid Event Type") on
        `action_source = business_messaging` events. Custom event
        names are also rejected.

        Use `LeadSubmitted` (NOT `Lead`) for lead-style conversions.
         (required)
                event_time: Unix seconds. Defaults to the time of the request when
        omitted. Meta's attribution window is 7 days from click;
        events older than that lose attribution.
                event_id: Stable dedup key. Reuse to suppress duplicate events
        (Meta dedupes against pixel events with the same id).
         (required)
                conversation_id: Zernio Conversation `_id` (preferred lookup). The
        conversation must have a captured `ctwa_clid` in metadata
        (set automatically by the WhatsApp webhook on the first
        inbound message after a CTWA ad click).
                phone_e164: Contact phone number, digits only with no '+'. When used
        in lieu of `conversationId`, the handler resolves to the
        most recent CTWA-attributed conversation for this phone
        on the supplied account.
                value: Conversion value (e.g. order total).
                currency: ISO 4217 currency code (e.g. `USD`).
                content_ids: Optional product / content identifiers.
                email: User email. Normalized + SHA-256 hashed before sending to Meta.
                external_id: Stable customer identifier. Lowercased + SHA-256 hashed
        before sending to Meta.
                test_code: Meta `test_event_code` passthrough. Routes the event to
        the Test Events tab in Events Manager instead of the
        production dataset, useful for development."""
        client = _get_client()
        try:
            response = client.whatsapp.send_whats_app_conversion(
                account_id=account_id,
                event_name=event_name,
                event_time=event_time,
                event_id=event_id,
                conversation_id=conversation_id,
                phone_e164=phone_e164,
                value=value,
                currency=currency,
                content_ids=content_ids,
                email=email,
                external_id=external_id,
                test_code=test_code,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # WHATSAPP_CALLING

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get calling config for an account",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_calling_get_whats_app_calling_config(account_id: str) -> str:
        """Get calling config for an account

        Args:
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_calling.get_whats_app_calling_config(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Enable calling on a number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_calling_enable_whats_app_calling_legacy(
        id: str,
        account_id: str,
        forward_to: str,
        sip_auth_username: str | None = None,
        sip_auth_password: str | None = None,
        recording_enabled: bool = False,
        call_icon_countries: list[str] | None = None,
        max_call_duration_seconds: int | None = None,
        forward_caller_id: str = "business",
    ) -> str:
        """Enable calling on a number

        Args:
            id: WhatsAppPhoneNumber Mongo ID (required)
            account_id: (required)
            forward_to: tel:+E164 / sip:... / wss://... destination (required)
            sip_auth_username
            sip_auth_password: Stored encrypted, never returned by any endpoint.
            recording_enabled
            call_icon_countries
            max_call_duration_seconds: Hard cap (seconds) on a forwarded call; the carrier hangs up both legs when it fires. Safety valve against dead-air billing when a destination hangs up but the signal is lost.
            forward_caller_id: Caller ID presented to the forward destination. caller = the WhatsApp user's number (sip: destinations only; ignored on tel: forwards). Fixes AI-agent trunks that reject seeing the business number call itself."""
        client = _get_client()
        try:
            response = client.whatsapp_calling.enable_whats_app_calling_legacy(
                id=id,
                account_id=account_id,
                forward_to=forward_to,
                sip_auth_username=sip_auth_username,
                sip_auth_password=sip_auth_password,
                recording_enabled=recording_enabled,
                call_icon_countries=call_icon_countries,
                max_call_duration_seconds=max_call_duration_seconds,
                forward_caller_id=forward_caller_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update calling config",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_calling_update_whats_app_calling_legacy(
        id: str,
        account_id: str,
        forward_to: str | None = None,
        sip_auth_username: str | None = None,
        sip_auth_password: str | None = None,
        recording_enabled: bool | None = None,
        call_icon_countries: str | None = None,
        max_call_duration_seconds: str | None = None,
        forward_caller_id: str | None = None,
    ) -> str:
        """Update calling config

        Args:
            id: (required)
            account_id: (required)
            forward_to
            sip_auth_username
            sip_auth_password
            recording_enabled
            call_icon_countries
            max_call_duration_seconds: Hard cap (seconds) on forwarded calls; null clears the cap.
            forward_caller_id: caller = present the WhatsApp user's number to the forward destination (sip: only)."""
        client = _get_client()
        try:
            response = client.whatsapp_calling.update_whats_app_calling_legacy(
                id=id,
                account_id=account_id,
                forward_to=forward_to,
                sip_auth_username=sip_auth_username,
                sip_auth_password=sip_auth_password,
                recording_enabled=recording_enabled,
                call_icon_countries=call_icon_countries,
                max_call_duration_seconds=max_call_duration_seconds,
                forward_caller_id=forward_caller_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Disable calling on a number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_calling_disable_whats_app_calling_legacy(
        id: str, account_id: str
    ) -> str:
        """Disable calling on a number

        Args:
            id: (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_calling.disable_whats_app_calling_legacy(
                id=id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Check call permission",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_calling_get_whats_app_call_permissions(
        account_id: str, to: str
    ) -> str:
        """Check call permission

        Args:
            account_id: (required)
            to: Consumer wa_id (E.164, leading + optional) (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_calling.get_whats_app_call_permissions(
                account_id=account_id, to=to
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Initiate outbound call",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_calling_initiate_whats_app_call(
        account_id: str,
        to: str,
        action: str | None = None,
        body_text: str | None = None,
        forward_to: str | None = None,
        record_override: bool | None = None,
        biz_opaque_callback_data: str | None = None,
    ) -> str:
        """Initiate outbound call

            Args:
                account_id: (required)
                to: Consumer wa_id (E.164, leading + optional) (required)
                action: Omit to place a call. Set to send the consent prompt instead.
                body_text: Body text shown with the consent prompt (send_call_permission_request only).
                forward_to: Per-call destination override. Same accepted shape as the
        number's stored forwardTo (tel:+E164, sip:..., wss://...).
                record_override
                biz_opaque_callback_data: Accepted for forward compatibility. Not currently echoed
        back in webhook payloads (SIP-first flow does not pass
        through Meta's Graph API where Meta would echo this)."""
        client = _get_client()
        try:
            response = client.whatsapp_calling.initiate_whats_app_call(
                account_id=account_id,
                to=to,
                action=action,
                body_text=body_text,
                forward_to=forward_to,
                record_override=record_override,
                biz_opaque_callback_data=biz_opaque_callback_data,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List call history for an account",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_calling_list_whats_app_calls(
        account_id: str,
        status: str | None = None,
        direction: str | None = None,
        since: str | None = None,
        until: str | None = None,
        before: str | None = None,
        limit: int | None = None,
    ) -> str:
        """List call history for an account

        Args:
            account_id: (required)
            status
            direction
            since
            until
            before: Return calls with startedAt strictly before this instant (use the previous page's nextCursor).
            limit"""
        client = _get_client()
        try:
            response = client.whatsapp_calling.list_whats_app_calls(
                account_id=account_id,
                status=status,
                direction=direction,
                since=since,
                until=until,
                before=before,
                limit=limit,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a single call",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_calling_get_whats_app_call(id: str, account_id: str) -> str:
        """Get a single call

        Args:
            id: (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_calling.get_whats_app_call(
                id=id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a call recording",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_calling_get_whats_app_call_recording(
        id: str, account_id: str, as_: str | None = None
    ) -> str:
        """Get a call recording

        Args:
            id: (required)
            account_id: (required)
            as_: `json` returns `{ url }` instead of a 302 redirect."""
        client = _get_client()
        try:
            response = client.whatsapp_calling.get_whats_app_call_recording(
                id=id, account_id=account_id, as_=as_
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Estimate per-minute cost",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_calling_get_whats_app_call_estimate(
        account_id: str,
        to: str,
        minutes: int | None = None,
        recording: bool | None = None,
    ) -> str:
        """Estimate per-minute cost

        Args:
            account_id: (required)
            to: (required)
            minutes
            recording"""
        client = _get_client()
        try:
            response = client.whatsapp_calling.get_whats_app_call_estimate(
                account_id=account_id, to=to, minutes=minutes, recording=recording
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get calling config for a number",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_calling_get_whats_app_calling(id: str) -> str:
        """Get calling config for a number

        Args:
            id: Phone number record ID (from GET /v1/phone-numbers). (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_calling.get_whats_app_calling(id=id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Enable calling on a number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_calling_enable_whats_app_calling(
        id: str,
        account_id: str,
        forward_to: str,
        sip_auth_username: str | None = None,
        sip_auth_password: str | None = None,
        recording_enabled: bool = False,
        call_icon_countries: list[str] | None = None,
        max_call_duration_seconds: int | None = None,
        forward_caller_id: str = "business",
    ) -> str:
        """Enable calling on a number

        Args:
            id: Phone number record ID (from GET /v1/phone-numbers). (required)
            account_id: (required)
            forward_to: tel:+E164 / sip:... / wss://... destination (required)
            sip_auth_username
            sip_auth_password: Stored encrypted, never returned by any endpoint.
            recording_enabled
            call_icon_countries
            max_call_duration_seconds: Hard cap (seconds) on a forwarded call; the carrier hangs up both legs when it fires. Safety valve against dead-air billing when a destination hangs up but the signal is lost.
            forward_caller_id: Caller ID presented to the forward destination. caller = the WhatsApp user's number (sip: destinations only; ignored on tel: forwards). Fixes AI-agent trunks that reject seeing the business number call itself."""
        client = _get_client()
        try:
            response = client.whatsapp_calling.enable_whats_app_calling(
                id=id,
                account_id=account_id,
                forward_to=forward_to,
                sip_auth_username=sip_auth_username,
                sip_auth_password=sip_auth_password,
                recording_enabled=recording_enabled,
                call_icon_countries=call_icon_countries,
                max_call_duration_seconds=max_call_duration_seconds,
                forward_caller_id=forward_caller_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update calling config",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_calling_update_whats_app_calling(
        id: str,
        account_id: str,
        forward_to: str | None = None,
        sip_auth_username: str | None = None,
        sip_auth_password: str | None = None,
        recording_enabled: bool | None = None,
        call_icon_countries: str | None = None,
        max_call_duration_seconds: str | None = None,
        forward_caller_id: str | None = None,
    ) -> str:
        """Update calling config

        Args:
            id: (required)
            account_id: (required)
            forward_to
            sip_auth_username
            sip_auth_password
            recording_enabled
            call_icon_countries
            max_call_duration_seconds: Hard cap (seconds) on forwarded calls; null clears the cap.
            forward_caller_id: caller = present the WhatsApp user's number to the forward destination (sip: only)."""
        client = _get_client()
        try:
            response = client.whatsapp_calling.update_whats_app_calling(
                id=id,
                account_id=account_id,
                forward_to=forward_to,
                sip_auth_username=sip_auth_username,
                sip_auth_password=sip_auth_password,
                recording_enabled=recording_enabled,
                call_icon_countries=call_icon_countries,
                max_call_duration_seconds=max_call_duration_seconds,
                forward_caller_id=forward_caller_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Disable calling on a number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_calling_disable_whats_app_calling(id: str, account_id: str) -> str:
        """Disable calling on a number

        Args:
            id: (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_calling.disable_whats_app_calling(
                id=id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Start caller-ID verification for a customer-brought number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_calling_start_whats_app_caller_id_verification(
        id: str, method: str = "sms"
    ) -> str:
        """Start caller-ID verification for a customer-brought number

        Args:
            id: Phone number record ID (from GET /v1/phone-numbers). (required)
            method"""
        client = _get_client()
        try:
            response = client.whatsapp_calling.start_whats_app_caller_id_verification(
                id=id, method=method
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Confirm the caller-ID verification code",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_calling_verify_whats_app_caller_id(id: str, code: str) -> str:
        """Confirm the caller-ID verification code

        Args:
            id: Phone number record ID (from GET /v1/phone-numbers). (required)
            code: (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_calling.verify_whats_app_caller_id(
                id=id, code=code
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # WHATSAPP_FLOWS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List flows",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_flows_list_whats_app_flows(account_id: str) -> str:
        """List flows

        Args:
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_flows.list_whats_app_flows(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create flow",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_flows_create_whats_app_flow(
        account_id: str,
        name: str,
        categories: list[str] | None,
        clone_flow_id: str | None = None,
        as_version: bool | None = None,
    ) -> str:
        """Create flow

        Args:
            account_id: WhatsApp social account ID (required)
            name: Flow display name (required)
            categories: Flow categories (required)
            clone_flow_id: Optional: ID of an existing flow to clone the Flow JSON from
            as_version: When cloning, true keeps the clone in cloneFlowId's version lineage (auto-numbered next version); false/absent creates an independent flow. Ignored without cloneFlowId."""
        client = _get_client()
        try:
            response = client.whatsapp_flows.create_whats_app_flow(
                account_id=account_id,
                name=name,
                categories=categories,
                clone_flow_id=clone_flow_id,
                as_version=as_version,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get flow",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_flows_get_whats_app_flow(
        flow_id: str, account_id: str, fields: str | None = None
    ) -> str:
        """Get flow

        Args:
            flow_id: Flow ID (required)
            account_id: WhatsApp social account ID (required)
            fields: Comma-separated fields to return (default: id,name,status,categories,validation_errors,json_version,preview,data_api_version,endpoint_uri)"""
        client = _get_client()
        try:
            response = client.whatsapp_flows.get_whats_app_flow(
                flow_id=flow_id, account_id=account_id, fields=fields
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update flow",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_flows_update_whats_app_flow(
        flow_id: str,
        account_id: str,
        name: str | None = None,
        categories: list[str] | None = None,
    ) -> str:
        """Update flow

        Args:
            flow_id: Flow ID (required)
            account_id: WhatsApp social account ID (required)
            name: New flow name
            categories"""
        client = _get_client()
        try:
            response = client.whatsapp_flows.update_whats_app_flow(
                flow_id=flow_id, account_id=account_id, name=name, categories=categories
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete flow",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_flows_delete_whats_app_flow(flow_id: str, account_id: str) -> str:
        """Delete flow

        Args:
            flow_id: Flow ID (required)
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_flows.delete_whats_app_flow(
                flow_id=flow_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get flow JSON asset",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_flows_get_whats_app_flow_json(flow_id: str, account_id: str) -> str:
        """Get flow JSON asset

        Args:
            flow_id: Flow ID (required)
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_flows.get_whats_app_flow_json(
                flow_id=flow_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Upload flow JSON",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_flows_upload_whats_app_flow_json(
        flow_id: str, account_id: str, flow_json: str
    ) -> str:
        """Upload flow JSON

        Args:
            flow_id: Flow ID (required)
            account_id: WhatsApp social account ID (required)
            flow_json: The Flow JSON content. Pass as a JSON object or a JSON string. (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_flows.upload_whats_app_flow_json(
                flow_id=flow_id, account_id=account_id, flow_json=flow_json
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get flow preview URL",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_flows_get_whats_app_flow_preview(
        flow_id: str, account_id: str, invalidate: bool | None = None
    ) -> str:
        """Get flow preview URL

        Args:
            flow_id: Flow ID (required)
            account_id: WhatsApp social account ID (required)
            invalidate: Mint a fresh preview link (default false)"""
        client = _get_client()
        try:
            response = client.whatsapp_flows.get_whats_app_flow_preview(
                flow_id=flow_id, account_id=account_id, invalidate=invalidate
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List flow versions",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_flows_list_whats_app_flow_versions(
        flow_id: str, account_id: str
    ) -> str:
        """List flow versions

        Args:
            flow_id: Flow ID (required)
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_flows.list_whats_app_flow_versions(
                flow_id=flow_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Publish flow",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_flows_publish_whats_app_flow(flow_id: str, account_id: str) -> str:
        """Publish flow

        Args:
            flow_id: Flow ID (required)
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_flows.publish_whats_app_flow(
                flow_id=flow_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Deprecate flow",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_flows_deprecate_whats_app_flow(flow_id: str, account_id: str) -> str:
        """Deprecate flow

        Args:
            flow_id: Flow ID (required)
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_flows.deprecate_whats_app_flow(
                flow_id=flow_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Send flow message",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_flows_send_whats_app_flow_message(
        account_id: str,
        to: str,
        flow_id: str,
        flow_cta: str,
        body: str,
        flow_action: str = "navigate",
        flow_token: str | None = None,
        flow_action_payload: dict[str, Any] | None = None,
        header: dict[str, Any] | None = None,
        footer: str | None = None,
        draft: bool | None = None,
    ) -> str:
        """Send flow message

        Args:
            account_id: WhatsApp social account ID (required)
            to: Recipient phone number (E.164 format, e.g. +1234567890) (required)
            flow_id: Published flow ID (required)
            flow_cta: CTA button text (e.g. 'Book Now', 'Sign Up') (required)
            flow_action: Action type: navigate opens a screen directly, data_exchange hits your endpoint first
            flow_token: Unique token to correlate responses. If omitted, auto-generated as '<flowId>:<uuid>' so the response can be attributed to this flow in the Flow Responses view.
            flow_action_payload
            body: Message body text (required)
            header
            footer: Optional footer text
            draft: Set true to test an unpublished (DRAFT) flow"""
        client = _get_client()
        try:
            response = client.whatsapp_flows.send_whats_app_flow_message(
                account_id=account_id,
                to=to,
                flow_id=flow_id,
                flow_cta=flow_cta,
                flow_action=flow_action,
                flow_token=flow_token,
                flow_action_payload=flow_action_payload,
                body=body,
                header=header,
                footer=footer,
                draft=draft,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List flow responses",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_flows_list_whats_app_flow_responses(
        account_id: str, flow_id: str | None = None, limit: int = 50
    ) -> str:
        """List flow responses

        Args:
            account_id: WhatsApp social account ID (required)
            flow_id: Scope to responses for this flow
            limit: Max responses to return"""
        client = _get_client()
        try:
            response = client.whatsapp_flows.list_whats_app_flow_responses(
                account_id=account_id, flow_id=flow_id, limit=limit
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # WHATSAPP_PHONE_NUMBERS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get number status",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_phone_numbers_get_whats_app_number_info(account_id: str) -> str:
        """Get number status

        Args:
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.get_whats_app_number_info(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List phone numbers",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_phone_numbers_get_whats_app_phone_numbers(
        status: str | None = None, profile_id: str | None = None
    ) -> str:
        """List phone numbers

            Args:
                status: Filter by status (by default excludes released numbers). NOTE:
        `status=pending_regulatory` returns the "provisioning" view — numbers
        still in review PLUS recently-declined (last 30 days) ones, so a
        failed registration surfaces (with `regulatoryDeclineReason`) instead
        of silently disappearing. Declined numbers can be re-submitted via
        POST /v1/whatsapp/phone-numbers/{id}/remediate. `verifying` is the
        short-lived state after the number is provisioned on our side while
        WhatsApp confirms the activation code; the number is not billed until
        it reaches `active`.
                profile_id: Filter by profile"""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.get_whats_app_phone_numbers(
                status=status, profile_id=profile_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Purchase phone number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_phone_numbers_purchase_whats_app_phone_number(
        profile_id: str,
        country: str = "US",
        purchase_intent_id: str | None = None,
        allow_multiple: bool = False,
    ) -> str:
        """Purchase phone number

        Args:
            profile_id: Profile to associate the number with (required)
            country: ISO 3166-1 alpha-2 country for the number (default US). International numbers require usage-based billing. Tier 3/4 countries return 202 { status: "kyc_required", kycUrl } — the customer must complete KYC at that URL before the number is ordered. See GET /v1/whatsapp/phone-numbers/countries.
            purchase_intent_id: Optional idempotency key. Send the same value when retrying a purchase: if a number was already bought under this key, the API returns { status: "already_purchased", numberId, phoneNumber } instead of provisioning a second number. Generate a fresh key for each genuinely new purchase.
            allow_multiple: Any second purchase within 10 minutes of a previous one is rejected with 409 code PURCHASE_VELOCITY as duplicate protection. Pass true to confirm the additional purchase is intentional (e.g. bulk provisioning)."""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.purchase_whats_app_phone_number(
                profile_id=profile_id,
                country=country,
                purchase_intent_id=purchase_intent_id,
                allow_multiple=allow_multiple,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List offerable number countries",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_phone_numbers_list_whats_app_number_countries() -> str:
        """List offerable number countries"""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.list_whats_app_number_countries()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Search available numbers",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_phone_numbers_search_available_whats_app_numbers(
        country: str = "US",
        type: str | None = None,
        prefix: str | None = None,
        locality: str | None = None,
        contains: str | None = None,
        limit: int = 20,
    ) -> str:
        """Search available numbers

        Args:
            country
            type: Number type; defaults to the country's WhatsApp-safe type
            prefix: Area code
            locality: City
            contains: Pattern to match within the number
            limit"""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.search_available_whats_app_numbers(
                country=country,
                type=type,
                prefix=prefix,
                locality=locality,
                contains=contains,
                limit=limit,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Check country availability",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_phone_numbers_check_whats_app_number_availability(
        country: str, number_type: str | None = None, sms: bool | None = None
    ) -> str:
        """Check country availability

        Args:
            country: ISO-2 country code. (required)
            number_type: Check a specific offered type (stock and address constraints are per type). Omitted = the country's default type.
            sms: Pass true when the buyer wants SMS: availability, areas, and areaOptions then describe the SMS-capable pool (an SMS purchase orders from it), not the wider voice-only pool."""
        client = _get_client()
        try:
            response = (
                client.whatsapp_phone_numbers.check_whats_app_number_availability(
                    country=country, number_type=number_type, sms=sms
                )
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get KYC form spec",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_phone_numbers_get_whats_app_number_kyc_form(
        country: str, profile_id: str
    ) -> str:
        """Get KYC form spec

        Args:
            country: (required)
            profile_id: (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.get_whats_app_number_kyc_form(
                country=country, profile_id=profile_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Submit KYC",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_phone_numbers_submit_whats_app_number_kyc(
        profile_id: str,
        country: str,
        submission_id: str | None = None,
        quantity: int = 1,
        reuse: bool | None = None,
        reuse_option_id: str | None = None,
        reuse_from: str | None = None,
        area_code: str | None = None,
        end_user_first_name: str | None = None,
        end_user_last_name: str | None = None,
        values: dict[str, Any] | None = None,
        documents: list[dict[str, Any]] | None = None,
        address: dict[str, Any] | None = None,
    ) -> str:
        """Submit KYC

        Args:
            profile_id: (required)
            country: (required)
            submission_id: Idempotency token for this submission attempt. A retry/double-submit with the same token returns the same number; omit and each call creates a new number.
            quantity: Provision several same-country numbers from one submission (1-5). The single verification covers all of them; each number is billed only when it activates. Numbers that fail to order are skipped (best-effort). With `areaCode`, a quantity above that area's live stock is rejected with a 400.
            reuse: Reuse a prior approved verification for this country (skips document/field collection; places the order immediately).
            reuse_option_id: Which reusable verification to use (GET reusable.options[].id). The unambiguous selection key. Omitted = the approved default. No match = 409.
            reuse_from: Legacy fallback for `reuseOptionId`: the source phone number (GET reusable.options[].fromPhoneNumber). Ambiguous when a number labels two verifications — prefer `reuseOptionId`. Omitted = the approved default. No match = 409.
            area_code: Area code (NDC) the number must be in. Hard constraint: an empty area pool fails with 409 code AREA_CODE_UNAVAILABLE instead of ordering from another area. Omit for any area. Options come from GET /v1/phone-numbers/availability (areaOptions); the purchase 202 kycUrl echoes the areaCode picked at purchase time so it can be passed here.
            end_user_first_name: End user's legal first name. Required when the country has an action/ID-verification (Onfido) requirement.
            end_user_last_name: End user's legal last name. Same condition as endUserFirstName.
            values: requirementId → textual value
            documents: One per document requirement. Each is EITHER inline base64 OR a `documentId` returned by POST /v1/whatsapp/phone-numbers/kyc/upload-document (use the upload endpoint for large files to stay under the request-size limit).
            address"""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.submit_whats_app_number_kyc(
                profile_id=profile_id,
                country=country,
                submission_id=submission_id,
                quantity=quantity,
                reuse=reuse,
                reuse_option_id=reuse_option_id,
                reuse_from=reuse_from,
                area_code=area_code,
                end_user_first_name=end_user_first_name,
                end_user_last_name=end_user_last_name,
                values=values,
                documents=documents,
                address=address,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Upload a KYC document",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_phone_numbers_upload_whats_app_number_kyc_document() -> str:
        """Upload a KYC document"""
        client = _get_client()
        try:
            response = (
                client.whatsapp_phone_numbers.upload_whats_app_number_kyc_document()
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Pre-validate KYC address",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_phone_numbers_validate_whats_app_number_kyc_address(
        country: str,
        street_address: str,
        locality: str,
        postal_code: str,
        administrative_area: str | None = None,
    ) -> str:
        """Pre-validate KYC address

        Args:
            country: ISO 3166-1 alpha-2 country code. (required)
            street_address: (required)
            locality: City / town. (required)
            administrative_area: State / province / region. When omitted, the pre-check is skipped (the final submit still validates).
            postal_code: (required)"""
        client = _get_client()
        try:
            response = (
                client.whatsapp_phone_numbers.validate_whats_app_number_kyc_address(
                    country=country,
                    street_address=street_address,
                    locality=locality,
                    administrative_area=administrative_area,
                    postal_code=postal_code,
                )
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a hosted KYC link",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_phone_numbers_create_whats_app_number_kyc_link(
        profile_id: str,
        country: str,
        area_code: str | None = None,
        branding: dict[str, Any] | None = None,
        redirect_url: str | None = None,
    ) -> str:
        """Create a hosted KYC link

            Args:
                profile_id: (required)
                country: ISO 3166-1 alpha-2 country code (must be a regulated/KYC country). (required)
                area_code: Area code (NDC) the eventual number must be in. Hard constraint carried by the link; the end customer filling the form makes no area choice. Options come from GET /v1/phone-numbers/availability (areaOptions).
                branding: Optional white-label of the hosted page the end customer sees.
                redirect_url: Where to send the end customer's browser after a successful
        submit. On completion Zernio appends `kyc=submitted` and
        `country=<ISO-2>` as query params. When omitted, the hosted
        page shows a built-in confirmation screen instead."""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.create_whats_app_number_kyc_link(
                profile_id=profile_id,
                country=country,
                area_code=area_code,
                branding=branding,
                redirect_url=redirect_url,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Move a number to another profile",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_phone_numbers_move_whats_app_number_to_profile(
        id: str, profile_id: str
    ) -> str:
        """Move a number to another profile

        Args:
            id: WhatsAppPhoneNumber id. (required)
            profile_id: Destination profile id. Must belong to the same team. (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.move_whats_app_number_to_profile(
                id=id, profile_id=profile_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get declined requirements",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_phone_numbers_get_whats_app_number_remediation(id: str) -> str:
        """Get declined requirements

        Args:
            id: WhatsAppPhoneNumber id. (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.get_whats_app_number_remediation(
                id=id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Resubmit a declined number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_phone_numbers_remediate_whats_app_number(
        id: str,
        values: dict[str, Any] | None = None,
        documents: list[dict[str, Any]] | None = None,
        address: dict[str, Any] | None = None,
    ) -> str:
        """Resubmit a declined number

        Args:
            id: (required)
            values
            documents
            address: Same shape as the KYC submit address."""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.remediate_whats_app_number(
                id=id, values=values, documents=documents, address=address
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get phone number",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_phone_numbers_get_whats_app_phone_number(phone_number_id: str) -> str:
        """Get phone number

        Args:
            phone_number_id: Phone number record ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.get_whats_app_phone_number(
                phone_number_id=phone_number_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Release phone number",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_phone_numbers_release_whats_app_phone_number(
        phone_number_id: str,
    ) -> str:
        """Release phone number

        Args:
            phone_number_id: Phone number record ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.release_whats_app_phone_number(
                phone_number_id=phone_number_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # WHATSAPP_SANDBOX

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List your sandbox sessions",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_sandbox_list_whats_app_sandbox_sessions() -> str:
        """List your sandbox sessions"""
        client = _get_client()
        try:
            response = client.whatsapp_sandbox.list_whats_app_sandbox_sessions()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Start a sandbox activation",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_sandbox_create_whats_app_sandbox_session(phone: str) -> str:
        """Start a sandbox activation

        Args:
            phone: Recipient phone in international format. Digits, spaces, dashes and a leading `+` are all accepted; the server normalizes to E.164 digits-only. (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_sandbox.create_whats_app_sandbox_session(
                phone=phone
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Revoke a sandbox session",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_sandbox_delete_whats_app_sandbox_session(session_id: str) -> str:
        """Revoke a sandbox session

        Args:
            session_id: The session id returned by POST /v1/whatsapp/sandbox/sessions. (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_sandbox.delete_whats_app_sandbox_session(
                session_id=session_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # WHATSAPP_TEMPLATES

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Look up a library template",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_templates_get_whats_app_library_template(
        account_id: str, name: str
    ) -> str:
        """Look up a library template

        Args:
            account_id: WhatsApp social account ID (required)
            name: Exact library template name (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_templates.get_whats_app_library_template(
                account_id=account_id, name=name
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # WORKFLOWS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List workflows",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def workflows_list_workflows(
        profile_id: str | None = None,
        status: str | None = None,
        limit: int = 50,
        skip: int = 0,
    ) -> str:
        """List workflows

        Args:
            profile_id: Filter by profile. Omit to list across all profiles
            status
            limit
            skip"""
        client = _get_client()
        try:
            response = client.workflows.list_workflows(
                profile_id=profile_id, status=status, limit=limit, skip=skip
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create workflow",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def workflows_create_workflow(
        profile_id: str,
        account_id: str,
        name: str,
        platform: str = "whatsapp",
        description: str | None = None,
        nodes: list[dict[str, Any]] | None = None,
        edges: list[dict[str, Any]] | None = None,
        entry_node_id: str | None = None,
    ) -> str:
        """Create workflow

        Args:
            profile_id: (required)
            account_id: (required)
            platform
            name: (required)
            description
            nodes
            edges
            entry_node_id: The trigger node id; derived from the single trigger node if omitted"""
        client = _get_client()
        try:
            response = client.workflows.create_workflow(
                profile_id=profile_id,
                account_id=account_id,
                platform=platform,
                name=name,
                description=description,
                nodes=nodes,
                edges=edges,
                entry_node_id=entry_node_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get workflow with graph",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def workflows_get_workflow(workflow_id: str) -> str:
        """Get workflow with graph

        Args:
            workflow_id: (required)"""
        client = _get_client()
        try:
            response = client.workflows.get_workflow(workflow_id=workflow_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Update workflow",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def workflows_update_workflow(
        workflow_id: str,
        name: str | None = None,
        description: str | None = None,
        nodes: list[dict[str, Any]] | None = None,
        edges: list[dict[str, Any]] | None = None,
        entry_node_id: str | None = None,
        account_id: str | None = None,
    ) -> str:
        """Update workflow

        Args:
            workflow_id: (required)
            name
            description
            nodes
            edges
            entry_node_id
            account_id: Reassign the workflow to a different `SocialAccount`. `platform` and `profileId` are derived server-side from the new account (the client never sends them directly). The account must belong to the caller's workspace and be on a workflow-supported platform (whatsapp, instagram, facebook, telegram, twitter, bluesky, reddit). Changing this triggers a graph revalidation against the new platform."""
        client = _get_client()
        try:
            response = client.workflows.update_workflow(
                workflow_id=workflow_id,
                name=name,
                description=description,
                nodes=nodes,
                edges=edges,
                entry_node_id=entry_node_id,
                account_id=account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Delete workflow",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def workflows_delete_workflow(workflow_id: str) -> str:
        """Delete workflow

        Args:
            workflow_id: (required)"""
        client = _get_client()
        try:
            response = client.workflows.delete_workflow(workflow_id=workflow_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Activate workflow",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def workflows_activate_workflow(workflow_id: str) -> str:
        """Activate workflow

        Args:
            workflow_id: (required)"""
        client = _get_client()
        try:
            response = client.workflows.activate_workflow(workflow_id=workflow_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Pause workflow",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def workflows_pause_workflow(workflow_id: str) -> str:
        """Pause workflow

        Args:
            workflow_id: (required)"""
        client = _get_client()
        try:
            response = client.workflows.pause_workflow(workflow_id=workflow_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List workflow runs",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def workflows_list_workflow_executions(
        workflow_id: str, status: str | None = None, limit: int = 25, skip: int = 0
    ) -> str:
        """List workflow runs

        Args:
            workflow_id: (required)
            status
            limit
            skip"""
        client = _get_client()
        try:
            response = client.workflows.list_workflow_executions(
                workflow_id=workflow_id, status=status, limit=limit, skip=skip
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Manually start a workflow run",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def workflows_trigger_workflow(
        workflow_id: str,
        to: str | None = None,
        conversation_id: str | None = None,
        text: str | None = None,
    ) -> str:
        """Manually start a workflow run

        Args:
            workflow_id: (required)
            to: Recipient phone (WhatsApp only)
            conversation_id: An existing conversation to run in (required for non-WhatsApp workflows)
            text: Simulated inbound text, seeded as the run's lastMessage variable"""
        client = _get_client()
        try:
            response = client.workflows.trigger_workflow(
                workflow_id=workflow_id,
                to=to,
                conversation_id=conversation_id,
                text=text,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get an execution's timeline",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def workflows_list_workflow_execution_events(
        workflow_id: str, execution_id: str
    ) -> str:
        """Get an execution's timeline

        Args:
            workflow_id: (required)
            execution_id: (required)"""
        client = _get_client()
        try:
            response = client.workflows.list_workflow_execution_events(
                workflow_id=workflow_id, execution_id=execution_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Duplicate a workflow",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def workflows_duplicate_workflow(workflow_id: str) -> str:
        """Duplicate a workflow

        Args:
            workflow_id: (required)"""
        client = _get_client()
        try:
            response = client.workflows.duplicate_workflow(workflow_id=workflow_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List a workflow's version history",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def workflows_list_workflow_versions(workflow_id: str) -> str:
        """List a workflow's version history

        Args:
            workflow_id: (required)"""
        client = _get_client()
        try:
            response = client.workflows.list_workflow_versions(workflow_id=workflow_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a specific workflow version",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def workflows_get_workflow_version(workflow_id: str, version: int) -> str:
        """Get a specific workflow version

        Args:
            workflow_id: (required)
            version: (required)"""
        client = _get_client()
        try:
            response = client.workflows.get_workflow_version(
                workflow_id=workflow_id, version=version
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Restore a workflow version",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def workflows_restore_workflow_version(workflow_id: str, version: int) -> str:
        """Restore a workflow version

        Args:
            workflow_id: (required)
            version: (required)"""
        client = _get_client()
        try:
            response = client.workflows.restore_workflow_version(
                workflow_id=workflow_id, version=version
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"
