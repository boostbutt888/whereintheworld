# My Travel Map

A personal, local-first travel map: record the places you **have been** (blue) and the places you **want to go** (orange) on a free, detailed world map.

- Runs on your own computer — a tiny Python server plus one HTML page.
- Your data lives in `travel-data.json` next to the app (not in this repository).
- Free mapping: [MapLibre GL JS](https://maplibre.org/) 5.24.0 (bundled in `lib/`) with [OpenFreeMap](https://openfreemap.org/) tiles and OpenStreetMap Nominatim search. No API keys.

## Run it

| Computer | Start with |
|---|---|
| Windows | `Launch My Travel Map (Windows).bat` |
| Mac | `Launch My Travel Map.command` |

Requires Python 3.7+. The app opens at `http://127.0.0.1:8765/` (or another free port). Keep the launcher window open while using it. Always start from the unzipped folder, never from inside a ZIP.

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
| `docs/PROJECT_CONTEXT.txt` | Requirements, design rules and regression checklist |

## Your data

`travel-data.json` is git-ignored on purpose. Back it up with the app's **Backup JSON** button or by copying the file.

Map data © OpenStreetMap contributors.
