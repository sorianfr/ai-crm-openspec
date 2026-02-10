## Why

We need a first-class Contacts feature on top of the existing FastAPI + SQLite + Jinja2 + HTMX foundation. Today the app only exposes a basic homepage and health check; there is no way to capture, view, or edit contact records, which blocks any real CRM workflows.

## What Changes

- **Contacts model**: Introduce a `Contact` entity with fields: `id`, `full_name` (required), `email` (optional), `phone` (optional), `company` (optional), `created_at`, `updated_at`, persisted in SQLite via SQLAlchemy and Alembic.
- **Routes** (exact):
  - `GET /contacts` — list contacts (server-rendered Jinja2 page).
  - `GET /contacts/new` — show create-contact form.
  - `POST /contacts` — create contact (standard POST; MAY use redirect, no HTMX partials required).
  - `GET /contacts/{id}/edit` — show edit form for contact.
  - `POST /contacts/{id}` — update contact (standard POST; MAY use redirect).
  - `POST /contacts/{id}/delete` — delete contact.
- **HTMX scope**: Delete from the list MUST use HTMX: submitting delete removes the row from the list without full page reload (e.g. POST returns a fragment or 204, row removed via `hx-swap`). Create and edit MAY be implemented as standard POST + redirect; partials are not required for create/edit.
- **Validations**: `full_name` required; `email` must be valid if provided; 404 when contact not found (e.g. invalid id for get/edit/update/delete).
- **Migrations**: Alembic migration(s) adding the `contacts` table.

## Capabilities

### New Capabilities
- `contacts-crud`: End-to-end ability to create, read, update, and delete contact records via the routes above; server-rendered Jinja2 UI with HTMX required only for delete-from-list (row removal); create/edit may use standard POST + redirect.

### Modified Capabilities
- `homepage`: Extend the homepage spec to link to the Contacts feature (e.g., navigation item or call-to-action) so users can discover and access contacts.

## Impact

- **Database**: New `contacts` table with columns for id, full_name (required), email, phone, company, created_at, updated_at; managed via SQLAlchemy and Alembic.
- **Backend code**:
  - Contact model (e.g. under `app/db` or `app/models`) and Pydantic schemas for validation.
  - Routes in `app/routes/contacts.py` implementing the exact paths above; 404 when contact not found.
- **Templates/UI**:
  - Jinja2 templates under `app/templates/contacts/` for list, new form, edit form, and (for HTMX delete) a list-row partial or fragment.
  - Homepage (or base template) updated to link to Contacts (e.g. nav to `/contacts`).
- **HTMX**: Delete flow only MUST support HTMX row removal from the list; create/edit MAY be POST+redirect.
- **Validations**: full_name required; email validated if present; 404 for missing contact id.
