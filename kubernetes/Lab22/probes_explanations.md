# 🧪 MongoDB Probes --- What Happens When They Fail?

## 1️⃣ **Startup Probe Fails**

### 👉 Meaning

MongoDB did not fully start within the allowed time (e.g., 5 minutes).

### 👉 What Kubernetes does?

-   Keeps retrying the startup probe\
-   **Does NOT restart the container**\
-   **Liveness & readiness probes stay disabled** until startup probe
    succeeds

### 👉 If it keeps failing beyond threshold?

Kubernetes **kills the container and restarts it** (CrashLoopBackOff).

------------------------------------------------------------------------

## 2️⃣ **Readiness Probe Fails**

### 👉 Meaning

MongoDB is running but **NOT ready to accept traffic**.

### 👉 What Kubernetes does?

-   **Removes the pod from service endpoints**\
-   No new connections will be routed to this pod\
-   Pod stays **alive**, NOT restarted

------------------------------------------------------------------------

## 3️⃣ **Liveness Probe Fails**

### 👉 Meaning

MongoDB is **unresponsive** or internal engine is stuck.

### 👉 What Kubernetes does?

-   **Kills the container**\
-   **Restarts it automatically** (self-healing)

------------------------------------------------------------------------

# 🔥 Why Same Command but Different Actions?

MongoDB uses the same internal command:

    db.adminCommand("ping")

But Kubernetes interprets **each probe type differently**:

  -------------------------------------------------------------------------
  Probe Type           Purpose                     What Failure Means
  -------------------- --------------------------- ------------------------
  **startupProbe**     Allow long boot time        Restart only after long
                                                   delay

  **readinessProbe**   Traffic control             Temporarily remove pod
                                                   from service

  **livenessProbe**    Crash detection             Restart container
                                                   immediately
                                                   
  -------------------------------------------------------------------------

------------------------------------------------------------------------

# 🧠 Analogy --- MongoDB as a Shop

### **Startup Probe**

"Is the shopkeeper awake yet?\
If not, don't force him to open --- wait."

### **Readiness Probe**

"Shop is open, but shelves are not ready.\
Don't send customers inside yet."

### **Liveness Probe**

"Shopkeeper fainted or frozen.\
Wake him up (restart)."

------------------------------------------------------------------------

### 💡 Summary

The **question asked is the same**:\
\> "Are you okay?"

But the **action taken** depends on **which probe is asking**.
