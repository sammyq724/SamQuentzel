# Sam Quentzel — Digital Career Portfolio

A static website for MGT 2010 Management Communication. No frameworks and no build service: GitHub Pages serves the `.html` files in this folder as they are.

**Live site (once GitHub Pages is on):** https://sammyq724.github.io/SamQuentzel/

## Turn on the live link (one time)

1. Open the repository on GitHub and go to **Settings → Pages**.
2. Under **Build and deployment**, set **Source** to **Deploy from a branch**.
3. Choose the branch that holds these files and the folder **/ (root)**, then **Save**.
4. Wait about a minute and open the link above. GitHub Pages needs the repository to be public on a free account.

## What is in the portfolio

| Piece | Page | Points |
| --- | --- | --- |
| Resume Page (image + downloadable PDF) | `resume.html` | Required |
| Purpose Essay | `purpose.html` | 15 |
| Career Artifact 1: interview with my mother | `interviews.html#mother` | 10 |
| Career Artifact 2: interview with my father | `interviews.html#father` | 10 |
| Brand Style Guide | `brand.html` | 10 |
| Core Story Set (4 STAR stories) | `stories.html` | 15 |
| Thought Piece | `thought-piece.html` | 15 |
| Podcast Thought Piece | `podcast.html` | 25 |
| **Total** | | **100** |

`portfolio-index.html` shows this same table on the site.

## Still to add

The two interviews and the podcast have a finished space on the site but no recording yet.

- **Interviews:** put the recording in `assets/media/` (or get an embed link), then open `tools/pages/interviews.html`. A comment above each interview shows exactly which block to replace with the player, and where the "What I learned" write-up goes.
- **Podcast:** same steps in `tools/pages/podcast.html`.
- Then rebuild (below) and commit.

## Editing the site

Page content lives in `tools/pages/`, one file per page. The shared header, navigation and footer live in `tools/build.py`. After any edit, rebuild:

```bash
python3 tools/build.py
```

The build also counts the words in the essay, each story and the thought piece, and fails if one falls outside the assignment's limits.

To preview locally:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Folder map

```
index.html, resume.html, ...   built pages (do not edit by hand; edit tools/pages/ and rebuild)
assets/css/site.css            all styles and the brand colors
assets/fonts/                  Archivo, Source Serif 4, IBM Plex Mono (open-source, self-hosted)
assets/img/                    headshot, resume image, LinkedIn cover
assets/docs/                   resume PDF
assets/media/                  interview and podcast recordings go here
tools/                         page sources and the build script
submission/                    the document to hand in: portfolio link + points table
```
