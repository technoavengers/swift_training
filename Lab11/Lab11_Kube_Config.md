✅ Lab: Understanding Kubeconfig & Switching Between Minikube and K3s

🕒 Estimated Time: 15–20 minutes

🎯 Objective

In this lab you will learn:

What a kubeconfig file is

How to list clusters, users, and contexts

How to switch between Minikube and K3s

How to merge multiple kubeconfig files

How to set default namespace inside a context

Perfect for developers running multiple clusters on the same laptop.

🔍 Step 1: View Your Current Kubeconfig

Kubeconfig is stored at:

~/.kube/config


View it:

kubectl config view


Pretty-format it:

kubectl config view --minify --flatten

🧩 Step 2: List All Clusters, Users, and Contexts
kubectl config get-clusters
kubectl config get-users
kubectl config get-contexts


Expected output (example):

CURRENT   NAME
*         minikube
          k3s

☸️ Step 3: Start Both Clusters
Start Minikube
minikube start

Start K3s (external machine or local)

If local K3s (binary install):

sudo systemctl start k3s


K3s stores its kubeconfig at:

/etc/rancher/k3s/k3s.yaml

🪄 Step 4: Import K3s Kubeconfig Into Your Main Config

K3s uses root-permission config, so copy it:

sudo cat /etc/rancher/k3s/k3s.yaml > ~/k3s.yaml


Fix the server URL inside k3s.yaml:

sed -i "s/127.0.0.1/$(hostname -I | awk '{print $1}')/g" ~/k3s.yaml


Now merge with your main kubeconfig:

export KUBECONFIG=~/.kube/config:~/k3s.yaml
kubectl config view --flatten > ~/.kube/config-merged
mv ~/.kube/config-merged ~/.kube/config


Now verify:

kubectl config get-contexts


You should see:

minikube

k3s

🔄 Step 5: Switch Between Clusters

Switch to Minikube:

kubectl config use-context minikube
kubectl get nodes


Switch to K3s:

kubectl config use-context k3s
kubectl get nodes

🧪 Step 6: Test Deployments on Each Cluster
Test on Minikube
kubectl config use-context minikube
kubectl create deployment nginx --image=nginx
kubectl get pods

Test on K3s
kubectl config use-context k3s
kubectl create deployment nginx --image=nginx
kubectl get pods

🎯 Step 7: View Current Context

To see which cluster you're connected to:

kubectl config current-context

🧭 Step 8: Set Default Namespace in a Context
Set for Minikube:
kubectl config set-context minikube --namespace=dev

Set for K3s:
kubectl config set-context k3s --namespace=qa


Check:

kubectl config view

🧹 Step 9: Clean Up

Switch to Minikube & delete test deployment:

kubectl config use-context minikube
kubectl delete deployment nginx


Switch to K3s & delete:

kubectl config use-context k3s
kubectl delete deployment nginx

🧠 What You Learned

You now understand:

✔ What kubeconfig is
✔ How to merge multiple kubeconfigs
✔ How to switch between Minikube & K3s
✔ How to view clusters, users, and contexts
✔ How to set default namespaces per contex