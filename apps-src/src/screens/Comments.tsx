/** A post's comments: each comment with its own reply box when it can be answered. */
import { ArrowLeft } from "pixelarticons/react/ArrowLeft.js";
import { Message } from "pixelarticons/react/Message.js";
import { useState } from "react";
import { type Comment, type CommentsData, formatDate } from "../api";
import { Badge, Button, Empty, Notice, ReplyBox, Section } from "../ui";
import type { Ctx } from "./context";

export function Comments({ ctx, data }: { ctx: Ctx; data: CommentsData }) {
  const [open, setOpen] = useState<string>();
  const [replied, setReplied] = useState<string[]>([]);
  const title = (data.post.text || "").split("\n")[0] || "Post";

  const reply = async (comment: Comment, text: string) => {
    const result = await ctx.act("comments_reply_to_inbox_post", { post_id: data.postId, account_id: data.accountId, message: text, comment_id: comment.id });
    if (!result.ok) return result.text || "The reply was not sent.";
    setReplied((list) => [...list, comment.id]);
    setOpen(undefined);
    ctx.tell(`From the Zernio app the user replied to comment ${comment.id} on post ${data.postId}: "${text}"`);
    return undefined;
  };

  return (
    <>
      <div className="back">
        <Button variant="ghost" size="sm" onClick={() => ctx.navigate("inbox")}><ArrowLeft className="icon" /> Inbox</Button>
      </div>
      <Section
        title={title}
        count={data.comments.length}
        actions={data.post.permalink ? <Button variant="link" size="sm" onClick={() => void ctx.app.openLink({ url: data.post.permalink! })}>View post</Button> : undefined}
      >
        {data.comments.length ? (
          <ol className="thread">
            {data.comments.map((c) => {
              const author = c.from.name || (c.from.username ? `@${c.from.username}` : "Someone");
              return (
                <li key={c.id} className="message">
                  <div className="message-meta">
                    <span className="type-label">{author}</span>
                    {c.from.isOwner && <Badge>You</Badge>}
                    <span className="row-secondary">{formatDate(c.createdTime, ctx.locale)}</span>
                    {!!c.replyCount && <span className="row-secondary">· {c.replyCount} replies</span>}
                    <span className="message-actions">
                      {replied.includes(c.id) ? (
                        <span className="row-secondary">Replied</span>
                      ) : c.canReply !== false && !c.from.isOwner ? (
                        <Button size="sm" variant="ghost" onClick={() => setOpen(open === c.id ? undefined : c.id)}>Reply</Button>
                      ) : null}
                    </span>
                  </div>
                  <p className="message-body">{c.isHidden ? <span className="row-secondary">Hidden</span> : c.message || <span className="row-secondary">No text</span>}</p>
                  {open === c.id && (
                    <ReplyBox
                      placeholder={`Reply to ${author}`}
                      onSend={(text) => reply(c, text)}
                      onDraft={() => ctx.ask(`Draft a reply to ${author}'s comment "${c.message ?? ""}" on my post (post_id ${data.postId}, account_id ${data.accountId}, comment_id ${c.id}).`)}
                    />
                  )}
                </li>
              );
            })}
          </ol>
        ) : (
          <Empty icon={<Message className="icon" />}>No comments on this post yet.</Empty>
        )}
      </Section>
      {data.comments.length > 0 && data.comments.every((c) => c.canReply === false) && <Notice tone="muted">This platform does not allow replies from the API.</Notice>}
    </>
  );
}
