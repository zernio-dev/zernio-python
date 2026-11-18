/**
 * The few dashboard primitives the app needs, drawn as the product look (v2)
 * draws them: Section (a panel with its grey bar), StatusPill, PlatformTile,
 * Spinner (the pixel rain), Notice and Button. Numbers in comments are the
 * design principles they follow (Schedule-Posts-API, design-principles.md).
 */
import type { ButtonHTMLAttributes, ReactNode } from "react";
import { platformIcon, platformName } from "./api";

/** 18. A block is a white panel; a list's panel is headed by a grey bar with its eyebrow title. */
export function Section({ title, actions, children }: { title: string; actions?: ReactNode; children: ReactNode }) {
  return (
    <section className="section">
      <div className="section-bar">
        <h2 className="type-eyebrow">{title}</h2>
        {actions && <div className="section-actions">{actions}</div>}
      </div>
      <div className="section-body">{children}</div>
    </section>
  );
}

type Tone = "success" | "warning" | "danger" | "info" | "muted";

/** 16, 48. A state is a filled pill in its colour, sentence case, no glyph in its text. */
export function StatusPill({ label, tone, suffix, title }: { label: string; tone: Tone; suffix?: ReactNode; title?: string }) {
  return (
    <span className={`status-pill status-pill-${tone}`} title={title ?? label}>
      {label}
      {suffix}
    </span>
  );
}

/** 7, 42. A platform shows as its app icon in a bordered tile (md, 22px). */
export function PlatformTile({ platform }: { platform: string }) {
  return (
    <span className="platform-tile">
      <img src={platformIcon(platform)} alt={platformName(platform)} width={16} height={16} />
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
export function Notice({ tone, icon, children }: { tone: "danger" | "success" | "muted"; icon?: ReactNode; children: ReactNode }) {
  return (
    <p className={`notice notice-${tone}`} role={tone === "danger" ? "alert" : "status"}>
      {icon}
      <span>{children}</span>
    </p>
  );
}

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "outline" | "ghost";
  size?: "sm" | "md";
  icon?: boolean;
};

/** Square controls, 28/32px (size/control-sm, -md); hover changes colour only (1). */
export function Button({ variant = "outline", size = "md", icon, className, ...props }: ButtonProps) {
  const classes = ["btn", `btn-${variant}`, `btn-${size}`, icon ? "btn-icon" : "", className ?? ""].filter(Boolean);
  return <button type="button" className={classes.join(" ")} {...props} />;
}
