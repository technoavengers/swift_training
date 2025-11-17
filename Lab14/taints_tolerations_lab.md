# Kubernetes Lab: Taints & Tolerations (Complete Practical Lab)

## 🕒 Estimated Time
25–30 minutes

## 🎯 Objective
In this lab, you will learn:

- What taints are and how to apply them
- What tolerations are and how they work
- How NoSchedule and NoExecute behave
- How to test taints using real pods
- How to verify and remove taints

This lab works on **Minikube multi-node** or any multi-node Kubernetes cluster.

---

# 🧠 1. Concept Overview

## Taints
Applied on **nodes** to repel pods unless they tolerate the taint.

Format:
```
key=value:effect
```

Effects:
- **NoSchedule** → Pod will not schedule
- **PreferNoSchedule** → Scheduler avoids this node
- **NoExecute** → Pods without toleration are evicted

## Tolerations
Applied on **pods** to allow scheduling onto tainted nodes.

---

# 🪜 2. Step 1 — Verify Nodes

```bash
kubectl get nodes -o wide
```

Example output:
```
minikube
minikube-m02
minikube-m03
```

We will taint **minikube-m02**.

---

# 🧪 3. Step 2 — Apply NoSchedule Taint

```bash
kubectl taint nodes minikube-m02 env=dev:NoSchedule
```

Verify:
```bash
kubectl describe node minikube-m02 | grep Taints
```

Expected:
```
Taints: env=dev:NoSchedule
```

---

# 🟥 4. Step 3 — Test Pod WITHOUT Toleration (NoSchedule)

Create file: **pod-no-toleration.yaml**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-no-toleration
spec:
  containers:
    - name: nginx
      image: nginx
```

Apply:

```bash
kubectl apply -f pod-no-toleration.yaml
kubectl get pod -o wide
```

Expected behavior:
- Pod **will NOT** schedule on `minikube-m02`
- Pod schedules on another node or stays Pending

Check:

```bash
kubectl describe pod pod-no-toleration
```

Look for:

```
node(s) had taint {env: dev}, that the pod didn't tolerate
```

---

# 🟩 5. Step 4 — Test Pod WITH Toleration (NoSchedule)

Create file: **pod-with-toleration.yaml**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-with-toleration
spec:
  tolerations:
    - key: "env"
      operator: "Equal"
      value: "dev"
      effect: "NoSchedule"
  containers:
    - name: nginx
      image: nginx
```

Apply:

```bash
kubectl apply -f pod-with-toleration.yaml
kubectl get pod -o wide
```

Expected:
- Pod **CAN** run on `minikube-m02` because of toleration

---

# ⚡ 6. Step 5 — Apply NoExecute Taint

Overwrite previous taint:

```bash
kubectl taint nodes minikube-m02 env=dev:NoExecute --overwrite
```

Verify:

```bash
kubectl describe node minikube-m02 | grep Taints
```

Expected:
```
env=dev:NoExecute
```

**NoExecute behavior:**
- Pods without toleration → **Evicted**
- Pods with toleration → Stay until tolerationSeconds expires

---

# 🟦 7. Step 6 — Pod With NoExecute Toleration (Timed Eviction)

Create file: **pod-noexecute.yaml**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-noexecute
spec:
  tolerations:
    - key: "env"
      operator: "Equal"
      value: "dev"
      effect: "NoExecute"
      tolerationSeconds: 20
  containers:
    - name: nginx
      image: nginx
```

Apply:

```bash
kubectl apply -f pod-noexecute.yaml
```

Expected:
- Pod schedules on `minikube-m02`
- After **20 seconds**, pod is **evicted**

Check events:
```bash
kubectl describe pod pod-noexecute | grep -i evict
```

---

# 🧹 8. Step 7 — Remove All Taints

```bash
kubectl taint nodes minikube-m02 env-
```

Verify:
```bash
kubectl describe node minikube-m02 | grep Taints
```

Expected:
```
Taints: <none>
```

---

# 🧽 9. Step 8 — Cleanup Pods

```bash
kubectl delete pod pod-no-toleration
kubectl delete pod pod-with-toleration
kubectl delete pod pod-noexecute
```

---

# 🎉 Lab Summary

You learned:

- What taints and tolerations do
- How NoSchedule prevents pod placement
- How NoExecute evicts existing pods
- How tolerations allow pods onto tainted nodes
- How to test both effects using real pods
- How to remove taints and restore the node

This completes the Taints & Tolerations Lab!
