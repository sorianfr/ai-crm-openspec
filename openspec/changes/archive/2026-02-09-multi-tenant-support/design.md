# Design — multi-tenant-support

## Context

The CRM is a FastAPI app using SQLAlchemy ORM and Alembic migrations. The system currently supports authentication (JWT) and RBAC (roles: admin/manager/sales) with a single shared database and **no tenant isolation**. Core persisted entities include:

- `app/models/contact.py` (contacts)
- `app/models/company.py` (companies)
- `app/models/note.py` (notes)
- `app/models/activity.py` (activities)
- `app/models/user.py` (users)
- `app/models/audit_log.py` (audit_logs)

Routes are implemented in `app/routes/*` (notably `contacts.py`, `companies.py`, `users.py`). Auth helpers are in `app/core/auth.py`; password hashing is in `app/core/password.py`; audit helper is in `app/core/audit.py`. SQLite foreign keys are enabled via a connect event in `app/db/session.py` (`PRAGMA foreign_keys=ON` when using sqlite).

This change introduces **multi-tenant support** using a shared database with strict row-level isolation by `tenant_id` across users and core entities, plus a breaking migration/backfill strategy for existing data.

## Goals / Non-Goals

**Goals:**

- Shared DB multi-tenancy with strict isolation enforced via `tenant_id` columns on core tables.
- Tenant source of truth is the **database**: enforcement MUST be based on `current_user.tenant_id` resolved from DB.
- Isolation behavior:
  - Reads by id query by `(id, tenant_id)` and return **404** if the record exists but belongs to another tenant (avoid tenant enumeration).
  - List endpoints return only rows filtered by `tenant_id`.
  - Writes always set `tenant_id = current_user.tenant_id` server-side; ignore any client-provided tenant_id.
- Scope applies to: users, contacts, companies, notes, activities, audit_logs (and any join tables, if present).
- Dev bootstrap (development only): ensure a default tenant exists and an admin user is assigned to it when `APP_ENV=development`.

**Non-Goals:**

- OAuth/OIDC and external providers.
- Advanced tenant admin UI.
- Separate database per tenant.
- “Superadmin” cross-tenant access (admin is tenant-local only).

## Decisions

### Tenancy model: shared DB with row-level isolation

- **Decision:** Use a single shared database and enforce tenant isolation via `tenant_id` columns and tenant-scoped queries.
- **Rationale:** Matches the goal of SaaS readiness without separate DBs and keeps operational complexity low.

### Tenant source of truth: DB user record

- **Decision:** Use `current_user.tenant_id` resolved from the DB as the source of truth for enforcement. JWT `tenant_id` claim MAY be included as an optimization, but enforcement MUST rely on the resolved user from DB.
- **Rationale:** Prevents stale/forged tenant context and ensures that changes to user/tenant assignments take effect consistently.

### Isolation behavior: 404 for cross-tenant reads-by-id

- **Decision:** For id-based reads/updates/deletes, query by `(id, tenant_id)` and return 404 when not found (including “exists but other tenant”).
- **Rationale:** Avoids tenant enumeration and matches common SaaS security patterns.

### Data model changes

- **Decision:** Introduce `tenants` table and add `tenant_id` (NOT NULL, FK `tenants.id`) to:
  - `users.tenant_id`
  - `contacts.tenant_id`
  - `companies.tenant_id`
  - `notes.tenant_id`
  - `activities.tenant_id`
  - `audit_logs.tenant_id`
- **Rationale:** Consistent row-level scoping; enables DB indexing and efficient filtering.

### Indexing

- **Decision:** Add an index on `tenant_id` for each scoped table; optionally add composite indexes like `(tenant_id, id)` when beneficial.
- **Rationale:** Tenant filtering will be on the hot path for most queries.

### Auth/JWT changes (modified `jwt-auth`)

- **Decision:** On login, include tenant_id claim in the JWT payload: `sub`, `role`, `tenant_id`, `exp`.
- **Decision:** `get_current_user` continues to resolve the user from DB; the user object carries `tenant_id`.
- **Decision:** Add a `get_current_tenant` dependency (returning tenant_id or Tenant object) that derives from `get_current_user`.
- **Rationale:** Tenant context becomes a first-class dependency for scoping; JWT claim can avoid extra lookups in some paths but is not authoritative.

### Scoping implementation approach

- **Decision:** Provide a consistent, centralized pattern for tenant scoping to avoid scattered ad-hoc filters.
  - Option A: helper `tenant_filter(stmt, tenant_id)` returning `stmt.where(Model.tenant_id == tenant_id)`
  - Option B: CRUD/service helpers that always accept `tenant_id` and enforce it
- **Decision:** For mutations, always:
  - create: set `tenant_id = current_user.tenant_id` server-side
  - update/delete: fetch by `(id, tenant_id)`; if not found -> 404; then mutate
- **Rationale:** Reduces the chance of missing a filter and makes tenant-scoping reviewable.

### Audit logs (modified `audit-logs`)

- **Decision:** Audit entries include `tenant_id = current_user.tenant_id` for all audited actions, including user-management audits.
- **Rationale:** Audit must be tenant-scoped like all other data.

### SQLite foreign keys

- **Decision:** Continue relying on SQLite FK enforcement via `PRAGMA foreign_keys=ON` in `app/db/session.py` (already present and conditional on sqlite).
- **Rationale:** Ensures FK constraints behave as expected in dev/test when using SQLite.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Missing tenant filter on a query leads to data leakage | Centralize tenant scoping via helper/service layer; review all routes that touch scoped tables. |
| Breaking migration/backfill mistakes could lock deployments | Use safe Alembic order: nullable columns → backfill → NOT NULL + constraints; test on a copy of prod data. |
| JWT contains stale tenant_id after reassignment | Enforcement uses DB user record; stale token does not grant cross-tenant access. |
| Performance regression due to tenant filters | Add indexes on tenant_id (and composites as needed); verify query plans for common endpoints. |

## Migration Plan

**BREAKING**: existing data will be assigned to a default tenant.

Alembic migrations in safe order:

1. **Create `tenants` table** (`id`, `name`, `created_at`).
2. **Create one default tenant row** (e.g. name = "Default") as part of a data migration step.
3. **Add `tenant_id` columns as nullable** to existing tables: users, contacts, companies, notes, activities, audit_logs.
4. **Backfill tenant_id** for all existing rows to the default tenant id.
5. **Alter columns to NOT NULL** + add FK constraints + add indexes on tenant_id (and optional composite indexes).

Rollback strategy:

- Code rollback is straightforward, but DB rollback is more complex after NOT NULL + FK enforcement. Prefer rolling forward with a fixed migration. If down migrations are maintained, ensure they reverse indexes/constraints/columns in reverse order.

Dev bootstrap (development only):

- Update seeding logic in `app/core/seed.py` to:
  - ensure default tenant exists
  - ensure default admin user exists and has `tenant_id` set to that tenant

## Open Questions

- Whether to represent tenant scoping for notes/activities via explicit `tenant_id` only, or also rely on the parent contact relationship (the design requires explicit tenant_id columns either way).
- Whether audit log read APIs will be added later; for now the table and scoping must support tenant-safe access.

