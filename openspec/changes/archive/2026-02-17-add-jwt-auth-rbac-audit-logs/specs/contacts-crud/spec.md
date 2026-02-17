## ADDED Requirements

### Requirement: Protected contact endpoints

At least one contact CRUD endpoint SHALL require JWT authentication and role-based authorization. Unauthenticated requests SHALL receive 401 Unauthorized; authenticated requests whose role is not allowed SHALL receive 403 Forbidden.

#### Scenario: At least one endpoint requires auth and RBAC
- **WHEN** the contacts-crud capability is implemented with auth/RBAC
- **THEN** at least one of the contact routes (e.g. POST `/contacts`, POST `/contacts/{id}`, POST `/contacts/{id}/delete`, or GET list/detail/edit) SHALL require a valid JWT (e.g. via get_current_user) and SHALL require the user's role to be in a defined set (e.g. via require_roles)
- **AND** requests without a valid Bearer token SHALL receive 401 Unauthorized
- **AND** requests with a valid token but insufficient role SHALL receive 403 Forbidden

#### Scenario: Protected endpoint behavior
- **WHEN** a request to a protected contact endpoint is made with a valid JWT and an allowed role
- **THEN** the route handler SHALL execute normally and SHALL return the usual success or error response (e.g. 200, 302, 404) according to the existing contacts-crud requirements
