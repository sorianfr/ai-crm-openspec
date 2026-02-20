# CSRF protection

The system SHALL protect cookie-authenticated state-changing requests from Cross-Site Request Forgery by validating a CSRF token on POST/PUT/PATCH/DELETE web routes.

## ADDED Requirements

### Requirement: CSRF token in session

The system SHALL store a CSRF token in the session.

#### Scenario: CSRF token per session
- **WHEN** a session is established (e.g. on login)
- **THEN** the system SHALL generate a random CSRF token
- **AND** SHALL store it in `session["csrf_token"]`
- **AND** SHALL rotate the token on login

### Requirement: CSRF token in forms

The system SHALL embed the CSRF token in all HTML forms that perform state-changing actions.

#### Scenario: Hidden input in forms
- **WHEN** an HTML form is rendered for a POST/PUT/PATCH/DELETE action
- **THEN** the form SHALL include a hidden input with the CSRF token
- **AND** the token SHALL be submitted with the form payload
- **AND** HTMX requests SHALL include the token via the form payload (hidden input submission)

#### Scenario: Optional X-CSRF-Token header
- **WHEN** the system validates CSRF
- **THEN** it MAY accept the token from an `X-CSRF-Token` request header
- **AND** MUST accept the token from the form body (hidden input)

### Requirement: CSRF validation on mutations

The system SHALL validate the CSRF token on all cookie-authenticated state-changing web routes.

#### Scenario: Valid CSRF token
- **WHEN** a POST, PUT, PATCH, or DELETE request is made to a cookie-authenticated web route with a valid CSRF token
- **THEN** the request SHALL proceed

#### Scenario: Invalid or missing CSRF token
- **WHEN** a POST, PUT, PATCH, or DELETE request is made to a cookie-authenticated web route without a valid CSRF token
- **THEN** the system SHALL respond with 403 Forbidden
- **AND** SHALL NOT perform the requested mutation
