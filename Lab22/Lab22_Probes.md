### Run Frontend

cd ~/swift_training/Lab22/Frontedn
kubectl apply -f app-configmap.yaml
kubectl apply -f nodejs-app-deployment.yaml


### Checks Pods
kubectl get pod
kubectl describe pod <pod-name>

Did you noticed the error for readiness probe, it is because mongodb is not yet running

Check the APplicaation code
cd ~/swift_training/Application/index.js

What code is written for /ready endpoint where readiness probe is hitting.


## Run Mongo
cd ~/swift_training/Lab22/Backend
kubectl apply -f mongo-pvc.yaml
kubectl apply -f mongodb-deployment.yaml
kubectl apply -f mongodb-service.yaml

## Restart nodejs

kubectl rollout restart deploy nodeapp

## check pod again

kubectl get pod

