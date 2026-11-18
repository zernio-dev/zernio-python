/**
 * The app's data, read through the server's ordinary tools (callServerTool),
 * so the API's validation and the user's scopes apply as they do for Claude.
 * Generated tools return compact JSON as their text.
 */
import type { App } from "@modelcontextprotocol/ext-apps";
import type { AccountsHealth } from "./model";

export type CallToolResult = Awaited<ReturnType<App["callServerTool"]>>;
export type CallTool = (name: string, args: Record<string, unknown>) => Promise<CallToolResult>;

export class ToolError extends Error {}

function json<T>(result: CallToolResult): T {
  const text = result.content
    .filter((block) => block.type === "text")
    .map((block) => (block as { text: string }).text)
    .join("");
  if (result.isError) throw new ToolError(text || "The tool call failed.");
  return JSON.parse(text) as T;
}

export class ZernioClient {
  constructor(private call: CallTool) {}

  async health(): Promise<AccountsHealth> {
    return json<AccountsHealth>(await this.call("accounts_get_all_accounts_health", {}));
  }

  /**
   * How many posts failed. posts_list_posts is not listed up front (it sits
   * behind search_tools), so this also tests whether the host lets an app
   * call a tool it never received in tools/list.
   */
  async failedPosts(): Promise<number> {
    const page = json<{ posts?: unknown[]; pagination?: { total?: number } }>(
      await this.call("posts_list_posts", { status: "failed", limit: 1 }),
    );
    return page.pagination?.total ?? page.posts?.length ?? 0;
  }
}
