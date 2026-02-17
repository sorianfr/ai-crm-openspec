# Proposal — add-jwt-auth-rbac-audit-logs

## Why
Our CRM currently lacks production-grade security controls: requests are not authenticated in a standardized way, there is no role-based authorization, and we have no audit trail for critical data changes. Adding JWT authentication, RBAC, and audit logs will make the system safer, more scalable in Kubernetes, and ready for future multi-tenant support.

## What Changes
- Add JWT-based authentication for API access:
  - New `/auth/login` endpoint returning an access token (HS256, exp).
  - Add a standard `Authorization: Bearer <token>` mechanism for protected routes.
- Add Role-Based Access Control (RBAC) for API authorization:
  - Add `role` to the user model with roles: `admin`, `manager`, `sales`.
  - Introduce reusable authorization checks (e.g., `require_roles([...])`).
- Add audit logging for core entity mutations:
  - New `audit_logs` persistence layer storing CREATE/UPDATE/DELETE actions.
  - Automatically write audit entries for mutations on core entities (customers and deals, or equivalent domain entities in this repo).
- Modify at least one existing capability to enforce protection by auth + RBAC:
  - Mark selected CRUD endpoints as requiring authentication and appropriate roles.
- Non-breaking by default for internal/dev usage, but endpoints that become protected will require tokens.
  - **BREAKING**: Any previously public endpoints that are now protected will return `401/403` unless authenticated/authorized.

## Capabilities

### New
- jwt-auth
- rbac
- audit-logs

### Modified
- contacts-crud (or equivalent primary CRUD capability in this repo) — enforce auth + RBAC on at least one existing endpoint.
- companies-crud (optional, if we also protect company endpoints; otherwise omit)
- contact-notes / contact-activities (optional, only if we enforce RBAC there as well)

## Impact
- **APIs**
  - Adds `/auth/login`.
  - Updates selected existing endpoints to require JWT authentication (`401`) and RBAC authorization (`403`).
- **Data model**
  - Adds `role` column/field to the user model; new `audit_logs` table (or equivalent) for CREATE/UPDATE/DELETE events on core entities.
- **Dependencies**
  - New dependency for JWT handling (e.g. PyJWT) and possibly password hashing (e.g. passlib/bcrypt).
- **Configuration**
  - JWT secret and token expiration (e.g. env vars) for production.
