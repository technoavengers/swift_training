# 📘 **Prometheus Installation Using Helm + RBAC Verification Guide**

This lab demonstrates:

-   Installing Prometheus using Helm\
-   Verifying automatically created ServiceAccounts\
-   Inspecting ClusterRoles created for Prometheus\
-   Inspecting ClusterRoleBindings created for Prometheus

------------------------------------------------------------------------

# 🧩 **1. Add Prometheus Helm Repository**

``` bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

------------------------------------------------------------------------

# 🧩 **2. Create Monitoring Namespace**

``` bash
kubectl create namespace monitoring
```

------------------------------------------------------------------------

# 🧩 **3. Install Prometheus Using Helm**

``` bash
helm install prom prometheus-community/kube-prometheus-stack -n monitoring
```

Check helm release:

``` bash
helm list -n monitoring
```

------------------------------------------------------------------------

# 🧩 **4. Verify ServiceAccounts Created Automatically**

``` bash
kubectl get sa -n monitoring
```

Expected ServiceAccounts include:

-   prom-kube-state-metrics\
-   prom-prometheus-node-exporter\
-   prom-prometheus-operator\
-   prom-kube-prometheus-stack-prometheus\
-   prom-alertmanager\
-   prom-grafana

------------------------------------------------------------------------

# 🧩 **5. Check ClusterRoles Created for Prometheus**

``` bash
kubectl get clusterrole | grep prom
```

Inspect a ClusterRole:

``` bash
kubectl describe clusterrole prom-kube-state-metrics
```

------------------------------------------------------------------------

# 🧩 **6. Check ClusterRoleBindings for Prometheus**

``` bash
kubectl get clusterrolebinding | grep prom
```

Describe one binding:

``` bash
kubectl describe clusterrolebinding prom-kube-prometheus-stack-prometheus
```

------------------------------------------------------------------------

# 🧩 **7. (Optional) Check Prometheus UI**

``` bash
kubectl port-forward -n monitoring svc/prom-kube-prometheus-stack-prometheus 9090:9090
```

Open:

    http://localhost:9090

------------------------------------------------------------------------

# 🎯 **Summary**

-   Prometheus Helm chart automatically creates:
    -   ServiceAccounts\
    -   Roles / ClusterRoles\
    -   RoleBindings / ClusterRoleBindings
-   RBAC enables Prometheus to:
    -   discover pods\
    -   read metrics\
    -   scrape endpoints\
    -   interact with Kubernetes objects
