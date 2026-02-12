## MODIFIED Requirements

### Requirement: Contact model

The system SHALL persist contact records in the database with fields: id, full_name (required), email (optional), phone (optional), company (optional legacy text), company_id (optional foreign key), created_at, updated_at.

#### Scenario: Contact model exists
- **WHEN** examining the data layer
- **THEN** a Contact model SHALL exist with the above fields
- **AND** `company` SHALL remain a persisted optional string field
- **AND** `company_id` SHALL be a nullable foreign key to `companies.id` using ON DELETE SET NULL
- **AND** the model SHALL be persisted via SQLAlchemy and the existing database session

#### Scenario: Timestamps maintained
- **WHEN** a contact is created or updated
- **THEN** created_at SHALL be set on insert
- **AND** updated_at SHALL be set on insert and on every update

### Requirement: Contacts list route

The system SHALL provide a GET route at `/contacts` that returns a server-rendered list of contacts.

#### Scenario: List route exists
- **WHEN** a GET request is made to `/contacts`
- **THEN** the route SHALL return an HTML response
- **AND** the page SHALL display contacts in a list or table

#### Scenario: List is server-rendered
- **WHEN** the list page is rendered
- **THEN** it SHALL be rendered with Jinja2 using the existing template infrastructure
- **AND** each contact row SHALL be suitable for HTMX delete (e.g. identifiable container for row removal)

#### Scenario: List ordered by most recently updated first
- **WHEN** a GET request is made to `/contacts`
- **THEN** the contacts SHALL be ordered by updated_at descending (most recently updated first)

#### Scenario: List company display remains legacy text
- **WHEN** the contacts list page is rendered for a contact that has both `company` text and `company_id`
- **THEN** the company value shown in the list SHALL come from the contact's `company` text field
- **AND** this change SHALL NOT require list display to switch to company name from `company_id`

### Requirement: Create contact routes

The system SHALL provide GET `/contacts/new` and POST `/contacts` for creating a new contact. Create MAY use standard POST with redirect (no HTMX partials required).

#### Scenario: New form route
- **WHEN** a GET request is made to `/contacts/new`
- **THEN** the route SHALL return an HTML page with a form to create a contact
- **AND** the form SHALL include fields for full_name (required), email, phone, company
- **AND** the form SHALL include an optional company selector bound to `company_id`

#### Scenario: Create submit
- **WHEN** a valid POST request is made to `/contacts` with full_name and optional email, phone, company, company_id
- **THEN** the system SHALL create the contact and MAY respond with a redirect (e.g. to `/contacts` or the new contact)
- **AND** the new contact SHALL be persisted with created_at and updated_at set
- **AND** the existing `company` text field SHALL be persisted independently from `company_id`

#### Scenario: Create with no company_id
- **WHEN** a valid POST request to `/contacts` omits `company_id` or submits it as blank
- **THEN** the system SHALL create the contact with `company_id` set to NULL
- **AND** the request SHALL still succeed

#### Scenario: Create validation - full_name required
- **WHEN** a POST request to `/contacts` (form-encoded) omits full_name or full_name is empty
- **THEN** the system SHALL re-render the create form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be created

#### Scenario: Create validation - email format
- **WHEN** a POST request to `/contacts` (form-encoded) provides an email that is not valid
- **THEN** the system SHALL re-render the create form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be created

#### Scenario: Create validation - company_id must exist
- **WHEN** a POST request to `/contacts` provides a non-empty `company_id` that does not match an existing company
- **THEN** the system SHALL re-render the create form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be created

### Requirement: Edit contact routes

The system SHALL provide GET `/contacts/{id}/edit` and POST `/contacts/{id}` for updating a contact. Edit MAY use standard POST with redirect (no HTMX partials required).

#### Scenario: Edit form route
- **WHEN** a GET request is made to `/contacts/{id}/edit` for an existing contact id
- **THEN** the route SHALL return an HTML page with a form pre-filled with that contact's data
- **AND** the form SHALL allow editing full_name (required), email, phone, company
- **AND** the form SHALL include an optional company selector bound to `company_id`

#### Scenario: Edit form - contact not found
- **WHEN** a GET request is made to `/contacts/{id}/edit` and no contact exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: Update submit
- **WHEN** a valid POST request is made to `/contacts/{id}` with full_name and optional email, phone, company, company_id
- **THEN** the system SHALL update the contact and MAY respond with a redirect (e.g. to `/contacts` or the contact)
- **AND** updated_at SHALL be set
- **AND** the existing `company` text field SHALL remain editable and persisted independently from `company_id`

#### Scenario: Update - contact not found
- **WHEN** a POST request is made to `/contacts/{id}` and no contact exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: Update validation - full_name required and email valid
- **WHEN** a POST request to `/contacts/{id}` (form-encoded) omits full_name or provides invalid email
- **THEN** the system SHALL re-render the edit form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be updated

#### Scenario: Update validation - company_id must exist
- **WHEN** a POST request to `/contacts/{id}` provides a non-empty `company_id` that does not match an existing company
- **THEN** the system SHALL re-render the edit form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be updated
