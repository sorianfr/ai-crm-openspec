## 1. Certificates and Traefik config

- [x] 1.1 Add script `scripts/generate-local-certs.sh` to generate self-signed certs at `docker/traefik/certs/local.crt` + `local.key` (SAN includes DNS:crm.local and IP:127.0.0.1)
- [x] 1.2 Add `docker/traefik/traefik.yml` (static config: entrypoints web:80 + websecure:443; docker provider; file provider for TLS; exposedByDefault=false)
- [x] 1.3 Add `docker/traefik/dynamic.yml` (TLS certificates pointing to `/certs/local.crt` + `/certs/local.key`)
- [x] 1.4 Add `docker/traefik/certs/.gitkeep` and update `.gitignore` to ignore certs except `.gitkeep` (do not commit private keys)

## 2. Compose and routing (prod)

- [x] 2.1 Add Traefik service to `docker-compose.prod.yml` (ports 80/443, volumes for docker socket + traefik.yml + dynamic.yml + certs)
- [x] 2.2 Add Traefik labels to `app` service: router Host(`crm.local`) on websecure with tls=true; router on web that redirects to https; service port 8000
- [x] 2.3 Stop publishing `app` port 8000 to host in prod (Traefik-only access)

## 3. Documentation and verification

- [x] 3.1 Update README with "Local HTTPS (production)" section: add 127.0.0.1 crm.local to /etc/hosts; run cert script; docker compose -f docker-compose.prod.yml up -d; open https://crm.local/login
- [x] 3.2 Add VERIFICATION.md for this change: curl check (curl -k https://crm.local/health); browser check (login persists, /contacts loads after login)
