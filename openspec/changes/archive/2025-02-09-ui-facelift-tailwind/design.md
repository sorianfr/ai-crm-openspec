## Context

The app uses Jinja2 templates with a single base (`base.html`) that includes HTMX and a simple text nav (Home | Contacts | Companies). Contacts and Companies each have list, new, and edit templates plus partials (e.g. contacts: `_contacts_table.html`, `_note_row.html`, `_add_note_form_container.html`). There is no shared UI component layer and no CSS framework; styling is minimal or absent. This change adds Tailwind via CDN and a small set of reusable `_ui` partials so that Contacts and Companies get a consistent facelift without duplicating utility classes or changing behavior.

## Goals / Non-Goals

**Goals:**

- Add Tailwind CSS via CDN to the base template and apply it to base layout (nav, container, spacing).
- Introduce `app/templates/_ui/` with four reusable partials: button (primary/secondary/danger), form_field (label + input + error block), card (container), empty_state (empty lists).
- Refactor Contacts and Companies templates to use these partials and Tailwind so the UI is consistent and maintainable.
- Keep all existing behavior (routes, HTMX, form actions, validation) unchanged.

**Non-Goals:**

- Tailwind build step, PurgeCSS, or custom config; CDN only.
- New pages, routes, or backend logic.
- Changing Jinja2 or HTMX usage patterns beyond swapping markup into shared partials.
- Full design system or component library beyond the four partials.

## Decisions

**1. Tailwind CDN choice**

- Use the **Tailwind Play CDN** (script tag that compiles Tailwind on the fly in the browser) for development and this facelift. It supports all utilities and is sufficient for a small app. Document that for production at scale, a built Tailwind asset would be preferable for performance.
- **Alternative:** Tailwind standalone CLI or npm build — rejected for this change to avoid a build step and keep the proposal scope (CDN-only).
- **Rationale:** Fastest path to a consistent UI; no node/npm required.

**2. Shared partials API**

- **`_ui/button.html`:** Accept at least: `type` (e.g. "submit" or "button"), `style` (e.g. "primary" | "secondary" | "danger"), optional `label`, optional `url` for link-style buttons. Support both `<button>` and `<a>` via a single partial or overloaded params so that "New contact" / "Cancel" links and submit/delete buttons can use the same component. Use Tailwind classes internally (e.g. primary = blue bg, secondary = gray border, danger = red).
- **`_ui/form_field.html`:** Accept: `name`, `id`, `label`, `type` (text, email, etc.), `value`, optional `errors` (list), optional attributes (placeholder, required). Render a wrapper, label, input, and optional error block with consistent spacing and error text styling.
- **`_ui/card.html`:** Accept optional `title`; block or content slot for body. Render a white (or light) container with shadow/border and padding so list and form sections can wrap content in a card.
- **`_ui/empty_state.html`:** Accept: `message`, optional `action_url` and `action_label` (e.g. "Add one" link). Used in contacts/companies list when there are no rows and in any other empty-list case.
- **Rationale:** Minimal surface area; templates pass data, partials own Tailwind class choices so we can change look in one place.

**3. Base template layout**

- Add the Tailwind script in `base.html` `<head>` (Play CDN or similar). Apply a constrained width container (e.g. `max-w-4xl mx-auto`), padding, and a simple nav bar with links (Home, Contacts, Companies) styled as a horizontal bar. No new blocks required; existing `{% block content %}` stays.
- **Rationale:** One place for Tailwind and global layout; all child templates inherit.

**4. Order of implementation**

- (1) Add Tailwind to base and style base/nav. (2) Create the four `_ui` partials with Tailwind classes. (3) Refactor Contacts templates (list, new, edit, and partials like `_contacts_table.html`) to use `_ui` and Tailwind. (4) Refactor Companies templates similarly. (5) Smoke-check that all pages render and HTMX still works.
- **Rationale:** Base and shared layer first so Contacts/Companies refactors have stable building blocks.

**5. Contacts/Companies usage of _ui**

- List pages: use `_ui/card.html` for the main content area, `_ui/empty_state.html` for the "no contacts/companies yet" branch, `_ui/button.html` for "New contact", "Apply filters", "Clear", delete buttons, etc. Table or list markup can stay in place with Tailwind table/list classes; optional wrapper in card.
- New/Edit forms: use `_ui/form_field.html` for each field; use `_ui/button.html` for submit and cancel. Wrap form in `_ui/card.html` if desired.
- Partials (e.g. note row, add-note form): use `_ui/button.html` for delete/add where it fits; form_field for the note content input. Avoid duplicating long Tailwind strings.
- **Rationale:** Proposal says templates SHOULD use these partials; design commits to that so we get consistency and one place to tweak styles.

## Risks / Trade-offs

- **CDN and production:** Play CDN compiles on the client and is not ideal for large production payloads. Mitigation: Document that; for this change, CDN is acceptable. Future change could add a build step if needed.
- **Partial API drift:** If we add many optional params to button or form_field, partials become complex. Mitigation: Keep params minimal; use sensible defaults and optional blocks/slots only where necessary.
- **Existing partials (e.g. _contacts_table.html):** Refactoring them to use _ui may touch many lines. Mitigation: Do it incrementally; prefer wrapping with card/empty_state and swapping buttons first, then form fields in forms.

## Migration Plan

- No database or config migration. Deploy by updating templates and adding `_ui` partials; ensure Tailwind script is in base. Rollback: revert template and `_ui` changes. No feature flags required.

## Open Questions

- None. Optional follow-up: add a second "slot" or block to `_ui/card.html` for card footer (e.g. button row) if needed; start with single body content only.
