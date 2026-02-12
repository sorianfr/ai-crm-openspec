## Context

The app already supports server-rendered contacts and notes using FastAPI routes, SQLAlchemy models, Jinja2 templates, and Alembic migrations. Contacts currently store company as a free-text `company` column and contact forms are validated with Pydantic schemas, then re-rendered on validation errors (HTTP 200). This change introduces a first-class `Company` entity and optional contact-to-company linkage while preserving existing `Contact.company` behavior to avoid breaking current workflows.

## Goals / Non-Goals

**Goals:**
- Add a new `companies` table and minimal Companies CRUD routes/pages: list, new, create, edit, update, delete.
- Add nullable `contacts.company_id` as a foreign key to `companies.id` with `ON DELETE SET NULL`, plus an index.
- Keep `contacts.company` string untouched and continue reading/writing it as before.
- Update contact new/edit forms to include an optional company dropdown that sets `company_id`.
- Keep implementation server-rendered (Jinja2 + form POST), with HTMX delete optional for companies.

**Non-Goals:**
- Migrating or normalizing legacy `contacts.company` text values into `companies`.
- Removing or repurposing `contacts.company` in this change.
- Building advanced company features (search, pagination, deduping, merge, REST API).

## Decisions

### Decision 1: Additive schema evolution only

**Approach:** Introduce `Company` as a new model/table and add `Contact.company_id` as nullable foreign key + index. The foreign key uses `ON DELETE SET NULL` so deleting a company never deletes contacts and does not fail due to referencing rows. Keep `Contact.company` (string) in model, forms, and persistence logic.

**Rationale:** This preserves compatibility and avoids data-loss or behavior regressions for existing contacts and tests. It also creates a clear migration path for a later full normalization change.

**Alternatives considered:** Replace `contacts.company` now (rejected: breaking behavior and higher migration risk).

### Decision 2: Company CRUD follows existing contact route/template style

**Approach:** Implement companies in a dedicated route module and template directory using the same server-rendered pattern as contacts:
- `GET /companies` list
- `GET /companies/new`, `POST /companies`
- `GET /companies/{id}/edit`, `POST /companies/{id}`
- `POST /companies/{id}/delete`

Validation uses a Pydantic form schema; on validation errors, re-render form with errors (HTTP 200). Delete may be standard POST+redirect or HTMX row removal; both are allowed by scope.

**Rationale:** Reuses proven patterns in this codebase and minimizes implementation complexity.

**Alternatives considered:** JSON API + SPA interactions (rejected: outside this server-rendered scope).

### Decision 3: Contact forms carry both legacy text and company reference

**Approach:** Extend contact create/edit handlers to accept optional `company_id` from a dropdown populated with existing companies. Keep existing text input for `company`; both fields are submitted and persisted independently (`company` text + `company_id` reference).

Validation rules:
- `company_id` may be omitted/blank (stored as `NULL`).
- If provided, it must reference an existing company; otherwise re-render with validation error.
- Existing `full_name`/`email` validation behavior remains unchanged.

**Rationale:** Satisfies non-breaking requirement and allows gradual adoption of structured linkage.

**Alternatives considered:** Auto-clearing text company when `company_id` is set (rejected: unexpected behavior change).

### Decision 4: Explicit relationship wiring in models, but conservative UI usage

**Approach:** Add SQLAlchemy relationship fields (`Contact.company_ref` / `Company.contacts`) for query ergonomics while keeping UI behavior conservative. Contact list display remains based on legacy `Contact.company` text for this change (no list UI behavior change). Contact new/edit forms gain optional `company_id` dropdown selection only.

**Rationale:** Relationship fields simplify lookups and future enhancements without forcing immediate UI behavior changes that could be interpreted as breaking.

**Alternatives considered:** No ORM relationships (rejected: more repetitive query code).

### Decision 5: Migration strategy is forward-compatible and rollback-safe

**Approach:** One migration adds `companies` table and `contacts.company_id` nullable column with index and foreign key (`ON DELETE SET NULL`). No backfill is performed. Downgrade drops FK/index/column and the companies table.

**Rationale:** Additive migration is low risk in production-like environments and does not require data transformation.

**Alternatives considered:** Two migrations (table first, FK later) were not chosen since current scope is small and can be safely expressed in one revision.

## Risks / Trade-offs

- [Risk] Contacts can have inconsistent text company and selected `company_id`. -> Mitigation: accept this as intentional transitional state; document behavior and defer reconciliation rules to a later change.
- [Risk] Company deletion can silently clear `company_id`, which may surprise users. -> Mitigation: document behavior and keep legacy `Contact.company` text visible in list view so users retain company context.
- [Trade-off] Supporting both legacy and structured company fields increases form and validation complexity. -> Mitigation: keep rules minimal and reuse existing form/schema patterns.
- [Trade-off] Optional HTMX for company delete means minor UX inconsistency. -> Mitigation: prioritize correctness; HTMX enhancement can be added without API changes.

## Migration Plan

1. Add `Company` model and update `Contact` model with nullable `company_id` and relationship definitions while retaining `company` string column.
2. Generate/apply Alembic revision:
   - Create `companies` table.
   - Add nullable `contacts.company_id`.
   - Add foreign key from `contacts.company_id` to `companies.id` with `ON DELETE SET NULL`.
   - Add index on `contacts.company_id`.
3. Add companies routes/templates and contact form updates for dropdown selection.
4. Verify create/edit/update/delete flows for companies and create/edit flows for contacts with and without `company_id`.
5. Rollback plan: downgrade migration (drop FK/index/column/table) and revert route/template/model changes.

## Open Questions

- None blocking for this phase.
