## Why

Production compose uses Secure cookies (`APP_ENV=production`), but without HTTPS browsers reject them. Local testing of a production-like setup needs HTTPS termination so Secure session cookies work in the browser. Adding Traefik as a reverse proxy with local HTTPS termination enables realistic dev/prod parity for cookie behavior.

## What Changes

- Add Traefik reverse proxy to production Compose stack
- Provide self-signed certificates for local HTTPS (e.g. `certs/` or similar)
- Configure Traefik dynamic TLS (file provider) for the self-signed cert
- Route `crm.local` (and/or `https://crm.local`) to the app service
- HTTP → HTTPS redirect so all traffic uses HTTPS
- Update verification docs (README, VERIFICATION.md) with HTTPS access instructions and host setup (`crm.local` in `/etc/hosts`)

## Capabilities

### New Capabilities

- `traefik-local-https`: Traefik reverse proxy for production compose, self-signed certs, dynamic TLS config, routing `crm.local` → app, HTTP→HTTPS redirect

### Modified Capabilities

- `docker-runtime-config`: Extend production compose to include Traefik service and TLS-aware routing (optional delta if spec-level behavior changes)

## Impact

- `docker-compose.prod.yml` (add Traefik service, labels on app, volumes for certs/config)
- New Traefik config files (static + dynamic for TLS)
- New certs directory / script for self-signed certs
- `README` and change `VERIFICATION.md` updates
