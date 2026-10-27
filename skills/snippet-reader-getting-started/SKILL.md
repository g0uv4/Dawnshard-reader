---
name: snippet-reader-getting-started
description: First-run setup for the Snippet Reader reading coach. Use when a user starts using Snippet Reader, asks to set it up, or no .snippet-reader/settings.json exists yet. Learns slice length and import sources, creates local data files, explains scheduling and the dashboard.
---
# Getting started (first conversation)

Reply in the user's language and locale throughout. Ask one thing at a time. The moment the user shares an article, stop asking and slice it (`snippet-reader-slicing`).

1. One line on what this does: turns long reads (links, pasted text, newsletters, X posts/threads, long videos) into short timed slices, asks one question per slice (a wrong answer lets the user re-read and retry, no penalty), and tracks points and streaks on a local dashboard. The conversation is for reading only.
2. A slice takes about one minute to read by default. Offer: 1 minute (default), 30 seconds, 3 minutes, or custom. Save `slice_seconds` and log the pick in `length_picks`.
3. Ask where newsletters or reports arrive, if anywhere: a folder of exported emails, an RSS feed, a mailbox the agent can read with a tool the user already configured, or none. Record `import_sources`. Import read-only; if only a summary is available (e.g. a paid newsletter whose full text is not in the user's own copy), store summary plus link and set `summary_only: true`.
4. Create the data folder (default `.snippet-reader/`; store its absolute path in `data_dir`) with `settings.json` and an empty `state.json`. Schemas: `references/settings.schema.json`, `references/state.schema.json`; examples: `assets/*.example.json` (all relative to this skill's folder). Copy `locale` and `timezone` into `state.json`. Build the dashboard as described in `snippet-reader-dashboard` (style reference first, built-in file as fallback).
5. Offer scheduled invites (default 08:00, 12:30, 20:30 in the user's time zone, quiet hours 21:00–06:00) and an optional weekly recap run (default Sunday 20:00, writes to the dashboard). Set them up only if the user agrees (`snippet-reader-daily-push`).
6. Optional tone: if the user wants a persona (e.g. a gentle bedtime storyteller who closes the last evening slice with a soft sign-off), save it in `settings.persona`. It never adds chatter beyond that sign-off.
7. Tell the user in one or two sentences what is now automatic and how to open the dashboard, then invite the first article. If they have nothing to read, suggest a few recent unread pieces from their import sources.
