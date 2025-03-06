 XDG_DATA_HOME=/Volumes/BOOTCAMP/kubeflow/images podman machine start


podman pull docker-0.unsee.tech/istio/pilot:1.24.2
podman image tag docker-0.unsee.tech/istio/pilot:1.24.2 docker.io/istio/pilot:1.24.2
podman save -o pilot.tar docker.io/istio/pilot:1.24.2
kind load image-archive pilot.tar  


podman pull docker-0.unsee.tech/istio/proxyv2:1.24.2
podman image tag docker-0.unsee.tech/istio/proxyv2:1.24.2 docker.io/istio/proxyv2:1.24.2
podman save -o proxyv2.tar docker.io/istio/proxyv2:1.24.2
kind load image-archive proxyv2.tar


podman pull docker.m.daocloud.io/kserve/kserve-controller:v0.14.1
podman image tag docker.m.daocloud.io/kserve/kserve-controller:v0.14.1 docker.io/kserve/kserve-controller:v0.14.1
podman save -o kserve-controller.tar docker.io/kserve/kserve-controller:v0.14.1
kind load image-archive kserve-controller.tar

# install kubernetes-dashboard
helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard

podman pull docker.m.daocloud.io/kubernetesui/dashboard-api:1.10.3
podman image tag docker.m.daocloud.io/kubernetesui/dashboard-api:1.10.3 docker.io/kubernetesui/dashboard-api:1.10.3
podman save -o dashboard-api.tar docker.io/kubernetesui/dashboard-api:1.10.3
kind load image-archive dashboard-api.tar


podman pull docker.m.daocloud.io/kubernetesui/dashboard-auth:1.2.3
podman image tag docker.m.daocloud.io/kubernetesui/dashboard-auth:1.2.3 docker.io/kubernetesui/dashboard-auth:1.2.3
podman save -o dashboard-auth.tar docker.io/kubernetesui/dashboard-auth:1.2.3
kind load image-archive dashboard-auth.tar

podman pull docker.m.daocloud.io/kubernetesui/dashboard-backend:1.2.3
podman image tag docker.m.daocloud.io/kubernetesui/dashboard-backend:1.2.3 docker.io/kubernetesui/dashboard-backend:1.2.3
podman save -o dashboard-backend.tar docker.io/kubernetesui/dashboard-backend:1.2.3
kind load image-archive dashboard-backend.tar

podman pull docker.m.daocloud.io/kubernetesui/dashboard-frontend:1.2.3
podman image tag docker.m.daocloud.io/kubernetesui/dashboard-frontend:1.2.3 docker.io/kubernetesui/dashboard-frontend:1.2.3
podman save -o dashboard-frontend.tar docker.io/kubernetesui/dashboard-frontend:1.2.3
kind load image-archive dashboard-frontend.tar  

podman pull docker.m.daocloud.io/kong:3.8
podman image tag docker.m.daocloud.io/kong:3.8 docker.io/kong:3.8
podman save -o kong.tar docker.io/kong:3.8
kind load image-archive kong.tar    

podman pull docker.m.daocloud.io/kubernetesui/dashboard-metrics-scraper:1.2.2
podman image tag docker.m.daocloud.io/kubernetesui/dashboard-metrics-scraper:1.2.2 docker.io/kubernetesui/dashboard-metrics-scraper:1.2.2
podman save -o dashboard-metrics-scraper.tar docker.io/kubernetesui/dashboard-metrics-scraper:1.2.2
kind load image-archive dashboard-metrics-scraper.tar

podman pull docker.m.daocloud.io/kubernetesui/dashboard-web:1.6.2
podman image tag docker.m.daocloud.io/kubernetesui/dashboard-web:1.6.2 docker.io/kubernetesui/dashboard-web:1.6.2
podman save -o dashboard-web.tar docker.io/kubernetesui/dashboard-web:1.6.2
kind load image-archive dashboard-web.tar

kubectl create serviceaccount cvbackup -n kube-system
kubectl create clusterrolebinding cvbackup-cluster-rule --clusterrole=cluster-admin --serviceaccount=kube-system:cvbackup
kubectl create token cvbackup -n kube-system


podman pull docker.m.daocloud.io/kserve/storage-initializer:v0.14.1
podman image tag docker.m.daocloud.io/kserve/storage-initializer:v0.14.1 docker.io/kserve/storage-initializer:v0.14.1
podman save -o storage-initializer.tar docker.io/kserve/storage-initializer:v0.14.1
kind load image-archive storage-initializer.tar

podman pull docker.m.daocloud.io/kserve/sklearnserver:v0.14.1
podman image tag docker.m.daocloud.io/kserve/sklearnserver:v0.14.1 docker.io/kserve/sklearnserver:v0.14.1
podman save -o sklearnserver.tar docker.io/kserve/sklearnserver:v0.14.1
kind load image-archive sklearnserver.tar


podman pull docker-0.unsee.tech/kserve/alibi-explainer:v0.12.1
podman image tag docker-0.unsee.tech/kserve/alibi-explainer:v0.12.1 docker.io/kserve/alibi-explainer:v0.12.1
podman save -o alibi-explainer.tar docker.io/kserve/alibi-explainer:v0.12.1
kind load image-archive alibi-explainer.tar 

podman pull quay.io/oauth2-proxy/oauth2-proxy:v7.7.1
podman image tag quay.io/oauth2-proxy/oauth2-proxy:v7.7.1 docker.io/oauth2-proxy/oauth2-proxy:v7.7.1
podman save -o oauth2-proxy.tar docker.io/oauth2-proxy/oauth2-proxy:v7.7.1
kind load image-archive oauth2-proxy.tar


podman pull docker-0.unsee.tech/dexidp/dex:v2.41.1
podman image tag docker-0.unsee.tech/dexidp/dex:v2.41.1 ghcr.io/dexidp/dex:v2.41.1
podman save -o dex.tar ghcr.io/dexidp/dex:v2.41.1
kind load image-archive dex.tar

podman pull docker-0.unsee.tech/kubeflownotebookswg/centraldashboard:v1.10.0-rc.1
podman image tag docker-0.unsee.tech/kubeflownotebookswg/centraldashboard:v1.10.0-rc.1 docker.io/kubeflownotebookswg/centraldashboard:v1.10.0-rc.1
podman save -o centraldashboard.tar docker.io/kubeflownotebookswg/centraldashboard:v1.10.0-rc.1
kind load image-archive centraldashboard.tar

podman pull docker-0.unsee.tech/kubeflownotebookswg/poddefaults-webhook:v1.10.0-rc.1
podman image tag docker-0.unsee.tech/kubeflownotebookswg/poddefaults-webhook:v1.10.0-rc.1 docker.io/kubeflownotebookswg/poddefaults-webhook:v1.10.0-rc.1
podman save -o poddefaults-webhook.tar docker.io/kubeflownotebookswg/poddefaults-webhook:v1.10.0-rc.1
kind load image-archive poddefaults-webhook.tar 


podman pull docker-0.unsee.tech/kubeflownotebookswg/jupyter-web-app:v1.10.0-rc.1
podman image tag docker-0.unsee.tech/kubeflownotebookswg/jupyter-web-app:v1.10.0-rc.1 docker.io/kubeflownotebookswg/jupyter-web-app:v1.10.0-rc.1
podman save -o jupyter-web-app.tar docker.io/kubeflownotebookswg/jupyter-web-app:v1.10.0-rc.1
kind load image-archive jupyter-web-app.tar

podman pull docker-0.unsee.tech/kubeflownotebookswg/notebook-controller:v1.10.0-rc.1
podman image tag docker-0.unsee.tech/kubeflownotebookswg/notebook-controller:v1.10.0-rc.1 docker.io/kubeflownotebookswg/notebook-controller:v1.10.0-rc.1
podman save -o notebook-controller.tar docker.io/kubeflownotebookswg/notebook-controller:v1.10.0-rc.1
kind load image-archive notebook-controller.tar

podman pull docker-0.unsee.tech/kubeflownotebookswg/kfam:v1.10.0-rc.1
podman image tag docker-0.unsee.tech/kubeflownotebookswg/kfam:v1.10.0-rc.1 docker.io/kubeflownotebookswg/kfam:v1.10.0-rc.1
podman save -o kfam.tar docker.io/kubeflownotebookswg/kfam:v1.10.0-rc.1
kind load image-archive kfam.tar

podman pull docker-0.unsee.tech/kubeflownotebookswg/profile-controller:v1.10.0-rc.1
podman image tag docker-0.unsee.tech/kubeflownotebookswg/profile-controller:v1.10.0-rc.1 docker.io/kubeflownotebookswg/profile-controller:v1.10.0-rc.1
podman save -o profile-controller.tar docker.io/kubeflownotebookswg/profile-controller:v1.10.0-rc.1
kind load image-archive profile-controller.tar

podman pull docker-0.unsee.tech/kubeflownotebookswg/jupyter-scipy:v1.10.0-rc.1
podman image tag docker-0.unsee.tech/kubeflownotebookswg/jupyter-scipy:v1.10.0-rc.1 docker.io/kubeflownotebookswg/jupyter-scipy:v1.10.0-rc.1
podman save -o jupyter-scipy.tar docker.io/kubeflownotebookswg/jupyter-scipy:v1.10.0-rc.1
kind load image-archive jupyter-scipy.tar

podman pull docker-0.unsee.tech/kubeflownotebookswg/tensorboards-web-app:v1.10.0-rc.1
podman image tag docker-0.unsee.tech/kubeflownotebookswg/tensorboards-web-app:v1.10.0-rc.1 docker.io/kubeflownotebookswg/tensorboards-web-app:v1.10.0-rc.1
podman save -o tensorboards-web-app.tar docker.io/kubeflownotebookswg/tensorboards-web-app:v1.10.0-rc.1
kind load image-archive tensorboards-web-app.tar



podman pull docker-0.unsee.tech/kubeflownotebookswg/tensorboard-controller:v1.10.0-rc.1
podman image tag docker-0.unsee.tech/kubeflownotebookswg/tensorboard-controller:v1.10.0-rc.1 docker.io/kubeflownotebookswg/tensorboard-controller:v1.10.0-rc.1
podman save -o tensorboard-controller.tar docker.io/kubeflownotebookswg/tensorboard-controller:v1.10.0-rc.1
kind load image-archive tensorboard-controller.tar

podman pull docker-0.unsee.tech/kubeflownotebookswg/volumes-web-app:v1.10.0-rc.1
podman image tag docker-0.unsee.tech/kubeflownotebookswg/volumes-web-app:v1.10.0-rc.1 docker.io/kubeflownotebookswg/volumes-web-app:v1.10.0-rc.1
podman save -o volumes-web-app.tar docker.io/kubeflownotebookswg/volumes-web-app:v1.10.0-rc.1
kind load image-archive volumes-web-app.tar

podman pull docker-0.unsee.tech/kubeflownotebookswg/pvcviewer-controller:v1.10.0-rc.1
podman image tag docker-0.unsee.tech/kubeflownotebookswg/pvcviewer-controller:v1.10.0-rc.1 docker.io/kubeflownotebookswg/pvcviewer-controller:v1.10.0-rc.1
podman save -o pvcviewer-controller.tar docker.io/kubeflownotebookswg/pvcviewer-controller:v1.10.0-rc.1
kind load image-archive pvcviewer-controller.tar

podman pull docker-0.unsee.tech/filebrowser/filebrowser:v2.25.0
podman image tag docker-0.unsee.tech/filebrowser/filebrowser:v2.25.0 docker.io/filebrowser/filebrowser:v2.25.0
podman save -o filebrowser.tar docker.io/filebrowser/filebrowser:v2.25.0
kind load image-archive filebrowser.tar 

podman pull docker-0.unsee.tech/tensorflow/tensorflow:2.5.1
podman image tag docker-0.unsee.tech/tensorflow/tensorflow:2.5.1 docker.io/tensorflow/tensorflow:2.5.1
podman save -o tensorflow.tar docker.io/tensorflow/tensorflow:2.5.1
kind load image-archive tensorflow.tar

podman pull docker-0.unsee.tech/kubeflowkatib/katib-ui:v0.18.0-rc.0
podman image tag docker-0.unsee.tech/kubeflowkatib/katib-ui:v0.18.0-rc.0 docker.io/kubeflowkatib/katib-ui:v0.18.0-rc.0
podman save -o katib-ui.tar docker.io/kubeflowkatib/katib-ui:v0.18.0-rc.0
kind load image-archive katib-ui.tar

podman pull docker-0.unsee.tech/kubeflowkatib/katib-db-manager:v0.18.0-rc.0
podman image tag docker-0.unsee.tech/kubeflowkatib/katib-db-manager:v0.18.0-rc.0 docker.io/kubeflowkatib/katib-db-manager:v0.18.0-rc.0
podman save -o katib-db-manager.tar docker.io/kubeflowkatib/katib-db-manager:v0.18.0-rc.0
kind load image-archive katib-db-manager.tar


podman pull docker-0.unsee.tech/mysql:8.0.29
podman image tag docker-0.unsee.tech/mysql:8.0.29 docker.io/mysql:8.0.29
podman save -o mysql.tar docker.io/mysql:8.0.29
kind load image-archive mysql.tar

podman pull docker-0.unsee.tech/kubeflowkatib/katib-controller:v0.18.0-rc.0
podman image tag docker-0.unsee.tech/kubeflowkatib/katib-controller:v0.18.0-rc.0 docker.io/kubeflowkatib/katib-controller:v0.18.0-rc.0
podman save -o katib-controller.tar docker.io/kubeflowkatib/katib-controller:v0.18.0-rc.0
kind load image-archive katib-controller.tar


podman pull docker-0.unsee.tech/kubeflowkatib/suggestion-hyperopt:v0.18.0-rc.0
podman image tag docker-0.unsee.tech/kubeflowkatib/suggestion-hyperopt:v0.18.0-rc.0 docker.io/kubeflowkatib/suggestion-hyperopt:v0.18.0-rc.0
podman save -o suggestion-hyperopt.tar docker.io/kubeflowkatib/suggestion-hyperopt:v0.18.0-rc.0
kind load image-archive suggestion-hyperopt.tar


podman pull docker-0.unsee.tech/kubeflow/training-operator:v1-5170a36
podman image tag docker-0.unsee.tech/kubeflow/training-operator:v1-5170a36 docker.io/kubeflow/training-operator:v1-5170a36
podman save -o training-operator.tar docker.io/kubeflow/training-operator:v1-5170a36
kind load image-archive training-operator.tar

podman pull docker-0.unsee.tech/kubeflowkatib/pytorch-mnist-cpu:v0.18.0-rc.0
podman image tag docker-0.unsee.tech/kubeflowkatib/pytorch-mnist-cpu:v0.18.0-rc.0 docker.io/kubeflowkatib/pytorch-mnist-cpu:latest
podman save -o pytorch-mnist-cpu.tar docker.io/kubeflowkatib/pytorch-mnist-cpu:latest
kind load image-archive pytorch-mnist-cpu.tar

podman pull docker-0.unsee.tech/kubeflowkatib/file-metrics-collector:v0.18.0-rc.0
podman image tag docker-0.unsee.tech/kubeflowkatib/file-metrics-collector:v0.18.0-rc.0 docker.io/kubeflowkatib/file-metrics-collector:v0.18.0-rc.0
podman save -o file-metrics-collector.tar docker.io/kubeflowkatib/file-metrics-collector:v0.18.0-rc.0
kind load image-archive file-metrics-collector.tar

podman pull  docker-0.unsee.tech/alpine:3.10
podman image tag docker-0.unsee.tech/alpine:3.10 docker.io/alpine:3.10
podman save -o alpine.tar docker.io/alpine:3.10
kind load image-archive alpine.tar

podman pull docker-0.unsee.tech/kserve/models-web-app:v0.14.0-rc.0
podman image tag docker-0.unsee.tech/kserve/models-web-app:v0.14.0-rc.0 docker.io/kserve/models-web-app:v0.14.0-rc.0
podman save -o models-web-app.tar docker.io/kserve/models-web-app:v0.14.0-rc.0
kind load image-archive models-web-app.tar


podman pull ghcr.nju.edu.cn/kubeflow/kfp-cache-server:2.4.0
podman image tag ghcr.nju.edu.cn/kubeflow/kfp-cache-server:2.4.0 ghcr.io/kubeflow/kfp-cache-server:2.4.0
podman save -o kfp-cache-server.tar ghcr.io/kubeflow/kfp-cache-server:2.4.0
kind load image-archive kfp-cache-server.tar


podman pull docker-0.unsee.tech/python:3.9
podman image tag docker-0.unsee.tech/python:3.9 docker.io/python:3.9
podman save -o python.tar docker.io/python:3.9
kind load image-archive python.tar

podman pull gcr.linkos.org/tfx-oss-public/ml_metadata_store_server:1.14.0
podman image tag gcr.linkos.org/tfx-oss-public/ml_metadata_store_server:1.14.0 ghcr.io/tfx-oss-public/ml_metadata_store_server:1.14.0
podman save -o ml_metadata_store_server.tar ghcr.io/tfx-oss-public/ml_metadata_store_server:1.14.0
kind load image-archive ml_metadata_store_server.tar

podman pull gcr.linkos.org/ml-pipeline/minio:RELEASE.2019-08-14T20-37-41Z-license-compliance
podman image tag gcr.linkos.org/ml-pipeline/minio:RELEASE.2019-08-14T20-37-41Z-license-compliance ghcr.io/ml-pipeline/minio:RELEASE.2019-08-14T20-37-41Z-license-compliance
podman save -o minio.tar ghcr.io/ml-pipeline/minio:RELEASE.2019-08-14T20-37-41Z-license-compliance
kind load image-archive minio.tar

podman pull gcr.linkos.org/ml-pipeline/mysql:8.0.26
podman image tag gcr.linkos.org/ml-pipeline/mysql:8.0.26 ghcr.io/ml-pipeline/mysql:8.0.26
podman save -o mysql.tar ghcr.io/ml-pipeline/mysql:8.0.26
kind load image-archive mysql.tar

podman pull ghcr.linkos.org/kubeflow/kfp-visualization-server:2.4.0
podman image tag ghcr.linkos.org/kubeflow/kfp-visualization-server:2.4.0 ghcr.io/kubeflow/kfp-visualization-server:2.4.0
podman save -o kfp-visualization-server.tar ghcr.io/kubeflow/kfp-visualization-server:2.4.0
kind load image-archive kfp-visualization-server.tar

podman pull gcr.linkos.org/ml-pipeline/workflow-controller:v3.4.17-license-compliance
podman image tag gcr.linkos.org/ml-pipeline/workflow-controller:v3.4.17-license-compliance ghcr.io/ml-pipeline/workflow-controller:v3.4.17-license-compliance
podman save -o workflow-controller.tar ghcr.io/ml-pipeline/workflow-controller:v3.4.17-license-compliance
kind load image-archive workflow-controller.tar





























































