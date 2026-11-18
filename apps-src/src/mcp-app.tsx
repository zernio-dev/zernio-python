/**
 * The Zernio MCP App, on the ext-apps React hooks (the pattern of the SDK's
 * basic-server-react example), drawn in the dashboard's design system v2.
 *
 * Every tool in src/late/mcp/apps/tools.py opens this app on its screen and
 * hands it `{view, data, args}`. The app switches screens and refreshes by
 * calling those same tools, so one set of components draws everything.
 */
import type { McpUiHostContext } from "@modelcontextprotocol/ext-apps";
import { useApp, useHostStyles } from "@modelcontextprotocol/ext-apps/react";
import { Expand } from "pixelarticons/react/Expand.js";
import { Reload } from "pixelarticons/react/Reload.js";
import { StrictMode, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  type AccountsHealth,
  type AdsData,
  type AnalyticsData,
  type ApprovalsData,
  type CallResult,
  type HomeData,
  type PostsData,
  type PreviewData,
  type Screen,
  screenOf,
  TABS,
  textOf,
  TOOLS,
  type View,
  VIEW_TITLES,
} from "./api";
import { installFonts } from "./fonts";
import { Accounts } from "./screens/Accounts";
import { Ads } from "./screens/Ads";
import { Analytics } from "./screens/Analytics";
import { Approvals } from "./screens/Approvals";
import type { ActResult, Ctx } from "./screens/context";
import { Home } from "./screens/Home";
import { Posts } from "./screens/Posts";
import { Preview } from "./screens/Preview";
import { Button, Notice, Spinner, Tabs } from "./ui";
import "./global.css";

installFonts();

/** How long to wait for the opening tool's result before loading the screen ourselves. */
const RESULT_GRACE_MS = 2500;

const VIEW_OF_TOOL = Object.fromEntries(Object.entries(TOOLS).map(([view, tool]) => [tool, view])) as Record<string, View>;

function ZernioApp() {
  const [hostContext, setHostContext] = useState<McpUiHostContext | undefined>();
  const [screen, setScreen] = useState<Screen>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>();
  const [notice, setNotice] = useState<string>();
  const toolArgs = useRef<Record<string, unknown>>({});
  const gotResult = useRef(false);

  const show = useCallback((result: CallResult) => {
    if (result.isError) {
      setError(textOf(result) || "The tool call failed.");
      return;
    }
    const next = screenOf(result);
    if (!next) {
      setError("This result has no screen to show.");
      return;
    }
    setError(undefined);
    setScreen(next);
  }, []);

  const { app, error: connectError } = useApp({
    appInfo: { name: "Zernio", version: "0.2.0" },
    capabilities: { availableDisplayModes: ["inline", "fullscreen"] },
    onAppCreated: (app) => {
      app.ontoolinput = ({ arguments: args }) => {
        toolArgs.current = args ?? {};
      };
      app.ontoolresult = (result) => {
        gotResult.current = true;
        show(result);
      };
      app.ontoolcancelled = () => setError("Cancelled.");
      app.onhostcontextchanged = (params) => setHostContext((prev) => ({ ...prev, ...params }));
      app.onerror = console.error;
    },
  });

  // Theme, host CSS variables and host fonts, kept in sync with the host.
  useHostStyles(app, app?.getHostContext());

  useEffect(() => {
    if (app) setHostContext(app.getHostContext());
  }, [app]);

  // A screen is a newer request than the one before it: a slow answer for a
  // screen the user already left is dropped.
  const seq = useRef(0);
  const load = useCallback(
    async (view: View, args: Record<string, unknown> = {}) => {
      if (!app) return;
      const mine = ++seq.current;
      setLoading(true);
      setNotice(undefined);
      try {
        const result = await app.callServerTool({ name: TOOLS[view], arguments: args });
        if (mine === seq.current) show(result);
      } catch (e) {
        if (mine === seq.current) setError(e instanceof Error ? e.message : String(e));
      } finally {
        if (mine === seq.current) setLoading(false);
      }
    },
    [app, show],
  );

  // Opened without a result (from Claude's Artifacts page, or a host that
  // delivers none): load the screen of the tool that opened us, else Home.
  useEffect(() => {
    if (!app) return;
    const timer = setTimeout(() => {
      if (gotResult.current) return;
      const tool = app.getHostContext()?.toolInfo?.tool?.name;
      const view = (tool && VIEW_OF_TOOL[tool]) || "home";
      void load(view, view === "home" ? {} : toolArgs.current);
    }, RESULT_GRACE_MS);
    return () => clearTimeout(timer);
  }, [app, load]);

  // Tell Claude what the app shows, so "these accounts" resolves to them.
  useEffect(() => {
    if (!app || !screen || !app.getHostCapabilities()?.updateModelContext) return;
    void app.updateModelContext({
      content: [{ type: "text", text: `The Zernio app shows ${VIEW_TITLES[screen.view]}.` }],
      structuredContent: { view: screen.view, args: screen.args },
    });
  }, [app, screen]);

  const ctx = useMemo<Ctx | undefined>(() => {
    if (!app) return undefined;
    return {
      app,
      locale: hostContext?.locale,
      fullscreen: hostContext?.displayMode === "fullscreen",
      navigate: (view, args) => void load(view, args),
      async act(tool, args): Promise<ActResult> {
        try {
          const result = await app.callServerTool({ name: tool, arguments: args });
          return { ok: !result.isError, text: textOf(result), data: result.structuredContent };
        } catch (e) {
          return { ok: false, text: e instanceof Error ? e.message : String(e) };
        }
      },
      ask(text) {
        void app.sendMessage({ role: "user", content: [{ type: "text", text }] }).then(({ isError }) =>
          setNotice(isError ? "Could not send it to Claude." : "Sent to Claude. Continue in the chat."),
        );
      },
      tell(text) {
        if (app.getHostCapabilities()?.updateModelContext) {
          void app.updateModelContext({ content: [{ type: "text", text }] });
        }
      },
    };
  }, [app, hostContext?.locale, hostContext?.displayMode, load]);

  if (connectError) return <Notice tone="danger">{connectError.message}</Notice>;
  if (!ctx) return <Loading />;

  const fullscreen = ctx.fullscreen;
  const canExpand = !fullscreen && !!hostContext?.availableDisplayModes?.includes("fullscreen");
  const insets = hostContext?.safeAreaInsets;

  return (
    <main
      className={fullscreen ? "app app-fullscreen" : "app"}
      style={{ paddingTop: insets?.top, paddingRight: insets?.right, paddingLeft: insets?.left }}
    >
      <header className="header">
        <img className="logo" src="https://zernio.com/icon.svg?v=4" alt="" width={18} height={18} />
        {/* 35. The breadcrumb is the screen's title. */}
        <span className="type-page-title">Zernio</span>
        {screen && <span className="crumb">{VIEW_TITLES[screen.view]}</span>}
        <span className="header-actions">
          {loading && screen && <Spinner label="Refreshing" />}
          {screen && (
            <Button variant="ghost" icon aria-label="Refresh" title="Refresh" disabled={loading} onClick={() => void load(screen.view, screen.args)}>
              <Reload className="icon" />
            </Button>
          )}
          {canExpand && (
            // requestDisplayMode must run inside the click: the host refuses it otherwise.
            <Button variant="ghost" icon aria-label="Open full screen" title="Open full screen" onClick={() => void ctx.app.requestDisplayMode({ mode: "fullscreen" })}>
              <Expand className="icon" />
            </Button>
          )}
        </span>
      </header>
      {fullscreen && (
        <Tabs
          items={TABS.map((key) => ({ key, label: VIEW_TITLES[key] }))}
          active={screen && TABS.includes(screen.view) ? screen.view : undefined}
          onPick={(view) => ctx.navigate(view)}
        />
      )}
      <div className="stack">
        {error && <Notice tone="danger">{error}</Notice>}
        {notice && <Notice tone="muted">{notice}</Notice>}
        {screen ? <ScreenView ctx={ctx} screen={screen} key={`${screen.view}:${JSON.stringify(screen.args)}`} /> : !error && <Loading />}
      </div>
    </main>
  );
}

function ScreenView({ ctx, screen }: { ctx: Ctx; screen: Screen }) {
  switch (screen.view) {
    case "home":
      return <Home ctx={ctx} data={screen.data as HomeData} />;
    case "posts":
      return <Posts ctx={ctx} data={screen.data as PostsData} />;
    case "analytics":
      return <Analytics ctx={ctx} data={screen.data as AnalyticsData} />;
    case "accounts":
      return <Accounts ctx={ctx} data={screen.data as AccountsHealth} />;
    case "ads":
      return <Ads ctx={ctx} data={screen.data as AdsData} />;
    case "preview":
      return <Preview ctx={ctx} data={screen.data as PreviewData} />;
    case "approvals":
      return <Approvals ctx={ctx} data={screen.data as ApprovalsData} />;
  }
}

function Loading() {
  return (
    <div className="loading">
      <Spinner />
    </div>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ZernioApp />
  </StrictMode>,
);
