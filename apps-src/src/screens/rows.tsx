/** The rows several screens share: an account and a failed post. */
import { useState } from "react";
import { type Account, type FailedPost, formatDate, platformName } from "../api";
import { Button, PlatformTile, PlatformTiles, Row, StatusPill, type Tone } from "../ui";
import type { Ctx } from "./context";

/** 48. Green works, amber needs action, red is broken. */
const ACCOUNT_STATE: Record<Account["status"], { label: string; tone: Tone }> = {
  healthy: { label: "Healthy", tone: "success" },
  warning: { label: "Needs attention", tone: "warning" },
  error: { label: "Broken", tone: "danger" },
};

export const ACCOUNT_RANK = { error: 0, warning: 1, healthy: 2 } as const;

function accountReason(account: Account): string {
  if (account.needsReconnect) return account.disconnectReason || "Needs to be reconnected";
  return account.issues?.[0] || account.disconnectReason || "";
}

export function AccountRow({ ctx, account }: { ctx: Ctx; account: Account }) {
  const state = ACCOUNT_STATE[account.status];
  const reason = accountReason(account);
  const handle = account.username ? `@${account.username}` : account.displayName;
  return (
    <Row
      lead={<PlatformTile platform={account.platform} />}
      name={platformName(account.platform)}
      secondary={handle}
      state={<StatusPill label={state.label} tone={state.tone} reason={reason || undefined} />}
      fix={
        account.needsReconnect ? (
          <Button size="sm" onClick={() => void ctx.app.openLink({ url: "https://zernio.com/dashboard" })}>Reconnect</Button>
        ) : account.status !== "healthy" ? (
          <Button
            size="sm"
            onClick={() =>
              ctx.ask(
                `My ${platformName(account.platform)} account ${handle ?? account.accountId} (account_id ${account.accountId}) shows "${reason || state.label}" in Zernio. Help me fix it.`,
              )
            }
          >
            Ask Claude
          </Button>
        ) : null
      }
    />
  );
}

/** A post's name: its title, else its first line, else what it is. */
function postName(post: FailedPost): string {
  const first = post.content.split("\n").find((line) => line.trim());
  return post.title || first || "Post without text";
}

export function FailedPostRow({ ctx, post }: { ctx: Ctx; post: FailedPost }) {
  const [state, setState] = useState<"idle" | "busy" | "queued" | string>("idle");
  const reason = post.errors.length
    ? post.errors.map((e) => (post.platforms.length > 1 ? `${platformName(e.platform)}: ${e.message}` : e.message)).join("\n")
    : "No error message recorded";

  const retry = async () => {
    setState("busy");
    const result = await ctx.act("posts_retry", { post_id: post.id });
    // posts_retry answers in text: ✅ when queued, ⚠️ or ❌ when not.
    const ok = result.ok && result.text.trim().startsWith("✅");
    setState(ok ? "queued" : result.text || "Retry failed");
    if (ok) ctx.tell(`From the Zernio app the user queued post ${post.id} for retry.`);
  };

  return (
    <Row
      lead={<PlatformTiles platforms={post.platforms} />}
      name={postName(post)}
      secondary={formatDate(post.updatedAt, ctx.app.getHostContext()?.locale)}
      state={
        state === "queued" ? (
          <StatusPill label="Queued" tone="info" />
        ) : state !== "idle" && state !== "busy" ? (
          <StatusPill label="Retry failed" tone="danger" reason={state} />
        ) : (
          <StatusPill label="Failed" tone="danger" reason={reason} />
        )
      }
      fix={
        state === "queued" ? null : (
          <Button size="sm" disabled={state === "busy"} onClick={() => void retry()}>
            {state === "busy" ? "Retrying…" : "Retry"}
          </Button>
        )
      }
    />
  );
}
