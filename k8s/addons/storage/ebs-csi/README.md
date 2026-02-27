# AWS EBS CSI Storage Add-on (kubeadm on AWS)

This add-on installs the **AWS EBS CSI driver** and creates a **default `gp3` StorageClass** for a self‑managed **kubeadm** cluster running on EC2 instances.

The manifests live under:

- `k8s/addons/storage/ebs-csi/storageclass-gp3.yaml`
- `k8s/addons/storage/ebs-csi/install-ebs-csi.sh`

They are **not wired into the app Kustomize overlays**; you run them independently when you want EBS‑backed dynamic provisioning.

## Prerequisites

- A self‑managed Kubernetes cluster created with **kubeadm** on **AWS EC2** instances.
- `kubectl` and `helm` installed on your workstation and pointing at the cluster.
- Control plane and nodes configured with `--allow-privileged=true` for the API server (standard for kubeadm on AWS when using CSI drivers).
- **Node IAM permissions**:
  - Each worker node must have an **instance profile / IAM role** attached.
  - That role must include the AWS managed policy:
    - `arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy`
  - This allows the driver to create, attach, detach, and delete EBS volumes.
- EC2 instances must have access to the **EC2 metadata service** (IMDS) or equivalent metadata source so the driver can discover region and instance details.

## What gets installed

Running the install script will:

1. Add the upstream Helm repo `aws-ebs-csi-driver`.
2. Install or upgrade the `aws-ebs-csi-driver` Helm release in the `kube-system` namespace.
3. Apply `storageclass-gp3.yaml`, which defines:
   - `provisioner: ebs.csi.aws.com`
   - `parameters.type: gp3`
   - `parameters.fsType: ext4`
   - `volumeBindingMode: WaitForFirstConsumer`
   - `allowVolumeExpansion: true`
   - `metadata.annotations.storageclass.kubernetes.io/is-default-class: "true"` (marks it as the **default** StorageClass).

## How to install

From the repo root:

```bash
cd k8s/addons/storage/ebs-csi
./install-ebs-csi.sh
```

The script will:

- Add/update the Helm repo.
- Install/upgrade the driver into `kube-system`.
- Apply the `gp3` default StorageClass.
- Print current StorageClasses and the aws‑ebs‑csi driver pods.

## How to validate the driver

1. **Check StorageClasses**

   ```bash
   kubectl get storageclass
   ```

   You should see something like:

   - `gp3 (default)` with:
     - `PROVISIONER` = `ebs.csi.aws.com`

2. **Check driver pods**

   ```bash
   kubectl -n kube-system get pods -l app.kubernetes.io/name=aws-ebs-csi-driver
   ```

   Expect the controller Deployment and node DaemonSet pods to be in `Running` / `Ready` state.

3. **Smoke test with a PVC**

   Create a simple test PersistentVolumeClaim (PVC), for example:

   ```yaml
   apiVersion: v1
   kind: PersistentVolumeClaim
   metadata:
     name: ebs-gp3-test
   spec:
     accessModes:
       - ReadWriteOnce
     resources:
       requests:
         storage: 4Gi
   ```

   Apply it:

   ```bash
   kubectl apply -f pvc-test.yaml
   kubectl get pvc ebs-gp3-test
   ```

   The PVC should transition to `Bound`, and `kubectl get pv` should show a dynamically created PV with an EBS volume ID in its annotations.

4. **(Optional) Attach to a test Pod**

   If you want to be extra sure, mount the PVC into a simple Pod, confirm it starts successfully, and check the node has an EBS volume attached in the EC2 console.

If any of these steps fail, double‑check:

- Worker node IAM role includes `AmazonEBSCSIDriverPolicy`.
- Nodes can reach the EC2 metadata service (IMDS).
- The cluster’s `kube-apiserver` allows privileged pods.

