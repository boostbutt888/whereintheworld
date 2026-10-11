#!/bin/zsh
cd "$(dirname "$0")" || exit 1

clear
echo "Starting My Travel Map v8.2..."
echo "Folder: $(pwd)"
echo ""

# A working Python 3.7+ is needed (macOS's /usr/bin/python3 can be a stub that
# only offers to install the developer tools).
if ! command -v python3 >/dev/null 2>&1 || ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,7) else 1)' >/dev/null 2>&1; then
  echo "PYTHON 3 IS NOT INSTALLED (or is not working)."
  echo "Install it from https://www.python.org/downloads/ and run this launcher again."
  osascript -e 'display dialog "My Travel Map needs Python 3.\n\nInstall it from python.org/downloads, then double-click the launcher again." buttons {"OK"} default button "OK" with icon caution' >/dev/null 2>&1
  exit 1
fi

if [ ! -f server.py ]; then
  echo "server.py is missing from this folder. Unzip the whole My Travel Map folder first."
  exit 1
fi

python3 server.py
echo ""
echo "My Travel Map has stopped. If you see an error above, send a screenshot of this window."
