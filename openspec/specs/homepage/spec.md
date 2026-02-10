## ADDED Requirements

### Requirement: Homepage route

The system SHALL provide a homepage route that serves a basic HTML template.

#### Scenario: Homepage route handler exists
- **WHEN** examining the project structure
- **THEN** a homepage route handler SHALL exist at `app/routes/home.py` (or similar)
- **AND** it SHALL define a GET endpoint at `/` (root path)

#### Scenario: Homepage route exists
- **WHEN** a GET request is made to `/` (root path)
- **THEN** the homepage route SHALL handle the request
- **AND** it SHALL return an HTML response

#### Scenario: Homepage template rendering
- **WHEN** the homepage route is accessed
- **THEN** it SHALL render a Jinja2 template
- **AND** the rendered HTML SHALL be returned as the response

#### Scenario: Homepage template exists
- **WHEN** examining templates
- **THEN** a homepage template SHALL exist at `app/templates/index.html`
- **AND** it SHALL extend the base template at `app/templates/base.html`

#### Scenario: Homepage content
- **WHEN** viewing the homepage
- **THEN** it SHALL display basic content indicating the application is running
- **AND** it SHALL include HTMX library for future interactive features

### Requirement: Homepage links to Contacts

The homepage SHALL provide a way for users to discover and navigate to the Contacts feature.

#### Scenario: Link to contacts from homepage
- **WHEN** the user views the homepage
- **THEN** the page SHALL include a link or call-to-action to the Contacts feature
- **AND** the link SHALL target `/contacts` (or the canonical contacts list URL)

#### Scenario: Link in navigation or content
- **WHEN** examining the homepage template or base layout
- **THEN** the Contacts link MAY appear in a navigation area or in the main content (e.g. "View contacts")
- **AND** the link SHALL be visible when the homepage is rendered
