/** Accounts: every connected account by health, the broken ones first. */
import { Users } from "pixelarticons/react/Users.js";
import { type AccountsHealth, formatNumber } from "../api";
import { Empty, Kpis, Rows, Section } from "../ui";
import type { Ctx } from "./context";
import { ACCOUNT_RANK, AccountRow } from "./rows";

export function Accounts({ ctx, data }: { ctx: Ctx; data: AccountsHealth }) {
  const summary = data.summary ?? {};
  const accounts = [...(data.accounts ?? [])].sort((a, b) => ACCOUNT_RANK[a.status] - ACCOUNT_RANK[b.status]);
  const n = (v?: number) => formatNumber(v, ctx.locale);
  return (
    <>
      <Kpis
        items={[
          { key: "healthy", label: "Healthy", value: n(summary.healthy) },
          { key: "warning", label: "Need attention", value: n(summary.warning) },
          { key: "error", label: "Broken", value: n(summary.error) },
        ]}
      />
      <Section title="Accounts" count={accounts.length}>
        {accounts.length ? (
          <Rows>{accounts.map((a) => <AccountRow key={a.accountId} ctx={ctx} account={a} />)}</Rows>
        ) : (
          <Empty icon={<Users className="icon" />}>No connected accounts yet.</Empty>
        )}
      </Section>
    </>
  );
}
