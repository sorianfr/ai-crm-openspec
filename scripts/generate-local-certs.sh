#!/usr/bin/env bash
# Generate self-signed certs for local HTTPS (crm.local).
# Output: docker/traefik/certs/local.crt + local.key
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CERTS_DIR="$PROJECT_ROOT/docker/traefik/certs"
mkdir -p "$CERTS_DIR"

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout "$CERTS_DIR/local.key" \
  -out "$CERTS_DIR/local.crt" \
  -subj "/CN=crm.local" \
  -addext "subjectAltName=DNS:crm.local,IP:127.0.0.1"

echo "Generated $CERTS_DIR/local.crt and $CERTS_DIR/local.key"
echo "Add 127.0.0.1 crm.local to /etc/hosts, then access https://crm.local"
