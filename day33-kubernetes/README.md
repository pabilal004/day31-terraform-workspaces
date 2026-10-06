# Day 33 — Kubernetes YAML & Service Configuration

## What was practiced

- Kubernetes YAML structure
- Deployment configuration
- Replicas
- Labels and selectors
- NGINX container image
- ClusterIP Service
- Service port and targetPort
- Service-to-Pod connectivity

## Project

Deployment:
- Name: day33-nginx
- Replicas: 2
- Image: nginx:1.27
- Pod label: app=day33-nginx

Service:
- Name: day33-nginx-service
- Type: ClusterIP
- Port: 80
- Target port: 80
- Selector: app=day33-nginx

## Verification

The Deployment reached 2/2 Ready.
The Service discovered both Pod endpoints.
A temporary curl Pod successfully requested:
http://day33-nginx-service

The response was the NGINX welcome page.
