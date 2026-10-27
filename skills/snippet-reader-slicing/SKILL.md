---
name: snippet-reader-slicing
description: Add an article to the Snippet Reader list and cut it into timed reading slices. Use when the user shares a link, X post or thread, pasted text, or a newsletter is imported. For long videos or podcasts use snippet-reader-video-slicing instead.
---
# Adding and slicing an article

## 1. Fetch
- Link: fetch the full text with the web/fetch tool available; fall back to a browser tool if needed.
- X post/thread: gather the whole same-author thread in order, include quoted posts, follow a link to the full article if the post points to one.
- Images: read visible text. Short video inside a post: use its caption text. Long video/podcast: switch to `snippet-reader-video-slicing`.
- Paywall, login wall, bot check, deleted or protected content: say so and ask the user to paste the text. Never ask for, echo or store passwords; never try to bypass access controls.
- Status `shelved` = the user set it aside on purpose; it doesn't count toward quota or expire, and resumes on request.
- Skip duplicates (same URL or same content hash in `state.json`) and say so.

## 2. Slice length (default 1 minute)
- Manual shares: offer 1 minute (default, first), 30 seconds, 3 minutes, any learned length, and custom. At most 4 presets plus custom.
- Learning: append each pick to `settings.json.length_picks`. A custom length picked 3+ times, or the most frequent pick, becomes `slice_seconds` and moves to the top.
- Imports and scheduled runs use `slice_seconds` without asking.

## 3. Cut
- Reading speed: about 320 characters/min for CJK, 230 words/min for English-like languages (1 minute ≈ 320 CJK characters ≈ 230 words).
- Allow up to 15% overflow rather than an extra cut. Break only between paragraphs, never mid-sentence.
- Header, localized, in bold: `**Source | Title | Slice N/M: subtitle**` (zh-TW: `**來源｜標題｜第 N/M 片：小標**`), then the slice text. End each slice with a one-line hook for the next slice (no spoilers, no false clickbait). A short single post can be one slice.
- Newsletters: leave out expired promo codes, tracking boilerplate and unsubscribe footers; keep a sponsor mention to one short line marked as sponsored.

## Working file (optional, local only)
Before sending, you may write `<data_dir>/cache/<id>-slices.md` so slicing is reviewable and re-reads are exact:
```
source: … | date: … | link: … | note: full text / summary only
rule: ~320 CJK chars (or 230 words) per slice, max +15%
## Slice 1/M | subtitle
(~X chars, ~Y sec)
<original text>
Q: … A) … B) … C) …  Answer: B
```
It contains article text, so it stays in the cache folder: never commit or publish it.

## 4. Store (`state.json`)
- Add an article object: `id`, `title` (X: handle + first line), `url`, `kind: "article"`, `slices_total`, `current_slice`, `added_at`, `opened: false`, `status`, plus per-slice records (see schema).
- `source` (publication/author), `summary_only` when only a summary was available. Never store full text in state. Optionally cache the plain text under `.snippet-reader/cache/<id>.txt` so the current slice's original paragraph can be re-pasted for re-reads; re-fetch if missing.
- If active articles (unread + in progress) are at quota, append to `queue` instead (see `snippet-reader-points`).
- Then send slice 1 and run `snippet-reader-quiz`, and refresh the dashboard (`snippet-reader-dashboard`).
