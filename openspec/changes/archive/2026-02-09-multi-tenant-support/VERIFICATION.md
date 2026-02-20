# Multi-tenant support – verification

## Prerequisites

- Migrations applied: `alembic upgrade head`
- Optional dev seed (default tenant + admin): start app once with `APP_ENV=development` or run seed.
- Verification tenants and users: run the DB script below.
- App running: `uvicorn app.main:app --reload` (default http://127.0.0.1:8000).

## 1. Create tenants A & B and users (DB script)

From project root:

```bash
python3 scripts/seed_verification_tenants.py
```

This creates:

- Tenants: "Tenant A", "Tenant B"
- Users: `admin_tenant_a@test.local`, `admin_tenant_b@test.local` (password: `test`)

Idempotent: safe to run again (skips if tenants already exist).

## 2. Curl commands

Get a token (tenant A):

```bash
TOKEN_A=$(curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin_tenant_a@test.local","password":"test"}' \
  | jq -r '.access_token')
```

List users as tenant A (scoped to tenant):

```bash
curl -s -H "Authorization: Bearer $TOKEN_A" http://127.0.0.1:8000/users | jq .
```

Create a user in tenant A and note `id`:

```bash
curl -s -X POST http://127.0.0.1:8000/users \
  -H "Authorization: Bearer $TOKEN_A" \
  -H "Content-Type: application/json" \
  -d '{"email":"sales_a@test.local","password":"pass","role":"sales"}' | jq .
```

Get token for tenant B:

```bash
TOKEN_B=$(curl -s -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin_tenant_b@test.local","password":"test"}' \
  | jq -r '.access_token')
```

List users as tenant B (must not include tenant A users):

```bash
curl -s -H "Authorization: Bearer $TOKEN_B" http://127.0.0.1:8000/users | jq .
```

Cross-tenant access by id must return **404** (replace `USER_A_ID` with the id from create):

```bash
curl -s -o /dev/null -w "%{http_code}" -X PATCH http://127.0.0.1:8000/users/USER_A_ID/role \
  -H "Authorization: Bearer $TOKEN_B" \
  -H "Content-Type: application/json" \
  -d '{"role":"manager"}'
# Expected: 404
```

## 3. Python verification script

From project root (requires `requests`):

```bash
pip install requests
python3 scripts/verify_multi_tenant.py
# Or against another base URL:
python3 scripts/verify_multi_tenant.py http://localhost:8000
```

The script logs in as tenant A, lists users, creates a user, then as tenant B lists users (asserts tenant A user is not in the list) and PATCHes tenant A’s user by id and asserts **404**.

## 4. Contact/company isolation (HTML flows)

Contacts and companies are tenant-scoped; list/detail/create/update/delete use `current_user.tenant_id`. To verify in the UI:

1. Log in as `admin_tenant_a@test.local`, create a contact, note its id in the URL.
2. Log in as `admin_tenant_b@test.local`, open `/contacts/<id>` with that id → **404**.
3. List contacts as B → only B’s contacts (A’s contact must not appear).

No public tenant admin API: tenants are created only via DB scripts (e.g. `scripts/seed_verification_tenants.py` or migrations).
