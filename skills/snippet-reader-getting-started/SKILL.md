---
name: snippet-reader-getting-started
description: First-run setup for the Snippet Reader reading coach. Use when a user starts using Snippet Reader, asks to set it up, or no .snippet-reader/settings.json exists yet. Learns slice length and import sources, creates local data files, explains scheduling and the dashboard.
---
> **Hard rule / 硬規則 — options first / 選項優先**
> Every point that needs a user decision offers numbered options (1/2/3 menu or buttons). Free typing only where unavoidable (URL, account, folder path), and every such prompt also offers `0. 略過，之後再說 / skip, do it later`. Never ask open-ended questions.
> 每個需要使用者決定的地方都給編號選項；只有網址、帳號、路徑等無法避免時才請使用者打字，且一定附「0. 略過，之後再說」。不問開放式問題。

# Getting started (first conversation)

Reply in the user's language. One numbered menu per reply. Any answer, including 0, moves to the next step. If the user shares an article mid-walk, stop and slice it (`snippet-reader-slicing`; long video or podcast: `snippet-reader-video-slicing`), then continue at step 6/6.

If reading mode is not announced yet, the first reply starts with `Dawnshard Reader 閱讀模式已開啟（說「結束 Dawnshard Reader」離開）。` and step 1/6 in the same message. Do not ask anything else first. If `dawnshard-reader` already sent step 1/6, do not repeat it.

Every numbered menu ends with 「請回覆數字。」. A URL, path, or account prompt is one line ending with 「……，或回覆 0 略過。」 and does not say 「請回覆數字。」. Do not ask for a persona; save `settings.persona` only if they volunteer one.

On the first step that must persist (step 2/6, even on 0), create `.snippet-reader/` (absolute path in `data_dir`) with `settings.json` and an empty `state.json`: `version` 1, `points` 0, `articles` []. Copy `locale` and `timezone` into `state.json`. Schemas: `references/settings.schema.json`, `references/state.schema.json`; examples: `assets/*.example.json` (paths relative to this skill). Build the dashboard as in `snippet-reader-dashboard` (style reference first, built-in file as fallback).

## 步驟 1/6：安裝位置

```
步驟 1/6：安裝位置
1. 全域安裝 ~/.agents/skills（建議）
2. 只裝在這個專案 .agents/skills
3. 已經裝好了
0. 略過，之後再說
請回覆數字。
```

1 copies this pack's `skills/*` into `~/.agents/skills`. 2 copies into `.agents/skills` and appends `.snippet-reader/` to `.gitignore`. 3 and 0 change nothing. Tell them to restart Codex only after 1 or 2.

下一步 / What's next: 步驟 2/6。

成功的樣子 / Success looks like: 8 skills are listed where they chose, or they skipped.

## 步驟 2/6：每片長度

```
步驟 2/6：每片長度
1. 3 分鐘
2. 5 分鐘（建議）
3. 10 分鐘
0. 略過，之後再說
請回覆數字。
```

Save `slice_seconds`: 1 → 180, 2 → 300, 3 → 600, and append that pick in `length_picks`. On 0, leave `slice_seconds` at 60 and do not log a pick. Do not offer other lengths in this walk.

下一步 / What's next: 步驟 3/6。

成功的樣子 / Success looks like: `settings.json`, `state.json`, and `dashboard.html` exist, and `python3 ~/.agents/skills/snippet-reader-dashboard/scripts/validate_state.py .snippet-reader/state.json` prints OK (repo install: `.agents/skills/.../validate_state.py`).

## 步驟 3/6：推送時間

```
步驟 3/6：推送時間
08:00 / 12:30 / 20:30，勿擾 21:00–06:00
1. 用預設
2. 只要早上 08:00
3. 不要推送
0. 略過，之後再說
請回覆數字。
```

1 saves `push_times` `08:00`, `12:30`, `20:30` and `quiet_hours` `21:00-06:00`. 2 saves only `08:00` with the same quiet hours. 3 saves `push_times` `[]`. 0 changes nothing. Write a schedule only for 1 or 2 (`snippet-reader-daily-push`). Do not add a recap question.

下一步 / What's next: 步驟 4/6。

成功的樣子 / Success looks like: push settings are saved, or they skipped.

## 步驟 4/6：來源

```
步驟 4/6：來源
1. RSS
2. 本機資料夾
3. 電子報
4. 電子郵件
0. 略過，之後再說
請回覆數字。
```

0 goes to step 5/6. For 1–4, if a URL, path, or account is required, ask one line and do not end it with 「請回覆數字。」:

- 1 RSS: 「請貼上 RSS 網址，或回覆 0 略過。」 → `{ "type": "rss", "location": "<feed url>" }`
- 2 folder: 「請貼上資料夾路徑，或回覆 0 略過。」 → `{ "type": "folder", "location": "<absolute path>" }`
- 3 newsletter: prefer its feed and use the RSS line. No feed → folder line, else the account line. Not a new `type`.
- 4 email: 「請貼上帳號，或回覆 0 略過。」 → `{ "type": "mailbox", "location": "<connector name>", "filter": "<label, sender, or query>" }`. If a filter is still required, one line: 「請貼上帳號與篩選（寄件者或標籤），或回覆 0 略過。」

0 on a typing line skips the source. `type` stays `rss`, `folder`, `mailbox`, or `other`. Append to `import_sources` when `settings.json` exists; otherwise remember and write with step 2. Read-only: do not change the feed, folder, or mailbox. Never ask for or store a password, app password, or token. Email only through a mail tool, connector, or MCP the user already configured, or a mail tool they run. Do not name a provider. Sign-in stays inside that tool.

Test: latest 3 titles (folder: newest 3 files; mailbox: 3 subjects matching `filter`; newsletter: latest issue, up to 3). Store title, link, and progress only. Set `is_new: true` when the item is written to `state.json`. If `slices_total` is unknown, show titles now and set `is_new` when sliced. Do not invent a slice count. Paid teaser with no full text in the user's own copy: `summary_only: true`.

On failure, this menu (it does end with 「請回覆數字。」):

```
1. 重試
2. 換一個來源
3. 改用資料夾
0. 略過，之後再說
請回覆數字。
```

1 repeats the test. 2 shows the step 4/6 source menu again. 3 asks 「請貼上資料夾路徑，或回覆 0 略過。」. 0 goes to step 5/6.

下一步 / What's next: 另一個來源，或步驟 5/6。

成功的樣子 / Success looks like: the read-only test listed up to 3 items, or they skipped.

## 步驟 5/6：第一篇文章

```
步驟 5/6：第一篇文章
1. 貼上網址
2. 從已連線來源挑一篇
3. 用範例文章
0. 略過，之後再說
請回覆數字。
```

1 next line: 「請貼上網址，或回覆 0 略過。」. Do not write 「請回覆數字。」 on that line. 2: a menu of up to 3 titles from the connected source, each numbered, plus `0. 略過，之後再說`, ending with 「請回覆數字。」. 3: use the sample article under this skill's `assets/`. Slice with `snippet-reader-slicing` (video or podcast: `snippet-reader-video-slicing`). State keeps title, link, and progress only. From a source test, set `is_new: true`.

下一步 / What's next: 步驟 6/6。

成功的樣子 / Success looks like: slice 1 is on screen with one question.

## 步驟 6/6：第一片

Show slice 1 only (`snippet-reader-quiz`). The menu is the question plus:

```
1. （選項）
2. （選項）
3. （選項）
4. 再看一次
0. 略過，之後再說
請回覆數字。
```

Wrong: re-read with a hint, retry, no penalty. Right: points stay on the dashboard. Do not send slice 2 in this message. 4 re-shows this slice. Then tell them how to open the dashboard: `python3 ~/.agents/skills/snippet-reader-dashboard/scripts/serve_dashboard.py .snippet-reader` and http://localhost:8765/dashboard.html (repo install: `.agents/skills/.../serve_dashboard.py`), or open `dashboard.html` and use 「選擇 state.json」.

下一步 / What's next: 「下一片」, or a skipped schedule. A new conversation starts with `$dawnshard-reader`.

成功的樣子 / Success looks like: slice 1 is answered; the dashboard shows the article, the points, and streak day 1.
