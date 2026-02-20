## MODIFIED Requirements

### Requirement: Activities are tenant-scoped

Activities SHALL have tenant_id and SHALL only be accessible when they match the current user's tenant. Creating an activity under a contact SHALL enforce that the contact belongs to the current tenant; otherwise the system SHALL return 404.

#### Scenario: Activity has tenant_id and matches current tenant
- **WHEN** an activity is created, read, updated, or deleted
- **THEN** the activity SHALL have tenant_id set to current_user.tenant_id (on create)
- **AND** reads/updates/deletes SHALL resolve the activity (and contact if applicable) within the current tenant
- **AND** cross-tenant access SHALL return 404

#### Scenario: Create activity under contact enforces same tenant
- **WHEN** an activity is created under a contact (e.g. POST /contacts/{id}/activities)
- **THEN** the system SHALL verify the contact exists and has tenant_id = current_user.tenant_id
- **AND** if the contact does not exist or belongs to another tenant SHALL return 404
- **AND** the new activity SHALL have tenant_id = current_user.tenant_id

#### Scenario: List and delete activities scoped by tenant
- **WHEN** activities are listed for a contact or an activity is deleted by id
- **THEN** the contact (if used) SHALL be resolved within the current tenant
- **AND** the activity SHALL be resolved within the current tenant
- **AND** SHALL NOT return or modify activities belonging to other tenants
