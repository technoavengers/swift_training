
# MongoDB SecurityContext Comparison Lab  
### **Secure vs Insecure MongoDB Deployments**  
Downloadable Lab Document

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
kubectl exec -it mongo-secure-pod -- bash -c "id -u root"
```

| Deployment | Output | Meaning |
|-----------|--------|---------|
| insecure | Works | Container can impersonate root |
| secure | Error / denied | Root access blocked |

---

## ✅ **4.3 Test: fsGroup**

### Run:
```
kubectl exec -it mongo-secure-pod -- ls -ld /data/db
```

| Deployment | Output | Meaning |
|-----------|--------|---------|
| insecure | Owned by root → may fail writing | PVC may block MongoDB |
| secure | Owned by 999:999 | MongoDB gains write access |

---

## ✅ **4.4 Test: Capability Dropping**

### Run:
```
kubectl exec -it mongo-secure-pod -- capsh --print 2>/dev/null
```

| Deployment | Output |
|-----------|---------|
| insecure | MANY capabilities enabled |
| secure | EMPTY bounding set |

Meaning: secure pod cannot do privileged OS actions.

---

## ✅ **4.5 Test: allowPrivilegeEscalation**

### Run:
```
kubectl exec -it mongo-secure-pod -- cat /proc/1/status | grep CapPrm
```

| Deployment | Output |
|-----------|--------|
| insecure | `CapPrm` shows elevated caps | Can escalate |
| secure | `0000000000000000` | No escalation |

---

## ✅ **4.6 Test: Seccomp (RuntimeDefault)**

### Run:
```
kubectl exec -it mongo-secure-pod -- cat /proc/1/status | grep Seccomp
```

| Deployment | Output |
|-----------|--------|
| insecure | `Seccomp: 0` | No syscall filtering |
| secure | `Seccomp: 2` | Syscall filtering active |

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

# 🏁 **5. Final Comparison Table**

| Feature | Insecure Pod | Secure Pod | Purpose |
|--------|--------------|------------|---------|
| runAsUser | root | 999 | Prevent root access |
| runAsGroup | root | 999 | Privilege isolation |
| fsGroup | none | 999 | PVC read/write fix |
| runAsNonRoot | No | Yes | Block root execution |
| allowPrivilegeEscalation | Yes | No | Disable SUID privilege |
| drop all capabilities | No | Yes | Remove OS privileges |
| seccomp | off | on | Syscall filtering |
| readOnlyRootFilesystem | No | Yes | Protect FS |

---

# 🎉 **End of Lab**

This lab clearly demonstrates the difference between **default insecure containers** vs **secure, production-ready workloads**.

---

# 📁 **Download This File**
The `.md` file is generated below.

