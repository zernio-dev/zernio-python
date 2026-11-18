/** Number and name formatting. Missing values read "—". */
import { COPY } from "./copy";

const PLATFORMS: Record<string, string> = {
  twitter: "X", instagram: "Instagram", facebook: "Facebook", linkedin: "LinkedIn",
  tiktok: "TikTok", youtube: "YouTube", threads: "Threads", pinterest: "Pinterest",
  reddit: "Reddit", bluesky: "Bluesky", googlebusiness: "Google Business",
  telegram: "Telegram", snapchat: "Snapchat", discord: "Discord", slack: "Slack",
  whatsapp: "WhatsApp",
};

export function platformName(platform: string | undefined): string {
  return (platform && PLATFORMS[platform]) || platform || COPY.unavailable;
}

export function count(value: number | undefined, locale?: string): string {
  if (value === undefined) return COPY.unavailable;
  return new Intl.NumberFormat(locale, { maximumFractionDigits: 0 }).format(value);
}
