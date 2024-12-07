kubectl port-forward --address 0.0.0.0 svc/argocd-server -n argocd 8080:80 &

kubectl port-forward --address 0.0.0.0 svc/auth-svc 8001:80 -n autohub &
kubectl port-forward --address 0.0.0.0 svc/vehicle-svc 8002:80 -n autohub &
kubectl port-forward --address 0.0.0.0 svc/booking-svc 8003:80 -n autohub &
kubectl port-forward --address 0.0.0.0 svc/support-svc 8004:80 -n autohub &
kubectl port-forward --address 0.0.0.0 svc/rsa-svc 8005:80 -n autohub &
kubectl port-forward --address 0.0.0.0 svc/feedback-svc 8006:80 -n autohub &
kubectl port-forward --address 0.0.0.0 svc/customer-svc 8007:80 -n autohub &
