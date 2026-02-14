## 1. Contact detail page (route and template)

- [x] 1.1 Add GET `/contacts/{id}` route that loads contact (with company_ref eager-loaded), notes (order by created_at desc), and activities (order by activity_date desc); return 404 if contact not found
- [x] 1.2 Create `app/templates/contacts/detail.html`: extend base, show contact summary (name, email, phone, company display), Notes section (contact-notes-list + add note form container), Activities section (contact-activities-list + add activity form container), and "Edit contact" link to `/contacts/{id}/edit`; reuse partials _note_row.html, _add_note_form_container.html, _activity_row.html, _add_activity_form_container.html
- [x] 1.3 Ensure GET `/contacts/{id}` is registered so it does not conflict with GET `/contacts/new` (literal route before parameterized route)

## 2. Edit page edit-only

- [x] 2.1 Remove Notes section and Activities section from `app/templates/contacts/edit.html` (the two section blocks and their includes)
- [x] 2.2 Add "Back to contact" link to `/contacts/{id}` on the edit page (e.g. near the form or buttons)
- [x] 2.3 In GET `/contacts/{id}/edit` handler: stop loading notes and activities; remove `notes` and `activities` from template context
- [x] 2.4 In POST `/contacts/{id}` handler: remove `notes` and `activities` from template context in all validation-error paths that re-render the edit form

## 3. Verification

- [x] 3.1 Verify GET `/contacts/{id}` returns detail page with summary, notes list, activities list, add forms, and "Edit contact" link; GET `/contacts/{id}` returns 404 for missing contact
- [x] 3.2 Verify GET `/contacts/{id}/edit` returns edit form only (no notes/activities sections) with "Back to contact" link; note/activity HTMX create and delete still work from the detail page
