/** Home: the workspace at a glance, with the way to each list. */
import { CheckDouble } from "pixelarticons/react/CheckDouble.js";
import { formatNumber, type HomeData } from "../api";
import { Empty, Kpis, More, Rows, Section } from "../ui";
import type { Ctx } from "./context";
import { ACCOUNT_RANK, AccountRow, FailedPostRow } from "./rows";

export function Home({ ctx, data }: { ctx: Ctx; data: HomeData }) {
  const summary = data.health.summary ?? {};
  const attention = (data.health.accounts ?? [])
    .filter((a) => a.status !== "healthy")
    .sort((a, b) => ACCOUNT_RANK[a.status] - ACCOUNT_RANK[b.status]);
  const shown = ctx.fullscreen ? 5 : 3;
  const n = (v?: number) => formatNumber(v, ctx.locale);

  return (
    <>
      <Kpis
        items={[
          { key: "accounts", label: "Accounts", value: n(summary.total) },
          { key: "attention", label: "Need attention", value: n((summary.warning ?? 0) + (summary.error ?? 0)) },
          { key: "failed", label: "Failed posts", value: n(data.failedTotal) },
        ]}
      />
      <Section title="Accounts that need attention" count={attention.length}>
        {attention.length ? (
          <Rows>{attention.slice(0, shown).map((a) => <AccountRow key={a.accountId} ctx={ctx} account={a} />)}</Rows>
        ) : (
          <Empty icon={<CheckDouble className="icon" />}>Every account can post.</Empty>
        )}
        {attention.length > shown && <More label={`All ${attention.length} accounts`} onClick={() => ctx.navigate("accounts")} />}
      </Section>
      <Section title="Failed posts" count={data.failedTotal}>
        {data.failedPosts.length ? (
          <Rows>{data.failedPosts.map((p) => <FailedPostRow key={p.id} ctx={ctx} post={p} />)}</Rows>
        ) : (
          <Empty icon={<CheckDouble className="icon" />}>Nothing failed to publish.</Empty>
        )}
        {data.failedTotal > data.failedPosts.length && <More label={`All ${data.failedTotal} failed posts`} onClick={() => ctx.navigate("posts")} />}
      </Section>
    </>
  );
}
