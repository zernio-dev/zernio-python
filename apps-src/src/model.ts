/** The app's state and the shapes of the API data it shows. */

export interface Account {
  accountId: string;
  platform: string;
  username?: string;
  displayName?: string;
  status: "healthy" | "warning" | "error";
  needsReconnect?: boolean;
  issues?: string[];
  disconnectReason?: string | null;
}

export interface AccountsHealth {
  summary?: { total?: number; healthy?: number; warning?: number; error?: number; needsReconnect?: number };
  accounts?: Account[];
}

export interface Feedback {
  tone: "ok" | "error";
  text: string;
}

export interface AppState {
  /** connecting: no data yet (skeleton). loading: refreshing over what is shown. */
  phase: "connecting" | "loading" | "ready";
  health?: AccountsHealth;
  /** undefined when the failed-posts call is not reachable from the app. */
  failedPosts?: number;
  error?: string;
  feedback?: Feedback;
}

export const INITIAL_STATE: AppState = { phase: "connecting" };
