# KV-Downloader

A small Flask web app that downloads video or audio from a link using yt-dlp (audio conversion uses ffmpeg/pydub). Early personal project, not maintained.

## Run locally

```
pip install -r requirements.txt
python app.py
```

## Cookies

Some downloads need a logged-in session. In `app.py` the app points yt-dlp at a Netscape-format cookie file at `./templates/cookies.txt`.

- The file is no longer in this repository. Without it, behavior depends on the code path: one helper (near line 49 of `app.py`) writes a placeholder file with fake data when none exists, while the other download call (near line 177) passes the same path and has not been tested without the file. Expect that downloads needing a login may fail until you provide your own cookies.
- If you use your own cookies, export them locally to that path and keep them out of Git. They are session credentials. `.gitignore` excludes them.
- `cookies.txt.example` shows the file format with fake values only.

## Notes

- Use it only for content you have the right to download.
- `wsgi.py` is a stub (`your_app_name` placeholder) and needs editing before deployment with gunicorn.
