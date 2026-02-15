# Contact detail page (view) + edit page only for editing

## Why

Today, to see a contact's Notes and Activities you must go through the Edit page. That mixes two different intents:
- viewing a contact and its interaction history (read/operate)
- editing the contact's fields (write)

A dedicated contact detail page improves UX and matches how CRMs work:
- users open a contact to see context (notes/activities/timeline)
- editing is a deliberate action via an "Edit" button

## What Changes

### New route: Contact detail page
Add a new server-rendered page:

- GET `/contacts/{id}`

This page SHALL display:
- Contact summary (name, email, phone, company display)
- Notes section (list + add + delete via HTMX) — same behavior as today
- Activities section (list + add + delete via HTMX) — same behavior as today
- A visible "Edit contact" button linking to `/contacts/{id}/edit`

### Edit page becomes "edit only"
Keep the existing edit route:

- GET `/contacts/{id}/edit`
- POST `/contacts/{id}`

But the edit page SHALL focus on editing contact fields only.
Notes and Activities SHOULD NOT be shown on the edit page anymore (to keep it clean).

The edit page SHALL include a "Back to contact" link to `/contacts/{id}`.

### No changes to create/delete behavior
All existing routes for notes and activities remain unchanged:

- POST `/contacts/{id}/notes`
- POST `/notes/{note_id}/delete`
- POST `/contacts/{id}/activities`
- POST `/activities/{activity_id}/delete`

No DB migrations in this change.

## Capabilities

### New capabilities
- None (this is mainly a UI/navigation restructure)

### Modified capabilities
- contacts-crud:
  - Add GET `/contacts/{id}` contact detail page
  - Edit page becomes edit-only UI (no notes/activities sections)

- contact-notes:
  - Notes are displayed and managed on contact detail page

- contact-activities:
  - Activities are displayed and managed on contact detail page

## Impact

- Routes:
  - Add GET `/contacts/{id}`

- Templates:
  - Add `app/templates/contacts/detail.html` (new)
  - Update `app/templates/contacts/edit.html` (remove notes/activities; add back link)
  - Reuse existing partials:
    - notes: `_note_row.html`, `_add_note_form_container.html`
    - activities: `_activity_row.html`, `_add_activity_form_container.html`

- Backend:
  - GET detail handler loads contact + notes + activities and passes to template
  - Ensure company_ref is eager-loaded (if display_company is used)

- Behavior:
  - Notes/Activities HTMX behavior stays the same (create append, delete row removal)
