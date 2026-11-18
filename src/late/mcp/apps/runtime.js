// Zernio MCP App runtime: the MCP Apps (2026-01-26) host bridge every view
// shares. JSON-RPC 2.0 over postMessage with the host window, no dependencies,
// so a view is one self-contained HTML document the host can review.
(function () {
  "use strict";

  var PROTOCOL_VERSION = "2026-01-26";
  var nextId = 1;
  var pending = {};
  var listeners = {};
  var context = {};

  function send(message) {
    message.jsonrpc = "2.0";
    window.parent.postMessage(message, "*");
  }

  function request(method, params) {
    var id = nextId++;
    return new Promise(function (resolve, reject) {
      pending[id] = { resolve: resolve, reject: reject };
      send({ id: id, method: method, params: params || {} });
    });
  }

  function notify(method, params) {
    send({ method: method, params: params || {} });
  }

  function emit(event, payload) {
    (listeners[event] || []).forEach(function (fn) {
      try {
        fn(payload);
      } catch (err) {
        console.error(err);
      }
    });
  }

  // Host notification -> view event.
  var EVENTS = {
    "ui/notifications/tool-input": "input",
    "ui/notifications/tool-input-partial": "partial",
    "ui/notifications/tool-result": "result",
    "ui/notifications/tool-cancelled": "cancelled",
  };

  function applyContext(changed) {
    // host-context-changed carries only the fields that changed.
    context = Object.assign({}, context, changed);
    var root = document.documentElement;
    if (changed.theme === "light" || changed.theme === "dark") {
      root.setAttribute("data-theme", changed.theme);
      root.style.colorScheme = changed.theme;
    }
    var styles = changed.styles || {};
    var variables = styles.variables || {};
    Object.keys(variables).forEach(function (name) {
      if (variables[name] != null) root.style.setProperty(name, variables[name]);
    });
    if (styles.css && styles.css.fonts && !document.getElementById("host-fonts")) {
      var fonts = document.createElement("style");
      fonts.id = "host-fonts";
      fonts.textContent = styles.css.fonts;
      document.head.appendChild(fonts);
    }
    var insets = changed.safeAreaInsets;
    if (insets) {
      ["top", "right", "bottom", "left"].forEach(function (side) {
        root.style.setProperty("--safe-" + side, (insets[side] || 0) + "px");
      });
    }
    if (changed.displayMode) root.setAttribute("data-display-mode", changed.displayMode);
    if (changed.deviceCapabilities && changed.deviceCapabilities.touch) {
      root.setAttribute("data-touch", "");
    }
    emit("context", context);
  }

  window.addEventListener("message", function (event) {
    if (event.source !== window.parent) return;
    var message = event.data;
    if (!message || message.jsonrpc !== "2.0") return;

    if (message.method === undefined) {
      var waiting = pending[message.id];
      if (!waiting) return;
      delete pending[message.id];
      if (message.error) waiting.reject(new Error(message.error.message || "Request failed"));
      else waiting.resolve(message.result || {});
      return;
    }

    var params = message.params || {};
    if (message.id !== undefined) {
      // Requests from the host: ping and teardown are the only ones a view
      // without its own tools receives.
      if (message.method === "ui/resource-teardown") emit("teardown", params);
      if (message.method === "ping" || message.method === "ui/resource-teardown") {
        send({ id: message.id, result: {} });
      } else {
        send({ id: message.id, error: { code: -32601, message: "Method not found" } });
      }
      return;
    }

    if (message.method === "ui/notifications/host-context-changed") applyContext(params);
    else if (EVENTS[message.method]) emit(EVENTS[message.method], params);
  });

  // Reports the document height so the host sizes the inline frame to fit,
  // the same measurement the official SDK's autoResize makes.
  function watchSize() {
    var queued = false;
    var last = "";
    function measure() {
      if (queued) return;
      queued = true;
      requestAnimationFrame(function () {
        queued = false;
        var root = document.documentElement;
        var previous = root.style.height;
        root.style.height = "max-content";
        var height = Math.ceil(root.getBoundingClientRect().height);
        root.style.height = previous;
        var width = Math.ceil(window.innerWidth);
        if (width + "x" + height === last) return;
        last = width + "x" + height;
        notify("ui/notifications/size-changed", { width: width, height: height });
      });
    }
    measure();
    var observer = new ResizeObserver(measure);
    observer.observe(document.documentElement);
    observer.observe(document.body);
  }

  // Tool results reach a view as {structuredContent, content}. Tools that
  // return text still carry it as structuredContent.result, and generated
  // tools' text is compact JSON, so data() unwraps both shapes.
  function textOf(result) {
    var structured = result && result.structuredContent;
    if (structured && typeof structured.result === "string") return structured.result;
    var blocks = (result && result.content) || [];
    return blocks
      .filter(function (block) { return block.type === "text"; })
      .map(function (block) { return block.text; })
      .join("\n");
  }

  function dataOf(result) {
    var structured = result && result.structuredContent;
    if (structured && !(Object.keys(structured).length === 1 && "result" in structured)) {
      return structured;
    }
    try {
      return JSON.parse(textOf(result));
    } catch (err) {
      return null;
    }
  }

  function el(tag, attrs) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (key) {
      var value = attrs[key];
      if (value == null || value === false) return;
      if (key === "text") node.textContent = value;
      else if (key === "class") node.className = value;
      else if (key.slice(0, 2) === "on") node.addEventListener(key.slice(2), value);
      else node.setAttribute(key, value === true ? "" : value);
    });
    for (var i = 2; i < arguments.length; i++) append(node, arguments[i]);
    return node;
  }

  function append(node, child) {
    if (child == null || child === false) return;
    if (Array.isArray(child)) child.forEach(function (c) { append(node, c); });
    else node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
  }

  var PLATFORM_NAMES = {
    twitter: "X", instagram: "Instagram", facebook: "Facebook", linkedin: "LinkedIn",
    tiktok: "TikTok", youtube: "YouTube", threads: "Threads", pinterest: "Pinterest",
    reddit: "Reddit", bluesky: "Bluesky", googlebusiness: "Google Business",
    telegram: "Telegram", snapchat: "Snapchat", discord: "Discord", slack: "Slack",
    whatsapp: "WhatsApp",
  };

  function platformName(platform) {
    return PLATFORM_NAMES[platform] || platform || "Unknown";
  }

  function compact(value) {
    try {
      return new Intl.NumberFormat(context.locale, { notation: "compact", maximumFractionDigits: 1 }).format(value || 0);
    } catch (err) {
      return String(value || 0);
    }
  }

  function date(value, options) {
    if (!value) return "";
    var parsed = new Date(value);
    if (isNaN(parsed)) return String(value);
    try {
      return parsed.toLocaleString(context.locale, Object.assign({ timeZone: context.timeZone }, options));
    } catch (err) {
      return parsed.toLocaleString();
    }
  }

  window.Zernio = {
    on: function (event, fn) {
      (listeners[event] = listeners[event] || []).push(fn);
    },
    connect: function (options) {
      options = options || {};
      return request("ui/initialize", {
        appInfo: { name: "Zernio " + (options.name || "view"), version: "1.0.0" },
        appCapabilities: { availableDisplayModes: options.displayModes || ["inline"] },
        protocolVersion: PROTOCOL_VERSION,
      }).then(function (result) {
        applyContext(result.hostContext || {});
        notify("ui/notifications/initialized");
        watchSize();
        return result;
      });
    },
    context: function () { return context; },
    callTool: function (name, args) {
      return request("tools/call", { name: name, arguments: args || {} });
    },
    openLink: function (url) { return request("ui/open-link", { url: url }); },
    requestDisplayMode: function (mode) { return request("ui/request-display-mode", { mode: mode }); },
    // Posts a message into the chat as the user, for Claude to act on.
    sendMessage: function (text) {
      return request("ui/message", { role: "user", content: [{ type: "text", text: text }] });
    },
    tellModel: function (text) {
      return request("ui/update-model-context", { content: [{ type: "text", text: text }] });
    },
    text: textOf,
    data: dataOf,
    el: el,
    platformName: platformName,
    compact: compact,
    date: date,
  };
})();
