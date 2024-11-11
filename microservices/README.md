# AutoHub Application

# Test Local

# start customer-service
cd microservices/customer-service
sh ./start.sh

#  start api-gateway
cd microservices/api-gateway
sh ./start.sh

cd microservices/customer-service
python test.py

cd microservices/api-gateway/test
python customer-service-test.py


#minikube k8s testing
#Create images
cd microservices/customer-service
sh ./build.sh
cd latest/api-gateway
sh ./build.sh

#Setup minikube
#Deploy the services
minikube image load customer-svc:latest
minikube image load gateway-svc:latest
cd latest/deployment
kubectl apply -f deployment.yaml

minikube ip

curl http://<minikube ip>:<port-defined-in-the-deployement-file>/customers


# Local Deployemnt - Docker Desktop

#Build the docker images for all the microservices
#e.g. 
cd latest
# gateway-svc
sh api-gateway/build.sh
# auth-svc
sh auth-service/build.sh
# customer-svc
sh customer-service/build.sh
# vehicle-svc
sh vehicle-catalouge-service/build.sh
# booking-svc
sh booking-service/build.sh
# support-svc
sh support-service/build.sh
# rsa-svc
sh rsa-service/build.sh
# feedback-svc
sh feedback-service/build.sh

# Deploy the images to local K8S cluster
# Move to deployment dir
* cd deployemnt
# Start the deployments 
* kubectl apply -f .
# Delete the deployments
* kubectl delete -f .
# check the status of the deployments and services 
* kubectl get pods
* kubectl get services
* kubectl get deployments



# ArgoCD

kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

cd latest/deployment
kubectl apply -f application.yaml

## Issues
kubectl edit deployment argocd-repo-server -n argocd
This will open the deployment configuration in your editor. Locate the env section under the argocd-repo-server container and add the ARGOCD_GPG_ENABLED variable like this:
spec:
  containers:
  - name: argocd-repo-server
    env:
    - name: ARGOCD_GPG_ENABLED
      value: "false"

kubectl rollout restart deployment argocd-repo-server -n argocd
kubectl logs -l app.kubernetes.io/name=argocd-repo-server -n argocd


# check for the argocd-server svc & port forward to access the UI
kubectl get svc -n argocd 

=> kubectl port-forward svc/argocd-server -n argocd 8080:80
=> kubectl port-forward svc/argocd-server -n argocd 8080:443

=> kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 --decode


kubectl -n kube-system edit configmap coredns
forward . /etc/resolv.conf {
    max_concurrent 1000
}
forward . 8.8.8.8 8.8.4.4 {
    max_concurrent 1000
}
kubectl -n kube-system rollout restart deployment coredns
kubectl run dns-check --rm -it --image=busybox --restart=Never -- nslookup github.com
