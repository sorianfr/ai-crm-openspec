## MODIFIED Requirements

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

The system SHALL provide POST `/contacts/{id}/notes` to create a note. Create SHALL be usable via HTMX from the contact detail page.

#### Scenario: Create note endpoint
- **WHEN** a POST request is made to `/contacts/{id}/notes` with valid form-encoded content (required)
- **THEN** the system SHALL create the note for that contact
- **AND** the response SHALL be HTTP 200 with an HTML fragment of the new note row (e.g. id="note-{id}")

#### Scenario: Create note – contact not found
- **WHEN** a POST request is made to `/contacts/{id}/notes` and no contact exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: Create note – content required
- **WHEN** a POST request to `/contacts/{id}/notes` omits content or content is empty (after strip)
- **THEN** the system SHALL respond with HTTP 200 and an HTML fragment that replaces the add-note form container (id="add-note-form-container"), including validation errors
- **AND** the note SHALL NOT be created

#### Scenario: HTMX create from contact detail page
- **WHEN** the user submits the add-note form on the contact detail page via HTMX (hx-post to `/contacts/{id}/notes`, hx-target="#contact-notes-list", hx-swap="beforeend")
- **THEN** the request SHALL be sent without full page navigation
- **AND** on success the response fragment SHALL be appended to the notes list
- **AND** on validation error the response SHALL target the add-note form container

### Requirement: Delete note

The system SHALL provide POST `/notes/{note_id}/delete` to delete a note. Delete from the contact detail page MUST support HTMX.

#### Scenario: Delete note endpoint
- **WHEN** a POST request is made to `/notes/{note_id}/delete` for an existing note id
- **THEN** the system SHALL delete the note
- **AND** the response SHALL be HTTP 200 with empty body

#### Scenario: Delete note – not found
- **WHEN** a POST request is made to `/notes/{note_id}/delete` and no note exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: HTMX row removal
- **WHEN** the user triggers delete for a note from the contact detail page via HTMX (hx-post to `/notes/{note_id}/delete`, hx-target the note row, hx-swap="outerHTML")
- **THEN** the request SHALL be sent without full page navigation
- **AND** the note row SHALL be removed from the list
