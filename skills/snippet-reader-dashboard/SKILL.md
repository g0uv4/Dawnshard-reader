---
name: snippet-reader-dashboard
description: Build and refresh the Snippet Reader dashboard as a local static HTML file that reads state.json. Use after every answered quiz, added/expired/finished/shelved article, scheduled run, or when the user asks for progress, points, streak, badges or the reading list. Also use for progress questions while Dawnshard reading mode is on.
---
# Reading dashboard (local HTML)

Paths below are relative to this skill's folder. The data folder is `settings.json.data_dir` (default `.snippet-reader/`).

The dashboard is one static file, `<data_dir>/dashboard.html`, that reads `state.json` in the same folder. Refreshing it means updating `state.json` (and `generated_at`); never create a second dashboard.

## First build: visual style
The first time you generate the dashboard HTML for a user:
1. Reuse a local copy of the style reference if one exists (e.g. `~/.cache/lieflat-charts` or a path the user gives); otherwise run
   `git clone --depth 1 https://github.com/larashero3-dotcom/lieflat-charts.git ~/.cache/lieflat-charts`.
2. Read its style rules (its `SKILL.md`, token and preset files) and build `<data_dir>/dashboard.html` in that visual style, using `assets/dashboard.html` as the functional spec: same sections, same `state.json` fields, same i18n keys, file-picker fallback, no build step. Follow that repository's license terms (it is a separate, non-MIT project): do not copy its files into this repo or into anything you publish; the generated dashboard stays on the user's machine.
3. Record the choice in `settings.json.dashboard_style` (`"lieflat-charts"` or `"builtin"`). Later refreshes only update `state.json`; if the HTML must be regenerated, keep the same style.
4. No network, clone fails, or the user declines: copy `assets/dashboard.html` as-is and set `dashboard_style: "builtin"`.

Open it with:
```bash
python3 <this-skill>/scripts/serve_dashboard.py <data_dir>      # http://localhost:8765/dashboard.html
```
or open the file directly and pick `state.json` with the file chooser (browsers block `fetch` from `file://`).
Check data with `python3 <this-skill>/scripts/validate_state.py <data_dir>/state.json` (uses `jsonschema` if installed).

## Role
The dashboard is the only home for everything that is not reading: expiry countdowns, points, level, streak, badges, weekly quest, weekly recap, queue, shelved items, comprehension, new-import marks and share drafts.

## Sections, most urgent first
0. Expiry quests: every unopened article with a 48h countdown bar (warning < 12h, danger < 3h), sorted by time left. Expired items in a small "gone" list. New imports carry a "new" mark.
1. One-sentence state ("2 unread, 1 expires tonight, 40 pts to level 3").
2. Today: slices read today, streak and freeze status, points, level, quota used/total, points to next level.
3. Counts: unread, in progress, done, queued, shelved, gone; comprehension = first-try correct ÷ questions (`state.stats`, else computed from slices).
4. Articles: progress dots per slice, slice N/M, added date, countdown; filter All/Unread/In progress/Done/Queued/Shelved; sort by expiring soon, newest, shortest.
5. Streak, level/points bar, badge wall (locked badges show progress), weekly quest card, weekly recap (slices, articles, points, best moment), share drafts, queue.
6. 7-day reading heatmap when there is history.

## Rules
- Every number comes from `state.json`; unknown shows "—". No demo data in a real user's state.
- Keep `state.locale` and `state.timezone` copied from settings; the page localizes from `state.locale`.
- Empty state: one line saying the list is empty and how to add an article.
- Readable at 360 px; at most one highlighted call-out; no external runtime libraries required to view it.
- Buttons only change the view; progress is saved through the conversation.
