## ADDED Requirements

### Requirement: Note model

The system SHALL persist note records in the database with fields: id, contact_id (FK to Contact), content (required text), created_at, updated_at.

#### Scenario: Note model exists
- **WHEN** examining the data layer
- **THEN** a Note model SHALL exist with the above fields
- **AND** it SHALL be persisted via SQLAlchemy and the existing database session

#### Scenario: Timestamps maintained
- **WHEN** a note is created or updated
- **THEN** created_at SHALL be set on insert
- **AND** updated_at SHALL be set on insert and on every update

### Requirement: Notes list for a contact

The system SHALL list notes for a contact on the contact detail page. Notes SHALL be ordered by created_at descending (newest first).

#### Scenario: Notes list on contact detail page
- **WHEN** a GET request is made to `/contacts/{id}` for an existing contact
- **THEN** the page SHALL display that contact's notes (in a notes section)
- **AND** notes SHALL be rendered with Jinja2 using the existing template infrastructure

#### Scenario: Notes ordered by newest first
- **WHEN** notes are displayed for a contact
- **THEN** the list SHALL be ordered by created_at descending

### Requirement: Create note

The system SHALL provide POST `/contacts/{id}/notes` to create a note for that contact. Create SHALL be usable via HTMX from the contact detail page; on success the response SHALL be a note-row HTML fragment so the list updates without full page reload.

#### Scenario: Create note endpoint
- **WHEN** a POST request is made to `/contacts/{id}/notes` with valid form-encoded content (required)
- **THEN** the system SHALL create the note for that contact
- **AND** the response SHALL be HTTP 200 with an HTML fragment of the new note row (suitable for HTMX append, e.g. element with id="note-{id}")

#### Scenario: Create note – contact not found
- **WHEN** a POST request is made to `/contacts/{id}/notes` and no contact exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: Create note – content required
- **WHEN** a POST request to `/contacts/{id}/notes` omits content or content is empty (after strip)
- **THEN** the system SHALL respond with HTTP 200 and an HTML fragment that replaces the add-note form container (id="add-note-form-container"), including validation errors and the add-note form with pre-filled content
- **AND** the response SHALL indicate that the fragment targets the form container (e.g. HX-Retarget and HX-Reswap response headers) so errors show in place and are not appended to the notes list
- **AND** the note SHALL NOT be created

#### Scenario: HTMX create from contact detail page
- **WHEN** the user submits the add-note form on the contact detail page via HTMX (hx-post to `/contacts/{id}/notes`, hx-target="#contact-notes-list", hx-swap="beforeend")
- **THEN** the request SHALL be sent without full page navigation
- **AND** on success the response fragment (note row) SHALL be appended to the notes list so the new row appears without reload
- **AND** on validation error the response SHALL target the add-note form container (id="add-note-form-container") so the form area is replaced with the form and errors in place

### Requirement: Delete note

The system SHALL provide POST `/notes/{note_id}/delete` to delete a note. Delete from the contact detail page MUST support HTMX: the note row SHALL be removed without full page reload.

#### Scenario: Delete note endpoint
- **WHEN** a POST request is made to `/notes/{note_id}/delete` for an existing note id
- **THEN** the system SHALL delete the note
- **AND** the response SHALL be HTTP 200 with empty body (so the client can swap the row with nothing and remove it)

#### Scenario: Delete note – not found
- **WHEN** a POST request is made to `/notes/{note_id}/delete` and no note exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: HTMX row removal
- **WHEN** the user triggers delete for a note from the contact detail page via HTMX (e.g. button with hx-post to `/notes/{note_id}/delete`, hx-target the note row, hx-swap="outerHTML")
- **THEN** the request SHALL be sent without full page navigation
- **AND** the note row SHALL be removed from the list (e.g. row has stable id such as id="note-{id}" and is replaced by empty response)

### Requirement: Note or contact not found (404)

The system SHALL return 404 Not Found when a contact id or note id is used in a relevant route and the resource does not exist.

#### Scenario: 404 for create note – contact missing
- **WHEN** POST `/contacts/{id}/notes` is requested and the contact does not exist
- **THEN** the response SHALL be 404 Not Found

#### Scenario: 404 for delete note
- **WHEN** POST `/notes/{note_id}/delete` is requested and the note does not exist
- **THEN** the response SHALL be 404 Not Found
