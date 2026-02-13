# Design: Smart Company assignment on Contact forms

## Context

- **Current state**: Contact create and update forms submit both `company` (free text) and `company_id` (dropdown). The backend persists both; `_resolve_company_id` validates `company_id` when present. There is no resolve-by-name or auto-create; company text is legacy only.
- **Constraint**: Company text is the primary source of truth. When text is non-empty, dropdown is ignored server-side and the dropdown is disabled in the UI. When text is empty, dropdown is used as today.
- **Stakeholders**: Users creating or editing contacts who want to type a company name and have it link or create a Company without leaving the form.

## Goals / Non-Goals

**Goals:**
- When company text is non-empty: resolve by name (case-insensitive, trimmed); link to existing Company or create one and link; ignore dropdown; UI disables dropdown when text has content.
- When company text is empty: use dropdown selection for `company_id` as today; optionally set `company` from selected company name.
- Same behavior on create and update contact routes. No new routes or form actions.

**Non-Goals:**
- Changing Companies list or company CRUD. No deduplication of existing companies. No sync of legacy-only contacts in bulk.

## Decisions

1. **Where to implement resolve-or-create**
   - **Choice**: Single helper (e.g. `_resolve_or_create_company(db, name: str) -> tuple[Company | None, str | None]`) used by both create_contact and update_contact. Returns (Company, None) on success, (None, error_message) on validation failure. Caller sets `contact.company_id` and `contact.company` from the result when company text was non-empty.
   - **Rationale**: Keeps create/update logic DRY and testable. No new service layer required.

2. **Name matching and normalization**
   - **Choice**: Trim whitespace; match existing company by name using case-insensitive comparison (e.g. `Company.name.ilike(normalized)` or one-by-one after load). "Exists" means one existing row; if multiple exist (legacy data), link to the first match.
   - **Rationale**: Avoids duplicate creates for "Acme" vs "acme". Trimming avoids creating companies that are only spaces.

3. **When to create a new Company**
   - **Choice**: Only when company text is non-empty after trim and no existing company matches (case-insensitive). Create with `Company(name=normalized_name)` then link contact.
   - **Rationale**: Matches proposal: "if not exists → create company and link it."

4. **Dropdown disabled in UI**
   - **Choice**: Disable the "Existing company" dropdown when the company text field has content. Implement via a small amount of inline script (e.g. on input/change of company text, set `company_id` select disabled when value length > 0) so it works without a build step. Alternatively server-render `disabled` when `form_company` is non-empty so initial load and re-renders after validation are correct; then optional JS to disable as user types.
   - **Rationale**: Proposal requires dropdown MUST be disabled when text has content. Server-rendered disabled when form_company is set covers validation re-renders; JS improves UX when user types without submitting.

5. **Empty company text and dropdown**
   - **Choice**: When company text is empty (or only whitespace), do not run resolve-or-create; use existing `_resolve_company_id(db, company_id)` and set `contact.company_id` and optionally `contact.company = selected_company.name` for display consistency.
   - **Rationale**: Preserves current behavior when user only uses dropdown; no create in that path.

## Risks / Trade-offs

- **Duplicate company names (legacy)**: If two companies exist with the same name (e.g. different casing stored), resolve-by-name may pick the first. **Mitigation**: Match case-insensitively and link to first; accept that duplicate names are a data-quality issue; no scope for dedupe in this change.
- **Race condition**: Two submissions with same new company name could create two companies. **Mitigation**: Accept for now; optional follow-up could use unique constraint on normalized name or "get or create" with lock.
- **Dropdown and JS**: If JS is disabled, dropdown might remain enabled while user types; server still ignores dropdown when text is non-empty. **Mitigation**: Server is source of truth; UX is best-effort when JS runs.

## Migration Plan

- **Deploy**: Code and template changes only. No DB migration (Company model unchanged; contact form behavior only).
- **Rollback**: Revert contact route and template changes; restore previous create/update logic and remove dropdown disable.

## Open Questions

- None.
