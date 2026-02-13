# Show linked Company name in Contacts UI (fallback to legacy text)

## Why

Contacts can have both a legacy free-text `company` field and an optional link to a Company record (`company_id`). The UI currently shows only the legacy text, so users do not see the canonical company name when a contact is linked. Showing the linked company name (with fallback to legacy text) improves consistency and makes it clear when a contact is associated with a company record.

## What Changes

- **Contacts list and detail/edit views**: Where the contact’s company is displayed, show the linked Company’s name when `company_id` is set; otherwise show the legacy `company` text. No change to form fields or persistence.
- **Display logic**: Use a single, consistent “display company” rule everywhere (e.g. linked company name if present, else legacy text). This may be a model property or a small helper used by templates/routes.
- No new routes, form actions, or API changes. No change to search/filter behavior (search can continue to use existing fields as today).

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- **contacts-crud**: Update the requirement that “list company display remains legacy text” so that the contacts list (and any other contact company display) SHALL show the linked Company’s name when `company_id` is set, and SHALL fall back to the legacy `company` text when there is no link or the link is invalid.

## Impact

- **Templates**: Contacts list table and any contact detail/edit view that shows company (e.g. `_contacts_table.html`, edit page) will use the new display rule.
- **Model/route layer**: May add a `display_company` (or equivalent) on the Contact model or expose the same value from routes so templates receive one value to render. No schema or DB migration required.
- **Spec**: `openspec/specs/contacts-crud/spec.md` will receive a delta that replaces or refines the “List company display remains legacy text” scenario with the new “linked name with legacy fallback” behavior.
