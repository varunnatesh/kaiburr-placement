# Task 2: Kubernetes Deployment

## Overview
This task extends Task 1 by deploying the application to Kubernetes with the following features:
- Application runs in a Kubernetes cluster
- MongoDB runs in a separate pod with persistent storage
- Application uses Kubernetes API to execute commands in dynamically created pods
- All configurations use environment variables

## Prerequisites
- Docker Desktop with Kubernetes enabled OR Minikube/Kind
- kubectl CLI installed
- Docker installed
- Task 1 application completed

## Project Structure
```
task2-kubernetes/
├── Dockerfile
├── mongodb-pv.yaml (Persistent Volume)
├── mongodb-deployment.yaml (MongoDB Deployment & Service)
├── service-account.yaml (RBAC for pod creation)
├── app-deployment.yaml (Application Deployment & Service)
└── README.md
```

## Setup Instructions

### Step 1: Build Docker Image

First, copy the application code to this directory and build the Docker image:

```powershell
# Copy application files
Copy-Item -Path ..\task1-java-backend\* -Destination . -Recurse -Exclude target,screenshots

# Build Docker image
docker build -t task-manager:latest .
```

### Step 2: Verify Kubernetes Cluster

Make sure your Kubernetes cluster is running:

```powershell
kubectl cluster-info
kubectl get nodes
```

### Step 3: Deploy MongoDB with Persistent Storage

```powershell
# Create persistent volume and claim
kubectl apply -f mongodb-pv.yaml

# Deploy MongoDB
kubectl apply -f mongodb-deployment.yaml

# Verify MongoDB is running
kubectl get pods -l app=mongodb
kubectl get pvc mongodb-pvc
```

### Step 4: Create Service Account and RBAC

The application needs permissions to create and manage pods:

```powershell
kubectl apply -f service-account.yaml
```

### Step 5: Deploy Application

```powershell
kubectl apply -f app-deployment.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services
```

### Step 6: Access the Application

The application can be accessed via kubectl proxy (recommended) or NodePort on port 30080:

```powershell
# Via kubectl proxy (in another terminal, run: kubectl proxy --port=8001)
curl http://127.0.0.1:8001/api/v1/namespaces/default/services/http:task-manager:8080/proxy/api/tasks

# NodePort (fallback)
# Docker Desktop
curl http://localhost:30080/api/tasks
# Minikube
curl http://$(minikube ip):30080/api/tasks
```

## Testing the Application

### 1. Create a Task

```powershell
curl -X PUT http://localhost:30080/api/tasks `
  -H "Content-Type: application/json" `
  -d '{\"id\":\"1\",\"name\":\"Print Date\",\"owner\":\"John Doe\",\"command\":\"date\"}'
```

### 2. Execute Task in Kubernetes Pod

```powershell
curl -X PUT http://localhost:30080/api/tasks/1/execute
```

This will:
1. Create a new busybox pod in the cluster
2. Execute the command inside that pod
3. Capture the output
4. Store the execution result
5. Delete the pod

### 3. Verify Pod Creation

While a task is executing, you can see the temporary pod:

```powershell
kubectl get pods
```

### 4. View Task Execution History

```powershell
curl http://localhost:30080/api/tasks/1
```

## Persistent Storage Verification

### Test MongoDB Data Persistence

1. Create some tasks
2. Delete the MongoDB pod:
```powershell
kubectl delete pod -l app=mongodb
```
3. Wait for Kubernetes to recreate the pod
4. Verify data still exists:
```powershell
curl http://localhost:30080/api/tasks
```

## Kubernetes Commands Reference

### View Application Logs

```powershell
# Get pod name
kubectl get pods -l app=task-manager

# View logs
kubectl logs <pod-name>

# Follow logs
kubectl logs -f <pod-name>
```

### View MongoDB Logs

```powershell
kubectl logs -l app=mongodb
```

### Access Application Shell

```powershell
kubectl exec -it <task-manager-pod-name> -- sh
```

### Scale Application

```powershell
kubectl scale deployment task-manager --replicas=3
```

## Architecture

```
┌─────────────────────────────────────────────┐
│           Kubernetes Cluster                │
│                                             │
│  ┌──────────────┐      ┌──────────────┐   │
│  │  Task Manager│◄─────┤   MongoDB    │   │
│  │     Pod      │      │     Pod      │   │
│  │              │      │              │   │
│  │  Port: 8080  │      │  Port: 27017 │   │
│  └──────┬───────┘      └──────┬───────┘   │
│         │                     │           │
│         │              ┌──────▼───────┐   │
│         │              │ Persistent   │   │
│         │              │   Volume     │   │
│         │              └──────────────┘   │
│         │                                 │
│         │  Creates/Deletes                │
│         ▼                                 │
│  ┌──────────────┐                         │
│  │  BusyBox Pod │  (Temporary)            │
│  │  Executes    │                         │
│  │  Command     │                         │
│  └──────────────┘                         │
│                                             │
└─────────────────┬───────────────────────────┘
                  │
                  │ NodePort: 30080
                  ▼
            [Your Machine]
```

## Key Features

1. **Isolated Command Execution**: Each command runs in its own pod
2. **Persistent Data**: MongoDB data survives pod restarts
3. **Environment Variables**: MongoDB connection configured via env vars
4. **RBAC**: Service account with minimal required permissions
5. **Auto-cleanup**: Temporary execution pods are automatically deleted

## Troubleshooting

### Pods not starting

```powershell
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

### Cannot create execution pods

```powershell
# Check service account
kubectl get serviceaccount task-manager-sa

# Check RBAC
kubectl get role pod-manager
kubectl get rolebinding task-manager-pod-manager
```

### MongoDB connection issues

```powershell
# Test MongoDB service
kubectl run -it --rm mongo-client --image=mongo:7.0 --restart=Never -- mongosh mongodb://mongodb:27017/taskmanager
```

## Cleanup

To remove all resources:

```powershell
kubectl delete -f app-deployment.yaml
kubectl delete -f service-account.yaml
kubectl delete -f mongodb-deployment.yaml
kubectl delete -f mongodb-pv.yaml
```


## Screenshots

### kubectl get pods
![](screenshots/kubectl_get_pods_2025-10-18_19-13-50.png)

### kubectl get svc
![](screenshots/kubectl_get_svc_2025-10-18_19-13-55.png)

### kubectl logs <task-manager-pod>
![](screenshots/kubectl_logs_2025-10-18_19-14-02.png)

### kubectl get pv,pvc
![](screenshots/kubectl_pv_pvc_2025-10-18_19-14-07.png)

### Browser hitting service
![](screenshots/app_access_2025-10-18_19-14-11.png)

## Next Steps

- Task 3: Create React frontend UI
- Task 4: Set up CI/CD pipeline

## Author

[Your Name]
Date: October 16, 2025
