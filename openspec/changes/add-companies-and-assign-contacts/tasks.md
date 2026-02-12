## 1. Models and schema migration

- [x] 1.1 Add `app/models/company.py` with Company model (`id`, `name`, `created_at`, `updated_at`) and export it from `app/models/__init__.py`
- [x] 1.2 Update `app/models/contact.py` to add nullable `company_id` FK to `companies.id` (with `ondelete="SET NULL"`), index on `company_id`, and relationship fields while keeping legacy `company` string unchanged
- [x] 1.3 Ensure Alembic metadata loading includes the new Company/Contact model changes (import path in `alembic/env.py` if needed)
- [x] 1.4 Create Alembic revision to add `companies` table and `contacts.company_id` (nullable FK + index, `ON DELETE SET NULL`)
- [x] 1.5 Apply migration locally and verify upgrade/downgrade runs cleanly

## 2. Company form schema and routes

- [x] 2.1 Add `CompanyFormSchema` in `app/schemas/company.py` with required non-empty `name` validation
- [x] 2.2 Create `app/routes/companies.py` with helper lookup for 404 behavior on missing company ids
- [x] 2.3 Implement GET `/companies` and GET `/companies/new` as server-rendered Jinja2 pages
- [x] 2.4 Implement POST `/companies` with form parsing, validation, success redirect, and HTTP 200 form re-render on validation errors
- [x] 2.5 Implement GET `/companies/{id}/edit` and POST `/companies/{id}` with prefill, validation, redirect on success, and 404/not-valid handling
- [x] 2.6 Implement POST `/companies/{id}/delete` with 404 for missing company and response compatible with server-rendered or HTMX-triggered delete

## 3. Company templates and navigation

- [x] 3.1 Add `app/templates/companies/list.html` to render companies with edit/delete actions
- [x] 3.2 Add `app/templates/companies/new.html` and `app/templates/companies/edit.html` with name field and validation error rendering
- [x] 3.3 Add navigation entry/link to `/companies` (and list-to-new/edit links) following existing template style

## 4. Contact create/edit integration for company_id

- [x] 4.1 Update GET `/contacts/new` and GET `/contacts/{id}/edit` to load companies for dropdown options
- [x] 4.2 Update POST `/contacts` and POST `/contacts/{id}` to accept optional `company_id` from form data (blank -> NULL)
- [x] 4.3 Validate non-empty `company_id` values against existing companies and re-render the same form with HTTP 200 on invalid selection
- [x] 4.4 Persist `company` (legacy text) and `company_id` independently in create/update flows
- [x] 4.5 Preserve selected `company_id` and dropdown options when re-rendering forms after validation errors

## 5. Contacts list and legacy display compatibility

- [x] 5.1 Keep contacts list display bound to legacy `Contact.company` text (no switch to related Company name in this change)
- [x] 5.2 Ensure existing contact list ordering and HTMX delete behavior remain unchanged after model/route updates

## 6. App wiring and imports

- [x] 6.1 Register companies router in `app/main.py` so all `/companies` routes are served
- [x] 6.2 Update schema/module exports (`app/schemas/__init__.py` and related imports) for new company schema usage

## 7. Manual verification and regression checks

- [x] 7.1 Manually verify Companies CRUD flows (`/companies` list/new/create/edit/update/delete), including validation re-render behavior (HTTP 200) and 404 handling for missing company ids
- [x] 7.2 Manually verify contacts create/edit flows with optional `company_id` (blank allowed, invalid selection shows validation errors, valid selection persists)
- [x] 7.3 Manually verify migration/data behavior: deleting a company sets referencing `contacts.company_id` to NULL and does not delete contacts
- [x] 7.4 Manually verify contacts list still shows legacy `company` text after assigning `company_id`
- [x] 7.5 Document manual smoke-check results for `/contacts` and `/companies`; do not add pytest or new automated test framework in this change

## Manual Verification Notes (2026-02-12)

- Used temporary database `manual_verify.db` to avoid changing local default DB state.
- Migration cycle validated on temp DB: `upgrade head`, `downgrade 002`, `upgrade head`.
- Verified companies flows manually over running app on port 8001: list/new/create/edit/update/delete, validation HTTP 200 re-render, and 404s for missing ids.
- Verified contacts create/edit accepts optional `company_id`; invalid `company_id` re-renders with validation error; valid `company_id` persists.
- Verified deleting a company sets referencing `contacts.company_id` to NULL while contact rows remain.
- Verified contacts list continues to display legacy `contacts.company` text (no list display switch to related company name).
