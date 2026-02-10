<!-- Implementation reminder: Create/edit are server-rendered HTML forms (application/x-www-form-urlencoded). Use FastAPI Form(...) for request fields and validate with Pydantic; on validation errors re-render the form template with error messages (HTTP 200). Do not use JSON body or 422 for these UI flows. -->

## 1. Contact model and package

- [x] 1.1 Create `app/models/__init__.py` and export Contact (e.g. `from app.models.contact import Contact`)
- [x] 1.2 Create `app/models/contact.py` with Contact model inheriting from `app.db.base.Base`, fields: id, full_name (required), email, phone, company, created_at, updated_at
- [x] 1.3 Ensure created_at and updated_at are set on insert; updated_at set on update

## 2. Alembic and migration

- [x] 2.1 In `alembic/env.py`, import Contact (e.g. `from app.models import Contact`) so Base.metadata includes the contacts table
- [x] 2.2 Generate Alembic migration for the contacts table (id, full_name NOT NULL, email, phone, company, created_at, updated_at)
- [x] 2.3 Apply migration (`alembic upgrade head`)

## 3. Pydantic schemas

- [x] 3.1 Create `app/schemas/contact.py` (or equivalent) with a schema for create/update: full_name required, email/phone/company optional, email validated when present
- [x] 3.2 Use the schema in contact routes to validate form data (after reading with Form(...)); on validation errors re-render the form template with error messages and return HTTP 200 (do not use JSON body or 422 for the UI flows)

## 4. Contact routes – list and create

- [x] 4.1 Create `app/routes/contacts.py` with a FastAPI APIRouter
- [x] 4.2 Implement GET `/contacts`: load contacts ordered by updated_at descending (most recently updated first), render `app/templates/contacts/list.html` with contacts
- [x] 4.3 Implement GET `/contacts/new`: render `app/templates/contacts/new.html` with create form
- [x] 4.4 Implement POST `/contacts`: accept form data via FastAPI Form(...) (full_name, email, phone, company); validate with Pydantic schema; on success create contact and redirect to `/contacts`; on validation error re-render `new.html` with submitted values and error messages (HTTP 200)

## 5. Contact routes – edit, update, delete

- [x] 5.1 Implement GET `/contacts/{id}/edit`: load contact by id, return 404 if not found, render `app/templates/contacts/edit.html`
- [x] 5.2 Implement POST `/contacts/{id}`: load contact by id, 404 if not found; accept form via Form(...); validate with Pydantic schema; on success update contact and redirect; on validation error re-render `edit.html` with submitted values and errors (HTTP 200)
- [x] 5.3 Implement POST `/contacts/{id}/delete`: load contact by id, 404 if not found; delete contact; return 200 with empty body (so HTMX outerHTML swap removes the row)

## 6. Templates – list and HTMX delete

- [x] 6.1 Create `app/templates/contacts/list.html` extending base; show contacts in a table or list
- [x] 6.2 In list.html, each row has `id="contact-{{ contact.id }}"`; delete button has `hx-post="/contacts/{{ contact.id }}/delete"`, `hx-target="#contact-{{ contact.id }}"`, `hx-swap="outerHTML"`
- [x] 6.3 Add link from list to “New contact” (e.g. `/contacts/new`) and per-row link to edit (e.g. `/contacts/{{ contact.id }}/edit`)

## 7. Templates – new and edit forms

- [x] 7.1 Create `app/templates/contacts/new.html` with form method="post" action="/contacts" (application/x-www-form-urlencoded), fields: full_name (required), email, phone, company; display validation errors when passed from route (HTTP 200 re-render)
- [x] 7.2 Create `app/templates/contacts/edit.html` with form method="post" action="/contacts/{{ contact.id }}", same fields pre-filled; display validation errors when passed from route (HTTP 200 re-render)
- [x] 7.3 Both templates extend base and use existing Jinja2/template patterns

## 8. Base template link and router registration

- [x] 8.1 In `app/templates/base.html`, add a link to `/contacts` (e.g. “Contacts” in nav or prominent link)
- [x] 8.2 In `app/main.py`, include the contacts router so GET/POST `/contacts`, `/contacts/new`, `/contacts/{id}/edit`, `/contacts/{id}`, `/contacts/{id}/delete` are served

## 9. Verification

- [x] 9.1 Verify GET `/contacts` shows list (empty or with data)
- [x] 9.2 Verify create flow: GET `/contacts/new`, submit valid form, redirect and see new contact in list
- [x] 9.3 Verify create validation: empty full_name or invalid email re-renders form with error messages (HTTP 200, no 422)
- [x] 9.4 Verify edit flow: GET `/contacts/{id}/edit`, update, redirect and see changes
- [x] 9.5 Verify 404: GET `/contacts/999/edit` (or nonexistent id) returns 404
- [x] 9.6 Verify HTMX delete: from list, click delete on a row; row disappears without full page reload
- [x] 9.7 Verify POST `/contacts/{id}/delete` for nonexistent id returns 404
- [x] 9.8 Verify base template link: “Contacts” (or equivalent) visible and links to `/contacts`
