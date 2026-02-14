## 1. Add View link to contacts list

- [x] 1.1 In the contacts list template (and list/table fragment used for HTMX, e.g. `_contacts_table.html`), add a "View" link per contact row pointing to `/contacts/{id}` so users can open the contact detail page directly
- [x] 1.2 Ensure the View link appears both on full page load and when the list is refreshed via HTMX (same partial)

## 2. Verification

- [x] 2.1 Verify the contacts list page shows a View link (or equivalent) per contact that navigates to `/contacts/{id}` (detail page with Notes and Activities)
- [x] 2.2 Verify the list fragment returned for HTMX (e.g. search/filter) also includes the View link per row
