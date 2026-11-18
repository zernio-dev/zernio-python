/** Inbox: the latest conversations and the posts with comments, each opening its thread. */
import { Mail } from "pixelarticons/react/Mail.js";
import { Message } from "pixelarticons/react/Message.js";
import { formatDate, formatNumber, type InboxData, platformName } from "../api";
import { Button, Empty, Kpis, PlatformTile, Row, Rows, Section, StatusPill } from "../ui";
import type { Ctx } from "./context";

export function Inbox({ ctx, data }: { ctx: Ctx; data: InboxData }) {
  const unread = data.conversations.reduce((sum, c) => sum + (c.unreadCount ?? 0), 0);
  const comments = data.posts.reduce((sum, p) => sum + (p.commentCount ?? 0), 0);
  const shown = ctx.fullscreen ? 15 : 5;
  const n = (v: number) => formatNumber(v, ctx.locale);

  return (
    <>
      <Kpis
        items={[
          { key: "conversations", label: "Conversations", value: n(data.conversations.length) },
          { key: "unread", label: "Unread", value: n(unread) },
          { key: "comments", label: "Comments", value: n(comments) },
        ]}
      />
      <Section title="Messages" count={data.conversations.length}>
        {data.conversations.length ? (
          <Rows>
            {data.conversations.slice(0, shown).map((c) => (
              <Row
                key={c.id}
                lead={<PlatformTile platform={c.platform} />}
                name={c.participantName || (c.isGroup ? "Group" : "Unknown")}
                secondary={c.lastMessage || formatDate(c.updatedTime, ctx.locale)}
                state={c.unreadCount ? <StatusPill label={`${c.unreadCount} unread`} tone="info" /> : undefined}
                fix={
                  <Button size="sm" onClick={() => ctx.navigate("conversation", { conversation_id: c.id, account_id: c.accountId })}>
                    Open
                  </Button>
                }
              />
            ))}
          </Rows>
        ) : (
          <Empty icon={<Mail className="icon" />}>No conversations yet.</Empty>
        )}
      </Section>
      <Section title="Comments" count={data.posts.length}>
        {data.posts.length ? (
          <Rows>
            {data.posts.slice(0, shown).map((p) => (
              <Row
                key={p.id}
                lead={<PlatformTile platform={p.platform} />}
                name={(p.content || "").split("\n")[0] || `${platformName(p.platform)} post`}
                secondary={`${formatNumber(p.commentCount ?? 0, ctx.locale)} comments · ${formatDate(p.createdTime, ctx.locale)}`}
                fix={
                  <Button size="sm" onClick={() => ctx.navigate("comments", { post_id: p.id, account_id: p.accountId })}>
                    Open
                  </Button>
                }
              />
            ))}
          </Rows>
        ) : (
          <Empty icon={<Message className="icon" />}>No comments on your recent posts.</Empty>
        )}
      </Section>
    </>
  );
}
