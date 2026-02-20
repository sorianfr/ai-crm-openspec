## MODIFIED Requirements

### Requirement: Audit log persistence (tenant-scoped)

Audit_logs SHALL have tenant_id (NOT NULL) and be tenant-scoped. All writes SHALL set tenant_id = current_user.tenant_id. Reads SHALL be scoped by tenant_id.

#### Scenario: Audit writes set tenant_id
- **WHEN** an audit log entry is written
- **THEN** tenant_id SHALL be set to current_user.tenant_id
- **AND** audit_logs table SHALL have tenant_id NOT NULL

#### Scenario: Audit reads scoped by tenant
- **WHEN** audit log entries are queried or listed
- **THEN** queries SHALL filter by tenant_id = current_user.tenant_id
- **AND** SHALL NOT return other tenants' entries
