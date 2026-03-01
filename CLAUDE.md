# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Test Commands

```bash
make                        # Build all (.nw → .py and .tex)
cd src/weblogin && make      # Build source only
cd tests && make             # Run tests (poetry run pytest)
cd tests && poetry run pytest tests/test_kth.py  # Single test file
poetry build                 # Build distribution packages
```

Integration tests require environment variables `KTH_LOGIN` and `KTH_PASSWD`.

## Literate Programming (CRITICAL)

This project uses **noweb literate programming**. The `.nw` files are the source of truth — `.py` and `.tex` files in `src/` and `tests/` are **generated artifacts** and must never be edited directly.

### Workflow for changes

1. Edit the `.nw` file (e.g., `src/weblogin/kth.nw`)
2. Run `make` to regenerate `.py` and `.tex` files
3. Run tests with `cd tests && make`

### Noweb conventions

- Code chunks: `<<chunk name>>=` on its own line, reference with `<<chunk name>>`
- Quote identifiers in prose with `[[code]]` (not `\texttt{}`)
- Escape identifiers in chunk names: `<<restrict to [[show_tree]]>>=`
- LaTeX documentation: use `\enquote{}` for quotes, `\cref{}` for cross-references, `description` environment for labeled lists
- Keep lines under 80 characters
- Each function gets its own `<<functions>>=` chunk with explanatory prose before it
- Tests go in `<<test functions>>=` chunks immediately after the code they test (never grouped at the end)
- Prose should explain **why**, not restate what the code does
- Public functions need PEP-257 docstrings (for users of compiled `.py`) in addition to noweb prose (for maintainers reading `.nw`)

### Generated files in .gitignore

The `.py` files in `src/weblogin/` and `tests/` are generated — only `.nw` files are committed.

## Architecture

**weblogin** provides transparent automated login to web UIs via `requests.Session` wrapping.

### Core classes (`src/weblogin/init.nw`)

- **`AutologinSession(handlers)`** — extends `requests.Session`; intercepts HTTP requests and triggers login handlers when authentication is needed
- **`AutologinHandler`** — abstract base class with `need_login(response)` and `login(session, response, args, kwargs)` methods

### Login handlers

- **`UGlogin`** (`kth.nw`) — KTH UG authentication (login.ug.kth.se)
- **`SAMLlogin`** (`kth.nw`) — KTH SAML authentication
- **`SSOlogin`** (`ladok.nw`) — LADOK SSO via SeamlessAccess

### Utility module

- **`seamlessaccess.py`** (`seamlessaccess.nw`) — client for the SeamlessAccess.org API to look up institution identity providers

### Usage pattern

```python
import weblogin
from weblogin.kth import UGlogin

session = weblogin.AutologinSession([
    UGlogin(username, password, "https://app.kth.se/")
])
response = session.get("https://app.kth.se/api/endpoint")
```

## Project Structure

```
src/weblogin/     # .nw source files → generates .py and .tex
tests/            # .nw source files → generates test .py files
doc/              # LaTeX documentation wrappers
makefiles/        # Git submodule with shared Makefile rules
```
