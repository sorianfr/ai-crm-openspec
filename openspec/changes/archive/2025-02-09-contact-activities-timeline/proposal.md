# Contact activity timeline (interactions)

## Why

The CRM currently supports contacts, companies, notes, and search.
However, it lacks a structured way to track interactions with contacts such as calls, emails, meetings, and tasks.

A timeline of activities is a core CRM feature because it answers:
- When did we last talk to this contact?
- What happened recently?
- What follow-ups exist?

Activities complement notes:
- Notes = free text knowledge
- Activities = structured events over time

This change introduces an **Activity timeline per contact** shown on the contact edit page.

---

## What Changes

### New Activity model

Add an Activity entity linked to Contact.

Fields:
- id
- contact_id (FK → contacts.id)
- type (call, email, meeting, task)
- description (required text)
- activity_date (date or datetime of the interaction)
- created_at
- updated_at

Activities are ordered by **activity_date descending**.

---

### Activities on contact edit page

The contact edit page SHALL gain a new **Activities section** below Notes.

Users SHALL be able to:
- View activities in a timeline/list
- Add a new activity inline (HTMX)
- Delete an activity inline (HTMX)

No separate activities page is introduced in this change.

---

### Routes

Add two routes:

- POST `/contacts/{contact_id}/activities`
  - Create activity via HTMX
- POST `/activities/{activity_id}/delete`
  - Delete activity via HTMX row removal

This mirrors the Notes pattern for consistency.

---

### UI behavior

On the contact edit page:

Activities section includes:
- List of activities (ordered by activity_date DESC)
- Inline "Add activity" form
- Delete button per activity

HTMX behavior:
- Create returns row fragment → appended to list
- Delete returns 200 empty → row removed via `hx-swap="outerHTML"`

---

## Capabilities

### New Capabilities

- **contact-activities**: Activity model and table; Activity timeline on contact edit page; Create and delete via HTMX; Ordered by activity_date descending.

### Modified Capabilities

- **contacts-crud**: Contact edit page SHALL display an Activities section; no changes to routes or existing contact behavior.

---

## Impact

### Backend
- New Activity model
- Alembic migration for activities table
- Two POST routes for create/delete

### Templates
- Contact edit template updated
- New partials for activity row and add form

### Dependencies
None new. Uses existing FastAPI + SQLAlchemy + Jinja2 + HTMX stack.
