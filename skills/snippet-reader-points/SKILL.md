---
name: snippet-reader-points
description: Gamification rules for Snippet Reader - points, quota levels, queue, streaks, streak freeze, badges, weekly quest. Use whenever a slice is answered, an article finishes or expires, an article is added at quota, or a day rolls over.
---
# Points, quota, queue, streaks, badges

All values are written to `state.json` and shown only on the dashboard, never announced in the conversation. Append every award to `points_log` (`at`, `reason`, `delta`) so totals can be audited.

## Points (never decrease)
| Event | Points |
|---|---|
| Slice answered correctly (any attempt) | +10 |
| Article finished | +20 |
| Finished before 48h expiry with every first try correct | +10 |
| Daily first slice ("warm-up") | +5 |
| Streak bonus per day | +5 × streak days, cap +50/day |
| Weekly surprise slice (one random slice per week) | double that slice's points |

Re-reads and hints never reduce points.

## Quota levels (active = unread + in progress)
| Points | Active quota |
|---|---|
| 0 | 5 |
| 100 | 7 |
| 250 | 10 |
| 500 | 15 |
| 1000 | 20 |
| 2000 | 30 |
Level = index in this table. Quota never drops.

## Queue
At quota, still accept shares and imports into `queue` (FIFO). When a slot opens (finish or expiry), promote the next item silently.

## Expiry
Unopened articles expire 48h after `added_at` (status `expired`, kept in the "gone" list). Opened articles never expire.

## Streak
A day (user's time zone) counts if at least one slice is answered. One free streak-freeze per ISO week, used automatically on a missed day (`streak.freeze_used_week`).

## Badges
`first-article` · `streak-7` · `streak-30` · `perfect-10` (10 first-try correct slices in a row) · `beat-expiry-5` (5 articles finished before expiry) · `first-share`. Store earned date; show locked badges with progress.

## Weekly quest
Default: finish 2 articles and get 5 first-try answers this week. Store in `weekly.quest` with progress; reset every Monday.

## Tone
No teasing or small talk. The conversation carries slices, questions, hints and one-line praise only.

## Stats
Keep `state.stats` current: `questions`, `first_try_correct`, `perfect_run` (resets on a non-first-try answer; 10 = `perfect-10`), `finished_before_expiry` (5 = `beat-expiry-5`).

## Shelved
Shelved articles don't count as active, never expire and earn nothing until resumed.
