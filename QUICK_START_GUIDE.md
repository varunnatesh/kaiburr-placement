# Quick Start Guide - Running All Tasks

## 🚀 Step-by-Step Startup Instructions

### Step 1: Start Docker Desktop (Required First!)

1. **Open Docker Desktop**:
   - Press `Windows Key` + Search for "Docker Desktop"
   - Click to open Docker Desktop
   - Wait for the whale icon in system tray to be stable (1-2 minutes)
   - Look for "Docker Desktop is running" in bottom left

2. **Verify Docker is Running**:
   ```powershell
   docker ps
   ```
   Should show: `CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES`
   (Empty list is OK, just no errors)

---

### Step 2: Start Minikube Kubernetes

```powershell
# Start minikube (takes 2-3 minutes first time)
minikube start

# Verify it's running
minikube status
```

**Expected Output**:
```
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

---

### Step 3: Deploy Backend to Kubernetes

```powershell
# Navigate to kubernetes directory
cd C:\placement\task2-kubernetes

# Deploy MongoDB
kubectl apply -f mongodb-pv.yaml
kubectl apply -f mongodb-deployment.yaml

# Deploy Backend App
kubectl apply -f service-account.yaml
kubectl apply -f app-deployment.yaml

# Check if pods are starting
kubectl get pods -w
```

**Wait until you see** (press Ctrl+C to stop watching):
```
NAME                           READY   STATUS    RESTARTS   AGE
mongodb-xxxxx                  1/1     Running   0          1m
task-manager-xxxxxxxxx         1/1     Running   0          1m
```

**Note**: Pods may show "Pending" or "ContainerCreating" for 2-3 minutes. This is normal!

---

### Step 4: Start kubectl Proxy (New Terminal)

**Open a NEW PowerShell terminal** and run:

```powershell
kubectl proxy --port=8001
```

**Expected Output**:
```
Starting to serve on 127.0.0.1:8001
```

**Keep this terminal running!** Don't close it.

---

### Step 5: Start React Frontend (New Terminal)

**Open ANOTHER NEW PowerShell terminal** and run:

```powershell
cd C:\placement\task3-react-frontend

# Start development server
npm run dev
```

**Expected Output**:
```
  VITE v5.x.x  ready in xxx ms

   ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

**Keep this terminal running too!**

---

### Step 6: Access the Application 🎉

**Open your browser and go to**:
```
http://localhost:3000/
```

You should see the Task Manager interface!

---

## 🧪 Testing the Application

### Test 1: Create a Task
1. Click "Create Task" button
2. Fill in:
   - **Name**: Test Task
   - **Description**: This is a test
   - **Assigned To**: Your Name
3. Click "Submit"
4. Task should appear in the list

### Test 2: View Task Details
1. Click on the task you created
2. Should show full details

### Test 3: Execute Task
1. Click "Execute" button on a task
2. Wait 5-10 seconds
3. Check execution history

### Test 4: Edit Task
1. Click "Edit" on a task
2. Change the description
3. Click "Update"

### Test 5: Delete Task
1. Click "Delete" on a task
2. Confirm deletion
3. Task should be removed from list

---

## 📊 Verification Commands

### Check Kubernetes Status
```powershell
# See all pods
kubectl get pods

# See all services
kubectl get services

# See logs from backend
kubectl logs -l app=task-manager

# See logs from MongoDB
kubectl logs -l app=mongodb
```

### Check Backend API Directly (via kubectl proxy)
```powershell
# Get all tasks via kubectl proxy
curl http://127.0.0.1:8001/api/v1/namespaces/default/services/http:task-manager:8080/proxy/api/tasks
```

---

## 🔧 Troubleshooting

### Problem: Docker Desktop won't start
**Solution**: 
- Restart your computer
- Ensure WSL2 is installed
- Check if virtualization is enabled in BIOS

### Problem: Minikube fails to start
**Solution**:
```powershell
# Delete and recreate
minikube delete
minikube start
```

### Problem: Pods stuck in "Pending"
**Solution**:
```powershell
# Check pod details
kubectl describe pod <pod-name>

# Usually resolved by waiting 2-3 minutes
```

### Problem: Pods stuck in "ImagePullBackOff"
**Solution**:
```powershell
# Load the Docker image into minikube
cd C:\placement\task2-kubernetes
docker build -t task-manager:v2 .
minikube image load task-manager:v2

# Restart the deployment
kubectl rollout restart deployment task-manager
```

### Problem: Frontend shows "Network Error"
**Solution**:
1. Ensure kubectl proxy is running on port 8001
2. Check backend pods are running: `kubectl get pods`
3. Restart frontend: Stop (Ctrl+C) and run `npm run dev` again

### Problem: MongoDB connection errors
**Solution**:
```powershell
# Check if MongoDB is running
kubectl get pods -l app=mongodb

# Check MongoDB logs
kubectl logs -l app=mongodb

# If needed, recreate MongoDB
kubectl delete -f mongodb-deployment.yaml
kubectl apply -f mongodb-deployment.yaml
```

---

## 🎯 Expected Terminal Layout

When everything is running, you should have:

**Terminal 1 - kubectl proxy**:
```
Starting to serve on 127.0.0.1:8001
(keep running)
```

**Terminal 2 - React Frontend**:
```
VITE v5.x.x ready in xxx ms
➜  Local:   http://localhost:3001/
(keep running)
```

**Terminal 3 - Monitoring (optional)**:
```powershell
kubectl get pods -w
```

---

## ⏱️ Startup Time Estimate

| Step | Time | Notes |
|------|------|-------|
| Docker Desktop start | 1-2 min | First time or after restart |
| Minikube start | 2-3 min | First time, ~30s if already initialized |
| Deploy to K8s | 2-3 min | Pulling images, starting pods |
| Frontend start | 10-20 sec | npm dev server |
| **Total** | **5-8 min** | One-time setup |

**After first setup**: Subsequent starts take only 2-3 minutes!

---

## 📝 Quick Reference Commands

### Start Everything
```powershell
# Terminal 1
minikube start
cd C:\placement\task2-kubernetes
kubectl apply -f .

# Terminal 2
kubectl proxy --port=8001

# Terminal 3
cd C:\placement\task3-react-frontend
npm run dev
```

### Stop Everything
```powershell
# Stop frontend (Terminal 3)
Ctrl + C

# Stop kubectl proxy (Terminal 2)
Ctrl + C

# Stop minikube (Terminal 1)
minikube stop
```

### Restart Just the Frontend
```powershell
cd C:\placement\task3-react-frontend
npm run dev
```

### Restart Just the Backend
```powershell
kubectl rollout restart deployment task-manager
```

---

## ✅ Success Checklist

Once everything is running, verify:

- [ ] Docker Desktop is running (whale icon in system tray)
- [ ] Minikube status shows "Running" (`minikube status`)
- [ ] All pods are "Running" (`kubectl get pods`)
- [ ] kubectl proxy shows "Starting to serve on 127.0.0.1:8001"
- [ ] Frontend shows "Local: http://localhost:3001/"
- [ ] Browser opens http://localhost:3001/ successfully
- [ ] Can create, view, edit, delete tasks
- [ ] Can execute tasks and see results

---

## 🎉 You're All Set!

All 5 tasks are now running:

✅ **Task 1**: Java Backend (running in Kubernetes)  
✅ **Task 2**: Kubernetes Deployment (pods running)  
✅ **Task 3**: React Frontend (http://localhost:3001/)  
✅ **Task 4**: CI/CD Pipeline (ready to trigger on GitHub)  
✅ **Task 5**: Data Science (88.42% model saved)

**Need help?** Check troubleshooting section above or ask for assistance!
