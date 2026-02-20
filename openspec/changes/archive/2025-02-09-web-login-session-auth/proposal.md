## Why

The CRM currently relies on JWT (Bearer tokens) for API access, but the HTML web UI (Jinja2/HTMX) has no first-class authentication flow. Users must be able to log in through a web form and use the application via secure cookie-based sessions, while preserving multi-tenant isolation and RBAC.

## What Changes

- Add web authentication routes:
  - `GET /login` (HTML login page)
  - `POST /login` (validate credentials, set session cookie, redirect)
  - `POST /logout` (clear session, redirect)
- Add session-based authentication for web UI routes:
  - Redirect unauthenticated users to `/login`
  - Resolve `current_user` from session `user_id` via DB lookup
- Enforce RBAC on web routes (e.g. contact creation allowed only for admin/manager)
- Add CSRF protection for cookie-authenticated POST requests (forms and HTMX)
- Keep existing JWT-based `/auth/login` and API endpoints unchanged
- Preserve multi-tenant scoping (tenant_id derived from DB user record)

## Capabilities

### New Capabilities

- `web-session-auth`: Cookie-based login/logout, session-based current_user resolution, redirect behavior for unauthenticated access
- `csrf-protection`: CSRF token stored in session, embedded in HTML forms, validated on POST/PUT/PATCH/DELETE web routes

### Modified Capabilities

- `contacts-crud`: Web routes require session authentication; preserve multi-tenant and RBAC enforcement
- `companies-crud`: Web routes require session authentication
- `contact-notes`: Web routes require session authentication
- `contact-activities`: Web routes require session authentication

## Impact

- New login/logout templates
- Middleware or dependency for session-based auth
- Updates to existing web routes to enforce session auth
- CSRF token handling in templates and route handlers
- No changes to public JWT API endpoints
