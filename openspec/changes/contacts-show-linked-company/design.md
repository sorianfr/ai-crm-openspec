# Design: Show linked Company name in Contacts UI

## Context

- **Current state**: Contact has `company` (legacy free text) and `company_id` (optional FK to Company). The relationship `company_ref` is already defined. Templates (contacts list, edit page) currently render `contact.company` only.
- **Constraint**: No DB migration, no route/URL changes, no form or persistence changes. Display-only.
- **Stakeholders**: Users viewing the contacts list or contact edit page who expect to see the canonical company name when a contact is linked.

## Goals / Non-Goals

**Goals:**
- Where the contact’s company is shown (list, edit/detail), display the linked Company’s name when `company_id` is set; otherwise display the legacy `company` text.
- Use one consistent rule so future UI additions don’t diverge.

**Non-Goals:**
- Changing search/filter behavior (continue using existing fields).
- Changing forms, validation, or persistence.
- Syncing or reconciling legacy `company` text with the linked Company name.

## Decisions

1. **Where to implement “display company”**
   - **Choice**: Add a **hybrid property** on the Contact model (e.g. `display_company`) that returns `company_ref.name` when `company_ref` is present and non-empty, else `company` (or empty string).
   - **Rationale**: Single place for the rule; templates and routes stay simple. No new route logic. Reusable for any future UI that shows company.
   - **Alternative**: Compute in the template (e.g. `contact.company_ref.name if contact.company_ref else contact.company`). Rejected to avoid repeating the rule and to keep templates simpler.

2. **Eager loading for the list**
   - **Choice**: When loading contacts for the list (and for edit), ensure `company_ref` is **eager-loaded** (e.g. `selectinload(Contact.company_ref)` or equivalent) so accessing `display_company` does not cause N+1 queries.
   - **Rationale**: List page renders many contacts; lazy-loading `company_ref` per row would be inefficient.

3. **Fallback when link is broken**
   - **Choice**: If `company_id` is set but `company_ref` is missing (e.g. company was deleted, SET NULL not yet applied, or load without relationship), fall back to legacy `company` text.
   - **Rationale**: Matches “fallback to legacy text” and avoids showing nothing or an error.

## Risks / Trade-offs

- **Stale legacy text**: When a contact is linked, we show the Company name; the legacy `company` field may still hold old text. We do not auto-clear or sync it. **Mitigation**: Accept as known; future change could add sync or UX to “copy company name to legacy” if desired.
- **N+1 if eager load missed**: If a new view shows contacts without eager-loading `company_ref`, each `display_company` access may hit the DB. **Mitigation**: Document that list and edit queries must load `company_ref`; consider a single helper that returns contacts “for list” with relationship loaded.

## Migration Plan

- **Deploy**: Code change only (model property + template updates + eager load in contacts list/edit queries). No migration, no config.
- **Rollback**: Revert the commit; templates go back to `contact.company` only.

## Open Questions

- None for this change.
