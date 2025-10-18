# CI/CD Pipeline Setup Guide

## Overview

This CI/CD pipeline automates the build, test, and deployment process for the Task Manager application using GitHub Actions. The pipeline ensures code quality, security, and seamless deployment to multiple environments.

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Trigger Events                            │
│  • Push to main/develop                                      │
│  • Pull Request to main                                      │
│  • Manual workflow dispatch                                  │
└──────────────────────┬───────────────────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Backend   │ │  Frontend   │ │  Security   │
│   Build     │ │   Build     │ │   Scan      │
│   & Test    │ │   & Lint    │ │  (Trivy)    │
└──────┬──────┘ └──────┬──────┘ └─────────────┘
       │               │
       └───────┬───────┘
               ▼
     ┌─────────────────┐
     │ Docker Build    │
     │ & Push to       │
     │ Registry        │
     └────────┬────────┘
              │
     ┌────────┴────────┐
     │                 │
     ▼                 ▼
┌──────────┐     ┌──────────┐
│ Deploy   │     │ Deploy   │
│ Dev      │     │ Prod     │
│(develop) │     │ (main)   │
└──────────┘     └──────────┘
```

## Features

### 1. Continuous Integration (CI)

- **Backend (Java/Spring Boot)**
  - Maven build and compilation
  - Unit test execution
  - Test report generation
  - Artifact upload

- **Frontend (React/TypeScript)**
  - NPM dependency installation
  - Code linting (ESLint)
  - Production build
  - Static asset generation

### 2. Security Scanning

- **Trivy Security Scanner**
  - Filesystem vulnerability scanning
  - SARIF report generation
  - GitHub Security tab integration
  - Critical and high severity alerts

### 3. Container Management

- **Docker Build & Push**
  - Multi-stage Docker builds
  - Layer caching (GitHub Actions cache)
  - Image tagging strategy:
    - `latest` for main branch
    - Git SHA for version tracking
    - Branch name for feature branches

### 4. Continuous Deployment (CD)

- **Development Environment** (develop branch)
  - Automatic deployment on push
  - Quick iteration testing

- **Production Environment** (main branch)
  - Automatic deployment after security scan
  - Deployment summary generation
  - Manual approval option (GitHub Environments)

## Prerequisites

### GitHub Repository Secrets

You need to configure the following secrets in your GitHub repository:

1. **Docker Hub Credentials**
   ```
   DOCKER_USERNAME: Your Docker Hub username
   DOCKER_PASSWORD: Your Docker Hub password or access token
   ```

2. **Kubernetes Configuration (Optional)**
   ```
   KUBECONFIG: Base64-encoded kubeconfig file for K8s deployment
   ```

### Setting Up Secrets

1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with its name and value

#### Creating Docker Hub Access Token

```bash
# Login to Docker Hub
# Go to Account Settings → Security → New Access Token
# Copy the token and use it as DOCKER_PASSWORD
```

#### Encoding Kubeconfig (if using Kubernetes deployment)

```bash
# On Linux/Mac
cat ~/.kube/config | base64 -w 0

# On Windows (PowerShell)
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Content ~/.kube/config -Raw)))
```

## Workflow Configuration

### File Location
```
.github/
└── workflows/
    └── ci-cd.yml
```

### Environment Variables

The pipeline uses the following environment variables:

```yaml
env:
  DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
  IMAGE_NAME: task-manager
  IMAGE_TAG: ${{ github.sha }}
  JAVA_VERSION: '17'
  NODE_VERSION: '20'
```

### Jobs Overview

#### 1. `build-and-test-backend`
- Runs on: `ubuntu-latest`
- Triggers: All push and PR events
- Actions:
  - Checkout code
  - Setup JDK 17
  - Maven build
  - Run unit tests
  - Upload JAR artifact

#### 2. `build-frontend`
- Runs on: `ubuntu-latest`
- Triggers: All push and PR events
- Actions:
  - Checkout code
  - Setup Node.js 20
  - Install dependencies
  - Lint code
  - Build production bundle
  - Upload dist artifact

#### 3. `docker-build-and-push`
- Runs on: `ubuntu-latest`
- Triggers: Push to main or develop
- Depends on: `build-and-test-backend`
- Actions:
  - Setup Docker Buildx
  - Login to Docker Hub
  - Build multi-arch image
  - Push to registry with tags

#### 4. `security-scan`
- Runs on: `ubuntu-latest`
- Triggers: All push and PR events
- Actions:
  - Run Trivy scanner
  - Generate SARIF report
  - Upload to GitHub Security

#### 5. `deploy-dev`
- Runs on: `ubuntu-latest`
- Triggers: Push to develop
- Environment: `development`
- Actions:
  - Deploy to dev environment

#### 6. `deploy-production`
- Runs on: `ubuntu-latest`
- Triggers: Push to main
- Environment: `production`
- Depends on: Security scan pass
- Actions:
  - Deploy to production
  - Create deployment summary

#### 7. `notify`
- Runs on: `ubuntu-latest`
- Triggers: Always (after deployment)
- Actions:
  - Send deployment status

## Usage

### Automatic Triggers

1. **Push to `develop` branch**
   ```bash
   git checkout develop
   git add .
   git commit -m "feat: add new feature"
   git push origin develop
   ```
   Result: Runs CI → Build Docker → Deploy to Dev

2. **Push to `main` branch**
   ```bash
   git checkout main
   git merge develop
   git push origin main
   ```
   Result: Runs CI → Security Scan → Build Docker → Deploy to Production

3. **Pull Request to `main`**
   ```bash
   git checkout -b feature/my-feature
   git push origin feature/my-feature
   # Create PR on GitHub
   ```
   Result: Runs CI → Security Scan (no deployment)

### Manual Trigger

1. Go to **Actions** tab in GitHub
2. Select **CI/CD Pipeline for Task Manager**
3. Click **Run workflow**
4. Select branch and click **Run workflow**

## Docker Image Tags

The pipeline creates the following Docker image tags:

- `username/task-manager:latest` - Latest main branch build
- `username/task-manager:abc1234` - Git commit SHA
- `username/task-manager:main` - Main branch
- `username/task-manager:develop` - Develop branch

## Deployment Strategies

### Local Minikube Deployment

After the pipeline builds and pushes images, deploy to local minikube:

```bash
# Pull the latest image
docker pull yourusername/task-manager:latest

# Load into minikube
minikube image load yourusername/task-manager:latest

# Update deployment
kubectl set image deployment/task-manager task-manager=yourusername/task-manager:latest

# Or apply the deployment
kubectl apply -f task2-kubernetes/app-deployment.yaml
```

### Production Kubernetes Deployment

Update the deployment to use CI-built images:

```yaml
# task2-kubernetes/app-deployment.yaml
spec:
  containers:
  - name: task-manager
    image: yourusername/task-manager:latest
    imagePullPolicy: Always
```

Then apply:
```bash
kubectl apply -f task2-kubernetes/app-deployment.yaml
kubectl rollout status deployment/task-manager
```

## Monitoring and Debugging

### View Pipeline Logs

1. Go to **Actions** tab
2. Click on the workflow run
3. Select a job to view logs

### Common Issues

#### 1. Maven Build Failure
- Check Java version compatibility
- Verify `pom.xml` syntax
- Check test failures

#### 2. Docker Build Failure
- Verify Dockerfile syntax
- Check build context
- Verify base image availability

#### 3. Docker Push Failure
- Verify Docker Hub credentials
- Check repository permissions
- Verify image name format

#### 4. Deployment Failure
- Check KUBECONFIG secret
- Verify Kubernetes cluster access
- Check deployment YAML syntax

### Troubleshooting Commands

```bash
# Check workflow runs
gh run list

# View workflow run details
gh run view <run-id>

# Re-run failed workflow
gh run rerun <run-id>

# Check secrets
gh secret list
```

## Security Best Practices

1. **Never commit secrets** - Use GitHub Secrets
2. **Scan dependencies** - Trivy runs automatically
3. **Review security alerts** - Check Security tab
4. **Use minimal base images** - Alpine Linux for production
5. **Enable branch protection** - Require PR reviews
6. **Use environment protection** - Manual approval for production

## Extending the Pipeline

### Add Slack Notifications

```yaml
- name: Send Slack notification
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {
        "text": "Deployment successful! 🎉"
      }
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Add Performance Testing

```yaml
- name: Run performance tests
  run: |
    npm install -g artillery
    artillery run perf-tests.yml
```

### Add Database Migration

```yaml
- name: Run database migrations
  run: |
    cd task1-java-backend
    mvn flyway:migrate
```

## Pipeline Metrics

Track the following metrics for your pipeline:

- **Build Time**: Average time for CI jobs
- **Test Coverage**: Percentage of code covered by tests
- **Deployment Frequency**: How often you deploy
- **Failure Rate**: Percentage of failed deployments
- **Mean Time to Recovery**: Time to fix failed deployments

## Next Steps

1. ✅ Configure GitHub Secrets
2. ✅ Test the pipeline with a commit
3. ✅ Review security scan results
4. ✅ Set up environment protection rules
5. ✅ Configure deployment notifications
6. ✅ Add monitoring and alerting

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Trivy Security Scanner](https://github.com/aquasecurity/trivy)
- [Kubernetes Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

## Support

For issues or questions:
- Check the Actions logs in GitHub
- Review the troubleshooting section
- Check security scan results
- Verify all secrets are configured correctly
