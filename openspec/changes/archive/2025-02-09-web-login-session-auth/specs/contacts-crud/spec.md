## ADDED Requirements

### Requirement: Web routes require session authentication

All contact web routes SHALL require session-based authentication. Mutations SHALL require CSRF. RBAC enforced for create (admin/manager). Tenant scoping preserved.

#### Scenario: Unauthenticated redirects to login
- **WHEN** an unauthenticated request is made to GET /contacts
- **THEN** the system SHALL redirect to /login

#### Scenario: Mutations require CSRF
- **WHEN** a POST creates, updates, or deletes a contact
- **THEN** the request SHALL include a valid CSRF token or SHALL be rejected with 403

#### Scenario: Create contact RBAC
- **WHEN** a user attempts to create a contact
- **THEN** the user role SHALL be admin or manager; sales SHALL receive 403

#### Scenario: Tenant scoping preserved
- **WHEN** contact web routes are accessed
- **THEN** tenant scoping SHALL remain in effect
