#! /bin/bash



kubectl create token cvbackup -n kube-system

kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443
kubectl -n kserve-test port-forward svc/sklearn-iris-predictor 8444:80
kubectl port-forward svc/istio-ingressgateway -n istio-system 8446:80
kubectl port-forward svc/centraldashboard -n kubeflow 8445:80