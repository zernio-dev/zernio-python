/**
 * The Zernio MCP App, on the ext-apps React hooks (the pattern of the SDK's
 * basic-server-react example). Opened by the zernio_open_app tool.
 */
import type { App, McpUiHostContext } from "@modelcontextprotocol/ext-apps";
import { useApp, useHostStyles } from "@modelcontextprotocol/ext-apps/react";
import { StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { installFonts } from "./fonts";
import { Home } from "./Home";
import { Spinner } from "./ui";
import "./global.css";

installFonts();

function ZernioApp() {
  const [hostContext, setHostContext] = useState<McpUiHostContext | undefined>();
  const [opened, setOpened] = useState(false);

  // useApp creates the App, lets us register handlers, then connects.
  const { app, error } = useApp({
    appInfo: { name: "Zernio", version: "0.1.0" },
    capabilities: { availableDisplayModes: ["inline", "fullscreen"] },
    onAppCreated: (app) => {
      app.ontoolresult = () => setOpened(true);
      app.onhostcontextchanged = (params) => setHostContext((prev) => ({ ...prev, ...params }));
      app.onerror = console.error;
    },
  });

  // Theme, host CSS variables and host fonts, kept in sync with the host.
  useHostStyles(app, app?.getHostContext());

  useEffect(() => {
    if (app) setHostContext(app.getHostContext());
  }, [app]);

  if (error) return <p className="notice notice-error">{error.message}</p>;
  if (!app || !opened) return <Skeleton />;
  return <Shell app={app} hostContext={hostContext} />;
}

function Shell({ app, hostContext }: { app: App; hostContext?: McpUiHostContext }) {
  const fullscreen = hostContext?.displayMode === "fullscreen";
  const insets = hostContext?.safeAreaInsets;
  return (
    <main
      className={fullscreen ? "app app-fullscreen" : "app"}
      style={{ paddingTop: insets?.top, paddingRight: insets?.right, paddingLeft: insets?.left }}
    >
      <header className="header">
        <img className="logo" src="https://zernio.com/icon.svg?v=4" alt="" width={18} height={18} />
        <span className="type-page-title">Zernio</span>
      </header>
      <Home
        app={app}
        fullscreen={fullscreen}
        canExpand={!fullscreen && !!hostContext?.availableDisplayModes?.includes("fullscreen")}
        locale={hostContext?.locale}
      />
    </main>
  );
}

function Skeleton() {
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
