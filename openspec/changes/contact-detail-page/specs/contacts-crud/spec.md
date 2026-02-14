## ADDED Requirements

### Requirement: Contact detail page

The system SHALL provide GET `/contacts/{id}` that returns a server-rendered contact detail page for viewing a contact and its notes and activities.

#### Scenario: Detail page route exists
- **WHEN** a GET request is made to `/contacts/{id}` for an existing contact id
- **THEN** the route SHALL return an HTML response for the contact detail page
- **AND** the page SHALL display the contact summary (full name, email, phone, company display)
- **AND** the page SHALL display a Notes section as specified by the contact-notes capability
- **AND** the page SHALL display an Activities section as specified by the contact-activities capability
- **AND** the page SHALL include a visible "Edit contact" button or link to `/contacts/{id}/edit`

#### Scenario: Detail page contact not found
- **WHEN** a GET request is made to `/contacts/{id}` and no contact exists with that id
- **THEN** the system SHALL respond with 404 Not Found

## MODIFIED Requirements

### Requirement: Edit contact routes

The system SHALL provide GET `/contacts/{id}/edit` and POST `/contacts/{id}` for updating a contact. The edit page SHALL display only the contact form and SHALL NOT display the notes or activities sections. The edit page SHALL include a "Back to contact" link to `/contacts/{id}`.

#### Scenario: Edit form route
- **WHEN** a GET request is made to `/contacts/{id}/edit` for an existing contact id
- **THEN** the route SHALL return an HTML page with a form pre-filled with that contact's data
- **AND** the form SHALL allow editing full_name (required), email, phone, company
- **AND** the form SHALL include an optional company selector bound to company_id
- **AND** the page SHALL NOT display the notes section or the activities section
- **AND** the page SHALL include a "Back to contact" link to `/contacts/{id}`

#### Scenario: Edit form contact not found
- **WHEN** a GET request is made to `/contacts/{id}/edit` and no contact exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: Update submit
- **WHEN** a valid POST request is made to `/contacts/{id}` with full_name and optional email, phone, company, company_id
- **THEN** the system SHALL update the contact and MAY respond with a redirect
- **AND** updated_at SHALL be set

#### Scenario: Update contact not found
- **WHEN** a POST request is made to `/contacts/{id}` and no contact exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: Update validation full_name required and email valid
- **WHEN** a POST request to `/contacts/{id}` omits full_name or provides invalid email
- **THEN** the system SHALL re-render the edit form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be updated

#### Scenario: Update validation company_id must exist when company text empty
- **WHEN** a POST request to `/contacts/{id}` has empty company text and provides a non-empty company_id that does not match an existing company
- **THEN** the system SHALL re-render the edit form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be updated

### Requirement: Contact not found (404)

The system SHALL return 404 Not Found when a contact id is used in a relevant route and no contact exists with that id.

#### Scenario: 404 for get detail
- **WHEN** GET `/contacts/{id}` is requested and the contact does not exist
- **THEN** the response SHALL be 404 Not Found

#### Scenario: 404 for get edit
- **WHEN** GET `/contacts/{id}/edit` is requested and the contact does not exist
- **THEN** the response SHALL be 404 Not Found

#### Scenario: 404 for update
- **WHEN** POST `/contacts/{id}` is requested and the contact does not exist
- **THEN** the response SHALL be 404 Not Found

#### Scenario: 404 for delete
- **WHEN** POST `/contacts/{id}/delete` is requested and the contact does not exist
- **THEN** the response SHALL be 404 Not Found

## REMOVED Requirements

### Requirement: Contact edit page displays notes section

**Reason:** Notes are displayed and managed on the contact detail page (GET `/contacts/{id}`), not on the edit page.

**Migration:** View and manage notes on the contact detail page at `/contacts/{id}`.

### Requirement: Contact edit page displays activities section

**Reason:** Activities are displayed and managed on the contact detail page (GET `/contacts/{id}`), not on the edit page.

**Migration:** View and manage activities on the contact detail page at `/contacts/{id}`.
