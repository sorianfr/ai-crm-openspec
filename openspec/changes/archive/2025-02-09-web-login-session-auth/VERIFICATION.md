# Web login session auth – verification

## Prerequisites

- Migrations applied, dev seed run (or verification tenants: `python3 scripts/seed_verification_tenants.py`)
- App running: `uvicorn app.main:app --reload`

## Verification steps

### 1. Unauthenticated redirect

- Visit `http://localhost:8000/contacts` without a session.
- **Expected:** Redirect to `/login`.

### 2. Login and browse

- Go to `http://localhost:8000/login`.
- Login with `admin_tenant_a@test.local` / `test`.
- **Expected:** Redirect to `/`.
- Visit `/contacts`, `/companies`.
- **Expected:** Data loads; logout button in nav.

### 3. Create contact (RBAC)

- As admin or manager, visit `/contacts/new` and create a contact.
- **Expected:** Contact created, redirect to `/contacts`.

### 4. CSRF protection

- Log in, then:
```bash
curl -v -X POST http://localhost:8000/contacts \
  -H "Cookie: session=YOUR_SESSION_COOKIE" \
  -d "full_name=Test&email=test@x.com"
```
- **Expected:** 403 (no csrf_token in body).

### 5. Logout

- Click "Log out" in the nav.
- **Expected:** Redirect to `/login`; session cleared.
- Visit `/contacts` again.
- **Expected:** Redirect to `/login`.
