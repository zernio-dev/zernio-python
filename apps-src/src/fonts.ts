/**
 * Geist, Geist Mono and Geist Pixel Square, the design system's three faces.
 * MCP Apps allow fonts only from declared origins (no data: URLs), so the MCP
 * server serves them; it writes its own public URL over ZERNIO_ORIGIN when it
 * serves this bundle, and lists that origin in the resource's CSP.
 */
const ORIGIN = "__ZERNIO_ORIGIN__";

const FACES = [
  { family: "Geist", file: "Geist-Variable.woff2", weight: "100 900" },
  { family: "Geist Mono", file: "GeistMono-Variable.woff2", weight: "100 900" },
  { family: "Geist Pixel Square", file: "GeistPixel-Square.woff2", weight: "500" },
];

export function installFonts(): void {
  if (ORIGIN.startsWith("__")) return;
  const style = document.createElement("style");
  style.textContent = FACES.map(
    (f) =>
      `@font-face{font-family:"${f.family}";src:url("${ORIGIN}/apps/fonts/${f.file}") format("woff2");font-weight:${f.weight};font-display:swap}`,
  ).join("");
  document.head.appendChild(style);
}
