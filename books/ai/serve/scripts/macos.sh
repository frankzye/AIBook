#! /bin/bash

kind create cluster --name kind --image m.daocloud.io/docker.io/kindest/node:v1.32.2
podman start kind-control-plane