# GlobalC60.com

Website for Global C60 Inc., Calgary, Alberta. One self-contained page plus a few support files.

Revision 1, 1 October 2026. Built from the approved content plan and the GlobalC60 Recovery Brand and Website Design Guide v1.2.

## Folders

| Folder | What it holds |
| --- | --- |
| `public/` | The website. Upload the contents of this folder to the web root. |
| `src/` | Source used to build `public/index.html`: page template, illustration generator, logo paths. |
| `docs/` | Design specification and content plan. Open the `.html` files in a browser. |

## Files in `public/`

| File | Purpose |
| --- | --- |
| `index.html` | The site. All styles, scripts, logo and drawings are inside it. Only Google Fonts loads from outside. |
| `og-image.png` | Link preview image (1200 x 630) for LinkedIn, X, Facebook, Teams, Slack. |
| `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png` | Browser and phone icons. |
| `logo-512.png` | Logo used in search engine structured data. |
| `robots.txt`, `sitemap.xml` | Search engine crawling. |

## Editing the site

Small text changes can be made directly in `public/index.html`.

For changes to layout, the logo or the drawings, edit `src/index.src.html` (or the scripts) and rebuild:

```
python3 src/gen_illustrations.py   # only if the drawings change; run from src/
python3 src/build.py               # writes public/index.html
```

Edits made only to `public/index.html` are overwritten the next time `build.py` runs, so make lasting changes in `src/index.src.html`.

## Interest form

The form opens in a pop-up from every "Register interest", "Host a unit" and "Buy our carbon" button. A static page cannot send email by itself, so it posts to a form service. Set one line near the bottom of `index.html` (and of `src/index.src.html`):

```
var FORM_ENDPOINT = "";   // a Formspree URL such as "https://formspree.io/f/abcdwxyz", or "netlify" on Netlify
```

Until it is set, the form asks visitors to email rvisser@globalc60.com.

For Bluehost: create a free Formspree form that sends to rvisser@globalc60.com, paste its URL into `FORM_ENDPOINT`, upload, and send a test submission.

## Deploying to Bluehost

1. In Bluehost, turn off the WordPress "Coming Soon" page, or remove WordPress from the globalc60.com document root if it is no longer needed. Back it up first.
2. Open File Manager (or connect by FTP) and go to the site's document root, usually `public_html`.
3. Upload everything inside `public/` (not the folder itself) so `index.html` sits in the document root.
4. Make sure SSL is active for globalc60.com in Bluehost, so the site loads on https.
5. Visit https://globalc60.com and check the page, the favicon and the form.

Domain and email stay where they are, so no DNS changes are needed.

## Before launch

- Set `FORM_ENDPOINT` and send a test submission.
- Confirm the SOx, NOx and carbon monoxide statement and the "significantly reduce the cost" line against the October test results.
- Confirm Elemental Air approves being named and linked.
- Each co-founder checks their team entry and LinkedIn link.
- Replace the logo when the re-set GLOBALC60 / RECOVERY wordmark is delivered.

See `docs/design-spec.html` section 11 for routine updates (lab results, TIER recognition, social channels, GCM launch).
