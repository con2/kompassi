#!/bin/bash
set -xue

# secret-generator
kubectl apply -f https://raw.githubusercontent.com/con2/kubernetes-secret-generator/con2/deploy/secret-generator-rbac.yaml
kubectl apply -f https://raw.githubusercontent.com/con2/kubernetes-secret-generator/con2/deploy/secret-generator.yaml

# ingress-nginx
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/mandatory.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/provider/cloud-generic.yaml
