# Multi-tenancy

The system SHALL support multiple tenants on a shared database with strict row-level isolation via tenant_id. All list endpoints SHALL filter by tenant_id; reads/updates/deletes by id SHALL query by (id, tenant_id) and return 404 on cross-tenant access; writes SHALL set tenant_id server-side from the current user.

## Requirements

### Requirement: Tenant model

The system SHALL persist tenants in a tenants table with id, name, and created_at.

### Requirement: Tenant scoping - list endpoints

All list endpoints for tenant-scoped entities SHALL return only rows where tenant_id matches the current user tenant_id.

### Requirement: Tenant scoping - reads/updates/deletes by id

Reads, updates, and deletes by id SHALL query by (id, tenant_id). If the record belongs to another tenant, the system SHALL return 404.

### Requirement: Tenant scoping - writes set tenant_id server-side

On create, tenant_id SHALL be set from current_user.tenant_id server-side. Client-provided tenant_id SHALL be ignored.

### Requirement: Dev bootstrap (development only)

When APP_ENV=development, the system SHALL ensure a default tenant exists and an admin user is assigned to that tenant.

### Requirement: Migration and backfill

Existing rows in tenant-scoped tables SHALL be assigned to a default tenant via backfill. tenant_id columns SHALL become NOT NULL with FK to tenants.id.
