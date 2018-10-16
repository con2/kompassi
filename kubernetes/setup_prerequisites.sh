#!/bin/bash
set -xue

# secret-generator
kubectl apply -f https://raw.githubusercontent.com/mittwald/kubernetes-secret-generator/master/deploy/secret-generator-rbac.yaml
kubectl apply -f https://raw.githubusercontent.com/mittwald/kubernetes-secret-generator/master/deploy/secret-generator.yaml

# ingress-nginx
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/mandatory.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/provider/cloud-generic.yaml
