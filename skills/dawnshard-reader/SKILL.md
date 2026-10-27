---
name: dawnshard-reader
description: Entry point and session mode for Dawnshard Reader (Dawnshard Reader / Snippet Reader). Use when the user types $dawnshard-reader or /Dawnshard-reader, says Dawnshard Reader / Snippet Reader / reading mode, OR when reading mode is already on in this conversation and the user sends any follow-up - a link or pasted text, an A/B/C or short answer, reread, next, shelve, dashboard, points or streak.
---
# Dawnshard Reader session mode

Trigger once per conversation. From then on, every later message in this conversation is handled under the Snippet Reader rules until the user ends the mode. The user never has to type the skill name again.

## Entering
1. Say in one line that reading mode is on and how to leave it ("結束 Dawnshard Reader" / "exit reading mode").
2. No `settings.json` in the data folder yet: run `snippet-reader-getting-started`. Otherwise resume: send the next slice of the article in progress, or ask for an article.

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
