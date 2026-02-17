## 1. Add PostgreSQL driver

- [x] 1.1 Add psycopg[binary]>=3.1 (psycopg v3) to requirements.txt so that SQLAlchemy can connect to PostgreSQL when DATABASE_URL is postgresql+psycopg://
- [x] 1.2 Ensure app/db/session.py keeps SQLite-only logic (connect_args, foreign_keys event) conditional on sqlite only; no regression for PostgreSQL when DATABASE_URL is postgresql+psycopg://

## 2. Documentation

- [x] 2.1 Document that production can use PostgreSQL by setting DATABASE_URL to postgresql+psycopg://user:pass@host:5432/dbname (e.g. in README or env example)

## 3. Verification

- [x] 3.1 Verify app starts and runs with DATABASE_URL=sqlite:///./app.db (unchanged)
- [x] 3.2 Verify app can connect and run with a PostgreSQL DATABASE_URL when a Postgres instance is available (or document that manual verification is required)
