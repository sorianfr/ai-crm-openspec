# Contact Activities

Activities (calls, emails, meetings, tasks) attached to contacts on the edit page.

## Requirements

### Requirement: Activity model

The system SHALL persist activity records in the database with fields: id, contact_id (FK to Contact, ON DELETE CASCADE), type (call, email, meeting, task), description (required text), activity_date (date or datetime of the interaction), created_at, updated_at.

#### Scenario: Activity model exists
- **WHEN** examining the data layer
- **THEN** an Activity model SHALL exist with the above fields
- **AND** it SHALL be persisted via SQLAlchemy and the existing database session
- **AND** contact_id SHALL be a foreign key to contacts.id with ON DELETE CASCADE

#### Scenario: Timestamps maintained
- **WHEN** an activity is created or updated
- **THEN** created_at SHALL be set on insert
- **AND** updated_at SHALL be set on insert and on every update

### Requirement: Activities list for a contact

The system SHALL list activities for a contact on the contact edit page. Activities SHALL be ordered by activity_date descending (newest first).

#### Scenario: Activities list on edit page
- **WHEN** a GET request is made to `/contacts/{id}/edit` for an existing contact
- **THEN** the page SHALL display that contact's activities (in an Activities section)
- **AND** activities SHALL be rendered with Jinja2 using the existing template infrastructure

#### Scenario: Activities ordered by activity_date descending
- **WHEN** activities are displayed for a contact
- **THEN** the list SHALL be ordered by activity_date descending

### Requirement: Create activity

The system SHALL provide POST `/contacts/{contact_id}/activities` to create an activity for that contact. Create SHALL be usable via HTMX from the contact edit page; on success the response SHALL be an activity-row HTML fragment so the list updates without full page reload.

#### Scenario: Create activity endpoint
- **WHEN** a POST request is made to `/contacts/{contact_id}/activities` with valid form-encoded type, description (required), and activity_date
- **THEN** the system SHALL create the activity for that contact
- **AND** the response SHALL be HTTP 200 with an HTML fragment of the new activity row (suitable for HTMX append, e.g. element with id="activity-{id}")

#### Scenario: Create activity – contact not found
- **WHEN** a POST request is made to `/contacts/{contact_id}/activities` and no contact exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: Create activity – description required
- **WHEN** a POST request to `/contacts/{contact_id}/activities` omits description or description is empty (after strip)
- **THEN** the system SHALL respond with HTTP 200 and an HTML fragment that replaces the add-activity form container (e.g. id="add-activity-form-container"), including validation errors and the add-activity form with pre-filled values
- **AND** the response SHALL indicate that the fragment targets the form container (e.g. HX-Retarget and HX-Reswap response headers) so errors show in place
- **AND** the activity SHALL NOT be created

#### Scenario: HTMX create from edit page
- **WHEN** the user submits the add-activity form on the contact edit page via HTMX (hx-post to `/contacts/{contact_id}/activities`, hx-target the activities list container, hx-swap="beforeend")
- **THEN** the request SHALL be sent without full page navigation
- **AND** on success the response fragment (activity row) SHALL be appended to the activities list so the new row appears without reload
- **AND** on validation error the response SHALL target the add-activity form container so the form area is replaced with the form and errors in place

### Requirement: Delete activity

The system SHALL provide POST `/activities/{activity_id}/delete` to delete an activity. Delete from the contact edit page MUST support HTMX: the activity row SHALL be removed without full page reload.

#### Scenario: Delete activity endpoint
- **WHEN** a POST request is made to `/activities/{activity_id}/delete` for an existing activity id
- **THEN** the system SHALL delete the activity
- **AND** the response SHALL be HTTP 200 with empty body (so the client can swap the row with nothing and remove it)

#### Scenario: Delete activity – not found
- **WHEN** a POST request is made to `/activities/{activity_id}/delete` and no activity exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: HTMX row removal
- **WHEN** the user triggers delete for an activity from the contact edit page via HTMX (e.g. button with hx-post to `/activities/{activity_id}/delete`, hx-target the activity row, hx-swap="outerHTML")
- **THEN** the request SHALL be sent without full page navigation
- **AND** the activity row SHALL be removed from the list (e.g. row has stable id such as id="activity-{id}" and is replaced by empty response)

### Requirement: Activity or contact not found (404)

The system SHALL return 404 Not Found when a contact id or activity id is used in a relevant route and the resource does not exist.

#### Scenario: 404 for create activity – contact missing
- **WHEN** POST `/contacts/{contact_id}/activities` is requested and the contact does not exist
- **THEN** the response SHALL be 404 Not Found

#### Scenario: 404 for delete activity
- **WHEN** POST `/activities/{activity_id}/delete` is requested and the activity does not exist
- **THEN** the response SHALL be 404 Not Found
