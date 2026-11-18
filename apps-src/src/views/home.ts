/**
 * Home: the workspace at a glance. Inline it is a compact card (three stats,
 * up to three accounts that need attention, Open Zernio); full screen it lists
 * every account.
 */
import { AlertTriangle, CircleCheck, CircleX, Maximize2, RefreshCw, SendHorizontal } from "lucide";
import { COPY } from "../copy";
import { h, icon } from "../dom";
import { count, platformName } from "../format";
import type { Account, AppState } from "../model";

export interface HomeEnv {
  state: AppState;
  compact: boolean;
  canExpand: boolean;
  locale?: string;
  /** Must run inside the click: the host refuses a mode change without a gesture. */
  expand(): void;
  refresh(): void;
  reconnect(): void;
  ask(account: Account): void;
}

const RANK = { error: 0, warning: 1, healthy: 2 } as const;

function issueOf(account: Account): string {
  if (account.needsReconnect) return account.disconnectReason || "Needs to be reconnected";
  return account.issues?.[0] || account.disconnectReason || "";
}

function badge(status: Account["status"]): HTMLElement {
  const glyph = status === "healthy" ? CircleCheck : status === "warning" ? AlertTriangle : CircleX;
  return h("span", { class: `badge badge-${status}` }, icon(glyph, "icon icon-sm"), COPY.status[status] ?? status);
}

function accountRow(env: HomeEnv, account: Account): HTMLElement {
  const issue = issueOf(account);
  return h(
    "li",
    { class: "row" },
    h(
      "div",
      { class: "row-main" },
      h(
        "div",
        { class: "row-title" },
        platformName(account.platform),
        h("span", { class: "muted" }, account.username ? `@${account.username}` : account.displayName ?? ""),
      ),
      issue ? h("div", { class: "row-sub" }, issue) : null,
    ),
    badge(account.status),
    account.status !== "healthy"
      ? h(
          "button",
          { class: "btn btn-ghost btn-icon", attrs: { "aria-label": `${COPY.askClaude}: ${account.username ?? account.accountId}`, title: COPY.askClaude }, on: { click: () => env.ask(account) } },
          icon(SendHorizontal),
        )
      : null,
  );
}

export function homeView(env: HomeEnv): HTMLElement {
  const { state } = env;
  const summary = state.health?.summary ?? {};
  const accounts = [...(state.health?.accounts ?? [])].sort((a, b) => RANK[a.status] - RANK[b.status]);
  const attention = accounts.filter((a) => a.status !== "healthy");
  const needAttention = (summary.warning ?? 0) + (summary.error ?? 0);
  const listed = env.compact ? attention.slice(0, 3) : accounts;

  const stat = (label: string, value: string, tone = "") =>
    h("div", { class: `stat ${tone}` }, h("div", { class: "eyebrow" }, label), h("div", { class: "stat-value" }, value));

  return h(
    "div",
    { class: "home" },
    h(
      "div",
      { class: "stats" },
      stat(COPY.stats.accounts, count(summary.total, env.locale)),
      stat(COPY.stats.attention, count(needAttention, env.locale), needAttention ? "stat-warn" : ""),
      stat(COPY.stats.failed, count(state.failedPosts, env.locale), state.failedPosts ? "stat-error" : ""),
    ),
    h(
      "section",
      { class: "section" },
      h("div", { class: "eyebrow" }, env.compact ? COPY.attentionTitle : COPY.accountsTitle),
      listed.length
        ? h("ul", { class: "list" }, listed.map((a) => accountRow(env, a)))
        : h("p", { class: "empty" }, icon(CircleCheck), COPY.allHealthy),
    ),
    h(
      "div",
      { class: "actions" },
      env.canExpand
        ? h("button", { class: "btn btn-primary", on: { click: env.expand } }, icon(Maximize2), COPY.open)
        : null,
      summary.needsReconnect
        ? h("button", { class: "btn", on: { click: env.reconnect } }, COPY.reconnect)
        : null,
      h(
        "button",
        { class: "btn btn-ghost btn-icon", attrs: { "aria-label": COPY.refresh, title: COPY.refresh, disabled: state.phase === "loading" }, on: { click: env.refresh } },
        icon(RefreshCw, state.phase === "loading" ? "icon spin" : "icon"),
      ),
    ),
  );
}
