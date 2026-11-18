/**
 * The app reads its data through the server's ordinary tools
 * (app.callServerTool), so the user's scopes and the API's validation apply
 * as they do for Claude. Generated tools return compact JSON as their text.
 */
import type { App } from "@modelcontextprotocol/ext-apps";

export interface Account {
  accountId: string;
  platform: string;
  username?: string;
  displayName?: string;
  status: "healthy" | "warning" | "error";
  needsReconnect?: boolean;
  issues?: string[];
  disconnectReason?: string | null;
}

export interface AccountsHealth {
  summary?: { total?: number; healthy?: number; warning?: number; error?: number; needsReconnect?: number };
  accounts?: Account[];
}

async function callJson<T>(app: App, name: string, args: Record<string, unknown> = {}): Promise<T> {
  const result = await app.callServerTool({ name, arguments: args });
  const text = result.content
    .map((block) => (block.type === "text" ? block.text : ""))
    .join("");
  if (result.isError) throw new Error(text || `${name} failed`);
  return JSON.parse(text) as T;
}

export function getAccountsHealth(app: App): Promise<AccountsHealth> {
  return callJson<AccountsHealth>(app, "accounts_get_all_accounts_health");
}

/**
 * How many posts failed. posts_list_posts is not listed up front (it sits
 * behind search_tools), so this also shows whether the host lets an app call
 * a tool it never received in tools/list.
 */
export async function getFailedPostCount(app: App): Promise<number> {
  const page = await callJson<{ posts?: unknown[]; pagination?: { total?: number } }>(
    app,
    "posts_list_posts",
    { status: "failed", limit: 1 },
  );
  return page.pagination?.total ?? page.posts?.length ?? 0;
}

const PLATFORMS: Record<string, string> = {
  twitter: "X", instagram: "Instagram", facebook: "Facebook", linkedin: "LinkedIn",
  tiktok: "TikTok", youtube: "YouTube", threads: "Threads", pinterest: "Pinterest",
  reddit: "Reddit", bluesky: "Bluesky", googlebusiness: "Google Business",
  telegram: "Telegram", snapchat: "Snapchat", discord: "Discord", slack: "Slack",
  whatsapp: "WhatsApp",
};

export function platformName(platform: string): string {
  return PLATFORMS[platform] ?? platform;
}
