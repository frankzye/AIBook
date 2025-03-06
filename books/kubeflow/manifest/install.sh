#! /bin/bash

git clone https://github.com/kubeflow/manifests.git --depth 1

echo "Installing Istio configured with external authorization..."
kustomize build manifests/common/istio-1-24/istio-crds/base | kubectl apply -f -
kustomize build manifests/common/istio-1-24/istio-namespace/base | kubectl apply -f -
kustomize build manifests/common/istio-1-24/istio-install/overlays/oauth2-proxy | kubectl apply -f -

echo "Waiting for all Istio Pods to become ready..."
kubectl wait --for=condition=Ready pods --all -n istio-system --timeout 300s

# Oauth2-proxy
echo "Installing oauth2-proxy..."
kustomize build manifests/common/oauth2-proxy/overlays/m2m-dex-and-kind/ | kubectl apply -f -

kustomize build manifests/common/oauth2-proxy/overlays/m2m-dex-only/ | kubectl apply -f -
kubectl wait --for=condition=ready pod -l 'app.kubernetes.io/name=oauth2-proxy' --timeout=180s -n oauth2-proxy

echo "Installing Dex..."
kustomize build manifests/common/dex/overlays/oauth2-proxy | kubectl apply -f -
kubectl wait --for=condition=ready pods --all --timeout=180s -n auth

kustomize build manifests/common/oauth2-proxy/components/allow-unauthenticated-issuer-discovery/ | kubectl apply -f -

# Kubeflow namespace
echo "Installing Kubeflow namespace..."
kustomize build manifests/common/kubeflow-namespace/base | kubectl apply -f -


echo "Installing network policies..."
kustomize build manifests/common/networkpolicies/base | kubectl apply -f -

echo "Kubeflow Roles"
kustomize build manifests/common/kubeflow-roles/base | kubectl apply -f -


kustomize build manifests/common/istio-1-24/kubeflow-istio-resources/base | kubectl apply -f -


# install kubeflow pipeline
echo "install kubeflow pipeline"
kustomize build manifests/apps/pipeline/upstream/env/cert-manager/platform-agnostic-multi-user | kubectl apply -f -

echo "install katib"
kustomize build manifests/apps/katib/upstream/installs/katib-with-kubeflow | kubectl apply -f -

kustomize build manifests/apps/centraldashboard/overlays/oauth2-proxy | kubectl apply -f -

kustomize build manifests/apps/profiles/upstream/overlays/kubeflow | kubectl apply -f -

kustomize build manifests/apps/admission-webhook/upstream/overlays/cert-manager | kubectl apply -f -

kustomize build manifests/apps/jupyter/notebook-controller/upstream/overlays/kubeflow | kubectl apply -f -

kustomize build manifests/apps/jupyter/jupyter-web-app/upstream/overlays/istio | kubectl apply -f -

kustomize build manifests/apps/training-operator/upstream/overlays/kubeflow | kubectl apply --server-side --force-conflicts -f -

kustomize build manifests/apps/tensorboard/tensorboards-web-app/upstream/overlays/istio | kubectl apply -f -

kustomize build manifests/apps/tensorboard/tensorboard-controller/upstream/overlays/kubeflow | kubectl apply -f -

kustomize build manifests/apps/pvcviewer-controller/upstream/base | kubectl apply -f -

kustomize build manifests/apps/volumes-web-app/upstream/overlays/istio | kubectl apply -f -

kustomize build manifests/apps/kserve/models-web-app/overlays/kubeflow | kubectl apply -f -

kustomize build manifests/apps/kserve/kserve | kubectl apply --server-side --force-conflicts -f -

kustomize build manifests/apps/pipeline/upstream/env/cert-manager/platform-agnostic-multi-user | kubectl apply -f -
