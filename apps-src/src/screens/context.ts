/** What every screen gets from the app: the host, navigation and actions. */
import type { App } from "@modelcontextprotocol/ext-apps";
import type { View } from "../api";

export interface ActResult {
  ok: boolean;
  text: string;
  data?: unknown;
}

export interface Ctx {
  app: App;
  locale?: string;
  fullscreen: boolean;
  navigate(view: View, args?: Record<string, unknown>): void;
  /** Calls a write tool for a button; the host asks the user to approve it. */
  act(tool: string, args: Record<string, unknown>): Promise<ActResult>;
  /** Hands a task that needs judgement to the chat, in the user's voice. */
  ask(text: string): void;
  /** Tells Claude what just happened on screen, without a chat message. */
  tell(text: string): void;
}
