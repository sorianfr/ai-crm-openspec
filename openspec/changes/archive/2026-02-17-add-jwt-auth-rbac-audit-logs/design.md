# Design — add-jwt-auth-rbac-audit-logs

## Context

The CRM is a FastAPI app with SQLAlchemy, Alembic, and existing domain models: Contact, Company, Note, Activity. There is no user model or authentication today; routes are unprotected. This design adds JWT auth, RBAC (admin, manager, sales), and audit logging for entity mutations so the app is production-ready and auditable.

## Goals / Non-Goals

**Goals:**
- Stateless JWT authentication (HS256, expiration) with `/auth/login` and `Authorization: Bearer` on protected routes.
- Role-Based Access Control: user model with `role` (admin, manager, sales); reusable `get_current_user` and `require_roles` dependencies.
- Audit logging: persist CREATE/UPDATE/DELETE for core entities (e.g. Contact, Company) in an `audit_logs` table; write entries automatically on mutation.
- Protect at least one existing CRUD endpoint with auth + RBAC and return 401/403 when missing or insufficient.

**Non-Goals:**
- Multi-tenancy (separate change).
- OAuth or external identity providers.
- Refresh tokens (future enhancement).

## Decisions

### Authentication: JWT with HS256
- **Choice:** Access tokens as JWTs, signed with HS256, expiration from config.
- **Alternatives:** Session cookies (stateful), RS256 (adds key management). HS256 keeps ops simple; secret from env (e.g. `JWT_SECRET`).
- **Rationale:** Stateless, standard `Authorization: Bearer`, easy to validate in FastAPI dependencies.

### User model and credentials
- **Choice:** Add a `User` model (e.g. id, email, password_hash, role, created_at). Passwords hashed with a secure scheme (e.g. passlib + bcrypt).
- **Alternatives:** No local users / OAuth only (out of scope); storing plaintext (rejected).
- **Rationale:** Login must validate credentials; role is required for RBAC. Seed/migration for at least one user for dev and tests.

### RBAC: role enum and dependency
- **Choice:** Enum or string constraint for `admin`, `manager`, `sales`. `get_current_user` validates JWT and loads user; `require_roles(allowed_roles)` checks `current_user.role in allowed_roles`, else 403.
- **Alternatives:** Fine-grained permissions (deferred); no roles (rejected per proposal).
- **Rationale:** Simple, explicit, and sufficient for “at least one endpoint protected by auth + RBAC.”

### Audit log schema and trigger
- **Choice:** New table `audit_logs`: id, timestamp, user_id (nullable if not yet authenticated), action (CREATE/UPDATE/DELETE), entity_type (e.g. contact, company), entity_id, summary or changed fields (e.g. JSON or text). Write from application code on commit (e.g. after flush) for Contact and Company mutations.
- **Alternatives:** DB triggers (DB-specific, less portable); logging only to files (not queryable). Application-level writes keep logic in one place and work with SQLite and PostgreSQL.
- **Rationale:** Clear audit trail for who changed what and when; entity_type/entity_id support future queries and reporting.

### Which endpoints to protect first
- **Choice:** Protect at least one contacts-crud endpoint (e.g. create/update/delete contact) with `get_current_user` and `require_roles([...])`. Optionally protect one companies-crud endpoint; contact-notes/contact-activities can remain optional for this change.
- **Rationale:** Satisfies “at least one existing endpoint” and demonstrates the pattern; expansion can follow the same pattern.

### Configuration
- **Choice:** Env vars: `JWT_SECRET`, `JWT_EXPIRATION_MINUTES` (or seconds). Optional: `JWT_ALGORITHM` (default HS256). No secrets in code.
- **Rationale:** 12-factor; same pattern as existing `DATABASE_URL` / `APP_ENV`.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-------------|
| JWT secret weak or leaked | Document strong secret in production; rotate if compromised. |
| No refresh tokens | Short-lived access token; document future refresh flow. |
| Audit log volume | Index (user_id, entity_type, timestamp); optional retention/archival later. |
| Existing clients call newly protected endpoints | **BREAKING**: Document which endpoints now return 401/403; clients must use `/auth/login` and send Bearer token. |

## Migration Plan

1. Add dependency: PyJWT (and passlib/bcrypt or equivalent for password hashing).
2. Add User model and Alembic migration (users table with role).
3. Add audit_logs table and migration.
4. Implement `/auth/login`, JWT creation/validation, `get_current_user`, `require_roles`.
5. Add audit logging helper and call it on Contact/Company create/update/delete.
6. Protect selected contact (and optionally company) endpoints; add env vars to `.env.example` and README.
7. Seed one admin user for development (migration or script).
8. Deploy: set `JWT_SECRET` and optionally `JWT_EXPIRATION_*` in production; run migrations before traffic.

Rollback: revert code; migrations adding columns/tables can be reversed with down-revisions if needed. Existing data in users/audit_logs would remain unless explicitly dropped.

## Open Questions

- Exact list of endpoints to protect (e.g. POST/PUT/DELETE contact only, or also GET list/detail for contacts).
- Whether to audit Note/Activity in this change or limit to Contact and Company only (proposal says “core entities” — Contact and Company are the primary entities; Note/Activity can be deferred).
