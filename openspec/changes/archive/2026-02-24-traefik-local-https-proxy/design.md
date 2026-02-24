# Design: Traefik local HTTPS proxy

## Context

Production compose (`docker-compose.prod.yml`) runs the app with `APP_ENV=production` and Secure cookies enabled. Browsers only send Secure cookies over HTTPS. Without a reverse proxy terminating TLS locally, testing production cookie behavior fails. The current prod compose exposes the app on port 8000 directly; we need HTTPS in front so Secure cookies work in the browser.

## Goals / Non-Goals

**Goals:**

- Add Traefik as a reverse proxy to the production Compose stack
- Provide self-signed certificates for local HTTPS (no external CA)
- Configure Traefik dynamic TLS via file provider for the self-signed cert
- Route `crm.local` (and `https://crm.local`) to the app service
- HTTP → HTTPS redirect so all traffic uses HTTPS
- Update verification docs with host setup and HTTPS access instructions

**Non-Goals:**

- Let's Encrypt or external CA; production TLS in a real environment
- Changes to the app code (no TLS handling in the app)
- Dev compose (remains HTTP on localhost)

## Decisions

### Traefik as reverse proxy

**Choice:** Use Traefik v3 (or v2) in Docker.  
**Rationale:** Traefik is built for containers, supports dynamic config via file provider, and handles TLS and redirects out of the box. Alternatives: nginx (more config work for dynamic TLS), Caddy (simpler but less Docker-native). Traefik's label-based routing and file provider fit our compose setup.

### Self-signed certificates

**Choice:** Provide a script or pre-generated certs in `certs/` (e.g. `certs/crm.local.crt`, `certs/crm.local.key`) for `crm.local` and `*.crm.local`. Use `openssl` to generate.  
**Rationale:** Self-signed certs are sufficient for local testing; users will accept the browser warning. A script (e.g. `scripts/generate-local-certs.sh`) makes regeneration easy. Certs committed or documented in README so new clones can run without extra steps (or script run on first use).

### Dynamic TLS (file provider)

**Choice:** Use Traefik's file provider for dynamic TLS configuration, pointing to the self-signed cert.  
**Rationale:** Static config defines entrypoints; dynamic config defines TLS certificates and routes. This keeps cert rotation (if needed) simple without rebuilding the image.

### Hostname and routing

**Choice:** Use `crm.local` as the canonical hostname. Traefik routes `Host(`crm.local`)` (and optionally `Host(`www.crm.local`)`) to the app service.  
**Rationale:** `.local` is a common convention for local dev; avoids conflicts with real domains. Users add `127.0.0.1 crm.local` to `/etc/hosts`.

### HTTP → HTTPS redirect

**Choice:** Configure an HTTP entrypoint (80) that redirects to HTTPS (443).  
**Rationale:** Ensures all traffic uses HTTPS so Secure cookies are sent. Traefik middleware `redirectscheme` or an HTTP router with `redirect` achieves this.

### Port exposure

**Choice:** Expose Traefik on 80 (HTTP) and 443 (HTTPS) on the host. The app service no longer needs port 8000 published; Traefik reaches it on the internal network.  
**Rationale:** Single entry point; app is only reachable through Traefik, matching a production-style setup.

### File layout

- `docker/traefik/traefik.yml` – static config (entrypoints, providers)
- `docker/traefik/dynamic/` – dynamic config (TLS certs, routers, services)
- `certs/` – self-signed certs for `crm.local` (gitignored if generated; or commit with script)
- `scripts/generate-local-certs.sh` – generates certs for `crm.local`

## Risks / Trade-offs

| Risk | Mitigation |
|------|------------|
| Browser warns on self-signed cert | Expected; document that users must accept/trust for local testing |
| `/etc/hosts` not configured | Document clearly in README and VERIFICATION; provide exact line to add |
| Cert path wrong in container | Use volume mount; verify paths in Traefik config |
| Traefik and app both need network | Use same compose network; Traefik forwards to `http://app:8000` |

## Migration Plan

- Add Traefik service and config; add app labels for Traefik
- Remove or comment app port 8000 publish in prod compose (or keep for debug)
- Add cert generation script; document first-run steps
- Update README: add "Local HTTPS (production compose)" with `crm.local` setup
- Add VERIFICATION.md steps for HTTPS access, login, and session persistence

## Open Questions

- Whether to commit generated self-signed certs (simplifies onboarding) or require running the script (clearer but extra step)
- Whether to support `www.crm.local` redirect to `crm.local` (optional)
