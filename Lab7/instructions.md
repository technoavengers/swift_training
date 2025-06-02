# Lab: Use ConfigMap for PostgreSQL Credentials in Flask App

## 🧩 Objective

You will:
- Create a ConfigMap to store PostgreSQL connection details.
- Inject values into PostgreSQL and Flask pods.
- Deploy both components and test data submission.

---

## 🚀 Step-by-Step Guide

### Step 1: Apply ConfigMap

```bash
kubectl apply -f configmap.yaml
```

### Step 1: Create Secret for Postgres Credentials
```bash
kubectl create secret generic postgres-secret \
  --from-literal=username=flaskuser \
  --from-literal=password=flaskpass
```

### Step 2: Deploy PostgreSQL

```bash
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
```

### Step 3: Deploy Flask App

```bash
kubectl apply -f flask-deployment.yaml
kubectl apply -f flask-service.yaml
```

### Step 4: Test the App

Get your EC2 public IP and access the app:

```bash
curl http://<your-ec2-public-ip>:30000
```

Fill out the form and ensure data is stored in PostgreSQL.

---

## 🧹 Cleanup

```bash
kubectl delete -f .
```
