# Proposal — user-management

## Why

The CRM has authentication and roles (admin, manager, sales) but no way to manage users from the application. Adding user-management endpoints (create, list, change role, optionally delete) turns the CRM into a real enterprise system where admins can onboard users and assign roles without touching the database directly.

## What Changes

- **POST /users** (admin only): Create a new user (e.g. email, password, role). Returns 201 with user id or 400/422 on validation error. Protected by `require_roles(["admin"])`.
- **GET /users**: List users (e.g. id, email, role, created_at; no password). Protected by authenticated user; scope (all users vs. limited) can be admin-only or extended later.
- **PATCH /users/{id}/role**: Update a user's role (admin only). Body: `{ "role": "admin" | "manager" | "sales" }`. Returns 200 or 404/400.
- **(Optional) DELETE /users/{id}**: Delete a user (admin only). Returns 204 or 404. Optional for this change; can be deferred.

All new endpoints SHALL require JWT authentication. POST, PATCH, and (if implemented) DELETE SHALL require admin role; GET may be admin-only or allow manager for listing.

## Capabilities

### New Capabilities

- **user-management**: API to create users (POST /users), list users (GET /users), and update a user's role (PATCH /users/{id}/role). Optional: delete user (DELETE /users/{id}). All protected by existing auth and RBAC (admin for write operations).

### Modified Capabilities

- None. User model and RBAC already exist; this change adds management endpoints only.

## Impact

- **APIs**: New routes under `/users`: POST (create), GET (list), PATCH `/{id}/role` (update role). Optional DELETE `/{id}`.
- **Data model**: No new tables; uses existing `users` table. Optional: audit log entries for user create/update/delete.
- **Dependencies**: None new.
- **Configuration**: None new.
