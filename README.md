# Dawnshard Reader（Dawnshard Reader技能包 / Snippet Reader skills）

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

Verified with codex-cli 0.151.0 (no login needed): `codex debug prompt-input` lists all seven skills from `.agents/skills`, `~/.agents/skills` and `~/.codex/skills`.

## 快速開始 / Quick start

1. 「幫我設定Dawnshard Reader」/ "Set up Snippet Reader" → runs getting-started.
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
