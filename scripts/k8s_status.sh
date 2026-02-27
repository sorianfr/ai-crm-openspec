#!/usr/bin/env bash
# Show status of CRM resources in the crm namespace.
set -e
echo "=== Namespace crm ==="
kubectl get namespace crm 2>/dev/null || true
echo ""
echo "=== Pods ==="
kubectl get pods -n crm 2>/dev/null || true
echo ""
echo "=== Services ==="
kubectl get svc -n crm 2>/dev/null || true
echo ""
echo "=== Ingress ==="
kubectl get ingress -n crm 2>/dev/null || true
echo ""
echo "=== StatefulSets / Deployments ==="
kubectl get statefulset,deployment -n crm 2>/dev/null || true
