# Design: Contact detail page + edit-only edit page

## Context

The app currently has no dedicated contact "view" route. The only way to see a contact's Notes and Activities is GET `/contacts/{id}/edit`, which shows the edit form plus notes and activities. That conflates viewing (read/operate on notes and activities) with editing (changing contact fields). This change introduces a view route and narrows the edit page to editing only.

**Current state:**
- GET `/contacts/{id}/edit` returns the full edit page with contact form, notes section, and activities section.
- Notes and activities are managed via HTMX (create appends row, delete swaps row out). Routes: POST `/contacts/{id}/notes`, POST `/notes/{id}/delete`, POST `/contacts/{id}/activities`, POST `/activities/{id}/delete`.
- Templates: `contacts/edit.html`, partials `_note_row.html`, `_add_note_form_container.html`, `_activity_row.html`, `_add_activity_form_container.html`.

**Constraints:**
- No DB or schema changes.
- Notes/activities HTMX endpoints and behavior stay as-is.
- Reuse existing partials for notes and activities on the new detail page.

## Goals / Non-Goals

**Goals:**
- Add GET `/contacts/{id}` that renders a contact detail page (summary + notes + activities + "Edit contact" button).
- Make the edit page edit-only: contact form + "Back to contact" link; remove notes and activities sections from the edit template.
- Keep all existing note/activity create/delete routes and HTMX behavior; they are used from the detail page instead of the edit page.

**Non-Goals:**
- No new capabilities or API changes for notes/activities.
- No change to list page or to how users navigate to a contact from the list (list can link to detail or edit; linking to detail is a natural follow-up).
- No migration, no new models.

## Decisions

### 1. New detail route and handler

**Decision:** Add GET `/contacts/{id}` that loads the contact (with `company_ref` eager-loaded), notes (ordered by `created_at` desc), and activities (ordered by `activity_date` desc), then render `contacts/detail.html`.

**Rationale:** Matches proposal: one new route, one new template. Same data loading pattern as current edit handler for notes/activities, so we can mirror that logic.

**Alternatives:** Expose a shared "contact view data" helper used by both detail and edit; rejected for this change to keep the edit page simpler (edit will no longer load notes/activities).

### 2. Detail template structure

**Decision:** Create `contacts/detail.html` that extends the same base as edit, shows contact summary (name, email, phone, company), then includes the same Notes and Activities sections as today's edit page: `#contact-notes-list` + `_add_note_form_container.html`, `#contact-activities-list` + `_add_activity_form_container.html`. Add an "Edit contact" button/link to `/contacts/{id}/edit`.

**Rationale:** Reusing the exact same partials and container IDs keeps existing HTMX targets (e.g. `hx-target="#contact-notes-list"`) working without any change to routes or partials.

**Alternatives:** Different container IDs on detail would require conditional targets or duplicate partials; rejected.

### 3. Edit page strip-down

**Decision:** Remove from `contacts/edit.html` the Notes section and the Activities section (the two `<section>` blocks and their includes). Add a "Back to contact" link to `/contacts/{id}`. Edit handler stops loading notes and activities; remove `notes` and `activities` from the template context for GET and from all POST error paths that re-render the edit form.

**Rationale:** Edit page becomes a single-purpose form. Fewer queries and less markup on edit. Back link makes the round-trip detail → edit → detail clear.

**Alternatives:** Keep notes/activities on edit but hide via CSS; rejected because proposal explicitly says they should not be shown.

### 4. Route order and 404

**Decision:** Register GET `/contacts/{id}` in the same router as existing contact routes. Use the same 404 behavior as edit: if contact is not found, return 404 (e.g. HTTPException). Ensure this route does not conflict with GET `/contacts/new` by defining routes so that literal path segments win (e.g. `/contacts/new` before `/contacts/{id}`).

**Rationale:** FastAPI matches routes in order; `new` is already a literal. For `/contacts/123`, the `{id}` route matches. No new dependencies.

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| List page still links to edit | Out of scope for this change. List can be updated later to link to `/contacts/{id}` instead of `/contacts/{id}/edit`. |
| Bookmarked edit URLs show less content | Acceptable; edit is for editing. Users can use "Back to contact" to reach the detail view. |
| Duplicate data-loading logic (detail vs former edit) | Detail handler duplicates the note/activity loading that edit had. Acceptable for now; a shared helper could be introduced later if needed. |

## Migration Plan

- Deploy as a single release: add GET `/contacts/{id}` and `detail.html`, change `edit.html` and edit handler.
- No DB or config migration. No feature flag required.
- Rollback: revert code; no data changes to undo.

## Open Questions

- None. List page link target (detail vs edit) can be decided in a follow-up change.
