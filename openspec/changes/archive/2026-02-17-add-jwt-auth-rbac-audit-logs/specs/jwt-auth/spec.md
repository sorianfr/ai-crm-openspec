# JWT authentication

The system SHALL authenticate API clients using stateless JWT access tokens (HS256) issued after successful login. Protected routes SHALL require a valid token in `Authorization: Bearer <token>` and SHALL return 401 when the token is missing, invalid, or expired.

## Goal and non-goals

**Goal:** Provide a standard, stateless way to authenticate requests via JWT (HS256, expiration). Clients obtain a token from POST `/auth/login` and send it on protected routes. No server-side session store.

**Non-goals:** OAuth or external identity providers; refresh tokens; multi-tenancy (separate change).

## ADDED Requirements

### Requirement: Login endpoint

The system SHALL provide POST `/auth/login` that accepts credentials and returns a JWT access token on success.

#### Scenario: Login request and response
- **WHEN** a POST request is made to `/auth/login` with a body containing valid credentials (e.g. email and password)
- **THEN** the system SHALL validate the credentials against stored user data (password_hash verified)
- **AND** on success the response SHALL return HTTP 200 with a JSON body containing an access token (e.g. `access_token`, `token_type: "bearer"`)
- **AND** the token SHALL be a JWT signed with HS256 and SHALL include at least claims: sub (subject, e.g. user id), role, exp (expiration)

#### Scenario: Login error – invalid credentials
- **WHEN** a POST request is made to `/auth/login` with invalid or unknown email or wrong password
- **THEN** the system SHALL respond with HTTP 401 Unauthorized
- **AND** SHALL NOT return an access token

#### Scenario: Login error – missing or malformed body
- **WHEN** a POST request is made to `/auth/login` without required fields (e.g. email or password missing) or with malformed payload
- **THEN** the system SHALL respond with HTTP 422 Unprocessable Entity or 400 Bad Request as appropriate
- **AND** SHALL NOT return an access token

### Requirement: JWT format and signing

The system SHALL issue and accept JWTs with a defined format and signing algorithm.

#### Scenario: JWT claims
- **WHEN** the system issues or validates a JWT for authentication
- **THEN** the token SHALL include at least: sub (subject, e.g. user identifier), role (user role for RBAC), exp (expiration time)
- **AND** the signing algorithm SHALL be HS256

#### Scenario: Token expiration
- **WHEN** a protected route receives a JWT with exp in the past or missing
- **THEN** the system SHALL treat the token as invalid and SHALL respond with 401 Unauthorized

### Requirement: Configuration via environment

The system SHALL read JWT configuration from environment variables so that secrets and expiration are not hard-coded.

#### Scenario: JWT secret and expiration
- **WHEN** the application creates or validates JWTs
- **THEN** the signing secret SHALL be read from an environment variable (e.g. JWT_SECRET)
- **AND** the token expiration SHALL be read from an environment variable (e.g. JWT_EXPIRATION_MINUTES or JWT_EXPIRATION_SECONDS)
- **AND** production deployments SHALL require a strong JWT_SECRET (documented); weak or default secrets SHALL be rejected or warned in production

### Requirement: Password storage and verification

The system SHALL store user passwords only as a one-way hash and SHALL verify passwords on login without storing or transmitting plaintext.

#### Scenario: Password stored as hash
- **WHEN** a user password is stored (e.g. on user creation or update)
- **THEN** the system SHALL store only a password hash (password_hash), not plaintext
- **AND** the hashing scheme SHALL be suitable for verification (e.g. bcrypt or equivalent via passlib)

#### Scenario: Password verified on login
- **WHEN** a POST request to `/auth/login` includes email and password
- **THEN** the system SHALL look up the user by email and SHALL verify the provided password against the stored password_hash
- **AND** login SHALL succeed only if the verification succeeds

### Requirement: Protected route behavior (401)

The system SHALL reject requests to protected routes when the request is unauthenticated (missing, invalid, or expired token).

#### Scenario: Missing or invalid Authorization header
- **WHEN** a request to a protected route is made without an Authorization header or with a non-Bearer scheme or malformed token
- **THEN** the system SHALL respond with HTTP 401 Unauthorized
- **AND** SHALL NOT execute the protected handler

#### Scenario: Expired or tampered token
- **WHEN** a request to a protected route includes a JWT that is expired or fails signature verification
- **THEN** the system SHALL respond with HTTP 401 Unauthorized
- **AND** SHALL NOT execute the protected handler

### Requirement: Minimal dev bootstrap (optional)

For development and testing only, the system MAY provide a way to seed one admin user (e.g. via migration or documented script) so that login can be exercised without manual user creation. This requirement is optional and SHALL NOT create or expose default users in production.

#### Scenario: Dev seed optional
- **WHEN** the capability is implemented with a dev bootstrap
- **THEN** seeding SHALL be restricted to development/test environments (e.g. APP_ENV=development) or explicitly run scripts
- **AND** production SHALL NOT rely on seeded default credentials
