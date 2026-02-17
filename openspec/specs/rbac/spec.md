# Role-Based Access Control (RBAC)

The system SHALL enforce role-based authorization on selected endpoints. Users SHALL have a role (admin, manager, sales). Protected routes SHALL require an authenticated user and SHALL allow access only when the user's role is in the set of allowed roles; otherwise the system SHALL return 403 Forbidden.

## Requirements

### Requirement: User model with role

The system SHALL persist a user role for each user so that authorization decisions can be made from the authenticated identity.

#### Scenario: Role field on user
- **WHEN** examining the user data model
- **THEN** each user SHALL have a role field (or equivalent) with values restricted to: admin, manager, sales
- **AND** the role SHALL be persisted and SHALL be available after authentication (e.g. in JWT claims and/or loaded user object)

#### Scenario: Roles are consistent with JWT
- **WHEN** a JWT is issued at login
- **THEN** the token SHALL include the user's role (e.g. in a role claim)
- **AND** when the current user is resolved for a request (e.g. via get_current_user), the role SHALL be available for authorization checks

### Requirement: get_current_user dependency

The system SHALL provide a reusable dependency (e.g. get_current_user) that resolves the current user from the request (e.g. from Authorization Bearer JWT) and SHALL use it on protected routes.

#### Scenario: Resolve user from valid token
- **WHEN** a request to a protected route includes a valid, non-expired JWT in Authorization Bearer
- **THEN** the dependency SHALL decode the token, SHALL resolve the user (e.g. by sub), and SHALL provide the user object to the route handler
- **AND** the route handler SHALL receive the authenticated user

#### Scenario: No user when unauthenticated
- **WHEN** a request to a protected route does not include a valid token (missing, invalid, or expired)
- **THEN** the dependency SHALL not invoke the route handler and SHALL cause the response to be 401 Unauthorized

### Requirement: require_roles dependency

The system SHALL provide a reusable dependency (e.g. require_roles) that restricts access to users whose role is in a given set of allowed roles.

#### Scenario: Access allowed when role in allowed set
- **WHEN** a request to a route protected by require_roles(allowed_roles) is made and the current user's role is in allowed_roles
- **THEN** the route handler SHALL be invoked and SHALL receive the current user

#### Scenario: 403 when role not allowed
- **WHEN** a request to a route protected by require_roles(allowed_roles) is made and the current user's role is NOT in allowed_roles
- **THEN** the system SHALL respond with HTTP 403 Forbidden
- **AND** SHALL NOT execute the protected handler

#### Scenario: 403 after successful authentication
- **WHEN** the request is authenticated (valid JWT) but the user's role is not in the set required by the endpoint
- **THEN** the response SHALL be 403 Forbidden (not 401), indicating valid identity but insufficient permission
