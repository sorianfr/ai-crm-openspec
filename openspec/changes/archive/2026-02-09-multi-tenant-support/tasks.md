## 1. Models and migrations

- [x] 1.1 Add Tenant model (id, name, created_at) and create tenants table via Alembic migration
- [x] 1.2 Add tenant_id as nullable column to users, contacts, companies, notes, activities, audit_logs; create default tenant row in migration
- [x] 1.3 Backfill tenant_id on all existing rows to default tenant id
- [x] 1.4 Alter tenant_id columns to NOT NULL, add FK constraints to tenants.id, add indexes on tenant_id (and optional composite indexes)

## 2. Seed update (dev bootstrap)

- [x] 2.1 Update app/core/seed.py: ensure default tenant exists; ensure admin user exists and has tenant_id set to that tenant (APP_ENV=development only)

## 3. Auth changes

- [x] 3.1 Include tenant_id in JWT payload on login (create_access_token); ensure User model has tenant_id available
- [x] 3.2 Add get_current_tenant dependency (or equivalent) that returns tenant_id/tenant from get_current_user
- [x] 3.3 Ensure get_current_user resolves user from DB and user carries tenant_id; tokens without tenant_id claim accepted via DB lookup (backwards compatibility)

## 4. Tenant scoping – contacts, companies, notes, activities

- [x] 4.1 Apply tenant scoping to contacts CRUD: list filter by tenant_id; get/update/delete by (id, tenant_id) with 404 on wrong tenant; create with tenant_id = current_user.tenant_id
- [x] 4.2 Apply tenant scoping to companies CRUD: same pattern as contacts
- [x] 4.3 Apply tenant scoping to contact-notes: notes have tenant_id; create note under contact only if contact.tenant_id = current_user.tenant_id (404 otherwise); list/delete scoped by tenant
- [x] 4.4 Apply tenant scoping to contact-activities: same pattern as notes

## 5. Audit helper and user-management

- [x] 5.1 Update audit helper (log_audit) to accept and persist tenant_id; all call sites pass current_user.tenant_id
- [x] 5.2 Ensure user-management (POST/GET/PATCH users) and any other audit call sites pass tenant_id; user list scoped by tenant if applicable

## 6. Verification

- [x] 6.1 Verification plan (no new public APIs for tenant creation): create two tenants A and B and two users (one admin per tenant) via DB script or migration; login as tenant A user, create contact, confirm it appears only for tenant A; attempt to access tenant B contact id as tenant A user and confirm 404; verify audit_logs rows have correct tenant_id and are filtered by tenant
