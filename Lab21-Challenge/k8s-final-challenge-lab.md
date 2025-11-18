# 🚀 Kubernetes FINAL CHALLENGE LAB  
### **NodeJS Frontend + MongoDB Backend – Production-Grade Deployment**

This challenge validates your understanding of real-world Kubernetes concepts such as namespaces, affinity, taints, PDB, HPA, RBAC, and Helm charts.  
You already have working NodeJS + MongoDB YAML files—now extend them to production‑ready K8s components.

---

# 🧩 CHALLENGE PART 1 — Namespace Design

Create two namespaces:

```
frontend
database
```

Component placement:

| Component | Namespace |
|----------|-----------|
| NodeJS Frontend | frontend |
| MongoDB Database | database |

Update YAML manifests using:

```yaml
metadata:
  namespace: frontend
```
or:
```yaml
metadata:
  namespace: database
```

---

# 🧩 CHALLENGE PART 2 — Add Resource Requests & Limits

Apply below resource limits to the **NodeJS frontend deployment**:

```yaml
resources:
  requests:
    cpu: 100m
    memory: 256Mi
  limits:
    cpu: 300m
    memory: 512Mi
```

---

# 🧩 CHALLENGE PART 3 — Node Affinity (MongoDB)

MongoDB must run **only** on nodes labeled:

```
node-type=database
```

### Step 1 — Label the node:
```
kubectl label nodes minikube-m02 node-type=database
```

### Step 2 — Add affinity to MongoDB deployment:

```yaml
affinity:
  nodeAffinity:
    requiredDuringSchedulingIgnoredDuringExecution:
      nodeSelectorTerms:
      - matchExpressions:
        - key: node-type
          operator: In
          values:
          - database
```

Verify MongoDB pod runs ONLY on `minikube-m02`.

---

# 🧩 CHALLENGE PART 4 — Taints and Tolerations

### Step 1 — Apply taint:

```
kubectl taint nodes minikube-m02 db=true:NoSchedule
```

### Step 2 — Add toleration in MongoDB deployment:

```yaml
tolerations:
- key: "db"
  operator: "Equal"
  value: "true"
  effect: "NoSchedule"
```

MongoDB must still schedule successfully.

---

# 🧩 CHALLENGE PART 5 — Pod Disruption Budget (PDB)

Create a PDB for the **NodeJS Frontend**:

```yaml
maxUnavailable: 1
```

This ensures at least one frontend pod is always available during voluntary evictions.

---

# 🧩 CHALLENGE PART 6 — Horizontal Pod Autoscaler (HPA)

Create an HPA for NodeJS frontend:

```
minReplicas: 2
maxReplicas: 6
targetCPUUtilization: 50%
```

Either use:

```
kubectl autoscale deployment node-frontend --cpu-percent=50 --min=2 --max=6
```

OR YAML.

---

# 🧩 CHALLENGE PART 7 — RBAC

Create user:

```
student-user
```

### User Permissions:

| Action | Namespace | Allowed? |
|--------|-----------|----------|
| get pods | frontend | YES |
| get pods | database | NO |
| delete pods | any | NO |

### Required:

1. Create a **Role** in `frontend` namespace:
   ```
   verbs: ["get", "list"]
   resources: ["pods"]
   ```
2. Create a **RoleBinding** binding **student-user**.
3. Validate:

```
kubectl auth can-i get pods -n frontend --as student-user
kubectl auth can-i get pods -n database --as student-user
kubectl auth can-i delete pods --as student-user
```

---

# 🧩 CHALLENGE PART 9 — Helm Chart

You must build a complete Helm chart:

```
helm create myhelmchart
```

Modify directory structure:

```
myhelmchart/
  Chart.yaml
  values.yaml
  templates/
    frontend-deployment.yaml
    frontend-service.yaml
    mongodb-deployment.yaml
    mongodb-service.yaml
    mongodb-pvc.yaml
    ingress.yaml
    pdb.yaml
    hpa.yaml
    rbac.yaml
```

Use template variables such as:

```yaml
{{ .Values.frontend.image }}
{{ .Values.frontend.replicaCount }}
{{ .Release.Name }}
```

---

# 🧩 CHALLENGE PART 10 — Install the Helm Chart

Install:

```
helm install myhelm ./myhelmchart
```

Upgrade:

```
helm upgrade myhelm ./myhelmchart
```

Rollback:

```
helm rollback myhelm 1
```

Uninstall:

```
helm uninstall myhelm
```

---

# ✅ FINAL VALIDATION CHECKLIST

validate **all** points below to pass the challenge.

---

## ✔ Namespace Validation
- NodeJS pods in **frontend**
- MongoDB pods in **database**

---

## ✔ Resource Limits
Verify using:

```
kubectl get pod -n frontend -o jsonpath='{..resources}'
```

---

## ✔ Node Affinity (MongoDB)
- MongoDB pod **must run only** on `minikube-m02`
- Verified via:

```
kubectl get pods -o wide -n database
```

---

## ✔ Taints & Tolerations
- MongoDB schedules despite taint
- Other pods **must NOT** schedule on tainted node

---

## ✔ PDB
Check:

```
kubectl get pdb -n frontend
```

Should show:

```
maxUnavailable = 1
```

---

## ✔ HPA
Verify:

```
kubectl get hpa -n frontend
```

HPA must scale pods under CPU load.

---

## ✔ RBAC
Verify:

```
kubectl auth can-i get pods -n frontend --as student-user   # YES
kubectl auth can-i get pods -n database --as student-user   # NO
kubectl auth can-i delete pods --as student-user            # NO
```

---

## ✔ Helm Chart
- Templates render successfully:

```
helm template myhelm ./myhelmchart
```

- Helm install runs without error:

```
helm install myhelm ./myhelmchart
```

---

## ✔ Application Functionality
- Frontend reachable via NodePort
- Submissions are stored in MongoDB

---

🎉 **Congratulations! This is your full Kubernetes Production-Grade Challenge Lab.**
