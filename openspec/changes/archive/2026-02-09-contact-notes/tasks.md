## 1. Note model and database

- [x] 1.1 Add Note model in app/models/note.py (id, contact_id FK, content, created_at, updated_at)
- [x] 1.2 Register Note in app/models/__init__.py and import in Alembic env.py
- [x] 1.3 Add Alembic migration: create notes table with contact_id FK and index on contact_id

## 2. Pydantic schema

- [x] 2.1 Add NoteFormSchema (content required, non-empty after strip) in app/schemas/note.py or app/schemas/contact.py

## 3. Edit page data loading

- [x] 3.1 In GET /contacts/{id}/edit, load notes for contact ordered by created_at desc and pass notes to edit template

## 4. Create note route

- [x] 4.1 Add POST /contacts/{contact_id}/notes in app/routes/contacts.py: Form content, validate with NoteFormSchema, 404 if contact missing
- [x] 4.2 On success: create note, return 200 with HTML fragment of new note row (id="note-{id}")
- [x] 4.3 On validation error: return 200 with HTML fragment that replaces #add-note-form-container (form + errors, pre-filled content); set HX-Retarget and HX-Reswap so response targets form container

## 5. Delete note route

- [x] 5.1 Add POST /notes/{note_id}/delete in app/routes/contacts.py: load note, 404 if missing, delete, return 200 with empty body

## 6. Edit template – notes section

- [x] 6.1 In contacts/edit.html add Notes section below contact form: list of note rows (content, created_at, delete button)
- [x] 6.2 Each note row wrapped in element with id="note-{{ note.id }}" and delete button with hx-post to /notes/{id}/delete, hx-target self, hx-swap outerHTML
- [x] 6.3 Wrap add-note form in container id="add-note-form-container"; form has hx-post to /contacts/{{ contact.id }}/notes, hx-target="#contact-notes-list", hx-swap="beforeend"
- [x] 6.4 Add notes list container id="contact-notes-list" for HTMX append of new note rows on success

## 7. Verification

- [x] 7.1 Verify edit page shows notes list (ordered created_at desc), add form works via HTMX, delete removes row via HTMX; 404 for invalid contact/note ids
