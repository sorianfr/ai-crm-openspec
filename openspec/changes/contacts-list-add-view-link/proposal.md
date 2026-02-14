# Contacts list: add View link to contact detail page

## Why

The contact detail page (GET `/contacts/{id}`) shows a contact's summary, Notes, and Activities. Today, the contacts list does not link directly to that view; users who want to see Notes and Activities must open the Edit page first. Adding a direct View link from the list to the contact detail page lets users go straight to viewing and managing Notes and Activities without going through Edit.

## What Changes

- On the contacts list page (GET `/contacts`), each contact row SHALL include a "View" link (or equivalent) that targets the contact detail page `/contacts/{id}`.
- Optional: the existing "Edit" link, if present, may remain; the list SHALL offer at least one way to open the contact (view and/or edit) so users can reach the detail page directly.

No new routes or backend behavior; template-only change to the contacts list (and any list fragment used for HTMX refresh).

## Capabilities

### New Capabilities

- None

### Modified Capabilities

- **contacts-crud**: Contacts list route — the list page (and list fragment) SHALL include a direct link to the contact detail page (e.g. "View" or "View contact") pointing to `/contacts/{id}` so users can access the detail page (Notes and Activities) without going through Edit.

## Impact

- **Templates:** Update the contacts list template (and list/table partial if used for HTMX) to add a View link per contact row pointing to `/contacts/{id}`.
- **Routes / backend:** No change.
- **APIs:** No change.
