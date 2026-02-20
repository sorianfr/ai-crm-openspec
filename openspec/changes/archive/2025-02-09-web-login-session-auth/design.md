# Design — web-login-session-auth

## Context

The CRM is a FastAPI app with a Jinja2/HTMX web UI and JWT-based API authentication. Web routes (contacts, companies, notes, activities) currently depend on `get_current_user`, which requires a Bearer token. There is no web login flow—users cannot log in via the browser. Multi-tenant isolation and RBAC are already enforced; `current_user` is resolved from the DB and carries `tenant_id` and `role`. This change adds cookie-based sessions for the web UI while keeping JWT for API use.

## Goals / Non-Goals

**Goals:**

- First-class web login/logout so users can access the UI without manual token handling
- Session-based authentication for HTML routes; redirect unauthenticated users to `/login`
- CSRF protection for cookie-authenticated mutations
- Preserve multi-tenant scoping and RBAC (user resolved from DB)
- Keep JWT `/auth/login` and API endpoints unchanged

**Non-Goals:**

- Replacing JWT with cookies for API endpoints
- OAuth/OIDC
- Full user admin UI

## Decisions

### Session mechanism

- **Decision:** Use Starlette `SessionMiddleware` with a strong secret from environment (e.g. `SESSION_SECRET`)
- **Decision:** Store only `user_id` in session; never store `role` or `tenant_id`—always resolve user from DB (source of truth)
- **Decision:** Cookie settings:
  - `HttpOnly = True`
  - `SameSite = "lax"`
  - `Secure = True` in production, `False` in development
  - Reasonable `max_age` (e.g. 8–12 hours)
- **Rationale:** Minimal session state reduces exposure; DB is authoritative for role/tenant changes.

### Dependencies: get_current_web_user and require_web_roles

- **Decision:** Implement `get_current_web_user`:
  - If session has no `user_id` → redirect to `/login`
  - If user not found in DB → clear session and redirect to `/login`
  - Returns `User` object (with `tenant_id`, `role` from DB)
- **Decision:** Implement `require_web_roles(allowed_roles)`:
  - If role not allowed: normal requests → 403 page; HTMX requests → 403 status
- **Rationale:** Parallel to existing JWT `get_current_user` / `require_roles`; web paths use their own dependency to avoid mixing Bearer and cookie auth.

### Login flow

- **Decision:**
  - `GET /login` renders login template
  - `POST /login`: validate email/password with existing password hashing; on success set `session["user_id"] = user.id`, generate new CSRF token, redirect to `/`; on failure re-render login page with generic error (no user enumeration)
  - `POST /logout`: clear session, redirect to `/login`
- **Rationale:** Simple, secure flow; failure messages avoid enumeration.

### CSRF protection

- **Decision:** Generate random CSRF token per session, store in `session["csrf_token"]`
- **Decision:** Embed `csrf_token` in all HTML forms as hidden input
- **Decision:** For HTMX: rely on hidden input submission (recommended); optionally support `X-CSRF-Token` header
- **Decision:** Validate CSRF token on all cookie-authenticated POST/PUT/PATCH/DELETE web routes; on failure return 403
- **Rationale:** Required for cookie-based auth; hidden input covers forms and HTMX.

### Multi-tenant integration

- **Decision:** No changes to tenant scoping logic; `current_user` from DB already includes `tenant_id`
- **Decision:** JWT API endpoints unchanged
- **Rationale:** Session auth and JWT share the same user model; tenant enforcement remains DB-based.

### Route updates

- **Decision:** All HTML routes (`/contacts`, `/companies`, notes, activities) must depend on `get_current_web_user`, validate CSRF on mutations, and enforce `require_web_roles` where appropriate
- **Decision:** Web login uses `/login`; JWT login remains at `/auth/login`
- **Rationale:** Clear separation between web and API auth.

### Template changes

- **Decision:** Add `login.html` template
- **Decision:** Update base template: show logout button when authenticated; include `csrf_token` hidden field in forms
- **Rationale:** Consistent UI and CSRF coverage across forms.

## Risks / Trade-offs

- **[Session fixation]** → Regenerate session on login (Starlette session backend handles this when session data changes)
- **[CSRF bypass via GET]** → CSRF validation only on state-changing methods (POST/PUT/PATCH/DELETE); GET remains safe
- **[Cookie theft]** → HttpOnly, Secure (in prod), SameSite=lax mitigate XSS and some CSRF; keep session lifetime bounded

## Migration Plan

- Add `SessionMiddleware` and `SESSION_SECRET` config
- Introduce `get_current_web_user` and `require_web_roles`; wire into existing web routes
- Add CSRF generation/validation; update forms and mutation handlers
- No data migration; no breaking changes to JWT API
