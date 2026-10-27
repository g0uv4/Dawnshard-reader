---
name: snippet-reader-getting-started
description: First-run setup for the Snippet Reader reading coach. Use when a user starts using Snippet Reader, asks to set it up, or no .snippet-reader/settings.json exists yet. Learns slice length and import sources, creates local data files, explains scheduling and the dashboard.
---
> **Hard rule / 硬規則 — options first / 選項優先**
> Every point that needs a user decision offers numbered options (1/2/3 menu or buttons). Free typing only where unavoidable (URL, account, folder path), and every such prompt also offers `0. 略過，之後再說 / skip, do it later`. Never ask open-ended questions.
> 每個需要使用者決定的地方都給編號選項；只有網址、帳號、路徑等無法避免時才請使用者打字，且一定附「0. 略過，之後再說」。不問開放式問題。

# Getting started (first conversation)

Reply in the user's language and locale throughout. Ask one thing at a time. The moment the user shares an article, stop asking and slice it (`snippet-reader-slicing`).

1. One line on what this does: turns long reads (links, pasted text, newsletters, X posts/threads, long videos) into short timed slices, asks one question per slice (a wrong answer lets the user re-read and retry, no penalty), and tracks points and streaks on a local dashboard. The conversation is for reading only.
2. A slice takes about one minute to read by default. Offer: 1 minute (default), 30 seconds, 3 minutes, or custom. Save `slice_seconds` and log the pick in `length_picks`.
3. Sources, one at a time, when the user is ready. They may say "none for now" and paste links later. Ask where reading arrives, recommend from the table, connect, run a read-only test that lists the latest 3 items, and use the fallback when it fails. After each source or a skip, say what is next (another source, or the first article) and what success looks like (the 3 items listed, or an explicit skip).
   | They get reading from… | Recommend |
   |---|---|
   | a blog or site with a feed | `rss` (easiest, no login) |
   | exported or saved files (.eml, .html, .md, .txt) | `folder` |
   | a newsletter | its own feed (`rss`) if it has one; else a folder of forwarded or exported issues (`folder`); else `mailbox` with `filter` (sender or label) |
   | a general mailbox | `mailbox`, only if a mail tool is already configured |
   | nowhere | skip |
   - Record the source in `import_sources`. `type` stays `rss`, `folder`, `mailbox`, or `other`. Do not add a type. A newsletter is `rss`, `folder`, or `mailbox` plus a `filter`.
   - If `settings.json` is not written yet, remember the source and write it in item 4. If it exists, append now.
   - Read-only: do not change the feed, folder, or mailbox. Never ask for or store a password, app password, or token.
   - Email only through a mail tool, connector, or MCP the user already configured, or a mail tool they run themselves. Do not name a provider. Do not put credentials in chat. If the tool needs sign-in, the user finishes that in the tool.
   - Store title, link, and progress only. When an item is written into `state.json`, set `is_new: true`. If `slices_total` is not known yet, show the titles now and set `is_new` when the item is sliced. Do not invent a slice count.
   - Paid newsletter whose full text is not in the user's own copy: store the summary plus the link and set `summary_only: true`.
   - **rss.** Connect `{ "type": "rss", "location": "<feed url>" }`. Test: fetch the feed, list the latest 3 titles. Fails: the URL is HTML, not a feed → look for a feed link on the page or a `/feed` or `/rss` path; the sandbox blocks network → allow network only if the user agrees (flag in `snippet-reader-daily-push`), otherwise they paste links.
   - **folder.** Connect `{ "type": "folder", "location": "<absolute path>" }`, read-only. Test: list the newest 3 files and their titles. Fails: path missing or outside the sandbox → an absolute path the sandbox can read; unsupported format → export as `.html`, `.md`, `.txt`, or `.eml`.
   - **newsletter.** Use the rss, folder, or mailbox steps above. Prefer the newsletter's feed. Paid teaser only: `summary_only: true`, or ask the user to paste. Test: latest issue title, up to 3 issues when more exist.
   - **mailbox.** Connect `{ "type": "mailbox", "location": "<connector name>", "filter": "<label, sender, or query>" }`. Test: read-only search, latest 3 subjects that match `filter`. Fails: no mail tool → folder of exported or forwarded mail (folder steps); too many hits → narrow `filter`.
4. Create the data folder (default `.snippet-reader/`; store its absolute path in `data_dir`) with `settings.json` and an empty `state.json`. Include `import_sources` already chosen in item 3, or `[]` when the user skipped. Empty state means `version` 1, `points` 0, and `articles` [] — no articles yet, not a blank file. Schemas: `references/settings.schema.json`, `references/state.schema.json`; examples: `assets/*.example.json` (all relative to this skill's folder). Copy `locale` and `timezone` into `state.json`. Build the dashboard as described in `snippet-reader-dashboard` (style reference first, built-in file as fallback).
5. Offer scheduled invites (default 08:00, 12:30, 20:30 in the user's time zone, quiet hours 21:00–06:00) and an optional weekly recap run (default Sunday 20:00, writes to the dashboard). Set them up only if the user agrees (`snippet-reader-daily-push`).
6. Optional tone: if the user wants a persona (e.g. a gentle bedtime storyteller who closes the last evening slice with a soft sign-off), save it in `settings.persona`. It never adds chatter beyond that sign-off.
7. Tell the user in one or two sentences what is now automatic and how to open the dashboard, then invite the first article. If they have nothing to read, suggest a few recent unread pieces from their import sources.
