/** A conversation: the thread, oldest first, and the reply box under it. */
import { ArrowLeft } from "pixelarticons/react/ArrowLeft.js";
import { Mail } from "pixelarticons/react/Mail.js";
import { useState } from "react";
import { type ConversationData, type Message } from "../api";
import { Button, Empty, ReplyBox, Section } from "../ui";
import type { Ctx } from "./context";

function when(value: string | null | undefined, locale?: string): string {
  if (!value) return "";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "" : date.toLocaleString(locale, { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" });
}

export function ConversationView({ ctx, data }: { ctx: Ctx; data: ConversationData }) {
  const [messages, setMessages] = useState<Message[]>(data.messages);
  const contact = messages.find((m) => m.direction === "incoming")?.senderName || "this contact";

  const send = async (text: string) => {
    const result = await ctx.act("ui_send_message", { conversation_id: data.conversationId, account_id: data.accountId, message: text });
    if (!result.ok) return result.text || "The message was not sent.";
    setMessages((list) => [...list, { id: `sent-${Date.now()}`, message: text, direction: "outgoing", senderName: "You", createdAt: new Date().toISOString(), attachments: 0 }]);
    ctx.tell(`From the Zernio app the user replied to ${contact} in conversation ${data.conversationId}: "${text}"`);
    return undefined;
  };

  return (
    <>
      <div className="back">
        <Button variant="ghost" size="sm" onClick={() => ctx.navigate("inbox")}><ArrowLeft className="icon" /> Inbox</Button>
      </div>
      <Section title={contact} count={messages.length}>
        {messages.length ? (
          <ol className="thread">
            {messages.map((m) => (
              <li key={m.id} className={m.direction === "outgoing" ? "message message-out" : "message"}>
                <div className="message-meta">
                  <span className="type-label">{m.direction === "outgoing" ? "You" : m.senderName || "Them"}</span>
                  <span className="row-secondary">{when(m.createdAt, ctx.locale)}</span>
                </div>
                <p className="message-body">
                  {m.isDeleted ? <span className="row-secondary">Deleted</span> : m.message || <span className="row-secondary">{m.attachments ? `${m.attachments} attachment${m.attachments > 1 ? "s" : ""}` : "No text"}</span>}
                </p>
              </li>
            ))}
          </ol>
        ) : (
          <Empty icon={<Mail className="icon" />}>No messages in this conversation yet.</Empty>
        )}
        <ReplyBox
          placeholder={`Reply to ${contact}`}
          onSend={send}
          onDraft={() => ctx.ask(`Draft a reply to ${contact} in my Zernio conversation ${data.conversationId} (account_id ${data.accountId}), based on the last messages.`)}
        />
      </Section>
    </>
  );
}
