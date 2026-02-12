## ADDED Requirements

### Requirement: Contacts list search and filter query parameters

The system SHALL support search and filter inputs on GET `/contacts` using query parameters: `q` (string), `has_email` (bool), and `has_phone` (bool).

#### Scenario: Query parameters accepted
- **WHEN** a GET request is made to `/contacts` with any combination of `q`, `has_email`, and `has_phone`
- **THEN** the route SHALL parse and apply the provided parameters
- **AND** omitted parameters SHALL use default behavior (no search term; boolean filters false)

#### Scenario: Search query filters contacts
- **WHEN** a GET request is made to `/contacts?q=<text>` with non-empty `q`
- **THEN** the returned list SHALL include only contacts matching the search text
- **AND** matching SHALL be applied to contact full_name, email, or company

#### Scenario: has_email filter
- **WHEN** a GET request is made to `/contacts?has_email=true`
- **THEN** the returned list SHALL include only contacts with a non-empty email value

#### Scenario: has_phone filter
- **WHEN** a GET request is made to `/contacts?has_phone=true`
- **THEN** the returned list SHALL include only contacts with a non-empty phone value

#### Scenario: Combined filters
- **WHEN** a GET request is made to `/contacts` with both `has_email=true` and `has_phone=true`
- **THEN** the returned list SHALL include only contacts that satisfy both filters
- **AND** if `q` is also present, search SHALL be applied together with both filters

### Requirement: Contacts list ordering after filtering

The system SHALL preserve contact ordering by `updated_at` descending after applying search and filters.

#### Scenario: Ordered filtered results
- **WHEN** a GET request is made to `/contacts` with any search/filter parameters
- **THEN** the returned contacts SHALL be ordered by updated_at descending (most recently updated first)

### Requirement: HTMX fragment response for contacts results

GET `/contacts` SHALL return either full-page HTML or an HTMX fragment based on the presence of the `HX-Request` header.

#### Scenario: Non-HTMX request returns full page
- **WHEN** a GET request is made to `/contacts` without `HX-Request`
- **THEN** the response SHALL be the full contacts page HTML
- **AND** it SHALL include a stable results container with id `contacts-results`

#### Scenario: HTMX request returns results fragment
- **WHEN** a GET request is made to `/contacts` with `HX-Request` present
- **THEN** the response SHALL contain only the list/table fragment template (e.g. `contacts/_contacts_table.html`)
- **AND** the fragment SHALL be suitable for swap into `#contacts-results`

### Requirement: Contacts list UI controls for search and filters

The contacts list page SHALL provide a search input and two boolean filter controls that submit via HTMX to GET `/contacts`.

#### Scenario: Search and filter controls present
- **WHEN** the user views the contacts list page
- **THEN** the page SHALL include a `q` search input
- **AND** the page SHALL include `has_email` and `has_phone` boolean controls

#### Scenario: Controls update results in place
- **WHEN** the user submits or changes the search/filter controls via HTMX
- **THEN** the request SHALL target GET `/contacts`
- **AND** the response SHALL update only `#contacts-results` without full page reload
