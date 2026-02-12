## ADDED Requirements

### Requirement: Company model

The system SHALL persist company records in the database with fields: id, name (required), created_at, updated_at.

#### Scenario: Company model exists
- **WHEN** examining the data layer
- **THEN** a Company model SHALL exist with the above fields
- **AND** it SHALL be persisted via SQLAlchemy and the existing database session

#### Scenario: Company timestamps maintained
- **WHEN** a company is created or updated
- **THEN** created_at SHALL be set on insert
- **AND** updated_at SHALL be set on insert and on every update

### Requirement: Companies list route

The system SHALL provide a GET route at `/companies` that returns a server-rendered list of companies.

#### Scenario: List route exists
- **WHEN** a GET request is made to `/companies`
- **THEN** the route SHALL return an HTML response
- **AND** the page SHALL display companies in a list or table

#### Scenario: List is server-rendered
- **WHEN** the companies list page is rendered
- **THEN** it SHALL be rendered with Jinja2 using the existing template infrastructure

### Requirement: Create company routes

The system SHALL provide GET `/companies/new` and POST `/companies` for creating a new company.

#### Scenario: New form route
- **WHEN** a GET request is made to `/companies/new`
- **THEN** the route SHALL return an HTML page with a form to create a company
- **AND** the form SHALL include a required `name` field

#### Scenario: Create submit
- **WHEN** a valid POST request is made to `/companies` with a non-empty name
- **THEN** the system SHALL create the company
- **AND** the response SHALL redirect to a company page (for example `/companies`)

#### Scenario: Create validation - name required
- **WHEN** a POST request to `/companies` omits name or provides an empty name
- **THEN** the system SHALL re-render the create form with validation errors (HTTP 200)
- **AND** the company SHALL NOT be created

### Requirement: Edit company routes

The system SHALL provide GET `/companies/{id}/edit` and POST `/companies/{id}` for updating a company.

#### Scenario: Edit form route
- **WHEN** a GET request is made to `/companies/{id}/edit` for an existing company id
- **THEN** the route SHALL return an HTML page with a form pre-filled with that company's data

#### Scenario: Edit form - company not found
- **WHEN** a GET request is made to `/companies/{id}/edit` and no company exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: Update submit
- **WHEN** a valid POST request is made to `/companies/{id}` with a non-empty name
- **THEN** the system SHALL update the company and MAY respond with a redirect (for example `/companies`)
- **AND** updated_at SHALL be set

#### Scenario: Update validation - name required
- **WHEN** a POST request to `/companies/{id}` omits name or provides an empty name
- **THEN** the system SHALL re-render the edit form with validation errors (HTTP 200)
- **AND** the company SHALL NOT be updated

#### Scenario: Update - company not found
- **WHEN** a POST request is made to `/companies/{id}` and no company exists with that id
- **THEN** the system SHALL respond with 404 Not Found

### Requirement: Delete company

The system SHALL provide POST `/companies/{id}/delete` to delete a company.

#### Scenario: Delete endpoint
- **WHEN** a POST request is made to `/companies/{id}/delete` for an existing company id
- **THEN** the system SHALL delete the company
- **AND** the response SHALL be compatible with server-rendered navigation or HTMX-based row removal

#### Scenario: Delete - company not found
- **WHEN** a POST request is made to `/companies/{id}/delete` and no company exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: Delete preserves contacts
- **WHEN** a company is deleted and one or more contacts reference that company via `company_id`
- **THEN** those contacts SHALL NOT be deleted
- **AND** each affected contact's `company_id` SHALL be set to NULL

### Requirement: Contact-company foreign key behavior

The system SHALL enforce an optional foreign key from `contacts.company_id` to `companies.id` with `ON DELETE SET NULL`.

#### Scenario: Foreign key exists
- **WHEN** examining the database schema
- **THEN** `contacts.company_id` SHALL reference `companies.id`
- **AND** the `contacts.company_id` column SHALL be nullable

#### Scenario: Delete behavior uses SET NULL
- **WHEN** a referenced company row is deleted
- **THEN** the database SHALL set referencing `contacts.company_id` values to NULL
- **AND** the delete operation SHALL NOT be rejected because of those references
