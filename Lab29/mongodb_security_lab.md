
# MongoDB SecurityContext Comparison Lab  
### **Secure vs Insecure MongoDB Deployments**  

---

# 📌 **Lab Objective**
You will deploy **two MongoDB applications**:

| Deployment | Security Hardening | Purpose |
|-----------|--------------------|---------|
| **mongo-insecure** | ❌ No security context | Baseline behavior |
| **mongo-secure** | ✅ SecurityContext applied | Demonstrate isolation & enforcement |

Then you will test each security setting and compare the results side-by-side.

---

# 🧩 **1. YAML: Insecure MongoDB Deployment**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongo-insecure
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mongo-insecure
  template:
    metadata:
      labels:
        app: mongo-insecure
    spec:
      containers:
      - name: mongo
        image: mongo:5.0
        ports:
        - containerPort: 27017
        volumeMounts:
          - mountPath: /data/db
            name: db
      volumes:
      - name: db
        emptyDir: {}
```

Apply:

```
kubectl apply -f mongo-insecure.yaml
```

---

# 🛡️ **2. YAML: Secure MongoDB Deployment**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongo-secure
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mongo-secure
  template:
    metadata:
      labels:
        app: mongo-secure
    spec:
      securityContext:
        runAsUser: 999
        runAsGroup: 999
        fsGroup: 999
        seccompProfile:
          type: RuntimeDefault
      containers:
      - name: mongo
        image: mongo:5.0
        ports:
        - containerPort: 27017
        securityContext:
          runAsNonRoot: true
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: false
          capabilities:
            drop:
              - ALL
        volumeMounts:
          - mountPath: /data/db
            name: db
      volumes:
      - name: db
        emptyDir: {}
```

Apply:

```
kubectl apply -f mongo-secure.yaml
```

---

# 🔍 **3. Identify Pods**

```
kubectl get pods -l app=mongo-secure
kubectl get pods -l app=mongo-insecure
```

Store pod names:

- `mongo-secure-pod`
- `mongo-insecure-pod`

---

# 🧪 **4. LAB TESTING — Side-by-Side Comparisons**

---

## ✅ **4.1 Test: runAsUser & runAsGroup**

### Run:
```
kubectl exec -it mongo-insecure-pod -- id
kubectl exec -it mongo-secure-pod -- id
```

| Deployment | Output | Meaning |
|-----------|--------|---------|
| insecure | `uid=0(root)` | Runs as **root** → dangerous |
| secure | `uid=999 gid=999` | Runs as **non-root** |

---

## ✅ **4.2 Test: runAsNonRoot**

### Run:
```
kubectl exec -it mongo-secure-pod -- bash 
su
```

| Deployment | Output | Meaning |
|-----------|--------|---------|
| insecure | Works | Container can impersonate root |
| secure  | will ask for password

---


## ✅ **4.5 Test: allowPrivilegeEscalation**

### Run:
```
kubectl exec -it mongo-secure-pod -- cat /proc/1/status | grep CapPrm
kubectl exec -it mongo-insecure-pod -- cat /proc/1/status | grep CapPrm
```

| Deployment | Output |
|-----------|--------|
| insecure | `CapPrm` shows elevated caps | Can escalate |
| secure | `0000000000000000` | No escalation |

---

## ✅ **4.6 Test: Seccomp (RuntimeDefault)**
🎯 WHAT IS SECCOMP?

SECCOMP = Secure Computing Mode
It is a Linux kernel feature that:

✔ Restricts which system calls a container can use
✔ Prevents dangerous operations (e.g., mount, ptrace, reboot, setns, etc.)
✔ Acts as a firewall for syscalls
✔ Protects against container escape vulnerabilities

It is one of the strongest security layers in containers.


### Run:
```
kubectl exec -it mongo-secure-pod -- cat /proc/1/status | grep Seccomp
```

| Deployment | Output |
|-----------|--------|
| insecure | `Seccomp: 0` | No syscall filtering |
| secure | `Seccomp: 2` | 🔒 Seccomp Filtering is fully enforced |

---

## ✅ **4.7 Test: readOnlyRootFilesystem**

### Run:
```
kubectl exec -it mongo-secure-pod -- touch /testfile
kubectl exec -it mongo-insecure-pod -- touch /testfile
```

| Deployment | Result |
|-----------|--------|
| insecure | File created | Writable rootFS (unsafe) |
| secure | ❌ Permission denied | Protected filesystem |

---


---

# 🎉 **End of Lab**

This lab clearly demonstrates the difference between **default insecure containers** vs **secure, production-ready workloads**.



