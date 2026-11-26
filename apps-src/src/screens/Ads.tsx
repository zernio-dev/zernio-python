/** Ads: what needs attention across the ads, most severe first, each with its fix. */
import { Megaphone } from "pixelarticons/react/Megaphone.js";
import { useState } from "react";
import { type AdsAlert, type AdsData, formatNumber, platformName } from "../api";
import { Button, Empty, Kpis, PlatformTile, Row, Rows, Section, StatusPill, type Tone } from "../ui";
import type { Ctx } from "./context";

const SEVERITY: Record<AdsAlert["severity"], { label: string; tone: Tone }> = {
  error: { label: "Error", tone: "danger" },
  warning: { label: "Warning", tone: "warning" },
  info: { label: "Info", tone: "info" },
};

export function Ads({ ctx, data }: { ctx: Ctx; data: AdsData }) {
  const [dismissed, setDismissed] = useState<string[]>([]);
  const alerts = (data.alerts ?? []).filter((a) => !dismissed.includes(a.id));
  const counts = data.counts ?? {};
  const n = (v?: number) => formatNumber(v ?? 0, ctx.locale);

  const dismiss = async (alert: AdsAlert) => {
    const result = await ctx.act("ui_dismiss_ads_alert", { alert_id: alert.id });
    if (result.ok) {
      setDismissed((d) => [...d, alert.id]);
      ctx.tell(`From the Zernio app the user dismissed ads alert ${alert.id} ("${alert.title}") for 30 days.`);
    }
  };

  return (
    <>
      <Kpis
        items={[
          { key: "error", label: "Errors", value: n(counts.error) },
          { key: "warning", label: "Warnings", value: n(counts.warning) },
          { key: "info", label: "Info", value: n(counts.info) },
        ]}
      />
      <Section title="Ads that need attention" count={alerts.length}>
        {alerts.length ? (
          <Rows>
            {alerts.map((alert) => (
              <AlertRow key={alert.id} ctx={ctx} alert={alert} onDismiss={() => void dismiss(alert)} />
            ))}
          </Rows>
        ) : (
          <Empty icon={<Megaphone className="icon" />}>Nothing needs attention in your ads.</Empty>
        )}
      </Section>
    </>
  );
}

function AlertRow({ ctx, alert, onDismiss }: { ctx: Ctx; alert: AdsAlert; onDismiss: () => void }) {
  const severity = SEVERITY[alert.severity] ?? SEVERITY.info;
  const url = alert.fix?.url ? (alert.fix.url.startsWith("/") ? `https://zernio.com${alert.fix.url}` : alert.fix.url) : undefined;
  const entity = alert.entity?.name ?? undefined;
  return (
    <Row
      lead={alert.platform ? <PlatformTile platform={alert.platform} /> : undefined}
      name={alert.title}
      secondary={entity}
      state={<StatusPill label={severity.label} tone={severity.tone} reason={alert.message} />}
      fix={
        <span className="row-actions">
          {url ? (
            <Button size="sm" title={alert.fix?.label} onClick={() => void ctx.app.openLink({ url })}>Fix</Button>
          ) : (
            <Button
              size="sm"
              onClick={() =>
                ctx.ask(
                  `Help me fix this ${platformName(alert.platform)} ads alert${entity ? ` on "${entity}"` : ""}: ${alert.title}. ${alert.message ?? ""} (alert id ${alert.id})`,
                )
              }
            >
              Ask Claude
            </Button>
          )}
          <Button size="sm" variant="ghost" onClick={onDismiss} title="Hide for 30 days">Dismiss</Button>
        </span>
      }
    />
  );
}
