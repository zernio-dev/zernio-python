/**
 * Post preview: the post as it will go out, the account each platform reaches,
 * validation, and Publish now (two steps) or Save as draft.
 */
import { Image } from "pixelarticons/react/Image.js";
import { Video } from "pixelarticons/react/Video.js";
import { useState } from "react";
import { platformName, type PreviewData } from "../api";
import { Button, Notice, PlatformTile, Row, Rows, Section, StatusPill } from "../ui";
import type { Ctx } from "./context";

type Outcome = { ok: boolean; text: string };

export function Preview({ ctx, data }: { ctx: Ctx; data: PreviewData }) {
  const [confirming, setConfirming] = useState(false);
  const [busy, setBusy] = useState<"publish" | "draft" | null>(null);
  const [outcome, setOutcome] = useState<Outcome>();
  const errors = data.validation?.errors ?? [];
  const warnings = data.validation?.warnings ?? [];
  const unresolved = data.targets.filter((t) => t.error);
  const blocked = unresolved.length > 0 || data.validation?.valid === false;
  const length = Array.from(data.content).length;

  const submit = async (mode: "publish" | "draft") => {
    setBusy(mode);
    setConfirming(false);
    const result = await ctx.act("posts_cross_post", { ...data.request, ...(mode === "publish" ? { publish_now: true } : { is_draft: true }) });
    // posts_cross_post reports account problems as text starting with ❌.
    const ok = result.ok && !result.text.trim().startsWith("❌");
    setOutcome({ ok, text: result.text });
    setBusy(null);
    ctx.tell(
      ok
        ? `From the Zernio app the user ${mode === "publish" ? "published" : "saved as a draft"} the previewed post. ${result.text}`
        : `Submitting the previewed post from the Zernio app failed. ${result.text}`,
    );
  };

  return (
    <>
      <Section title="Post" actions={<span className="row-secondary">{length} characters</span>}>
        <p className="post-body">{data.content}</p>
        {data.media.length > 0 && (
          <div className="media">
            {data.media.slice(0, 4).map((m, i) =>
              m.type === "image" ? (
                <img key={i} src={m.url} alt={`Attached image ${i + 1}`} loading="lazy" />
              ) : (
                <span key={i} className="media-tile" title={m.url}>
                  {m.type === "video" ? <Video className="icon" /> : <Image className="icon" />}
                </span>
              ),
            )}
          </div>
        )}
      </Section>

      <Section title="Goes out to" count={data.targets.length}>
        <Rows>
          {data.targets.map((t, i) => (
            <Row
              key={i}
              lead={<PlatformTile platform={t.platform} />}
              name={platformName(t.platform)}
              secondary={t.handle ? `@${t.handle}` : undefined}
              state={t.error ? <StatusPill label="Pick an account" tone="danger" reason={t.error} /> : <StatusPill label="Ready" tone="success" />}
              fix={
                t.error ? (
                  <Button size="sm" onClick={() => ctx.ask(`Preview this post again for ${platformName(t.platform)}: I'll tell you which account. ${t.error}`)}>
                    Ask Claude
                  </Button>
                ) : undefined
              }
            />
          ))}
        </Rows>
      </Section>

      {errors.map((e, i) => <Notice key={`e${i}`} tone="danger">{e.platform ? `${platformName(e.platform)}: ` : ""}{e.error}</Notice>)}
      {warnings.map((w, i) => <Notice key={`w${i}`} tone="warning">{w.platform ? `${platformName(w.platform)}: ` : ""}{w.warning}</Notice>)}

      {outcome ? (
        <Notice tone={outcome.ok ? "success" : "danger"}>{outcome.text}</Notice>
      ) : (
        <div className="actions">
          {confirming ? (
            <>
              <Button variant="primary" disabled={!!busy} onClick={() => void submit("publish")}>
                {busy === "publish" ? "Publishing…" : `Publish to ${data.targets.length} ${data.targets.length === 1 ? "platform" : "platforms"} now`}
              </Button>
              <Button onClick={() => setConfirming(false)}>Cancel</Button>
            </>
          ) : (
            <>
              <Button variant="primary" disabled={blocked || !!busy} onClick={() => setConfirming(true)}>Publish now</Button>
              <Button disabled={!!busy} onClick={() => void submit("draft")}>{busy === "draft" ? "Saving…" : "Save as draft"}</Button>
            </>
          )}
        </div>
      )}
    </>
  );
}
