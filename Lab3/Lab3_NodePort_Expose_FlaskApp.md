
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

## ☘️ Step 1: Run the Flask APP Replica Set
Create the same replica set again with 3 replicas as we have explored in last lab.

```bash
cd ~/swift_training/Lab3
kubecl apply -f flask_replicaset.yaml
```


## ☘️ Step 1: Explore NodePort YAML File

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

## ☘️ Step 2: Deploy the NodePort Service

```bash
cd Lab3
kubectl apply -f flask_nodeport.yaml
```

---

## ☘️ Step 3: Verify the Service

```bash
kubectl get svc flask-nodeport
```

You should see:

```
flask-nodeport   NodePort   <cluster-ip>   <none>   5000:30000/TCP   1m
```

---


## ☘️ Step 6: Test Using Port Forwarding 


```bash
kubectl port-forward service/flask-nodeport 8080:5000
```

Now run curl command to test the service:

```
curl http://localhost:8080
```

---

## ☘️ Step 7: Cleanup

```bash
kubectl delete svc flask-nodeport
```

---

## ✅ Conclusion

In this lab, you:

- Exposed your Flask app using a NodePort on port 30000
- Retrieved Minikube IP to access the service externally
- Used `kubectl port-forward` for local access
- Verified that the application is accessible via browser

---

🎉 **Congratulations**, your service is now exposed and accessible!  
✨ **END OF LAB** ✨
