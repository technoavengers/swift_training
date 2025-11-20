# NetworkPolicy Demo in K3s

## Step 1: Create Namespaces
```bash
kubectl create ns frontend
kubectl create ns backend
```

## Step 2: Deploy Backend
```bash
kubectl -n backend run backend-pod --image=nginx --port=80
kubectl -n backend expose pod backend-pod --port=80
```

## Step 3: Deploy Test Pod
```bash
kubectl -n frontend run testpod --image=busybox --command -- sleep 3600
```

## Step 4: Test Connectivity Before Policy
```bash
kubectl -n frontend exec -it testpod -- wget -qO- http://backend-pod.backend.svc.cluster.local
```

## Step 5: Deny-All NetworkPolicy
Create `deny-all.yaml`:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: backend
spec:
  podSelector: {}
  policyTypes:
  - Ingress
```
Apply:
```bash
kubectl apply -f deny-all.yaml
```

## Step 6: Test Connectivity After Policy
```bash
kubectl -n frontend exec -it testpod -- wget -qO- http://backend-pod.backend.svc.cluster.local
```

## Step 7: Allow Frontend Namespace
Create `allow-frontend.yaml`:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend
  namespace: backend
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          access: "frontend"
```

Label namespace:
```bash
kubectl label ns frontend access=frontend
```

Apply:
```bash
kubectl apply -f allow-frontend.yaml
```

## Step 8: Test Again
```bash
kubectl -n frontend exec -it testpod -- wget -qO- http://backend-pod.backend.svc.cluster.local
```

## Step 9: Test From Another Namespace
```bash
kubectl run test2 --rm -it --image=busybox --restart=Never -- wget -qO- http://backend-pod.backend.svc.cluster.local
```
