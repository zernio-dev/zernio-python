/**
 * Home: the workspace at a glance. Inline it shows the KPI row and up to
 * three accounts that need attention, with Open Zernio; full screen it lists
 * every account.
 */
import type { App } from "@modelcontextprotocol/ext-apps";
import { CheckDouble } from "pixelarticons/react/CheckDouble.js";
import { Expand } from "pixelarticons/react/Expand.js";
import { InfoBox } from "pixelarticons/react/InfoBox.js";
import { Reload } from "pixelarticons/react/Reload.js";
import { WarningDiamond } from "pixelarticons/react/WarningDiamond.js";
import { useCallback, useEffect, useState } from "react";
import { type Account, type AccountsHealth, getAccountsHealth, getFailedPostCount, platformName } from "./api";
import { Button, Notice, PlatformTile, Section, Spinner, StatusPill } from "./ui";

interface Props {
  app: App;
  fullscreen: boolean;
  canExpand: boolean;
  locale?: string;
}

const RANK = { error: 0, warning: 1, healthy: 2 } as const;
/** 48. Green works, amber needs action, red is broken. */
const STATE = {
  healthy: { label: "Healthy", tone: "success" },
  warning: { label: "Needs attention", tone: "warning" },
  error: { label: "Broken", tone: "danger" },
} as const;

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
    setError(h.status === "rejected" ? String((h.reason as Error)?.message ?? h.reason) : undefined);
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
  const needAttention = (summary.warning ?? 0) + (summary.error ?? 0);

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
    const issue = reasonOf(account) || STATE[account.status].label;
    const { isError } = await app.sendMessage({
      role: "user",
      content: [{ type: "text", text: `My ${platformName(account.platform)} account @${account.username ?? account.accountId} (account_id ${account.accountId}) shows "${issue}" in Zernio. Help me fix it.` }],
    });
    setNotice(isError ? "Could not send it to Claude." : "Sent to Claude. Continue in the chat.");
  };

  const fmt = (n?: number) => (n === undefined ? "—" : new Intl.NumberFormat(locale).format(n));
  const listed = fullscreen ? accounts : attention.slice(0, 3);

  if (loading && !health && !error) {
    return <div className="loading"><Spinner /></div>;
  }

  return (
    <div className="stack">
      {error && <Notice tone="danger" icon={<WarningDiamond className="icon" />}>Could not load your workspace. {error}</Notice>}
      {notice && <Notice tone="muted">{notice}</Notice>}

      {/* 20. Every KPI on one row of one panel, divided by hairlines: grey label on top, then the figure. */}
      <div className="kpis">
        <Kpi label="Accounts" value={fmt(summary.total)} />
        <Kpi label="Need attention" value={fmt(needAttention)} />
        <Kpi label="Failed posts" value={fmt(failed)} />
      </div>

      <Section
        title={fullscreen ? "Accounts" : "Accounts that need attention"}
        actions={
          <Button variant="ghost" size="sm" icon onClick={() => void load()} disabled={loading} aria-label="Refresh" title="Refresh">
            {loading ? <Spinner label="Refreshing" /> : <Reload className="icon" />}
          </Button>
        }
      >
        {listed.length ? (
          <ul className="rows">
            {listed.map((a) => (
              <AccountRow
                key={a.accountId}
                account={a}
                onReconnect={() => void app.openLink({ url: "https://zernio.com/dashboard" })}
                onAsk={() => void ask(a)}
              />
            ))}
          </ul>
        ) : (
          // 54. An empty list says what it would hold, with an icon.
          <div className="empty"><CheckDouble className="icon" /> Every account can post.</div>
        )}
      </Section>

      {canExpand && (
        <div className="actions">
          {/* requestDisplayMode must run inside the click: the host refuses it otherwise. */}
          <Button variant="primary" onClick={() => void app.requestDisplayMode({ mode: "fullscreen" })}>
            <Expand className="icon" /> Open Zernio
          </Button>
        </div>
      )}
    </div>
  );
}

function Kpi({ label, value }: { label: string; value: string }) {
  return (
    <div className="kpi">
      <div className="kpi-label">{label}</div>
      <div className="type-metric">{value}</div>
    </div>
  );
}

function reasonOf(account: Account): string {
  if (account.needsReconnect) return account.disconnectReason || "Needs to be reconnected";
  return account.issues?.[0] || account.disconnectReason || "";
}

/** 40, 43, 66. One line: tile, name with the handle in grey, the state (its reason behind the info mark), the fix. */
function AccountRow({ account, onReconnect, onAsk }: { account: Account; onReconnect: () => void; onAsk: () => void }) {
  const state = STATE[account.status];
  const reason = reasonOf(account);
  return (
    <li className="row">
      <PlatformTile platform={account.platform} />
      <div className="row-name">
        <span className="type-label">{platformName(account.platform)}</span>
        <span className="row-secondary">{account.username ? `@${account.username}` : account.displayName}</span>
      </div>
      <StatusPill label={state.label} tone={state.tone} title={reason || state.label} suffix={reason ? <InfoBox className="icon-sm" aria-hidden /> : undefined} />
      <div className="row-fix">
        {account.needsReconnect ? (
          <Button size="sm" onClick={onReconnect}>Reconnect</Button>
        ) : account.status !== "healthy" ? (
          <Button size="sm" onClick={onAsk}>Ask Claude</Button>
        ) : null}
      </div>
    </li>
  );
}
