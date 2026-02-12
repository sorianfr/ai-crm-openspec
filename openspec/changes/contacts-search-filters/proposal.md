## Why

Users need to find contacts quickly by name, email, or company and to narrow the list (e.g. only contacts with email or phone). Adding search and filters to the contacts list with HTMX keeps the interaction on the same page (no full reload) and stays consistent with the existing server-rendered, HTMX-based UI.

## What Changes

- **Query parameters** for GET `/contacts`: `q` (string, optional search text), `has_email` (bool), `has_phone` (bool). Filters in this change are ONLY these two boolean toggles (no company dropdowns or other filters yet).
- **Search:** Apply `q` to filter contacts (e.g. by full_name, email, company); exact matching rules in specs/design.
- **Filters:** When `has_email` is true, only contacts with a non-empty email; when `has_phone` is true, only contacts with a non-empty phone. Both optional.
- **HTMX pattern:** Single GET `/contacts` endpoint. If the request includes the `HX-Request` header, return only a list/table fragment (e.g. from `app/templates/contacts/_contacts_table.html`) to be swapped into a stable container with `id="contacts-results"`. When `HX-Request` is not present, return the full page as today (list inside the same container).
- **Ordering:** Preserve ordering by `updated_at` descending after applying search and filters.
- Preserve existing behavior when no query params are applied (no breaking changes to links or bookmarking).

## Capabilities

### New Capabilities

- `contacts-search-filters`: Search and filter on the contacts list. Query params: `q` (string), `has_email` (bool), `has_phone` (bool). GET `/contacts` returns full page or, when `HX-Request` is present, only the fragment from `_contacts_table.html` for swap into `#contacts-results`. Search box and two boolean toggles (has_email, has_phone) on the list page trigger HTMX GET with params and target `#contacts-results`. Results ordered by updated_at desc.

### Modified Capabilities

- `contacts-crud`: GET `/contacts` SHALL accept optional query parameters `q`, `has_email`, `has_phone` and SHALL return filtered results ordered by updated_at desc; when `HX-Request` is present, the response SHALL be the list/table fragment only (for swap into `#contacts-results`).

## Impact

- **Routes:** GET `/contacts` extended with optional query params `q`, `has_email`, `has_phone`; single endpoint, response varies by `HX-Request`.
- **Templates:** Contacts list page gains search form and two filter toggles; list content inside a container `id="contacts-results"`; new partial `app/templates/contacts/_contacts_table.html` used for both full page and HTMX fragment.
- **Data:** No schema changes; filter/search in the existing Contact query (e.g. ilike for q, IS NOT NULL and != '' for has_email/has_phone).
- **Dependencies:** None new.
