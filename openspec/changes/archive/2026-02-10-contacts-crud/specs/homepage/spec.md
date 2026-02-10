## ADDED Requirements

### Requirement: Homepage links to Contacts

The homepage SHALL provide a way for users to discover and navigate to the Contacts feature.

#### Scenario: Link to contacts from homepage
- **WHEN** the user views the homepage
- **THEN** the page SHALL include a link or call-to-action to the Contacts feature
- **AND** the link SHALL target `/contacts` (or the canonical contacts list URL)

#### Scenario: Link in navigation or content
- **WHEN** examining the homepage template or base layout
- **THEN** the Contacts link MAY appear in a navigation area or in the main content (e.g. “View contacts”)
- **AND** the link SHALL be visible when the homepage is rendered
