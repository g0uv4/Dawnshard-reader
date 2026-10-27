---
name: snippet-reader-daily-push
description: Scheduled reading invites for Snippet Reader. Use when a scheduled run fires (cron, codex exec or a ChatGPT/Codex scheduled task), or when the user wants to set up, change or remove the invite schedule, weekly recap or newsletter import.
---
# Daily push and scheduling

Rule: each push is one short invitation to read the next slice. Everything else (expiry countdowns, points, level, streak, badges, quest, weekly recap, queue and import notices, share drafts) goes to the dashboard only.

## Setting up the schedule
Defaults in the user's time zone: invites at 08:00, 12:30, 20:30 (`settings.push_times`), nothing during quiet hours 21:00–06:00 (`quiet_hours`), optional weekly recap run Sunday 20:00 (`weekly_recap`) that writes the recap to the dashboard. Pick one mechanism with the user:

- **Scheduled task in the ChatGPT/Codex desktop app**: create a scheduled task on the reading project with the prompt `$snippet-reader-daily-push Run once.` (recap: `$snippet-reader-daily-push Run the weekly recap.`). The Codex CLI cannot create these. If the project is a Git repo, runs may happen in a separate worktree, so always read and write the absolute `settings.data_dir`, kept outside the repo or git-ignored. The task uses the app's sandbox settings; it needs write access to `data_dir` (and network if it imports feeds).
- **cron + codex exec** (any machine; `codex exec` defaults to a read-only sandbox, so allow writes):
  ```cron
  # crontab uses the system time zone; CRON_TZ works on cronie/systemd-cron but not every cron.
  0 8  * * *   cd /path/to/reading-workspace && codex exec --skip-git-repo-check -s workspace-write "Run the snippet-reader-daily-push skill once." >> .snippet-reader/push.log 2>&1
  30 12,20 * * * cd /path/to/reading-workspace && codex exec --skip-git-repo-check -s workspace-write "Run the snippet-reader-daily-push skill once." >> .snippet-reader/push.log 2>&1
  0 20 * * 0   cd /path/to/reading-workspace && codex exec --skip-git-repo-check -s workspace-write "Run the snippet-reader-daily-push skill: weekly recap only." >> .snippet-reader/push.log 2>&1
  ```
  Feed imports need network: add `-c sandbox_workspace_write.network_access=true` only if the user agrees. `codex exec` must already be signed in on that machine; never put keys in crontab, this repo or state files (use the environment).
- Delivery: write the invite to `<data_dir>/inbox/<timestamp>.md`, or pipe it to `settings.notify_command` (the user's own notifier or webhook, secrets from the environment).
- Verify the schedule exists after creating it, and tell the user in one or two sentences what is now automated.

## Each run
1. Housekeeping, silently: import new items from `import_sources` (read-only, `is_new: true`), expire unopened articles past 48h, promote from the queue, apply streak/freeze for the new day (`snippet-reader-points`).
2. Inside quiet hours, or nothing left to read: send nothing. If the list is empty, the dashboard may list a few suggested unread items from the import sources.
3. Otherwise deliver the next slice of the article in progress (or the oldest unread) at `slice_seconds`, with its question (`snippet-reader-quiz`). One message per run.
4. Weekly recap run: compute `weekly.recap` (slices, articles, points, best moment), reset the quest on Monday, send no chat message unless the user asked for one.
5. Refresh the dashboard (`snippet-reader-dashboard`). Don't link it unless asked.

## Never in the invite
Expiry reminders, points or levels, streak or badge news, import or queue notices, recaps, share drafts, small talk.
