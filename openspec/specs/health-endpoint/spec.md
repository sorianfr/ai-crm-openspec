## ADDED Requirements

### Requirement: Health check endpoint

The system SHALL provide a health check API endpoint for monitoring and readiness checks.

#### Scenario: Health endpoint route exists
- **WHEN** examining the project structure
- **THEN** a health endpoint route handler SHALL exist at `app/routes/health.py`
- **AND** it SHALL define a GET endpoint at `/health`

#### Scenario: Health endpoint exists
- **WHEN** a GET request is made to `/health`
- **THEN** the endpoint SHALL return a successful HTTP response (200 status code)

#### Scenario: Health response format
- **WHEN** the health endpoint is called
- **THEN** it SHALL return a JSON response
- **AND** the response SHALL indicate the service status (e.g., `{"status": "ok"}`)

#### Scenario: Health endpoint documentation
- **WHEN** viewing the OpenAPI documentation at `/docs`
- **THEN** the `/health` endpoint SHALL be documented
- **AND** it SHALL show the expected response schema
