
# ✅ Lab 13: Understanding PodDisruptionBudgets (PDB) and Horizontal Pod Autoscaler (HPA) in Kubernetes

🕒 **Estimated Time**: 25–30 minutes

---

## 🎯 Objective
This lab introduces two important Kubernetes features for availability and scalability: **PodDisruptionBudgets (PDB)** and **Horizontal Pod Autoscaler (HPA)**. You will learn to set a disruption budget to maintain high availability and apply autoscaling to scale pods based on CPU utilization.

---


#  PART 1- PodDisruptionBudget (PDB)
PDB ensures that a minimum number of Pods remain available during voluntary disruptions like node drains or rolling updates.

## ☘️ Setup: Start Minikube

Start minikube with 3 nodes
```bash
minikube start --nodes=3
```
Check nodes
```bash
kubectl get node
```

Since k3s and minikube both are running
Please check context, it should point to minikube as current (*)
```bash
kubectl config get-contexts
```


## ☘️ Step 1: Create a Deployment

```bash
kubectl create deployment web --image=nginx --replicas=3
```

## ☘️ Step 2: Check Pods Location

Check where are pods running?:

```bash
kubectl get pod -o wide
```

Did you noticed that pods are running on different minikube nodes


## ☘️ Step 3 : Create a PodDisruptionBudget

You have been provided with  file named `pdb.yaml` in Lab13 folder.

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: web-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: web
```
🔍 What This File Does
This PodDisruptionBudget (PDB) ensures that at least 2 pods with the label app: web are always available during any voluntary disruptions, such as:

- Node maintenance (kubectl drain)
- Rolling updates
- Cluster scaling

## ☘️ Step 4: Apply the PDB:

```bash
cd ~/swift_training/Lab13
kubectl apply -f pdb.yaml
```

## ☘️ Step 5: Check PDB status:

```bash
kubectl get pdb
```

## ☘️ Step 6: Simulate a Node Drain to Test PDB:
In Kubernetes, draining a node simulates a voluntary disruption by cordoning the node (preventing new pods from being scheduled) and evicting all the pods on that node. PDB will prevent more pods than the minAvailable number from being evicted.
– Drain the Node

```bash
kubectl drain minikube-m02 --ignore-daemonsets --delete-emptydir-data
```

Did you see pdb constraint message, if not yet keep moving

## ☘️ Step 7: Check pods location

After running the drain command, check the status of the pods and check where are they running?

```bash
kubectl get pods -o wide
```

## ☘️ Step 8: Drain Node
Let's drain another node
```bash
kubectl drain minikube-m03 --ignore-daemonsets --delete-emptydir-data
```
Did you see pdb constraint message now, which means it will not allow this node to go down unless 2 replicas are not available on some other node. After it is able to achive min 2 replicas on some other node, node can go down.


## ☘️ Step 9: Check Pods Location

After running the drain command, check the status of the pods and check where are they running?

```bash
kubectl get pods -o wide
```


## ☘️ Step 10: Uncordon the Node
After testing the node drain and PDB behavior, you can uncordon the node to allow scheduling again:

```bash
kubectl uncordon minikube-m02
kubectl uncordon minikube-m03
```

## ☘️ Step 11: Check Node status

```bash
kubectl get node
```

## ☘️ Step 12: Cleanup

```bash
kubectl delete -f .
kubectl delete deployment web
```

END OF PART-1