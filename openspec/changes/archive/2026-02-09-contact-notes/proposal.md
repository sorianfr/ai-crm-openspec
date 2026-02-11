## Why

Users need to attach notes to contacts (e.g. call summaries, follow-ups). Adding contact notes as a server-rendered feature with Jinja2 and HTMX keeps the stack consistent with the existing contacts CRUD and allows create/delete from the contact edit page without full page reloads.

## What Changes

- Add a **Note** model: id, contact_id (FK to Contact), content (required text), created_at, updated_at.
- **List notes** for a contact (required). Notes ordered by **created_at descending**.
- **Create note** via HTMX from the contact edit page: POST `/contacts/{id}/notes`.
- **Delete note** via HTMX from the contact edit page: POST `/notes/{note_id}/delete` (e.g. row removal).
- **No edit-note** flow in this change; no separate notes page; no link from the contacts list.
- Notes UI lives **only on GET `/contacts/{id}/edit`**: the edit page SHALL show the contact’s notes (list + inline add form + delete per row via HTMX).

## Capabilities

### New Capabilities

- `contact-notes`: Notes attached to a contact. Note model (id, contact_id, content, created_at, updated_at); list notes for a contact (created_at desc); create via POST `/contacts/{id}/notes` and delete via POST `/notes/{note_id}/delete`; UI and HTMX create/delete on the contact edit page only.

### Modified Capabilities

- `contacts-crud`: The contact edit page (GET `/contacts/{id}/edit`) SHALL display the contact’s notes section (list, add form, delete per note via HTMX). No new routes or links from the contacts list.

## Impact

- **Data**: New `notes` table with contact_id (FK), content (required), created_at, updated_at; Alembic migration; index on contact_id.
- **App**: New Note model (e.g. `app/models/note.py`), Pydantic schema(s), routes POST `/contacts/{id}/notes` and POST `/notes/{note_id}/delete`; contact edit template updated to include notes list, add form, and HTMX delete.
- **Dependencies**: None new.
- **Existing**: Contact edit route and template only; no changes to contact list or other contact routes.
