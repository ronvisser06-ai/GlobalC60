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

The form opens in a pop-up from every "Register interest", "Host a unit" and "Buy our carbon" button. It submits to Formspree, which emails each submission to rvisser@globalc60.com.

- Endpoint: `https://formspree.io/f/xyezaoww`, set in `FORM_ENDPOINT` near the bottom of the page and in the form's `action` attribute (the fallback when JavaScript is off). If it ever changes, update both, in `src/index.src.html`, then rebuild.
- Each email has the subject "GlobalC60.com: new interest registration". Replying goes to the visitor's email address.
- The interest is sent as readable text, for example "Deploying the technology on our site", along with the page the visitor submitted from.
- Spam: a hidden `_gotcha` field. Formspree discards submissions where it is filled in.
- After the site is live, send one test submission from https://globalc60.com. In Formspree, consider restricting the form to the globalc60.com domain.

## Deploying to Bluehost

1. In Bluehost, turn off the WordPress "Coming Soon" page, or remove WordPress from the globalc60.com document root if it is no longer needed. Back it up first.
2. Open File Manager (or connect by FTP) and go to the site's document root, usually `public_html`.
3. Upload everything inside `public/` (not the folder itself) so `index.html` sits in the document root.
4. Make sure SSL is active for globalc60.com in Bluehost, so the site loads on https.
5. Visit https://globalc60.com and check the page, the favicon and the form. Send one test submission and confirm it arrives at rvisser@globalc60.com.

Domain and email stay where they are, so no DNS changes are needed.

## Before launch

- Send a test submission from the live site.
- Confirm the SOx, NOx and carbon monoxide statement and the "significantly reduce the cost" line against the October test results.
- Confirm Elemental Air approves being named and linked.
- Each co-founder checks their team entry and LinkedIn link.
- Replace the logo when the re-set GLOBALC60 / RECOVERY wordmark is delivered.

See `docs/design-spec.html` section 11 for routine updates (lab results, TIER recognition, social channels, GCM launch).
