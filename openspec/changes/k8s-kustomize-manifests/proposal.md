# K8s Kustomize Manifests

## Why

Deploy the CRM app to Kubernetes (e.g. kubeadm clusters) using Kustomize for base and overlay-based customization, without relying on cloud-specific controllers.

## What Changes

- **k8s/base**: Namespace, App Deployment, App Service, ConfigMap, Secret, Postgres StatefulSet, Postgres Service, Ingress. Postgres persistence via StatefulSet `volumeClaimTemplates` (PVC). App reads DB connection from env vars (ConfigMap + Secret).
- **k8s/overlays/dev**: Image tag override (`crm-app:dev`), replica count, resource limits (lighter for dev), Ingress host `crm.dev.local`.
- **App config**: Support building `DATABASE_URL` from `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`, `DB_PORT` when `DATABASE_URL` is not set (for K8s env injection).
- **kustomization.yaml** in `k8s/base` and `k8s/overlays/dev`. Manifests are kubeadm-compatible (standard Ingress with `ingressClassName: nginx`, no cloud LB required).

## Capabilities

- Kubernetes deployment via Kustomize; app config from env; Postgres with persistent storage; dev overlay for image/replicas/resources/ingress host.

## Impact

- New `k8s/base/*` and `k8s/overlays/dev/*`.
- `app/core/config.py`: build `DATABASE_URL` from `DB_*` env vars when unset.
