# 逐步指南 / Step-by-step guide

> **Hard rule / 硬規則 — options first / 選項優先**
> Every point that needs a user decision offers numbered options (1/2/3 menu or buttons). Free typing only where unavoidable (URL, account, folder path), and every such prompt also offers `0. 略過，之後再說 / skip, do it later`. Never ask open-ended questions.
> 每個需要使用者決定的地方都給編號選項；只有網址、帳號、路徑等無法避免時才請使用者打字，且一定附「0. 略過，之後再說」。不問開放式問題。

從安裝到第一片，依步驟 0 到步驟 4 做。短版在 README 的「快速開始」。閱讀資料在本機的 `.snippet-reader/`；狀態檔只留標題、連結和進度。

Follow Step 0 through Step 4 from install to the first slice. The short path is Quick start in the README. Reading data stays in local `.snippet-reader/`; state keeps titles, links, and progress only.

## 步驟 0：事前準備 / Step 0: Prerequisites

準備已登入的 Codex CLI，或 ChatGPT／Codex 桌面應用，再加上 git 與 python3（python3 用來開本機儀表板）。沒有字幕的影片才需要 yt-dlp、ffmpeg、Whisper，可以晚一點再裝。

You need a signed-in Codex CLI, or the ChatGPT/Codex desktop app, plus git and python3 (python3 serves the local dashboard). yt-dlp, ffmpeg, and Whisper are only for videos that have no captions; install them later if you need them.

```bash
codex --version
git --version
python3 --version
```

### 失敗時 / If it fails

某個指令不存在就先裝好該工具，再查一次版本。沒有 `codex` 時，用 Codex CLI 或 ChatGPT／Codex 桌面應用。

If a command is missing, install that tool and check the version again. With no `codex` command, use the Codex CLI or the ChatGPT/Codex desktop app.

### 下一步 / What's next

步驟 1。

Step 1.

### 成功的樣子 / Success looks like

三個指令都印出版本。

Each of the three commands prints a version.

## 步驟 1：安裝 / Step 1: Install

Codex 會讀 `.agents/skills`（從目前資料夾往上到 repo 根目錄）和 `~/.agents/skills`（個人、所有專案）。舊路徑 `~/.codex/skills` 仍會讀。

Codex reads `.agents/skills` (from the working directory up to the repo root) and `~/.agents/skills` (user-wide). The legacy path `~/.codex/skills` is still read.

**個人（所有專案）/ user-wide:**

```bash
git clone https://github.com/g0uv4/Dawnshard-reader.git
mkdir -p ~/.agents/skills
cp -r Dawnshard-reader/skills/* ~/.agents/skills/
```

**單一 repo（可選）/ one repo (optional):**

```bash
mkdir -p .agents/skills
cp -r Dawnshard-reader/skills/* .agents/skills/
cp Dawnshard-reader/AGENTS.md ./AGENTS.md
echo ".snippet-reader/" >> .gitignore
```

`AGENTS.md` 讓Dawnshard Reader 閱讀模式在這份專案裡持續生效：同一段對話會一直用這些技能，直到你說「結束 Dawnshard Reader」。裝好後重開 Codex。

`AGENTS.md` keeps reading mode on for that project: the same conversation keeps using these skills until you say "exit reading mode". Restart Codex after installing.

用 `/skills` 查看，或執行 `codex debug prompt-input`（不用登入）。應看到 8 個技能：`dawnshard-reader`，以及 7 個 `snippet-reader-*`（getting-started、slicing、video-slicing、quiz、points、daily-push、dashboard）。

Check with `/skills`, or run `codex debug prompt-input` (no login). You should see 8 skills: `dawnshard-reader`, plus seven `snippet-reader-*` skills (getting-started, slicing, video-slicing, quiz, points, daily-push, dashboard).

### 失敗時 / If it fails

清單裡沒有這些技能時，確認 `ls ~/.agents/skills/*/SKILL.md` 印出 8 個檔案，然後重開 Codex。技能若在 repo 裡，改查 `.agents/skills/*/SKILL.md`。

If the list is missing skills, check that `ls ~/.agents/skills/*/SKILL.md` prints 8 files, then restart Codex. For a repo install, check `.agents/skills/*/SKILL.md` instead.

### 下一步 / What's next

步驟 2。輸入 `$dawnshard-reader`。

Step 2. Type `$dawnshard-reader`.

### 成功的樣子 / Success looks like

`/skills` 或 `codex debug prompt-input` 列出 8 個技能。

`/skills` or `codex debug prompt-input` lists 8 skills.

## 步驟 2：第一次執行 / Step 2: First run

1. 輸入 `$dawnshard-reader`（說「Dawnshard Reader」也會進入）。代理用一行說明Dawnshard Reader 閱讀模式已開啟，以及離開方式：「結束 Dawnshard Reader」／"exit reading mode"。同一段對話之後都算Dawnshard Reader 閱讀模式，新對話要再輸入一次。
2. 還沒有 `settings.json` 時，代理一次只問一件事：
   - 切片長度：預設約 1 分鐘，或 30 秒、3 分鐘、自訂。
   - 來源：細節在步驟 3。可以先說「現在沒有」。
   - 建立 `.snippet-reader/`。`settings.json` 的 `data_dir` 寫絕對路徑，並放上空的 `state.json`。同時產生 `dashboard.html`：會先 clone [lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts)（本機已有就重用）並照它的風格產生；沒有網路或 clone 失敗就用技能內建的頁面。本包裝只連結該專案，不收錄它的檔案。
   - 詢問是否要排程。你同意才設定。預設推送 08:00、12:30、20:30（你的時區），安靜時段 21:00–06:00，每週回顧為週日 20:00（寫在儀表板上）。
   - 語氣可選。想要的話存進 `settings.persona`，只在收尾多一句。
3. 儀表板檔案這一步會產生。打開它是步驟 4。

1. Type `$dawnshard-reader` (saying Dawnshard Reader also enters). The agent replies in one line that reading mode is on and that you leave with 「結束 Dawnshard Reader」 / "exit reading mode". The rest of this conversation stays in reading mode. A new conversation needs `$dawnshard-reader` again.
2. With no `settings.json` yet, the agent asks one thing at a time:
   - Slice length: about 1 minute by default, or 30 seconds, 3 minutes, or custom.
   - Sources: details are in Step 3. "None for now" is fine.
   - Create `.snippet-reader/`. `data_dir` in `settings.json` is an absolute path, plus an empty `state.json`. It also builds `dashboard.html`: it clones [lieflat-charts](https://github.com/larashero3-dotcom/lieflat-charts) first (or reuses a local copy) and follows that style; with no network or a failed clone, it uses the built-in page. This pack only links to that project and does not include its files.
   - Offer a schedule. It is saved only if you agree. Defaults: pushes at 08:00, 12:30, and 20:30 in your time zone, quiet hours 21:00–06:00, weekly recap Sunday 20:00 (written on the dashboard).
   - Optional tone, saved in `settings.persona`. It only adds a short sign-off.
3. The dashboard file is created here. You open it in Step 4.

### 失敗時 / If it fails

寫不進資料夾時，沙箱需要 workspace-write。改選一個代理寫得進去的 `data_dir`，並在設定裡存它的絕對路徑。

If the folder cannot be written, the sandbox needs workspace-write. Pick a `data_dir` the agent can write, and store that absolute path in settings.

### 下一步 / What's next

步驟 3。你已經有文章、或先不接來源，就直接做步驟 4。

Step 3. If you already have an article, or you skipped sources, go to Step 4.

### 成功的樣子 / Success looks like

`.snippet-reader/settings.json`、`state.json`、`dashboard.html` 都在，而且下面的指令印出 OK。裝在 repo 裡時，把 `~/.agents/skills` 換成 `.agents/skills`。

`.snippet-reader/settings.json`, `state.json`, and `dashboard.html` exist, and the command below prints OK. For a repo install, use `.agents/skills` in place of `~/.agents/skills`.

```bash
python3 ~/.agents/skills/snippet-reader-dashboard/scripts/validate_state.py .snippet-reader/state.json
```

## 步驟 3：選擇並連接來源 / Step 3: Choose and connect sources

來源可選，一次接一個。代理只唯讀，不改你的 feed、資料夾或信箱。不要把密碼或 token 貼到對話裡；代理也不會問、不會存。付費電子報若全文不在你自己的副本裡，只存摘要和連結，並設 `summary_only: true`。

設定裡的 `import_sources[].type` 只用既有的 `rss`、`folder`、`mailbox`、`other`。電子報不是新型別：用 feed、資料夾，或信箱加 `filter`。

Sources are optional. Connect one at a time. The agent only reads; it does not change your feed, folder, or mailbox. Do not paste a password or token into the chat; the agent does not ask for one or store one. For a paid newsletter whose full text is not in your own copy, it keeps the summary and the link and sets `summary_only: true`.

`import_sources[].type` stays the existing set: `rss`, `folder`, `mailbox`, `other`. A newsletter is not a new type: use a feed, a folder, or a mailbox plus a `filter`.

| 你的閱讀從哪來 / You get reading from… | 用這個 / Use |
|---|---|
| 有 feed 的部落格或網站 / a blog or site with a feed | RSS（最簡單，不用登入）/ RSS (easiest, no login) |
| 匯出的 .eml、.html、.md、.txt，或存下來的文章 / exported .eml, .html, .md, .txt, or saved articles | 本機資料夾 / a local folder |
| 收件匣裡的電子報 / a newsletter in your inbox | 電子報自己的 RSS，或轉寄／匯出到資料夾，或已接好的郵件工具加 filter / the newsletter's own RSS, or forward/export into a folder, or a mail tool you already set up plus a filter |
| 一般信箱 / a general mailbox | 電子郵件，而且你已經自己接好郵件工具 / email, and only through a mail tool you already set up |
| 都沒有 / none | 略過，之後自己貼連結 / skip and paste links later |

現在沒有來源就說一聲，直接做步驟 4。

If you have no source yet, say so and go to Step 4.

### 3a RSS

把 feed 網址給代理，寫成下面的 JSON。唯讀測試：抓取 feed，列出最新 3 則標題。

Give the agent the feed URL. It stores the JSON below. Read-only test: fetch the feed and list the latest 3 titles.

```json
{ "type": "rss", "location": "<feed url>" }
```

### 失敗時 / If it fails

打開的是一般網頁：到頁面上找 RSS 連結，或試同一個站的 `/feed`、`/rss` 路徑。沙箱擋住網路時，只有你同意才開放網路；不然改貼文章連結。

The page is ordinary HTML: look for an RSS link on the page, or try a `/feed` or `/rss` path on the same site. If the sandbox blocks the network, allow network only after you agree; otherwise paste the article link.

### 下一步 / What's next

再接一個來源，或進入步驟 4。

Connect another source, or go to Step 4.

### 成功的樣子 / Success looks like

畫面上有最新 3 則標題，這則來源在 `import_sources` 裡。寫進 `state.json` 的項目會標成新的（`is_new: true`），只留標題、連結和進度。

The latest 3 titles are on screen, and the source is in `import_sources`. Items written to `state.json` are marked new (`is_new: true`) with title, link, and progress only.

### 3b 本機資料夾 / Local folder

給一個絕對路徑。代理只讀這個資料夾，並寫成下面的 JSON。唯讀測試：列出最新 3 個檔案和標題。

Give an absolute path. The agent only reads that folder and stores the JSON below. Read-only test: list the newest 3 files and their titles.

```json
{ "type": "folder", "location": "<absolute path>" }
```

### 失敗時 / If it fails

找不到路徑，或路徑在沙箱外面：改給一個代理讀得到的絕對路徑。格式不支援：匯出成 `.html`、`.md`、`.txt` 或 `.eml`。

Path missing, or outside the sandbox: give an absolute path the agent can read. Unsupported format: export as `.html`, `.md`, `.txt`, or `.eml`.

### 下一步 / What's next

再接一個來源，或進入步驟 4。

Connect another source, or go to Step 4.

### 成功的樣子 / Success looks like

最新 3 個檔案和標題列出來了，來源已寫進設定。

The newest 3 files and titles are listed, and the source is saved in settings.

### 3c 電子報 / Newsletter

依這個順序選一種接法：

1. 電子報自己有 feed：用 3a（優先）。
2. 把各期轉寄或匯出到一個資料夾：用 3b。
3. 用你已經接好的郵件工具，並加上 `filter`（寄件者或標籤）：用 3d。

付費內容若只有預告、全文不在你自己的副本裡：設 `summary_only: true`，存摘要和連結。

Pick one, in this order:

1. The newsletter has its own feed: use 3a (preferred).
2. Forward or export issues into a folder: use 3b.
3. Use a mail tool you already set up, plus a `filter` (sender or label): use 3d.

When a paid issue is only a teaser and the full text is not in your own copy: set `summary_only: true` and keep the summary and the link.

唯讀測試：列出最新一期的標題；找得到更多期時，最多列 3 則。

Read-only test: show the latest issue title; if more issues are available, list up to 3.

### 失敗時 / If it fails

只有預告文字：設 `summary_only: true`，或改把全文貼上。

Only teaser text is available: set `summary_only: true`, or paste the full text.

### 下一步 / What's next

再接一個來源，或進入步驟 4。

Connect another source, or go to Step 4.

### 成功的樣子 / Success looks like

看得到最新一期的標題，來源已寫進設定。

The latest issue title is shown, and the source is saved in settings.

### 3d 電子郵件 / Email

只走你已經在自己的代理裡接好的郵件工具、connector 或 MCP，或你自己執行的郵件工具。代理不指定廠商，也不問、不存密碼、應用程式密碼或 token。工具若要求登入，在那個工具裡完成。唯讀測試：搜尋符合 `filter` 的信，列出最新 3 個主旨，不改動信箱。

Use only a mail tool, connector, or MCP you already configured in your own agent, or a mail tool you run yourself. The agent does not name a provider, and it does not ask for or store a password, app password, or token. If the tool asks you to sign in, finish that in the tool. Read-only test: search for mail that matches `filter`, list the latest 3 subjects, and leave the mailbox unchanged.

```json
{ "type": "mailbox", "location": "<connector name>", "filter": "<label, sender, or query>" }
```

### 失敗時 / If it fails

沒有郵件工具：改把信轉寄或匯出到資料夾，回到 3b。工具要求登入：在工具裡完成，不在對話裡貼密碼或 token。結果太多：把 `filter` 縮到標籤、寄件者或更窄的查詢。

No mail tool: forward or export mail into a folder and return to 3b. The tool asks you to sign in: finish that in the tool; do not paste a password or token into the chat. Too many results: narrow `filter` to a label, a sender, or a tighter query.

### 下一步 / What's next

再接一個來源，或進入步驟 4。

Connect another source, or go to Step 4.

### 成功的樣子 / Success looks like

最新 3 個主旨列出來了，這個 mailbox 來源和 `filter` 已寫進設定。

The latest 3 subjects are listed, and the mailbox source plus its `filter` are saved in settings.

### 下一步 / What's next

進入步驟 4。還想加來源就回到 3a–3d。

Go to Step 4. To add another source, return to 3a–3d.

### 成功的樣子 / Success looks like

至少一個來源通過唯讀測試，或你明確先不接來源。

At least one source passed its read-only test, or you explicitly skipped sources for now.

## 步驟 4：第一篇文章與第一片 / Step 4: First article and first slice

1. 貼上連結、從來源清單挑一篇，或貼上正文。
2. 代理切成約一分鐘的切片，狀態檔只存標題、連結和進度，不存全文。它送出第 1 片和一題 A/B/C。
3. 作答。答錯：原段配上提示再讀一次，再答，不扣分。答對：積分只出現在儀表板上。
4. 要第 2 片就說「下一片」或 next（這一片答完才繼續）。要暫停就說「擱置」或 shelve。
5. 用下面的指令打開儀表板，瀏覽器開 http://localhost:8765/dashboard.html 。技能裝在 repo 裡時，把 `~/.agents/skills` 換成 `.agents/skills`。也可以直接開 `dashboard.html`，用頁面上的「選擇 state.json」載入。

1. Paste a link, pick one from the source list, or paste the text.
2. The agent cuts it into slices of about one minute. State stores the title, link, and progress only, not the full text. It sends slice 1 and one A/B/C question.
3. Answer. A wrong answer: re-read the original paragraph with a hint, then retry, with no penalty. A right answer: points show on the dashboard only.
4. For slice 2, say 「下一片」 or next (only after this slice is answered). To pause, say 「擱置」 or shelve.
5. Open the dashboard with the command below, then visit http://localhost:8765/dashboard.html . For a repo install, use `.agents/skills` in place of `~/.agents/skills`. You can also open `dashboard.html` and use 「選擇 state.json」 on the page.

```bash
python3 ~/.agents/skills/snippet-reader-dashboard/scripts/serve_dashboard.py .snippet-reader
```

### 失敗時 / If it fails

付費牆或打不開：把正文貼上。代理不會問密碼。長影片或 Podcast：改走影片切片；先用字幕，沒有字幕再用你本機的 yt-dlp、ffmpeg、Whisper。

Paywall or blocked page: paste the text. The agent does not ask for a password. A long video or podcast: use video slicing; start from captions, and if there are none, use your local yt-dlp, ffmpeg, and Whisper.

### 下一步 / What's next

若步驟 2 略過排程，可以現在補上（08:00、12:30、20:30，安靜時段 21:00–06:00）。然後繼續讀。新對話再輸入 `$dawnshard-reader`。

If you skipped the schedule in Step 2, you can add it now (08:00, 12:30, 20:30, quiet hours 21:00–06:00). Then keep reading. In a new conversation, type `$dawnshard-reader` again.

### 成功的樣子 / Success looks like

第 1 片已作答。儀表板看得到這篇文章、積分，以及連續天數第 1 天。

Slice 1 is answered. The dashboard shows the article, the points, and streak day 1.
