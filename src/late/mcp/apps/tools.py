"""Display tools: one per view, always listed, each fetching its own data.

The data tools stay text-only behind search_tools. A view binds to the tool
the host called, so a view on a tool reached through call_tool never renders;
these show_* tools are the listed entry points instead (monday.com's
show-table / show-board pattern). Each returns a text summary for the model
and clients without MCP Apps, and structured_content for its view.

The ui_* tools are app-only: the views' buttons call them, the model never
sees them.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from fastmcp.apps import AppConfig
from fastmcp.exceptions import ToolError
from fastmcp.tools import ToolResult
from mcp.types import ToolAnnotations

from late.client.exceptions import LateError

if TYPE_CHECKING:
    from fastmcp import FastMCP

_DISPLAY = (
    "UI display tool: renders an interactive view in clients that support MCP Apps, "
    "with a text summary for those that do not."
)

_READ = ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False)


def _server() -> Any:
    # Imported at call time: server.py registers these tools while it is
    # still loading.
    from late.mcp import server

    return server


def _api(call: Any) -> Any:
    try:
        return call()
    except LateError as e:
        raise ToolError(f"Error: {e}") from e


def register_tools(mcp: FastMCP, view_uri: Any) -> None:
    def show(name: str, view: str, title: str, description: str) -> Any:
        return mcp.tool(
            name=name,
            description=f"{description}\n\n{_DISPLAY}",
            annotations=_READ.model_copy(update={"title": title}),
            app=AppConfig(resource_uri=view_uri(view)),
        )

    def app_only(name: str, title: str, description: str) -> Any:
        return mcp.tool(
            name=name,
            description=description,
            annotations=ToolAnnotations(
                title=title, readOnlyHint=False, destructiveHint=True, openWorldHint=True
            ),
            app=AppConfig(visibility=["app"]),
        )

    @show(
        "show_post_preview",
        "post-preview",
        "Preview a post",
        "Show the user how a post will go out on each platform before anything is "
        "published: the account each platform resolves to, the text, the media, and "
        "validation errors and warnings. Use it when the user wants to see or review a "
        "post first. Nothing is published; the view's Publish now and Save as draft "
        "buttons call posts_cross_post with these same arguments. For a scheduled post, "
        "confirm in chat and call posts_create or posts_cross_post.\n\n"
        "Args:\n"
        "    content: The post text (required)\n"
        "    platforms: Comma-separated platforms, e.g. 'twitter,linkedin' (required). "
        "Repeat a platform to target several of its accounts.\n"
        "    account_ids: Comma-separated account IDs parallel to platforms. Empty "
        "positions resolve automatically.\n"
        "    profile_id: Scope automatic resolution to one profile.\n"
        "    media_urls: Comma-separated media URLs to attach.",
    )
    def show_post_preview(
        content: str,
        platforms: str,
        account_ids: str = "",
        profile_id: str = "",
        media_urls: str = "",
    ) -> ToolResult:
        server = _server()
        client = server._get_client()

        target_platforms = [p.strip().lower() for p in platforms.split(",") if p.strip()]
        if not target_platforms:
            raise ToolError("No platforms specified.")
        ids = [i.strip() for i in account_ids.split(",")] if account_ids else []
        ids += [""] * max(0, len(target_platforms) - len(ids))

        # Resolved the way posts_cross_post resolves them, so the preview names
        # the accounts a publish would reach and shows the same ambiguity errors.
        targets: list[dict[str, str]] = []
        for plat, acc_id in zip(target_platforms, ids[: len(target_platforms)], strict=True):
            try:
                acc = server._resolve_account(client, plat, acc_id, profile_id)
            except ValueError as e:
                targets.append({"platform": plat, "error": str(e)})
                continue
            targets.append(
                {
                    "platform": server._platform_str(acc.platform),
                    "accountId": acc.field_id,
                    "handle": acc.username or acc.displayName or "",
                }
            )

        media = server._media_items(media_urls)
        resolved = [
            {"platform": t["platform"], "accountId": t["accountId"]}
            for t in targets
            if "accountId" in t
        ]
        validation: dict[str, Any] | None = None
        if resolved:
            try:
                validation = client.validate.validate_post(
                    resolved, content=content, media_items=media or None
                )
            except LateError as e:
                validation = {"warnings": [{"warning": f"Validation unavailable: {e}"}]}

        lines = [
            "Preview only, nothing was published.",
            "Targets: "
            + ", ".join(
                f"{t['platform']} (@{t['handle']})" if t.get("handle") else t["platform"]
                for t in targets
            ),
            f"Length: {len(content)} characters"
            + (f", {len(media)} media file(s)" if media else ""),
        ]
        lines += [f"Account ({t['platform']}): {t['error']}" for t in targets if "error" in t]
        for issue in (validation or {}).get("errors") or []:
            lines.append(f"Error ({issue.get('platform') or 'all'}): {issue.get('error')}")
        for issue in (validation or {}).get("warnings") or []:
            lines.append(f"Warning ({issue.get('platform') or 'all'}): {issue.get('warning')}")
        if len(resolved) == len(targets):
            lines.append(
                "To publish it as previewed, call posts_cross_post with platforms="
                f"'{','.join(t['platform'] for t in targets)}' and account_ids="
                f"'{','.join(t['accountId'] for t in targets)}'."
            )

        return ToolResult(
            content="\n".join(lines),
            structured_content={
                "kind": "preview",
                "post": {
                    "content": content,
                    "media": [
                        {"type": getattr(m["type"], "value", m["type"]), "url": m["url"]}
                        for m in media
                    ],
                    "targets": targets,
                },
                "validation": validation,
                # What the view's buttons send to posts_cross_post, with the
                # accounts already resolved.
                "request": {
                    "content": content,
                    "platforms": ",".join(t["platform"] for t in targets),
                    "account_ids": ",".join(t.get("accountId", "") for t in targets),
                    "profile_id": profile_id,
                    "media_urls": media_urls,
                },
            },
        )

    @show(
        "show_failed_posts",
        "failed-posts",
        "Show failed posts",
        "Show the posts that failed to publish, each platform's error, and a Retry button "
        "per post. Use it when the user wants to see what failed or fix it.\n\n"
        "Args:\n"
        "    limit: Maximum number of posts to show. Default: 10.",
    )
    def show_failed_posts(limit: int = 10) -> ToolResult:
        server = _server()
        client = server._get_client()
        posts = _api(lambda: client.posts.list(status="failed", limit=limit)).posts or []

        view = [
            {
                "id": post.field_id,
                "content": (post.content or "")[:280],
                "platforms": [t.platform for t in post.platforms or [] if t.platform],
                "errors": [
                    {"platform": platform, "message": message}
                    for platform, message in server._failed_targets(post)
                ],
            }
            for post in posts
        ]
        lines = [f"{len(view)} failed post(s)."] + [
            f"- {p['id']} ({', '.join(p['platforms'])}): "
            + ("; ".join(f"{e['platform']}: {e['message']}" for e in p["errors"]) or "Unknown error")
            for p in view
        ]
        return ToolResult(content="\n".join(lines), structured_content={"posts": view})

    @show(
        "show_analytics",
        "analytics",
        "Show analytics",
        "Show daily post analytics as a chart: totals for impressions, engagement, views and "
        "posts, a per-day chart of each, and a fullscreen per-platform breakdown. Use it when "
        "the user wants to see how their posts perform. Defaults to the last 180 days.\n\n"
        "Args:\n"
        "    platform: Only this platform, e.g. 'instagram'.\n"
        "    profile_id: Only this profile.\n"
        "    account_id: Only this account.\n"
        "    from_date: Inclusive start date (ISO 8601).\n"
        "    to_date: Inclusive end date (ISO 8601).",
    )
    def show_analytics(
        platform: str = "",
        profile_id: str = "",
        account_id: str = "",
        from_date: str = "",
        to_date: str = "",
    ) -> ToolResult:
        client = _server()._get_client()
        data = _api(
            lambda: client.analytics.get_daily_metrics(
                platform=platform or None,
                profile_id=profile_id or None,
                account_id=account_id or None,
                from_date=from_date or None,
                to_date=to_date or None,
            )
        )
        totals = data.get("totals") or {}
        days = data.get("dailyData") or []
        text = (
            f"{len(days)} day(s) with posts. Totals: {totals.get('postCount', 0)} posts, "
            f"{totals.get('impressions', 0)} impressions, {totals.get('engagement', 0)} "
            f"engagements, {totals.get('views', 0)} views."
        )
        return ToolResult(content=text, structured_content=data)

    @show(
        "show_account_health",
        "account-health",
        "Show account health",
        "Show connected social accounts by health status, the ones that need attention and "
        "why, with a link to reconnect. Use it when the user asks whether their accounts "
        "work or why posting fails for one.\n\n"
        "Args:\n"
        "    profile_id: Only this profile.\n"
        "    platform: Only this platform.",
    )
    def show_account_health(profile_id: str = "", platform: str = "") -> ToolResult:
        client = _server()._get_client()
        data = _api(
            lambda: client.accounts.get_all_accounts_health(
                profile_id=profile_id or None, platform=platform or None
            )
        )
        summary = data.get("summary") or {}
        unhealthy = [a for a in data.get("accounts") or [] if a.get("status") != "healthy"]
        lines = [
            f"{summary.get('total', 0)} account(s): {summary.get('healthy', 0)} healthy, "
            f"{summary.get('warning', 0)} warning, {summary.get('error', 0)} error, "
            f"{summary.get('needsReconnect', 0)} need reconnecting."
        ] + [
            f"- {a.get('platform')} @{a.get('username') or a.get('accountId')}: {a.get('status')}"
            + (f" ({(a.get('issues') or [a.get('disconnectReason')])[0]})" if a.get("issues") or a.get("disconnectReason") else "")
            for a in unhealthy[:25]
        ]
        return ToolResult(content="\n".join(lines), structured_content=data)

    @show(
        "show_ads_alerts",
        "ads-alerts",
        "Show ads that need attention",
        "Show what needs attention across the user's ads, most severe first: rejected ads, "
        "delivery issues, payment problems, campaigns spending without results, capped "
        "budgets, lost connections and failing syncs. Each has a link to fix it and can be "
        "dismissed for 30 days. Use it when the user asks how their ads are doing or what "
        "is wrong with them.\n\n"
        "Args:\n"
        "    account_id: Only alerts of this ads connection.\n"
        "    profile_id: Only alerts of the ads connections on this profile.",
    )
    def show_ads_alerts(account_id: str = "", profile_id: str = "") -> ToolResult:
        client = _server()._get_client()
        data = _api(
            lambda: client.ad_campaigns.list_ads_alerts(
                account_id=account_id or None, profile_id=profile_id or None
            )
        )
        alerts = data.get("alerts") or []
        lines = [f"{len(alerts)} ads alert(s)."] + [
            f"- [{a.get('severity')}] {a.get('title')}: {a.get('message')} (id: {a.get('id')})"
            for a in alerts[:25]
        ]
        return ToolResult(content="\n".join(lines), structured_content=data)

    @show(
        "show_automation_approvals",
        "automation-approvals",
        "Show automation approvals",
        "Show the changes an ads automation is waiting for a person to approve (pauses, "
        "budget, bid and target changes), with Approve and Reject buttons. Use it when the "
        "user wants to review or decide pending automation approvals. Find automation IDs "
        "with search_tools ('list automations').\n\n"
        "Args:\n"
        "    automation_id: The automation (required)\n"
        "    status: Only requests in this status. Default: pending.",
    )
    def show_automation_approvals(
        automation_id: str,
        status: Literal["pending", "approved", "rejected", "expired", "cancelled"] = "pending",
    ) -> ToolResult:
        client = _server()._get_client()
        data = _api(
            lambda: client.automations.list_automation_approvals(
                automation_id=automation_id, status=status
            )
        )
        approvals = data.get("approvals") or []
        lines = [f"{len(approvals)} {status} approval request(s)."] + [
            f"- {a.get('id')}: {len(a.get('changes') or [])} change(s), expires {a.get('expiresAt')}"
            + ("" if a.get("canDecide") else " (you cannot decide it)")
            for a in approvals
        ]
        return ToolResult(
            content="\n".join(lines),
            structured_content={**data, "automationId": automation_id},
        )

    @app_only(
        "ui_dismiss_ads_alert",
        "Dismiss an ads alert",
        "Hide an ads alert for 30 days. Called by the ads alerts view.",
    )
    def ui_dismiss_ads_alert(alert_id: str) -> dict[str, Any]:
        client = _server()._get_client()
        return _api(lambda: client.ad_campaigns.dismiss_ads_alert(alert_id))

    @app_only(
        "ui_decide_automation_approval",
        "Approve or reject an automation request",
        "Approve or reject a pending automation approval request. Called by the automation "
        "approvals view.",
    )
    def ui_decide_automation_approval(
        automation_id: str, approval_id: str, decision: Literal["approve", "reject"]
    ) -> dict[str, Any]:
        client = _server()._get_client()
        decide = (
            client.automations.approve_automation_approval
            if decision == "approve"
            else client.automations.reject_automation_approval
        )
        return _api(lambda: decide(automation_id, approval_id))
