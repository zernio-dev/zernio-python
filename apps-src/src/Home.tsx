/**
 * Home: the workspace at a glance. Inline it is a compact card (three
 * numbers, up to three accounts that need attention, Open Zernio); full
 * screen it lists every account.
 */
import type { App } from "@modelcontextprotocol/ext-apps";
import { CircleAlert, CircleCheck, Maximize2, RefreshCw, SendHorizontal } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { type Account, type AccountsHealth, getAccountsHealth, getFailedPostCount, platformName } from "./api";

interface Props {
  app: App;
  fullscreen: boolean;
  canExpand: boolean;
  locale?: string;
}

const RANK = { error: 0, warning: 1, healthy: 2 } as const;

export function Home({ app, fullscreen, canExpand, locale }: Props) {
  const [health, setHealth] = useState<AccountsHealth>();
  const [failed, setFailed] = useState<number>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>();
  const [notice, setNotice] = useState<string>();

  const load = useCallback(async () => {
    setLoading(true);
    const [h, f] = await Promise.allSettled([getAccountsHealth(app), getFailedPostCount(app)]);
    if (h.status === "fulfilled") setHealth(h.value);
    setError(h.status === "rejected" ? String(h.reason) : undefined);
    setFailed(f.status === "fulfilled" ? f.value : undefined);
    if (f.status === "rejected") console.warn("[zernio] failed posts unavailable:", f.reason);
    setLoading(false);
  }, [app]);

  useEffect(() => {
    void load();
  }, [load]);

  const accounts = [...(health?.accounts ?? [])].sort((a, b) => RANK[a.status] - RANK[b.status]);
  const attention = accounts.filter((a) => a.status !== "healthy");
  const summary = health?.summary ?? {};

  // Tell Claude what the panel shows, so "these accounts" resolves to them.
  useEffect(() => {
    if (!health || !app.getHostCapabilities()?.updateModelContext) return;
    const names = attention.map((a) => `${a.platform} @${a.username ?? a.accountId}`).join(", ");
    void app.updateModelContext({
      content: [{
        type: "text",
        text: `The Zernio panel shows ${summary.total ?? 0} accounts, ${attention.length} needing attention${names ? ` (${names})` : ""}${failed !== undefined ? `, and ${failed} failed posts` : ""}.`,
      }],
    });
  }, [app, health, failed]);

  const ask = async (account: Account) => {
    const issue = account.issues?.[0] || account.disconnectReason || account.status;
    const { isError } = await app.sendMessage({
      role: "user",
      content: [{ type: "text", text: `My ${platformName(account.platform)} account @${account.username ?? account.accountId} (account_id ${account.accountId}) shows "${issue}" in Zernio. Help me fix it.` }],
    });
    setNotice(isError ? "Could not send it to Claude." : "Sent to Claude. Continue in the chat.");
  };

  const fmt = (n?: number) => (n === undefined ? "—" : new Intl.NumberFormat(locale).format(n));
  const listed = fullscreen ? accounts : attention.slice(0, 3);
  const needAttention = (summary.warning ?? 0) + (summary.error ?? 0);

  return (
    <>
      {loading && health && <div className="progress" role="progressbar" aria-label="Refreshing" />}
      {error && <p className="notice notice-error" role="alert">Could not load your workspace. {error}</p>}
      {notice && <p className="notice" role="status">{notice}</p>}

      <div className="stats">
        <Stat label="Accounts" value={fmt(summary.total)} />
        <Stat label="Need attention" value={fmt(needAttention)} tone={needAttention ? "warning" : undefined} />
        <Stat label="Failed posts" value={fmt(failed)} tone={failed ? "error" : undefined} />
      </div>

      <section className="section">
        <h2 className="eyebrow">{fullscreen ? "All accounts" : "Need attention"}</h2>
        {listed.length ? (
          <ul className="list">
            {listed.map((a) => (
              <AccountRow key={a.accountId} account={a} onAsk={() => void ask(a)} />
            ))}
          </ul>
        ) : (
          <p className="empty"><CircleCheck size={16} aria-hidden /> Every account can post.</p>
        )}
      </section>

      <div className="actions">
        {canExpand && (
          // requestDisplayMode must run inside the click: the host refuses it otherwise.
          <button className="btn btn-primary" onClick={() => void app.requestDisplayMode({ mode: "fullscreen" })}>
            <Maximize2 size={16} aria-hidden /> Open Zernio
          </button>
        )}
        {!!summary.needsReconnect && (
          <button className="btn" onClick={() => void app.openLink({ url: "https://zernio.com/dashboard" })}>
            Reconnect in Zernio
          </button>
        )}
        <button className="btn btn-ghost btn-icon" onClick={() => void load()} disabled={loading} aria-label="Refresh" title="Refresh">
          <RefreshCw size={16} className={loading ? "spin" : undefined} aria-hidden />
        </button>
      </div>
    </>
  );
}

function Stat({ label, value, tone }: { label: string; value: string; tone?: "warning" | "error" }) {
  return (
    <div className={tone ? `stat stat-${tone}` : "stat"}>
      <div className="eyebrow">{label}</div>
      <div className="stat-value">{value}</div>
    </div>
  );
}

function AccountRow({ account, onAsk }: { account: Account; onAsk: () => void }) {
  const issue = account.needsReconnect
    ? account.disconnectReason || "Needs to be reconnected"
    : account.issues?.[0] || account.disconnectReason || "";
  const label = { healthy: "Healthy", warning: "Warning", error: "Error" }[account.status];
  return (
    <li className="row">
      <div className="row-main">
        <div className="row-title">
          {platformName(account.platform)} <span className="muted">{account.username ? `@${account.username}` : account.displayName}</span>
        </div>
        {issue && <div className="row-sub">{issue}</div>}
      </div>
      <span className={`badge badge-${account.status}`}>
        {account.status === "healthy" ? <CircleCheck size={14} aria-hidden /> : <CircleAlert size={14} aria-hidden />}
        {label}
      </span>
      {account.status !== "healthy" && (
        <button className="btn btn-ghost btn-icon" onClick={onAsk} title="Ask Claude to fix" aria-label={`Ask Claude to fix @${account.username ?? account.accountId}`}>
          <SendHorizontal size={16} aria-hidden />
        </button>
      )}
    </li>
  );
}
