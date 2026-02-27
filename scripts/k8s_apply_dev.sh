#!/usr/bin/env bash
# Apply the dev overlay to the current cluster (e.g. minikube / kubeadm).
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"
kubectl kustomize k8s/overlays/dev | kubectl apply -f -
