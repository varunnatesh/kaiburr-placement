# Main Project README

## Kaiburr Placement Tasks - Complete Submission

This repository contains all 5 tasks completed as part of the Kaiburr placement process.

### 📁 Project Structure

```
placement/
├── task1-java-backend/          # Task 1: Java REST API
├── task2-kubernetes/            # Task 2: Kubernetes Deployment
├── task3-react-frontend/        # Task 3: React UI
├── task4-cicd-pipeline/         # Task 4: CI/CD Pipeline
└── task5-data-science/          # Task 5: Text Classification
```

### ✅ Completed Tasks

#### Task 1: Java Backend REST API
- ✅ Spring Boot application with REST endpoints
- ✅ MongoDB integration
- ✅ CRUD operations for tasks
- ✅ Command validation
- ✅ Task execution functionality
- 📂 [View Task 1](./task1-java-backend/)

#### Task 2: Kubernetes Deployment
- ✅ Dockerfile for containerization
- ✅ Kubernetes manifests (Deployment, Service, PV, PVC)
- ✅ MongoDB with persistent storage
- ✅ Kubernetes API integration for pod-based execution
- ✅ RBAC configuration
- 📂 [View Task 2](./task2-kubernetes/)

#### Task 3: React Frontend
- ✅ React 19 with TypeScript
- ✅ Ant Design UI components
- ✅ Full CRUD operations
- ✅ Task execution and history viewing
- ✅ Accessibility features (WCAG 2.1 AA)
- ✅ Responsive design
- 📂 [View Task 3](./task3-react-frontend/)

#### Task 4: CI/CD Pipeline
- ✅ GitHub Actions workflow
- ✅ Automated build and test
- ✅ Docker image build and push
- ✅ Security scanning with Trivy
- ✅ Automated deployment to Kubernetes
- 📂 [View Task 4](./task4-cicd-pipeline/)

#### Task 5: Data Science
- ✅ Consumer complaint text classification
- ✅ EDA and visualization
- ✅ Text preprocessing
- ✅ Multiple ML models (Logistic Regression, Naive Bayes, Random Forest, SVM, XGBoost)
- ✅ Model comparison and evaluation
- ✅ Prediction on new data
- 📂 [View Task 5](./task5-data-science/)

### 🚀 Quick Start Guide

#### Prerequisites
- Java 17+
- Node.js 20+
- Docker Desktop with Kubernetes
- Python 3.9+
- MongoDB
- Maven
- npm

#### Task 1: Java Backend
```powershell
cd task1-java-backend
mvn clean install
mvn spring-boot:run
```

#### Task 2: Kubernetes
```powershell
cd task2-kubernetes
docker build -t task-manager:latest .
kubectl apply -f mongodb-pv.yaml
kubectl apply -f mongodb-deployment.yaml
kubectl apply -f service-account.yaml
kubectl apply -f app-deployment.yaml
```

#### Task 3: React Frontend
```powershell
cd task3-react-frontend
npm install
npm run dev
```

#### Task 4: CI/CD
```powershell
# Push to GitHub to trigger pipeline
git add .
git commit -m "Initial commit"
git push origin main
```

#### Task 5: Data Science
```powershell
cd task5-data-science
pip install -r requirements.txt
jupyter notebook
```

### 📊 Technology Stack

**Backend:**
- Java 17
- Spring Boot 3.2.0
- MongoDB
- Maven

**Frontend:**
- React 19
- TypeScript
- Ant Design
- Vite

**DevOps:**
- Docker
- Kubernetes
- GitHub Actions

**Data Science:**
- Python
- Scikit-learn
- XGBoost
- NLTK
- Pandas, NumPy

### 📸 Screenshots

Each task directory contains a `README.md` with detailed instructions and placeholders for screenshots showing:
- Application running
- API requests and responses
- UI interactions
- Kubernetes deployments
- CI/CD pipeline execution
- Model training and evaluation results
- Your name and timestamp

### 📝 Submission Checklist

- ✅ Each task in separate directory
- ✅ README.md for each task
- ✅ Screenshots embedded in READMEs
- ✅ Code well-structured and documented
- ✅ All requirements met
- ✅ Git repository ready for submission

### 🔗 Separate Repositories

For submission, create separate GitHub repositories:
1. `task1-java-backend` → GitHub Repo 1
2. `task2-kubernetes` → GitHub Repo 2
3. `task3-react-frontend` → GitHub Repo 3
4. `task4-cicd-pipeline` → GitHub Repo 4
5. `task5-data-science` → GitHub Repo 5

### 📧 Contact

**Author:** VARUN K N  
**Email:** varunnatesh10@gmail.com  
**Date:** October 16, 2025

