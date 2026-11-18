/**
 * The dashboard primitives the app is built from, drawn as the product look
 * (v2) draws them. Every screen uses only these, so they all read alike.
 * Numbers in comments are the design principles they follow
 * (Schedule-Posts-API, .claude/rules/design-principles.md).
 */
import { InfoBox } from "pixelarticons/react/InfoBox.js";
import type { ButtonHTMLAttributes, ReactNode } from "react";
import { platformIcon, platformName } from "./api";

/** 18. A block is a white panel; a list's panel is headed by a grey bar with its eyebrow title. */
export function Section({ title, count, actions, children, flush }: {
  title: string;
  count?: number;
  actions?: ReactNode;
  children: ReactNode;
  /** The body runs edge to edge (a table, a chart). */
  flush?: boolean;
}) {
  return (
    <section className="section">
      <div className="section-bar">
        <h2 className="type-eyebrow">
          {title}
          {count !== undefined && <span className="count">{count}</span>}
        </h2>
        {actions && <div className="section-actions">{actions}</div>}
      </div>
      <div className={flush ? "section-body section-body-flush" : "section-body"}>{children}</div>
    </section>
  );
}

export type Tone = "success" | "warning" | "danger" | "info" | "muted";

/** 16, 43, 48, 66. A state is a filled pill in its colour; its reason sits behind the info mark. */
export function StatusPill({ label, tone, reason }: { label: string; tone: Tone; reason?: string }) {
  return (
    <span className={`status-pill status-pill-${tone}`} title={reason ?? label}>
      {label}
      {reason && <InfoBox className="icon-sm" aria-label={reason} />}
    </span>
  );
}

/** 16. A label that is not a state: outlined and colourless. */
export function Badge({ children }: { children: ReactNode }) {
  return <span className="badge">{children}</span>;
}

/** 7, 42. A platform shows as its app icon in a bordered tile (md, 22px). */
export function PlatformTile({ platform }: { platform: string }) {
  return (
    <span className="platform-tile" title={platformName(platform)}>
      <img src={platformIcon(platform)} alt={platformName(platform)} width={16} height={16} />
    </span>
  );
}

export function PlatformTiles({ platforms }: { platforms: string[] }) {
  const unique = [...new Set(platforms)];
  return (
    <span className="platform-tiles">
      {unique.slice(0, 3).map((p) => <PlatformTile key={p} platform={p} />)}
      {unique.length > 3 && <Badge>+{unique.length - 3}</Badge>}
    </span>
  );
}

/** 17. Loading is a 3x3 pixel rain in the text colour, stepping between frames. */
export function Spinner({ label = "Loading" }: { label?: string }) {
  return (
    <span className="spinner" role="status" aria-label={label}>
      {Array.from({ length: 9 }, (_, i) => {
        const frame = (Math.floor(i / 3) + (i % 3)) % 3;
        return <span key={i} style={{ animationDelay: `${(-((3 - frame) % 3) / 3) * 600}ms` }} />;
      })}
    </span>
  );
}

/** 15. A notice is coloured text with its icon, not a box. */
export function Notice({ tone, children }: { tone: "danger" | "warning" | "success" | "muted"; children: ReactNode }) {
  return (
    <p className={`notice notice-${tone}`} role={tone === "danger" ? "alert" : "status"}>
      {tone !== "muted" && <InfoBox className="icon" aria-hidden />}
      <span>{children}</span>
    </p>
  );
}

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "outline" | "ghost" | "link";
  size?: "sm" | "md";
  icon?: boolean;
};

/** Square controls, 28/32px; hover changes colour only (1); focus darkens the border (13). */
export function Button({ variant = "outline", size = "md", icon, className, ...props }: ButtonProps) {
  const classes = ["btn", `btn-${variant}`, `btn-${size}`, icon ? "btn-icon" : "", className ?? ""].filter(Boolean);
  return <button type="button" className={classes.join(" ")} {...props} />;
}

/** 20. Every KPI on one row of one panel, divided by hairlines; picking one draws a rule along its foot. */
export function Kpis({ items, selected, onSelect, children }: {
  items: { key: string; label: string; value: string }[];
  selected?: string;
  onSelect?: (key: string) => void;
  /** The chart that explains the picked figure, in the same panel. */
  children?: ReactNode;
}) {
  return (
    <div className="kpis">
      <div className="kpi-row" style={{ gridTemplateColumns: `repeat(${items.length}, minmax(0, 1fr))` }}>
        {items.map((item) =>
          onSelect ? (
            <button
              key={item.key}
              type="button"
              className={item.key === selected ? "kpi kpi-selected" : "kpi"}
              aria-pressed={item.key === selected}
              onClick={() => onSelect(item.key)}
            >
              <div className="kpi-label">{item.label}</div>
              <div className="type-metric">{item.value}</div>
            </button>
          ) : (
            <div key={item.key} className="kpi">
              <div className="kpi-label">{item.label}</div>
              <div className="type-metric">{item.value}</div>
            </div>
          ),
        )}
      </div>
      {children && <div className="kpi-chart">{children}</div>}
    </div>
  );
}

/** 28. Underline tabs: the active one is marked, the rest grey; hover only darkens the text. */
export function Tabs<K extends string>({ items, active, onPick }: {
  items: { key: K; label: string }[];
  active?: K;
  onPick: (key: K) => void;
}) {
  return (
    <nav className="tabs" aria-label="Screens">
      {items.map((item) => (
        <button
          key={item.key}
          type="button"
          className={item.key === active ? "tab tab-active" : "tab"}
          aria-current={item.key === active ? "page" : undefined}
          onClick={() => onPick(item.key)}
        >
          {item.label}
        </button>
      ))}
    </nav>
  );
}

/** 22, 40, 43, 44. A row is one line: lead, name with its grey secondary fact, state, then the fix. */
export function Row({ lead, name, secondary, state, fix }: {
  lead?: ReactNode;
  name: ReactNode;
  secondary?: ReactNode;
  state?: ReactNode;
  fix?: ReactNode;
}) {
  return (
    <li className="row">
      {lead}
      <div className="row-name">
        <span className="type-label">{name}</span>
        {secondary && <span className="row-secondary">{secondary}</span>}
      </div>
      {state}
      <div className="row-fix">{fix}</div>
    </li>
  );
}

export function Rows({ children }: { children: ReactNode }) {
  return <ul className="rows">{children}</ul>;
}

/** 54. An empty list says what it would hold, with an icon. */
export function Empty({ icon, children }: { icon: ReactNode; children: ReactNode }) {
  return <div className="empty">{icon}{children}</div>;
}

/** A list cut short says so, with the way to the rest. */
export function More({ label, onClick }: { label: string; onClick: () => void }) {
  return (
    <div className="more">
      <Button variant="link" size="sm" onClick={onClick}>{label}</Button>
    </div>
  );
}
