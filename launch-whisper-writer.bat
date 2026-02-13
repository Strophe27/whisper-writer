@echo off
REM Store the directory where the batch file is located
set SCRIPT_DIR=%~dp0
REM Change directory to where this script is located
cd /d "%SCRIPT_DIR%"

REM --- Bypass proxy / Contourner le VPN (si le VPN utilise un proxy système) ---
REM Décommentez les 3 lignes ci-dessous pour que WhisperWriter ignore le proxy
REM et utilise votre connexion directe (IP normale) pour les API.
REM set NO_PROXY=*
REM set HTTP_PROXY=
REM set HTTPS_PROXY=

REM Run the app with full path
python "%SCRIPT_DIR%run.py"
REM When the app ends, optionally pause to view output
pause 