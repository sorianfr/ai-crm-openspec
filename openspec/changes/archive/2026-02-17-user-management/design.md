# Design — user-management

## Context

The CRM already has a `User` model (id, email, password_hash, role, created_at), JWT auth, and RBAC via `get_current_user` and `require_roles(allowed_roles)`. Password hashing is in `app/core/password.py` (hash_password, verify_password). There is no API yet to create or manage users; this design adds user-management endpoints that reuse existing auth and the same User table.

## Goals / Non-Goals

**Goals:**

- **POST /users** (admin-only): Create user with email, password, role. Store password via existing `hash_password`; validate role in [admin, manager, sales]. On duplicate email return 409 Conflict (or 400 if preferred); never expose password_hash. Response 201 with body `{ id, email, role, created_at }`.
- **GET /users** (auth required, admin-only for now): Return list of `{ id, email, role, created_at }` for all users. No password or password_hash in response. Keeps behavior simple and consistent with enterprise “admin manages users.”
- **PATCH /users/{id}/role** (admin-only): Update a user’s role. Input: body `{ "role": "admin" | "manager" | "sales" }`. Return 404 if user not found, 400 on invalid role. Response 200 with updated `{ id, email, role, created_at }`.

**Non-Goals:**

- **DELETE /users/{id}**: Explicitly out of scope for this change. Can be added in a follow-up; design and implementation will not include delete.
- Pagination (limit/offset) for GET /users: Deferred; can be added later if needed.

## Decisions

### Reuse existing auth and password

- **Choice:** Use `get_current_user` and `require_roles(["admin"])` for all three endpoints. Use `app/core/password.hash_password` when creating users.
- **Rationale:** No new auth mechanism; consistent with existing protected routes (e.g. POST /contacts). JWT role claim can be used as an optimization (e.g. short-circuit) but authorization SHALL be enforced via the same dependency so role changes take effect after token refresh or next login.

### Duplicate email: 409 vs 400

- **Choice:** Return **409 Conflict** when creating a user with an email that already exists.
- **Alternatives:** 400 Bad Request (simpler, less RESTful). 409 is standard for “resource already exists” and helps clients distinguish duplicate from other validation errors.
- **Rationale:** Clear semantics; if the project already uses 409 elsewhere, stay consistent; otherwise 409 is recommended for duplicate resource.

### GET /users scope: admin-only

- **Choice:** GET /users requires admin role (same as POST and PATCH) for this change.
- **Alternatives:** Allow manager to list users (e.g. for assignment); list only current user. Deferred.
- **Rationale:** Simplest and consistent with “enterprise admin manages users”; scope can be relaxed in a later change.

### Response shape and security

- **Choice:** All responses that return user data SHALL include only `id`, `email`, `role`, `created_at`. Never return `password_hash` or any password-related field.
- **Rationale:** Aligns with proposal and avoids leaking sensitive data.

### PATCH /users/{id}/role only

- **Choice:** Single PATCH endpoint for role only: `PATCH /users/{id}/role` with body `{ "role": "..." }`. No generic PATCH /users/{id} that could allow changing email or password in this change.
- **Rationale:** Minimal surface; password change (if needed) can be a separate endpoint later.

## Risks / Trade-offs

| Risk | Mitigation |
|------|-------------|
| GET /users returns many rows without pagination | Defer pagination; document that large deployments may need limit/offset later. |
| Admin deletes last admin | Out of scope (no DELETE in this change). If DELETE is added later, consider preventing removal of last admin. |
| Role change not reflected in current JWT | Expected: existing tokens keep old role until expiry or re-login. Document if needed. |

## Migration Plan

- No database migrations (existing `users` table is sufficient).
- Add new router (e.g. `app/routes/users.py`) with POST /users, GET /users, PATCH /users/{id}/role; register under `/users` in `app/main.py`.
- Use existing User model and session; no new dependencies.
- Deploy: ship code; no data or config changes required.

## Open Questions

- None blocking. Optional: whether to add audit log entries for user create/role update in this change (proposal mentioned optional; can be a follow-up).

## Verification (Swagger and curl)

- **401** on POST/GET/PATCH /users without `Authorization: Bearer <token>`.
- **403** on POST/GET/PATCH /users with a valid token but non-admin role.
- **409** on POST /users when email already exists.
- **404** on PATCH /users/{id}/role when user id does not exist.
- **422** on invalid body (e.g. missing email/password/role, or role not in admin/manager/sales).
- All user response bodies contain only `id`, `email`, `role`, `created_at` (no `password` or `password_hash`).
- Swagger: `/docs` — lock icon on user endpoints; try with/without token and with admin vs non-admin.
- curl: login with admin@dev.local, get token; call POST /users (201), GET /users (200), PATCH /users/2/role (200); repeat POST same email (409); PATCH /users/99999/role (404).
