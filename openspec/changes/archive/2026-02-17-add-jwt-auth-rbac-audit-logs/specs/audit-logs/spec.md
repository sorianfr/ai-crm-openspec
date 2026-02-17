# Audit logs

The system SHALL persist an audit trail of CREATE, UPDATE, and DELETE operations on core entities (e.g. Contact, Company). Each audit entry SHALL record who performed the action, when, and which entity was affected, so that changes can be reviewed and attributed.

## ADDED Requirements

### Requirement: Audit log persistence

The system SHALL maintain an audit_logs (or equivalent) persistence layer that stores one record per audited action.

#### Scenario: Audit log table or equivalent
- **WHEN** examining the data layer
- **THEN** an audit log store SHALL exist (e.g. audit_logs table) with at least: identifier, timestamp, user identifier (nullable if action is unauthenticated), action (CREATE/UPDATE/DELETE), entity type (e.g. contact, company), entity id, and optional summary or changed-fields data
- **AND** entries SHALL be persisted via the same database session/engine as the rest of the application

#### Scenario: Audit entry created on entity create
- **WHEN** a core entity (e.g. Contact or Company) is created and the transaction is committed
- **THEN** the system SHALL write an audit log entry with action CREATE, the entity type, and the new entity's id
- **AND** the entry SHALL include timestamp and, when available, the user id of the actor

#### Scenario: Audit entry created on entity update
- **WHEN** a core entity (e.g. Contact or Company) is updated and the transaction is committed
- **THEN** the system SHALL write an audit log entry with action UPDATE, the entity type, and the entity's id
- **AND** the entry SHALL include timestamp and, when available, the user id of the actor

#### Scenario: Audit entry created on entity delete
- **WHEN** a core entity (e.g. Contact or Company) is deleted and the transaction is committed
- **THEN** the system SHALL write an audit log entry with action DELETE, the entity type, and the entity's id (before deletion)
- **AND** the entry SHALL include timestamp and, when available, the user id of the actor

### Requirement: Automatic audit on mutation

Audit entries for core entities SHALL be created automatically by the application when mutations are performed, not only when manually requested.

#### Scenario: No extra client action required
- **WHEN** a client creates, updates, or deletes a core entity through the normal API or routes
- **THEN** the corresponding audit log entry SHALL be written as part of the same operation (e.g. on commit or after flush)
- **AND** the client SHALL NOT be required to call a separate audit API to record the action
