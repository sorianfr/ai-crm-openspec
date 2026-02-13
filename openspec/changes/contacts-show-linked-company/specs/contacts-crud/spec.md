## MODIFIED Requirements

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

#### Scenario: List company display uses linked name with legacy fallback
- **WHEN** the contacts list page is rendered for a contact
- **THEN** the company value shown in the list SHALL be the linked Company's name when the contact has `company_id` set and the linked Company exists
- **AND** when the contact has no `company_id` or the linked Company does not exist, the company value shown SHALL be the contact's legacy `company` text (or empty if none)
