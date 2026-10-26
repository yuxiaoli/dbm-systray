# Command reference. Copy individual examples from the repository root.
# NEVER execute/source this file. This is a Windows desktop tray application;
# PowerShell examples below are commented, not Bash commands.
# Static QA only: no GUI, local DB, editor, server or dependency was executed.
# Requires Windows, an interactive desktop, Python ^3.10, and required tools.
# app.py imports Windows-only CREATE_NEW_CONSOLE at module import, so its
# platform.system checks do NOT make it portable to macOS/Linux.

# === PowerShell setup: choose ONE installation method ===
# Manifest/lock option (includes json-manager-cli for the JsonCli menu):
# poetry install
# README alternative, using a new dedicated environment:
# python -m venv venv
# .\venv\Scripts\python.exe -m pip install -r requirements.txt
# requirements.txt omits manifest's json-manager-cli; JsonCli will need its
# executable already available. No automatic dependency change is done here.
# These examples use the venv interpreter directly; no activation-policy changes.

# === Required configuration BEFORE startup OR help ===
# app.py checks configs/config.json at import, before parsing -c/--config/-h.
# That DEFAULT file must already exist even if using a different --config path.
# No config file is shipped; user must supply an authorized local one.
# README schema: JSON array of objects {"name":"YOUR_LABEL","path":"YOUR_FILE.sqlite"}
# or .json paths. No JSON Schema validation is actually performed at runtime.
# Paths are relative to the process working directory unless absolute.
# Never point this tray app at real databases without backup/authorization:
# menu tools can edit database/JSON contents; no read-only wrapper exists.

# Help works only after the above platform/import/default-config prerequisites.
# poetry run python src/db_manager/app.py --help
# .\venv\Scripts\python.exe src/db_manager/app.py --help

# === PowerShell launch variants; opens the system tray ===
# Default config and ten ports 8080..8089:
# poetry run python src/db_manager/app.py
# Custom config only (default file must STILL exist due to import-time check):
# poetry run python src/db_manager/app.py --config "YOUR_CONFIG.json"
# Custom ports: START COUNT, NOT start/end. Allocates from highest port downward.
# poetry run python src/db_manager/app.py --ports 18080 5
# poetry run python src/db_manager/app.py -c "YOUR_CONFIG.json" -p 18080 5
# README venv equivalent:
# .\venv\Scripts\python.exe src/db_manager/app.py -c "YOUR_CONFIG.json" -p 18080 5
# There is no port-range validation or collision probe. Use a positive count,
# legal nonprivileged available ports; failed launches can consume pool entries.

# === Environment and tray actions (GUI, not invented CLI subcommands) ===
# load_dotenv(override=True) reads .env and can replace existing environment values.
# Use trusted local executable paths, not credentials or arbitrary shell snippets:
# EDITOR: JSON/config editor (Windows default notepad).
# SQLITE_BROWSER_EXE: SQLite Browser executable (no fallback in source).
# SQLITE_WEB: sqlite_web executable (default sqlite_web).
# LITECLI: litecli executable (default litecli).
# JSONCLI: jsoncli executable (default jsoncli; omitted from README env list).
# .sqlite menu: SQLite Browser; LiteCli; sqlite-web > Start server/Stop server/
# Web page; Open directory. .json menu: Edit...; JsonCli; Open directory.
# Starting sqlite-web launches a real local database web interface. The wrapper
# supplies ONLY port and file path, no authentication/read-only/host flags.
# Do not expose it to other machines; review tool defaults before intentional use.
# Web page opens http://127.0.0.1:ALLOCATED_PORT in the browser.
# External terminal commands interpolate paths without safe quoting; spaces and
# shell metacharacters can break invocation or cause unintended shell behavior.
# Treat executable values and paths as trusted input; this reference is no fix.
# Configuration > Edit opens the chosen config; Reload rebuilds menus but does
# not stop previously started servers or reload .env.
# Quit terminates tracked sqlite-web processes, waits, then closes the tray.
# No runtime CLI flags exist to start/stop a particular database or reload config.
# No project-defined tests/lint/build/release commands; tests only has __init__.py.
