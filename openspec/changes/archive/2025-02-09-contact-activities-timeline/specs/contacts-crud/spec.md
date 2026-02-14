## ADDED Requirements

### Requirement: Contact edit page displays activities section

The contact edit page (GET `/contacts/{id}/edit`) SHALL display an Activities section below the Notes section. The Activities section SHALL show the contact's activities (list, add form, per-activity delete) as specified by the contact-activities capability. No separate activities page is required. Existing contact edit routes and behavior SHALL remain unchanged.

#### Scenario: Activities section on edit page
- **WHEN** a GET request is made to `/contacts/{id}/edit` for an existing contact
- **THEN** the page SHALL include an Activities section
- **AND** the Activities section SHALL appear below the Notes section
- **AND** the Activities section SHALL show the list of activities for that contact (ordered by activity_date descending), an inline form to add an activity, and a way to delete each activity (e.g. delete button per row)
