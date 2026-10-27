---
name: dawnshard-reader
description: Entry point and session mode for Dawnshard Reader (Dawnshard Reader / Snippet Reader). Use when the user types $dawnshard-reader or /Dawnshard-reader, says Dawnshard Reader / Snippet Reader / reading mode, OR when reading mode is already on in this conversation and the user sends any follow-up - a link or pasted text, an A/B/C or short answer, reread, next, shelve, dashboard, points or streak.
---
> **Hard rule / 硬規則 — options first / 選項優先**
> Every point that needs a user decision offers numbered options (1/2/3 menu or buttons). Free typing only where unavoidable (URL, account, folder path), and every such prompt also offers `0. 略過，之後再說 / skip, do it later`. Never ask open-ended questions.
> 每個需要使用者決定的地方都給編號選項；只有網址、帳號、路徑等無法避免時才請使用者打字，且一定附「0. 略過，之後再說」。不問開放式問題。

## FIRST REPLY on first use — literal template (MANDATORY) / 首次使用的第一則回覆

If `.snippet-reader/settings.json` does not exist, your FIRST reply is exactly this menu (translate only if the user writes in another language). Do not ask anything else first — not slice length, not goals.

```
Dawnshard Reader 閱讀模式已開啟（說「結束 Dawnshard Reader」離開）。
步驟 1/6：安裝位置
1. 全域安裝 ~/.agents/skills（建議）
2. 只裝在這個專案 .agents/skills
3. 已經裝好了
0. 略過，之後再說
請回覆數字。
```

Then show each next step as ONE numbered menu per reply, in this order, after the user answers (any answer, including 0, moves to the next step):
- 步驟 2/6 每片長度: `1. 3 分鐘` `2. 5 分鐘（建議）` `3. 10 分鐘` `0. 略過，之後再說`
- 步驟 3/6 推送時間 08:00 / 12:30 / 20:30，勿擾 21:00–06:00: `1. 用預設` `2. 只要早上 08:00` `3. 不要推送` `0. 略過，之後再說`
- 步驟 4/6 來源: `1. RSS` `2. 本機資料夾` `3. 電子報` `4. 電子郵件` `0. 略過，之後再說`. If they pick 1–4 and a URL/path is needed, ask for it with `0. 略過，之後再說` also listed. On failure: `1. 重試` `2. 換一個來源` `3. 改用資料夾` `0. 略過，之後再說`
- 步驟 5/6 第一篇文章: `1. 貼上網址` `2. 從已連線來源挑一篇` `3. 用範例文章` `0. 略過，之後再說`
- 步驟 6/6 第一片: show slice 1 with question options `1.` `2.` `3.` plus `4. 再看一次` `0. 略過，之後再說`
Every menu ends with 「請回覆數字。」 Never end a turn with an open-ended question.

# Dawnshard Reader session mode

Trigger once per conversation. From then on, every later message in this conversation is handled under the Snippet Reader rules until the user ends the mode. The user never has to type the skill name again.

## Entering
1. Say in one line that reading mode is on and how to leave it ("結束 Dawnshard Reader" / "exit reading mode").
2. No `settings.json` in the data folder yet: walk one beat at a time, in order: first run → sources → first article → first slice → dashboard. Do not batch beats. If the user shares an article mid-walk, stop setup and slice it, then continue at the first-slice beat. Close every beat with 下一步 / What's next and 成功的樣子 / Success looks like, in the user's language, then wait.
   - **First run.** `snippet-reader-getting-started` items 1, 2, 4, 5, and 6: one-line purpose, slice length, create the data folder, offer the schedule (08:00, 12:30, 20:30, quiet hours 21:00–06:00, weekly recap Sunday 20:00 only if they agree), optional persona. Leave sources to the next beat; "none for now" is fine. What's next: connect a source, or the first article if they skipped sources or already have something to read. Success looks like: `.snippet-reader/settings.json`, `state.json`, and `dashboard.html` exist, and `python3 ~/.agents/skills/snippet-reader-dashboard/scripts/validate_state.py .snippet-reader/state.json` prints OK (repo install: `.agents/skills/.../validate_state.py`).
   - **Sources.** One source at a time, using `snippet-reader-getting-started` step 3. What's next: another source, or the first article. Success looks like: the read-only test listed the latest 3 items, or the user skipped.
   - **First article.** A pasted link, a pick from the source list, or pasted text. Slice it (`snippet-reader-slicing`; long video or podcast: `snippet-reader-video-slicing`). Store title, link, and progress only. If it came from the source test, set `is_new: true`. What's next: answer the one question on slice 1. Success looks like: slice 1 is on screen with one A/B/C question.
   - **First slice.** `snippet-reader-quiz` for slice 1 only. Wrong: re-read with a hint, retry, no penalty. Right: points stay on the dashboard. During this first-run walk, do not send slice 2 in that same message. What's next: open the dashboard. They can say 「下一片」 / next for slice 2, or 「擱置」 / shelve to pause. Success looks like: slice 1 has been answered.
   - **Dashboard.** Tell them how to open it (`snippet-reader-dashboard`): `python3 ~/.agents/skills/snippet-reader-dashboard/scripts/serve_dashboard.py .snippet-reader` then http://localhost:8765/dashboard.html (repo install: `.agents/skills/.../serve_dashboard.py`), or open `dashboard.html` and use 「選擇 state.json」. What's next: the schedule if they skipped it, then keep reading. A new conversation starts with `$dawnshard-reader` again. Success looks like: the dashboard shows the article, the points, and streak day 1.
3. Settings already exist: resume. Send the next slice of the article in progress, or ask for an article.

## While the mode is on, route each message
| User message | Do |
|---|---|
| link, X post, pasted text, newsletter | `snippet-reader-slicing` (long video/podcast: `snippet-reader-video-slicing`) |
| an answer: A/B/C, a letter, a short answer to the last question | `snippet-reader-quiz` |
| "reread", "再看一次", "show it again" | `snippet-reader-quiz` (re-read) |
| "next", "繼續", "下一片" | next slice (only if the current one is answered) |
| "shelve", "擱置", "resume" | `snippet-reader-points` (shelved) |
| dashboard, progress, points, streak, badges, list | `snippet-reader-dashboard` |
| schedule, push times, imports, recap | `snippet-reader-daily-push` |
| anything else | answer briefly, then return to reading |

Open the sub-skill's `SKILL.md` (sibling folders, e.g. `../snippet-reader-quiz/SKILL.md`) the first time you need it in this conversation; reuse it after that.

## Keeping the mode
- Treat the mode as on for the rest of the conversation even if it is long. If earlier context was compacted and this file is no longer visible, re-open it; the reading-mode rule in `AGENTS.md` (if installed) keeps the mode on.
- Conversation rules from `AGENTS.md` apply: reply in the user's language, reading only in the chat, all stats on the dashboard.

## Leaving
On "結束 Dawnshard Reader", "exit reading mode", "stop", or a clearly unrelated task the user says to switch to: reply one line, and stop routing. A new conversation starts with the mode off.

## Option menus for first run / 首次使用選單

- Install / 安裝: `1. 全域 ~/.agents/skills` · `2. 只裝在這個專案 .agents/skills` · `0. 略過`
- Push times / 推送時間 (08:00 / 12:30 / 20:30): `1. 保留預設` · `2. 調整` · `0. 之後再說`
- Quiet hours / 勿擾 (21:00–06:00): `1. 保留` · `2. 調整` · `0. 之後再說`
- Source / 來源: `1. RSS` · `2. 本機資料夾` · `3. 電子報` · `4. 電子郵件` · `0. 之後再說`
- Connection failed / 連線失敗: `1. 重試` · `2. 換一個來源` · `3. 改用資料夾` · `0. 略過`
- First article / 第一篇: `1. 貼上網址` · `2. 從已連線來源挑` · `3. 用範例文章` · `0. 略過`
- First segment / 第一段: `1. 確認` · `2. 調整長度` · `0. 略過`
- Quiz / 測驗: answer `1–4`, or `5. 看答案` · `0. 跳過`
