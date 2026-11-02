# My Travel Map

A personal, local-first travel map: record the places you **have been** (blue) and the places you **want to go** (orange) on a free, detailed world map.

Two editions live in this repository:

| Edition | Folder | Data stored in | Who uses it |
|---|---|---|---|
| **Desktop v8.2** | repository root | `travel-data.json` next to the app (not in this repository) | You, on your own computer |
| **Online v9.0** | [`online/`](online/) | Supabase (Postgres), one private row per Google account | Anyone you share the link with, each with their own map |

- Free mapping: [MapLibre GL JS](https://maplibre.org/) 5.24.0 (bundled in `lib/`) with [OpenFreeMap](https://openfreemap.org/) tiles and OpenStreetMap Nominatim search. No API keys.

## Run the desktop edition

| Computer | Start with |
|---|---|
| Windows | `Launch My Travel Map (Windows).bat` |
| Mac | `Launch My Travel Map.command` |

Requires Python 3.7+. The app opens at `http://127.0.0.1:8765/` (or another free port). Keep the launcher window open while using it. Always start from the unzipped folder, never from inside a ZIP.

## Put the online edition up

**Live address (GitHub Pages):** https://boostbutt888.github.io/whereintheworld/ — published automatically from `online/site/` by `.github/workflows/pages.yml` on every push to `main`.

Follow [`online/SETUP-GUIDE.txt`](online/SETUP-GUIDE.txt) (GitHub Pages steps are at the end): create a free Supabase project, run `online/supabase-setup.sql`, turn on Google sign-in, put your Project URL and anon/publishable key in `online/site/config.js`, then drag `online/site/` onto Netlify Drop. Move your desktop data across with **Import → Merge** of `travel-data.json`.

## Features

- Been here / Want to go lists, grouped by country with counts, A–Z / Z–A, collapse/expand, filter
- Click a city, town, mountain or landmark label to add it (with a "What did you mean?" chooser when labels overlap)
- Search shows the place's outline and a pin on the map, with one-click **+ Add**
- Profile (name, year of birth), dark mode, five map styles, English/Latin labels, mountain labels
- Safe saving: every change is confirmed written to `travel-data.json` or rolled back
- Import (Merge / Replace with automatic backup), JSON backup, Google My Maps KML export

## Files

| File | Purpose |
|---|---|
| `My_Travel_Map.html` | The app (UI and logic) |
| `server.py` | Local server, reads/writes `travel-data.json` (127.0.0.1 only) |
| `Launch My Travel Map*.{bat,command}` | Launchers |
| `lib/` | MapLibre GL JS 5.24.0 (BSD-3-Clause) |
| `README.txt` | User guide and version history |
| `docs/PROJECT_CONTEXT.txt` | Requirements, design rules, version history (v7 → v9) and regression checklist |
| `online/` | Online edition: `site/` (Netlify), `supabase-setup.sql`, `SETUP-GUIDE.txt` |

## Your data

`travel-data.json` is git-ignored on purpose. Back it up with the app's **Backup JSON** button or by copying the file.

Map data © OpenStreetMap contributors.
