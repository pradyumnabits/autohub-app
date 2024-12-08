

#ArgoCD
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl get svc argocd-server -n argocd
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
kubectl -n argocd patch svc argocd-server -p '{"spec": {"type": "NodePort"}}'
kubectl port-forward --address 0.0.0.0 svc/argocd-server -n argocd 8080:80
sudo minikube tunnel

screen
Enter
kubectl port-forward --address 0.0.0.0 svc/argocd-server -n argocd 8080:80
ctrl A D
 screen -r
 screen -r <screen-id>

sudo ufw status
sudo ufw allow 8001/tcp

sudo ufw allow 8000:9999/tcp
sudo ufw allow 8000:9999/udp


#[port forwarding]
kubectl port-forward --address 0.0.0.0 svc/argocd-server -n argocd 8080:80

kubectl port-forward --address 0.0.0.0 svc/auth-svc 8001:80 -n autohub &
kubectl port-forward --address 0.0.0.0 svc/vehicle-svc 8002:80 -n autohub &
kubectl port-forward --address 0.0.0.0 svc/booking-svc 8003:80 -n autohub &
kubectl port-forward --address 0.0.0.0 svc/support-svc 8004:80 -n autohub &
kubectl port-forward --address 0.0.0.0 svc/rsa-svc 8005:80 -n autohub &
kubectl port-forward --address 0.0.0.0 svc/feedback-svc 8006:80 -n autohub &
kubectl port-forward --address 0.0.0.0 svc/customer-svc 8007:80 -n autohub &

nohup ./port-forward.sh &


http://139.84.217.135:8001/docs
http://139.84.217.135:8001/ping