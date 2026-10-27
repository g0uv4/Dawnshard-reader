# Dawnshard Reader（Dawnshard Reader技能包 / Snippet Reader skills）

> **Hard rule / 硬規則 — options first / 選項優先**
> Every point that needs a user decision offers numbered options (1/2/3 menu or buttons). Free typing only where unavoidable (URL, account, folder path), and every such prompt also offers `0. 略過，之後再說 / skip, do it later`. Never ask open-ended questions.
> 每個需要使用者決定的地方都給編號選項；只有網址、帳號、路徑等無法避免時才請使用者打字，且一定附「0. 略過，之後再說」。不問開放式問題。

把長文、電子報、X 串文、長影片／Podcast 切成約一分鐘的「切片」，每片一題閱讀測驗，搭配積分、等級、連續天數、徽章等遊戲化機制，並用一個本機 HTML 儀表板呈現進度。適用 OpenAI Codex（Agent Skills 格式），也適用任何讀得懂 `SKILL.md` 的代理。

Turn long reads (articles, newsletters, X threads, long videos/podcasts) into ~1‑minute **slices**, quiz every slice, gamify progress (points, quota levels, streaks, badges, weekly quests) and show everything on a **local static HTML dashboard**. Written for OpenAI Codex Agent Skills; works with any agent that reads `SKILL.md`.

## Skills

| Skill | 用途 / Purpose |
|---|---|
| `snippet-reader-getting-started` | 首次設定：切片長度、匯入來源、排程、儀表板 / first-run setup |
| `snippet-reader-slicing` | 文章抓取與切片 / fetch & slice articles |
| `snippet-reader-video-slicing` | 影片／Podcast 以字幕切片 / slice video via captions |
| `snippet-reader-quiz` | 每片一題、答錯重讀加提示 / proof-of-reading quiz |
| `snippet-reader-points` | 積分、額度等級、佇列、連續天數、徽章 / gamification |
| `snippet-reader-daily-push` | 每日推送（cron / Codex 自動化）/ scheduled invites |
| `snippet-reader-dashboard` | 產生本機 HTML 儀表板 / local HTML dashboard |

Data lives in local JSON files (`./.snippet-reader/`). Schemas and examples: `skills/snippet-reader-getting-started/{references,assets}/`. Dashboard template and helper scripts: `skills/snippet-reader-dashboard/{assets,scripts}/` — they live inside the skills so they are still there after installation.

## 安裝 / Install

Codex 會掃描 `.agents/skills`（專案內，從目前資料夾往上到 repo 根目錄）與 `~/.agents/skills`（個人）。舊路徑 `~/.codex/skills` 仍可讀但已不建議。
Codex discovers skills in `.agents/skills` (repo, from the working directory up to the repo root) and `~/.agents/skills` (user). `~/.codex/skills` still works but is legacy.

**個人（所有專案）/ user-wide:**
```bash
git clone https://github.com/g0uv4/Dawnshard-reader.git
mkdir -p ~/.agents/skills
cp -r Dawnshard-reader/skills/* ~/.agents/skills/
```

**單一 repo / per repository:**
```bash
mkdir -p .agents/skills
cp -r Dawnshard-reader/skills/* .agents/skills/
cp Dawnshard-reader/AGENTS.md ./AGENTS.md   # optional, then edit
echo ".snippet-reader/" >> .gitignore        # keep reading data out of git
```

重新啟動 Codex；用 `$snippet-reader-slicing` 指名呼叫、輸入 `/skills` 挑選，或直接貼文章連結讓代理自動挑技能。
Restart Codex; invoke explicitly (`$snippet-reader-slicing`), pick via `/skills`, or just paste a link.

Verified with codex-cli 0.151.0 (no login needed): `codex debug prompt-input` lists all eight skills from `.agents/skills`, `~/.agents/skills` and `~/.codex/skills`.

## 一次觸發，整段對話有效 / Trigger once per conversation

輸入 `$dawnshard-reader`（Codex CLI 也可用 `/skills` 選取；說「Dawnshard Reader」也會隱式觸發）就進入Dawnshard Reader 閱讀模式。之後同一對話裡貼文章、回答 A/B/C、說「再看一次」、問儀表板，都不必再輸入技能名，直到你說「結束 Dawnshard Reader」。新對話要再觸發一次。
Codex 機制：技能清單（名稱＋描述）每輪都在脈絡中；選用某技能時才讀入完整 SKILL.md，讀入後留在對話歷史裡。另外每個子技能的 description 都寫了「Dawnshard Reader 閱讀模式中的後續訊息」，搭配 AGENTS.md 的持續規則，脈絡被壓縮後也能接續。若想更穩，把本 repo 的 `AGENTS.md` 放到專案根目錄（Codex 每輪都會讀）。
Type `$dawnshard-reader` once; reading mode then stays on for the whole conversation until you say "exit reading mode". The skill list (names + descriptions) is in context every turn and a loaded SKILL.md stays in the conversation history; follow-up-friendly descriptions plus the AGENTS.md rule cover context compaction. Start a new conversation → trigger again.

## 逐步指南 / Step-by-step guide

一次一個選單，步驟 1/6 到 6/6。任何回覆（含 0）進入下一步。編號選單以「請回覆數字。」結尾。網址、路徑、帳號那一行是「……，或回覆 0 略過。」，不要寫「請回覆數字。」。完整說明見 [docs/GUIDE.md](docs/GUIDE.md)。

One menu at a time, steps 1/6 through 6/6. Any reply, including 0, moves on. Numbered menus end with 「請回覆數字。」. A URL, path, or account line ends with 「……，或回覆 0 略過。」 and does not say 「請回覆數字。」. Full notes: [docs/GUIDE.md](docs/GUIDE.md).

### 中文

步驟 1/6：安裝位置
1. 全域安裝 ~/.agents/skills（建議）
2. 只裝在這個專案 .agents/skills
3. 已經裝好了
0. 略過，之後再說
請回覆數字。
下一步：步驟 2/6。
成功：8 個技能已列出，或已略過。

步驟 2/6：每片長度
1. 3 分鐘
2. 5 分鐘（建議）
3. 10 分鐘
0. 略過，之後再說
請回覆數字。
下一步：步驟 3/6。
成功：`slice_seconds` 已寫入或已略過。

步驟 3/6：推送時間（08:00 / 12:30 / 20:30，勿擾 21:00–06:00）
1. 用預設
2. 只要早上 08:00
3. 不要推送
0. 略過，之後再說
請回覆數字。
下一步：步驟 4/6。
成功：推送設定已存，或已略過。

步驟 4/6：來源
1. RSS
2. 本機資料夾
3. 電子報
4. 電子郵件
0. 略過，之後再說
請回覆數字。
要網址、路徑或帳號時改問一行：「請貼上 RSS 網址，或回覆 0 略過。」／「請貼上資料夾路徑，或回覆 0 略過。」／「請貼上帳號，或回覆 0 略過。」／「請貼上網址，或回覆 0 略過。」
連線失敗：
1. 重試
2. 換一個來源
3. 改用資料夾
0. 略過，之後再說
請回覆數字。
下一步：另一個來源，或步驟 5/6。
成功：唯讀測試列出最多 3 則，或已略過。

步驟 5/6：第一篇文章
1. 貼上網址
2. 從已連線來源挑一篇
3. 用範例文章
0. 略過，之後再說
請回覆數字。
選 1 的下一則：「請貼上網址，或回覆 0 略過。」
下一步：步驟 6/6。
成功：第 1 片和一題在畫面上。

步驟 6/6：第一片
1. （選項）
2. （選項）
3. （選項）
4. 再看一次
0. 略過，之後再說
請回覆數字。
下一步：說「下一片」，或補上略過的步驟。
成功：第 1 片已作答；儀表板有這篇、積分、連續第 1 天。

### English

Step 1/6: Install location
1. User-wide ~/.agents/skills (recommended)
2. This project only, .agents/skills
3. Already installed
0. 略過，之後再說
請回覆數字。
Next: step 2/6.
Success: the 8 skills are listed, or this step was skipped.

Step 2/6: Slice length
1. 3 minutes
2. 5 minutes (recommended)
3. 10 minutes
0. 略過，之後再說
請回覆數字。
Next: step 3/6.
Success: `slice_seconds` is saved, or this step was skipped.

Step 3/6: Push times (08:00 / 12:30 / 20:30, quiet hours 21:00–06:00)
1. Use the defaults
2. Morning 08:00 only
3. No pushes
0. 略過，之後再說
請回覆數字。
Next: step 4/6.
Success: push settings are saved, or this step was skipped.

Step 4/6: Source
1. RSS
2. Local folder
3. Newsletter
4. Email
0. 略過，之後再說
請回覆數字。
When a URL, path, or account is required, one line: 「請貼上 RSS 網址，或回覆 0 略過。」 / 「請貼上資料夾路徑，或回覆 0 略過。」 / 「請貼上帳號，或回覆 0 略過。」 / 「請貼上網址，或回覆 0 略過。」
Connection failed:
1. Retry
2. Switch source
3. Use a folder
0. 略過，之後再說
請回覆數字。
Next: another source, or step 5/6.
Success: the read-only test listed up to 3 items, or this step was skipped.

Step 5/6: First article
1. Paste a URL
2. Pick one from a connected source
3. Use the sample article
0. 略過，之後再說
請回覆數字。
After 1: 「請貼上網址，或回覆 0 略過。」
Next: step 6/6.
Success: slice 1 is on screen with one question.

Step 6/6: First slice
1. (choice)
2. (choice)
3. (choice)
4. Read again
0. 略過，之後再說
請回覆數字。
Next: say 「下一片」, or fill in a skipped step.
Success: slice 1 is answered; the dashboard shows the article, the points, and streak day 1.

## 快速開始 / Quick start

最短路徑如下；逐步說明與失敗時怎麼辦見 [docs/GUIDE.md](docs/GUIDE.md)。
Shortest path below. The full steps and what to do when something fails are in [docs/GUIDE.md](docs/GUIDE.md).

1. `$dawnshard-reader`（或「幫我設定Dawnshard Reader」）→ 進入Dawnshard Reader 閱讀模式，首次會跑設定 / enters reading mode, runs setup the first time.
2. 貼一篇文章連結 / paste an article link → sliced and stored in `.snippet-reader/state.json`.
3. 回答每片的題目 / answer each slice's question.
4. 開儀表板 / open the dashboard:
   ```bash
   python3 ~/.agents/skills/snippet-reader-dashboard/scripts/serve_dashboard.py .snippet-reader   # http://localhost:8765/dashboard.html
   ```
   （也可直接開 `dashboard.html` 並用頁面上的「選擇 state.json」按鈕載入。/ Or open the file directly and use the file picker.)

## 儀表板風格 / Dashboard style

第一次生成儀表板 HTML 時，代理會先 `git clone https://github.com/larashero3-dotcom/lieflat-charts.git`（本機已有就重用），依其視覺風格生成 `dashboard.html`，之後沿用同一風格；沒網路或 clone 失敗就用內建的 `assets/dashboard.html`。本 repo 只連結該專案、不含其任何檔案；它有自己的授權（非 MIT），請依其條款使用。
On first build the agent clones [lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts) (or reuses a local copy), generates the dashboard in that style and keeps it; offline it falls back to the built-in template. This repo only links to that project and includes none of its files; it has its own (non-MIT) license.

## 排程 / Scheduling

See `skills/snippet-reader-daily-push/SKILL.md`: defaults 08:00 / 12:30 / 20:30, quiet hours 21:00–06:00, optional Sunday 20:00 recap. Use a scheduled task in the ChatGPT/Codex desktop app, or cron with `codex exec --skip-git-repo-check -s workspace-write` (exec is read-only by default). The Codex CLI can't create scheduled tasks itself.

## 在 Codex 的限制 / Limits in Codex

- Push delivery: Codex has no built-in chat push; invites go to `<data_dir>/inbox/` or your own `notify_command`.
- Tappable answer buttons depend on the client; otherwise options are typed A/B/C.
- Mailbox imports need a mail tool/connector you configure; paid newsletters give only a summary unless the full text is in your own copy.
- Video without captions needs local yt-dlp, ffmpeg and Whisper.

## 隱私 / Privacy

No accounts, tokens or personal data are included. State files store titles, links and progress only — never full article text.

## License

MIT
