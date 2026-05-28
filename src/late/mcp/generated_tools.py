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
        include_over_limit: bool = False,
        page: int | None = None,
        limit: int | None = None,
    ) -> str:
        """List accounts

        Args:
            profile_id: Filter accounts by profile ID
            platform: Filter accounts by platform (e.g. "instagram", "twitter").
            include_over_limit: When true, includes accounts from over-limit profiles.
            page: Page number (1-based). When provided with limit, enables server-side pagination. Omit for all accounts.
            limit: Page size. Required alongside page for pagination."""
        client = _get_client()
        try:
            response = client.accounts.list_accounts(
                profile_id=profile_id,
                platform=platform,
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
            title="Move account to a different profile",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def accounts_move_account_to_profile(account_id: str, profile_id: str) -> str:
        """Move account to a different profile

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
            uri: New action URL
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
    ) -> str:
        """Batch get reviews

        Args:
            account_id: (required)
            location_names: Array of full location resource names (e.g. ['accounts/123/locations/456']) (required)
            page_size: Number of reviews per page (max 50)
            page_token: Pagination token from previous response"""
        client = _get_client()
        try:
            response = client.accounts.batch_get_google_business_reviews(
                account_id=account_id,
                location_names=location_names,
                page_size=page_size,
                page_token=page_token,
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
            type: Filter to one audience type. `saved_targeting` returns stored TargetingSpec audiences (each item carries a `spec`); the other types return uploaded/derived audiences."""
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
            title="List campaigns",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ad_campaigns_list_ad_campaigns(
        page: int = 1,
        limit: int = 20,
        source: str = "all",
        platform: str | None = None,
        status: str | None = None,
        ad_account_id: str | None = None,
        account_id: str | None = None,
        profile_id: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
    ) -> str:
        """List campaigns

        Args:
            page: Page number
            limit
            source: `all` (default) returns both Zernio-created ads and those discovered from the platform's ad manager — matches the web UI's default view. Pass `zernio` to restrict to isExternal=false only. Status is NOT filtered by default — use the `status` param for that.
            platform
            status: Filter by derived campaign status (post-aggregation)
            ad_account_id: Platform ad account ID (e.g. act_123 for Meta)
            account_id: Social account ID
            profile_id: Profile ID
            from_date: Start of metrics date range (YYYY-MM-DD, inclusive). Defaults to 90 days ago when both date params are omitted.
            to_date: End of metrics date range (YYYY-MM-DD, inclusive). Defaults to today. Max 730-day range."""
        client = _get_client()
        try:
            response = client.ad_campaigns.list_ad_campaigns(
                page=page,
                limit=limit,
                source=source,
                platform=platform,
                status=status,
                ad_account_id=ad_account_id,
                account_id=account_id,
                profile_id=profile_id,
                from_date=from_date,
                to_date=to_date,
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
            title="Update a campaign (budget and/or bid strategy)",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ad_campaigns_update_ad_campaign(
        campaign_id: str,
        platform: str,
        budget: dict[str, Any] | None = None,
        bid_strategy: str | None = None,
    ) -> str:
        """Update a campaign (budget and/or bid strategy)

        Args:
            campaign_id: Platform campaign ID (required)
            platform: (required)
            budget
            bid_strategy: Campaign-level default. Ad sets inherit this unless they override."""
        client = _get_client()
        try:
            response = client.ad_campaigns.update_ad_campaign(
                campaign_id=campaign_id,
                platform=platform,
                budget=budget,
                bid_strategy=bid_strategy,
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
    def ad_campaigns_delete_ad_campaign(campaign_id: str, platform: str) -> str:
        """Delete a campaign

        Args:
            campaign_id: Platform campaign ID (required)
            platform: (required)"""
        client = _get_client()
        try:
            response = client.ad_campaigns.delete_ad_campaign(
                campaign_id=campaign_id, platform=platform
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
            status_option
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
            title="Update an ad set (budget, status, and/or bid strategy)",
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
        bid_strategy: str | None = None,
        bid_amount: float | None = None,
        roas_average_floor: float | None = None,
    ) -> str:
        """Update an ad set (budget, status, and/or bid strategy)

            Args:
                ad_set_id: Platform ad set ID (required)
                platform: (required)
                budget: Omit if not updating budget
                status: Omit if not toggling delivery state
                bid_strategy: Ad-set-level bid strategy. Overrides the campaign-level default.
        Supported on Meta (facebook, instagram) and TikTok. On TikTok the
        Meta-style enum is mapped to bid_type / bid_price / deep_bid_type
        automatically. Other platforms (linkedin, pinterest, google, twitter)
        return 501 Not Implemented when bidStrategy is set.
                bid_amount: Bid cap in WHOLE currency units (USD: 5 = $5.00; JPY: 100 = ¥100). Required when
        bidStrategy is LOWEST_COST_WITH_BID_CAP or COST_CAP. Internally converted to Meta's
        smallest-denomination integer.
                roas_average_floor: Minimum ROAS as a decimal multiplier (2.0 = 2.0x). Required when bidStrategy is
        LOWEST_COST_WITH_MIN_ROAS. Sent to Meta as `bid_constraints.roas_average_floor` × 10000."""
        client = _get_client()
        try:
            response = client.ad_campaigns.update_ad_set(
                ad_set_id=ad_set_id,
                platform=platform,
                budget=budget,
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
        account_id: str | None = None,
        profile_id: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        sort: str = "newest",
    ) -> str:
        """Get campaign tree

        Args:
            page: Page number
            limit: Campaigns per page
            source: `all` (default) returns both Zernio-created ads and those discovered from the platform's ad manager — matches the web UI's default view. Pass `zernio` to restrict to isExternal=false only. Status is NOT filtered by default — use the `status` param for that.
            platform
            status: Filter by derived campaign status (post-aggregation)
            ad_account_id: Platform ad account ID
            account_id: Social account ID
            profile_id: Profile ID
            from_date: Start of metrics date range (YYYY-MM-DD). Defaults to 90 days ago.
            to_date: End of metrics date range (YYYY-MM-DD). Defaults to today. Max 730-day range.
            sort: Campaign-level sort order. `newest` (default) / `oldest` order by the campaign's newest-ad createdAt. `spend_desc` / `spend_asc` order by aggregated spend in the requested date range; campaigns with no spend land at the end."""
        client = _get_client()
        try:
            response = client.ad_campaigns.get_ad_tree(
                page=page,
                limit=limit,
                source=source,
                platform=platform,
                status=status,
                ad_account_id=ad_account_id,
                account_id=account_id,
                profile_id=profile_id,
                from_date=from_date,
                to_date=to_date,
                sort=sort,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get daily aggregate ad metrics for an account",
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
        """Get daily aggregate ad metrics for an account

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

    # ADS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List ads",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ads_list_ads(
        page: int = 1,
        limit: int = 50,
        source: str = "all",
        status: str | None = None,
        platform: str | None = None,
        account_id: str | None = None,
        ad_account_id: str | None = None,
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
            profile_id: Profile ID
            campaign_id: Platform campaign ID (filter ads within a campaign)
            platform_ad_id: Meta ad ID. Returns the ad with this platform-side ad ID.
            effective_object_story_id: Facebook `{pageId}_{postId}` of the post the ad's engagement lives on (Meta `effective_object_story_id`). Use to map a Business-Manager-visible post back to the Zernio ad.
            effective_instagram_media_id: Instagram media ID of the boosted post (Meta `effective_instagram_media_id`). Use to map a Business-Manager-visible IG post back to the Zernio ad.
            from_date: Start of metrics date range (YYYY-MM-DD). Defaults to 90 days ago.
            to_date: End of metrics date range (YYYY-MM-DD). Defaults to today. Max 730-day range."""
        client = _get_client()
        try:
            response = client.ads.list_ads(
                page=page,
                limit=limit,
                source=source,
                status=status,
                platform=platform,
                account_id=account_id,
                ad_account_id=ad_account_id,
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
            title="Get ad details",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ads_get_ad(ad_id: str) -> str:
        """Get ad details

           Args:
               ad_id: Zernio `_id` (hex), Meta `platformAdId` (numeric), or one of the creative's effective story/media IDs. See description for details.
        (required)"""
        client = _get_client()
        try:
            response = client.ads.get_ad(ad_id=ad_id)
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
    def ads_update_ad(
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
                targeting: Meta + TikTok only. Pinterest / X / LinkedIn / Google return 501.
                creative: Replace the ad's creative. Meta + TikTok only.

        - **Meta**: requires `headline`, `body`, `callToAction`, `linkUrl`, `imageUrl`. The
          ad's existing creative is replaced via a new `/act_X/adcreatives` upload + ad
          update. The old creative is retained on the ad account for historical reporting.
        - **TikTok**: patch-style. Pass any subset; `headline` is ignored (TikTok creatives
          have no headline slot). `body` becomes the in-feed `ad_text`; `linkUrl` becomes
          `landing_page_url`; `videoUrl` triggers a fresh upload.
                name"""
        client = _get_client()
        try:
            response = client.ads.update_ad(
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
    def ads_delete_ad(ad_id: str) -> str:
        """Cancel an ad

        Args:
            ad_id: (required)"""
        client = _get_client()
        try:
            response = client.ads.delete_ad(ad_id=ad_id)
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
    def ads_get_ad_analytics(
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
            breakdowns: Comma-separated breakdown dimensions. Meta: age, gender, country, publisher_platform, device_platform, region. TikTok: gender, age, country_code, platform, ac, language."""
        client = _get_client()
        try:
            response = client.ads.get_ad_analytics(
                ad_id=ad_id, from_date=from_date, to_date=to_date, breakdowns=breakdowns
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List comments on an ad",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ads_get_ad_comments(
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
            response = client.ads.get_ad_comments(
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
    def ads_list_ads_business_centers(account_id: str) -> str:
        """List TikTok Business Centers

        Args:
            account_id: ID of the `tiktokads` (or parent `tiktok` posting) SocialAccount (required)"""
        client = _get_client()
        try:
            response = client.ads.list_ads_business_centers(account_id=account_id)
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
    def ads_list_ad_accounts(
        account_id: str, ad_account_id: str | None = None, limit: int | None = None
    ) -> str:
        """List ad accounts

        Args:
            account_id: Social account ID (required)
            ad_account_id: Filter response to a single platform ad account ID (e.g. `act_123` for Meta, advertiser_id for TikTok). Returns at most one item.
            limit: Clamp the returned `accounts[]` length. Useful for typeahead pickers on agency tokens with hundreds of advertisers."""
        client = _get_client()
        try:
            response = client.ads.list_ad_accounts(
                account_id=account_id, ad_account_id=ad_account_id, limit=limit
            )
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
    def ads_boost_post(
        account_id: str,
        ad_account_id: str,
        name: str,
        goal: str,
        budget: dict[str, Any] | None,
        post_id: str | None = None,
        platform_post_id: str | None = None,
        currency: str | None = None,
        schedule: dict[str, Any] | None = None,
        targeting: dict[str, Any] | None = None,
        bid_strategy: str | None = None,
        bid_amount: float | None = None,
        roas_average_floor: float | None = None,
        tracking: dict[str, Any] | None = None,
        special_ad_categories: list[str] | None = None,
        link_url: str | None = None,
        call_to_action: str | None = None,
        spark_auth_code: str | None = None,
        dsa_beneficiary: str | None = None,
        dsa_payor: str | None = None,
    ) -> str:
        """Boost post as ad

            Args:
                post_id: Zernio post ID (provide this or platformPostId)
                platform_post_id: Platform post ID (alternative to postId)
                account_id: Social account ID (required)
                ad_account_id: Platform ad account ID (required)
                name: (required)
                goal: Available goals vary by platform. Meta (Facebook/Instagram) and TikTok support all 7. LinkedIn supports all except app_promotion. Twitter/X supports engagement, traffic, awareness, video_views, app_promotion. Pinterest and Google Ads support only engagement, traffic, awareness, video_views. (required)
                budget: (required)
                currency
                schedule
                targeting
                bid_strategy: Meta bid strategy applied to the ad set. On TikTok, mapped to
        `bid_type` / `bid_price` / `deep_bid_type` automatically.
                bid_amount: Bid cap in WHOLE currency units (USD: 5 = $5.00; JPY: 100 = ¥100). Required when
        `bidStrategy` is `LOWEST_COST_WITH_BID_CAP` or `COST_CAP`. Backward-compat: providing
        `bidAmount` without `bidStrategy` is treated as `LOWEST_COST_WITH_BID_CAP`.
                roas_average_floor: Minimum ROAS as a decimal multiplier (e.g. 2.0 = 2.0x ROAS). Required when
        `bidStrategy` is `LOWEST_COST_WITH_MIN_ROAS`. Sent to Meta as
        `bid_constraints.roas_average_floor` × 10000 (Meta uses fixed-point integers).
                tracking: Meta only. Tracking specs (pixel, URL tags).
                special_ad_categories: Meta only. Required for housing, employment, credit, or political ads.
                link_url: TikTok-only. Custom destination URL for the Spark Ad. Without this, TikTok
        Spark Ads have no clickable destination — required for traffic / conversion
        objectives. Maps to `landing_page_url` on the creative entry of /v2/ad/create/
        (TikTok SDK `AdcreateCreatives.landing_page_url`). Ignored on Meta / LinkedIn /
        Pinterest / X / Google (those infer the destination from the boosted post).
                call_to_action: TikTok-only. Call-to-action button label on the Spark Ad creative (e.g.
        `LEARN_MORE`, `SHOP_NOW`, `DOWNLOAD_NOW`, `SIGN_UP`, `WATCH_NOW`). Maps to
        `call_to_action` on the creative entry of /v2/ad/create/. Pass-through —
        the platform validates the value. See TikTok's "Enumeration - Call-to-Action"
        reference for the full list.
                spark_auth_code: TikTok-only. Spark Code (creator's `auth_code`) authorizing cross-creator
        Spark Ads — the advertiser can boost a video owned by a DIFFERENT TikTok
        account. Without this, boosts are limited to videos owned by the same
        account running the ads (same-BC creators only). The creator generates the
        code in their TikTok app's Promote settings and shares it with the
        advertiser. Maps to `auth_code` on the creative entry of /v2/ad/create/.
                dsa_beneficiary: Name of the legal entity benefiting from the ad.
        Required by Meta when targeting EU users (DSA Article 26).
        Not enforced at schema level; enforced server-side when targeting intersects EU member states.
                dsa_payor: Name of the legal entity paying for the ad.
        Required by Meta when targeting EU users (DSA Article 26).
        Note Meta API spelling: dsa_payor (not dsa_payer)."""
        client = _get_client()
        try:
            response = client.ads.boost_post(
                post_id=post_id,
                platform_post_id=platform_post_id,
                account_id=account_id,
                ad_account_id=ad_account_id,
                name=name,
                goal=goal,
                budget=budget,
                currency=currency,
                schedule=schedule,
                targeting=targeting,
                bid_strategy=bid_strategy,
                bid_amount=bid_amount,
                roas_average_floor=roas_average_floor,
                tracking=tracking,
                special_ad_categories=special_ad_categories,
                link_url=link_url,
                call_to_action=call_to_action,
                spark_auth_code=spark_auth_code,
                dsa_beneficiary=dsa_beneficiary,
                dsa_payor=dsa_payor,
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
    def ads_create_standalone_ad(
        account_id: str,
        ad_account_id: str,
        name: str,
        goal: str | None = None,
        budget_amount: float | None = None,
        budget_type: str | None = None,
        currency: str | None = None,
        headline: str | None = None,
        long_headline: str | None = None,
        body: str | None = None,
        call_to_action: str | None = None,
        link_url: str | None = None,
        lead_gen_form_id: str | None = None,
        image_url: str | None = None,
        images: dict[str, Any] | None = None,
        video: dict[str, Any] | None = None,
        creatives: list[dict[str, Any]] | None = None,
        ad_set_id: str | None = None,
        business_name: str | None = None,
        board_id: str | None = None,
        organization_id: str | None = None,
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
        saved_targeting_id: str | None = None,
        special_ad_categories: list[str] | None = None,
        end_date: str | None = None,
        audience_id: str | None = None,
        campaign_type: str = "display",
        keywords: list[str] | None = None,
        additional_headlines: list[str] | None = None,
        additional_descriptions: list[str] | None = None,
        advantage_audience: int | None = None,
        attribution_spec: list[dict[str, Any]] | None = None,
        gender: str = "all",
        bid_strategy: str | None = None,
        bid_amount: float | None = None,
        roas_average_floor: float | None = None,
        dsa_beneficiary: str | None = None,
        dsa_payor: str | None = None,
        brand_identity: dict[str, Any] | None = None,
        identity_type: str | None = None,
        promoted_object: dict[str, Any] | None = None,
    ) -> str:
        """Create standalone ad

            Args:
                account_id: (required)
                ad_account_id: (required)
                name: (required)
                goal: Required on legacy + multi-creative shapes. Inherited from the ad set on the attach shape. Available goals vary by platform. Meta-specific: `conversions` requires `promotedObject.pixelId` + `promotedObject.customEventType`; `app_promotion` requires `promotedObject.applicationId` + `promotedObject.objectStoreUrl`; `lead_generation` accepts an optional `promotedObject.pageId` (auto-filled from the connected Page when omitted). TikTok-specific: `conversions` (website-conversion ad group) requires `promotedObject.pixelId` (your TikTok Pixel ID) and accepts an optional `promotedObject.customEventType` (a TikTok `optimization_event` code like `ON_WEB_ORDER`, `INITIATE_ORDER`, `ON_WEB_REGISTER`, `FORM`); to inherit a pixel + event from an existing ad group, pass `adSetId` instead. LinkedIn-specific: `engagement`, `traffic`, `awareness`, and `video_views` are supported for standalone ads (creates a Direct Sponsored Content single image or single video ad). `traffic` requires `linkUrl`; `video_views` requires the `video` field. For `lead_generation` / `conversions` on LinkedIn — or to promote an existing post — use `POST /v1/ads/boost`.
                budget_amount: Required on legacy + multi-creative shapes. Inherited on attach.
                budget_type: Required on legacy + multi-creative shapes. Inherited on attach.
                currency
                headline: Required for Meta, Google, Pinterest, and LinkedIn on legacy + attach shapes (skip for multi-creative — use `creatives[].headline`). Ignored for TikTok and X/Twitter. Max: Meta=255, Google=30, Pinterest=100, LinkedIn=400. On LinkedIn this is the ad's headline (the bold text on the creative); for traffic ads it's the link card title.
                long_headline: Google Display only — defaults to `headline` if omitted. On LinkedIn, reused as the optional secondary description text on traffic (link) ads; omitted if not provided.
                body: Required on legacy + attach shapes. For X/Twitter this is the tweet text (max 280 chars including a ~24-char URL when `linkUrl` is set). On LinkedIn this is the post commentary (the intro text shown above the ad). Max: Google=90, Pinterest=500.
                call_to_action: Required on legacy + attach shapes for Meta. Honoured on TikTok (passes through to the Spark Ad creative's `call_to_action`) and on LinkedIn (the CTA button on the ad; defaults to LEARN_MORE when `linkUrl` is set). LinkedIn accepts: LEARN_MORE, SIGN_UP, DOWNLOAD, SUBSCRIBE, REGISTER, JOIN, ATTEND, REQUEST_DEMO, VIEW_QUOTE, APPLY, SEE_MORE, SHOP_NOW, BUY_NOW. Ignored by Google, Pinterest, and X/Twitter.
                link_url: Required on legacy + attach shapes (skip for multi-creative). On LinkedIn it's the ad's destination URL; required for `traffic` ads, optional for `engagement` / `awareness`. NOT required when `goal` is `lead_generation` (the ad opens a Lead Gen form instead of a destination).
                lead_gen_form_id: Meta Lead Gen forms only (facebook/instagram). The leadgen_forms ID to attach to the ad's creative — create one via POST /v1/ads/lead-forms. REQUIRED when `goal` is `lead_generation`; ignored otherwise. The ad set's promoted_object.page_id + LEAD_GENERATION optimization are derived automatically from the goal.
                image_url: Image creative for Meta/Google/Pinterest/LinkedIn on legacy + attach shapes (mutually exclusive with `video`). Required for LinkedIn ads unless `video` is set. Not required for Google Search campaigns. For TikTok, this field carries the VIDEO URL (the TikTok ads endpoint is video-only; the field retains the `imageUrl` name for cross-platform consistency). Ignored for X/Twitter. For Google Display, treated as the landscape image (alias of `images.landscape`); supply `images.square` alongside or the request is rejected. For LinkedIn the image is uploaded to LinkedIn under the authoring Company Page (see `organizationId`); recommended ratio 1.91:1 (e.g. 1200×627).
                images: Google Display (Responsive Display Ads) only. Google RDA requires both a landscape (1.91:1) and a square (1:1) marketing image; sending only one is rejected upstream as 'Too few.' (NOT_ENOUGH_*_MARKETING_IMAGE_ASSET). Supply both URLs here. Either this field or the legacy `imageUrl` can provide the landscape, but `square` has no legacy counterpart so it must be set here for Display.
                video: Meta (facebook, instagram) and LinkedIn. When set, creates a VIDEO ad on the legacy (or, for Meta, attach) shape. Mutually exclusive with `imageUrl`. For Meta multi-creative, set `video` per entry inside `creatives[]` instead. For LinkedIn the video is uploaded to LinkedIn under the authoring Company Page (see `organizationId`) and the campaign format is set to SINGLE_VIDEO; LinkedIn ignores `thumbnailUrl` (it auto-generates the poster frame) — supply MP4 H.264/AAC, 3s-30min, 75KB-500MB.
                creatives: Meta-only. When present, switches to the multi-creative shape:
        creates 1 campaign + 1 ad set + N ads (one per entry here).
        Top-level `headline` / `body` / `imageUrl` / `linkUrl` /
        `callToAction` are ignored in this mode. Mutually exclusive with `adSetId`.
                ad_set_id: Meta-only. When present, switches to the attach shape: adds
        one new ad to this existing ad set without creating a new
        campaign. Budget, targeting, goal, schedule, AND bid strategy
        are inherited from the ad set on Meta — passing `bidStrategy`
        in attach mode returns 400. To change an existing ad set's
        bid, use `PUT /v1/ads/ad-sets/{adSetId}`. Mutually exclusive
        with `creatives[]`.

        Supported on Meta (facebook, instagram) and TikTok. On TikTok
        the `adSetId` is the ad group ID; the new ad inherits the
        ad group's bid + budget + targeting.
                business_name: Google Display only
                board_id: Pinterest only. Board ID (auto-creates if not provided).
                organization_id: LinkedIn only. The Company Page that authors the Direct Sponsored Content ("dark") post backing the ad — accepts a numeric organization ID or a full `urn:li:organization:N` URN. Required unless the resolved `accountId` is a connected LinkedIn Company-Page account (defaults to that page) or the LinkedIn ad account is org-owned (defaults to the account's owning organization). The authenticated member must be an ADMINISTRATOR or DIRECT_SPONSORED_CONTENT_POSTER of this page (and the page must be associated with the ad account), or LinkedIn returns 403. Ignored by every other platform.
                countries: ISO 3166-1 alpha-2 country codes (e.g. ['NL']). Defaults to ['US'] when no `cities` or `regions` are provided. (LinkedIn currently honours country-level targeting only.)
                cities: Meta-only. City-level geo targeting. Each city is targeted by Meta's opaque `key` (the city ID) which can be looked up via `GET /v1/ads/targeting/search?type=city&q=<name>&country_code=<ISO>`. Optional `radius` + `distance_unit` extend the targeting beyond the city limits (e.g. radius 25 km around the city center). Both must be set together, or both omitted (Meta defaults to ~16 km when omitted).

        Cannot overlap with the same country in `countries` (Meta returns a "locations overlap" error). Either drop the country or scope it to a different country.
                regions: Meta-only. Region-level (state/province) geo targeting. Each region is targeted by Meta's opaque `key` (the region ID) which can be looked up via `GET /v1/ads/targeting/search?type=region&q=<name>&country_code=<ISO>`.
                age_min
                age_max
                interests: Interest objects from /v1/ads/interests. Each must include id and name.
                zips: Postal/ZIP geo targeting. `key` is the platform's postal location ID from /v1/ads/targeting/search?dimension=geo&geoType=zip. Supported on Meta, Google, TikTok, Pinterest, X.
                metros: DMA / metro-area geo targeting. `key` is the platform's metro ID from /v1/ads/targeting/search?dimension=geo&geoType=metro.
                custom_locations: Point-radius (lat/lng) geo targeting. Meta only (custom_locations). Rejected on platforms without radius support.
                behaviors: Behaviour entities from /v1/ads/targeting/search?dimension=behavior. Supported on Meta and TikTok. Each must include id.
                income_tier: Normalized household-income tier. Meta and TikTok express all four; Google maps only
        `top_10`; rejected on LinkedIn, X, and Pinterest. On Meta, income targeting is incompatible
        with housing/employment/credit `specialAdCategories`.
                languages: Language codes (e.g. ['en']). Restricts the audience by language.
                saved_targeting_id: ID of a `saved_targeting` audience (created via POST /v1/ads/audiences). When set, its stored
        TargetingSpec is expanded as the base targeting; inline fields on this body merge on top. Lets you
        reuse a named targeting preset without re-sending every field.
                special_ad_categories: Meta only. Declares the ad's special category, required for housing, employment, credit, or
        political/social-issue ads (Meta enforces restricted targeting for these). Note: setting a special
        category disables income/zip targeting on Meta.
                end_date: Required for lifetime budgets
                audience_id: Custom audience ID for targeting
                campaign_type: Google only
                keywords: Google Search only
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
                gender: Meta only. Restrict the audience by gender. 'male' targets men only, 'female' targets women only, 'all' (default) targets everyone. Ignored by non-Meta platforms.
                bid_strategy: Meta bid strategy applied to the ad set.
                bid_amount: Bid cap in WHOLE currency units (USD: 5 = $5.00; JPY: 100 = ¥100). Required when
        `bidStrategy` is `LOWEST_COST_WITH_BID_CAP` or `COST_CAP`.
                roas_average_floor: Minimum ROAS as a decimal multiplier (e.g. 2.0 = 2.0x ROAS). Required when
        `bidStrategy` is `LOWEST_COST_WITH_MIN_ROAS`. Sent to Meta as
        `bid_constraints.roas_average_floor` × 10000.
                dsa_beneficiary: Name of the legal entity benefiting from the ad.
        Required by Meta when targeting EU users (DSA Article 26).
        Not enforced at schema level; enforced server-side when targeting intersects EU member states.
                dsa_payor: Name of the legal entity paying for the ad.
        Required by Meta when targeting EU users (DSA Article 26).
        Note Meta API spelling: dsa_payor (not dsa_payer).
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
                promoted_object: What the ad optimises against. Behaviour depends on the platform.

        **Meta**: forwarded to the ad set's `promoted_object` (snake-cased).
        Required for goals whose ad-set optimization_goal points at a specific
        event/page/app (without it Meta rejects the ad-set create with
        `error_subcode: 1815430` "Please select a promoted object for your ad set"):
          - `goal: conversions` (OFFSITE_CONVERSIONS): requires `pixelId` + `customEventType`
          - `goal: app_promotion` (APP_INSTALLS): requires `applicationId` + `objectStoreUrl`
          - `goal: lead_generation` (LEAD_GENERATION): `pageId` is auto-filled from the connected Page when omitted

        Other Meta goals (engagement, traffic, awareness, video_views) ignore this field.

        **TikTok**: only `goal: conversions` uses it.
          - `pixelId` maps to the ad group's `pixel_id`. Required: a TikTok website-conversion
            ad group without a pixel is rejected with `40002: Please select a pixel`.
          - `customEventType` maps to the ad group's `optimization_event` (the pixel event to
            optimise for). Optional: TikTok accepts a pixel-only auto-bid conversion ad group.
            See the `customEventType` field below for the valid TikTok codes.

        The remaining `promotedObject.*` fields are Meta-only. Platforms other than
        Meta and TikTok ignore `promotedObject` entirely."""
        client = _get_client()
        try:
            response = client.ads.create_standalone_ad(
                account_id=account_id,
                ad_account_id=ad_account_id,
                name=name,
                goal=goal,
                budget_amount=budget_amount,
                budget_type=budget_type,
                currency=currency,
                headline=headline,
                long_headline=long_headline,
                body=body,
                call_to_action=call_to_action,
                link_url=link_url,
                lead_gen_form_id=lead_gen_form_id,
                image_url=image_url,
                images=images,
                video=video,
                creatives=creatives,
                ad_set_id=ad_set_id,
                business_name=business_name,
                board_id=board_id,
                organization_id=organization_id,
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
                saved_targeting_id=saved_targeting_id,
                special_ad_categories=special_ad_categories,
                end_date=end_date,
                audience_id=audience_id,
                campaign_type=campaign_type,
                keywords=keywords,
                additional_headlines=additional_headlines,
                additional_descriptions=additional_descriptions,
                advantage_audience=advantage_audience,
                attribution_spec=attribution_spec,
                gender=gender,
                bid_strategy=bid_strategy,
                bid_amount=bid_amount,
                roas_average_floor=roas_average_floor,
                dsa_beneficiary=dsa_beneficiary,
                dsa_payor=dsa_payor,
                brand_identity=brand_identity,
                identity_type=identity_type,
                promoted_object=promoted_object,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List submitted leads (cross-form CRM view)",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ads_list_leads(
        form_id: str | None = None,
        account_id: str | None = None,
        limit: int = 25,
        since: int | None = None,
        cursor: str | None = None,
    ) -> str:
        """List submitted leads (cross-form CRM view)

        Args:
            form_id: Filter to a single lead form.
            account_id: Filter to a single connected account.
            limit
            since: Unix seconds; only leads created at/after this Meta timestamp.
            cursor: Keyset cursor from a previous response's pagination.cursor."""
        client = _get_client()
        try:
            response = client.ads.list_leads(
                form_id=form_id,
                account_id=account_id,
                limit=limit,
                since=since,
                cursor=cursor,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List Lead Gen (Instant) forms",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ads_list_lead_forms(
        account_id: str, limit: int = 25, cursor: str | None = None
    ) -> str:
        """List Lead Gen (Instant) forms

        Args:
            account_id: Connected facebook account id. (required)
            limit
            cursor"""
        client = _get_client()
        try:
            response = client.ads.list_lead_forms(
                account_id=account_id, limit=limit, cursor=cursor
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a Lead Gen (Instant) form",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ads_create_lead_form(
        account_id: str,
        name: str,
        questions: list[dict[str, Any]] | None,
        privacy_policy_url: str,
        privacy_policy_link_text: str | None = None,
        follow_up_action_url: str | None = None,
        locale: str | None = None,
        thank_you_title: str | None = None,
        thank_you_body: str | None = None,
        thank_you_button_text: str | None = None,
        thank_you_button_type: str | None = None,
        thank_you_website_url: str | None = None,
        is_optimized_for_quality: bool | None = None,
    ) -> str:
        """Create a Lead Gen (Instant) form

        Args:
            account_id: (required)
            name: (required)
            questions: (required)
            privacy_policy_url: (required)
            privacy_policy_link_text
            follow_up_action_url
            locale
            thank_you_title
            thank_you_body
            thank_you_button_text
            thank_you_button_type
            thank_you_website_url
            is_optimized_for_quality"""
        client = _get_client()
        try:
            response = client.ads.create_lead_form(
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
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Get a single Lead Gen form",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ads_get_lead_form(form_id: str, account_id: str) -> str:
        """Get a single Lead Gen form

        Args:
            form_id: (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.ads.get_lead_form(form_id=form_id, account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Archive a Lead Gen form",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ads_archive_lead_form(form_id: str, account_id: str) -> str:
        """Archive a Lead Gen form

        Args:
            form_id: (required)
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.ads.archive_lead_form(
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
    def ads_list_form_leads(
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
            response = client.ads.list_form_leads(
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
            title="Create a synthetic test lead",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ads_create_test_lead(
        form_id: str, account_id: str, field_data: list[dict[str, Any]] | None
    ) -> str:
        """Create a synthetic test lead

        Args:
            form_id: (required)
            account_id: (required)
            field_data: (required)"""
        client = _get_client()
        try:
            response = client.ads.create_test_lead(
                form_id=form_id, account_id=account_id, field_data=field_data
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Search targeting interests (deprecated)",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ads_search_ad_interests(q: str, account_id: str) -> str:
        """Search targeting interests (deprecated)

        Args:
            q: Search query (required)
            account_id: Social account ID (required)"""
        client = _get_client()
        try:
            response = client.ads.search_ad_interests(q=q, account_id=account_id)
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
    def ads_search_ad_targeting(
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
            response = client.ads.search_ad_targeting(
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
    def ads_estimate_ad_reach(
        account_id: str,
        spec: dict[str, Any] | None,
        optimization_goal: str | None = None,
    ) -> str:
        """Estimate audience reach

            Args:
                account_id: Social account ID on the target ad platform. (required)
                spec: The targeting spec to estimate. Same shape used by POST /v1/ads/create. (required)
                optimization_goal: Optional. The optimization goal the estimate should assume (platform's
        own vocabulary, e.g. Meta `REACH`, `LINK_CLICKS`, `OFFSITE_CONVERSIONS`).
        Some platforms vary the estimate by goal; omit to use the platform default."""
        client = _get_client()
        try:
            response = client.ads.estimate_ad_reach(
                account_id=account_id, spec=spec, optimization_goal=optimization_goal
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Send conversion events to an ad platform",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ads_send_conversions(
        account_id: str,
        destination_id: str,
        events: list[dict[str, Any]] | None,
        test_code: str | None = None,
        consent: dict[str, Any] | None = None,
    ) -> str:
        """Send conversion events to an ad platform

            Args:
                account_id: SocialAccount ID (metaads, googleads, or linkedinads). (required)
                destination_id: Platform destination identifier. For Meta, the pixel/dataset
        ID. For Google, the conversion action resource name. For
        LinkedIn, the conversion rule ID or full
        `urn:lla:llaPartnerConversion:{id}` URN.
         (required)
                events: (required)
                test_code: Meta `test_event_code` passthrough. Ignored by Google and LinkedIn.
                consent: Batch-level user consent. Required by Google for EEA/UK
        events under the Feb 2026 restrictions. Ignored by Meta
        and LinkedIn."""
        client = _get_client()
        try:
            response = client.ads.send_conversions(
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
            title="List destinations for the Conversions API",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ads_list_conversion_destinations(account_id: str) -> str:
        """List destinations for the Conversions API

        Args:
            account_id: SocialAccount ID (metaads, googleads, or linkedinads). (required)"""
        client = _get_client()
        try:
            response = client.ads.list_conversion_destinations(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create a conversion destination (LinkedIn)",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ads_create_conversion_destination(
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
    ) -> str:
        """Create a conversion destination (LinkedIn)

            Args:
                account_id: SocialAccount ID (linkedinads). (required)
                ad_account_id: Sponsored ad account ID. Numeric (e.g. "5123456") or
        full `urn:li:sponsoredAccount:{id}` URN.
         (required)
                name: (required)
                type: Either a unified standard event name (e.g. "Purchase",
        "Lead", "AddToCart") or a LinkedIn rule type enum value
        (e.g. "PURCHASE", "QUALIFIED_LEAD"). The API maps
        standard names to LinkedIn enum values automatically.
         (required)
                attribution_type
                post_click_attribution_window_size: Default 30. 365 only allowed for LEAD, PURCHASE,
        ADD_TO_CART, QUALIFIED_LEAD, SUBMIT_APPLICATION rule
        types — the API rejects other combinations locally.
                view_through_attribution_window_size: Default 7. Same 365-day-window type restriction applies
        as `postClickAttributionWindowSize`.
                value_type: DYNAMIC (default) uses the per-event `value` from
        `sendConversions`. FIXED uses the rule's `value` field.
        NO_VALUE drops monetary value entirely.
                value: Static conversion value. Used when `valueType=FIXED`.
        The currency should match the ad account's currency.
                auto_association_type: Controls campaign association at rule-creation time:
        - ALL_CAMPAIGNS: associate the rule with every active,
          paused, and draft campaign in the ad account
        - OBJECTIVE_BASED: associate only campaigns whose
          objective matches the rule's type
        - NONE: don't auto-associate. Manage associations via
          the `/associations` endpoints below.
        Note: auto-association runs once at create time; new
        campaigns added after the rule still need explicit
        association."""
        client = _get_client()
        try:
            response = client.ads.create_conversion_destination(
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
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Fetch a single conversion destination",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ads_get_conversion_destination(
        account_id: str, destination_id: str, ad_account_id: str
    ) -> str:
        """Fetch a single conversion destination

        Args:
            account_id: (required)
            destination_id: (required)
            ad_account_id: Numeric ID or full `urn:li:sponsoredAccount:{id}` URN. (required)"""
        client = _get_client()
        try:
            response = client.ads.get_conversion_destination(
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
    def ads_update_conversion_destination(
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
            response = client.ads.update_conversion_destination(
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
            title="Soft-delete a conversion destination",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ads_delete_conversion_destination(
        account_id: str, destination_id: str, ad_account_id: str | None = None
    ) -> str:
        """Soft-delete a conversion destination

        Args:
            account_id: (required)
            destination_id: (required)
            ad_account_id: Required as query OR in JSON body."""
        client = _get_client()
        try:
            response = client.ads.delete_conversion_destination(
                account_id=account_id,
                destination_id=destination_id,
                ad_account_id=ad_account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List campaigns associated with a conversion destination",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ads_list_conversion_associations(
        account_id: str, destination_id: str, ad_account_id: str
    ) -> str:
        """List campaigns associated with a conversion destination

        Args:
            account_id: (required)
            destination_id: (required)
            ad_account_id: (required)"""
        client = _get_client()
        try:
            response = client.ads.list_conversion_associations(
                account_id=account_id,
                destination_id=destination_id,
                ad_account_id=ad_account_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Associate campaigns with a conversion destination",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ads_add_conversion_associations(
        account_id: str,
        destination_id: str,
        ad_account_id: str,
        campaign_ids: list[str] | None,
    ) -> str:
        """Associate campaigns with a conversion destination

        Args:
            account_id: (required)
            destination_id: (required)
            ad_account_id: (required)
            campaign_ids: (required)"""
        client = _get_client()
        try:
            response = client.ads.add_conversion_associations(
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
            title="Remove campaign↔conversion associations",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ads_remove_conversion_associations(
        account_id: str, destination_id: str, ad_account_id: str, campaign_ids: str
    ) -> str:
        """Remove campaign↔conversion associations

        Args:
            account_id: (required)
            destination_id: (required)
            ad_account_id: (required)
            campaign_ids: Comma-separated list of campaign IDs. (required)"""
        client = _get_client()
        try:
            response = client.ads.remove_conversion_associations(
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
            title="Fetch attribution metrics for a conversion destination",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def ads_get_conversion_metrics(
        account_id: str,
        destination_id: str,
        ad_account_id: str,
        start_date: str,
        end_date: str | None = None,
        granularity: str = "DAILY",
    ) -> str:
        """Fetch attribution metrics for a conversion destination

        Args:
            account_id: (required)
            destination_id: (required)
            ad_account_id: (required)
            start_date: (required)
            end_date
            granularity"""
        client = _get_client()
        try:
            response = client.ads.get_conversion_metrics(
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

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Create Click-to-WhatsApp ad(s)",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def ads_create_ctwa_ad(
        account_id: str,
        ad_account_id: str,
        name: str,
        budget_amount: float,
        budget_type: str,
        headline: str | None = None,
        body: str | None = None,
        image_url: str | None = None,
        video: dict[str, Any] | None = None,
        creatives: list[dict[str, Any]] | None = None,
        currency: str | None = None,
        end_date: str | None = None,
        countries: list[str] | None = None,
        cities: list[dict[str, Any]] | None = None,
        regions: list[dict[str, Any]] | None = None,
        zips: list[dict[str, Any]] | None = None,
        metros: list[dict[str, Any]] | None = None,
        custom_locations: list[dict[str, Any]] | None = None,
        age_min: int | None = None,
        age_max: int | None = None,
        interests: list[dict[str, Any]] | None = None,
        audience_id: str | None = None,
        advantage_audience: int | None = None,
        objective: str | None = None,
        bid_strategy: str | None = None,
        bid_amount: float | None = None,
        roas_average_floor: float | None = None,
        dsa_beneficiary: str | None = None,
        dsa_payor: str | None = None,
    ) -> str:
        """Create Click-to-WhatsApp ad(s)

            Args:
                account_id: Facebook or Instagram SocialAccount ID. (required)
                ad_account_id: Meta ad account ID, e.g. `act_123456789`. (required)
                name: Ad display name. Used to derive campaign / ad set names.
        On the multi-creative shape, each ad's Meta name gets a
        " #N" suffix (1-indexed) so Ads Manager shows them as a
        numbered batch.
         (required)
                headline: Single-creative shape only. Mutually exclusive with
        `creatives[]`.
                body: Primary text shown above the image / video. Single-creative
        shape only. Mutually exclusive with `creatives[]`.
                image_url: Image asset for single-creative shape. Mutually exclusive
        with `video` and with `creatives[]`. Required on the
        single-creative shape if `video` is not supplied.
                video: Video creative for single-creative shape. Mutually
        exclusive with `imageUrl` and with `creatives[]`. Required
        on the single-creative shape if `imageUrl` is not supplied.
                creatives: Multi-creative shape: N CTWA ads under one campaign + one
        ad set, sharing budget and targeting. Mutually exclusive
        with the top-level single-creative fields (`headline` /
        `body` / `imageUrl` / `video`). Each entry must supply its
        own headline, body, and exactly one of `imageUrl` /
        `video`.
                budget_amount: Budget amount in the ad account's currency major units
        (e.g. dollars for USD, not cents). Must be > 0.
         (required)
                budget_type: (required)
                currency: ISO 4217 currency code matching the ad account's currency
        (e.g. `USD`). Optional; Meta infers from the ad account
        when omitted.
                end_date: ISO 8601 datetime. Required when `budgetType` is `lifetime`.
                countries: ISO 3166-1 alpha-2 country codes. Defaults to `["US"]` only
        when no other geo (`cities`, `regions`, `zips`, `metros`,
        `customLocations`) is supplied.
                cities: City-level geo targeting for local CTWA campaigns (e.g.
        25km radius around Milan). Each entry maps to Meta's
        TargetingGeoLocationCity. `key` is Meta's city ID
        (lookupable via GET /v1/ads/targeting/search). `radius`
        and `distance_unit` are coupled: set both or neither.
                regions: Region / state-level geo targeting. `key` is Meta's region
        ID (lookupable via GET /v1/ads/targeting/search?type=region).
                zips: ZIP / postal-code geo targeting. `key` is the platform's
        postal id resolved via /v1/ads/targeting/search.
                metros: DMA / metro-area geo targeting. `key` is Meta's metro id
        (e.g. `DMA:807`).
                custom_locations: Point-radius geo (Meta `geo_locations.custom_locations`).
        Use for targeting a radius around a specific lat/long when
        no Meta city/region key fits. `distanceUnit` is required.
                age_min
                age_max
                interests
                audience_id: Custom audience ID to target.
                advantage_audience: Meta's Advantage+ audience expansion. `0` (default) keeps
        targeting strict; `1` lets Meta expand beyond the supplied
        targeting when its delivery system finds better matches.
        Always sent on CREATE (Meta requires it).
                objective: Defaults to `OUTCOME_ENGAGEMENT` (the broadly-supported CTWA
        objective). `OUTCOME_SALES` and `OUTCOME_LEADS` require
        additional account configuration (Dataset linked to the WABA
        for sales) and may be rejected by Meta if missing.
                bid_strategy: Meta bid strategy applied to the shared ad set. Defaults to
        `LOWEST_COST_WITHOUT_CAP` (auto-bid) when omitted.
        `LOWEST_COST_WITH_BID_CAP` and `COST_CAP` require
        `bidAmount`. `LOWEST_COST_WITH_MIN_ROAS` requires
        `roasAverageFloor`. CTWA's `optimization_goal` is fixed to
        `CONVERSATIONS`, but the bid strategy is independent.
                bid_amount: Whole currency units (e.g. `5` = $5.00 on a USD account).
        Required when `bidStrategy` is `LOWEST_COST_WITH_BID_CAP`
        or `COST_CAP`; rejected otherwise.
                roas_average_floor: Decimal ROAS multiplier (e.g. `2.0` = 2.0× ROAS floor).
        Required when `bidStrategy` is `LOWEST_COST_WITH_MIN_ROAS`;
        rejected otherwise. Meta enforces its own upper bound
        server-side.
                dsa_beneficiary: Name of the legal entity benefiting from the ad.
        Required by Meta when targeting EU users (DSA Article 26).
        Not enforced at schema level; enforced server-side when targeting intersects EU member states.
                dsa_payor: Name of the legal entity paying for the ad.
        Required by Meta when targeting EU users (DSA Article 26).
        Note Meta API spelling: dsa_payor (not dsa_payer)."""
        client = _get_client()
        try:
            response = client.ads.create_ctwa_ad(
                account_id=account_id,
                ad_account_id=ad_account_id,
                name=name,
                headline=headline,
                body=body,
                image_url=image_url,
                video=video,
                creatives=creatives,
                budget_amount=budget_amount,
                budget_type=budget_type,
                currency=currency,
                end_date=end_date,
                countries=countries,
                cities=cities,
                regions=regions,
                zips=zips,
                metros=metros,
                custom_locations=custom_locations,
                age_min=age_min,
                age_max=age_max,
                interests=interests,
                audience_id=audience_id,
                advantage_audience=advantage_audience,
                objective=objective,
                bid_strategy=bid_strategy,
                bid_amount=bid_amount,
                roas_average_floor=roas_average_floor,
                dsa_beneficiary=dsa_beneficiary,
                dsa_payor=dsa_payor,
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
            title="Get YouTube channel-level insights",
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
        """Get YouTube channel-level insights

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
            title="Get LinkedIn organization page aggregate analytics",
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
        """Get LinkedIn organization page aggregate analytics

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
            end_date: End date (YYYY-MM-DD). Defaults to 3 days ago (YouTube data latency)."""
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
        breakdown: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> str:
        """Get YouTube demographics

            Args:
                account_id: The Zernio SocialAccount ID for the YouTube account (required)
                breakdown: Comma-separated list of demographic dimensions: age, gender, country.
        Defaults to all three if omitted.
                start_date: Start date in YYYY-MM-DD format. Defaults to 90 days ago.
                end_date: End date in YYYY-MM-DD format. Defaults to 3 days ago (YouTube data latency)."""
        client = _get_client()
        try:
            response = client.analytics.get_you_tube_demographics(
                account_id=account_id,
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
    ) -> str:
        """Get daily aggregated metrics

        Args:
            platform: Filter by platform (e.g. "instagram", "tiktok"). Omit for all platforms.
            profile_id: Filter by profile ID. Omit for all profiles.
            account_id: Filter by social account ID
            from_date: Inclusive start date (ISO 8601). Defaults to 180 days ago.
            to_date: Inclusive end date (ISO 8601). Defaults to now.
            source: Filter by post origin. "late" for posts published via Zernio, "external" for posts imported from platforms."""
        client = _get_client()
        try:
            response = client.analytics.get_daily_metrics(
                platform=platform,
                profile_id=profile_id,
                account_id=account_id,
                from_date=from_date,
                to_date=to_date,
                source=source,
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
        account_id: str, urn: str, limit: int = 25, cursor: str | None = None
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

    # API_KEYS

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
    ) -> str:
        """Create key

        Args:
            name: (required)
            expires_in: Days until expiry
            scope: 'full' grants access to all profiles (default), 'profiles' restricts to specific profiles
            profile_ids: Profile IDs this key can access. Required when scope is 'profiles'.
            permission: 'read-write' allows all operations (default), 'read' restricts to GET requests only"""
        client = _get_client()
        try:
            response = client.api_keys.create_api_key(
                name=name,
                expires_in=expires_in,
                scope=scope,
                profile_ids=profile_ids,
                permission=permission,
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
        platform_post_id: str | None = None,
        post_id: str | None = None,
        post_title: str | None = None,
        keywords: list[str] | None = None,
        match_mode: str = "contains",
        buttons: list[dict[str, Any]] | None = None,
        comment_reply: str | None = None,
    ) -> str:
        """Create comment-to-DM automation

        Args:
            profile_id: (required)
            account_id: Instagram or Facebook account ID (required)
            platform_post_id: Platform media/post ID. Omit for an account-wide (any-post) automation.
            post_id: Zernio post ID. Required only when also targeting a specific post via platformPostId.
            post_title: Post content snippet for display
            name: Automation label (required)
            keywords: Trigger keywords (empty = any comment triggers)
            match_mode
            dm_message: DM text to send to commenter. Max 640 chars when buttons are set, otherwise ~1000. (required)
            buttons: Optional inline DM buttons (1-3). Phone buttons are Facebook-only. Omit or pass [] for a plain-text DM.
            comment_reply: Optional public reply to the comment"""
        client = _get_client()
        try:
            response = client.comment_automations.create_comment_automation(
                profile_id=profile_id,
                account_id=account_id,
                platform_post_id=platform_post_id,
                post_id=post_id,
                post_title=post_title,
                name=name,
                keywords=keywords,
                match_mode=match_mode,
                dm_message=dm_message,
                buttons=buttons,
                comment_reply=comment_reply,
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
        keywords: list[str] | None = None,
        match_mode: str | None = None,
        dm_message: str | None = None,
        buttons: list[dict[str, Any]] | None = None,
        comment_reply: str | None = None,
        is_active: bool | None = None,
    ) -> str:
        """Update automation settings

        Args:
            automation_id: (required)
            name
            keywords
            match_mode
            dm_message
            buttons: Inline DM buttons (1-3). Pass [] to clear all buttons.
            comment_reply
            is_active"""
        client = _get_client()
        try:
            response = client.comment_automations.update_comment_automation(
                automation_id=automation_id,
                name=name,
                keywords=keywords,
                match_mode=match_mode,
                dm_message=dm_message,
                buttons=buttons,
                comment_reply=comment_reply,
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
        post_id: str, comment_id: str, account_id: str, cid: str | None = None
    ) -> str:
        """Like comment

        Args:
            post_id: (required)
            comment_id: (required)
            account_id: The social account ID (required)
            cid: (Bluesky only) Content identifier for the comment"""
        client = _get_client()
        try:
            response = client.comments.like_inbox_comment(
                post_id=post_id, comment_id=comment_id, account_id=account_id, cid=cid
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
    ) -> str:
        """Get OAuth connect URL

        Args:
            platform: Social media platform to connect (required)
            profile_id: Your Zernio profile ID (get from /v1/profiles) (required)
            redirect_url: Your custom redirect URL after connection completes. Standard mode appends ?connected={platform}&profileId=X&accountId=Y&username=Z. Headless mode appends OAuth data params for platforms requiring selection (e.g. LinkedIn orgs, Facebook pages). If no selection is needed, the account is created directly and the redirect includes accountId.
            headless: When true, the user is redirected to your redirect_url with raw OAuth data (code, state) instead of Zernio's default account selection UI. Use this to build a custom connect experience."""
        client = _get_client()
        try:
            response = client.connect.get_connect_url(
                platform=platform,
                profile_id=profile_id,
                redirect_url=redirect_url,
                headless=headless,
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
                redirect_url: Custom redirect URL after OAuth completes (same-token platforms only)
                headless: Enable headless mode (same-token platforms only)
                ad_account_id: (metaads only) Scope ad sync to a single Meta ad account. Without this
        param, sync covers every `act_*` the connected token can see. Pass this
        to limit `sync.totalAds` / `synced` and the resulting ads to one ad
        account. Format: `act_<digits>` (matches what `/me/adaccounts` returns).
        Validated against the connected token; unreachable IDs return 400.
        For multiple accounts use `adAccountIds` instead.
                ad_account_ids: (metaads only) Scope ad sync to multiple Meta ad accounts. Repeat the
        param (`?adAccountIds=act_1&adAccountIds=act_2`) or comma-separate
        (`?adAccountIds=act_1,act_2`). Validated against the connected token.
        Persisted server-side; latest call wins. Omitting both `adAccountId`
        and `adAccountIds` keeps any previously persisted scope unchanged."""
        client = _get_client()
        try:
            response = client.connect.connect_ads(
                platform=platform,
                profile_id=profile_id,
                account_id=account_id,
                redirect_url=redirect_url,
                headless=headless,
                ad_account_id=ad_account_id,
                ad_account_ids=ad_account_ids,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="Configure TikTok Ads Brand Identity",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_configure_tik_tok_ads_brand_identity(
        account_id: str, display_name: str, image_url: str
    ) -> str:
        """Configure TikTok Ads Brand Identity

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
    ) -> str:
        """List GBP locations

        Args:
            profile_id: Profile ID from your connection flow. Required for auth validation when provided.
            pending_data_token: Token from the OAuth callback redirect. Preferred over tempToken because it preserves server-side token storage. One of pendingDataToken or tempToken is required.
            temp_token: Legacy. Direct Google access token. Use pendingDataToken instead when available."""
        client = _get_client()
        try:
            response = client.connect.list_google_business_locations(
                profile_id=profile_id,
                pending_data_token=pending_data_token,
                temp_token=temp_token,
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
        redirect_url: str | None = None,
    ) -> str:
        """Select GBP location

        Args:
            profile_id: Profile ID from your connection flow (required)
            location_id: The Google Business location ID selected by the user (required)
            pending_data_token: Token from the OAuth callback redirect (pendingDataToken query param). Tokens and profile data are retrieved server-side from this token. (required)
            redirect_url: Optional custom redirect URL to return to after selection"""
        client = _get_client()
        try:
            response = client.connect.select_google_business_location(
                profile_id=profile_id,
                location_id=location_id,
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
            title="Connect WhatsApp via credentials",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def connect_whats_app_credentials(
        profile_id: str, access_token: str, waba_id: str, phone_number_id: str
    ) -> str:
        """Connect WhatsApp via credentials

        Args:
            profile_id: Your Zernio profile ID (required)
            access_token: Permanent System User access token from Meta Business Suite (required)
            waba_id: WhatsApp Business Account ID from Meta (required)
            phone_number_id: Phone Number ID from Meta WhatsApp Manager (required)"""
        client = _get_client()
        try:
            response = client.connect.connect_whats_app_credentials(
                profile_id=profile_id,
                access_token=access_token,
                waba_id=waba_id,
                phone_number_id=phone_number_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List WhatsApp phone numbers for selection",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def connect_list_whats_app_phone_numbers(profile_id: str, temp_token: str) -> str:
        """List WhatsApp phone numbers for selection

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
            title="Complete WhatsApp phone number selection",
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
        """Complete WhatsApp phone number selection

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
    def connect_get_gmb_locations(account_id: str) -> str:
        """List GBP locations

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.connect.get_gmb_locations(account_id=account_id)
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
    def connect_update_gmb_location(account_id: str, selected_location_id: str) -> str:
        """Update GBP location

        Args:
            account_id: (required)
            selected_location_id: (required)"""
        client = _get_client()
        try:
            response = client.connect.update_gmb_location(
                account_id=account_id, selected_location_id=selected_location_id
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
        search: str | None = None,
        tag: str | None = None,
        platform: str | None = None,
        is_subscribed: str | None = None,
        limit: int = 50,
        skip: int = 0,
    ) -> str:
        """List contacts

        Args:
            profile_id: Filter by profile. Omit to list across all profiles
            search
            tag
            platform
            is_subscribed
            limit
            skip"""
        client = _get_client()
        try:
            response = client.contacts.list_contacts(
                profile_id=profile_id,
                search=search,
                tag=tag,
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
        account_id: str,
        platform: str,
        contacts: list[dict[str, Any]] | None,
    ) -> str:
        """Bulk create contacts

        Args:
            profile_id: (required)
            account_id: (required)
            platform: (required)
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
        scope: str, profile_ids: list[str] | None = None
    ) -> str:
        """Create invite token

        Args:
            scope: 'all' grants access to all profiles, 'profiles' restricts to specific profiles (required)
            profile_ids: Required if scope is 'profiles'. Array of profile IDs to grant access to."""
        client = _get_client()
        try:
            response = client.invites.create_invite_token(
                scope=scope, profile_ids=profile_ids
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
    ) -> str:
        """List activity logs

        Args:
            type: Log category to query
            status: Filter by status
            platform: Filter by platform
            action: Filter by action (e.g., post.published, message.sent, account.connected, webhook.delivered)
            search: Free-text search across log fields
            days: Number of days to look back (max 90)
            limit: Maximum number of logs to return (max 100)
            skip: Number of logs to skip (for pagination)"""
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
        template_language: str | None = None,
        template_params: list[str] | None = None,
    ) -> str:
        """Create conversation

        Args:
            account_id: The social account ID to send from (required)
            participant_id: Recipient identifier. For X this is the numeric user ID; for WhatsApp, the recipient phone number in international format (digits, country code included). Provide either this or participantUsername.
            participant_username: Recipient handle/username — an X or Bluesky handle (with or without @) or a Reddit username (with or without u/). Resolved via lookup. Provide either this or participantId.
            message: Text content of the message. At least one of message, attachment, or (for WhatsApp) templateName is required.
            skip_dm_check: X/Twitter only. Skip the receives_your_dm eligibility check before sending. Use if you have already verified the recipient accepts DMs.
            template_name: WhatsApp only. Name of the approved template to start the conversation with (required for WhatsApp).
            template_language: WhatsApp only. Template language code (e.g. en_US).
            template_params: WhatsApp only. Body variable values, in order, substituted into the template body ({{1}}, {{2}}, ...)."""
        client = _get_client()
        try:
            response = client.messages.create_inbox_conversation(
                account_id=account_id,
                participant_id=participant_id,
                participant_username=participant_username,
                message=message,
                skip_dm_check=skip_dm_check,
                template_name=template_name,
                template_language=template_language,
                template_params=template_params,
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
        attachment_type: str | None = None,
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
                conversation_id: The conversation ID (id field from list conversations endpoint). This is the platform-specific conversation identifier, not an internal database ID. (required)
                account_id: Social account ID (required)
                message: Message text
                attachment_url: URL of the attachment to send (image, video, audio, or file). The URL must be publicly accessible. For binary file uploads, use multipart/form-data instead.
                attachment_type: Type of attachment. Defaults to file if not specified.
                voice_note: WhatsApp only. When `true` on an audio attachment, the message is sent
        as a voice message (PTT) — the recipient sees the waveform + voice-note
        UI instead of a basic audio attachment. The audio file MUST be `.ogg`
        encoded with the OPUS codec (mono) per Meta's voice-message contract;
        other formats are rejected by WhatsApp. Ignored for non-audio attachments.
                quick_replies: Quick reply buttons. Mutually exclusive with buttons. Max 13 items.
                buttons: Action buttons. Mutually exclusive with quickReplies. Max 3 items.
                template: Generic template for carousels (Instagram/Facebook only, ignored on Telegram).
                interactive: WhatsApp-only. Rich interactive payload for list messages, CTA URL
        buttons, and Flow prompts. When set, takes priority over `buttons`
        and `quickReplies`. The shape mirrors Meta's Cloud API `interactive`
        object verbatim, so any payload that works against Meta directly
        will also work here.

        Use `buttons` / `quickReplies` for simple button replies
        (WhatsApp's `interactive.type: "button"`) — the abstraction caps at
        3 buttons and handles the auto-conversion for you. Use this field
        only for `list`, `cta_url`, or `flow` messages.

        Tap events come back via the `message.received` webhook with
        `metadata.interactiveType` set to `list_reply` or `nfm_reply`.
                reply_markup: Telegram-native keyboard markup. Ignored on other platforms.
                messaging_type: Facebook messaging type. Required when using messageTag.
                message_tag: Facebook message tag for messaging outside 24h window. Requires messagingType MESSAGE_TAG. Instagram only supports HUMAN_AGENT.
                reply_to: Platform message ID to quote-reply to. For WhatsApp, pass the wamid (available in message.platformMessageId from webhooks). For Telegram, pass the Telegram message ID.
                location: WhatsApp-only. Send a location pin.
                contacts: WhatsApp-only. Send one or more contact cards."""
        client = _get_client()
        try:
            response = client.messages.send_inbox_message(
                conversation_id=conversation_id,
                account_id=account_id,
                message=message,
                attachment_url=attachment_url,
                attachment_type=attachment_type,
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
            limit: Results per page
            status
            platform
            profile_id
            created_by
            date_from
            date_to
            include_hidden
            search: Search posts by text content.
            sort_by: Sort order for results.
            account_id: Filter posts to those published via a specific social account (24-char hex ObjectId)."""
        client = _get_client()
        try:
            response = client.posts.list_posts(
                page=page,
                limit=limit,
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
                tiktok_settings: Root-level TikTok settings applied to all TikTok platforms. Merged into each platform's platformSpecificData, with platform-specific settings taking precedence.
                facebook_settings: Root-level Facebook settings applied to all Facebook platforms. Merged into each platform's platformSpecificData, with platform-specific settings taking precedence.
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
        content: str | None = None,
        scheduled_for: str | None = None,
        tiktok_settings: dict[str, Any] | None = None,
        facebook_settings: dict[str, Any] | None = None,
        recycling: dict[str, Any] | None = None,
    ) -> str:
        """Update post

        Args:
            post_id: (required)
            content
            scheduled_for
            tiktok_settings: Root-level TikTok settings applied to all TikTok platforms. Merged into each platform's platformSpecificData, with platform-specific settings taking precedence.
            facebook_settings: Root-level Facebook settings applied to all Facebook platforms. Merged into each platform's platformSpecificData, with platform-specific settings taking precedence.
            recycling"""
        client = _get_client()
        try:
            response = client.posts.update_post(
                post_id=post_id,
                content=content,
                scheduled_for=scheduled_for,
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
            platform: The platform to edit the post on. Currently only twitter is supported. (required)
            content: The new tweet text content (required)"""
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
    def profiles_list_profiles(include_over_limit: bool = False) -> str:
        """List profiles

        Args:
            include_over_limit: When true, includes over-limit profiles (marked with isOverLimit: true)."""
        client = _get_client()
        try:
            response = client.profiles.list_profiles(
                include_over_limit=include_over_limit
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
    def queue_delete_queue_slot(profile_id: str, queue_id: str) -> str:
        """Delete schedule

        Args:
            profile_id: (required)
            queue_id: Queue ID to delete (required)"""
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

    # TRACKING_TAGS

    @mcp.tool(
        annotations=ToolAnnotations(
            title="List tracking tags (Meta Pixels)",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def tracking_tags_list_tracking_tags(
        account_id: str, ad_account_id: str | None = None
    ) -> str:
        """List tracking tags (Meta Pixels)

        Args:
            account_id: Meta ads SocialAccount id (platform `metaads`). (required)
            ad_account_id: Optional. Scope to one ad account, e.g. `act_123456789`."""
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
            title="Create a tracking tag (Meta Pixel)",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def tracking_tags_create_tracking_tag(
        account_id: str, ad_account_id: str, name: str
    ) -> str:
        """Create a tracking tag (Meta Pixel)

        Args:
            account_id: Meta ads SocialAccount id (platform `metaads`). (required)
            ad_account_id: Meta ad account id, e.g. `act_123456789`. (required)
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
            title="Fetch a single tracking tag (Meta Pixel)",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def tracking_tags_get_tracking_tag(account_id: str, tag_id: str) -> str:
        """Fetch a single tracking tag (Meta Pixel)

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
            title="Update a tracking tag (Meta Pixel)",
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
        """Update a tracking tag (Meta Pixel)

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
            title="List ad accounts a tracking tag is shared with",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def tracking_tags_list_tracking_tag_shared_accounts(
        account_id: str, tag_id: str
    ) -> str:
        """List ad accounts a tracking tag is shared with

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
            title="Share a tracking tag with an ad account",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def tracking_tags_add_tracking_tag_shared_account(
        account_id: str, tag_id: str, ad_account_id: str
    ) -> str:
        """Share a tracking tag with an ad account

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
            title="Stop sharing a tracking tag with an ad account",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def tracking_tags_remove_tracking_tag_shared_account(
        account_id: str, tag_id: str, ad_account_id: str | None = None
    ) -> str:
        """Stop sharing a tracking tag with an ad account

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
            title="Aggregated event stats for a tracking tag (Meta Pixel)",
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
        """Aggregated event stats for a tracking tag (Meta Pixel)

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

    # USAGE

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
            title="Get plan and usage stats",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def usage_get_usage_stats(reconcile: bool | None = None) -> str:
        """Get plan and usage stats

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
    ) -> str:
        """Create webhook

        Args:
            name: Webhook name (1-50 characters) (required)
            url: Webhook endpoint URL (must be a valid URL, whitespace trimmed) (required)
            secret: Secret key for HMAC-SHA256 signature verification
            events: Events to subscribe to (at least one required) (required)
            is_active: Enable or disable webhook delivery. Defaults to `true` when omitted.
            custom_headers: Custom headers to include in webhook requests"""
        client = _get_client()
        try:
            response = client.webhooks.create_webhook_settings(
                name=name,
                url=url,
                secret=secret,
                events=events,
                is_active=is_active,
                custom_headers=custom_headers,
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
    ) -> str:
        """Update webhook

        Args:
            id: Webhook ID to update (required) (required)
            name: Webhook name (1-50 characters). Must be non-empty if provided.
            url: Webhook endpoint URL (must be a valid URL, whitespace trimmed). Must be a valid URL if provided.
            secret: Secret key for HMAC-SHA256 signature verification
            events: Events to subscribe to. Must contain at least one event if provided.
            is_active: Enable or disable webhook delivery
            custom_headers: Custom headers to include in webhook requests"""
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
                components: Template components (header, body, footer, buttons). Required for custom templates, omit when using library_template_name.
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
    def whatsapp_upload_whats_app_profile_photo() -> str:
        """Upload profile picture"""
        client = _get_client()
        try:
            response = client.whatsapp.upload_whats_app_profile_photo()
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
            title="Provision CTWA conversions dataset",
            readOnlyHint=False,
            destructiveHint=True,
            openWorldHint=True,
        )
    )
    def whatsapp_create_whats_app_dataset(account_id: str) -> str:
        """Provision CTWA conversions dataset

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
            title="List recent WhatsApp conversion events",
            readOnlyHint=True,
            destructiveHint=False,
            openWorldHint=False,
        )
    )
    def whatsapp_list_whats_app_conversions(account_id: str, limit: int = 50) -> str:
        """List recent WhatsApp conversion events

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
            status: Filter by status (by default excludes released numbers)
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
    def whatsapp_phone_numbers_purchase_whats_app_phone_number(profile_id: str) -> str:
        """Purchase phone number

        Args:
            profile_id: Profile to associate the number with (required)"""
        client = _get_client()
        try:
            response = client.whatsapp_phone_numbers.purchase_whats_app_phone_number(
                profile_id=profile_id
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
