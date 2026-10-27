---
name: snippet-reader-quiz
description: Proof-of-reading quiz for Snippet Reader. Use right after sending a slice: ask one question, praise a correct answer, re-paste the paragraph with escalating hints on a wrong answer, handle "show it again" re-read requests, and unlock the next slice. Also use for any A/B/C or short answer while Dawnshard reading mode is on.
---
> **Hard rule / 硬規則 — options first / 選項優先**
> Every point that needs a user decision offers numbered options (1/2/3 menu or buttons). Free typing only where unavoidable (URL, account, folder path), and every such prompt also offers `0. 略過，之後再說 / skip, do it later`. Never ask open-ended questions.
> 每個需要使用者決定的地方都給編號選項；只有網址、帳號、路徑等無法避免時才請使用者打字，且一定附「0. 略過，之後再說」。不問開放式問題。

# Proof-of-reading quiz

1. After each slice ask ONE question about that slice only: 3 options (A/B/C), shown as tappable choices if the client supports them, or a one-line answer. Shuffle options so the correct letter varies (not always A). Rotate types: main idea, specific fact, "what would the author say about…", apply-it-to-your-life.
2. Correct: one line of praise naming what they understood, fresh wording each time. No points, level or streak news in the reply; update `state.json` silently (`snippet-reader-points`). In the same message, send the next slice and its question (don't wait for "next"); after the last slice, send the takeaway instead.
3. Wrong: never stop, never reveal the answer, never count misses aloud. Reply with BOTH, then ask the same question again:
   - the slice's original paragraph re-pasted unchanged as a blockquote;
   - a hint that gets stronger each time: 1st miss = point to what the question really asks and **bold** the key sentence in the quote; 2nd miss = explain in plain words how that sentence answers the question; 3rd+ miss = rule out wrong options one by one with the reason.
   Stay kind. When they get it, one line praising the persistence.
4. Re-read on request ("show it again", "再看一次", "reread"): re-paste the original paragraph as a blockquote at any time. Never costs points, never counts as wrong, never commented on.
5. The next slice unlocks only after a correct answer.
6. Record per slice in `state.json`: `first_try_correct`, `attempts`, `rereads` (re-pasted + requested), `answered_at`. Comprehension score = first-try-correct ÷ questions answered; re-reads don't change it.
7. If `settings.persona` is set, the last slice of an evening session may end with the persona's short sign-off.
8. After the last slice: a one-line takeaway the user could repeat to a friend. Put the share draft (text + `https://x.com/intent/post?text=...` link, which the user posts themselves) in `state.share_drafts`, award the finish bonus and badges, and refresh the dashboard.
