#!/usr/bin/env bash
# Install AWS EBS CSI driver via Helm and configure a default gp3 StorageClass.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Adding aws-ebs-csi-driver Helm repo..."
helm repo add aws-ebs-csi-driver https://kubernetes-sigs.github.io/aws-ebs-csi-driver
helm repo update

echo "Installing / upgrading aws-ebs-csi-driver into kube-system..."
helm upgrade --install aws-ebs-csi-driver aws-ebs-csi-driver/aws-ebs-csi-driver \
  --namespace kube-system \
  --create-namespace

echo "Applying gp3 default StorageClass..."
kubectl apply -f storageclass-gp3.yaml

echo
echo "=== StorageClasses ==="
kubectl get storageclass

echo
echo "=== AWS EBS CSI driver pods (kube-system) ==="
kubectl -n kube-system get pods -l app.kubernetes.io/name=aws-ebs-csi-driver

