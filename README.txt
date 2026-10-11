MY TRAVEL MAP v8.2
==================

HOW TO RUN
- Mac:     double-click "Launch My Travel Map.command"
- Windows: double-click "Launch My Travel Map (Windows).bat"
The map opens in your browser. Keep the Terminal / command window open while
you use the app; close it when you are finished.
Always start with the launcher - not by opening My_Travel_Map.html directly -
or the app cannot save to travel-data.json.

IF IT DOES NOT LAUNCH
- Windows: the launcher window now stays open and says what is wrong. Most
  often Python 3 is not installed: get it from https://www.python.org/downloads/
  and tick "Add python.exe to PATH" in the installer. (Typing "python" opening
  the Microsoft Store means Python is NOT installed.)
- Mac, "you do not have appropriate access privileges": the launcher lost its
  run permission (this happens when the folder is copied from a Windows PC or
  some cloud drives). Either unzip the .zip directly on the Mac, or open
  Terminal and run:   chmod +x <drag the .command file here>   then try again.
- Mac, "cannot be opened because it is from an unidentified developer":
  right-click (Control-click) the launcher > Open > Open. Needed once only.
- Last resort, any computer: open Terminal / Command Prompt in this folder and
  run   python3 server.py   (Windows: py server.py)

YOUR DATA
travel-data.json (in this folder) is the master database: profile + places.
Every add / edit / delete / profile change / import is written to it
immediately, and the app waits for the file to be written before treating the
change as done. The header shows "✓ JSON connected - N places" when all is well.

This package does NOT include a travel-data.json, so it can never overwrite
yours. The file is created on the first save.

UPGRADING FROM v7 (or earlier)
Either:
  A) Copy your existing populated travel-data.json into this v8 folder, then
     start v8. It loads as-is (v7 files are fully compatible).
or
  B) Start v8, click Import, choose your travel-data.json (or a Backup JSON
     file), then choose "Merge with existing".
Close any old Travel Map Terminal window first (not required - v8 picks a
different port if 8765 is busy - but it avoids confusion).

WHAT'S NEW IN v8.2 - WHERE I WANT TO GO
- Every place is tagged either "Been here" (blue) or "Want to go" (orange).
  Places saved before v8.2 count as "Been here" - nothing to do.
- Tabs above the list: Been here (n) / Want to go (n) / Both. In Both, the
  list has two sections - "Where I've been" and "Where I want to go" - each
  grouped by country with its own counts and collapse state. The map shows
  only the markers for the selected tab.
- Add / Edit dialog has a Been here / Want to go choice. New places default to
  the tab you are on (Want to go tab -> Want to go).
- Been to a Want-to-go place? Click "✓ Been" in the list or "✓ I've been here"
  in its map popup to move it across.
- Search results are now purple (orange means Want to go).
- Google KML export has two folders, Where I've been / Where I want to go, with
  blue / orange pins and a "status" column.
- travel-data.json: each place gets "status": "been" or "want".

WHAT'S NEW IN v8.1
- Dark mode for the interface: "Theme" menu next to Profile - Auto (follows
  your Mac's appearance), Light or Dark. Your choice is remembered.
  The map itself keeps its own style menu (top right); pick "Dark" there too
  for a fully dark screen.
- Search results are now marked on the map: the searched area is outlined
  (cities, countries, parks...) or circled (mountains, landmarks), with a pin
  and the place name. "+ Add" saves it straight to your places with name,
  country and coordinates filled in; the X removes it. A new search replaces it.
- New and edited places get createdAt / updatedAt timestamps (existing ones
  are kept).
- "Sync browser -> JSON" is only offered when the browser holds places the file
  does not have. If you drop a newer travel-data.json into the folder, the
  app no longer offers to overwrite it with an older browser copy.

WHAT'S NEW IN v8
Map selection
- Country, state and province names are no longer picked as "places".
  Clicking near the "Malaysia" label no longer saves "Malaysia".
- Nearest label wins: candidates are ranked by type AND distance from the click.
- "What did you mean?" chooser when several good places are labelled at the
  spot you clicked (e.g. a peak and a town). "None of these" uses the exact
  clicked spot with a name lookup.
- The Add dialog says what was selected (Town, Mountain / peak, Landmark...).
- Clicking the map to close a popup, or clicking a marker, no longer opens
  "Add place".

Data safety
- The browser fallback copy is updated only after travel-data.json has been
  written, so a failed save can no longer leave a bogus "Sync" offer behind.
- Stale-window protection: if travel-data.json was changed by another window
  (e.g. an old tab left open), saves from the stale window are refused instead
  of overwriting newer data. Reload the page to continue.
- The server never overwrites a travel-data.json it cannot read (corrupt or
  hand-edited with a mistake); the app shows the problem instead.
- The server keeps any extra fields already in travel-data.json.
- Each place is checked for valid coordinates before it is written.
- "Sync browser -> JSON" downloads a backup of the current JSON first.
- Merge duplicate detection ignores case, accents and punctuation and treats
  the same name within 1 km as a duplicate.

Reliability
- MapLibre GL JS 5.24.0 is bundled in ./lib (no longer loaded from unpkg), so
  a new MapLibre release cannot change the app unexpectedly.
- Name look-ups and searches are limited to 1 request per second, as
  OpenStreetMap Nominatim asks.

Browsing
- The filter now hides non-matching markers on the map as well as in the list,
  and "My places" zooms to the filtered places.
- Countries are grouped ignoring capitalisation ("malaysia" and "Malaysia"
  appear as one group, shown with the most common spelling).
- Collapse all / Expand all button.
- Notes preview under each place in the list.
- Your chosen map style is remembered.
- Windows launcher added (Mac remains the primary platform).

Retained from v7: country grouping and counts, A-Z / Z-A, collapse/expand,
visible Edit/Delete in list and popups, Profile (name, year of birth), safe
Merge / Replace / Cancel import with backup before Replace, JSON backup,
Google KML export, English/Latin labels, mountain labels, 5 map styles,
dynamic port launcher, no-cache serving.

FILES
My_Travel_Map.html                  the app
server.py                           local server (127.0.0.1 only)
Launch My Travel Map.command        Mac launcher
Launch My Travel Map (Windows).bat  Windows launcher
lib/                                MapLibre GL JS 5.24.0 (BSD licence)
travel-data.json                    your data (created on first save)

Map data (c) OpenStreetMap contributors, tiles by OpenFreeMap.
Internet is needed for map tiles and name look-ups; your data stays local.
