#!/usr/bin/env python3
"""My Travel Map v8 - local server.

Serves the app from this folder and reads/writes travel-data.json.
Only listens on 127.0.0.1 (this computer).
"""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, unquote
import hashlib, json, os, sys, threading, time, webbrowser

APP_NAME = "My Travel Map"
VERSION = 8          # travel-data.json format version
BUILD = "8.2"        # app build
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "travel-data.json"
PREFERRED_PORT = 8765
WRITE_LOCK = threading.Lock()


def empty_db():
    return {"app": APP_NAME, "version": VERSION,
            "profile": {"name": "", "yearOfBirth": ""}, "places": []}


def revision_of(raw: bytes) -> str:
    return hashlib.sha1(raw).hexdigest() if raw else ""


def read_file():
    """Return (raw_bytes, parsed_object_or_None, error_or_None)."""
    if not DATA.exists():
        return b"", None, None
    raw = DATA.read_bytes()
    if not raw.strip():
        return raw, None, None
    try:
        return raw, json.loads(raw.decode("utf-8-sig")), None
    except Exception as e:  # corrupt / hand-edited file
        return raw, None, f"travel-data.json is not valid JSON ({e})"


class Handler(SimpleHTTPRequestHandler):
    # ---------- helpers ----------
    def send_json(self, code, obj, extra_headers=None):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extra_headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def translate_path(self, path):
        # Serve only files inside the app folder.
        clean = unquote(urlparse(path).path).lstrip("/")
        target = (ROOT / clean).resolve()
        if target != ROOT and ROOT not in target.parents:
            return str(ROOT / "__forbidden__")
        return str(target)

    # ---------- routes ----------
    def do_GET(self):
        route = self.path.split("?", 1)[0]
        if route == "/api/data":
            raw, obj, err = read_file()
            if err:
                self.send_json(500, {"ok": False, "error": err})
                return
            if obj is None:
                obj = empty_db()
            self.send_json(200, obj, {"X-Data-Revision": revision_of(raw),
                                      "X-App-Version": str(VERSION)})
            return
        if route == "/api/info":
            self.send_json(200, {"app": APP_NAME, "version": VERSION,
                                 "folder": str(ROOT), "dataFile": str(DATA)})
            return
        if route == "/":
            self.path = "/My_Travel_Map.html"
        super().do_GET()

    def do_POST(self):
        if self.path.split("?", 1)[0] != "/api/data":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            incoming = json.loads(self.rfile.read(length).decode("utf-8"))
            if not isinstance(incoming, dict):
                raise ValueError("body must be an object")

            places = incoming.get("places")
            if not isinstance(places, list):
                raise ValueError("places must be a list")
            for i, p in enumerate(places):
                if not isinstance(p, dict):
                    raise ValueError(f"place #{i + 1} is not an object")
                try:
                    lat, lng = float(p.get("lat")), float(p.get("lng"))
                except (TypeError, ValueError):
                    raise ValueError(f"place #{i + 1} has invalid coordinates")
                if not (-90 <= lat <= 90 and -180 <= lng <= 180):
                    raise ValueError(f"place #{i + 1} has out-of-range coordinates")

            profile_in = incoming.get("profile", {})
            if not isinstance(profile_in, dict):
                raise ValueError("profile must be an object")
        except Exception as e:
            self.send_json(400, {"ok": False, "error": str(e)})
            return

        with WRITE_LOCK:
            raw, current, err = read_file()
            if err:
                # Never overwrite a file we cannot read - it may hold the only copy.
                self.send_json(409, {"ok": False, "error": err +
                                     ". Fix or move the file, then restart. Nothing was written."})
                return

            # Stale-window protection: refuse writes based on an older copy.
            base = incoming.get("baseRevision")
            if base is not None and base != revision_of(raw):
                self.send_json(409, {"ok": False, "stale": True,
                                     "error": "travel-data.json was changed by another window or program. Reload the page before making changes. Nothing was written."})
                return

            # Keep every top-level field already in the file (forward compatibility),
            # then apply the fields this app manages.
            payload = dict(current) if isinstance(current, dict) else {}
            old_profile = payload.get("profile") if isinstance(payload.get("profile"), dict) else {}
            profile = dict(old_profile)
            profile.update(profile_in)
            profile["name"] = str(profile.get("name", "") or "")
            profile["yearOfBirth"] = str(profile.get("yearOfBirth", "") or "")

            payload["app"] = APP_NAME
            payload["version"] = VERSION
            payload["profile"] = profile
            payload["places"] = places
            # Preserve any other top-level keys the client sent (future fields).
            for k, v in incoming.items():
                if k not in ("app", "version", "profile", "places", "baseRevision"):
                    payload[k] = v

            ordered = {"app": payload.pop("app"), "version": payload.pop("version"),
                       "profile": payload.pop("profile"), "places": payload.pop("places")}
            ordered.update(payload)

            new_raw = json.dumps(ordered, ensure_ascii=False, indent=2).encode("utf-8")
            tmp = DATA.with_name(DATA.name + ".tmp")
            try:
                with open(tmp, "wb") as f:
                    f.write(new_raw)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp, DATA)
            except Exception as e:
                self.send_json(500, {"ok": False, "error": f"Could not write travel-data.json: {e}"})
                return

        self.send_json(200, {"ok": True, "revision": revision_of(new_raw),
                             "count": len(places)})

    def end_headers(self):
        # Always serve the current files from this folder; never a cached older copy.
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass


def make_server():
    # Prefer 8765, but if an older Travel Map is still running there, use a free
    # port instead of accidentally opening the old app.
    try:
        return ThreadingHTTPServer(("127.0.0.1", PREFERRED_PORT), Handler)
    except OSError:
        return ThreadingHTTPServer(("127.0.0.1", 0), Handler)


def open_browser(port):
    time.sleep(0.4)
    webbrowser.open(f"http://127.0.0.1:{port}/?build=v{BUILD}")


if __name__ == "__main__":
    os.chdir(ROOT)
    httpd = make_server()
    port = httpd.server_address[1]

    if "--no-browser" not in sys.argv:
        threading.Thread(target=open_browser, args=(port,), daemon=True).start()

    print("")
    print(f"{APP_NAME} v{BUILD} is running.")
    print(f"Folder:    {ROOT}")
    print(f"Data file: {DATA}{'' if DATA.exists() else '  (will be created on first save)'}")
    print(f"Address:   http://127.0.0.1:{port}/")
    if port != PREFERRED_PORT:
        print("")
        print(f"NOTE: Port {PREFERRED_PORT} was already in use, probably by an older")
        print("Travel Map window. This version has safely started on a different port.")
    print("")
    print("Keep this window open while using the app. Close it when you are finished.")
    print("")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()
