## MODIFIED Requirements

### Requirement: JWT payload includes tenant_id

The token issued on login SHALL include a tenant_id claim. Enforcement of tenant scoping SHALL use the user loaded from the DB; the JWT tenant_id claim is not authoritative.

#### Scenario: Login token includes tenant_id
- **WHEN** a user successfully logs in
- **THEN** the JWT payload SHALL include sub, role, exp, and tenant_id
- **AND** invalid or expired token SHALL result in 401

#### Scenario: get_current_user uses DB for tenant_id
- **WHEN** get_current_user resolves the current user
- **THEN** the user SHALL be loaded from the database and SHALL carry tenant_id from the DB
- **AND** tenant scoping SHALL use this DB tenant_id

#### Scenario: Backwards compatibility
- **WHEN** a token lacks tenant_id (minted before this change)
- **THEN** the system SHALL accept it by looking up the user from the DB
- **AND** newly minted tokens SHALL include tenant_id
