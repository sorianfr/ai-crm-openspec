## Why

The Contacts and Companies pages are functional but visually minimal. Adding Tailwind CSS via CDN gives a quick, dependency-light way to improve layout, typography, and consistency across these areas without introducing a build step or changing the server-rendered + HTMX approach.

## What Changes

- **Tailwind CSS via CDN:** Include the Tailwind Play CDN (or official CDN) in the base template so all pages can use utility classes.
- **Minimal shared UI layer:** Introduce a small set of reusable partials under `app/templates/_ui/` to ensure consistency and avoid repeating Tailwind classes inline:
  - `_ui/button.html` — primary / secondary / danger styles
  - `_ui/form_field.html` — label + input + optional error block pattern
  - `_ui/card.html` — white card container used for list/form sections
  - `_ui/empty_state.html` — used when lists are empty
- **Contacts and Companies** templates SHOULD use these partials instead of repeating Tailwind classes everywhere; this keeps Tailwind usage consistent and prepares the project for future UI changes.
- **Base layout:** Apply Tailwind to the existing base template (e.g. nav, container, spacing) so the shell looks polished and consistent.
- **Contacts UI:** Apply Tailwind via the shared partials and targeted classes to the contacts list (search/filters, table), new/edit forms, and contact-related partials.
- **Companies UI:** Apply Tailwind via the shared partials to the companies list and new/edit forms so they match the contacts styling.
- **Scope:** Styling and layout only; no behavior changes to routes, HTMX, or forms. Existing functionality (search, filters, CRUD, delete) remains unchanged.

## Capabilities

### New Capabilities

- `ui-tailwind-facelift`: Styling and layout for the app using Tailwind CSS (CDN). A minimal shared UI layer under `app/templates/_ui/` provides reusable partials: button (primary/secondary/danger), form_field (label+input+error), card (container), empty_state (empty lists). Base template and global nav use Tailwind; Contacts and Companies pages use the shared partials and Tailwind for a consistent UI. No new routes or backend logic.

### Modified Capabilities

- None. This is a presentation-only change; existing specs (contacts-crud, companies-crud, contacts-search-filters, etc.) do not change in behavior. If desired, `jinja2-templating` could note that the project uses Tailwind for styling—optional and left empty unless we want an explicit spec delta.

## Impact

- **Templates:** `base.html` gains Tailwind script/link. New shared partials under `app/templates/_ui/`: `button.html`, `form_field.html`, `card.html`, `empty_state.html`. Contacts and Companies templates are updated to use these partials and Tailwind; existing `contacts/*.html` and `companies/*.html` (and related partials) are refactored to use `_ui` where appropriate.
- **Assets:** Tailwind loaded from CDN; no new npm/node or build pipeline.
- **Dependencies:** None in Python; front-end only (Tailwind CDN).
- **Existing behavior:** Unchanged; only visual presentation and layout improve.
