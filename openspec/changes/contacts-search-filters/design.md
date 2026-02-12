## Context

The contacts list is served by GET `/contacts`, which renders `contacts/list.html` with a table of contacts ordered by `updated_at` desc. There is no search or filter today. The list uses HTMX only for delete (row removal). This change adds optional query parameters and uses the `HX-Request` header to return either the full page or a table fragment so the list can update in place when the user changes search or filters.

## Goals / Non-Goals

**Goals:**

- Extend GET `/contacts` with optional query params: `q` (search string), `has_email` (bool), `has_phone` (bool).
- Apply search (e.g. `q` matches full_name, email, or company) and filters (has_email → non-empty email, has_phone → non-empty phone); preserve ordering by `updated_at` desc.
- When the request includes the `HX-Request` header, return only the list/table fragment (from a partial template) for swap into `#contacts-results`; otherwise return the full list page.
- Add search box and two boolean toggles (has_email, has_phone) on the list page that trigger HTMX GET with the current params and target `#contacts-results`.

**Non-Goals:**

- Company dropdown or any filter other than has_email and has_phone.
- New routes; pagination; sorting by other columns.
- Changing the contact model or database schema.

## Decisions

**1. Query parameter types and parsing**

- `q`: Optional string (default empty). Empty or omitted means no search filter.
- `has_email`, `has_phone`: Boolean. FastAPI does not natively treat query params as booleans; use `Query(False)` and accept `"true"`, `"1"`, `"on"` (case-insensitive) as true, anything else or omitted as false. Alternatively use a single string param and parse (e.g. `Optional[str] = None` then `param in ("true", "1", "on")`). Recommendation: use `Query(False)` with a small helper or dependency that normalizes common string values to bool so the handler receives clean booleans.
- **Rationale:** Keeps handler logic simple; avoids ambiguity (e.g. "false" vs missing).

**2. Search semantics**

- Apply `q` only when non-empty (after strip). Match contacts where **any** of full_name, email, or company contains the search string (case-insensitive). Use SQLAlchemy `or_` of `ilike` (or `contains`) on the three columns; SQLite supports `ilike` for case-insensitive match.
- **Rationale:** Single search box across the main text fields; no separate “search in” selector in this change.

**3. Filter semantics**

- `has_email` true: restrict to contacts where email IS NOT NULL and trimmed length > 0 (or `Contact.email != ""` and `Contact.email.isnot(None)`).
- `has_phone` true: restrict to contacts where phone IS NOT NULL and trimmed length > 0. Apply both filters when both are true (AND).
- **Rationale:** Simple “has value” filters; no empty-string vs NULL ambiguity in the spec if we treat both as “no value”.

**4. HX-Request and response shape**

- Check the `HX-Request` request header (HTMX sets it to `"true"`). If present, render only the fragment (the table or the wrapper that goes inside `#contacts-results`) and return it; status 200. If not present, render the full `contacts/list.html` as today (which will include the same fragment inside `#contacts-results`).
- **Rationale:** One endpoint, one set of query logic; response varies by client (browser vs HTMX). No duplicate filtering logic.

**5. Template structure**

- Introduce a partial, e.g. `app/templates/contacts/_contacts_table.html`, that contains the table (or the contents of the `#contacts-results` container). The partial receives `contacts` (and optionally `q`, `has_email`, `has_phone` for preserving form state).
- The full list page `contacts/list.html` includes: (1) page title and “New contact” link, (2) search form (input `q`, two checkboxes has_email/has_phone, submit or HTMX-triggered GET), (3) a wrapper `<div id="contacts-results">` that contains the partial (so full-page load and HTMX swap both render the same markup).
- Search/filter form: use GET and `hx-get="/contacts"`, `hx-target="#contacts-results"`, `hx-swap="innerHTML"` (or `outerHTML` if the partial includes the wrapper). Include current `q`, `has_email`, `has_phone` in the request (e.g. form fields or `hx-vals`). Trigger on submit and optionally on change (e.g. `hx-trigger="change"` for checkboxes, debounced for search) so the list updates without full page reload.
- **Rationale:** Single source of truth for the table; full page and fragment stay in sync.

**6. Ordering**

- Apply `order_by(Contact.updated_at.desc())` after all filters (search + has_email + has_phone). No other sort options in this change.
- **Rationale:** Matches existing behavior and proposal.

## Risks / Trade-offs

- **Empty search:** Empty `q` is treated as “no search” (show all that pass filters). No “search for empty” case. Mitigation: Document; no change needed for MVP.
- **Boolean query parsing:** Different clients might send different strings. Mitigation: Normalize in one place (dependency or helper) and document accepted values (true/1/on).
- **Large result sets:** No pagination; a very large filtered list could be slow. Mitigation: Out of scope for this change; add pagination later if needed.

## Migration Plan

- No database or config migration. Deploy updated route and templates; ensure HTMX is loaded on the list page (already is via base). Rollback: revert route and templates.

## Open Questions

- None. Optional follow-up: trigger search on input with debounce (e.g. `hx-trigger="keyup changed delay:300ms"`) for better UX; can be added in a later change.
