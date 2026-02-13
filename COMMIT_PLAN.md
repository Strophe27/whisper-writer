# Commit plan for fork changes

Use these commits in order. Run from the repo root (e.g. in the terminal integrated in Cursor).

**Note:** Do not commit `src/config.json` (it can contain API keys; it is in `.gitignore`). The `0.4.7` file/folder is untracked; add it to `.gitignore` or commit it only if you know what it is.

---

## Commit 1 – Persistent logging and crash handling

**Message:**
```
Add persistent logging and crash handling for debugging

- Add src/logger_config.py: rotating file log (logs/whisper-writer.log),
  excepthook for unhandled exceptions, message sanitization for binary data
- run.py: init logging early, wrap main.py launch in try/except, log exit code
- main.py: call setup_logging() and install_excepthook() at startup
- result_thread.py: use logging.exception() instead of traceback.print_exc()
- utils.py: log config/.env errors and console_print output to file
- .gitignore: add logs/ and src/config.json
```

**Files to stage:**
```
git add src/logger_config.py run.py src/main.py src/result_thread.py src/utils.py .gitignore
git commit -m "Add persistent logging and crash handling for debugging

- Add src/logger_config.py: rotating file log (logs/whisper-writer.log),
  excepthook for unhandled exceptions, message sanitization for binary data
- run.py: init logging early, wrap main.py launch in try/except, log exit code
- main.py: call setup_logging() and install_excepthook() at startup
- result_thread.py: use logging.exception() instead of traceback.print_exc()
- utils.py: log config/.env errors and console_print output to file
- .gitignore: add logs/ and src/config.json"
```

---

## Commit 2 – Windows launcher and startup shortcut

**Message:**
```
Add Windows batch launcher and startup shortcut script

- launch-whisper-writer.bat: run app from project dir, optional proxy bypass
- create-shortcut.ps1: create shortcut in Startup folder (edit paths for your install)
```

**Files to stage:**
```
git add launch-whisper-writer.bat create-shortcut.ps1
git commit -m "Add Windows batch launcher and startup shortcut script

- launch-whisper-writer.bat: run app from project dir, optional proxy bypass
- create-shortcut.ps1: create shortcut in Startup folder (edit paths for your install)"
```

---

## Commit 3 – API-only requirements

**Message:**
```
Add requirements-api-only.txt for API-only installs

Deps for transcription/LLM via APIs only (no local Whisper/Vosk).
```

**Files to stage:**
```
git add requirements-api-only.txt
git commit -m "Add requirements-api-only.txt for API-only installs

Deps for transcription/LLM via APIs only (no local Whisper/Vosk)."
```

---

## Commit 4 – Document fork changes in README and CHANGELOG

**Message:**
```
Document fork changes in README and CHANGELOG

- README: 'Changes in this fork' section (logging, launcher, VPN, Groq)
- README: translate VPN section to English
- CHANGELOG: add Unreleased entry for fork additions and fixes
```

**Files to stage:**
```
git add README.md CHANGELOG.md
git commit -m "Document fork changes in README and CHANGELOG

- README: 'Changes in this fork' section (logging, launcher, VPN, Groq)
- README: translate VPN section to English
- CHANGELOG: add Unreleased entry for fork additions and fixes"
```

---

## Optional: single commit

If you prefer one commit for everything:

```
git add src/logger_config.py run.py src/main.py src/result_thread.py src/utils.py .gitignore launch-whisper-writer.bat create-shortcut.ps1 requirements-api-only.txt README.md CHANGELOG.md
git commit -m "Fork: logging, Windows launcher, VPN docs, API-only deps

- Add persistent logging (logs/whisper-writer.log) and excepthook for debugging
- Add launch-whisper-writer.bat and create-shortcut.ps1 for Windows
- README: fork changes section, VPN in English, Groq note
- requirements-api-only.txt, CHANGELOG updated"
```

Do not add: `src/config.json`, `.env`, or `0.4.7` unless you intend to track them.
