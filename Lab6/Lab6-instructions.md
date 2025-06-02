# Lab: Persist PostgreSQL Data Using PVC with Flask App on K3s

## Step-by-step Instructions

## ☘️ Pre-requiste : Setup K3s Cluster
1. Stop Minikube
```bash
minikube stop
minikube delete
```


1. Run below to start k3s cluster

```bash
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable=traefik" sh -
sudo cp /etc/rancher/k3s/k3s.yaml $HOME/k3s.yaml
sudo chown $USER:$USER $HOME/k3s.yaml
export KUBECONFIG=$HOME/k3s.yaml
```

### Step 1: Check existing storage classes
```bash
kubectl get storageclasses
```

### Step 2: Create PVC with Storage Class

```bash
kubectl apply -f postgres-pv-pvc.yaml
```

### Step 3: Check  PVC
```bash
kubectl get pvc
```

### Step 4: Deploy PostgreSQL with PVC

Explore postgres-deployment.yaml and check how PVc is added into deployment

Now apply postgres deployment

```bash
kubectl apply -f postgres-deployment.yaml

Expose it via Service 

```
```bash
kubectl apply -f postgres-service.yaml
```

### Step 3: Deploy Flask App and Expose it via Service

We have not done any changes in flask deployment and flask service, it is same as in last lab.

Explore flask-deployment.yaml and flask-service.yaml if you want

```bash
kubectl apply -f flask-deployment.yaml
kubectl apply -f flask-service.yaml
```

### 🔍 To get the EC2 public IP address:
Run the following command in terminal and it will provide you public IP address of EC2 machine you are using:
```bash
curl http://169.254.169.254/latest/meta-data/public-ipv4
```
### 🔍 Open your local browser and go to:
Replace the EC2-Address that you have recieved in last command in below URL

  👉 `http://<your-ec2-public-ip>:30000`

---

## ☘️ Step 10: Test the App

- Fill in a **username** and **age**
- Click **Submit**
- You should see:  
  `Thank you, <name>! Your age <age> has been recorded.`

---

### Step 11: Test Data Persistence

```bash
kubectl delete pod -l app=postgres
```

Then access the app again and check if previous data persists.

👉 `http://<your-ec2-public-ip>:30000`
