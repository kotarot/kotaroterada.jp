# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, etc.) working in this repository.
Human-oriented usage is in [README.md](README.md).

## What this repo is

Personal portfolio / biography site of Kotaro Terada (寺田 晃太朗), served at <https://kotaroterada.jp/>.

- Content is written in **Markdown** (`markdown/bio.md` = English, `markdown/bio.ja.md` = Japanese).
- A custom Python script (`convert.py`) converts Markdown → HTML using Python-Markdown, BeautifulSoup and a Jinja2 template (`bio.tpl`).
- The generated pages are served by a small **Flask** app (`app/main.py`) on **Google App Engine** (Python 3.13 runtime).
- Deployment is automated by GitHub Actions on push to `main`.

## Repository layout

| Path | Purpose |
| --- | --- |
| `markdown/bio.md` | English biography content (source of `/bio`) |
| `markdown/bio.ja.md` | Japanese biography content (source of `/bio.ja`) |
| `bio.yaml` | Site config: name, title, description, keywords, copyright, root URL, photos, OGP |
| `bio.tpl` | Jinja2 HTML shell for bio pages (`<head>`, OGP meta, CSS/JS includes) |
| `convert.py` | Markdown → HTML converter (sections, TOC nav, header/footer) |
| `build.sh` | Full build: regenerates `app/templates/` and `app/static/` |
| `assets/templates/index.html` | Hand-written top page (`/`) — **not** generated |
| `assets/static/` | Static files (photos, CSS, `robots.txt`, `humans.txt`, vendored Skyline CSS framework) |
| `app/main.py` | Flask app: routes `/`, `/bio`, `/bio.ja`, `/cv`→`/bio`, `/cv.ja`→`/bio.ja`, domain redirects |
| `app/main_test.py` | pytest tests for routes (require a prior build) |
| `app/app.yaml`, `app/dispatch.yaml` | GAE service and domain dispatch config |
| `.github/workflows/` | `build.yaml` / `ci.yaml` (every push), `deploy.yaml` (push to `main`), `ping.yaml` (daily uptime check) |

`app/static/`, `app/templates/` and `app/requirements.txt` are **build outputs** (git-ignored). Never edit them by hand; edit the sources and rerun `./build.sh`.

## Commands

Run from the repository root.

```bash
# Setup (once)
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt -r requirements-test.txt

# Build (Markdown -> app/templates/*.html, copy assets into app/)
./build.sh

# Tests (must build first)
cd app && pytest --verbose

# Local server
cd app && python main.py          # http://127.0.0.1:5000/
```

Deployment happens automatically on merge to `main` (`.github/workflows/deploy.yaml`). Do not run `gcloud app deploy` yourself.

CI runs the build and tests on Python 3.10–3.13 (Ubuntu and macOS), so avoid syntax/features newer than Python 3.10.

## Editing the biography content

- **Always update both languages together.** `bio.md` and `bio.ja.md` mirror each other section by section and line by line; a change in one almost always needs the matching change in the other.
- Line breaks inside an entry use **two trailing spaces** (`  `) at the end of the line. Keep them; many editors strip them.
- Entries under Work Experience are formatted as:
  ```
  Sep. 2023 &ndash; **present**  
  Role, [Org](url) (May 2025 &ndash; present)  
  ```
  - English dates: `Jan.`, `Feb.`, … `May`, `Jun.`, `Jul.` … `Dec.` followed by the year (e.g. `Jul. 2026`). Current = `**present**` / `present`.
  - Japanese dates: `2026年7月`. Current = `**現在**` / `現在`.
  - Ranges use `&ndash;`. When a role ends and a new one starts, list the newest role first and close the previous role's range (e.g. `(May 2025 &ndash; Jun. 2026)`).
- The `{{photo}}` placeholder near the top of each Markdown file is replaced by the profile photo block. Keep it.
- Raw HTML is allowed (icons like `<i class="fas fa-envelope"></i>`, emoji-css `<i class="em em-jp">`).

### Constraints imposed by `convert.py`

- The first line of the Markdown must render to a `<p>` (the language switch link) — it is wrapped as the first section.
- Every `## ` (h2) starts a new `<section>` and becomes an entry in the header/footer nav. Its `id` is the heading text lowercased with spaces → `-`.
- `## ` and `### ` headings must be **plain text** (no links/inline markup): `convert.py` uses `h.string`, which is `None` for mixed content and will crash. Links are fine in `####` headings.
- Tests assert on specific strings: `Work Experience` (en), `所属・経歴` (ja), `Biography of`, `Website of`. Renaming those headings requires updating `app/main_test.py`.

## Other common edits

- **Copyright year** appears in `bio.yaml` (`page.copyright`) and `assets/templates/index.html` footer — update both.
- **Photos** live in `assets/static/photo/`; select them via `bio.yaml` (`page.photo`, `page.bgphoto`).
- **New route**: add it to `app/main.py` and a test in `app/main_test.py`.

## Workflow checklist

1. Edit sources (`markdown/`, `bio.yaml`, `bio.tpl`, `assets/`, `convert.py`, `app/main.py`).
2. `./build.sh` — must print `Converted: ...` for both pages without errors.
3. `cd app && pytest` — all tests must pass.
4. Optionally grep the generated HTML in `app/templates/` to confirm the change rendered as intended.
5. Commit only source files (build outputs are git-ignored). Work on a feature branch and open a PR to `main`; merging deploys to production.
