# User management

The system SHALL provide API endpoints for admins to create users, list users, and update a user's role. All endpoints require JWT authentication; POST and PATCH require admin role; GET is admin-only for this change. Passwords SHALL be stored only as a hash and SHALL never be returned in responses. User create and role update SHALL be recorded in the audit log.

## Goal and non-goals

**Goal:** Enable enterprise user management via API: create users (POST /users), list users (GET /users), and change role (PATCH /users/{id}/role), all protected by auth and admin RBAC, with audit trail for create and role update.

**Non-goals:** No DELETE user in this change; no self-registration; no UI (API only).

## Requirements

### Requirement: Authentication and RBAC for user-management

All user-management endpoints SHALL require a valid JWT. POST /users and PATCH /users/{id}/role SHALL require the admin role. GET /users SHALL require the admin role for this change. Missing or invalid token SHALL result in 401; valid token with insufficient role SHALL result in 403.

#### Scenario: All endpoints require authentication
- **WHEN** a request to POST /users, GET /users, or PATCH /users/{id}/role is made without a valid Bearer token
- **THEN** the system SHALL respond with 401 Unauthorized
- **AND** SHALL NOT execute the handler

#### Scenario: POST and PATCH require admin role
- **WHEN** a request to POST /users or PATCH /users/{id}/role is made with a valid token but the user's role is not admin
- **THEN** the system SHALL respond with 403 Forbidden
- **AND** SHALL NOT execute the handler

#### Scenario: GET /users requires admin role
- **WHEN** a request to GET /users is made with a valid token but the user's role is not admin
- **THEN** the system SHALL respond with 403 Forbidden
- **AND** SHALL NOT execute the handler

#### Scenario: Admin can access all user-management endpoints
- **WHEN** a request to any user-management endpoint is made with a valid token and the user's role is admin
- **THEN** the system SHALL execute the handler and return the appropriate response

### Requirement: POST /users (create user)

The system SHALL provide POST /users to create a user. Request body SHALL contain email, password, and role. Role SHALL be one of admin, manager, sales. On success the system SHALL return 201 with body { id, email, role, created_at }. Password SHALL be stored only as a hash.

#### Scenario: Create user success
- **WHEN** a valid POST request is made to /users with body { email, password, role } where role is admin, manager, or sales
- **THEN** the system SHALL create the user with the given email, store the password as password_hash using the existing hashing utility, set role and created_at
- **AND** SHALL return 201 Created with body { id, email, role, created_at }
- **AND** SHALL NOT return password or password_hash

#### Scenario: Validations – email and password required
- **WHEN** a POST request to /users omits email or password or provides empty values
- **THEN** the system SHALL respond with 422 Unprocessable Entity (or equivalent validation error)
- **AND** SHALL NOT create a user

#### Scenario: Validation – role must be allowed
- **WHEN** a POST request to /users provides a role that is not one of admin, manager, sales
- **THEN** the system SHALL respond with 422 Unprocessable Entity
- **AND** SHALL NOT create a user

#### Scenario: Duplicate email
- **WHEN** a POST request to /users provides an email that already exists
- **THEN** the system SHALL respond with 409 Conflict
- **AND** SHALL NOT create a user
- **AND** SHALL NOT expose password_hash

#### Scenario: Invalid body
- **WHEN** a POST request to /users has a malformed or invalid body (e.g. wrong types, missing required fields)
- **THEN** the system SHALL respond with 422 Unprocessable Entity
- **AND** SHALL NOT create a user

### Requirement: GET /users (list users)

The system SHALL provide GET /users that returns a list of users. Response SHALL be 200 with a JSON array of objects each containing id, email, role, created_at. Response SHALL NOT include password or password_hash.

#### Scenario: List users success
- **WHEN** a valid GET request is made to /users by an authenticated admin
- **THEN** the system SHALL return 200 OK with a JSON array of user objects
- **AND** each object SHALL contain only id, email, role, created_at
- **AND** SHALL NOT include password or password_hash

#### Scenario: Empty list
- **WHEN** GET /users is called and no users exist
- **THEN** the system SHALL return 200 OK with an empty array

### Requirement: PATCH /users/{id}/role (update role)

The system SHALL provide PATCH /users/{id}/role to update a user's role. Request body SHALL contain role (admin, manager, or sales). On success the system SHALL return 200 with { id, email, role, created_at }. If the user is not found the system SHALL return 404.

#### Scenario: Update role success
- **WHEN** a valid PATCH request is made to /users/{id}/role with body { role } where role is admin, manager, or sales and the user exists
- **THEN** the system SHALL update the user's role
- **AND** SHALL return 200 OK with body { id, email, role, created_at }
- **AND** SHALL NOT return password or password_hash

#### Scenario: User not found
- **WHEN** a PATCH request is made to /users/{id}/role for a user id that does not exist
- **THEN** the system SHALL respond with 404 Not Found
- **AND** SHALL NOT update any user

#### Scenario: Invalid body or role
- **WHEN** a PATCH request to /users/{id}/role has invalid body or role not in admin, manager, sales
- **THEN** the system SHALL respond with 422 Unprocessable Entity
- **AND** SHALL NOT update the user

### Requirement: Security – no password in responses

The system SHALL never return password or password_hash in any user-management API response.

#### Scenario: User payload excludes secrets
- **WHEN** any user-management endpoint returns user data (POST 201, GET 200, PATCH 200)
- **THEN** the response body SHALL contain only id, email, role, created_at (or array thereof)
- **AND** SHALL NOT contain password, password_hash, or any secret field

### Requirement: Password storage

When creating a user via POST /users, the system SHALL store the password only as a one-way hash using the existing hashing utility (e.g. app/core/password.hash_password).

#### Scenario: Password stored as hash
- **WHEN** a user is created via POST /users
- **THEN** the system SHALL persist only password_hash (output of the existing hashing utility)
- **AND** SHALL NOT store plaintext password

### Requirement: Audit logging for user create and role update

The system SHALL write an audit log entry on successful user create and on successful role update. Entries SHALL NOT contain passwords or hashes.

#### Scenario: Audit on user create
- **WHEN** POST /users completes successfully (201)
- **THEN** the system SHALL write an audit log entry with action CREATE, entity_type user (or User), entity_id set to the new user's id, user_id set to the acting admin's id
- **AND** the summary SHALL NOT include password or password_hash

#### Scenario: Audit on role update
- **WHEN** PATCH /users/{id}/role completes successfully (200)
- **THEN** the system SHALL write an audit log entry with action UPDATE, entity_type user (or User), entity_id set to the user's id, user_id set to the acting admin's id
- **AND** the summary MAY describe the change (e.g. "role changed to X") without any secrets
