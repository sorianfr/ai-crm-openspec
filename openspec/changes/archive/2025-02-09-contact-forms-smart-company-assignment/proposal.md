# Smart Company assignment on Contact forms (auto-create + lock dropdown)

## Why

Contact forms today have a free-text company field and a separate "Existing company" dropdown. Users must either pick an existing company or type text that is only stored as legacy text and does not create or link to a Company. That leads to duplicate or inconsistent company data and extra steps when the company is new. Smart assignment should let users type a name and have it auto-create or link a Company when appropriate, with the company text field as the primary source of truth and the dropdown disabled when text has content.

## What Changes

- **Source of truth**: The company **text** field is the primary source of truth. Server-side logic and UI behavior SHALL follow from that.
- **When company text is NOT empty**:
  - Ignore the dropdown value server-side.
  - Find a company by name (case-insensitive match).
  - If a company exists with that name → link the contact to it (`company_id` + set `company` text to that name).
  - If no company exists → create a new Company with that name and link the contact to it.
  - The dropdown MUST be disabled in the UI when the company text field has content.
- **When company text IS empty**:
  - The user MAY select a company from the dropdown.
  - The selected `company_id` is used normally (contact is linked to that company; `company` text may be set from the selected company’s name for consistency).
- **Unified behavior on new and edit**: The same rules SHALL apply on both create and update contact forms.
- No new routes or APIs; form action URLs and methods remain. No change to Companies list or company CRUD.

## Capabilities

### New Capabilities

- None.

### Modified Capabilities

- **contacts-crud**: Add/update requirements for contact create and update so that (1) when company text is non-empty, the dropdown value is ignored and the system SHALL resolve by name (case-insensitive): link to existing company or create a new one and link; (2) when company text is empty, the dropdown selection SHALL be used normally for `company_id`; (3) the UI SHALL disable the company dropdown when the company text field has content.

## Impact

- **Backend**: Contact create/update handlers will treat company text as primary: when non-empty, resolve by name (case-insensitive) or create Company and set `company_id` and `company`; when empty, use dropdown `company_id` as today.
- **Templates**: Contact new/edit forms SHALL disable the "Existing company" dropdown when the company text field has content (e.g. via client-side or server-rendered disabled state).
- **Companies**: New companies may be created implicitly from contact forms when the user types a new company name; no change to company list or company CRUD routes.
