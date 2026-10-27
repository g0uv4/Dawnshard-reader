---
name: snippet-reader-video-slicing
description: Slice a long video or podcast (YouTube link or local file) into readable topic slices from captions or a transcript, then quiz each slice. Use when the user shares a long video/podcast to "read". Captions first, audio-only transcription as fallback, never frame-by-frame viewing.
---
# Slicing a long video or podcast

Rule: work only from text. Never download the whole video, never view frames, never generate video. Prefer the cheapest path.

## 1. Get the text (cheapest first)
1. If the user already has a transcript, use it as-is.
2. YouTube link: read existing captions (manual first, auto-generated second), keeping timestamps, e.g.
   `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs "zh.*,en.*" -o "cache/%(id)s" <url>`
3. No captions: download the audio stream only, convert to mono 16 kHz with ffmpeg, and transcribe with the smallest Whisper model that is good enough. Run one transcription job at a time; tell the user it will take a while.
   `yt-dlp -f bestaudio -o cache/audio.%(ext)s <url> && ffmpeg -i cache/audio.* -ac 1 -ar 16000 cache/audio.wav`
4. Site blocks the download or asks for bot verification, or the video is private/paid: stop, do not work around it; ask for a transcript or file.
5. Check that ffmpeg, yt-dlp and whisper exist before use; install only when needed. Delete audio files after transcription.

## 2. Prepare
- Keep the cleaned, timestamped transcript in `.snippet-reader/cache/` only. State keeps title, url, slice count, progress and each slice's start time.
- Captions and Whisper get names and numbers wrong. Mention this once, and don't quiz on a word that may be mis-transcribed.

## 3. Cut by topic
- Split at topic changes (timestamps, pauses), not fixed minutes, aiming for the user's slice length in reading time (same speeds and 15% overflow as `snippet-reader-slicing`).
- Each slice: the same bold localized header as `snippet-reader-slicing` plus the start time, a timestamp link (YouTube: `<url>&t=<seconds>s`), a short summary in the user's language, and a one-line hook. Don't spoil later slices.

## 4. Quiz, points, store
- Same rules as `snippet-reader-quiz` and `snippet-reader-points`. Quiz only on what the transcript actually says.
- Store with `kind: "video"` or `"podcast"` and `duration_seconds`; respect quota and queue; refresh the dashboard.
