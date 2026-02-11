## Context

The app already has contact CRUD: FastAPI, Jinja2 templates, Form + Pydantic validation, and HTMX for delete (contact list row removal via POST to delete, response 200 with empty body and `hx-swap="outerHTML"`). The contact edit page is GET `/contacts/{contact_id}/edit` and renders `contacts/edit.html` with the contact form; there is no notes section yet. This change adds notes that live only on that edit page: list, create, and delete via HTMX, with no separate notes page and no link from the contacts list.

## Goals / Non-Goals

**Goals:**

- Add a Note model and `notes` table; list notes for a contact on the edit page, ordered by `created_at` desc.
- Create note via HTMX from the edit page (POST `/contacts/{id}/notes`); delete note via HTMX (POST `/notes/{note_id}/delete`) with row removal.
- Keep implementation consistent with existing patterns: Form + Pydantic, server-rendered HTML, HTMX for partial updates.

**Non-Goals:**

- Editing an existing note; a dedicated notes page; a link to notes from the contacts list.
- New dependencies; changes to contact list or other contact routes beyond the edit page.

## Decisions

**1. Note model and persistence**

- Add `app/models/note.py` with a `Note` model: `id`, `contact_id` (FK to Contact), `content` (required text), `created_at`, `updated_at`. Register in `app/models/__init__.py` and ensure Alembic `env.py` imports it. Use one Alembic migration adding the `notes` table and an index on `contact_id`.
- **Rationale:** Matches proposal; timestamps support future edit/audit if we add it later. Single migration keeps rollout simple.

**2. Where to put note routes**

- Keep note routes in **app/routes/contacts.py** so all contact-edit surface (contact form + notes) lives in one place.

**3. Create note (POST `/contacts/{id}/notes`)**

- Accept `content` via `Form(...)`. Validate with a Pydantic schema (e.g. `NoteFormSchema`: content required, non-empty after strip). If contact does not exist, return 404.
- **HTMX targets:** The add-note form uses `hx-target="#contact-notes-list"` and `hx-swap="beforeend"` so the default behavior is to append the response to the notes list.
- **On success:** Return 200 with HTML fragment of the new note row (e.g. a wrapper with `id="note-{{ note.id }}"`). The response is appended to `#contact-notes-list`; the form stays as-is and keeps targeting the list for the next submit.
- **On validation error:** Return 200 with an HTML fragment that replaces `#add-note-form-container` (the wrapper around the add-note form). The fragment SHALL contain the add-note form plus validation errors and pre-filled content. So that this response goes to the form container (not the list), the response SHALL include the HTMX response headers `HX-Retarget: #add-note-form-container` and `HX-Reswap: outerHTML` so the fragment replaces the form container and errors show in place.
- **Rationale:** Separate targets for success vs error: success appends a row to the list; error replaces the form area so errors appear in place and are not appended to the list.

**4. Delete note (POST `/notes/{note_id}/delete`)**

- Load note by id; if not found, return 404. Delete and commit; return 200 with empty body (same as contact delete).
- The note row in the template MUST be wrapped in an element with a stable id (e.g. `id="note-{{ note.id }}"`) and the delete button MUST use `hx-post` to this URL with `hx-target` that element and `hx-swap="outerHTML"` so the row is replaced by the empty response and disappears.
- **Rationale:** Matches existing contact delete behavior and proposal (HTMX row removal).

**5. Edit page data and template**

- GET `/contacts/{id}/edit`: Load contact and its notes (e.g. `db.execute(select(Note).where(Note.contact_id == contact_id).order_by(Note.created_at.desc()))`). Pass `contact` and `notes` to `contacts/edit.html`.
- In the template, add a "Notes" section below the contact form: (1) a notes list container with `id="contact-notes-list"` containing note rows (each with content, created_at, delete button with HTMX), (2) a wrapper `id="add-note-form-container"` containing the inline "Add note" form (content field, submit). The form uses HTMX: `hx-post` to `/contacts/{id}/notes`, `hx-target="#contact-notes-list"`, `hx-swap="beforeend"`. On success the response is the note row and is appended to the list; on validation error the server returns a fragment plus `HX-Retarget` / `HX-Reswap` so the form container is replaced and errors show in place.
- **Rationale:** Single source of truth for the edit page; separate targets keep success (append row) and error (replace form area) behavior clear.

**6. Validation and 404**

- Content required and non-empty after strip; no other validations in this change. 404 when contact id on create is invalid or note id on delete is invalid.
- **Rationale:** Keeps scope small; more validation can be added later.

## Risks / Trade-offs

- **Validation errors on create:** If we return a fragment that only contains error text, the user might lose the typed content unless we re-render the form with `form_content` in the fragment. Mitigation: On validation error, return a fragment that replaces `#add-note-form-container` (via HX-Retarget / HX-Reswap) and includes the add-note form pre-filled with the submitted content and error messages.
- **Delete from wrong contact:** POST `/notes/{note_id}/delete` deletes by note id only; we do not check that the note belongs to the "current" contact. Mitigation: Acceptable for this scope; note id is unguessable. If needed later, we can add a check that the note’s contact_id matches the session or referrer.
- **No CSRF:** Same as existing contact forms; out of scope for this change.

## Migration Plan

- Single Alembic migration: create `notes` table (id, contact_id FK, content NOT NULL, created_at, updated_at), index on contact_id. No backfill. Deploy: run migrations as usual; rollback: downgrade migration to drop the table.

## Open Questions

- None for implementation. Optional follow-up: add edit-note in a future change if needed.
