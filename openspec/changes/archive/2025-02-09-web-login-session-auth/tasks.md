## 1. Configuration and session middleware

- [x] 1.1 Add config: SESSION_SECRET (required), SESSION_MAX_AGE (optional), APP_ENV-based Secure flag for cookies
- [x] 1.2 Add SessionMiddleware in app/main.py with SESSION_SECRET, max_age, and cookie settings (HttpOnly, SameSite=lax, Secure in prod)

## 2. Web auth helpers

- [x] 2.1 Implement get_current_web_user: resolve User from session user_id via DB; redirect to /login if missing/invalid; clear session if user not found
- [x] 2.2 Implement require_web_roles(allowed_roles): return 403 for forbidden; for HTMX requests return status 403 (no redirect)

## 3. CSRF protection

- [x] 3.1 Implement CSRF helpers: generate token (per session), validate token; store in session["csrf_token"]
- [x] 3.2 Integrate CSRF in templates: add base macro/helper to include csrf_token hidden field in forms

## 4. Login and logout routes

- [x] 4.1 Add GET /login (render login form) and POST /login (validate credentials, set session user_id, rotate CSRF, redirect to /)
- [x] 4.2 Add POST /logout (clear session, redirect to /login)
- [x] 4.3 Create login.html template with email/password form

## 5. Update web routes

- [x] 5.1 Update contacts web routes to use get_current_web_user, require_web_roles (create: admin/manager), and CSRF validation on mutations
- [x] 5.2 Update companies web routes to use session auth and CSRF on mutations
- [x] 5.3 Update contact-notes web routes (create note, delete note) to use session auth and CSRF
- [x] 5.4 Update contact-activities web routes (create activity, delete activity) to use session auth and CSRF
- [x] 5.5 Keep JWT API routes (/auth/login, /users, etc.) unchanged

## 6. Verification

- [x] 6.1 Browser: visiting /contacts without session redirects to /login
- [x] 6.2 Login with known user (admin_tenant_a@test.local / test) allows browsing /contacts
- [x] 6.3 Create contact from UI works when logged in with admin/manager
- [x] 6.4 POST without valid CSRF token returns 403 (e.g. curl without csrf field)
- [x] 6.5 Logout clears session and redirects to /login
