
# ✅ Lab 3: Expose Flask App using NodePort and Port Forwarding

**Time:** 15–20 Minutes

---

## 🧾 Lab Summary

In this lab, you will expose your Python-Flask application running on Kubernetes using a **NodePort** service. This allows you to access the app externally using a specific port on the Node. You will also test it using `kubectl port-forward` for local access.

---

## 🎯 Objectives

- 🌐 Create a NodePort service to expose the Flask app  
- 🚪 Access the app via external IP and port 30000  
- 🧪 Use `kubectl port-forward` as an alternative for testing  

---

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

## ☘️ Step 1: Run the Flask APP Replica Set
Create the same replica set again with 3 replicas as we have explored in last lab.

```bash
cd ~/swift_training/Lab3
kubectl apply -f flask_replicaset.yaml
```


## ☘️ Step 2: Explore NodePort YAML File

In `Lab3`, open the file `flask_nodeport_service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-nodeport
spec:
  type: NodePort
  selector:
    app: flask
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
      nodePort: 30000
```

---

## ☘️ Step 3: Deploy the NodePort Service

```bash
kubectl apply -f flask_nodeport_service.yaml
```

---

## ☘️ Step 4: Verify the Service

```bash
kubectl get svc flask-nodeport
```

You should see:

```
flask-nodeport   NodePort   <cluster-ip>   <none>   5000:30000/TCP   1m
```

---


## ☘️ Step 5: Access the Flask App

### 🔍 To get the EC2 public IP address:
Run the following command in terminal and it will provide you public IP address of EC2 machine you are using:
```bash
curl http://169.254.169.254/latest/meta-data/public-ipv4
```
### 🔍 Open your local browser and go to:
Replace the EC2-Address that you have recieved in last command in below URL

  👉 `http://<your-ec2-public-ip>:30000`


## ☘️ Step 6: Let's create a LoadBalancer Service

```bash
kubectl apply -f flask_loadbalancer_service.yaml
```

---

## ☘️ Step 7: Verify the Service

```bash
kubectl get svc 
```

## ☘️ Step 8: Access the Flask App

Use the External IP and nodePort provided in loadbalancer svc

```bash
curl http://external-ip:nodePort
```

---

## ☘️ Step 7: Cleanup

```bash
kubectl delete svc flask-nodeport
kubectl delete rs flask-replicaset
```

---

## ✅ Conclusion

In this lab, you:

- Exposed your Flask app using a NodePort on port 30000
- Used `kubectl port-forward` for local access
- Verified that the application is accessible via service

---

🎉 **Congratulations**, you have completed this lab
✨ **END OF LAB** ✨
