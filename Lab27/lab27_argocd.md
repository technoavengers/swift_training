## Use k3s
export KUBECONFIG=$HOME/k3s.yaml

## Create dev namespace
kubectl create namespace dev

### Install ArgoCD helm chart in argocd namespace
helm repo add argo https://argoproj.github.io/argo-helm
helm repo update
kubectl create namespace argocd


helm install argocd argo/argo-cd \
  -n argocd \
  --set server.service.type=NodePort \
  --set server.service.nodePortHttp=30000 \


## Access ArgoUI in browser
Check your Ec2 Ip address:
curl -s http://169.254.169.254/latest/meta-data/public-ipv4


Now Open Brower and try
EC2_address: 30000

Login to ARgoCD

## Use below Credentials
username-admin

## Get password by running below command
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d && echo

#### Create a Application
cd ~/ArgoCD
kubectl apply -f application.yaml
kubectl get application -n argocd

### Check Application on UI

### Check what has been deployed?
kubectl get all -n dev


