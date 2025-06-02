
# ✅ Lab 14: Managing Pod Placement Using Affinity and Anti-Affinity in Kubernetes

🕒 **Estimated Time**: 20 minutes

---

## 🎯 Lab Overview

This lab will help you understand how to configure **node affinity** and **pod affinity/anti-affinity** to control the placement of MinIO pods on specific nodes or to avoid scheduling them together based on labels.

---

## ☘️ Step 1: Set Up the Kubernetes Cluster

Start a Minikube cluster with 3 nodes:

```bash
minikube delete
minikube start --nodes 3
```

---

## ☘️ Step 2: Check the Nodes

```bash
kubectl get nodes
```

---

## ☘️ Step 3: Label One of Your Nodes

```bash
kubectl label nodes minikube node-type=storage-node
```

---

## ☘️ Step 4: MinIO StatefulSet with Node Affinity

Explore the YAML file `minio_statefulset_with_node_affinity.yaml` located in Lab13 folder and Focus on section representing affinity

```yaml
 affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: node-type
                operator: In
                values:
                - storage-node  # Use the node label you applied earlier
```



Apply the StatefulSet:

```bash
kubectl apply -f minio_statefulset_with_node_affinity.yaml
```

This YAML enforces scheduling MinIO pods **only on nodes labeled** `node-type=storage-node`.

---

## 🔍 Behavior

- **Hard Constraint**: Pods won't schedule unless a matching node exists.
- **Post-Scheduling**: If labels are removed later, the pod stays running.

---

## ☘️ Step 5: Check Pod Placement

```bash
kubectl get pod -o wide
```

Check that pods are scheduled only on nodes with the label `node-type=storage-node`.

---

## ☘️ Step 6: Label One More Node

```bash
kubectl label nodes minikube-m02 node-type=storage-node
```

---

## ☘️ Step 7: Add Pod Anti-Affinity

Explore the YAML `minio_statefulset_with_node_affinity_pod_antiaffinity.yaml` with pod anti-affinity and focus on section that defines pod anti-affinity:

```yaml
podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - minio
            topologyKey: "kubernetes.io/hostname"
```

## ☘️ Step 8: Delete the existing StatefulSet:


```bash
kubectl delete statefulset minio
```

## ☘️ Step 8: Create new StatefulSet:

New statefulSet has affinity for node but it also has pod anit-affinity

```bash
kubectl apply -f minio_statefulset_with_node_affinity_pod_antiaffinity.yaml
```

---

## 🔍 Explanation

### 🔹 Node Affinity
- Ensures pods are only scheduled on nodes with label `node-type=storage-node`
- Enforced during scheduling time

### 🔹 Pod Anti-Affinity
- Ensures **MinIO pods (app=minio)** are not scheduled on the same node
- Controlled using `topologyKey: kubernetes.io/hostname`
- Spreads pods across available nodes

---

## ✅ End of Lab

You now understand how to:
- Use **Node Affinity** to guide pod placement onto labeled nodes
- Use **Pod Anti-Affinity** to avoid co-scheduling similar pods
