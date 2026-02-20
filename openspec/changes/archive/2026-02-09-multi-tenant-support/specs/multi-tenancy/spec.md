# Multi-tenancy

The system SHALL support multiple tenants (companies) on a shared database with strict row-level isolation via `tenant_id`. All list endpoints SHALL filter by tenant_id; reads/updates/deletes by id SHALL query by (id, tenant_id) and return 404 on cross-tenant access; writes SHALL set tenant_id server-side from the current user. Existing data SHALL be migrated to a default tenant; tenant_id columns SHALL become NOT NULL after backfill.

## Goal and non-goals

**Goal:** SaaS-ready multi-tenant isolation: tenants table, tenant_id on users and core entities, tenant-scoped queries and mutations, dev bootstrap (default tenant + admin), migration/backfill so existing rows get a default tenant.

**Non-goals:** OAuth/OIDC; advanced tenant admin UI; separate database per tenant; superadmin or cross-tenant access.

## ADDED Requirements

### Requirement: Tenant model

The system SHALL persist tenants in a `tenants` table with id, name, and created_at.

#### Scenario: Tenants table exists
- **WHEN** examining the data layer
- **THEN** a tenants table SHALL exist with columns id (primary key), name (string), created_at (timestamp)
- **AND** the application SHALL use this table as the source of tenant records

### Requirement: Tenant scoping – list endpoints

All list (index) endpoints for tenant-scoped entities SHALL return only rows where tenant_id matches the current user's tenant_id.

#### Scenario: List filtered by tenant
- **WHEN** a list endpoint for contacts, companies, notes, activities, users, or audit_logs is invoked by an authenticated user
- **THEN** the query SHALL filter by tenant_id = current_user.tenant_id
- **AND** the response SHALL contain only records belonging to that tenant

### Requirement: Tenant scoping – reads/updates/deletes by id

Reads, updates, and deletes that target a record by id SHALL query by (id, tenant_id). If the record exists but belongs to another tenant, the system SHALL return 404 (no cross-tenant access or tenant enumeration).

#### Scenario: Get by id returns 404 when wrong tenant
- **WHEN** a request to read, update, or delete a record by id is made and the record exists but has a different tenant_id than the current user
- **THEN** the system SHALL respond with 404 Not Found
- **AND** SHALL NOT return or modify the record

#### Scenario: Get by id returns record when same tenant
- **WHEN** a request to read, update, or delete a record by id is made and the record has the same tenant_id as the current user
- **THEN** the system SHALL return or modify the record as appropriate
- **AND** SHALL NOT expose other tenants' data

### Requirement: Tenant scoping – writes set tenant_id server-side

On create, the system SHALL set tenant_id from current_user.tenant_id server-side. Client-provided tenant_id SHALL be ignored.

#### Scenario: Create sets tenant from current user
- **WHEN** a new contact, company, note, activity, user, or audit_log entry is created
- **THEN** tenant_id SHALL be set to current_user.tenant_id
- **AND** any tenant_id supplied in the request body or URL SHALL be ignored

### Requirement: Dev bootstrap (development only)

When APP_ENV=development, the system SHALL ensure a default tenant exists and an admin user is assigned to that tenant (e.g. for local login and testing).

#### Scenario: Default tenant and admin in development
- **WHEN** the application starts with APP_ENV=development
- **THEN** the bootstrap logic SHALL ensure at least one tenant exists (e.g. name "Default")
- **AND** SHALL ensure an admin user exists and has tenant_id set to that default tenant
- **AND** SHALL NOT create multiple tenants by default unless explicitly added for testing

#### Scenario: No bootstrap in production
- **WHEN** APP_ENV is not development
- **THEN** the application SHALL NOT create a default tenant or admin as part of startup
- **AND** tenant and user creation SHALL be via migrations or explicit operations only

### Requirement: Migration and backfill

Existing rows in tenant-scoped tables SHALL be assigned to a default tenant via backfill. After backfill, tenant_id columns SHALL be NOT NULL and SHALL have foreign key constraints to tenants.id.

#### Scenario: Backfill to default tenant
- **WHEN** migrations are run for multi-tenant-support
- **THEN** a default tenant row SHALL be created if not present
- **AND** all existing rows in users, contacts, companies, notes, activities, and audit_logs SHALL have tenant_id set to that default tenant's id
- **AND** thereafter tenant_id columns SHALL be altered to NOT NULL with FK and indexes as specified in the design

### Requirement: Testing acceptance – cross-tenant isolation

A user in tenant A SHALL NOT be able to read, update, or delete resources belonging to tenant B. Access attempts SHALL result in 404 (or 403 where appropriate).

#### Scenario: Tenant A cannot access tenant B resource by id
- **WHEN** a user belonging to tenant A requests a resource by id that belongs to tenant B
- **THEN** the system SHALL respond with 404 Not Found (or 403 Forbidden)
- **AND** SHALL NOT return or modify tenant B's data

#### Scenario: Tenant A list does not include tenant B data
- **WHEN** a user belonging to tenant A requests a list of contacts, companies, notes, or activities
- **THEN** the response SHALL contain only records with tenant_id equal to tenant A
- **AND** SHALL NOT include any records belonging to tenant B
