## ADDED Requirements

### Requirement: Web routes require session authentication

All company web routes SHALL require session-based authentication. Mutations SHALL require CSRF. Tenant scoping preserved.

#### Scenario: Unauthenticated redirects to login
- **WHEN** an unauthenticated request is made to GET /companies
- **THEN** the system SHALL redirect to /login

#### Scenario: Mutations require CSRF
- **WHEN** a POST creates, updates, or deletes a company
- **THEN** the request SHALL include a valid CSRF token or SHALL be rejected with 403

#### Scenario: Tenant scoping preserved
- **WHEN** company web routes are accessed
- **THEN** tenant scoping SHALL remain in effect
