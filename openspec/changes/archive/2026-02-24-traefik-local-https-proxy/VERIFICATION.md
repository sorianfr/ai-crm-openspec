# Traefik local HTTPS proxy – verification

## Prerequisites

- Add `127.0.0.1 crm.local` to `/etc/hosts`
- Run `./scripts/generate-local-certs.sh` to create self-signed certs
- Prod env: `.env.prod` with `JWT_SECRET`, `SESSION_SECRET`, `DATABASE_URL`

## Curl check

```bash
curl -k https://crm.local/health
```

Expect 200 and healthy response.

## Browser check

1. Open https://crm.local/login (accept self-signed cert warning)
2. Log in
3. Navigate to /contacts
4. Confirm session persists (no redirect back to login)
