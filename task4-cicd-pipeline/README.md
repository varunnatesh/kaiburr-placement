# Task 4: CI/CD Pipeline

## Overview
Automated CI/CD pipeline using GitHub Actions for building, testing, and deploying the Task Manager application. Includes code build, Docker image creation, security scanning, and automated deployment.

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions Pipeline                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Trigger: Push to main/develop               │
│                  or Pull Request to main                     │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
        ┌───────────────────┐  ┌───────────────────┐
        │  Build & Test     │  │  Build Frontend   │
        │  Java Backend     │  │  React App        │
        │                   │  │                   │
        │  • Maven Build    │  │  • npm install    │
        │  • Run Tests      │  │  • Lint Code      │
        │  • Upload JAR     │  │  • Build          │
        └─────────┬─────────┘  └─────────┬─────────┘
                  │                      │
                  └──────────┬───────────┘
                             ▼
                  ┌─────────────────────┐
                  │  Docker Build       │
                  │  & Push             │
                  │                     │
                  │  • Build Image      │
                  │  • Push to Registry │
                  │  • Tag with SHA     │
                  └──────────┬──────────┘
                             │
                  ┌──────────┴──────────┐
                  │                     │
                  ▼                     ▼
       ┌─────────────────┐   ┌─────────────────┐
       │ Security Scan   │   │ Deploy Staging  │
       │                 │   │                 │
       │ • Trivy Scan    │   │ • Update K8s    │
       │ • Upload SARIF  │   │ • Rollout       │
       └─────────────────┘   └────────┬────────┘
                                      │
                                      ▼
                           ┌─────────────────┐
                           │  Notifications  │
                           │                 │
                           │  • Success ✅   │
                           │  • Failure ❌   │
                           └─────────────────┘
```

## Features

### ✅ Automated Build Process
- Java backend build with Maven
- React frontend build with npm
- Artifact uploading for downstream jobs
- Dependency caching for faster builds

### ✅ Testing
- Unit tests for backend
- Linting for frontend
- Test result reporting

### ✅ Docker Image Management
- Multi-stage Docker build
- Image tagging with Git SHA
- Push to Docker Hub
- Build caching for optimization

### ✅ Security
- Trivy vulnerability scanning
- Security report upload to GitHub
- Code quality checks

### ✅ Deployment
- Automated deployment to staging
- Kubernetes rollout management
- Deployment verification
- Environment protection

### ✅ Notifications
- Success/failure notifications
- Slack integration (configurable)

## Pipeline Jobs

### 1. build-and-test-backend
**Purpose:** Build and test the Java application

**Steps:**
- Checkout code
- Setup JDK 17
- Maven build
- Run unit tests
- Upload JAR artifact

**Triggers:** All pushes and PRs

### 2. build-frontend
**Purpose:** Build the React frontend

**Steps:**
- Checkout code
- Setup Node.js 20
- Install dependencies
- Lint code
- Build production bundle
- Upload build artifact

**Triggers:** All pushes and PRs

### 3. docker-build-and-push
**Purpose:** Create and publish Docker image

**Steps:**
- Download backend JAR
- Setup Docker Buildx
- Login to Docker Hub
- Build multi-platform image
- Push to registry
- Tag with multiple formats

**Triggers:** Push to main branch only

### 4. security-scan
**Purpose:** Scan for vulnerabilities

**Steps:**
- Run Trivy scanner
- Generate SARIF report
- Upload to GitHub Security

**Triggers:** All pushes and PRs

### 5. deploy-staging
**Purpose:** Deploy to staging environment

**Steps:**
- Setup kubectl
- Configure cluster access
- Update deployment
- Wait for rollout
- Verify deployment

**Triggers:** Push to main branch only

### 6. notify
**Purpose:** Send deployment notifications

**Steps:**
- Check job status
- Send appropriate notification

**Triggers:** After deployment job

## Setup Instructions

### Step 1: Fork/Create Repository

1. Create a new GitHub repository for your project
2. Push your code to the repository

### Step 2: Configure Secrets

Go to Settings → Secrets and Variables → Actions and add:

#### Required Secrets

**Docker Hub:**
- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub password or access token

**Kubernetes (for deployment):**
- `KUBECONFIG` - Base64 encoded kubeconfig file
  ```powershell
  # Generate base64 kubeconfig
  $kubeconfig = Get-Content ~/.kube/config -Raw
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($kubeconfig)
  $encoded = [Convert]::ToBase64String($bytes)
  Write-Output $encoded
  ```

**Optional Secrets:**
- `SLACK_WEBHOOK_URL` - For Slack notifications

### Step 3: Enable GitHub Actions

1. Go to the Actions tab in your repository
2. Enable workflows if prompted
3. The pipeline will trigger automatically on push

### Step 4: Configure Environments

1. Go to Settings → Environments
2. Create `staging` environment
3. Add protection rules:
   - Required reviewers (optional)
   - Wait timer (optional)
4. Add environment-specific variables if needed

## Pipeline Configuration

### File Location
`.github/workflows/ci-cd.yml`

### Trigger Configuration

```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
```

### Environment Variables

```yaml
env:
  DOCKER_USERNAME: ${{ secrets.DOCKER_USERNAME }}
  DOCKER_PASSWORD: ${{ secrets.DOCKER_PASSWORD }}
  IMAGE_NAME: task-manager
  IMAGE_TAG: ${{ github.sha }}
```

## Docker Image Tagging Strategy

Images are tagged with multiple formats:
- `latest` - Latest build from main branch
- `<branch-name>` - Latest build from specific branch
- `<git-sha>` - Specific commit (immutable)

Example:
- `username/task-manager:latest`
- `username/task-manager:main`
- `username/task-manager:a1b2c3d`

## Deployment Process

### Staging Deployment
1. Pipeline runs on push to main
2. Docker image is built and pushed
3. Kubernetes deployment is updated
4. Rollout is verified
5. Notification is sent

### Manual Deployment Trigger
You can manually trigger deployment from GitHub Actions UI:
1. Go to Actions tab
2. Select the workflow
3. Click "Run workflow"
4. Select branch

## Monitoring and Debugging

### View Pipeline Logs
1. Go to Actions tab
2. Click on a workflow run
3. View logs for each job

### Common Issues

#### Build Failures
**Problem:** Maven or npm build fails
**Solution:** Check build logs, ensure dependencies are available

#### Docker Push Fails
**Problem:** Authentication error
**Solution:** Verify DOCKER_USERNAME and DOCKER_PASSWORD secrets

#### Deployment Fails
**Problem:** Cannot connect to Kubernetes
**Solution:** Verify KUBECONFIG secret is correct

#### Security Scan Warnings
**Problem:** Vulnerabilities found
**Solution:** Update dependencies, review Trivy report

## Extending the Pipeline

### Add More Environments

```yaml
deploy-production:
  name: Deploy to Production
  needs: [deploy-staging]
  runs-on: ubuntu-latest
  environment:
    name: production
    url: https://taskmanager.example.com
  # ... deployment steps
```

### Add Integration Tests

```yaml
integration-tests:
  name: Run Integration Tests
  needs: [deploy-staging]
  runs-on: ubuntu-latest
  steps:
    - name: Run API tests
      run: |
        npm install -g newman
        newman run tests/postman-collection.json
```

### Add Performance Testing

```yaml
performance-tests:
  name: Performance Tests
  needs: [deploy-staging]
  runs-on: ubuntu-latest
  steps:
    - name: Run k6 tests
      run: |
        k6 run tests/load-test.js
```

## Best Practices Implemented

✅ **Separation of Concerns** - Each job has a specific purpose
✅ **Fail Fast** - Tests run before deployment
✅ **Artifact Management** - Build once, deploy many times
✅ **Security First** - Vulnerability scanning integrated
✅ **Caching** - Dependencies cached for speed
✅ **Immutable Artifacts** - Git SHA tagging
✅ **Environment Protection** - Staging environment with controls
✅ **Notifications** - Team stays informed

## Local Testing

### Test Docker Build Locally

```powershell
# Build image
docker build -t task-manager:local -f task2-kubernetes/Dockerfile task2-kubernetes

# Run container
docker run -p 8080:8080 -e MONGODB_URI=mongodb://host.docker.internal:27017/taskmanager task-manager:local
```

### Test Frontend Build Locally

```powershell
cd task3-react-frontend
npm install
npm run build
npm run preview
```

## Metrics and Reporting

The pipeline provides:
- Build duration
- Test results
- Security scan results
- Deployment status
- Artifact sizes

View these in the Actions tab summary.

## Cost Optimization

- Uses GitHub's free tier effectively
- Caches dependencies to reduce build time
- Conditional jobs (only deploy on main branch)
- Artifact retention limited to 7 days

## Alternative CI/CD Tools

This pipeline can be adapted for:
- **Jenkins** - Use Jenkinsfile
- **GitLab CI** - Use .gitlab-ci.yml
- **Azure DevOps** - Use azure-pipelines.yml
- **AWS CodePipeline** - Use buildspec.yml
- **CircleCI** - Use .circleci/config.yml

## Screenshots Checklist

[Add screenshots showing:]
1. GitHub Actions workflow running
2. Successful build completion
3. Docker image in Docker Hub
4. Security scan results
5. Deployment to staging
6. Kubernetes pods after deployment
7. Failed build with error messages (for demonstration)
8. Notifications received
9. Your name and timestamp visible

## Additional Files

### .dockerignore
```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
screenshots
```

### .gitignore additions
```
# Build artifacts
target/
dist/
build/

# CI/CD
kubeconfig.yaml
*.sarif
```

## Security Considerations

- Secrets are never logged or exposed
- Kubeconfig is base64 encoded
- Docker credentials use tokens, not passwords
- Security scans run on every build
- SARIF reports uploaded for tracking

## Maintenance

### Update Dependencies
- Review Dependabot alerts
- Update base images regularly
- Keep Actions versions current

### Monitor Performance
- Track build times
- Optimize slow jobs
- Review cache hit rates

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Trivy Scanner](https://github.com/aquasecurity/trivy)
- [Kubernetes Deployment Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)

## Author
[Your Name]
Date: October 16, 2025

## Next Steps
Complete Task 5: Data Science text classification project
