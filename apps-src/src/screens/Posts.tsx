/** Failed posts: every post that did not publish, its reason and Retry. */
import { CheckDouble } from "pixelarticons/react/CheckDouble.js";
import type { PostsData } from "../api";
import { Empty, Rows, Section } from "../ui";
import type { Ctx } from "./context";
import { FailedPostRow } from "./rows";

export function Posts({ ctx, data }: { ctx: Ctx; data: PostsData }) {
  return (
    <Section title="Failed posts" count={data.total}>
      {data.posts.length ? (
        <Rows>{data.posts.map((p) => <FailedPostRow key={p.id} ctx={ctx} post={p} />)}</Rows>
      ) : (
        <Empty icon={<CheckDouble className="icon" />}>Nothing failed to publish.</Empty>
      )}
    </Section>
  );
}
