# 🚀 Deploying to Union AI / Internal Platform (like ASter)

## Overview
You can use your GitHub repo but deploy to Union AI instead of Streamlit Cloud. This keeps your app within your company's infrastructure.

## Method 1: Direct Docker Deployment

### Step 1: Build & Push Docker Image
```bash
# Build the Docker image
docker build -t hts-survey-explorer:latest .

# Tag for your internal registry (replace with your company's registry)
docker tag hts-survey-explorer:latest your-registry.company.com/hts-survey-explorer:latest

# Push to internal registry
docker push your-registry.company.com/hts-survey-explorer:latest
```

### Step 2: Deploy on Union AI
```bash
# Use Union CLI (if available)
union app deploy \
  --name hts-survey-explorer \
  --image your-registry.company.com/hts-survey-explorer:latest \
  --port 8501 \
  --replicas 1
```

## Method 2: Using Flyte/Union Workflows

### Step 1: Register the workflow
```bash
# Register with Union/Flyte
pyflyte register union_app.py \
  --project your-project \
  --domain production \
  --version v1
```

### Step 2: Execute the workflow
```bash
flytectl create execution \
  --project your-project \
  --domain production \
  --workflow deploy_hts_explorer
```

## Method 3: ASter-Style Deployment

If your ASter tool has specific requirements:

### Step 1: Create ASter config
```yaml
# aster-config.yaml
app:
  name: hts-survey-explorer
  type: streamlit
  source:
    type: github
    repo: https://github.com/YOUR_USERNAME/hts-survey-explorer.git
    branch: main

  runtime:
    python: "3.9"
    memory: "1Gi"
    cpu: "1"

  environment:
    STREAMLIT_SERVER_PORT: "8501"
    STREAMLIT_SERVER_ADDRESS: "0.0.0.0"

  expose:
    port: 8501
    path: "/"
```

### Step 2: Deploy with ASter
```bash
aster deploy -f aster-config.yaml
```

## Method 4: Kubernetes Deployment (if Union uses K8s)

```bash
# Apply the Kubernetes configuration
kubectl apply -f union-deploy.yaml

# Check deployment status
kubectl get pods -l app=hts-survey-explorer

# Get the service URL
kubectl get service hts-survey-explorer-service
```

## 🔧 Environment Variables

Add these to your Union AI deployment:
```
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

## 📝 GitHub Integration

Your Union AI can pull directly from GitHub:

1. **Set up Deploy Key** in your GitHub repo:
   - Go to Settings → Deploy keys
   - Add your Union AI's public SSH key

2. **Configure Union AI** to pull from GitHub:
   ```yaml
   source:
     type: git
     url: git@github.com:YOUR_USERNAME/hts-survey-explorer.git
     branch: main
     ssh_key: ${UNION_DEPLOY_KEY}
   ```

3. **Auto-deploy on push** (optional):
   - Set up webhook in GitHub → Settings → Webhooks
   - Point to your Union AI webhook URL
   - Select "Push" events

## 🎯 Quick Steps Summary

1. ✅ Your code is in GitHub
2. Build Docker image: `docker build -t hts-survey-explorer .`
3. Push to your internal registry
4. Deploy using Union CLI or your ASter tool
5. Share internal URL with team

## 💡 Benefits of Union AI over Streamlit Cloud

- ✅ **Internal only** - Stays within company network
- ✅ **Better security** - Your company's auth/SSO
- ✅ **More control** - Custom resources, scaling
- ✅ **Integration** - Works with other internal tools
- ✅ **No external dependencies** - All within your infrastructure

## Need Help?

Contact your DevOps team or whoever manages ASter/Union AI for:
- Registry URL
- Deployment permissions
- Specific Union AI commands for your org
- Internal DNS/URL for your app