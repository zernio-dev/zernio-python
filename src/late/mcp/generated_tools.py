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
        """List account groups for the authenticated user"""
        client = _get_client()
        try:
            response = client.account_groups.list_account_groups()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def account_groups_create_account_group(name: str, account_ids: str) -> str:
        """Create a new account group

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
        """Update an account group

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
        """Delete an account group

        Args:
            group_id: (required)"""
        client = _get_client()
        try:
            response = client.account_groups.delete_account_group(group_id=group_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # ACCOUNTS

    @mcp.tool()
    def accounts_list_accounts(
        profile_id: str = "", include_over_limit: bool = False
    ) -> str:
        """List connected social accounts

            Args:
                profile_id: Filter accounts by profile ID
                include_over_limit: When true, includes accounts from profiles that exceed the user's plan limit.
        Useful for disconnecting accounts from over-limit profiles so they can be deleted."""
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
        """Get follower stats and growth metrics

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
        """Update a social account

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
        """Disconnect a social account

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
        """Check health of all connected accounts

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
        """Check health of a specific account

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
        """Get Google Business Profile reviews

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
    def accounts_get_linked_in_mentions(
        account_id: str, url: str, display_name: str = ""
    ) -> str:
        """Resolve a LinkedIn profile or company URL to a URN for @mentions

            Args:
                account_id: The LinkedIn account ID (required)
                url: LinkedIn profile URL, company URL, or vanity name.
        - Person: `miquelpalet`, `linkedin.com/in/miquelpalet`
        - Organization: `company/microsoft`, `linkedin.com/company/microsoft`
         (required)
                display_name: The exact display name as shown on LinkedIn.
        - **Person mentions:** Required for clickable mentions. If not provided, a name is derived from the vanity URL which may not match exactly.
        - **Organization mentions:** Optional. If not provided, the company name is automatically retrieved from LinkedIn."""
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
        from_date: str = "",
        to_date: str = "",
        limit: int = 50,
        page: int = 1,
        sort_by: str = "date",
        order: str = "desc",
    ) -> str:
        """Unified analytics for posts

            Args:
                post_id: Returns analytics for a single post. Accepts both Late Post IDs (from `POST /v1/posts`)
        and External Post IDs (from this endpoint's list response). The API automatically
        resolves Late Post IDs to their corresponding External Post analytics.
                platform: Filter by platform (default "all")
                profile_id: Filter by profile ID (default "all")
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
        """YouTube daily views breakdown

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
        """Get aggregate analytics for a LinkedIn personal account

            Args:
                account_id: The ID of the LinkedIn personal account (required)
                aggregation: Type of aggregation for the analytics data.
        - `TOTAL` (default): Returns single totals for each metric
        - `DAILY`: Returns daily breakdown of metrics

        Note: `MEMBERS_REACHED` metric is not available with `DAILY` aggregation.
                start_date: Start date for analytics data in YYYY-MM-DD format.
        If provided without endDate, endDate defaults to today.
        If omitted entirely, returns lifetime analytics.
                end_date: End date for analytics data in YYYY-MM-DD format (exclusive).
        If provided without startDate, startDate defaults to 30 days before endDate.
                metrics: Comma-separated list of metrics to fetch. If omitted, fetches all available metrics.
        Valid values: IMPRESSION, MEMBERS_REACHED, REACTION, COMMENT, RESHARE"""
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
        """Get analytics for a specific LinkedIn post by URN

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
        """List API keys for the current user"""
        client = _get_client()
        try:
            response = client.api_keys.list_api_keys()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def api_keys_create_api_key(name: str, expires_in: int = 0) -> str:
        """Create a new API key

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
        """Delete an API key

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
        """List posts with comments across all accounts

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
        """Get comments for a post

        Args:
            post_id: (required)
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
        """Reply to a post or comment

        Args:
            post_id: (required)
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
        """Delete a comment

        Args:
            post_id: (required)
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
        """Hide a comment

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
        """Unhide a comment

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
        """Like a comment

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
        """Unlike a comment

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
        """Send private reply to comment author

        Args:
            post_id: The Instagram media/post ID (required)
            comment_id: The comment ID to send a private reply to (required)
            account_id: The Instagram social account ID (required)
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
        """Start OAuth connection for a platform

            Args:
                platform: Social media platform to connect (required)
                profile_id: Your Late profile ID (get from /v1/profiles) (required)
                redirect_url: Optional: Your custom redirect URL after connection completes.

        **Standard Mode:** Omit `headless=true` to use our hosted page selection UI.
        After the user selects a Facebook Page, Late redirects here with:
        `?connected=facebook&profileId=X&username=Y`

        **Headless Mode (Facebook, LinkedIn, Pinterest, Google Business Profile & Snapchat):**
        Pass `headless=true` as a query parameter on this endpoint (not inside `redirect_url`), e.g.:
        `GET /v1/connect/facebook?profileId=PROFILE_ID&redirect_url=https://yourapp.com/callback&headless=true`
        `GET /v1/connect/linkedin?profileId=PROFILE_ID&redirect_url=https://yourapp.com/callback&headless=true`
        `GET /v1/connect/pinterest?profileId=PROFILE_ID&redirect_url=https://yourapp.com/callback&headless=true`
        `GET /v1/connect/googlebusiness?profileId=PROFILE_ID&redirect_url=https://yourapp.com/callback&headless=true`
        `GET /v1/connect/snapchat?profileId=PROFILE_ID&redirect_url=https://yourapp.com/callback&headless=true`

        After OAuth, the user is redirected directly to your `redirect_url` with OAuth data:
        - **Facebook:** `?profileId=X&tempToken=Y&userProfile=Z&connect_token=CT&platform=facebook&step=select_page`
        - **LinkedIn:** `?profileId=X&pendingDataToken=TOKEN&connect_token=CT&platform=linkedin&step=select_organization`
          Use `GET /v1/connect/pending-data?token=TOKEN` to fetch tempToken, userProfile, organizations, refreshToken.
        - **Pinterest:** `?profileId=X&tempToken=Y&userProfile=Z&connect_token=CT&platform=pinterest&step=select_board`
        - **Google Business:** `?profileId=X&tempToken=Y&userProfile=Z&connect_token=CT&platform=googlebusiness&step=select_location`
        - **Snapchat:** `?profileId=X&tempToken=Y&userProfile=Z&publicProfiles=PROFILES&connect_token=CT&platform=snapchat&step=select_public_profile`
          (publicProfiles contains `id`, `display_name`, `username`, `profile_image_url`, `subscriber_count`)

        Then use the respective endpoints to build your custom UI:
        - Facebook: `/v1/connect/facebook/select-page` (GET to fetch, POST to save)
        - LinkedIn: `/v1/connect/linkedin/organizations` (GET to fetch logos), `/v1/connect/linkedin/select-organization` (POST to save)
        - Pinterest: `/v1/connect/pinterest/select-board` (GET to fetch, POST to save)
        - Google Business: `/v1/connect/googlebusiness/locations` (GET) and `/v1/connect/googlebusiness/select-location` (POST)
        - Snapchat: `/v1/connect/snapchat/select-profile` (POST to save selected public profile)

        Example: `https://yourdomain.com/integrations/callback`"""
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
        """Complete OAuth token exchange manually (for server-side flows)

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
        """List Facebook Pages after OAuth (Headless Mode)

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
        """Select a Facebook Page to complete the connection (Headless Mode)

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
        """List Google Business Locations after OAuth (Headless Mode)

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
        """Select a Google Business location to complete the connection (Headless Mode)

            Args:
                profile_id: Profile ID from your connection flow (required)
                location_id: The Google Business location ID selected by the user (required)
                temp_token: Temporary Google access token from OAuth (required)
                user_profile: Decoded user profile object from the OAuth callback. **Important:** This contains
        the refresh token needed for token refresh. Always include this field.
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
        """Fetch pending OAuth selection data (Headless Mode)

        Args:
            token: The pending data token from the OAuth redirect URL (`pendingDataToken` parameter) (required)"""
        client = _get_client()
        try:
            response = client.connect.get_pending_o_auth_data(token=token)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def connect_list_linked_in_organizations(temp_token: str, org_ids: str) -> str:
        """Fetch full LinkedIn organization details (Headless Mode)

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
        """Select LinkedIn organization or personal account after OAuth

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
        """List Pinterest Boards after OAuth (Headless Mode)

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
        """Select a Pinterest Board to complete the connection (Headless Mode)

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
        """List Snapchat Public Profiles after OAuth (Headless Mode)

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
        """Select a Snapchat Public Profile to complete the connection (Headless Mode)

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
        """Connect Bluesky using app password

            Args:
                identifier: Your Bluesky handle (e.g. user.bsky.social) or email address (required)
                app_password: App password generated from Bluesky Settings > App Passwords (required)
                state: Required state parameter formatted as `{userId}-{profileId}`.
        - `userId`: Your Late user ID (get from `GET /v1/users` → `currentUserId`)
        - `profileId`: The profile ID to connect the account to (get from `GET /v1/profiles`)
         (required)
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
        """Generate Telegram access code

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
        """Direct Telegram connection (power users)

            Args:
                chat_id: The Telegram chat ID. Can be:
        - Numeric ID (e.g., "-1001234567890")
        - Username with @ prefix (e.g., "@mychannel")
         (required)
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
        """Check Telegram connection status

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
        """List available Facebook pages for a connected account

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
        """Update selected Facebook page for a connected account

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
        """Get available LinkedIn organizations for a connected account

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
        """Switch LinkedIn account type (personal/organization)

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
        """List Pinterest boards for a connected account

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
        """Set default Pinterest board on the connection

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
        """List available Google Business Profile locations for a connected account

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
        """Update selected Google Business Profile location for a connected account

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
        """List Reddit subreddits for a connected account

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
        """Set default subreddit on the connection

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

    # INVITES

    @mcp.tool()
    def invites_create_invite_token(scope: str, profile_ids: str = "") -> str:
        """Create a team member invite token

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
    def logs_list_logs(
        status: str = "",
        platform: str = "",
        action: str = "",
        days: int = 7,
        limit: int = 50,
        skip: int = 0,
    ) -> str:
        """Get publishing logs

        Args:
            status: Filter by log status
            platform: Filter by platform
            action: Filter by action type
            days: Number of days to look back (max 7)
            limit: Maximum number of logs to return (max 100)
            skip: Number of logs to skip (for pagination)"""
        client = _get_client()
        try:
            response = client.logs.list_logs(
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
    def logs_get_log(log_id: str) -> str:
        """Get a single log entry

        Args:
            log_id: The log entry ID (required)"""
        client = _get_client()
        try:
            response = client.logs.get_log(log_id=log_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def logs_get_post_logs(post_id: str, limit: int = 50) -> str:
        """Get logs for a specific post

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
        """Get a presigned URL for direct file upload (up to 5GB)

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
        """List conversations across all accounts

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
        """Get conversation details

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
        """Get messages in a conversation

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
        conversation_id: str, account_id: str, message: str
    ) -> str:
        """Send a message

        Args:
            conversation_id: The conversation ID (id field from list conversations endpoint). This is the platform-specific conversation identifier, not an internal database ID. (required)
            account_id: Social account ID (required)
            message: Message text (required)"""
        client = _get_client()
        try:
            response = client.messages.send_inbox_message(
                conversation_id=conversation_id, accountId=account_id, message=message
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
        """List posts visible to the authenticated user

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
        """Get a single post

        Args:
            post_id: (required)"""
        client = _get_client()
        try:
            response = client.posts.get_post(post_id=post_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def posts_update_post(post_id: str) -> str:
        """Update a post

        Args:
            post_id: (required)"""
        client = _get_client()
        try:
            response = client.posts.update_post(post_id=post_id)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def posts_delete_post(post_id: str) -> str:
        """Delete a post

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
        """Validate and schedule multiple posts from CSV

        Args:
            dry_run"""
        client = _get_client()
        try:
            response = client.posts.bulk_upload_posts(dry_run=dry_run)
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # PROFILES

    @mcp.tool()
    def profiles_list_profiles(include_over_limit: bool = False) -> str:
        """List profiles visible to the authenticated user

            Args:
                include_over_limit: When true, includes profiles that exceed the user's plan limit.
        Over-limit profiles will have `isOverLimit: true` in the response.
        Useful for managing/deleting profiles after a plan downgrade."""
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
        """Create a new profile

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
        """Get a profile by id

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
        """Update a profile

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
        """Delete a profile (must have no connected accounts)

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
        """Get queue schedules for a profile

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
        """Create a new queue for a profile

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
        """Create or update a queue schedule

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
        """Delete a queue schedule

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
        """Preview upcoming queue slots for a profile

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
        """Preview the next available queue slot (informational only)

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
        """Search Reddit posts via a connected account

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
        """Fetch subreddit feed via a connected account

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
        """List reviews across all accounts

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
        """Reply to a review

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
        """Delete a review reply

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
        """Download YouTube video or audio

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
        """Get YouTube video transcript

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
        """Download Instagram reel or post

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
        """Check Instagram hashtags for bans

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
        """Download Twitter/X video

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
        """Download Bluesky video

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
        """Get plan and usage stats for current account"""
        client = _get_client()
        try:
            response = client.usage.get_usage_stats()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    # USERS

    @mcp.tool()
    def users_list_users() -> str:
        """List team users (root + invited)"""
        client = _get_client()
        try:
            response = client.users.list_users()
            return _format_response(response)
        except Exception as e:
            return f"Error: {e}"

    @mcp.tool()
    def users_get_user(user_id: str) -> str:
        """Get user by id (self or invited)

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
        """List all webhooks"""
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
        """Create a new webhook

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
        """Update a webhook

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
        """Delete a webhook

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
        """Get webhook delivery logs

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
