// Railway Infrastructure as Code for the hosted MCP server (mcp.zernio.com).
// Replaces railway.toml (Config as Code stops being read on 2026-12-01).
// Railway does not read this file at deploy time: `railway config plan` and
// `railway config apply` push it to the linked environment.
import { defineRailway, github, preserve, project, service } from "railway/iac";

// GitHub source per environment, as connected today. Omitting it disconnects
// the repo, and pushes stop deploying. dev tracks whichever branch is under test.
const SOURCES: Record<string, ReturnType<typeof github>> = {
  production: github("zernio-dev/zernio-python", { branch: "develop" }),
  dev: github("zernio-dev/zernio-python", {
    branch: "chore/railway-eu-replicas",
  }),
  "zernio-mcp-dev": github("zernio-dev/zernio-mcp", { checkSuites: true }),
};

// Variables stay managed in Railway; preserve() keeps the current values.
const VARIABLES: Record<string, string[]> = {
  production: [
    "AXIOM_DATASET",
    "AXIOM_TOKEN",
    "PORT",
    "RAILWAY_DEPLOYMENT_DRAINING_SECONDS",
    "SENTRY_DSN",
    "SENTRY_TRACES_SAMPLE_RATE",
    "WEB_CONCURRENCY",
    // Turns on the MCP App (src/late/mcp/apps): interactive views in Claude and ChatGPT.
    "ZERNIO_MCP_APPS",
  ],
  "zernio-mcp-dev": ["MCP_PUBLIC_URL", "PORT", "SENTRY_DSN"],
  dev: ["MCP_PUBLIC_URL", "PORT", "ZERNIO_MCP_APPS"],
};

export default defineRailway((ctx) => {
  const environment = ctx.environment ?? "";
  const env = Object.fromEntries(
    (VARIABLES[environment] ?? []).map((name) => [name, preserve()]),
  );

  // The service instance itself is set to Railpack with no health check, so
  // the builder, Dockerfile path and health check must be explicit here.
  // No start command: it would override the Dockerfile CMD.
  const mcpServer = service("mcp-server", {
    source: SOURCES[environment],
    build: {
      builder: "DOCKERFILE",
      dockerfilePath: "Dockerfile",
    },
    // /health returns 503 until every WEB_CONCURRENCY worker is up.
    healthcheck: "/health",
    healthcheckTimeout: 100,
    // Restart policy type is ON_FAILURE, Railway's default (stored as null, so
    // setting it here shows as a change on every plan).
    deploy: {
      restartPolicyMaxRetries: 3,
      // EU West (Amsterdam), next to the Zernio API. Streamable HTTP runs
      // stateless, so replicas need no sticky sessions. Railway merges region
      // maps, so a region we leave must be set to null (0 is rejected); the
      // `replicas` shorthand cannot express that.
      multiRegionConfig: {
        "europe-west4": { numReplicas: environment === "production" ? 2 : 1 },
        "us-west2": null,
      },
    },
    domains:
      environment === "production"
        ? [{ domain: "mcp.zernio.com", port: 8080 }]
        : [],
    env,
  });

  return project("zernio-mcp", {
    resources: [mcpServer],
  });
});
