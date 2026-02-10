## Context

The application already has the bootstrap in place: FastAPI, SQLite via SQLAlchemy, Alembic, Jinja2 templates, and HTMX in the base template. Routes live under `app/routes/`, templates under `app/templates/`, and the database layer in `app/db/` (base, session). There are no domain models or CRUD features yet. This change adds the first domain entity (Contact) and full CRUD with a server-rendered UI, reusing the existing stack without new infrastructure.

## Goals / Non-Goals

**Goals:**
- Add a Contact model and `contacts` table with the agreed fields and validations.
- Implement the six exact routes (list, new, create, edit, update, delete) with 404 when contact is missing.
- Serve all contact pages via Jinja2; support HTMX delete-from-list (row removal without full reload).
- Keep create/edit as simple POST + redirect (no HTMX partials required).
- Add a discoverable link to Contacts from the homepage (or base layout).

**Non-Goals:**
- REST/JSON API for contacts; authentication; pagination (can be added later); soft delete; audit logging.

## Decisions

### Decision 1: Contact model location

**Approach:** Define the Contact model in `app/models/contact.py`, with `app/models/__init__.py` exposing the model (e.g. `from app.models.contact import Contact`). The model SHALL inherit from `app.db.base.Base` so it uses the existing engine/session and Alembic metadata.

**Rationale:** A dedicated `app/models/` package keeps domain models separate from the generic db layer and scales to more entities (e.g. Company, Note) without crowding `app/db`. Single file per model keeps the package simple.

**Alembic:** Ensure `alembic/env.py` imports the Contact model (e.g. `from app.models import Contact` or `from app.models.contact import Contact`) so that `Base.metadata` (or the same metadata the model is bound to) includes the `contacts` table for autogenerate. If the model were kept in `app/db/models.py` instead, the same requirement applies: env must import that module so metadata includes Contact.

### Decision 2: Form submission and validation (no JSON / no 422 for UI)

**Approach:** Create and update forms submit as **application/x-www-form-urlencoded** (standard HTML form POST). In the route handlers, use **FastAPI `Form(...)`** to read the fields (full_name, email, phone, company). After reading form data, validate with a **Pydantic schema** (e.g. in `app/schemas/contact.py`): full_name required, email/phone/company optional, email format validated when present. Use the same schema for create and update.

- **On success:** Create or update the contact and redirect (e.g. to `/contacts` or the contact’s edit page).
- **On validation error:** Do **not** return 422 or rely on JSON. Re-render the same form template (new.html or edit.html) with the submitted values and error messages, and return **HTTP 200**.

**Rationale:** The UI is server-rendered; users stay on the form page and see inline validation errors. No JSON body or 422 for these flows.

**Alternatives considered:** JSON body + 422 (not used for the form UI); form-only validation in templates (duplicated logic).

### Decision 3: Route module and URL shape

**Approach:** Implement all contact routes in `app/routes/contacts.py` with a single router mounted under a prefix (e.g. no prefix so paths are exactly `GET /contacts`, `GET /contacts/new`, `POST /contacts`, `GET /contacts/{id}/edit`, `POST /contacts/{id}`, `POST /contacts/{id}/delete`). Use path parameter `id` (integer or string); resolve contact and return 404 if not found. For **GET /contacts**, load contacts ordered by **updated_at descending** (most recently updated first).

**Rationale:** Matches the proposal’s exact routes; one module keeps contact logic discoverable. Ordering by updated_at descending keeps the list relevant to recent activity.

**Alternatives considered:** Separate routers per “resource” (overkill for this scope); string slugs instead of id (id is simpler and already specified).

### Decision 4: Create and edit – form POST, Form(...), redirect or 200 re-render

**Approach:** Create and edit use standard HTML form POST (application/x-www-form-urlencoded). Route handlers declare parameters with **FastAPI `Form(...)`** to receive the fields. Validate with the Pydantic schema; on success, redirect (e.g. to `GET /contacts` or the contact’s edit page). On validation failure, re-render the form template with the submitted values and error messages and return **HTTP 200** (do not use 422 for the UI). No HTMX partials required for these flows.

**Rationale:** Keeps the UI flow simple and accessible; validation errors are shown in the same page. HTMX is reserved for delete-from-list.

**Alternatives considered:** HTMX partials for create/edit (explicitly not required); JSON body and 422 (not used for form UI).

### Decision 5: HTMX delete-from-list (concrete pattern)

**Approach:** Use a simple, reliable pattern with no out-of-band swap:

- In `list.html`, each contact row is wrapped in an element with `id="contact-{{ id }}"` (e.g. `<tr id="contact-{{ contact.id }}">` or a `<div>` with that id).
- The delete button (or link) uses:
  - `hx-post="/contacts/{{ contact.id }}/delete"`
  - `hx-target="#contact-{{ contact.id }}"`
  - `hx-swap="outerHTML"`
- The delete endpoint `POST /contacts/{id}/delete` returns **200** with an **empty body** (or a minimal fragment like an empty string or single empty element). HTMX replaces the target’s outer HTML with that response, so the row disappears.

**Rationale:** Same-origin target + outerHTML swap is predictable and works without OOB swap or 204 handling. Empty response body makes the row vanish reliably.

### Decision 6: 404 when contact not found

**Approach:** For `GET /contacts/{id}/edit`, `POST /contacts/{id}`, and `POST /contacts/{id}/delete`, load the contact by id (from path). If no row exists (or id invalid), raise/return FastAPI’s `HTTPException(status_code=404)`. Do not create or update on not-found.

**Rationale:** Matches the spec and avoids leaking existence of contacts via different error behaviour.

### Decision 7: Homepage / base link to Contacts

**Approach:** Add a link to `/contacts` in the base template (e.g. `app/templates/base.html`) so every page, including the homepage, shows a consistent “Contacts” entry (nav or prominent link). If the project prefers a homepage-only link, add it to `app/templates/index.html` instead; base is preferred so the link is available from list/edit/new as well.

**Rationale:** Satisfies “users can discover and access contacts”; base template gives one place to maintain the link.

**Alternatives considered:** Link only on homepage (still valid; base is better for navigation).

### Decision 8: Template layout for contacts

**Approach:** Add `app/templates/contacts/` with: `list.html` (list page; each row has `id="contact-{{ id }}"` and a delete button with `hx-post`, `hx-target`, `hx-swap="outerHTML"` as in Decision 5), `new.html` (create form), `edit.html` (edit form). Rows may be inline in `list.html` or in a partial; the row id and delete attributes are required. All extend `base.html`.

**Rationale:** Keeps contact UI in one directory; the concrete row-id and HTMX delete pattern is documented in Decision 5.

## Risks / Trade-offs

- **Risk:** No pagination on list; large contact sets could slow the list page.
  - **Mitigation:** Accept for this change; add pagination in a later iteration if needed.

- **Trade-off:** Single schema for create/update (same fields) vs separate create/update schemas.
  - **Decision:** Single schema is enough; id and timestamps are server-managed.

## Migration Plan

1. Add `app/models/__init__.py` and `app/models/contact.py` with the Contact model (inheriting from `app.db.base.Base`). Ensure `alembic/env.py` imports the model (e.g. `from app.models import Contact`) so `Base.metadata` includes the `contacts` table for autogenerate.
2. Generate and apply an Alembic migration that creates the `contacts` table (id, full_name NOT NULL, email, phone, company, created_at, updated_at).
3. Deploy/run the app; no data migration or backfill required. Rollback: revert code and run a downgrade migration that drops `contacts` if needed.

## Open Questions

- None blocking. Optional: whether to add a simple “Contacts” label or icon in the base nav for future consistency with other CRM sections.
