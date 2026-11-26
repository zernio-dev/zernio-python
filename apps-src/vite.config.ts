// Builds the app into one self-contained HTML file (scripts and styles
// inlined), the shape an MCP Apps ui:// resource needs. Same setup as the
// ext-apps basic-server-react example.
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import { viteSingleFile } from "vite-plugin-singlefile";

export default defineConfig({
  plugins: [react(), viteSingleFile()],
  build: {
    outDir: "../src/late/mcp/apps/bundle",
    emptyOutDir: true,
    rolldownOptions: { input: "mcp-app.html" },
  },
});
