# 🧪 **Lab 2: Deploying the MinIO Operator on Kubernetes**

**Estimated Time:** 25 minutes

------------------------------------------------------------------------

## 📘 **Introduction to the MinIO Operator**

In the previous lab, you learned how CRDs and custom controllers work by
building your own Operator.\
Now, let's explore a real-world operator: **The MinIO Operator**.

### ⭐ What is the MinIO Operator?

The **MinIO Operator** simplifies:

-   Deploying MinIO clusters\
-   Managing storage pools\
-   Managing multi-tenant object storage\
-   Automation of Pods, PVCs, StatefulSets, Secrets, and Services

MinIO uses **CRDs** such as **Tenant** to define complete MinIO
clusters.

📌 Reference GitHub Repository:\
🔗 https://github.com/minio/operator

------------------------------------------------------------------------

# 🧩 **Step 1: Deploy the MinIO Operator**

Apply the operator manifest:

``` bash
kubectl apply -f minio-operator.yaml
```

------------------------------------------------------------------------

# 🧩 **Step 2: Verify Operator Pods**

Check if operator components are running:

``` bash
kubectl get pod -n minio-operator
```

You should see controller pods, webhook pods, etc.

------------------------------------------------------------------------

# 🧩 **Step 3: Check CRDs Installed by the Operator**

List CRDs:

``` bash
kubectl get crd
```

You will find CRDs like:

-   `tenants.minio.min.io`
-   `buckets.minio.min.io`
-   `users.minio.min.io`

------------------------------------------------------------------------

### 🔍 Describe the Tenant CRD

``` bash
kubectl describe crd tenants.minio.min.io
```

👉 This is a large CRD, similar to the CRD you created in **Lab 1**, but
with many more fields used by MinIO internally.

------------------------------------------------------------------------

# 🧩 **Step 4: Create Namespace for MinIO Tenant**

Create a namespace file `minio-namespace.yaml`:

``` yaml
apiVersion: v1
kind: Namespace
metadata:
  name: minio-tenant
```

Apply it:

``` bash
kubectl apply -f minio-namespace.yaml
```

------------------------------------------------------------------------

# 🧩 **Step 5: Create Secret for MinIO Tenant**

Create `minio-secret.yaml`:

``` yaml
apiVersion: v1
kind: Secret
metadata:
  name: storage-configuration
  namespace: minio-tenant
stringData:
  config.env: |-
    export MINIO_ROOT_USER="minio"
    export MINIO_ROOT_PASSWORD="minio123"
    export MINIO_STORAGE_CLASS_STANDARD="EC:2"
    export MINIO_BROWSER="on"
type: Opaque
```

Apply:

``` bash
kubectl apply -f minio-secret.yaml
```

Check secret:

``` bash
kubectl get secret -n minio-tenant
```

------------------------------------------------------------------------

# 🧩 **Step 6: Create a MinIO Tenant Using Tenant CRD**

Create `minio-tenant.yaml`:

``` yaml
apiVersion: minio.min.io/v2
kind: Tenant
metadata:
  labels:
    app: minio
  name: myminio
  namespace: minio-tenant
spec:
  configuration:
    name: storage-configuration
  image: quay.io/minio/minio:RELEASE.2024-08-17T01-24-54Z
  mountPath: /export
  pools:
  - name: pool-0
    servers: 2
    volumeClaimTemplate:
      apiVersion: v1
      kind: persistentvolumeclaims
      spec:
        accessModes:
        - ReadWriteOnce
        resources:
          requests:
            storage: 1Gi
        storageClassName: standard
    volumesPerServer: 2
  requestAutoCert: false
```

Apply Tenant:

``` bash
kubectl apply -f minio-tenant.yaml
```

------------------------------------------------------------------------

# 🧩 **Step 7: Validate the Tenant Deployment**

### ✔ Check Tenant Object

``` bash
kubectl get tenant -n minio-tenant
```

### ✔ Check All Resources Created

``` bash
kubectl get all -n minio-tenant
```

Check PVCs created automatically:

``` bash
kubectl get pvc -n minio-tenant
```

------------------------------------------------------------------------

# 🧠 **What the Tenant CRD Creates Automatically**

When you create a Tenant resource:

### 🔹 **StatefulSets**

-   A StatefulSet with **2 replicas** (based on `servers: 2`)

### 🔹 **Pods**

-   One MinIO Pod per server instance\
-   Each Pod contains:
    -   **InitContainer**: runs once for config\
    -   **Main MinIO container**

### 🔹 **Persistent Volume Claims**

-   **2 PVCs per server**, per `volumesPerServer: 2`

### 🔹 **Services**

-   **Headless service** for internal networking\
-   **Console service** for MinIO UI

------------------------------------------------------------------------

# 🧹 **Cleanup**

To delete everything created:

``` bash
kubectl delete -f minio-tenant.yaml
kubectl delete -f minio-secret.yaml
kubectl delete -f minio-namespace.yaml
```

------------------------------------------------------------------------

# 🎉 **Lab Conclusion**

In this lab, you:

✔ Installed the **MinIO Operator**\
✔ Explored CRDs created by the operator\
✔ Created your MinIO Tenant using a CRD\
✔ Observed how the Operator automatically created StatefulSets, PVCs,
Pods, and Services

This demonstrates how operators like MinIO automate complex distributed
system deployments using **CRDs + controllers**, similar to your custom
operator from Lab 1.
