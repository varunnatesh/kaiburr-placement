# CI/CD Pipeline Quick Start

## Step 1: Configure GitHub Secrets

### Required Secrets

1. **DOCKER_USERNAME** - Your Docker Hub username
2. **DOCKER_PASSWORD** - Your Docker Hub access token

### How to Add Secrets

```bash
# Using GitHub CLI
gh secret set DOCKER_USERNAME
gh secret set DOCKER_PASSWORD

# Or via GitHub UI:
# Settings → Secrets and variables → Actions → New repository secret
```

### Create Docker Hub Access Token

1. Login to [Docker Hub](https://hub.docker.com/)
2. Go to **Account Settings** → **Security**
3. Click **New Access Token**
4. Name it: `github-actions-ci-cd`
5. Copy the token (you won't see it again!)
6. Use this as `DOCKER_PASSWORD` secret

## Step 2: Initialize Git Repository (if not already done)

```powershell
# Navigate to project root
cd C:\placement

# Initialize git (if needed)
git init

# Add remote repository
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git

# Create .gitignore
@"
# Java
target/
*.jar
*.class
*.log

# Node
node_modules/
dist/
npm-debug.log*

# IDE
.vscode/
.idea/
*.iml

# OS
.DS_Store
Thumbs.db

# Kubernetes
*.kubeconfig
"@ | Out-File -FilePath .gitignore -Encoding utf8

# Add all files
git add .

# Commit
git commit -m "Initial commit with CI/CD pipeline"

# Push to main branch
git branch -M main
git push -u origin main
```

## Step 3: Create Development Branch

```powershell
# Create and checkout develop branch
git checkout -b develop

# Push develop branch
git push -u origin develop
```

## Step 4: Test the Pipeline

### Option A: Make a test commit

```powershell
# Make a small change
echo "# Test CI/CD" >> README.md

# Commit and push to develop
git add README.md
git commit -m "test: trigger CI/CD pipeline"
git push origin develop
```

### Option B: Manual trigger

1. Go to your GitHub repository
2. Click on **Actions** tab
3. Select **CI/CD Pipeline for Task Manager**
4. Click **Run workflow** button
5. Select branch (main or develop)
6. Click **Run workflow**

## Step 5: Monitor Pipeline Execution

### Via GitHub UI

1. Go to **Actions** tab
2. Click on the running workflow
3. Watch jobs execute in real-time
4. Check logs for each step

### Via GitHub CLI

```powershell
# List recent workflow runs
gh run list

# Watch a specific run
gh run watch

# View run details
gh run view --log
```

## Step 6: Verify Docker Image

After successful pipeline run:

```powershell
# Check Docker Hub for your image
# Visit: https://hub.docker.com/r/YOUR-USERNAME/task-manager

# Pull the image locally
docker pull YOUR-USERNAME/task-manager:latest

# List local images
docker images | Select-String "task-manager"
```

## Step 7: Deploy Updated Image to Minikube

```powershell
# Pull the CI-built image
docker pull YOUR-USERNAME/task-manager:latest

# Load into minikube
minikube image load YOUR-USERNAME/task-manager:latest

# Update deployment to use your Docker Hub image
cd C:\placement\task2-kubernetes

# Edit app-deployment.yaml to use your image
# Change: image: task-manager:v2
# To:     image: YOUR-USERNAME/task-manager:latest

# Apply the updated deployment
kubectl apply -f app-deployment.yaml

# Wait for rollout
kubectl rollout status deployment/task-manager

# Verify new pod is running
kubectl get pods -l app=task-manager
```

## Common Workflows

### Deploy a New Feature

```powershell
# Create feature branch
git checkout develop
git pull origin develop
git checkout -b feature/new-awesome-feature

# Make your changes
# ... edit files ...

# Commit changes
git add .
git commit -m "feat: add awesome new feature"

# Push feature branch
git push origin feature/new-awesome-feature

# Create Pull Request on GitHub
# After PR is merged to develop, pipeline will:
# 1. Run tests
# 2. Build Docker image
# 3. Deploy to development environment
```

### Release to Production

```powershell
# Checkout main branch
git checkout main
git pull origin main

# Merge develop into main
git merge develop

# Tag the release
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push to main
git push origin main
git push origin v1.0.0

# Pipeline will:
# 1. Run all tests
# 2. Run security scan
# 3. Build Docker image with 'latest' tag
# 4. Deploy to production
```

### Hotfix for Production

```powershell
# Create hotfix branch from main
git checkout main
git checkout -b hotfix/critical-bug-fix

# Fix the bug
# ... edit files ...

# Commit fix
git add .
git commit -m "fix: critical bug in authentication"

# Push hotfix
git push origin hotfix/critical-bug-fix

# Create PR to main
# After merge, pipeline deploys immediately
```

## Viewing Pipeline Results

### GitHub Actions Dashboard

```
Repository → Actions → CI/CD Pipeline for Task Manager
```

You'll see:
- ✅ **Green checkmark**: All jobs passed
- ❌ **Red X**: One or more jobs failed
- 🟡 **Yellow circle**: Pipeline is running

### Job Details

Click on any workflow run to see:
- **Jobs**: All pipeline jobs (build, test, deploy)
- **Logs**: Detailed execution logs
- **Artifacts**: Built JARs, test reports, etc.
- **Summary**: Deployment information

### Security Scan Results

```
Repository → Security → Code scanning alerts
```

View Trivy security scan results:
- Critical vulnerabilities
- High severity issues
- Affected dependencies
- Remediation suggestions

## Troubleshooting

### Pipeline Fails on Backend Build

```powershell
# Check if project builds locally
cd C:\placement\task1-java-backend

# Try building with Maven (if installed)
mvn clean install

# Or use Docker to build
cd C:\placement
docker build -f task2-kubernetes\Dockerfile .
```

### Pipeline Fails on Frontend Build

```powershell
# Check if frontend builds locally
cd C:\placement\task3-react-frontend

# Install dependencies
npm install

# Try building
npm run build

# Check for linting errors
npm run lint
```

### Docker Push Fails

1. Verify secrets are set correctly:
   ```powershell
   gh secret list
   ```

2. Test Docker Hub login locally:
   ```powershell
   docker login
   # Enter your username and access token
   ```

3. Check image name format:
   - Should be: `username/task-manager:tag`
   - Not: `task-manager:tag`

### Deployment Doesn't Update

```powershell
# Force pull new image
kubectl rollout restart deployment/task-manager

# Check image being used
kubectl describe pod -l app=task-manager | Select-String "Image:"

# Delete pod to force recreation
kubectl delete pod -l app=task-manager
```

## Pipeline Status Badge

Add this to your README.md to show pipeline status:

```markdown
[![CI/CD Pipeline](https://github.com/YOUR-USERNAME/YOUR-REPO/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/YOUR-USERNAME/YOUR-REPO/actions/workflows/ci-cd.yml)
```

## Next Steps

- ✅ Set up GitHub Secrets
- ✅ Push code to GitHub
- ✅ Verify pipeline runs successfully
- ✅ Update deployment to use CI-built images
- ✅ Set up branch protection rules
- ✅ Configure deployment environments
- ⬜ Add Slack/email notifications
- ⬜ Set up automated database migrations
- ⬜ Add performance testing
- ⬜ Configure monitoring and logging

## Additional Resources

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Docker Hub**: https://hub.docker.com/
- **GitHub CLI**: https://cli.github.com/
- **Full Setup Guide**: See `CI-CD-SETUP.md`

## Questions?

Check the detailed setup guide in `CI-CD-SETUP.md` or review the workflow file at `.github/workflows/ci-cd.yml`.
