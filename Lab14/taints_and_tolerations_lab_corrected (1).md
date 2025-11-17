
# Kubernetes Lab: Taints & Tolerations (Complete Practical Lab)

## 🕒 Estimated Time
25–30 minutes

## 🎯 Objective
In this lab, you will learn:
- What taints and tolerations are
- How NoSchedule works
- How NoExecute works
- How to test scheduling behavior using Kubernetes pods
- How to clean up and verify node status

This lab works on Minikube multi-node or any multi-node Kubernetes cluster.

---

# 1️⃣ Step 1 — Verify Your Nodes

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

# 2️⃣ Step 2 — Apply a NoSchedule Taint

```bash
kubectl taint nodes minikube-m02 env=dev:NoSchedule
```

Verify taint:
```bash
kubectl describe node minikube-m02 | grep Taints
```

Expected:
```
Taints: env=dev:NoSchedule
```

---

# 3️⃣ Step 3 — Pod WITHOUT Toleration (Should Fail on Tainted Node)

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

Apply pod:

```bash
kubectl apply -f pod-no-toleration.yaml
kubectl get pod -o wide
```

Expected behavior:
- Pod **will NOT** schedule on `minikube-m02`
- Pod schedules on another node or goes pending

Check:
```bash
kubectl describe pod pod-no-toleration
```

Look for:
```
node(s) had taint {env: dev}, that the pod didn't tolerate
```

---

# 4️⃣ Step 4 — Pod WITH Toleration (Should Work on Tainted Node)

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

Apply pod:

```bash
kubectl apply -f pod-with-toleration.yaml
kubectl get pod -o wide
```

Expected:
- Pod **CAN** run on `minikube-m02`

---

# 5️⃣ Step 5 — Apply NoExecute Taint (Eviction Test)

Overwrite taint:

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

Behavior:
- Pods without toleration → **evicted immediately**
- Pods with toleration → stay until tolerationSeconds

---

# 6️⃣ Step 6 — Pod With NoExecute Toleration (Timed Eviction)

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
- Pod schedules on tainted node
- After **20 seconds**, pod is **evicted**

Check events:
```bash
kubectl describe pod pod-noexecute | grep -i evict
```

---

# 7️⃣ Step 7 — Remove All Taints

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

# 8️⃣ Step 8 — Cleanup

```bash
kubectl delete pod pod-no-toleration
kubectl delete pod pod-with-toleration
kubectl delete pod pod-noexecute
```

---

# 🎉 Lab Completed

You now understand:
- How NoSchedule blocks pods
- How tolerations allow scheduled pods
- How NoExecute evicts pods
- How to work with real Kubernetes taint scenarios

This completes your Taints & Tolerations Lab!
