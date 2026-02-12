## ADDED Requirements

### Requirement: Contact model

The system SHALL persist contact records in the database with fields: id, full_name (required), email (optional), phone (optional), company (optional legacy text), company_id (optional foreign key), created_at, updated_at.

#### Scenario: Contact model exists
- **WHEN** examining the data layer
- **THEN** a Contact model SHALL exist with the above fields
- **AND** `company` SHALL remain a persisted optional string field
- **AND** `company_id` SHALL be a nullable foreign key to `companies.id` using ON DELETE SET NULL
- **AND** it SHALL be persisted via SQLAlchemy and the existing database session

#### Scenario: Timestamps maintained
- **WHEN** a contact is created or updated
- **THEN** created_at SHALL be set on insert
- **AND** updated_at SHALL be set on insert and on every update

### Requirement: Contacts list route

The system SHALL provide a GET route at `/contacts` that returns a server-rendered list of contacts and supports optional query parameters `q` (string), `has_email` (bool), and `has_phone` (bool).

#### Scenario: List route exists
- **WHEN** a GET request is made to `/contacts` without `HX-Request`
- **THEN** the route SHALL return an HTML response for the full contacts page
- **AND** the page SHALL display contacts in a list or table

#### Scenario: List is server-rendered
- **WHEN** the list page is rendered
- **THEN** it SHALL be rendered with Jinja2 using the existing template infrastructure
- **AND** each contact row SHALL be suitable for HTMX delete (e.g. identifiable container for row removal)

#### Scenario: Query parameters filter results
- **WHEN** a GET request is made to `/contacts` with any of `q`, `has_email`, or `has_phone`
- **THEN** the route SHALL apply the provided search/filter parameters to the contacts query
- **AND** omitted parameters SHALL not constrain results

#### Scenario: Search query behavior
- **WHEN** a GET request is made to `/contacts?q=<text>` with non-empty search text
- **THEN** the route SHALL filter contacts by matching the text against full_name, email, or company

#### Scenario: has_email and has_phone behavior
- **WHEN** a GET request is made to `/contacts?has_email=true` and/or `/contacts?has_phone=true`
- **THEN** `has_email=true` SHALL include only contacts with non-empty email
- **AND** `has_phone=true` SHALL include only contacts with non-empty phone

#### Scenario: List ordered by most recently updated first after filtering
- **WHEN** a GET request is made to `/contacts` with or without search/filter parameters
- **THEN** the contacts SHALL be ordered by updated_at descending (most recently updated first)

#### Scenario: HTMX list fragment response
- **WHEN** a GET request is made to `/contacts` with `HX-Request` present
- **THEN** the route SHALL return only the contacts list/table fragment
- **AND** the fragment SHALL be suitable for swap into a stable container (e.g. `#contacts-results`)

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

#### Scenario: Create validation – full_name required
- **WHEN** a POST request to `/contacts` (form-encoded) omits full_name or full_name is empty
- **THEN** the system SHALL re-render the create form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be created

#### Scenario: Create validation – email format
- **WHEN** a POST request to `/contacts` (form-encoded) provides an email that is not valid
- **THEN** the system SHALL re-render the create form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be created

#### Scenario: Create validation – company_id must exist
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

#### Scenario: Edit form – contact not found
- **WHEN** a GET request is made to `/contacts/{id}/edit` and no contact exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: Update submit
- **WHEN** a valid POST request is made to `/contacts/{id}` with full_name and optional email, phone, company, company_id
- **THEN** the system SHALL update the contact and MAY respond with a redirect (e.g. to `/contacts` or the contact)
- **AND** updated_at SHALL be set
- **AND** the existing `company` text field SHALL remain editable and persisted independently from `company_id`

#### Scenario: Update – contact not found
- **WHEN** a POST request is made to `/contacts/{id}` and no contact exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: Update validation – full_name required and email valid
- **WHEN** a POST request to `/contacts/{id}` (form-encoded) omits full_name or provides invalid email
- **THEN** the system SHALL re-render the edit form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be updated

#### Scenario: Update validation – company_id must exist
- **WHEN** a POST request to `/contacts/{id}` provides a non-empty `company_id` that does not match an existing company
- **THEN** the system SHALL re-render the edit form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be updated

### Requirement: Delete contact

The system SHALL provide POST `/contacts/{id}/delete` to delete a contact. Delete from the list MUST support HTMX: the row SHALL be removed from the list without a full page reload.

#### Scenario: Delete endpoint
- **WHEN** a POST request is made to `/contacts/{id}/delete` for an existing contact id
- **THEN** the system SHALL delete the contact
- **AND** the response SHALL support HTMX (e.g. 204 No Content or a fragment that removes the row)

#### Scenario: Delete – contact not found
- **WHEN** a POST request is made to `/contacts/{id}/delete` and no contact exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: HTMX row removal
- **WHEN** the user triggers delete from the contacts list page via HTMX (e.g. button with hx-post to `/contacts/{id}/delete`)
- **THEN** the request SHALL be sent without full page navigation
- **AND** the list SHALL update so that the deleted contact's row is removed (e.g. via hx-swap or 204 and out-of-band swap)

### Requirement: Contact not found (404)

The system SHALL return 404 Not Found when a contact id is used in a relevant route and no contact exists with that id.

#### Scenario: 404 for get edit
- **WHEN** GET `/contacts/{id}/edit` is requested and the contact does not exist
- **THEN** the response SHALL be 404 Not Found

#### Scenario: 404 for update
- **WHEN** POST `/contacts/{id}` is requested and the contact does not exist
- **THEN** the response SHALL be 404 Not Found

#### Scenario: 404 for delete
- **WHEN** POST `/contacts/{id}/delete` is requested and the contact does not exist
- **THEN** the response SHALL be 404 Not Found

### Requirement: Contact edit page displays notes section

The contact edit page (GET `/contacts/{id}/edit`) SHALL display the contact's notes section: a list of notes, an inline add-note form, and per-note delete via HTMX. No separate notes page and no link from the contacts list are required.

#### Scenario: Notes section on edit page
- **WHEN** a GET request is made to `/contacts/{id}/edit` for an existing contact
- **THEN** the page SHALL include a notes section
- **AND** the notes section SHALL show the list of notes for that contact (ordered by created_at descending)

#### Scenario: Add note form on edit page
- **WHEN** the user views the contact edit page
- **THEN** the notes section SHALL include an inline form to add a note (content field), wrapped in a container (e.g. id="add-note-form-container") so validation errors can replace the form area in place
- **AND** the form SHALL submit via HTMX to POST `/contacts/{id}/notes` (success appends note row to list; error replaces form container with form and errors)

#### Scenario: Delete note from edit page
- **WHEN** the user views the contact edit page
- **THEN** each note row SHALL include a way to delete that note (e.g. delete button)
- **AND** the delete action SHALL use HTMX (e.g. hx-post to `/notes/{note_id}/delete`) so the row is removed without full page reload
