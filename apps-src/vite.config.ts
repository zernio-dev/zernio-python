// Builds the app into one self-contained HTML file (scripts and styles
// inlined), the shape an MCP Apps ui:// resource needs: the host reviews the
// whole document and nothing loads from a CDN.
import { defineConfig } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

export default defineConfig({
  plugins: [viteSingleFile()],
  build: {
    outDir: "../src/late/mcp/apps/bundle",
    emptyOutDir: true,
    target: "es2022",
    rollupOptions: { input: "app.html" },
  },
});
