## ADDED Requirements

### Requirement: HTMX library integration

The system SHALL include HTMX library for future dynamic web interactions.

#### Scenario: HTMX library via CDN
- **WHEN** examining the base template
- **THEN** HTMX library SHALL be included via CDN link in a script tag
- **AND** it SHALL be accessible to all templates that extend the base template

#### Scenario: HTMX in base template
- **WHEN** the base template at `app/templates/base.html` is rendered
- **THEN** HTMX library SHALL be included via CDN script tag in the HTML head or body
- **AND** templates extending the base template SHALL be ready to use HTMX attributes for future features

#### Scenario: Static assets directory
- **WHEN** examining the project structure
- **THEN** a `static/` directory SHALL exist at `app/static/` for static assets
- **AND** FastAPI SHALL be configured to serve static files from this directory
