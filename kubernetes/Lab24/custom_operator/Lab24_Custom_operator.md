# 🧪 **Lab 1: Understanding Operators & Custom Resource Definitions (CRDs)**

**Estimated Time:** 15 minutes

------------------------------------------------------------------------

## 🎯 **Objective**

In this lab, you will:

-   Create a **Custom Resource Definition (CRD)**\
-   Create a **Custom Resource**\
-   Build a **custom Kubernetes Operator** using **Kopf (Python)**\
-   Understand how Operators automate application lifecycle management\
-   See how MinIO Operator works similarly with its Tenant CRD

------------------------------------------------------------------------

## 📌 **Pre‑requisites**

-   Minikube or any Kubernetes cluster\
-   Python 3.x\
-   kubectl installed

------------------------------------------------------------------------

# 📘 **What is an Operator?**

A **Kubernetes Operator** is a **custom controller** that:

-   Understands a custom application\
-   Uses Kubernetes **events + reconciliation loops**\
-   Automates complex tasks such as:
    -   Deployment\
    -   Scaling\
    -   Backup\
    -   Recovery\
    -   Upgrades

Operators rely on:

### 🧩 **CRDs (Custom Resource Definitions)**

Define **new Kubernetes APIs** --- e.g., `Tenant`, `AppConfig`.

### 🧩 **Custom Controllers**

Watch CRDs and ensure the **desired state == actual state**.

------------------------------------------------------------------------

# 🧩 **Step 1: Start Kubernetes Cluster**

Start Minikube:

``` bash
minikube start
```

------------------------------------------------------------------------

# 🧩 **Step 2: Create a Custom Resource Definition (CRD)**

Create `appconfig-crd.yaml`:

``` yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: appconfigs.mycompany.com
spec:
  group: mycompany.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                appName:
                  type: string
                replicas:
                  type: integer
  scope: Namespaced
  names:
    plural: appconfigs
    singular: appconfig
    kind: AppConfig
    shortNames:
    - appcfg
```

### ✔ Apply CRD:

``` bash
kubectl apply -f appconfig-crd.yaml
```

### ✔ Verify:

``` bash
kubectl get crds
```

------------------------------------------------------------------------

# 🧩 **Step 3: Create a Custom Resource**

Create `appconfig.yaml`:

``` yaml
apiVersion: mycompany.com/v1
kind: AppConfig
metadata:
  name: myapp-config
spec:
  appName: MyApp
  replicas: 3
```

Apply:

``` bash
kubectl apply -f appconfig.yaml
```

Verify:

``` bash
kubectl get appconfigs
```

------------------------------------------------------------------------

# 🧩 **Step 4: Create the Operator Using Python (Kopf)**

## 1️⃣ Install dependencies

``` bash
pip install kopf kubernetes
```

------------------------------------------------------------------------

## 2️⃣ Create `operator.py`

``` python
import kopf
import kubernetes.client
from kubernetes.client.rest import ApiException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CREATE EVENT
@kopf.on.create('mycompany.com', 'v1', 'appconfigs')
def create_fn(spec, name, namespace, **kwargs):
    app_name = spec.get('appName', 'defaultapp').lower()
    replicas = spec.get('replicas', 1)

    deployment = {
        "apiVersion": "apps/v1",
        "kind": "Deployment",
        "metadata": {"name": name, "namespace": namespace},
        "spec": {
            "replicas": replicas,
            "selector": {"matchLabels": {"app": name}},
            "template": {
                "metadata": {"labels": {"app": name}},
                "spec": {
                    "containers": [
                        {"name": app_name, "image": "nginx"}
                    ]
                },
            },
        },
    }

    api = kubernetes.client.AppsV1Api()
    try:
        api.create_namespaced_deployment(namespace=namespace, body=deployment)
        logger.info(f"Deployment '{name}' created with {replicas} replicas for '{app_name}'")
        return {'message': f"Deployment '{name}' created"}
    except ApiException as e:
        logger.error(f"Failed to create Deployment: {e}")
        raise kopf.PermanentError(str(e))


# UPDATE EVENT
@kopf.on.update('mycompany.com', 'v1', 'appconfigs')
def update_fn(spec, name, namespace, **kwargs):
    replicas = spec.get('replicas', 1)

    deployment_patch = {"spec": {"replicas": replicas}}

    api = kubernetes.client.AppsV1Api()
    try:
        api.patch_namespaced_deployment(name=name, namespace=namespace, body=deployment_patch)
        logger.info(f"Deployment '{name}' updated to {replicas} replicas")
        return {'message': "Updated"}
    except ApiException as e:
        logger.error(f"Failed to update deployment: {e}")
        raise kopf.PermanentError(str(e))


# DELETE EVENT
@kopf.on.delete('mycompany.com', 'v1', 'appconfigs')
def delete_fn(name, namespace, **kwargs):
    api = kubernetes.client.AppsV1Api()
    try:
        api.delete_namespaced_deployment(name=name, namespace=namespace)
        logger.info(f"Deployment '{name}' deleted")
    except ApiException as e:
        if e.status != 404:
            raise kopf.PermanentError(str(e))
```

------------------------------------------------------------------------

## 3️⃣ Run the Operator

``` bash
kopf run operator.py
```

Operator now listens for:

-   create events\
-   update events\
-   delete events

------------------------------------------------------------------------

# 🧩 **Step 5: Test the Operator**

### ✔ Verify Deployment Creation

``` bash
kubectl get deployments
```

### ✔ Update the Custom Resource

Modify `appconfig.yaml`:

``` yaml
spec:
  replicas: 5
```

Apply:

``` bash
kubectl apply -f appconfig.yaml
```

Check:

``` bash
kubectl get deployments
```

### ✔ Delete Custom Resource

``` bash
kubectl delete -f appconfig.yaml
```

Check:

``` bash
kubectl get deployments
```

------------------------------------------------------------------------

# 🧹 **Step 6: Clean Up**

``` bash
kubectl delete crd appconfigs.mycompany.com
```

------------------------------------------------------------------------

# 🎉 **Conclusion**

In this lab, you:

✔ Created a **CRD**\
✔ Built a **custom Operator**\
✔ Handled create/update/delete events\
✔ Automated a Deployment lifecycle\
✔ Learned how MinIO Operator works internally
