## Why

Contacts currently store company as free text, which leads to duplicates and inconsistent naming. Introducing a first-class Company entity now enables structured assignment without disrupting existing contact data entry.

## What Changes

- Add a new `Company` table and minimal server-rendered CRUD flows: list, new, create, edit, update, and delete (Jinja2-based; HTMX delete optional).
- Add an optional `Contact.company_id` foreign key so each contact can be linked to one existing company.
- Keep the existing `Contact.company` string field unchanged as legacy/free-text in this change (no replacement or removal).
- Update contact new/edit forms to include an optional company dropdown sourced from existing companies, setting `company_id` while preserving the current text field behavior.
- Add migrations for the `companies` table and nullable `contacts.company_id` column, including an index on `company_id`.
- Add validation and not-found handling for company CRUD and company selection in contact forms.

## Capabilities

### New Capabilities
- `companies-crud`: Manage company records and expose selectable company data for related workflows.

### Modified Capabilities
- `contacts-crud`: Add optional company assignment via `company_id` in contact create/edit forms while retaining the existing free-text `company` field.

## Impact

- Affected specs: new `companies-crud`; modified `contacts-crud`.
- Affected code: SQLAlchemy models, Alembic migrations, FastAPI routes, form handling, and Jinja2 templates for companies and contact forms.
- Data impact: additive schema changes only (`companies` table, nullable `contacts.company_id`, and index); existing `contacts.company` data remains intact.
- Compatibility: no breaking changes to existing contact text-company workflows in this phase.
- Testing impact: add coverage for companies CRUD routes, migration shape, and optional contact `company_id` assignment.
