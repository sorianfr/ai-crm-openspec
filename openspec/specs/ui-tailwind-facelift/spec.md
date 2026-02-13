## Requirements

### Requirement: Tailwind CSS available globally

The application SHALL load Tailwind CSS via a CDN (e.g. Tailwind Play CDN) so that all pages can use Tailwind utility classes without a build step.

#### Scenario: Tailwind loaded in base template
- **WHEN** examining the base template (e.g. `app/templates/base.html`)
- **THEN** the template SHALL include a Tailwind CDN script or link in the head
- **AND** child templates that extend the base SHALL inherit Tailwind availability

#### Scenario: No build step required
- **WHEN** deploying or running the application
- **THEN** Tailwind SHALL be provided via CDN only
- **AND** no npm, node, or Tailwind CLI build SHALL be required for this change

### Requirement: Base layout uses Tailwind

The base template SHALL apply Tailwind classes for the global layout and navigation so the shell looks consistent across all pages.

#### Scenario: Base has styled layout
- **WHEN** any page is rendered that extends the base template
- **THEN** the main content area SHALL be within a layout that uses Tailwind (e.g. constrained width container, padding)
- **AND** the existing content block SHALL remain unchanged in structure (only styling added)

#### Scenario: Navigation uses Tailwind
- **WHEN** the base template is rendered
- **THEN** the navigation (Home, Contacts, Companies) SHALL be styled with Tailwind classes
- **AND** the nav SHALL remain functional (links unchanged)

### Requirement: Shared UI partials exist

The application SHALL provide a minimal shared UI layer under `app/templates/_ui/` with four reusable partials: button, form_field, card, and empty_state.

#### Scenario: Button partial exists
- **WHEN** examining `app/templates/_ui/`
- **THEN** a partial `button.html` SHALL exist
- **AND** it SHALL support at least primary, secondary, and danger styles (e.g. via a style or variant parameter)

#### Scenario: Form field partial exists
- **WHEN** examining `app/templates/_ui/`
- **THEN** a partial `form_field.html` SHALL exist
- **AND** it SHALL support label, input, and optional error block (e.g. via name, id, label, type, value, optional errors)

#### Scenario: Card partial exists
- **WHEN** examining `app/templates/_ui/`
- **THEN** a partial `card.html` SHALL exist
- **AND** it SHALL render a container suitable for list or form sections (e.g. white card with padding/shadow)

#### Scenario: Empty state partial exists
- **WHEN** examining `app/templates/_ui/`
- **THEN** a partial `empty_state.html` SHALL exist
- **AND** it SHALL support a message and optional action (e.g. message, optional action_url and action_label) for empty lists

### Requirement: Contacts and Companies use shared partials

Contacts and Companies templates SHALL use the shared `_ui` partials (button, form_field, card, empty_state) instead of repeating Tailwind classes inline, so that styling stays consistent and future UI changes are easier.

#### Scenario: Contacts list uses shared partials
- **WHEN** examining the contacts list template and related partials (e.g. list, table, search form)
- **THEN** they SHALL use at least one of the shared partials (e.g. card, empty_state, button) where appropriate
- **AND** the contacts list SHALL retain existing behavior (search, filters, HTMX, delete)

#### Scenario: Contacts forms use shared partials
- **WHEN** examining the contacts new and edit templates (and contact-related form partials)
- **THEN** form fields and actions SHALL use the shared partials (e.g. form_field, button) where appropriate
- **AND** form behavior (validation, redirect, HTMX for notes) SHALL remain unchanged

#### Scenario: Companies list uses shared partials
- **WHEN** examining the companies list template
- **THEN** it SHALL use at least one of the shared partials (e.g. card, empty_state, button) where appropriate
- **AND** the companies list SHALL retain existing behavior (links, delete if applicable)

#### Scenario: Companies forms use shared partials
- **WHEN** examining the companies new and edit templates
- **THEN** form fields and actions SHALL use the shared partials (e.g. form_field, button) where appropriate
- **AND** form behavior (validation, redirect) SHALL remain unchanged

### Requirement: Styling only, no behavior change

This capability SHALL affect only presentation (layout, typography, Tailwind classes and shared partials). It SHALL NOT change routes, form actions, HTMX behavior, or validation logic.

#### Scenario: Routes unchanged
- **WHEN** this change is applied
- **THEN** no new routes SHALL be added and no existing route URLs or methods SHALL change
- **AND** response behavior (redirects, status codes, HTML structure for HTMX targets) SHALL remain as before

#### Scenario: Forms and HTMX unchanged
- **WHEN** this change is applied
- **THEN** form action URLs, form method, and HTMX attributes (hx-get, hx-post, hx-target, hx-swap) SHALL remain as before
- **AND** validation and error display behavior SHALL remain as before (only styling of errors may change)
