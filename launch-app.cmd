@echo off
setlocal
rem ===================================================================
rem  SUPER WEAPON BALL: THE SUNDERED CROWN -- launch the desktop app.
rem
rem  Double-click this, or run it from a terminal. It starts the app on
rem  whatever CLAUDE.md section 0 currently calls the build of record.
rem
rem  WHY THIS IS A LAUNCHER AND NOT A PACKAGED .exe. A packaged build
rem  would bundle its own copy of Electron and freeze a SNAPSHOT of the
rem  game inside it. Both are wrong for this project: the runtime is
rem  PINNED at electron 44.0.0 because the pair with playwright 1.62.0
rem  is measured bit-equal (docs/RUNTIME-DRIFT.md), and the app is
rem  supposed to show the live build of record so it cannot drift from
rem  what the video renders (docs/ARCHITECTURE.md section 1). A frozen
rem  copy would quietly become a second, older game.
rem
rem  So this runs the pinned Electron out of app/node_modules against
rem  the repo as it stands right now.
rem ===================================================================

rem %~dp0 is this file's own folder, with a trailing backslash, so the
rem launcher works from a shortcut or any working directory.
set "REPO=%~dp0"
set "APP=%REPO%app"
set "ELECTRON=%APP%\node_modules\.bin\electron.cmd"

if not exist "%APP%\package.json" (
  echo.
  echo   Cannot find "%APP%\package.json".
  echo   This file has to sit in the repo root, next to CLAUDE.md.
  echo.
  pause
  exit /b 2
)

if not exist "%ELECTRON%" (
  echo.
  echo   Electron is not installed yet. Installing it now -- this is a
  echo   one-time step and takes a couple of minutes.
  echo.
  pushd "%APP%"
  call npm install
  set "INSTALL_FAILED=%ERRORLEVEL%"
  popd
  if not "%INSTALL_FAILED%"=="0" (
    echo.
    echo   npm install failed. Is Node installed and on PATH?
    echo.
    pause
    exit /b 1
  )
)

if not exist "%ELECTRON%" (
  echo.
  echo   Still no Electron at "%ELECTRON%" after installing.
  echo.
  pause
  exit /b 1
)

rem Run it from app/ -- main.js resolves the repo as its own parent, so
rem the working directory has to be the app folder and not wherever the
rem shortcut was clicked from.
pushd "%APP%"
call "%ELECTRON%" .
set "CODE=%ERRORLEVEL%"
popd

rem PAUSE ONLY ON FAILURE. A console that vanishes on a crash is how a
rem broken launch looks like a launcher that did nothing at all -- the
rem same shape as the ffmpeg failure in CLAUDE.md section 5, which
rem killed an encode after a successful capture and named no file.
if not "%CODE%"=="0" (
  echo.
  echo   The app exited with code %CODE%.
  echo.
  pause
)
exit /b %CODE%
