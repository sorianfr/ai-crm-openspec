# Web session authentication

The system SHALL provide cookie-based authentication for the web UI so users can log in via a form and browse protected HTML routes without Bearer tokens. Session stores only user_id; user (including tenant_id, role) is always resolved from the DB.

## Goal and non-goals

**Goal:** First-class web login/logout; session-based current_user resolution; redirect unauthenticated users to /login; preserve multi-tenant and RBAC.

**Non-goals:** Replacing JWT for API; OAuth/OIDC; user admin UI.

## Requirements

### Requirement: Login routes

The system SHALL provide web login routes at GET /login and POST /login.

#### Scenario: GET /login returns HTML form
- **WHEN** a GET request is made to /login
- **THEN** the system SHALL return an HTML login page with a form for email and password
- **AND** the form SHALL POST to /login

#### Scenario: POST /login success
- **WHEN** a POST request is made to /login with valid email and password
- **THEN** the system SHALL validate credentials using existing password hashing
- **AND** SHALL set a session cookie storing only user_id
- **AND** SHALL rotate the CSRF token in session
- **AND** SHALL redirect to /

#### Scenario: POST /login failure
- **WHEN** a POST request is made to /login with invalid credentials
- **THEN** the system SHALL re-render the login page with a generic error message
- **AND** SHALL NOT indicate whether the email or password was wrong (no user enumeration)

### Requirement: Logout route

The system SHALL provide POST /logout to clear the session and redirect to login.

#### Scenario: POST /logout
- **WHEN** a POST request is made to /logout
- **THEN** the system SHALL clear the session
- **AND** SHALL redirect to /login

### Requirement: Session middleware and cookie settings

The system SHALL use Starlette SessionMiddleware with configuration from environment.

#### Scenario: Session secret from environment
- **WHEN** the application starts
- **THEN** the session secret SHALL be loaded from environment (e.g. SESSION_SECRET)
- **AND** SHALL be required for production

#### Scenario: Cookie flags
- **WHEN** a session cookie is set
- **THEN** HttpOnly SHALL be True
- **AND** SameSite SHALL be lax
- **AND** Secure SHALL be True in production and False in development (APP_ENV-based)
- **AND** max_age SHALL be a reasonable value (e.g. 8-12 hours)

#### Scenario: Session stores only user_id
- **WHEN** a user logs in successfully
- **THEN** the session SHALL store only user_id
- **AND** SHALL NOT store role or tenant_id (these are resolved from DB)

### Requirement: get_current_web_user

The system SHALL provide get_current_web_user that resolves the authenticated user for web routes.

#### Scenario: Session has user_id and user exists
- **WHEN** get_current_web_user is invoked and the session contains a valid user_id and the user exists in the DB
- **THEN** it SHALL return the User object with tenant_id and role from the DB
- **AND** SHALL NOT use session-stored role or tenant_id

#### Scenario: Session missing or invalid user
- **WHEN** get_current_web_user is invoked and the session has no user_id or the user is not found in the DB
- **THEN** the system SHALL clear the session if present
- **AND** SHALL redirect to /login
- **AND** SHALL NOT proceed with the protected route

### Requirement: require_web_roles

The system SHALL provide require_web_roles(allowed_roles) to enforce RBAC on web routes.

#### Scenario: Role allowed
- **WHEN** require_web_roles is invoked and the current user role is in the allowed list
- **THEN** the request SHALL proceed

#### Scenario: Role not allowed – normal request
- **WHEN** require_web_roles is invoked and the current user role is not allowed and the request is not an HTMX request
- **THEN** the system SHALL return 403 Forbidden
- **AND** MAY return an HTML error page

#### Scenario: Role not allowed – HTMX request
- **WHEN** require_web_roles is invoked and the current user role is not allowed and the request has HX-Request header
- **THEN** the system SHALL return HTTP 403 status
- **AND** SHALL NOT redirect (to avoid redirect loops with HTMX)
