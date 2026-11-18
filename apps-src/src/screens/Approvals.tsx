/** Approvals: the changes an automation waits on, each request with Approve and Reject. */
import { Clock } from "pixelarticons/react/Clock.js";
import { useState } from "react";
import { type Approval, type ApprovalChange, type ApprovalsData, formatDate } from "../api";
import { Badge, Button, Empty, Notice, Row, Rows, Section, StatusPill, type Tone } from "../ui";
import type { Ctx } from "./context";

const CHANGE: Record<string, string> = {
  "ads.pause": "Pause",
  "ads.activate": "Activate",
  "ads.set_budget": "Budget",
  "ads.duplicate": "Duplicate",
  "ads.edit_name": "Rename",
  "ads.set_bid": "Bid",
  "ads.set_target": "Target",
  "ads.reallocate_budget": "Reallocate",
};

const STATE: Record<Approval["status"], { label: string; tone: Tone }> = {
  pending: { label: "Waiting for you", tone: "warning" },
  approved: { label: "Approved", tone: "success" },
  rejected: { label: "Rejected", tone: "muted" },
  expired: { label: "Expired", tone: "muted" },
  cancelled: { label: "Cancelled", tone: "muted" },
};

function valueOf(v: ApprovalChange["previous"]): string {
  if (!v) return "";
  const first = Object.values(v)[0];
  return first === undefined ? "" : String(first);
}

export function Approvals({ ctx, data }: { ctx: Ctx; data: ApprovalsData }) {
  const [approvals, setApprovals] = useState(data.approvals);
  if (!approvals.length) {
    return (
      <Section title="Approvals" count={0}>
        <Empty icon={<Clock className="icon" />}>Nothing is waiting for approval.</Empty>
      </Section>
    );
  }
  return (
    <>
      {approvals.map((approval) => (
        <ApprovalPanel
          key={approval.id}
          ctx={ctx}
          automationId={data.automationId}
          approval={approval}
          onDecided={(next) => setApprovals((list) => list.map((a) => (a.id === next.id ? next : a)))}
        />
      ))}
    </>
  );
}

function ApprovalPanel({ ctx, automationId, approval, onDecided }: {
  ctx: Ctx;
  automationId: string;
  approval: Approval;
  onDecided: (approval: Approval) => void;
}) {
  const [busy, setBusy] = useState<"approve" | "reject" | null>(null);
  const [error, setError] = useState<string>();
  const state = STATE[approval.status];
  const pending = approval.status === "pending";

  const decide = async (decision: "approve" | "reject") => {
    setBusy(decision);
    setError(undefined);
    const result = await ctx.act("ui_decide_automation_approval", { automation_id: automationId, approval_id: approval.id, decision });
    const next = (result.data as { approval?: Approval } | undefined)?.approval;
    setBusy(null);
    if (!result.ok || !next) {
      setError(result.text || "The decision did not go through.");
      return;
    }
    onDecided(next);
    ctx.tell(`From the Zernio app the user ${decision === "approve" ? "approved" : "rejected"} automation request ${approval.id} (automation ${automationId}); it is now ${next.status}.`);
  };

  return (
    <Section
      title={pending ? `Expires ${formatDate(approval.expiresAt, ctx.locale, { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" })}` : "Request"}
      count={approval.changes.length}
      actions={<StatusPill label={state.label} tone={state.tone} reason={approval.decidedBy?.email ? `Decided by ${approval.decidedBy.email}` : undefined} />}
    >
      <Rows>
        {approval.changes.map((change, i) => {
          const from = valueOf(change.previous);
          const to = valueOf(change.target);
          return (
            <Row
              key={i}
              lead={<Badge>{CHANGE[change.type] ?? change.type}</Badge>}
              name={change.subject?.name ?? change.subject?.id ?? "—"}
              secondary={change.subject?.kind}
              state={from || to ? <span className="type-mono">{from} → {to}</span> : undefined}
              fix={change.status && change.status !== "pending" ? <span className="row-secondary">{change.status}</span> : undefined}
            />
          );
        })}
      </Rows>
      {error && <Notice tone="danger">{error}</Notice>}
      {pending && approval.canDecide && (
        <div className="section-footer">
          <Button variant="primary" disabled={!!busy} onClick={() => void decide("approve")}>{busy === "approve" ? "Approving…" : "Approve"}</Button>
          <Button disabled={!!busy} onClick={() => void decide("reject")}>{busy === "reject" ? "Rejecting…" : "Reject"}</Button>
        </div>
      )}
      {pending && !approval.canDecide && <Notice tone="muted">Only {approval.to?.join(", ")} can decide this.</Notice>}
    </Section>
  );
}
