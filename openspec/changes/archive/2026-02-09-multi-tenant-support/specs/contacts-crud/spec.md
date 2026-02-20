## MODIFIED Requirements

### Requirement: Contacts are tenant-scoped

All contact list, query, and mutations SHALL be scoped by current_user.tenant_id. Cross-tenant access by id SHALL return 404. New contacts SHALL be created with current tenant.

#### Scenario: List filtered by tenant
- **WHEN** contacts are listed or searched
- **THEN** the query SHALL filter by tenant_id = current_user.tenant_id

#### Scenario: Read/update/delete by id returns 404 when wrong tenant
- **WHEN** a contact is read, updated, or deleted by id and belongs to another tenant
- **THEN** the system SHALL return 404 Not Found

#### Scenario: Create sets current tenant
- **WHEN** a new contact is created
- **THEN** tenant_id SHALL be set to current_user.tenant_id
- **AND** client-provided tenant_id SHALL be ignored
