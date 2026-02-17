## 1. Dependencies and configuration

- [x] 1.1 Add PyJWT and password-hashing dependency (e.g. passlib[bcrypt]) to requirements.txt
- [x] 1.2 Add JWT_SECRET and JWT_EXPIRATION_MINUTES (or JWT_EXPIRATION_SECONDS) to app config; load from env; add to .env.example and README

## 2. User model and migrations

- [x] 2.1 Create User model with id, email, password_hash, role (admin/manager/sales), created_at; persist via SQLAlchemy
- [x] 2.2 Add Alembic migration for users table with role constraint

## 3. Audit log persistence

- [x] 3.1 Create AuditLog model (id, timestamp, user_id nullable, action, entity_type, entity_id, optional summary); add Alembic migration for audit_logs table

## 4. JWT auth and login

- [x] 4.1 Implement POST /auth/login: accept email/password (JSON or form); verify against User password_hash; return 401 on invalid credentials, 422/400 on missing or malformed body
- [x] 4.2 On successful login, create JWT with sub, role, exp (HS256); return 200 with access_token and token_type "bearer"
- [x] 4.3 Implement get_current_user dependency: extract Bearer token, decode and validate JWT (signature, exp), resolve user (e.g. by sub); raise 401 when missing, invalid, or expired

## 5. RBAC

- [x] 5.1 Implement require_roles(allowed_roles) dependency: after get_current_user, check current_user.role in allowed_roles; return 403 if not allowed

## 6. Audit logging on mutations

- [x] 6.1 Add helper to create and persist an audit log entry (action, entity_type, entity_id, user_id from context, timestamp)
- [x] 6.2 Call audit helper on Contact create, update, delete (on commit or after flush)
- [x] 6.3 Call audit helper on Company create, update, delete (on commit or after flush)

## 7. Protect at least one contact endpoint

- [x] 7.1 Protect at least one contact CRUD route (e.g. POST /contacts or POST /contacts/{id} or POST /contacts/{id}/delete) with get_current_user and require_roles; ensure 401 without token, 403 with valid token but insufficient role

## 8. Dev bootstrap and verification

- [x] 8.1 Optional: seed one admin user in development (e.g. migration or script) when APP_ENV=development; do not seed in production
- [x] 8.2 Verify login returns token and protected endpoint returns 401 without token and 403 with wrong role; verify audit entries created on contact/company mutation
