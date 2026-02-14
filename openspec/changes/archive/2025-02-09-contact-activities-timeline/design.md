# Design: Contact activity timeline

## Context

- **Current state**: Contact edit page has a Notes section: list of notes (ordered by created_at DESC), inline add-note form, per-note delete. Notes use POST `/contacts/{id}/notes` (create, returns row fragment) and POST `/notes/{note_id}/delete` (delete, empty 200, row removed via hx-swap). Activity timeline SHALL mirror this pattern for consistency and reuse of existing HTMX/Jinja2 patterns.
- **Constraint**: No separate activities page; activities live only on contact edit. Use existing stack (FastAPI, SQLAlchemy, Alembic, Jinja2, HTMX).
- **Stakeholders**: Users viewing a contact who want to see and record calls, emails, meetings, and tasks in one place.

## Goals / Non-Goals

**Goals:**
- Add Activity model (contact_id, type, description, activity_date, created_at, updated_at) with Alembic migration.
- Expose activities on contact edit page: list (activity_date DESC), inline add form, delete per row; create and delete via HTMX (same UX as notes).
- Add POST `/contacts/{contact_id}/activities` and POST `/activities/{activity_id}/delete`; no new GET routes.

**Non-Goals:**
- No activities list page, no global activity feed, no edit activity (add/delete only in this change). No reminders or due dates for tasks. No linking activities to companies.

## Decisions

1. **activity_date type**
   - **Choice**: Store as **datetime** (e.g. `DateTime` in SQLAlchemy) with optional time part. Display can show date only or date+time depending on type or UI.
   - **Rationale**: Supports "when did we talk" and "meeting at 2pm"; date-only can be represented with time 00:00:00. Simpler than separate date + optional time columns.
   - **Alternative**: Date only. Rejected to allow future time-of-day for meetings/calls.

2. **Activity type storage**
   - **Choice**: Store `type` as a string column (e.g. `String(32)`) with values `call`, `email`, `meeting`, `task`. Validate in application (Pydantic schema or route) and optionally constrain in DB (CHECK or enum type) in migration.
   - **Rationale**: Keeps schema simple; easy to add types later. Matches proposal enum.
   - **Alternative**: Integer enum in DB. Rejected for readability and simpler migrations.

3. **Contact → Activity relationship**
   - **Choice**: Activity has `contact_id` FK to `contacts.id` with **ON DELETE CASCADE** so deleting a contact removes their activities.
   - **Rationale**: Same as Notes; avoids orphaned rows.

4. **HTMX and template structure**
   - **Choice**: Mirror Notes: (1) Activity list container (e.g. `#contact-activities-list`) with rows; (2) Add-activity form in a container (e.g. `#add-activity-form-container`) for error retarget; (3) Create returns single activity-row fragment, hx-target list, hx-swap beforeend; (4) Delete returns 200 empty, row has hx-post to delete, hx-swap outerHTML so row disappears.
   - **Rationale**: Reuses proven pattern; minimal new concepts for templates and front end.

5. **Ordering**
   - **Choice**: Query activities by `activity_date DESC` (newest first). If two activities share the same second, ordering is undefined; created_at can be used as tiebreaker if needed.
   - **Rationale**: Proposal specifies activity_date descending; matches "recent first" expectation.

## Risks / Trade-offs

- **Orphaned activities if FK not CASCADE**: If migration used SET NULL or RESTRICT, contact delete could fail or leave orphans. **Mitigation**: Use ON DELETE CASCADE in migration.
- **Validation errors on create**: If description empty or type invalid, return 200 with fragment that retargets to add-activity form container (same as notes) so errors show in place. **Mitigation**: Document in spec; implement HX-Retarget / HX-Reswap for error response.
- **Large activity lists**: No pagination in this change. **Mitigation**: Accept; add pagination in a future change if needed.

## Migration Plan

- **Deploy**: (1) Add Activity model and Alembic migration creating `activities` table (id, contact_id FK CASCADE, type, description NOT NULL, activity_date NOT NULL, created_at, updated_at). (2) Add routes and templates. (3) Run migration before or with deploy.
- **Rollback**: Revert code; run migration downgrade to drop `activities` table. No data migration from other systems.

## Open Questions

- None.
