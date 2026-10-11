@echo off
setlocal
cd /d "%~dp0"
title My Travel Map v8.2
echo Starting My Travel Map v8.2...
echo Folder: %cd%
echo.
rem Find a real Python 3.7+ (skips the Microsoft Store "python" shortcut, which is not Python).
set "PY="
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,7) else 1)" >nul 2>nul && set "PY=py -3"
if not defined PY (python -c "import sys; sys.exit(0 if sys.version_info >= (3,7) else 1)" >nul 2>nul && set "PY=python")
if not defined PY (python3 -c "import sys; sys.exit(0 if sys.version_info >= (3,7) else 1)" >nul 2>nul && set "PY=python3")
if not defined PY goto nopython
if not exist "server.py" goto nofiles
echo Using: %PY%
echo.
%PY% server.py
echo.
echo My Travel Map has stopped. If you see an error above, send a screenshot of this window.
pause
exit /b

:nopython
echo PYTHON 3 WAS NOT FOUND ON THIS PC.
echo.
echo 1. Download Python from https://www.python.org/downloads/
echo 2. Run the installer and TICK "Add python.exe to PATH" on the first screen.
echo 3. Double-click this launcher again.
echo.
pause
exit /b

:nofiles
echo server.py is missing from this folder: %cd%
echo Unzip the whole My Travel Map folder first, then run the launcher from inside it.
pause
