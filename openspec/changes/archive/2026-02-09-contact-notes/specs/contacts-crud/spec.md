## ADDED Requirements

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
