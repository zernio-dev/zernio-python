/**
 * The screens, the tool that opens each one, and the shapes of their data.
 *
 * Every screen comes from one of the server's tools as structuredContent
 * `{view, data, args}` (src/late/mcp/apps/tools.py). The app switches screens
 * and refreshes by calling those same tools through the host
 * (app.callServerTool), so the user's scopes and the API's validation apply
 * as they do for Claude.
 */
import type { App } from "@modelcontextprotocol/ext-apps";

export type View = "home" | "posts" | "analytics" | "accounts" | "ads" | "inbox" | "conversation" | "comments" | "preview";

export const TOOLS: Record<View, string> = {
  home: "zernio_open_app",
  posts: "show_failed_posts",
  analytics: "show_analytics",
  accounts: "show_account_health",
  ads: "show_ads_alerts",
  inbox: "show_inbox",
  conversation: "show_conversation",
  comments: "show_post_comments",
  preview: "show_post_preview",
};

export const VIEW_TITLES: Record<View, string> = {
  home: "Home",
  posts: "Failed posts",
  analytics: "Analytics",
  accounts: "Accounts",
  ads: "Ads",
  inbox: "Inbox",
  conversation: "Conversation",
  comments: "Comments",
  preview: "Post preview",
};

/** The screens with a tab; the others open from a tool with their own arguments. */
export const TABS: View[] = ["home", "inbox", "posts", "analytics", "accounts", "ads"];

export interface Screen<D = unknown> {
  view: View;
  data: D;
  args: Record<string, unknown>;
}

export type CallResult = Awaited<ReturnType<App["callServerTool"]>>;

export function textOf(result: CallResult): string {
  return result.content.map((block) => (block.type === "text" ? block.text : "")).join("");
}

/** The screen a tool result carries, or undefined when it is not one of ours. */
export function screenOf(result: CallResult): Screen | undefined {
  const sc = result.structuredContent as Partial<Screen> | undefined;
  if (!sc || typeof sc.view !== "string" || !(sc.view in TOOLS)) return undefined;
  return { view: sc.view as View, data: sc.data, args: (sc.args as Record<string, unknown>) ?? {} };
}

/* Data of each screen */

export interface Account {
  accountId: string;
  platform: string;
  profileId?: string;
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

export interface FailedPost {
  id: string;
  title: string;
  content: string;
  platforms: string[];
  errors: { platform: string | null; message: string }[];
  updatedAt: string | null;
}

export interface HomeData {
  health: AccountsHealth;
  failedPosts: FailedPost[];
  failedTotal: number;
}

export interface PostsData {
  posts: FailedPost[];
  total: number;
}

export interface Metrics {
  impressions?: number;
  reach?: number;
  likes?: number;
  comments?: number;
  shares?: number;
  saves?: number;
  clicks?: number;
  views?: number;
}

export interface AnalyticsData {
  dailyData?: { date: string; postCount?: number; metrics?: Metrics }[];
  platformBreakdown?: (Metrics & { platform: string; postCount?: number })[];
  totals?: Metrics & { postCount?: number; engagement?: number };
}

export interface AdsAlert {
  id: string;
  kind?: string;
  severity: "error" | "warning" | "info";
  title: string;
  message?: string;
  platform?: string;
  entity?: { level?: string; id?: string; name?: string | null };
  fix?: { label?: string; url?: string };
}

export interface AdsData {
  alerts?: AdsAlert[];
  counts?: { error?: number; warning?: number; info?: number };
}

export interface Conversation {
  id: string;
  platform: string;
  accountId: string;
  accountUsername?: string | null;
  participantName?: string | null;
  lastMessage?: string | null;
  updatedTime?: string | null;
  unreadCount?: number | null;
  isGroup?: boolean | null;
}

export interface CommentedPost {
  id: string;
  platform: string;
  accountId: string;
  accountUsername?: string | null;
  content?: string | null;
  createdTime?: string | null;
  commentCount?: number | null;
}

export interface InboxData {
  conversations: Conversation[];
  posts: CommentedPost[];
}

export interface Message {
  id: string;
  message?: string | null;
  senderName?: string | null;
  direction?: "incoming" | "outgoing" | string | null;
  createdAt?: string | null;
  isDeleted?: boolean | null;
  attachments: number;
}

export interface ConversationData {
  conversationId: string;
  accountId: string;
  messages: Message[];
}

export interface Comment {
  id: string;
  message?: string | null;
  createdTime?: string | null;
  likeCount?: number | null;
  replyCount?: number | null;
  canReply?: boolean | null;
  isHidden?: boolean | null;
  from: { name?: string | null; username?: string | null; isOwner?: boolean | null };
}

export interface CommentsData {
  postId: string;
  accountId: string;
  post: { text?: string | null; permalink?: string | null; createdAt?: string | null };
  comments: Comment[];
}

export interface PreviewData {
  content: string;
  media: { type?: string; url: string }[];
  targets: { platform: string; accountId?: string; handle?: string; error?: string }[];
  validation?: {
    valid?: boolean;
    errors?: { platform?: string; error: string }[];
    warnings?: { platform?: string; warning: string }[];
  } | null;
  request: Record<string, unknown>;
}

/* Platforms */

const PLATFORMS: Record<string, string> = {
  twitter: "X", x: "X", instagram: "Instagram", facebook: "Facebook", linkedin: "LinkedIn",
  tiktok: "TikTok", youtube: "YouTube", threads: "Threads", pinterest: "Pinterest",
  reddit: "Reddit", bluesky: "Bluesky", googlebusiness: "Google Business",
  telegram: "Telegram", snapchat: "Snapchat", discord: "Discord", slack: "Slack",
  whatsapp: "WhatsApp", meta: "Meta", google: "Google", microsoft: "Microsoft",
  openai: "ChatGPT", linkedinads: "LinkedIn Ads", metaads: "Meta Ads", tiktokads: "TikTok Ads",
  googleads: "Google Ads", pinterestads: "Pinterest Ads", xads: "X Ads", redditads: "Reddit Ads",
};

export function platformName(platform: string | null | undefined): string {
  if (!platform) return "Unknown";
  return PLATFORMS[platform] ?? platform.charAt(0).toUpperCase() + platform.slice(1);
}

/** The platform's full-colour app icon, as the dashboard shows it (zernio.com/platform-logos). */
const ICON_FILES: Record<string, string> = {
  twitter: "x", xads: "x", googlebusiness: "google", google: "googleads", openai: "chatgpt",
  metaads: "meta", linkedinads: "linkedin", tiktokads: "tiktok", pinterestads: "pinterest",
  redditads: "reddit", googleads: "googleads",
};

export function platformIcon(platform: string): string {
  return `https://zernio.com/platform-logos/${ICON_FILES[platform] ?? platform}-icon.png`;
}

/* Formatting */

export function formatNumber(value: number | undefined, locale?: string, compact = false): string {
  if (value === undefined || value === null) return "—";
  return new Intl.NumberFormat(locale, compact ? { notation: "compact", maximumFractionDigits: 1 } : undefined).format(value);
}

export function formatDate(value: string | null | undefined, locale?: string, options?: Intl.DateTimeFormatOptions): string {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString(locale, options ?? { month: "short", day: "numeric" });
}
