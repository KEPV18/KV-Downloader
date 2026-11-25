# KV-Downloader

A small Flask web app that downloads video or audio from a link using yt-dlp (audio conversion uses ffmpeg/pydub). Early personal project, not maintained.

## Run locally

```
pip install -r requirements.txt
python app.py
```

## Cookies

Some downloads need a logged-in session. The app reads a Netscape-format cookie file at `./templates/cookies.txt`; if the file is missing, the download helper creates a placeholder with no real data (see `app.py`).

- Do not commit cookie files. They are session credentials. `.gitignore` excludes them.
- `cookies.txt.example` shows the file format with fake values only.
- If you use your own cookies, export them locally and keep them out of Git.

## Notes

- Use it only for content you have the right to download.
- `wsgi.py` is a stub (`your_app_name` placeholder) and needs editing before deployment with gunicorn.
