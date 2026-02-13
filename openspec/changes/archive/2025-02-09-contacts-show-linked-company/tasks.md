## 1. Display company on Contact model

- [x] 1.1 Add a hybrid property `display_company` on the Contact model that returns the linked Company's name when `company_ref` is present and has a name, otherwise returns the legacy `company` text (or empty string)

## 2. Eager-load company_ref

- [x] 2.1 In the contacts list route (GET `/contacts`), eager-load `Contact.company_ref` when querying contacts (e.g. using `selectinload(Contact.company_ref)`) so `display_company` does not cause N+1 queries
- [x] 2.2 When loading a single contact for the edit page (GET `/contacts/{id}/edit`), eager-load `company_ref` so `display_company` is available without extra queries

## 3. Use display_company in templates

- [x] 3.1 In `app/templates/contacts/_contacts_table.html`, replace the company cell to use `contact.display_company` (or equivalent) instead of `contact.company`, so the list shows linked company name with legacy fallback

## 4. Verification

- [x] 4.1 Verify contacts list shows the linked Company name when a contact has `company_id` set and the company exists
- [x] 4.2 Verify contacts list shows legacy `company` text when a contact has no `company_id` or the linked company does not exist
