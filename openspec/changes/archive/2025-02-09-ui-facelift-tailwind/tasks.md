## 1. Tailwind and base layout

- [x] 1.1 Add Tailwind Play CDN script to base template head (e.g. app/templates/base.html)
- [x] 1.2 Apply Tailwind to base: constrained container (e.g. max-w-4xl mx-auto), padding, and styled nav bar (Home, Contacts, Companies) with Tailwind classes
- [x] 1.3 Ensure block content remains unchanged in structure; only wrap/style with Tailwind

## 2. Shared UI partials

- [x] 2.1 Create app/templates/_ui/button.html with primary, secondary, and danger styles (support button and link usage via type/url/label params)
- [x] 2.2 Create app/templates/_ui/form_field.html with label, input, optional errors (name, id, label, type, value, optional errors)
- [x] 2.3 Create app/templates/_ui/card.html with optional title and body content (white card container with padding/shadow)
- [x] 2.4 Create app/templates/_ui/empty_state.html with message and optional action_url/action_label

## 3. Contacts templates refactor

- [x] 3.1 Refactor contacts list (list.html, _contacts_table.html): use _ui card, empty_state, and button where appropriate; keep search/filters and HTMX behavior
- [x] 3.2 Refactor contacts new and edit forms: use _ui form_field and button; wrap in card if desired; preserve validation and redirect behavior
- [x] 3.3 Refactor contact-related partials (e.g. _note_row, _add_note_form_container): use _ui button and form_field where appropriate; preserve HTMX

## 4. Companies templates refactor

- [x] 4.1 Refactor companies list: use _ui card, empty_state, and button where appropriate; preserve list and delete behavior
- [x] 4.2 Refactor companies new and edit forms: use _ui form_field and button; wrap in card if desired; preserve validation and redirect behavior

## 5. Verification

- [x] 5.1 Verify all pages render (home, contacts list/new/edit, companies list/new/edit) with Tailwind and no broken layout
- [x] 5.2 Verify Contacts: search/filters, HTMX list update, create/edit/delete, notes add/delete still work
- [x] 5.3 Verify Companies: create/edit/delete still work; no route or form action changes
