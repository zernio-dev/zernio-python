/**
 * Analytics: the KPIs on one row, the picked one's daily chart in the same
 * panel (20), and the platforms with each one's share as a grey bar.
 */
import { ChartLine } from "pixelarticons/react/ChartLine.js";
import { useState } from "react";
import { type AnalyticsData, formatDate, formatNumber, type Metrics, platformName } from "../api";
import { Empty, Kpis, PlatformTile, Section } from "../ui";
import type { Ctx } from "./context";

type Key = "impressions" | "engagement" | "views" | "posts";

const LABELS: Record<Key, string> = {
  impressions: "Impressions",
  engagement: "Engagement",
  views: "Views",
  posts: "Posts",
};

function engagement(m: Metrics = {}): number {
  return (m.likes ?? 0) + (m.comments ?? 0) + (m.shares ?? 0) + (m.saves ?? 0);
}

function dayValue(day: NonNullable<AnalyticsData["dailyData"]>[number], key: Key): number {
  if (key === "posts") return day.postCount ?? 0;
  if (key === "engagement") return engagement(day.metrics);
  return day.metrics?.[key] ?? 0;
}

export function Analytics({ ctx, data }: { ctx: Ctx; data: AnalyticsData }) {
  const [key, setKey] = useState<Key>("impressions");
  const days = [...(data.dailyData ?? [])].sort((a, b) => a.date.localeCompare(b.date));
  const totals = data.totals ?? {};
  const total: Record<Key, number> = {
    impressions: totals.impressions ?? 0,
    engagement: totals.engagement ?? engagement(totals),
    views: totals.views ?? 0,
    posts: totals.postCount ?? 0,
  };
  const n = (v: number) => formatNumber(v, ctx.locale, true);
  const platforms = [...(data.platformBreakdown ?? [])].sort((a, b) => (b.impressions ?? 0) - (a.impressions ?? 0));
  const maxImpressions = Math.max(1, ...platforms.map((p) => p.impressions ?? 0));

  return (
    <>
      <Kpis
        items={(Object.keys(LABELS) as Key[]).map((k) => ({ key: k, label: LABELS[k], value: n(total[k]) }))}
        selected={key}
        onSelect={(k) => setKey(k as Key)}
      >
        {days.length ? (
          <Chart
            points={days.map((d) => ({ date: d.date, value: dayValue(d, key) }))}
            label={LABELS[key]}
            locale={ctx.locale}
            tall={ctx.fullscreen}
          />
        ) : (
          <Empty icon={<ChartLine className="icon" />}>No posts in this period.</Empty>
        )}
      </Kpis>
      {platforms.length > 0 && (
        <Section title="Platforms" count={platforms.length} flush>
          <table className="table">
            <thead>
              <tr>
                <th>Platform</th>
                <th className="num">Posts</th>
                <th className="num">Impressions</th>
                <th className="num">Engagement</th>
                <th className="share-col">Share</th>
              </tr>
            </thead>
            <tbody>
              {platforms.map((p) => (
                <tr key={p.platform}>
                  <td>
                    <span className="cell-lead"><PlatformTile platform={p.platform} /> {platformName(p.platform)}</span>
                  </td>
                  <td className="num">{formatNumber(p.postCount, ctx.locale)}</td>
                  <td className="num">{n(p.impressions ?? 0)}</td>
                  <td className="num">{n(engagement(p))}</td>
                  <td className="share-col">
                    <span className="share"><span style={{ width: `${((p.impressions ?? 0) / maxImpressions) * 100}%` }} /></span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Section>
      )}
    </>
  );
}

/** A daily line in the panel's hue (chart/3), dashed gridlines, dates at the ends and middle. */
function Chart({ points, label, locale, tall }: {
  points: { date: string; value: number }[];
  label: string;
  locale?: string;
  tall: boolean;
}) {
  const [hover, setHover] = useState<number | null>(null);
  const w = 600;
  const h = tall ? 220 : 120;
  const max = Math.max(1, ...points.map((p) => p.value));
  const step = points.length > 1 ? w / (points.length - 1) : 0;
  const xy = points.map((p, i) => [i * step, h - (p.value / max) * (h - 8) - 4] as const);
  const line = xy.map(([x, y], i) => `${i ? "L" : "M"}${x.toFixed(1)} ${y.toFixed(1)}`).join("");
  const at = hover ?? points.length - 1;
  const dates = [0, Math.floor((points.length - 1) / 2), points.length - 1];

  return (
    <div className="chart">
      <div className="chart-readout">
        <span className="kpi-label">{formatDate(points[at].date, locale, { weekday: "short", month: "short", day: "numeric", timeZone: "UTC" })}</span>
        <span className="type-label">{formatNumber(points[at].value, locale)} {label.toLowerCase()}</span>
      </div>
      <div className="chart-plot">
        <span className="chart-max">{formatNumber(max, locale, true)}</span>
        <svg
          viewBox={`0 0 ${w} ${h}`}
          preserveAspectRatio="none"
          style={{ height: h }}
          role="img"
          aria-label={`${label} per day`}
          onPointerMove={(e) => {
            const box = e.currentTarget.getBoundingClientRect();
            setHover(Math.max(0, Math.min(points.length - 1, Math.round(((e.clientX - box.left) / box.width) * (points.length - 1)))));
          }}
          onPointerLeave={() => setHover(null)}
        >
          {[0.5, 1].map((f) => (
            <line key={f} x1={0} x2={w} y1={h - f * (h - 8) - 4} y2={h - f * (h - 8) - 4} className="chart-grid" />
          ))}
          <line x1={0} x2={w} y1={h - 0.5} y2={h - 0.5} className="chart-axis" />
          <path d={line} className="chart-line" />
          {hover !== null && <line x1={xy[hover][0]} x2={xy[hover][0]} y1={0} y2={h} className="chart-grid" />}
        </svg>
      </div>
      <div className="chart-dates">
        {dates.map((i, k) => (
          <span key={k}>{formatDate(points[i].date, locale, { month: "short", day: "numeric", timeZone: "UTC" })}</span>
        ))}
      </div>
    </div>
  );
}
