"""
Auto-generated MCP tool handlers.

DO NOT EDIT - Run `python scripts/generate_mcp_tools.py` to regenerate.
"""

from __future__ import annotations

from typing import Any


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
                status = getattr(p, "status", "unknown")
                lines.append(f"- [{status}] {content}...")
            return "\n".join(lines)
        if hasattr(response, "accounts") and response.accounts:
            accs = response.accounts
            lines = [f"Found {len(accs)} account(s):"]
            for a in accs[:10]:
                platform = getattr(a, "platform", "?")
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
            return f"Post ID: {getattr(p, 'field_id', 'N/A')}\nStatus: {getattr(p, 'status', 'N/A')}"
        if hasattr(response, "profile") and response.profile:
            p = response.profile
            return f"Profile: {getattr(p, 'name', 'N/A')} (ID: {getattr(p, 'field_id', 'N/A')})"
    return str(response)


def register_generated_tools(mcp, _get_client):
    """Register all auto-generated tools with the MCP server."""

    # ACCOUNT_GROUPS

    @mcp.tool()
    def account_groups_list_account_groups() -> str:
        """List groups"""
        client = _get_client()
        try:
            response = client.account_groups.list_account_groups()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def account_groups_create_account_group(name: str, account_ids: str) -> str:
        """Create group

        Args:
            name: (required)
            account_ids: (required)"""
        client = _get_client()
        try:
            response = client.account_groups.create_account_group(
                name=name, account_ids=account_ids
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def account_groups_update_account_group(
        group_id: str, name: str = "", account_ids: str = ""
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def account_settings_set_messenger_menu(
        account_id: str, persistent_menu: str
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def account_settings_set_instagram_ice_breakers(
        account_id: str, ice_breakers: str
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def account_settings_set_telegram_commands(account_id: str, commands: str) -> str:
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

    @mcp.tool()
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

    @mcp.tool()
    def accounts_list_accounts(
        profile_id: str = "", platform: str = "", include_over_limit: bool = False
    ) -> str:
        """List accounts

        Args:
            profile_id: Filter accounts by profile ID
            platform: Filter accounts by platform (e.g. "instagram", "twitter").
            include_over_limit: When true, includes accounts from over-limit profiles."""
        client = _get_client()
        try:
            response = client.accounts.list_accounts(
                profile_id=profile_id,
                platform=platform,
                include_over_limit=include_over_limit,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_get_follower_stats(
        account_ids: str = "",
        profile_id: str = "",
        from_date: str = "",
        to_date: str = "",
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

    @mcp.tool()
    def accounts_update_account(
        account_id: str, username: str = "", display_name: str = ""
    ) -> str:
        """Update account

        Args:
            account_id: (required)
            username
            display_name"""
        client = _get_client()
        try:
            response = client.accounts.update_account(
                account_id=account_id, username=username, display_name=display_name
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
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

    @mcp.tool()
    def accounts_get_all_accounts_health(
        profile_id: str = "", platform: str = "", status: str = ""
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def accounts_get_google_business_reviews(
        account_id: str,
        location_id: str = "",
        page_size: int = 50,
        page_token: str = "",
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

    @mcp.tool()
    def accounts_get_google_business_food_menus(
        account_id: str, location_id: str = ""
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

    @mcp.tool()
    def accounts_update_google_business_food_menus(
        account_id: str, menus: str, location_id: str = "", update_mask: str = ""
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

    @mcp.tool()
    def accounts_get_google_business_location_details(
        account_id: str, location_id: str = "", read_mask: str = ""
    ) -> str:
        """Get location details

        Args:
            account_id: The Zernio account ID (from /v1/accounts) (required)
            location_id: Override which location to query. If omitted, uses the account's selected location. Use GET /gmb-locations to list valid IDs.
            read_mask: Comma-separated fields to return. Available: name, title, phoneNumbers, categories, storefrontAddress, websiteUri, regularHours, specialHours, serviceArea, serviceItems, profile, openInfo, metadata, moreHours."""
        client = _get_client()
        try:
            response = client.accounts.get_google_business_location_details(
                account_id=account_id, location_id=location_id, read_mask=read_mask
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_update_google_business_location_details(
        account_id: str,
        update_mask: str,
        location_id: str = "",
        regular_hours: str = "",
        special_hours: str = "",
        profile: str = "",
        website_uri: str = "",
        phone_numbers: str = "",
        categories: str = "",
        service_items: str = "",
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

    @mcp.tool()
    def accounts_list_google_business_media(
        account_id: str,
        location_id: str = "",
        page_size: int = 100,
        page_token: str = "",
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

    @mcp.tool()
    def accounts_create_google_business_media(
        account_id: str,
        source_url: str,
        location_id: str = "",
        media_format: str = "PHOTO",
        description: str = "",
        category: str = "",
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

    @mcp.tool()
    def accounts_delete_google_business_media(
        account_id: str, media_id: str, location_id: str = ""
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

    @mcp.tool()
    def accounts_get_google_business_attributes(
        account_id: str, location_id: str = ""
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

    @mcp.tool()
    def accounts_update_google_business_attributes(
        account_id: str, attributes: str, attribute_mask: str, location_id: str = ""
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

    @mcp.tool()
    def accounts_list_google_business_place_actions(
        account_id: str,
        location_id: str = "",
        page_size: int = 100,
        page_token: str = "",
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

    @mcp.tool()
    def accounts_create_google_business_place_action(
        account_id: str, uri: str, place_action_type: str, location_id: str = ""
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

    @mcp.tool()
    def accounts_delete_google_business_place_action(
        account_id: str, name: str, location_id: str = ""
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

    @mcp.tool()
    def accounts_get_linked_in_mentions(
        account_id: str, url: str, display_name: str = ""
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

    # ANALYTICS

    @mcp.tool()
    def analytics_get_analytics(
        post_id: str = "",
        platform: str = "",
        profile_id: str = "",
        account_id: str = "",
        source: str = "all",
        from_date: str = "",
        to_date: str = "",
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

    @mcp.tool()
    def analytics_get_you_tube_daily_views(
        video_id: str, account_id: str, start_date: str = "", end_date: str = ""
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

    @mcp.tool()
    def analytics_get_instagram_account_insights(
        account_id: str,
        metrics: str = "",
        since: str = "",
        until: str = "",
        metric_type: str = "total_value",
        breakdown: str = "",
    ) -> str:
        """Get Instagram account-level insights

            Args:
                account_id: The Zernio SocialAccount ID for the Instagram account (required)
                metrics: Comma-separated list of metrics. Defaults to "reach,views,accounts_engaged,total_interactions".
        Valid metrics: reach, views, accounts_engaged, total_interactions, comments, likes, saves, shares,
        replies, reposts, follows_and_unfollows, profile_links_taps.
        Note: only "reach" supports metricType=time_series. All other metrics are total_value only.
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

    @mcp.tool()
    def analytics_get_instagram_demographics(
        account_id: str,
        metric: str = "follower_demographics",
        breakdown: str = "",
        timeframe: str = "this_month",
    ) -> str:
        """Get Instagram audience demographics

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

    @mcp.tool()
    def analytics_get_daily_metrics(
        platform: str = "",
        profile_id: str = "",
        account_id: str = "",
        from_date: str = "",
        to_date: str = "",
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

    @mcp.tool()
    def analytics_get_best_time_to_post(
        platform: str = "", profile_id: str = "", source: str = "all"
    ) -> str:
        """Get best times to post

        Args:
            platform: Filter by platform (e.g. "instagram", "tiktok"). Omit for all platforms.
            profile_id: Filter by profile ID. Omit for all profiles.
            source: Filter by post origin. "late" for posts published via Zernio, "external" for posts imported from platforms."""
        client = _get_client()
        try:
            response = client.analytics.get_best_time_to_post(
                platform=platform, profile_id=profile_id, source=source
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def analytics_get_content_decay(
        platform: str = "", profile_id: str = "", source: str = "all"
    ) -> str:
        """Get content performance decay

        Args:
            platform: Filter by platform (e.g. "instagram", "tiktok"). Omit for all platforms.
            profile_id: Filter by profile ID. Omit for all profiles.
            source: Filter by post origin. "late" for posts published via Zernio, "external" for posts imported from platforms."""
        client = _get_client()
        try:
            response = client.analytics.get_content_decay(
                platform=platform, profile_id=profile_id, source=source
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def analytics_get_posting_frequency(
        platform: str = "", profile_id: str = "", source: str = "all"
    ) -> str:
        """Get posting frequency vs engagement

        Args:
            platform: Filter by platform (e.g. "instagram", "tiktok"). Omit for all platforms.
            profile_id: Filter by profile ID. Omit for all profiles.
            source: Filter by post origin. "late" for posts published via Zernio, "external" for posts imported from platforms."""
        client = _get_client()
        try:
            response = client.analytics.get_posting_frequency(
                platform=platform, profile_id=profile_id, source=source
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def analytics_get_post_timeline(
        post_id: str, from_date: str = "", to_date: str = ""
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

    @mcp.tool()
    def analytics_get_linked_in_aggregate_analytics(
        account_id: str,
        aggregation: str = "TOTAL",
        start_date: str = "",
        end_date: str = "",
        metrics: str = "",
    ) -> str:
        """Get LinkedIn aggregate stats

        Args:
            account_id: The ID of the LinkedIn personal account (required)
            aggregation: TOTAL (default, lifetime totals) or DAILY (time series). MEMBERS_REACHED not available with DAILY.
            start_date: Start date (YYYY-MM-DD). If omitted, returns lifetime analytics.
            end_date: End date (YYYY-MM-DD, exclusive). Defaults to today if omitted.
            metrics: Comma-separated metrics: IMPRESSION, MEMBERS_REACHED, REACTION, COMMENT, RESHARE. Omit for all."""
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

    @mcp.tool()
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

    @mcp.tool()
    def analytics_get_linked_in_post_reactions(
        account_id: str, urn: str, limit: int = 25, cursor: str = ""
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

    @mcp.tool()
    def api_keys_list_api_keys() -> str:
        """List keys"""
        client = _get_client()
        try:
            response = client.api_keys.list_api_keys()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def api_keys_create_api_key(
        name: str,
        expires_in: int = 0,
        scope: str = "full",
        profile_ids: str = "",
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

    @mcp.tool()
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

    @mcp.tool()
    def broadcasts_list_broadcasts(
        profile_id: str = "",
        status: str = "",
        platform: str = "",
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

    @mcp.tool()
    def broadcasts_create_broadcast(
        profile_id: str,
        account_id: str,
        platform: str,
        name: str,
        description: str = "",
        message: str = "",
        template: str = "",
        segment_filters: str = "",
    ) -> str:
        """Create a broadcast draft

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

    @mcp.tool()
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

    @mcp.tool()
    def broadcasts_update_broadcast(broadcast_id: str) -> str:
        """Update a broadcast

        Args:
            broadcast_id: (required)"""
        client = _get_client()
        try:
            response = client.broadcasts.update_broadcast(broadcast_id=broadcast_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def broadcasts_delete_broadcast(broadcast_id: str) -> str:
        """Delete a broadcast (draft only)

        Args:
            broadcast_id: (required)"""
        client = _get_client()
        try:
            response = client.broadcasts.delete_broadcast(broadcast_id=broadcast_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def broadcasts_send_broadcast(broadcast_id: str) -> str:
        """Trigger immediate send

        Args:
            broadcast_id: (required)"""
        client = _get_client()
        try:
            response = client.broadcasts.send_broadcast(broadcast_id=broadcast_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
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

    @mcp.tool()
    def broadcasts_cancel_broadcast(broadcast_id: str) -> str:
        """Cancel a broadcast

        Args:
            broadcast_id: (required)"""
        client = _get_client()
        try:
            response = client.broadcasts.cancel_broadcast(broadcast_id=broadcast_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def broadcasts_list_broadcast_recipients(
        broadcast_id: str, status: str = "", limit: int = 50, skip: int = 0
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

    @mcp.tool()
    def broadcasts_add_broadcast_recipients(
        broadcast_id: str,
        contact_ids: str = "",
        phones: str = "",
        use_segment: bool = False,
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

    @mcp.tool()
    def comment_automations_list_comment_automations(profile_id: str = "") -> str:
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

    @mcp.tool()
    def comment_automations_create_comment_automation(
        profile_id: str,
        account_id: str,
        platform_post_id: str,
        name: str,
        dm_message: str,
        post_id: str = "",
        post_title: str = "",
        keywords: str = "",
        match_mode: str = "contains",
        comment_reply: str = "",
    ) -> str:
        """Create a comment-to-DM automation

        Args:
            profile_id: (required)
            account_id: Instagram or Facebook account ID (required)
            platform_post_id: Platform media/post ID (required)
            post_id: Zernio post ID (optional)
            post_title: Post content snippet for display
            name: Automation label (required)
            keywords: Trigger keywords (empty = any comment triggers)
            match_mode
            dm_message: DM text to send to commenter (required)
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
                comment_reply=comment_reply,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def comment_automations_get_comment_automation(automation_id: str) -> str:
        """Get automation details with recent logs

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

    @mcp.tool()
    def comment_automations_update_comment_automation(
        automation_id: str,
        name: str = "",
        keywords: str = "",
        match_mode: str = "",
        dm_message: str = "",
        comment_reply: str = "",
        is_active: bool = False,
    ) -> str:
        """Update automation settings

        Args:
            automation_id: (required)
            name
            keywords
            match_mode
            dm_message
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
                comment_reply=comment_reply,
                is_active=is_active,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def comment_automations_delete_comment_automation(automation_id: str) -> str:
        """Delete automation and all logs

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

    @mcp.tool()
    def comment_automations_list_comment_automation_logs(
        automation_id: str, status: str = "", limit: int = 50, skip: int = 0
    ) -> str:
        """List trigger logs for an automation

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

    @mcp.tool()
    def comments_list_inbox_comments(
        profile_id: str = "",
        platform: str = "",
        min_comments: int = 0,
        since: str = "",
        sort_by: str = "date",
        sort_order: str = "desc",
        limit: int = 50,
        cursor: str = "",
        account_id: str = "",
    ) -> str:
        """List commented posts

        Args:
            profile_id: Filter by profile ID
            platform: Filter by platform
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

    @mcp.tool()
    def comments_get_inbox_post_comments(
        post_id: str,
        account_id: str,
        subreddit: str = "",
        limit: int = 25,
        cursor: str = "",
        comment_id: str = "",
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

    @mcp.tool()
    def comments_reply_to_inbox_post(
        post_id: str,
        account_id: str,
        message: str,
        comment_id: str = "",
        parent_cid: str = "",
        root_uri: str = "",
        root_cid: str = "",
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def comments_like_inbox_comment(
        post_id: str, comment_id: str, account_id: str, cid: str = ""
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

    @mcp.tool()
    def comments_unlike_inbox_comment(
        post_id: str, comment_id: str, account_id: str, like_uri: str = ""
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

    @mcp.tool()
    def comments_send_private_reply_to_comment(
        post_id: str, comment_id: str, account_id: str, message: str
    ) -> str:
        """Send private reply

        Args:
            post_id: The media/post ID (Instagram media ID or Facebook post ID) (required)
            comment_id: The comment ID to send a private reply to (required)
            account_id: The social account ID (Instagram or Facebook) (required)
            message: The message text to send as a private DM (required)"""
        client = _get_client()
        try:
            response = client.comments.send_private_reply_to_comment(
                post_id=post_id,
                comment_id=comment_id,
                account_id=account_id,
                message=message,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # CONNECT

    @mcp.tool()
    def connect_get_connect_url(
        platform: str, profile_id: str, redirect_url: str = "", headless: bool = False
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def connect_select_facebook_page(
        profile_id: str,
        page_id: str,
        temp_token: str,
        user_profile: str = "",
        redirect_url: str = "",
    ) -> str:
        """Select Facebook page

        Args:
            profile_id: Profile ID from your connection flow (required)
            page_id: The Facebook Page ID selected by the user (required)
            temp_token: Temporary Facebook access token from OAuth (required)
            user_profile: Decoded user profile object from the OAuth callback
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

    @mcp.tool()
    def connect_list_google_business_locations(profile_id: str, temp_token: str) -> str:
        """List GBP locations

        Args:
            profile_id: Profile ID from your connection flow (required)
            temp_token: Temporary Google access token from the OAuth callback redirect (required)"""
        client = _get_client()
        try:
            response = client.connect.list_google_business_locations(
                profile_id=profile_id, temp_token=temp_token
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def connect_select_google_business_location(
        profile_id: str,
        location_id: str,
        temp_token: str,
        user_profile: str = "",
        redirect_url: str = "",
    ) -> str:
        """Select GBP location

        Args:
            profile_id: Profile ID from your connection flow (required)
            location_id: The Google Business location ID selected by the user (required)
            temp_token: Temporary Google access token from OAuth (required)
            user_profile: Decoded user profile from the OAuth callback. Contains the refresh token. Always include this field.
            redirect_url: Optional custom redirect URL to return to after selection"""
        client = _get_client()
        try:
            response = client.connect.select_google_business_location(
                profile_id=profile_id,
                location_id=location_id,
                temp_token=temp_token,
                user_profile=user_profile,
                redirect_url=redirect_url,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def connect_select_linked_in_organization(
        profile_id: str,
        temp_token: str,
        user_profile: str,
        account_type: str,
        selected_organization: str = "",
        redirect_url: str = "",
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

    @mcp.tool()
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

    @mcp.tool()
    def connect_select_pinterest_board(
        profile_id: str,
        board_id: str,
        temp_token: str,
        board_name: str = "",
        user_profile: str = "",
        refresh_token: str = "",
        expires_in: int = 0,
        redirect_url: str = "",
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

    @mcp.tool()
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

    @mcp.tool()
    def connect_select_snapchat_profile(
        profile_id: str,
        selected_public_profile: str,
        temp_token: str,
        user_profile: str,
        refresh_token: str = "",
        expires_in: int = 0,
        redirect_url: str = "",
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

    @mcp.tool()
    def connect_bluesky_credentials(
        identifier: str, app_password: str, state: str, redirect_uri: str = ""
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def connect_get_facebook_pages(account_id: str) -> str:
        """List Facebook pages

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.connect.get_facebook_pages(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def connect_update_linked_in_organization(
        account_id: str, account_type: str, selected_organization: str = ""
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

    @mcp.tool()
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

    @mcp.tool()
    def connect_update_pinterest_boards(
        account_id: str, default_board_id: str, default_board_name: str = ""
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def contacts_list_contacts(
        profile_id: str = "",
        search: str = "",
        tag: str = "",
        platform: str = "",
        is_subscribed: str = "",
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

    @mcp.tool()
    def contacts_create_contact(
        profile_id: str,
        name: str,
        email: str = "",
        company: str = "",
        tags: str = "",
        is_subscribed: bool = True,
        notes: str = "",
        account_id: str = "",
        platform: str = "",
        platform_identifier: str = "",
        display_identifier: str = "",
    ) -> str:
        """Create a contact

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

    @mcp.tool()
    def contacts_get_contact(contact_id: str) -> str:
        """Get contact with channels

        Args:
            contact_id: (required)"""
        client = _get_client()
        try:
            response = client.contacts.get_contact(contact_id=contact_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def contacts_update_contact(
        contact_id: str,
        name: str = "",
        email: str = "",
        company: str = "",
        avatar_url: str = "",
        tags: str = "",
        is_subscribed: bool = False,
        is_blocked: bool = False,
        notes: str = "",
    ) -> str:
        """Update a contact

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

    @mcp.tool()
    def contacts_delete_contact(contact_id: str) -> str:
        """Delete a contact

        Args:
            contact_id: (required)"""
        client = _get_client()
        try:
            response = client.contacts.delete_contact(contact_id=contact_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
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

    @mcp.tool()
    def contacts_bulk_create_contacts(
        profile_id: str, account_id: str, platform: str, contacts: str
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

    @mcp.tool()
    def custom_fields_set_contact_field_value(
        contact_id: str, slug: str, value: str
    ) -> str:
        """Set a custom field value

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

    @mcp.tool()
    def custom_fields_clear_contact_field_value(contact_id: str, slug: str) -> str:
        """Clear a custom field value

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

    @mcp.tool()
    def custom_fields_list_custom_fields(profile_id: str = "") -> str:
        """List custom field definitions

        Args:
            profile_id: Filter by profile. Omit to list across all profiles"""
        client = _get_client()
        try:
            response = client.custom_fields.list_custom_fields(profile_id=profile_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def custom_fields_create_custom_field(
        profile_id: str, name: str, type: str, slug: str = "", options: str = ""
    ) -> str:
        """Create a custom field definition

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

    @mcp.tool()
    def custom_fields_update_custom_field(
        field_id: str, name: str = "", options: str = ""
    ) -> str:
        """Update a custom field definition

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

    @mcp.tool()
    def custom_fields_delete_custom_field(field_id: str) -> str:
        """Delete a custom field definition

        Args:
            field_id: (required)"""
        client = _get_client()
        try:
            response = client.custom_fields.delete_custom_field(field_id=field_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # INVITES

    @mcp.tool()
    def invites_create_invite_token(scope: str, profile_ids: str = "") -> str:
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

    @mcp.tool()
    def logs_list_posts_logs(
        status: str = "",
        platform: str = "",
        action: str = "",
        days: int = 7,
        limit: int = 50,
        skip: int = 0,
        search: str = "",
    ) -> str:
        """List publishing logs

        Args:
            status: Filter by log status
            platform: Filter by platform
            action: Filter by action type
            days: Number of days to look back (max 7)
            limit: Maximum number of logs to return (max 100)
            skip: Number of logs to skip (for pagination)
            search: Search through log entries by text content."""
        client = _get_client()
        try:
            response = client.logs.list_posts_logs(
                status=status,
                platform=platform,
                action=action,
                days=days,
                limit=limit,
                skip=skip,
                search=search,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def logs_list_connection_logs(
        platform: str = "",
        event_type: str = "",
        status: str = "",
        days: int = 7,
        limit: int = 50,
        skip: int = 0,
    ) -> str:
        """List connection logs

        Args:
            platform: Filter by platform
            event_type: Filter by event type
            status: Filter by status (shorthand for event types)
            days: Number of days to look back (max 7)
            limit: Maximum number of logs to return (max 100)
            skip: Number of logs to skip (for pagination)"""
        client = _get_client()
        try:
            response = client.logs.list_connection_logs(
                platform=platform,
                event_type=event_type,
                status=status,
                days=days,
                limit=limit,
                skip=skip,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def logs_get_post_logs(post_id: str, limit: int = 50) -> str:
        """Get post logs

        Args:
            post_id: The post ID (required)
            limit: Maximum number of logs to return (max 100)"""
        client = _get_client()
        try:
            response = client.logs.get_post_logs(post_id=post_id, limit=limit)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # MEDIA

    @mcp.tool()
    def media_get_media_presigned_url(
        filename: str, content_type: str, size: int = 0
    ) -> str:
        """Get presigned upload URL

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

    @mcp.tool()
    def messages_list_inbox_conversations(
        profile_id: str = "",
        platform: str = "",
        status: str = "",
        sort_order: str = "desc",
        limit: int = 50,
        cursor: str = "",
        account_id: str = "",
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def messages_get_inbox_conversation_messages(
        conversation_id: str, account_id: str
    ) -> str:
        """List messages

        Args:
            conversation_id: The conversation ID (id field from list conversations endpoint). This is the platform-specific conversation identifier, not an internal database ID. (required)
            account_id: Social account ID (required)"""
        client = _get_client()
        try:
            response = client.messages.get_inbox_conversation_messages(
                conversation_id=conversation_id, account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def messages_send_inbox_message(
        conversation_id: str,
        account_id: str,
        message: str = "",
        attachment_url: str = "",
        attachment_type: str = "",
        quick_replies: str = "",
        buttons: str = "",
        template: str = "",
        reply_markup: str = "",
        messaging_type: str = "",
        message_tag: str = "",
        reply_to: str = "",
    ) -> str:
        """Send message

        Args:
            conversation_id: The conversation ID (id field from list conversations endpoint). This is the platform-specific conversation identifier, not an internal database ID. (required)
            account_id: Social account ID (required)
            message: Message text
            attachment_url: URL of the attachment to send (image, video, audio, or file). The URL must be publicly accessible. For binary file uploads, use multipart/form-data instead.
            attachment_type: Type of attachment. Defaults to file if not specified.
            quick_replies: Quick reply buttons. Mutually exclusive with buttons. Max 13 items.
            buttons: Action buttons. Mutually exclusive with quickReplies. Max 3 items.
            template: Generic template for carousels (Instagram/Facebook only, ignored on Telegram).
            reply_markup: Telegram-native keyboard markup. Ignored on other platforms.
            messaging_type: Facebook messaging type. Required when using messageTag.
            message_tag: Facebook message tag for messaging outside 24h window. Requires messagingType MESSAGE_TAG. Instagram only supports HUMAN_AGENT.
            reply_to: Platform message ID to reply to (Telegram only)."""
        client = _get_client()
        try:
            response = client.messages.send_inbox_message(
                conversation_id=conversation_id,
                account_id=account_id,
                message=message,
                attachment_url=attachment_url,
                attachment_type=attachment_type,
                quick_replies=quick_replies,
                buttons=buttons,
                template=template,
                reply_markup=reply_markup,
                messaging_type=messaging_type,
                message_tag=message_tag,
                reply_to=reply_to,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def messages_edit_inbox_message(
        conversation_id: str,
        message_id: str,
        account_id: str,
        text: str = "",
        reply_markup: str = "",
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

    # POSTS

    @mcp.tool()
    def posts_list_posts(
        page: int = 1,
        limit: int = 10,
        status: str = "",
        platform: str = "",
        profile_id: str = "",
        created_by: str = "",
        date_from: str = "",
        date_to: str = "",
        include_hidden: bool = False,
        search: str = "",
        sort_by: str = "scheduled-desc",
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
            sort_by: Sort order for results."""
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
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
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

    @mcp.tool()
    def posts_update_post(
        post_id: str,
        content: str = "",
        scheduled_for: str = "",
        tiktok_settings: str = "",
        recycling: str = "",
    ) -> str:
        """Update post

        Args:
            post_id: (required)
            content
            scheduled_for
            tiktok_settings: Root-level TikTok settings applied to all TikTok platforms. Merged into each platform's platformSpecificData, with platform-specific settings taking precedence.
            recycling"""
        client = _get_client()
        try:
            response = client.posts.update_post(
                post_id=post_id,
                content=content,
                scheduled_for=scheduled_for,
                tiktok_settings=tiktok_settings,
                recycling=recycling,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def posts_update_post_metadata(
        post_id: str,
        platform: str,
        video_id: str = "",
        account_id: str = "",
        title: str = "",
        description: str = "",
        tags: str = "",
        category_id: str = "",
        privacy_status: str = "",
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
            privacy_status: Video privacy setting"""
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
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # PROFILES

    @mcp.tool()
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

    @mcp.tool()
    def profiles_create_profile(
        name: str, description: str = "", color: str = ""
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

    @mcp.tool()
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

    @mcp.tool()
    def profiles_update_profile(
        profile_id: str,
        name: str = "",
        description: str = "",
        color: str = "",
        is_default: bool = False,
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

    @mcp.tool()
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

    @mcp.tool()
    def queue_list_queue_slots(
        profile_id: str, queue_id: str = "", all: str = ""
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

    @mcp.tool()
    def queue_create_queue_slot(
        profile_id: str, name: str, timezone: str, slots: str, active: bool = True
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

    @mcp.tool()
    def queue_update_queue_slot(
        profile_id: str,
        timezone: str,
        slots: str,
        queue_id: str = "",
        name: str = "",
        active: bool = True,
        set_as_default: bool = False,
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

    @mcp.tool()
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

    @mcp.tool()
    def queue_preview_queue(
        profile_id: str, queue_id: str = "", count: int = 20
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

    @mcp.tool()
    def queue_get_next_queue_slot(profile_id: str, queue_id: str = "") -> str:
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

    @mcp.tool()
    def reddit_search_reddit(
        account_id: str,
        q: str,
        subreddit: str = "",
        restrict_sr: str = "",
        sort: str = "new",
        limit: int = 25,
        after: str = "",
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

    @mcp.tool()
    def reddit_get_reddit_feed(
        account_id: str,
        subreddit: str = "",
        sort: str = "hot",
        limit: int = 25,
        after: str = "",
        t: str = "",
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

    @mcp.tool()
    def reviews_list_inbox_reviews(
        profile_id: str = "",
        platform: str = "",
        min_rating: int = 0,
        max_rating: int = 0,
        has_reply: bool = False,
        sort_by: str = "date",
        sort_order: str = "desc",
        limit: int = 25,
        cursor: str = "",
        account_id: str = "",
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def sequences_list_sequences(
        profile_id: str = "", status: str = "", limit: int = 50, skip: int = 0
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

    @mcp.tool()
    def sequences_create_sequence(
        profile_id: str,
        account_id: str,
        platform: str,
        name: str,
        description: str = "",
        steps: str = "",
        exit_on_reply: bool = True,
        exit_on_unsubscribe: bool = True,
    ) -> str:
        """Create a sequence

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

    @mcp.tool()
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

    @mcp.tool()
    def sequences_update_sequence(sequence_id: str) -> str:
        """Update a sequence

        Args:
            sequence_id: (required)"""
        client = _get_client()
        try:
            response = client.sequences.update_sequence(sequence_id=sequence_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def sequences_delete_sequence(sequence_id: str) -> str:
        """Delete a sequence

        Args:
            sequence_id: (required)"""
        client = _get_client()
        try:
            response = client.sequences.delete_sequence(sequence_id=sequence_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def sequences_activate_sequence(sequence_id: str) -> str:
        """Activate a sequence

        Args:
            sequence_id: (required)"""
        client = _get_client()
        try:
            response = client.sequences.activate_sequence(sequence_id=sequence_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def sequences_pause_sequence(sequence_id: str) -> str:
        """Pause a sequence

        Args:
            sequence_id: (required)"""
        client = _get_client()
        try:
            response = client.sequences.pause_sequence(sequence_id=sequence_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def sequences_enroll_contacts(
        sequence_id: str, contact_ids: str, channel_ids: str = ""
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

    @mcp.tool()
    def sequences_unenroll_contact(sequence_id: str, contact_id: str) -> str:
        """Unenroll a contact from a sequence

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

    @mcp.tool()
    def sequences_list_sequence_enrollments(
        sequence_id: str, status: str = "", limit: int = 50, skip: int = 0
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

    # TOOLS

    @mcp.tool()
    def tools_download_you_tube_video(
        url: str,
        action: str = "download",
        format: str = "video",
        quality: str = "hd",
        format_id: str = "",
    ) -> str:
        """Download YouTube video

        Args:
            url: YouTube video URL or video ID (required)
            action: Action to perform: 'download' returns download URL, 'formats' lists available formats
            format: Desired format (when action=download)
            quality: Desired quality (when action=download)
            format_id: Specific format ID from formats list"""
        client = _get_client()
        try:
            response = client.tools.download_you_tube_video(
                url=url,
                action=action,
                format=format,
                quality=quality,
                format_id=format_id,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def tools_get_you_tube_transcript(url: str, lang: str = "en") -> str:
        """Get YouTube transcript

        Args:
            url: YouTube video URL or video ID (required)
            lang: Language code for transcript"""
        client = _get_client()
        try:
            response = client.tools.get_you_tube_transcript(url=url, lang=lang)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def tools_download_instagram_media(url: str) -> str:
        """Download Instagram media

        Args:
            url: Instagram reel or post URL (required)"""
        client = _get_client()
        try:
            response = client.tools.download_instagram_media(url=url)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def tools_check_instagram_hashtags(hashtags: str) -> str:
        """Check IG hashtag bans

        Args:
            hashtags: (required)"""
        client = _get_client()
        try:
            response = client.tools.check_instagram_hashtags(hashtags=hashtags)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def tools_download_tik_tok_video(
        url: str, action: str = "download", format_id: str = ""
    ) -> str:
        """Download TikTok video

        Args:
            url: TikTok video URL or ID (required)
            action: 'formats' to list available formats
            format_id: Specific format ID (0 = no watermark, etc.)"""
        client = _get_client()
        try:
            response = client.tools.download_tik_tok_video(
                url=url, action=action, format_id=format_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def tools_download_twitter_media(
        url: str, action: str = "download", format_id: str = ""
    ) -> str:
        """Download Twitter/X media

        Args:
            url: Twitter/X post URL (required)
            action
            format_id"""
        client = _get_client()
        try:
            response = client.tools.download_twitter_media(
                url=url, action=action, format_id=format_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def tools_download_facebook_video(url: str) -> str:
        """Download Facebook video

        Args:
            url: Facebook video or reel URL (required)"""
        client = _get_client()
        try:
            response = client.tools.download_facebook_video(url=url)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def tools_download_linked_in_video(url: str) -> str:
        """Download LinkedIn video

        Args:
            url: LinkedIn post URL (required)"""
        client = _get_client()
        try:
            response = client.tools.download_linked_in_video(url=url)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def tools_download_bluesky_media(url: str) -> str:
        """Download Bluesky media

        Args:
            url: Bluesky post URL (required)"""
        client = _get_client()
        try:
            response = client.tools.download_bluesky_media(url=url)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # TWITTER_ENGAGEMENT

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def usage_get_usage_stats() -> str:
        """Get plan and usage stats"""
        client = _get_client()
        try:
            response = client.usage.get_usage_stats()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # USERS

    @mcp.tool()
    def users_list_users() -> str:
        """List users"""
        client = _get_client()
        try:
            response = client.users.list_users()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
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

    @mcp.tool()
    def validate_post_length(text: str) -> str:
        """Validate post character count

        Args:
            text: The post text to check (required)"""
        client = _get_client()
        try:
            response = client.validate.validate_post_length(text=text)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def validate_post(platforms: str, content: str = "", media_items: str = "") -> str:
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

    @mcp.tool()
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

    @mcp.tool()
    def validate_subreddit(name: str) -> str:
        """Check subreddit existence

        Args:
            name: Subreddit name (with or without "r/" prefix) (required)"""
        client = _get_client()
        try:
            response = client.validate.validate_subreddit(name=name)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # WEBHOOKS

    @mcp.tool()
    def webhooks_get_webhook_settings() -> str:
        """List webhooks"""
        client = _get_client()
        try:
            response = client.webhooks.get_webhook_settings()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def webhooks_create_webhook_settings(
        name: str = "",
        url: str = "",
        secret: str = "",
        events: str = "",
        is_active: bool = False,
        custom_headers: str = "",
    ) -> str:
        """Create webhook

        Args:
            name: Webhook name (max 50 characters)
            url: Webhook endpoint URL (must be HTTPS in production)
            secret: Secret key for HMAC-SHA256 signature verification
            events: Events to subscribe to
            is_active: Enable or disable webhook delivery
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

    @mcp.tool()
    def webhooks_update_webhook_settings(
        id: str,
        name: str = "",
        url: str = "",
        secret: str = "",
        events: str = "",
        is_active: bool = False,
        custom_headers: str = "",
    ) -> str:
        """Update webhook

        Args:
            id: Webhook ID to update (required) (required)
            name: Webhook name (max 50 characters)
            url: Webhook endpoint URL (must be HTTPS in production)
            secret: Secret key for HMAC-SHA256 signature verification
            events: Events to subscribe to
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def webhooks_get_webhook_logs(
        limit: int = 50, status: str = "", event: str = "", webhook_id: str = ""
    ) -> str:
        """Get delivery logs

        Args:
            limit: Maximum number of logs to return (max 100)
            status: Filter by delivery status
            event: Filter by event type
            webhook_id: Filter by webhook ID"""
        client = _get_client()
        try:
            response = client.webhooks.get_webhook_logs(
                limit=limit, status=status, event=event, webhook_id=webhook_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # WHATSAPP

    @mcp.tool()
    def whatsapp_send_whats_app_bulk(
        account_id: str, recipients: str, template: str
    ) -> str:
        """Bulk send template messages

        Args:
            account_id: WhatsApp social account ID (required)
            recipients: List of recipients (max 100) (required)
            template: (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.send_whats_app_bulk(
                account_id=account_id, recipients=recipients, template=template
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_get_whats_app_contacts(
        account_id: str,
        search: str = "",
        tag: str = "",
        group: str = "",
        opted_in: str = "",
        limit: int = 50,
        skip: int = 0,
    ) -> str:
        """List contacts

        Args:
            account_id: WhatsApp social account ID (required)
            search: Search contacts by name, phone, email, or company
            tag: Filter by tag
            group: Filter by group
            opted_in: Filter by opt-in status
            limit: Maximum results (default 50)
            skip: Offset for pagination"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_contacts(
                account_id=account_id,
                search=search,
                tag=tag,
                group=group,
                opted_in=opted_in,
                limit=limit,
                skip=skip,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_create_whats_app_contact(
        account_id: str,
        phone: str,
        name: str,
        email: str = "",
        company: str = "",
        tags: str = "",
        groups: str = "",
        is_opted_in: bool = True,
        custom_fields: str = "",
        notes: str = "",
    ) -> str:
        """Create contact

        Args:
            account_id: WhatsApp social account ID (required)
            phone: Phone number in E.164 format (required)
            name: Contact name (required)
            email: Contact email
            company: Company name
            tags: Tags for categorization
            groups: Groups the contact belongs to
            is_opted_in: Whether the contact has opted in to receive messages
            custom_fields: Custom key-value fields
            notes: Notes about the contact"""
        client = _get_client()
        try:
            response = client.whatsapp.create_whats_app_contact(
                account_id=account_id,
                phone=phone,
                name=name,
                email=email,
                company=company,
                tags=tags,
                groups=groups,
                is_opted_in=is_opted_in,
                custom_fields=custom_fields,
                notes=notes,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_get_whats_app_contact(contact_id: str) -> str:
        """Get contact

        Args:
            contact_id: Contact ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_contact(contact_id=contact_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_update_whats_app_contact(
        contact_id: str,
        name: str = "",
        email: str = "",
        company: str = "",
        tags: str = "",
        groups: str = "",
        is_opted_in: bool = False,
        is_blocked: bool = False,
        custom_fields: str = "",
        notes: str = "",
    ) -> str:
        """Update contact

        Args:
            contact_id: Contact ID (required)
            name: Contact name
            email: Contact email
            company: Company name
            tags: Tags (replaces existing)
            groups: Groups (replaces existing)
            is_opted_in: Opt-in status (changes are timestamped)
            is_blocked: Block status
            custom_fields: Custom fields to merge (set value to null to remove a field)
            notes: Notes about the contact"""
        client = _get_client()
        try:
            response = client.whatsapp.update_whats_app_contact(
                contact_id=contact_id,
                name=name,
                email=email,
                company=company,
                tags=tags,
                groups=groups,
                is_opted_in=is_opted_in,
                is_blocked=is_blocked,
                custom_fields=custom_fields,
                notes=notes,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_delete_whats_app_contact(contact_id: str) -> str:
        """Delete contact

        Args:
            contact_id: Contact ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.delete_whats_app_contact(contact_id=contact_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_import_whats_app_contacts(
        account_id: str,
        contacts: str,
        default_tags: str = "",
        default_groups: str = "",
        skip_duplicates: bool = True,
    ) -> str:
        """Bulk import contacts

        Args:
            account_id: WhatsApp social account ID (required)
            contacts: Contacts to import (max 1000) (required)
            default_tags: Tags applied to all imported contacts
            default_groups: Groups applied to all imported contacts
            skip_duplicates: Skip contacts with existing phone numbers"""
        client = _get_client()
        try:
            response = client.whatsapp.import_whats_app_contacts(
                account_id=account_id,
                contacts=contacts,
                default_tags=default_tags,
                default_groups=default_groups,
                skip_duplicates=skip_duplicates,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_bulk_update_whats_app_contacts(
        action: str, contact_ids: str, tags: str = "", groups: str = ""
    ) -> str:
        """Bulk update contacts

        Args:
            action: Bulk action to perform (required)
            contact_ids: Contact IDs to update (max 500) (required)
            tags: Tags to add or remove (required for addTags/removeTags)
            groups: Groups to add or remove (required for addGroups/removeGroups)"""
        client = _get_client()
        try:
            response = client.whatsapp.bulk_update_whats_app_contacts(
                action=action, contact_ids=contact_ids, tags=tags, groups=groups
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_bulk_delete_whats_app_contacts(contact_ids: str) -> str:
        """Bulk delete contacts

        Args:
            contact_ids: Contact IDs to delete (max 500) (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.bulk_delete_whats_app_contacts(
                contact_ids=contact_ids
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_get_whats_app_groups(account_id: str) -> str:
        """List contact groups

        Args:
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_groups(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_rename_whats_app_group(
        account_id: str, old_name: str, new_name: str
    ) -> str:
        """Rename group

        Args:
            account_id: WhatsApp social account ID (required)
            old_name: Current group name (required)
            new_name: New group name (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.rename_whats_app_group(
                account_id=account_id, old_name=old_name, new_name=new_name
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_delete_whats_app_group(account_id: str, group_name: str) -> str:
        """Delete group

        Args:
            account_id: WhatsApp social account ID (required)
            group_name: Group name to delete (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.delete_whats_app_group(
                account_id=account_id, group_name=group_name
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
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

    @mcp.tool()
    def whatsapp_create_whats_app_template(
        account_id: str,
        name: str,
        category: str,
        language: str,
        components: str = "",
        library_template_name: str = "",
        library_template_body_inputs: str = "",
        library_template_button_inputs: str = "",
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
        by Meta with no review wait. Omit `components` when using this field.
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

    @mcp.tool()
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

    @mcp.tool()
    def whatsapp_update_whats_app_template(
        template_name: str, account_id: str, components: str
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

    @mcp.tool()
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

    @mcp.tool()
    def whatsapp_get_whats_app_broadcasts(
        account_id: str, status: str = "", limit: int = 50, skip: int = 0
    ) -> str:
        """List broadcasts

        Args:
            account_id: WhatsApp social account ID (required)
            status: Filter by broadcast status
            limit: Maximum results (default 50)
            skip: Offset for pagination"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_broadcasts(
                account_id=account_id, status=status, limit=limit, skip=skip
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_create_whats_app_broadcast(
        account_id: str,
        name: str,
        template: str,
        description: str = "",
        recipients: str = "",
    ) -> str:
        """Create broadcast

        Args:
            account_id: WhatsApp social account ID (required)
            name: Broadcast name (required)
            description: Broadcast description
            template: (required)
            recipients: Initial recipients (optional)"""
        client = _get_client()
        try:
            response = client.whatsapp.create_whats_app_broadcast(
                account_id=account_id,
                name=name,
                description=description,
                template=template,
                recipients=recipients,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_get_whats_app_broadcast(broadcast_id: str) -> str:
        """Get broadcast

        Args:
            broadcast_id: Broadcast ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_broadcast(
                broadcast_id=broadcast_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_delete_whats_app_broadcast(broadcast_id: str) -> str:
        """Delete broadcast

        Args:
            broadcast_id: Broadcast ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.delete_whats_app_broadcast(
                broadcast_id=broadcast_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_send_whats_app_broadcast(broadcast_id: str) -> str:
        """Send broadcast

        Args:
            broadcast_id: Broadcast ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.send_whats_app_broadcast(
                broadcast_id=broadcast_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_schedule_whats_app_broadcast(
        broadcast_id: str, scheduled_at: str
    ) -> str:
        """Schedule broadcast

        Args:
            broadcast_id: Broadcast ID (required)
            scheduled_at: ISO 8601 date-time for sending (must be in the future, max 30 days) (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.schedule_whats_app_broadcast(
                broadcast_id=broadcast_id, scheduled_at=scheduled_at
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_cancel_whats_app_broadcast_schedule(broadcast_id: str) -> str:
        """Cancel scheduled broadcast

        Args:
            broadcast_id: Broadcast ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.cancel_whats_app_broadcast_schedule(
                broadcast_id=broadcast_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_get_whats_app_broadcast_recipients(
        broadcast_id: str, status: str = "", limit: int = 100, skip: int = 0
    ) -> str:
        """List recipients

        Args:
            broadcast_id: Broadcast ID (required)
            status: Filter by recipient delivery status
            limit: Maximum results (default 100)
            skip: Offset for pagination"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_broadcast_recipients(
                broadcast_id=broadcast_id, status=status, limit=limit, skip=skip
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_add_whats_app_broadcast_recipients(
        broadcast_id: str, recipients: str
    ) -> str:
        """Add recipients

        Args:
            broadcast_id: Broadcast ID (required)
            recipients: Recipients to add (max 1000) (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.add_whats_app_broadcast_recipients(
                broadcast_id=broadcast_id, recipients=recipients
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_remove_whats_app_broadcast_recipients(
        broadcast_id: str, phones: str
    ) -> str:
        """Remove recipients

        Args:
            broadcast_id: Broadcast ID (required)
            phones: Phone numbers to remove (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.remove_whats_app_broadcast_recipients(
                broadcast_id=broadcast_id, phones=phones
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
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

    @mcp.tool()
    def whatsapp_update_whats_app_business_profile(
        account_id: str,
        about: str = "",
        address: str = "",
        description: str = "",
        email: str = "",
        websites: str = "",
        vertical: str = "",
        profile_picture_handle: str = "",
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

    @mcp.tool()
    def whatsapp_upload_whats_app_profile_photo() -> str:
        """Upload profile picture"""
        client = _get_client()
        try:
            response = client.whatsapp.upload_whats_app_profile_photo()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def whatsapp_get_whats_app_display_name(account_id: str) -> str:
        """Get display name and review status

        Args:
            account_id: WhatsApp social account ID (required)"""
        client = _get_client()
        try:
            response = client.whatsapp.get_whats_app_display_name(account_id=account_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
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

    @mcp.tool()
    def whatsapp_list_whats_app_group_chats(
        account_id: str, limit: int = 25, after: str = ""
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

    @mcp.tool()
    def whatsapp_create_whats_app_group_chat(
        account_id: str,
        subject: str,
        description: str = "",
        join_approval_mode: str = "",
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

    @mcp.tool()
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

    @mcp.tool()
    def whatsapp_update_whats_app_group_chat(
        group_id: str,
        account_id: str,
        subject: str = "",
        description: str = "",
        join_approval_mode: str = "",
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

    @mcp.tool()
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

    @mcp.tool()
    def whatsapp_add_whats_app_group_participants(
        group_id: str, account_id: str, phone_numbers: str
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

    @mcp.tool()
    def whatsapp_remove_whats_app_group_participants(
        group_id: str, account_id: str, phone_numbers: str
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
    def whatsapp_approve_whats_app_group_join_requests(
        group_id: str, account_id: str, phone_numbers: str
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

    @mcp.tool()
    def whatsapp_reject_whats_app_group_join_requests(
        group_id: str, account_id: str, phone_numbers: str
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

    # WHATSAPP_PHONE_NUMBERS

    @mcp.tool()
    def whatsapp_phone_numbers_get_whats_app_phone_numbers(
        status: str = "", profile_id: str = ""
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

    @mcp.tool()
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

    @mcp.tool()
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

    @mcp.tool()
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
