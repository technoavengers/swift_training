
# ✅ Lab 9: Installing Apache Cassandra on Kubernetes Using Helm

🕒 **Estimated Time**: 15–20 minutes

---

## 🎯 Objective
In this lab, we are going to install a Cassandra cluster on Kubernetes using the Bitnami Helm chart and verify the setup by accessing it via `cqlsh`.

---

## ☘️ Step 0: Explore the Cassandra Helm Chart
Before installing, explore the Helm chart configuration options, default values, and documentation provided by Bitnami:
👉 [Bitnami Cassandra Helm Chart on Artifact Hub](https://artifacthub.io/packages/helm/bitnami/cassandra)
---

You can also inspect default values used in the chart by downloading on local machine:

Make sure you are in Lab10 folder

```bash
cd Kubernetes_Dockers/Lab11
```

Let's download default values.yaml in Lab10 folder

```bash
helm show values oci://registry-1.docker.io/bitnamicharts/cassandra > default-values.yaml
```
Above command will create a default-values.yaml in your Lab10 folder, explore values.yaml file.


## ☘️ Step 1: Add the Bitnami Helm Repository

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```


---

## ☘️ Step 2: Install Cassandra using Helm

```bash
helm upgrade --install cassandra oci://registry-1.docker.io/bitnamicharts/cassandra --set replicaCount=1 --set resources.requests.memory=1Gi --set resources.requests.cpu=500m --set resources.limits.memory=2Gi --set resources.limits.cpu=1 --set persistence.size=1Gi --set volumePermissions.enabled=true --set volumePermissions.securityContext.runAsUser=0 --set dbUser.password=cassandra --set dbUser.forcePassword=true
```

---

## ☘️ Step 3: Verify the Cassandra Pod is Running

```bash
kubectl get pods
```

> ✅ Ensure that the Cassandra pod status shows `Running`.

---

## ☘️ Step 5: Connect to Cassandra using `cqlsh`

Connect to the pod

```bash
kubectl exec -it cassandra-0 -- bash
```

Inside Terminal

```bash
cd bin
cqlsh cassandra 9042 -u cassandra -p cassandra
```

---

## ☘️ Step 6: Create Keyspace and Table, Insert and Query Data

Inside `cqlsh`:

```sql
DESCRIBE KEYSPACES;

CREATE KEYSPACE demo WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

USE demo;

CREATE TABLE users (id UUID PRIMARY KEY, name TEXT, email TEXT);

INSERT INTO users (id, name, email) VALUES (uuid(), 'Navdeep', 'navdeep@example.com');

SELECT * FROM users;
```

---

## ✅ Conclusion

You have successfully deployed **Apache Cassandra** using **Helm** on **Kubernetes**, connected using `cqlsh`, and performed basic CQL operations such as creating a keyspace, table, and inserting/querying data.
