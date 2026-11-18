/** The frame around every screen: brand header, progress line, feedback, body. */
import { COPY } from "../copy";
import { h, type Child } from "../dom";
import type { AppState } from "../model";

export function skeleton(): HTMLElement {
  return h(
    "div",
    { class: "skeleton", attrs: { "aria-busy": "true", "aria-label": "Loading" } },
    h("i", { attrs: { style: "width: 100%" } }),
    h("i", { attrs: { style: "width: 80%" } }),
    h("i", { attrs: { style: "width: 60%" } }),
  );
}

export function shell(state: AppState, body: Child): HTMLElement {
  return h(
    "main",
    { class: "app" },
    h(
      "header",
      { class: "header" },
      h("span", { class: "mark", attrs: { "aria-hidden": "true" } }),
      h("span", { class: "brand" }, COPY.brand),
      h("span", { class: "title" }, COPY.title),
    ),
    state.phase === "loading" ? h("div", { class: "progress", attrs: { role: "progressbar", "aria-label": "Refreshing" } }) : null,
    state.feedback
      ? h("div", { class: `notice notice-${state.feedback.tone}`, attrs: { role: state.feedback.tone === "error" ? "alert" : "status" } }, state.feedback.text)
      : null,
    state.error ? h("div", { class: "notice notice-error", attrs: { role: "alert" } }, state.error) : null,
    body,
  );
}
