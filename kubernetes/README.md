# Kubernetes Deployment for Prosper Tutor Lite

This directory contains Kubernetes manifests for deploying Prosper Tutor Lite in a production environment.

## Overview

The deployment consists of:
- Backend service (FastAPI)
- Frontend service (Streamlit)
- Persistent storage for vector databases and course content
- ConfigMap for application configuration
- Services for internal communication
- Ingress for external access

## Prerequisites

- Kubernetes cluster (>= 1.20)
- kubectl CLI configured
- helm CLI (optional, for advanced deployments)

## Quick Start

1. Create the namespace:
   ```bash
   kubectl apply -f namespace.yaml
   ```

2. Deploy all resources:
   ```bash
   kubectl apply -f .
   ```

Or using kustomize:
   ```bash
   kubectl apply -k .
   ```

3. Check the deployment status:
   ```bash
   kubectl get pods -n prosper-tutor
   ```

4. Get the external IP (if using LoadBalancer service):
   ```bash
   kubectl get svc prosper-tutor-lite-frontend -n prosper-tutor
   ```

## Components

### Deployments
- `prosper-tutor-lite-backend`: Runs the FastAPI backend with RAG pipeline
- `prosper-tutor-lite-frontend`: Runs the Streamlit frontend

### Services
- `prosper-tutor-lite-backend`: Internal service for backend API
- `prosper-tutor-lite-frontend`: External service for user access

### Storage
- `vectorstore-pvc`: Persistent storage for FAISS vector databases
- `courses-pvc`: Persistent storage for course content

### Configuration
- `prosper-tutor-config`: ConfigMap with application settings

## Scaling

Scale the backend deployment:
```bash
kubectl scale deployment prosper-tutor-lite-backend --replicas=5 -n prosper-tutor
```

## Updating

To update the application with a new image:
```bash
kubectl set image deployment/prosper-tutor-lite-backend backend=prosper-tutor-lite:v2.0 -n prosper-tutor
```

## Monitoring

Check logs:
```bash
kubectl logs -l app=prosper-tutor-lite -n prosper-tutor
```

Describe pods:
```bash
kubectl describe pod -l app=prosper-tutor-lite -n prosper-tutor
```

## Cleanup

Delete all resources:
```bash
kubectl delete -f .
```