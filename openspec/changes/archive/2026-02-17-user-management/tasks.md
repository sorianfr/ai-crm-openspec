## 1. Pydantic schemas

- [x] 1.1 Add Pydantic schemas for user-management: create user (email, password, role), user response (id, email, role, created_at), and role update body (role)

## 2. Users router and wiring

- [x] 2.1 Add users router (e.g. app/routes/users.py) and include it in main under /users

## 3. POST /users (admin-only)

- [x] 3.1 Implement POST /users with require_roles(["admin"]); accept email, password, role; validate role in admin/manager/sales; store password via hash_password; return 409 on duplicate email, 422 on invalid body; response 201 with { id, email, role, created_at }

## 4. GET /users (admin-only)

- [x] 4.1 Implement GET /users with require_roles(["admin"]); response 200 with list of { id, email, role, created_at }

## 5. PATCH /users/{id}/role (admin-only)

- [x] 5.1 Implement PATCH /users/{id}/role with require_roles(["admin"]); body { role }; 404 if user not found, 422 if invalid body/role; response 200 with { id, email, role, created_at }

## 6. Audit logging

- [x] 6.1 Add audit log calls: on successful POST /users write CREATE, entity_type user, entity_id, user_id (admin), summary without secrets; on successful PATCH /users/{id}/role write UPDATE, entity_type user, entity_id, user_id (admin), summary (e.g. "role changed to X")

## 7. Verification

- [x] 7.1 Verify with Swagger and curl: login as admin, call POST/GET/PATCH /users; verify 401 without token, 403 with non-admin token, 409 on duplicate email, 404 on unknown id; confirm responses never include password or password_hash
