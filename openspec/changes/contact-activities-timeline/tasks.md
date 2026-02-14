## 1. Activity model and migration

- [x] 1.1 Add Activity model in app/models/ with id, contact_id (FK to contacts.id, ON DELETE CASCADE), type (String, e.g. call/email/meeting/task), description (required text), activity_date (DateTime), created_at, updated_at; add relationship on Contact to activities
- [x] 1.2 Create Alembic migration that creates the activities table with the above columns and FK with ON DELETE CASCADE

## 2. Activity schema and routes

- [x] 2.1 Add Pydantic schema for activity form (type, description required, activity_date); validate type is one of call, email, meeting, task
- [x] 2.2 Add POST `/contacts/{contact_id}/activities`: validate form, create activity, return activity-row HTML fragment (200); on validation error return fragment that retargets to add-activity-form-container with HX-Retarget/HX-Reswap; 404 if contact not found
- [x] 2.3 Add POST `/activities/{activity_id}/delete`: delete activity, return 200 empty body; 404 if activity not found

## 3. Contact edit page – load and display activities

- [x] 3.1 In GET `/contacts/{id}/edit`, load activities for the contact ordered by activity_date DESC and pass them to the edit template
- [x] 3.2 Add Activities section below Notes on the contact edit template: list container (e.g. id="contact-activities-list"), activity rows (id="activity-{id}"), add-activity form container (id="add-activity-form-container")
- [x] 3.3 Create partials: activity row template (type, description, activity_date, delete button with hx-post to `/activities/{id}/delete`, hx-target self, hx-swap outerHTML) and add-activity form (type select/dropdown, description textarea, activity_date input, hx-post to `/contacts/{id}/activities`, hx-target contact-activities-list, hx-swap beforeend)

## 4. Verification

- [x] 4.1 Verify activities table exists after migration and Activity model matches spec
- [x] 4.2 Verify contact edit page shows Activities section with list (ordered by activity_date DESC), add form, and delete per row; create appends row via HTMX; delete removes row via HTMX
- [x] 4.3 Verify validation: empty description returns form with errors in add-activity-form-container; invalid type rejected; 404 for missing contact or activity
