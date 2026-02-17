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
                name=name, accountIds=account_ids
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
                group_id=group_id, name=name, accountIds=account_ids
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
        profile_id: str = "", include_over_limit: bool = False
    ) -> str:
        """List accounts

        Args:
            profile_id: Filter accounts by profile ID
            include_over_limit: When true, includes accounts from over-limit profiles."""
        client = _get_client()
        try:
            response = client.accounts.list_accounts(
                profile_id=profile_id, include_over_limit=include_over_limit
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
                account_id=account_id, username=username, displayName=display_name
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
    def accounts_get_google_business_reviews(
        account_id: str, page_size: int = 50, page_token: str = ""
    ) -> str:
        """Get reviews

        Args:
            account_id: The Late account ID (from /v1/accounts) (required)
            page_size: Number of reviews to fetch per page (max 50)
            page_token: Pagination token from previous response"""
        client = _get_client()
        try:
            response = client.accounts.get_google_business_reviews(
                account_id=account_id, page_size=page_size, page_token=page_token
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_get_google_business_food_menus(account_id: str) -> str:
        """Get food menus

        Args:
            account_id: The Late account ID (from /v1/accounts) (required)"""
        client = _get_client()
        try:
            response = client.accounts.get_google_business_food_menus(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_update_google_business_food_menus(
        account_id: str, menus: str, update_mask: str = ""
    ) -> str:
        """Update food menus

        Args:
            account_id: The Late account ID (from /v1/accounts) (required)
            menus: Array of food menus to set (required)
            update_mask: Field mask for partial updates (e.g. "menus")"""
        client = _get_client()
        try:
            response = client.accounts.update_google_business_food_menus(
                account_id=account_id, menus=menus, updateMask=update_mask
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_get_google_business_location_details(
        account_id: str, read_mask: str = ""
    ) -> str:
        """Get location details

        Args:
            account_id: The Late account ID (from /v1/accounts) (required)
            read_mask: Comma-separated fields to return. Available: name, title, phoneNumbers, categories, storefrontAddress, websiteUri, regularHours, specialHours, serviceArea, profile, openInfo, metadata, moreHours."""
        client = _get_client()
        try:
            response = client.accounts.get_google_business_location_details(
                account_id=account_id, read_mask=read_mask
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_update_google_business_location_details(
        account_id: str,
        update_mask: str,
        regular_hours: str = "",
        special_hours: str = "",
        profile: str = "",
        website_uri: str = "",
        phone_numbers: str = "",
    ) -> str:
        """Update location details

        Args:
            account_id: The Late account ID (from /v1/accounts) (required)
            update_mask: Required. Comma-separated fields to update (e.g. 'regularHours', 'specialHours', 'profile.description') (required)
            regular_hours
            special_hours
            profile
            website_uri
            phone_numbers"""
        client = _get_client()
        try:
            response = client.accounts.update_google_business_location_details(
                account_id=account_id,
                updateMask=update_mask,
                regularHours=regular_hours,
                specialHours=special_hours,
                profile=profile,
                websiteUri=website_uri,
                phoneNumbers=phone_numbers,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_list_google_business_media(
        account_id: str, page_size: int = 100, page_token: str = ""
    ) -> str:
        """List media

        Args:
            account_id: (required)
            page_size: Number of items to return (max 100)
            page_token: Pagination token from previous response"""
        client = _get_client()
        try:
            response = client.accounts.list_google_business_media(
                account_id=account_id, page_size=page_size, page_token=page_token
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_create_google_business_media(
        account_id: str,
        source_url: str,
        media_format: str = "PHOTO",
        description: str = "",
        category: str = "",
    ) -> str:
        """Upload photo

        Args:
            account_id: (required)
            source_url: Publicly accessible image URL (required)
            media_format
            description: Photo description
            category: Where the photo appears on the listing"""
        client = _get_client()
        try:
            response = client.accounts.create_google_business_media(
                account_id=account_id,
                sourceUrl=source_url,
                mediaFormat=media_format,
                description=description,
                category=category,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_delete_google_business_media(account_id: str, media_id: str) -> str:
        """Delete photo

        Args:
            account_id: (required)
            media_id: The media item ID to delete (required)"""
        client = _get_client()
        try:
            response = client.accounts.delete_google_business_media(
                account_id=account_id, media_id=media_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_get_google_business_attributes(account_id: str) -> str:
        """Get attributes

        Args:
            account_id: (required)"""
        client = _get_client()
        try:
            response = client.accounts.get_google_business_attributes(
                account_id=account_id
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_update_google_business_attributes(
        account_id: str, attributes: str, attribute_mask: str
    ) -> str:
        """Update attributes

        Args:
            account_id: (required)
            attributes: (required)
            attribute_mask: Comma-separated attribute names to update (e.g. 'has_delivery,has_takeout') (required)"""
        client = _get_client()
        try:
            response = client.accounts.update_google_business_attributes(
                account_id=account_id,
                attributes=attributes,
                attributeMask=attribute_mask,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_list_google_business_place_actions(
        account_id: str, page_size: int = 100, page_token: str = ""
    ) -> str:
        """List action links

        Args:
            account_id: (required)
            page_size
            page_token"""
        client = _get_client()
        try:
            response = client.accounts.list_google_business_place_actions(
                account_id=account_id, page_size=page_size, page_token=page_token
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_create_google_business_place_action(
        account_id: str, uri: str, place_action_type: str
    ) -> str:
        """Create action link

        Args:
            account_id: (required)
            uri: The action URL (required)
            place_action_type: Type of action (required)"""
        client = _get_client()
        try:
            response = client.accounts.create_google_business_place_action(
                account_id=account_id, uri=uri, placeActionType=place_action_type
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def accounts_delete_google_business_place_action(account_id: str, name: str) -> str:
        """Delete action link

        Args:
            account_id: (required)
            name: The resource name of the place action link (e.g. locations/123/placeActionLinks/456) (required)"""
        client = _get_client()
        try:
            response = client.accounts.delete_google_business_place_action(
                account_id=account_id, name=name
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
            post_id: Returns analytics for a single post. Accepts both Late Post IDs and External Post IDs. Late IDs are auto-resolved to External Post analytics.
            platform: Filter by platform (default "all")
            profile_id: Filter by profile ID (default "all")
            source: Filter by post source: late (posted via Late API), external (synced from platform), all (default)
            from_date: Inclusive lower bound
            to_date: Inclusive upper bound
            limit: Page size (default 50)
            page: Page number (default 1)
            sort_by: Sort by date or engagement
            order: Sort order"""
        client = _get_client()
        try:
            response = client.analytics.get_analytics(
                post_id=post_id,
                platform=platform,
                profile_id=profile_id,
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
            account_id: The Late account ID for the YouTube account (required)
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
    def api_keys_create_api_key(name: str, expires_in: int = 0) -> str:
        """Create key

        Args:
            name: (required)
            expires_in: Days until expiry"""
        client = _get_client()
        try:
            response = client.api_keys.create_api_key(name=name, expiresIn=expires_in)
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
            post_id: Late post ID or platform-specific post ID. Late IDs are auto-resolved. LinkedIn third-party posts accept full activity URN or numeric ID. (required)
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
        subreddit: str = "",
        parent_cid: str = "",
        root_uri: str = "",
        root_cid: str = "",
    ) -> str:
        """Reply to comment

        Args:
            post_id: Late post ID or platform-specific post ID. LinkedIn third-party posts accept full activity URN or numeric ID. (required)
            account_id: (required)
            message: (required)
            comment_id: Reply to specific comment (optional)
            subreddit: (Reddit only) Subreddit name for replies
            parent_cid: (Bluesky only) Parent content identifier
            root_uri: (Bluesky only) Root post URI
            root_cid: (Bluesky only) Root post CID"""
        client = _get_client()
        try:
            response = client.comments.reply_to_inbox_post(
                post_id=post_id,
                accountId=account_id,
                message=message,
                commentId=comment_id,
                subreddit=subreddit,
                parentCid=parent_cid,
                rootUri=root_uri,
                rootCid=root_cid,
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
            post_id: Late post ID or platform-specific post ID. LinkedIn third-party posts accept full activity URN or numeric ID. (required)
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
                post_id=post_id, comment_id=comment_id, accountId=account_id
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
                post_id=post_id, comment_id=comment_id, accountId=account_id, cid=cid
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
                accountId=account_id,
                message=message,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # CONNECT

    @mcp.tool()
    def connect_get_connect_url(
        platform: str, profile_id: str, redirect_url: str = ""
    ) -> str:
        """Get OAuth connect URL

        Args:
            platform: Social media platform to connect (required)
            profile_id: Your Late profile ID (get from /v1/profiles) (required)
            redirect_url: Your custom redirect URL after connection completes. Standard mode appends ?connected={platform}&profileId=X&username=Y. Headless mode appends OAuth data params."""
        client = _get_client()
        try:
            response = client.connect.get_connect_url(
                platform=platform, profile_id=profile_id, redirect_url=redirect_url
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
                platform=platform, code=code, state=state, profileId=profile_id
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
                profileId=profile_id,
                pageId=page_id,
                tempToken=temp_token,
                userProfile=user_profile,
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
                profileId=profile_id,
                locationId=location_id,
                tempToken=temp_token,
                userProfile=user_profile,
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
                profileId=profile_id,
                tempToken=temp_token,
                userProfile=user_profile,
                accountType=account_type,
                selectedOrganization=selected_organization,
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
            profile_id: Your Late profile ID (required)
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
            profile_id: Your Late profile ID (required)
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
                profileId=profile_id,
                boardId=board_id,
                boardName=board_name,
                tempToken=temp_token,
                userProfile=user_profile,
                refreshToken=refresh_token,
                expiresIn=expires_in,
                redirect_url=redirect_url,
            )
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def connect_list_snapchat_profiles(profile_id: str, temp_token: str) -> str:
        """List Snapchat profiles

        Args:
            profile_id: Your Late profile ID (required)
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
            profile_id: Your Late profile ID (required)
            selected_public_profile: The selected Snapchat Public Profile (required)
            temp_token: Temporary Snapchat access token from OAuth (required)
            user_profile: User profile data from OAuth redirect (required)
            refresh_token: Snapchat refresh token (if available)
            expires_in: Token expiration time in seconds
            redirect_url: Custom redirect URL after connection completes"""
        client = _get_client()
        try:
            response = client.connect.select_snapchat_profile(
                profileId=profile_id,
                selectedPublicProfile=selected_public_profile,
                tempToken=temp_token,
                userProfile=user_profile,
                refreshToken=refresh_token,
                expiresIn=expires_in,
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
                appPassword=app_password,
                state=state,
                redirectUri=redirect_uri,
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
                chatId=chat_id, profileId=profile_id
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
                account_id=account_id, selectedPageId=selected_page_id
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
                accountType=account_type,
                selectedOrganization=selected_organization,
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
                defaultBoardId=default_board_id,
                defaultBoardName=default_board_name,
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
                account_id=account_id, selectedLocationId=selected_location_id
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
                account_id=account_id, defaultSubreddit=default_subreddit
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
                scope=scope, profileIds=profile_ids
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
    ) -> str:
        """List publishing logs

        Args:
            status: Filter by log status
            platform: Filter by platform
            action: Filter by action type
            days: Number of days to look back (max 7)
            limit: Maximum number of logs to return (max 100)
            skip: Number of logs to skip (for pagination)"""
        client = _get_client()
        try:
            response = client.logs.list_posts_logs(
                status=status,
                platform=platform,
                action=action,
                days=days,
                limit=limit,
                skip=skip,
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
                filename=filename, contentType=content_type, size=size
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
                conversation_id=conversation_id, accountId=account_id, status=status
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
                accountId=account_id,
                message=message,
                quickReplies=quick_replies,
                buttons=buttons,
                template=template,
                replyMarkup=reply_markup,
                messagingType=messaging_type,
                messageTag=message_tag,
                replyTo=reply_to,
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
                accountId=account_id,
                text=text,
                replyMarkup=reply_markup,
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
            include_hidden"""
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
    ) -> str:
        """Update post

        Args:
            post_id: (required)
            content
            scheduled_for
            tiktok_settings: Root-level TikTok settings applied to all TikTok platforms. Merged into each platform's platformSpecificData, with platform-specific settings taking precedence."""
        client = _get_client()
        try:
            response = client.posts.update_post(
                post_id=post_id,
                content=content,
                scheduledFor=scheduled_for,
                tiktokSettings=tiktok_settings,
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
                isDefault=is_default,
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
                profileId=profile_id,
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
                profileId=profile_id,
                queueId=queue_id,
                name=name,
                timezone=timezone,
                slots=slots,
                active=active,
                setAsDefault=set_as_default,
                reshuffleExisting=reshuffle_existing,
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
    def queue_preview_queue(profile_id: str, count: int = 20) -> str:
        """Preview upcoming slots

        Args:
            profile_id: (required)
            count"""
        client = _get_client()
        try:
            response = client.queue.preview_queue(profile_id=profile_id, count=count)
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
                review_id=review_id, accountId=account_id, message=message
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
                review_id=review_id, accountId=account_id
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
                isActive=is_active,
                customHeaders=custom_headers,
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
                _id=id,
                name=name,
                url=url,
                secret=secret,
                events=events,
                isActive=is_active,
                customHeaders=custom_headers,
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
            response = client.webhooks.test_webhook(webhookId=webhook_id)
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
