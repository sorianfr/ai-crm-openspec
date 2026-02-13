## ADDED Requirements

### Requirement: Smart company assignment on contact forms

The company text field is the primary source of truth. When company text is non-empty, the server SHALL ignore the dropdown and SHALL resolve by company name (case-insensitive) or create a new Company and link the contact. When company text is empty, the dropdown selection SHALL be used for `company_id`. The UI SHALL disable the company dropdown when the company text field has content.

#### Scenario: Company text non-empty – resolve by name and link
- **WHEN** a valid POST to create or update a contact includes non-empty company text (after trim)
- **THEN** the server SHALL ignore the `company_id` form value
- **AND** the system SHALL find an existing Company by name (case-insensitive match)
- **AND** if a company exists, the contact SHALL be linked to it (`company_id` set, `company` text set to that name)
- **AND** the contact SHALL be created or updated successfully

#### Scenario: Company text non-empty – create company and link
- **WHEN** a valid POST to create or update a contact includes non-empty company text (after trim) and no existing Company matches that name (case-insensitive)
- **THEN** the system SHALL create a new Company with that name
- **AND** the contact SHALL be linked to the new company (`company_id` set, `company` text set to that name)
- **AND** the contact SHALL be created or updated successfully

#### Scenario: Company text empty – use dropdown
- **WHEN** a valid POST to create or update a contact has empty company text (or only whitespace)
- **THEN** the system SHALL use the `company_id` form value as the link to a company (if provided)
- **AND** if `company_id` is provided and valid, the contact SHALL be linked to that company and `company` text MAY be set from the selected company's name
- **AND** if `company_id` is omitted or blank, the contact SHALL have `company_id` set to NULL

#### Scenario: Company dropdown disabled when text has content
- **WHEN** the contact create or edit form is displayed and the company text field has content
- **THEN** the "Existing company" (company_id) dropdown SHALL be disabled in the UI
- **AND** when the company text field is empty, the dropdown SHALL be enabled so the user MAY select an existing company

## MODIFIED Requirements

### Requirement: Create contact routes

The system SHALL provide GET `/contacts/new` and POST `/contacts` for creating a new contact. Create MAY use standard POST with redirect (no HTMX partials required). Company assignment SHALL follow the Smart company assignment requirement (company text is primary; when non-empty resolve or create and link; when empty use dropdown).

#### Scenario: New form route
- **WHEN** a GET request is made to `/contacts/new`
- **THEN** the route SHALL return an HTML page with a form to create a contact
- **AND** the form SHALL include fields for full_name (required), email, phone, company
- **AND** the form SHALL include an optional company selector bound to `company_id`

#### Scenario: Create submit
- **WHEN** a valid POST request is made to `/contacts` with full_name and optional email, phone, company, company_id
- **THEN** the system SHALL create the contact and MAY respond with a redirect (e.g. to `/contacts` or the new contact)
- **AND** the new contact SHALL be persisted with created_at and updated_at set
- **AND** company and company_id SHALL be set according to the Smart company assignment requirement (company text non-empty: resolve by name or create Company and link; company text empty: use company_id from dropdown or NULL)

#### Scenario: Create with no company_id when company text empty
- **WHEN** a valid POST request to `/contacts` has empty company text and omits `company_id` or submits it as blank
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

#### Scenario: Create validation – company_id must exist when company text empty
- **WHEN** a POST request to `/contacts` has empty company text and provides a non-empty `company_id` that does not match an existing company
- **THEN** the system SHALL re-render the create form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be created

### Requirement: Edit contact routes

The system SHALL provide GET `/contacts/{id}/edit` and POST `/contacts/{id}` for updating a contact. Edit MAY use standard POST with redirect (no HTMX partials required). Company assignment SHALL follow the Smart company assignment requirement (company text is primary; when non-empty resolve or create and link; when empty use dropdown).

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
- **AND** company and company_id SHALL be set according to the Smart company assignment requirement (company text non-empty: resolve by name or create Company and link; company text empty: use company_id from dropdown or NULL)

#### Scenario: Update – contact not found
- **WHEN** a POST request is made to `/contacts/{id}` and no contact exists with that id
- **THEN** the system SHALL respond with 404 Not Found

#### Scenario: Update validation – full_name required and email valid
- **WHEN** a POST request to `/contacts/{id}` (form-encoded) omits full_name or provides invalid email
- **THEN** the system SHALL re-render the edit form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be updated

#### Scenario: Update validation – company_id must exist when company text empty
- **WHEN** a POST request to `/contacts/{id}` has empty company text and provides a non-empty `company_id` that does not match an existing company
- **THEN** the system SHALL re-render the edit form with validation errors (HTTP 200)
- **AND** the contact SHALL NOT be updated
