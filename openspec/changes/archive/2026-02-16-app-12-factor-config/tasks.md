## 1. Config from environment

- [x] 1.1 Add APP_ENV to app/core/config.py (read from env, default e.g. development)
- [x] 1.2 When APP_ENV is production, require DATABASE_URL to be set (fail fast at startup if missing); when not production, keep default DATABASE_URL for local dev
- [x] 1.3 Ensure DEBUG default remains false (or production-safe); no behavior change to existing DEBUG usage

## 2. Run contract for 0.0.0.0

- [x] 2.1 Ensure the standard run method uses uvicorn with --host 0.0.0.0 (add or update pyproject.toml script, Makefile, or README/run instructions)

## 3. Verification

- [x] 3.1 Verify APP_ENV, DATABASE_URL, DEBUG are loaded from env; production (APP_ENV=production) fails fast when DATABASE_URL unset; non-production starts with default DB
- [x] 3.2 Verify running the app via the standard run contract binds to 0.0.0.0 and is reachable from another interface or container
