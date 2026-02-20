# Proposal — multi-tenant support (tenant_id scoping)

## Why

We need to turn the CRM into a SaaS-ready system where multiple companies (tenants) can use the same application with strict data isolation. Tenant-scoped data and tenant_id in auth will enable multi-company use on a single deployment.

## What Changes

- Add **tenants** table and link users to tenants (`users.tenant_id`).
- Add **tenant_id** to core business entities: contacts, companies, notes, activities, and to **audit_logs**.
- Include **tenant_id** in JWT claims and resolve tenant from the authenticated user.
- Enforce **tenant scoping** on all queries and mutations (no cross-tenant access); user from tenant A cannot read or write tenant B data (404 or 403).
- Add minimal **tenant bootstrap for development** only: create a default tenant and admin user when `APP_ENV=development`.
- **BREAKING:** Existing data without tenant_id will be migrated/backfilled to a default tenant.

All new records SHALL be created with `current_user.tenant_id`. Audit logs SHALL include tenant_id and SHALL be scoped by tenant.

## Capabilities

### New Capabilities

- **multi-tenancy**: Tenant model and table; tenant_id on users and core entities; tenant resolution from JWT/user; query and mutation scoping; dev bootstrap (default tenant + admin). Acceptance: user from tenant A cannot read/write tenant B data; all new records use current_user.tenant_id; audit logs include tenant_id and are scoped.

### Modified Capabilities

- **jwt-auth**: Include tenant_id (e.g. tenant claim) in JWT and in token validation so tenant is available for scoping.
- **contacts-crud**: All contact queries and mutations scoped by tenant_id; create with current tenant.
- **companies-crud**: All company queries and mutations scoped by tenant_id; create with current tenant.
- **contact-notes**: Notes scoped by tenant (via contact or explicit tenant_id).
- **contact-activities**: Activities scoped by tenant (via contact or explicit tenant_id).
- **audit-logs**: Audit log entries include tenant_id; list/query audit logs scoped by tenant where applicable.

## Impact

- **Data model:** New `tenants` table; `tenant_id` (FK) on users, contacts, companies, notes, activities, audit_logs. Migrations and backfill for existing rows to a default tenant.
- **APIs:** No new public endpoints; existing endpoints behave tenant-scoped. Unauthorized cross-tenant access returns 404 or 403.
- **Auth:** JWT payload and get_current_user (or tenant resolution) expose tenant_id; all scoping uses it.
- **Configuration:** Optional dev bootstrap when APP_ENV=development (default tenant + admin).

## Non-Goals

- OAuth/OIDC.
- Advanced tenant admin UI.
- Separate database per tenant.

## Acceptance

- User from tenant A cannot read or write tenant B data (returns 404 or 403).
- All new records are created with `current_user.tenant_id`.
- Audit logs include tenant_id and are scoped as well.
