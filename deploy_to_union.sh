#!/bin/bash

# Deployment script for Union AI / Internal Platform
# Adjust based on your organization's Union AI setup

echo "🚀 Deploying HTS Survey Explorer to Union AI"

# Step 1: Build Docker image
echo "Building Docker image..."
docker build -t hts-survey-explorer:latest .

# Step 2: Tag for your internal registry
# Replace with your actual registry URL
REGISTRY="your-company-registry.com"
docker tag hts-survey-explorer:latest $REGISTRY/hts-survey-explorer:latest

# Step 3: Push to internal registry
echo "Pushing to internal registry..."
docker push $REGISTRY/hts-survey-explorer:latest

# Step 4: Deploy to Union AI
echo "Deploying to Union AI..."

# Option A: Using Union CLI
union run union_app.py

# Option B: Using kubectl if Union uses Kubernetes
# kubectl apply -f union-deploy.yaml

# Option C: Using Flyte CLI
# flytectl create execution --project hts --domain production --workflow deploy_hts_explorer

echo "✅ Deployment complete!"
echo "Check your Union AI dashboard for the app URL"