# Traefik local HTTPS proxy

The system SHALL provide a Traefik reverse proxy for production Compose with local HTTPS termination, self-signed certificates, routing of `crm.local` to the app, and HTTP→HTTPS redirect so Secure session cookies work in the browser.

## Requirements

### Requirement: Traefik reverse proxy in production compose

The production Compose stack SHALL include a Traefik service that terminates HTTPS and forwards requests to the app.

#### Scenario: Traefik service present
- **WHEN** the production Compose stack is started
- **THEN** a Traefik container SHALL be running
- **AND** SHALL expose HTTP (80) and HTTPS (443) on the host
- **AND** SHALL forward requests to the app service on the internal network

#### Scenario: App reachable only via Traefik
- **WHEN** production Compose is running
- **THEN** the app SHALL NOT need its port (e.g. 8000) published to the host for normal access
- **AND** external access SHALL go through Traefik

### Requirement: Self-signed certificates for local HTTPS

The system SHALL provide self-signed TLS certificates for `crm.local` so HTTPS works locally without an external CA.

#### Scenario: Certs available for crm.local
- **WHEN** deploying the production stack locally
- **THEN** self-signed certs for `crm.local` SHALL exist (e.g. in `certs/` or via script)
- **AND** Traefik SHALL be configured to use them for TLS termination

#### Scenario: Cert generation documented or automated
- **WHEN** certs are missing
- **THEN** a script or documented command SHALL generate them (e.g. `scripts/generate-local-certs.sh`)
- **OR** certs SHALL be committed so the stack runs without manual generation

### Requirement: Dynamic TLS configuration

Traefik SHALL use dynamic configuration (file provider) for TLS certificates so certs can be updated without rebuilding the image.

#### Scenario: File provider for TLS
- **WHEN** Traefik starts
- **THEN** it SHALL load TLS certificate configuration from a file provider (dynamic config)
- **AND** the cert paths SHALL point to the self-signed certs for `crm.local`

### Requirement: Route crm.local to app

Traefik SHALL route requests for host `crm.local` (and optionally `www.crm.local`) to the app service.

#### Scenario: Host-based routing
- **WHEN** a request arrives with `Host: crm.local`
- **THEN** Traefik SHALL forward it to the app service (e.g. `http://app:8000`)
- **AND** the response SHALL be returned to the client

#### Scenario: HTTPS access
- **WHEN** a request is made to `https://crm.local`
- **THEN** Traefik SHALL terminate TLS and forward the request to the app over HTTP on the internal network
- **AND** Secure cookies set by the app SHALL be accepted by the browser (because the connection is HTTPS)

### Requirement: HTTP to HTTPS redirect

All HTTP requests SHALL be redirected to HTTPS so Secure cookies work.

#### Scenario: HTTP redirect
- **WHEN** a request is made to `http://crm.local` (port 80)
- **THEN** Traefik SHALL respond with a redirect (e.g. 301 or 302) to `https://crm.local`
- **AND** the client SHALL be directed to use HTTPS

### Requirement: Verification documentation

The change SHALL include verification docs that describe how to access the app over HTTPS and how to set up `crm.local`.

#### Scenario: Host setup documented
- **WHEN** a user follows the verification or README instructions
- **THEN** they SHALL be told to add `127.0.0.1 crm.local` to `/etc/hosts` (or equivalent)
- **AND** the exact line or command SHALL be provided

#### Scenario: HTTPS access steps
- **WHEN** verifying the production stack
- **THEN** the docs SHALL describe accessing `https://crm.local` (accepting the self-signed cert warning)
- **AND** SHALL verify that login and session persistence work (Secure cookies)
