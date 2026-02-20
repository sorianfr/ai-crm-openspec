## MODIFIED Requirements

### Requirement: Notes are tenant-scoped

Notes SHALL have tenant_id and SHALL only be accessible when they match the current user's tenant. Creating a note under a contact SHALL enforce that the contact belongs to the current tenant; otherwise the system SHALL return 404.

#### Scenario: Note has tenant_id and matches current tenant
- **WHEN** a note is created, read, updated, or deleted
- **THEN** the note SHALL have tenant_id set to current_user.tenant_id (on create)
- **AND** reads/updates/deletes SHALL resolve the note (and contact if applicable) within the current tenant
- **AND** cross-tenant access SHALL return 404

#### Scenario: Create note under contact enforces same tenant
- **WHEN** a note is created under a contact (e.g. POST /contacts/{id}/notes)
- **THEN** the system SHALL verify the contact exists and has tenant_id = current_user.tenant_id
- **AND** if the contact does not exist or belongs to another tenant SHALL return 404
- **AND** the new note SHALL have tenant_id = current_user.tenant_id

#### Scenario: List and delete notes scoped by tenant
- **WHEN** notes are listed for a contact or a note is deleted by id
- **THEN** the contact (if used) SHALL be resolved within the current tenant
- **AND** the note SHALL be resolved within the current tenant
- **AND** SHALL NOT return or modify notes belonging to other tenants
