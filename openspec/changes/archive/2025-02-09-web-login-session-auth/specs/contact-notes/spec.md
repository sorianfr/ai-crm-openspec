## ADDED Requirements

### Requirement: Web routes require session authentication and CSRF

All note web routes (create, delete) SHALL require session authentication and CSRF validation on mutations.

#### Scenario: Unauthenticated access redirects to login
- **WHEN** an unauthenticated request is made to a note web route
- **THEN** the system SHALL redirect to /login
- **AND** SHALL NOT create or delete notes

#### Scenario: Mutations require CSRF
- **WHEN** a POST request creates or deletes a note
- **THEN** the request SHALL include a valid CSRF token
- **AND** SHALL be rejected with 403 if the token is missing or invalid

#### Scenario: Tenant scoping preserved
- **WHEN** note web routes are accessed by an authenticated user
- **THEN** tenant scoping SHALL remain in effect (notes created under contacts in current tenant; cross-tenant access returns 404)
