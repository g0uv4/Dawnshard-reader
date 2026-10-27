# 逐步指南 / Step-by-step guide

> **Hard rule / 硬規則 — options first / 選項優先**
> Every point that needs a user decision offers numbered options (1/2/3 menu or buttons). Free typing only where unavoidable (URL, account, folder path), and every such prompt also offers `0. 略過，之後再說 / skip, do it later`. Never ask open-ended questions.
> 每個需要使用者決定的地方都給編號選項；只有網址、帳號、路徑等無法避免時才請使用者打字，且一定附「0. 略過，之後再說」。不問開放式問題。

一次一個選單，從步驟 1/6 到 6/6。任何回覆（含 0）進入下一步。短版在 README 的「逐步指南」。閱讀資料在本機 `.snippet-reader/`；狀態檔只留標題、連結和進度。需要已登入的 Codex、git、python3。沒有字幕的影片才另需 yt-dlp、ffmpeg、Whisper。

One menu at a time, steps 1/6 through 6/6. Any reply, including 0, moves on. The short form is the step-by-step section in the README. Reading data stays in local `.snippet-reader/`; state keeps titles, links, and progress only. You need a signed-in Codex, git, and python3. yt-dlp, ffmpeg, and Whisper are only for video with no captions.

編號選單以「請回覆數字。」結尾。網址、路徑、帳號的那一行改為「……，或回覆 0 略過。」，那一行不要寫「請回覆數字。」。

Numbered menus end with 「請回覆數字。」. A URL, path, or account line ends with 「……，或回覆 0 略過。」. That line does not say 「請回覆數字。」.

## 步驟 1/6：安裝位置 / Step 1/6: Install location

```
步驟 1/6：安裝位置
1. 全域安裝 ~/.agents/skills（建議）
2. 只裝在這個專案 .agents/skills
3. 已經裝好了
0. 略過，之後再說
請回覆數字。
```

1 複製到 `~/.agents/skills`。2 複製到 `.agents/skills`，並把 `.snippet-reader/` 寫進 `.gitignore`。3 表示已裝好。0 先不裝。新安裝後重開 Codex。用 `/skills` 或 `codex debug prompt-input` 應看到 8 個技能。

1 copies into `~/.agents/skills`. 2 copies into `.agents/skills` and adds `.snippet-reader/` to `.gitignore`. 3 means already installed. 0 skips. Restart Codex after a new install. `/skills` or `codex debug prompt-input` should list 8 skills.

```bash
git clone https://github.com/g0uv4/Dawnshard-reader.git
mkdir -p ~/.agents/skills
cp -r Dawnshard-reader/skills/* ~/.agents/skills/
```

```bash
mkdir -p .agents/skills
cp -r Dawnshard-reader/skills/* .agents/skills/
cp Dawnshard-reader/AGENTS.md ./AGENTS.md
echo ".snippet-reader/" >> .gitignore
```

### 下一步 / What's next

步驟 2/6。

Step 2/6.

### 成功的樣子 / Success looks like

8 個技能已列出，或已選 3／0。

The 8 skills are listed, or you chose 3 or 0.

## 步驟 2/6：每片長度 / Step 2/6: Slice length

```
步驟 2/6：每片長度
1. 3 分鐘
2. 5 分鐘（建議）
3. 10 分鐘
0. 略過，之後再說
請回覆數字。
```

1 寫 180 秒，2 寫 300 秒，3 寫 600 秒，並記入 `length_picks`。0 先留預設。這一步建立 `.snippet-reader/`（`data_dir` 為絕對路徑）、`settings.json`、空的 `state.json`（`version` 1、`points` 0、`articles` []），以及 `dashboard.html`。

1 stores 180 seconds, 2 stores 300, 3 stores 600, and logs `length_picks`. 0 keeps the default for later. This step creates `.snippet-reader/` (`data_dir` is an absolute path), `settings.json`, an empty `state.json` (`version` 1, `points` 0, `articles` []), and `dashboard.html`.

### 下一步 / What's next

步驟 3/6。

Step 3/6.

### 成功的樣子 / Success looks like

`slice_seconds` 已寫入或已略過，且下面指令印出 OK（repo 安裝把 `~/.agents/skills` 換成 `.agents/skills`）。

`slice_seconds` is saved or skipped, and the command below prints OK (repo install: `.agents/skills` in place of `~/.agents/skills`).

```bash
python3 ~/.agents/skills/snippet-reader-dashboard/scripts/validate_state.py .snippet-reader/state.json
```

## 步驟 3/6：推送時間 / Step 3/6: Push times

```
步驟 3/6：推送時間
08:00 / 12:30 / 20:30，勿擾 21:00–06:00
1. 用預設
2. 只要早上 08:00
3. 不要推送
0. 略過，之後再說
請回覆數字。
```

1 存這三個時間與勿擾。2 只存 08:00，勿擾相同。3 不排推送。0 先不設。只有 1 或 2 才寫入排程。

1 stores those three times and quiet hours. 2 stores only 08:00, with the same quiet hours. 3 sets no pushes. 0 skips. Only 1 or 2 writes a schedule.

### 下一步 / What's next

步驟 4/6。

Step 4/6.

### 成功的樣子 / Success looks like

推送設定已存，或已略過。

Push settings are saved, or this step was skipped.

## 步驟 4/6：來源 / Step 4/6: Source

```
步驟 4/6：來源
1. RSS
2. 本機資料夾
3. 電子報
4. 電子郵件
0. 略過，之後再說
請回覆數字。
```

選 1–4 且需要網址、路徑或帳號時，下一則只問一行，不要以「請回覆數字。」結尾：

- RSS 或電子報 feed：「請貼上 RSS 網址，或回覆 0 略過。」
- 資料夾：「請貼上資料夾路徑，或回覆 0 略過。」
- 電子郵件：「請貼上帳號，或回覆 0 略過。」

If they pick 1–4 and a URL, path, or account is required, the next line does not end with 「請回覆數字。」:

- RSS or a newsletter feed: 「請貼上 RSS 網址，或回覆 0 略過。」
- Folder: 「請貼上資料夾路徑，或回覆 0 略過。」
- Email: 「請貼上帳號，或回覆 0 略過。」

唯讀測試列出最新最多 3 則。不改 feed、資料夾或信箱，不問、不存密碼或 token。`type` 只用 `rss`、`folder`、`mailbox`、`other`。電子報不是新型別。付費文只有預告時設 `summary_only: true`。寫入 `state.json` 的項目 `is_new: true`，只留標題、連結、進度。

The read-only test lists at most the latest 3 items. Do not change the feed, folder, or mailbox, and do not ask for or store a password or token. `type` stays `rss`, `folder`, `mailbox`, or `other`. A newsletter is not a new type. A paid teaser sets `summary_only: true`. Items written to `state.json` get `is_new: true` and keep title, link, and progress only.

```json
{ "type": "rss", "location": "<feed url>" }
{ "type": "folder", "location": "<absolute path>" }
{ "type": "mailbox", "location": "<connector name>", "filter": "<label, sender, or query>" }
```

連不上時用這個選單，不要改問開放題：

When the connection fails, use this menu. Do not ask an open question:

```
1. 重試
2. 換一個來源
3. 改用資料夾
0. 略過，之後再說
請回覆數字。
```

選 3 之後改問：「請貼上資料夾路徑，或回覆 0 略過。」

After 3, ask: 「請貼上資料夾路徑，或回覆 0 略過。」

### 下一步 / What's next

再接一個來源，或步驟 5/6。

Another source, or step 5/6.

### 成功的樣子 / Success looks like

唯讀測試列出最多 3 則，或已略過。

The read-only test listed up to 3 items, or this step was skipped.

## 步驟 5/6：第一篇文章 / Step 5/6: First article

```
步驟 5/6：第一篇文章
1. 貼上網址
2. 從已連線來源挑一篇
3. 用範例文章
0. 略過，之後再說
請回覆數字。
```

選 1 的下一則是：「請貼上網址，或回覆 0 略過。」不要寫「請回覆數字。」。選 2 再給最多 3 篇的編號選單，同樣以「請回覆數字。」結尾，並含 `0. 略過，之後再說`。選 3 用範例文章。長影片或 Podcast 改走影片切片。

After 1, the next line is 「請貼上網址，或回覆 0 略過。」. It does not say 「請回覆數字。」. After 2, offer up to 3 titles as a numbered menu that ends with 「請回覆數字。」 and includes `0. 略過，之後再說`. 3 uses the sample article. A long video or podcast uses video slicing.

### 下一步 / What's next

步驟 6/6。

Step 6/6.

### 成功的樣子 / Success looks like

第 1 片和一題在畫面上。

Slice 1 is on screen with one question.

## 步驟 6/6：第一片 / Step 6/6: First slice

```
步驟 6/6：第一片
1. （選項）
2. （選項）
3. （選項）
4. 再看一次
0. 略過，之後再說
請回覆數字。
```

答錯：原段加提示再讀，再答，不扣分。答對：積分在儀表板。同一則不要送第 2 片。

A wrong answer re-reads the paragraph with a hint, then retries, with no penalty. A right answer shows points on the dashboard. Do not send slice 2 in that same message.

```bash
python3 ~/.agents/skills/snippet-reader-dashboard/scripts/serve_dashboard.py .snippet-reader
```

然後開 http://localhost:8765/dashboard.html （repo 安裝改 `.agents/skills`）。或直接開 `dashboard.html`，用「選擇 state.json」。

Then open http://localhost:8765/dashboard.html (repo install: `.agents/skills`). Or open `dashboard.html` and use 「選擇 state.json」.

### 下一步 / What's next

說「下一片」繼續，或補上略過的步驟。新對話再輸入 `$dawnshard-reader`。

Say 「下一片」 to continue, or fill in a skipped step. A new conversation starts with `$dawnshard-reader`.

### 成功的樣子 / Success looks like

第 1 片已作答。儀表板有這篇、積分、連續第 1 天。

Slice 1 is answered. The dashboard shows the article, the points, and streak day 1.
