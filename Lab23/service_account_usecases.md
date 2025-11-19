🥇 1. Prometheus Service Discovery

Prometheus MUST discover Pods automatically so it knows what to scrape.

It does this by calling:

/api/v1/pods
/api/v1/services
/api/v1/endpoints


Prometheus absolutely requires:
- A service account
- RBAC → list/watch pods, endpoints, services
- The token is used by Prometheus to authenticate to the API server


🥉 2. CI/CD System (Argo Workflows / Tekton / Jenkins K8s Plugin)

Your CI/CD system runs inside Kubernetes and needs to:

- Create Pods
- Create Jobs
- Watch logs
- Delete pods after execution

Example: Argo Workflows

It interacts with Kubernetes APIs like:

POST /api/v1/namespaces/.../pods
POST /apis/batch/v1/namespaces/.../jobs

✔ Requires RBAC like:
resources: ["pods", "pods/log", "jobs"]
verbs: ["create", "delete", "get", "watch"]


🟩 EFK / ELK Example: Fluentd or Fluent-bit MUST use a Service Account

When You deploy: 
- Fluentd / Fluent-bit (daemonset)
- Elasticsearch
- Kibana

Fluentd’s job is to:

- read logs from every node
- detect new Pods
- extract pod labels/annotations
- enrich logs
- send logs to Elasticsearch

To do these correctly, Fluentd must communicate with the Kubernetes API.