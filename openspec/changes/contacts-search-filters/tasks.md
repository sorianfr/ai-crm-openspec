## 1. Contacts query and route behavior

- [x] 1.1 Extend GET `/contacts` handler to accept query params `q` (string), `has_email` (bool), and `has_phone` (bool)
- [x] 1.2 Implement search filtering for non-empty `q` across `full_name`, `email`, and `company`
- [x] 1.3 Implement boolean filters: `has_email=true` => non-empty email, `has_phone=true` => non-empty phone
- [x] 1.4 Preserve ordering by `updated_at` descending after applying search and filters
- [x] 1.5 Pass current query state (`q`, `has_email`, `has_phone`) to template context for UI state persistence

## 2. HTMX full-page vs fragment response

- [x] 2.1 Add HX-Request detection in GET `/contacts` and return fragment-only response when header is present
- [x] 2.2 Keep non-HTMX GET `/contacts` returning full `contacts/list.html` page
- [x] 2.3 Ensure fragment response is suitable for swap into `#contacts-results`

## 3. Contacts list templates refactor

- [x] 3.1 Create `app/templates/contacts/_contacts_table.html` partial with the contacts table/list markup
- [x] 3.2 Update `app/templates/contacts/list.html` to include a stable container `id="contacts-results"` that renders the new partial
- [x] 3.3 Keep existing contact row structure and HTMX delete behavior functional after moving table markup to the partial

## 4. Search and filter UI controls

- [x] 4.1 Add a search/filter form to `contacts/list.html` with controls for `q`, `has_email`, and `has_phone`
- [x] 4.2 Configure the form for HTMX GET to `/contacts` targeting `#contacts-results`
- [x] 4.3 Preserve entered/checked values on full-page render and after HTMX updates

## 5. Verification

- [x] 5.1 Verify full-page GET `/contacts` renders search/filter controls and results container
- [x] 5.2 Verify HTMX GET `/contacts` returns only the table fragment and swaps into `#contacts-results`
- [x] 5.3 Verify filtering scenarios (`q`, `has_email`, `has_phone`, combined) and ordering by `updated_at` desc
- [x] 5.4 Verify existing list delete action still removes rows correctly after template refactor
