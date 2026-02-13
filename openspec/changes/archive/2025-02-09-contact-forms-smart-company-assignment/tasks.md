## 1. Resolve-or-create company helper

- [x] 1.1 Add a helper (e.g. `_resolve_or_create_company(db, name: str)`) that trims and normalizes name; finds an existing Company by name (case-insensitive); if found returns (Company, None); if not found creates a new Company with that name and returns (Company, None); returns (None, error_message) only on validation failure (e.g. empty after trim)

## 2. Create contact – smart company assignment

- [x] 2.1 In POST `/contacts`, when company text is non-empty (after strip), ignore `company_id` and call the resolve-or-create helper; set the new contact's `company_id` and `company` from the result
- [x] 2.2 In POST `/contacts`, when company text is empty, use existing `_resolve_company_id` for `company_id` and set `company` from selected company name when a company is selected; validate `company_id` only when company text is empty

## 3. Update contact – smart company assignment

- [x] 3.1 In POST `/contacts/{id}`, when company text is non-empty (after strip), ignore `company_id` and call the resolve-or-create helper; set the contact's `company_id` and `company` from the result
- [x] 3.2 In POST `/contacts/{id}`, when company text is empty, use existing `_resolve_company_id` for `company_id` and set `company` from selected company name when a company is selected; validate `company_id` only when company text is empty

## 4. UI – disable dropdown when company text has content

- [x] 4.1 In contact new and edit templates, server-render the company_id select with `disabled` when `form_company` (or equivalent) is non-empty so the dropdown is disabled on initial load and after validation re-renders
- [x] 4.2 Optionally add a small inline script so the company_id dropdown is disabled when the company text input has content (as the user types), and enabled when the text field is cleared

## 5. Verification

- [x] 5.1 Verify create contact with non-empty company text: new company name creates a Company and links contact; existing company name (case-insensitive) links contact without creating duplicate
- [x] 5.2 Verify create/update with empty company text: dropdown selection links contact; blank dropdown sets company_id to NULL; invalid company_id when text empty returns validation error
- [x] 5.3 Verify dropdown is disabled when company text field has content (on load and after typing) and enabled when empty
