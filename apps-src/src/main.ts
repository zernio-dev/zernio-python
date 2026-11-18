/**
 * The Zernio MCP App: entry point. Wires the host connection (the official
 * ext-apps SDK) to the store, loads the workspace through the server's tools,
 * and renders. Opened by the zernio_open_app tool.
 */
import {
  App,
  applyDocumentTheme,
  applyHostFonts,
  applyHostStyleVariables,
  type McpUiHostContext,
} from "@modelcontextprotocol/ext-apps";
import { ZernioClient } from "./client";
import { COPY } from "./copy";
import { INITIAL_STATE, type Account, type AppState } from "./model";
import { Store } from "./store";
import { homeView } from "./views/home";
import { shell, skeleton } from "./views/shell";
import "./styles.css";

const app = new App({ name: "Zernio", version: "0.1.0" }, { availableDisplayModes: ["inline", "fullscreen"] });
const client = new ZernioClient((name, args) => app.callServerTool({ name, arguments: args }));
const store = new Store<AppState>(INITIAL_STATE);
const root = document.getElementById("root") as HTMLElement;

// A response for a load the user has already replaced is dropped.
let loadSeq = 0;

async function load(): Promise<void> {
  const seq = ++loadSeq;
  store.set({ phase: store.get().health ? "loading" : "connecting", error: undefined });
  const [health, failed] = await Promise.allSettled([client.health(), client.failedPosts()]);
  if (seq !== loadSeq) return;
  if (failed.status === "rejected") console.warn("[zernio-app] failed posts unavailable:", failed.reason);
  store.set({
    phase: "ready",
    health: health.status === "fulfilled" ? health.value : store.get().health,
    failedPosts: failed.status === "fulfilled" ? failed.value : undefined,
    error: health.status === "rejected" ? `${COPY.loadFailed} ${String((health.reason as Error).message ?? "")}` : undefined,
  });
  void tellModel();
}

/** Tells Claude what the panel shows, so "these accounts" resolves to them. */
async function tellModel(): Promise<void> {
  if (!app.getHostCapabilities()?.updateModelContext) return;
  const { health, failedPosts } = store.get();
  const attention = (health?.accounts ?? []).filter((a) => a.status !== "healthy");
  const text =
    `The Zernio panel shows the workspace: ${health?.summary?.total ?? 0} accounts, ` +
    `${attention.length} needing attention` +
    (attention.length ? ` (${attention.map((a) => `${a.platform} @${a.username ?? a.accountId}`).join(", ")})` : "") +
    (failedPosts !== undefined ? `, ${failedPosts} failed posts.` : ".");
  await app.updateModelContext({
    content: [{ type: "text", text }],
    structuredContent: { view: "home", attention: attention.map((a) => a.accountId), failedPosts },
  });
}

async function ask(account: Account): Promise<void> {
  const issue = account.issues?.[0] || account.disconnectReason || account.status;
  const result = await app.sendMessage({
    role: "user",
    content: [{ type: "text", text: `My ${account.platform} account @${account.username ?? account.accountId} (account_id ${account.accountId}) shows "${issue}" in Zernio. Help me fix it.` }],
  });
  store.set({ feedback: result.isError ? { tone: "error", text: "Could not send it to Claude." } : { tone: "ok", text: COPY.sentToClaude } });
}

function render(state: AppState): void {
  const ctx = app.getHostContext();
  const canExpand = ctx?.displayMode !== "fullscreen" && !!ctx?.availableDisplayModes?.includes("fullscreen");
  const body =
    state.phase === "connecting"
      ? skeleton()
      : homeView({
          state,
          compact: ctx?.displayMode !== "fullscreen",
          canExpand,
          locale: ctx?.locale,
          expand: () => void app.requestDisplayMode({ mode: "fullscreen" }).catch(() => undefined),
          refresh: () => void load(),
          reconnect: () => void app.openLink({ url: "https://zernio.com/dashboard" }),
          ask: (account) => void ask(account),
        });
  root.replaceChildren(shell(state, body));
}

function applyHostContext(ctx: McpUiHostContext): void {
  if (ctx.theme) applyDocumentTheme(ctx.theme);
  // Host tokens only set the page surface; the brand tokens are prefixed and
  // never overridden by them.
  if (ctx.styles?.variables) applyHostStyleVariables(ctx.styles.variables);
  if (ctx.styles?.css?.fonts) applyHostFonts(ctx.styles.css.fonts);
  const doc = document.documentElement;
  doc.dataset.display = ctx.displayMode ?? "inline";
  doc.style.setProperty("--safe-bottom", `${ctx.safeAreaInsets?.bottom ?? 0}px`);
  render(store.get());
}

// Handlers are registered before connect(): the host may send the tool result
// as soon as the handshake completes.
app.onerror = (err) => console.error("[zernio-app]", err);
app.onhostcontextchanged = applyHostContext;
app.ontoolresult = () => void load();
app.ontoolcancelled = () => store.set({ phase: "ready", error: "Cancelled." });

store.subscribe(render);
render(store.get());

void app.connect().then(() => {
  const ctx = app.getHostContext();
  if (ctx) applyHostContext(ctx);
});
