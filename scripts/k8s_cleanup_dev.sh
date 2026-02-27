#!/usr/bin/env bash
# Remove CRM resources applied from the dev overlay.
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"
kubectl kustomize k8s/overlays/dev | kubectl delete -f - --ignore-not-found --timeout=60s 2>/dev/null || true
# If any resources remain (e.g. PVCs with finalizers), delete namespace
kubectl delete namespace crm --ignore-not-found --timeout=120s 2>/dev/null || true
