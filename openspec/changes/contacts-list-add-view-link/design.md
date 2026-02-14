# Design: View link on contacts list

## Context

The contacts list is rendered by the list page and, when using HTMX (e.g. search/filters), by a list/table fragment. The contact detail page exists at GET `/contacts/{id}`. The list currently does not link to it; this change adds a direct View link per contact row.

**Current state:** List template(s) show contact rows; any existing link may point to edit. No link to `/contacts/{id}` today.

**Constraints:** Template-only; no new routes or backend logic.

## Goals / Non-Goals

**Goals:** Add a "View" (or equivalent) link on each contact row that goes to `/contacts/{id}` so users can open the detail page (Notes and Activities) without going through Edit.

**Non-Goals:** Changing list route behavior, search, or filters; changing the detail or edit pages.

## Decisions

### Where to add the link

**Decision:** Add the View link in the same template(s) that render each contact row—i.e. the full list page and the HTMX list/table fragment (e.g. `_contacts_table.html` or equivalent) so both initial load and HTMX-refreshed list show the link.

**Rationale:** Any partial used to render the list must include the link so behavior is consistent.

### View vs Edit

**Decision:** Add "View" as a separate link; keep "Edit" if present. Label "View" (or "View contact") and target `/contacts/{id}`.

**Rationale:** Proposal allows view and/or edit; offering both gives clear intent (view = detail, edit = form).

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Row gets busy with many links | Use a single View link; keep Edit/Delete as today. Acceptable. |

## Migration Plan

Single deploy; template change only. No rollback data steps.

## Open Questions

None.
