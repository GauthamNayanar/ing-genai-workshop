#!/bin/bash

set -euo pipefail

PROJECT_ID="${1:-}"
if [ -z "$PROJECT_ID" ]; then
    echo "Usage: bash $0 <PROJECT_ID>"
    exit 1
fi
echo "Using project ID: $PROJECT_ID"

# Install gcloud CLI if not already installed
echo "Checking for gcloud CLI..."
if command -v gcloud >/dev/null 2>&1; then
    echo "gcloud CLI is already installed."
else
    echo "gcloud CLI not found. Installing..."
    curl -sSL https://sdk.cloud.google.com | bash

    export PATH="$HOME/google-cloud-sdk/bin:$PATH"

    echo 'export PATH="$HOME/google-cloud-sdk/bin:$PATH"' >> ~/.bashrc
    echo "gcloud CLI installed successfully."
fi

# Set the active project explicitly
echo "Setting active project to: $PROJECT_ID"
gcloud config set project "$PROJECT_ID"


# 0. Download the login config JSON from WIF (replace the following command with the actual download command if needed)
echo "[0/3] Downloading one-day-sandbox-gcloud.json from WIF..."
gcloud iam workforce-pools create-login-config locations/global/workforcePools/sandbox-p/providers/entra --output-file=one-day-sandbox-gcloud.json

# 1. Re-login for gcloud CLI
echo "[1/3] Logging in to gcloud CLI..."
gcloud auth login --login-config=one-day-sandbox-gcloud.json

# 2. Re-login for ADC (Application Default Credentials)
echo "[2/3] Logging in for Application Default Credentials..."
gcloud auth application-default login --login-config=one-day-sandbox-gcloud.json

# 3. Set quota project again
echo "[3/3] Setting quota project..."
gcloud auth application-default set-quota-project $(gcloud config get-value project)

echo "Enabling required APIs..."
gcloud services enable aiplatform.googleapis.com --project="$PROJECT_ID"

echo "All authentication steps completed successfully."

# # 4. Revoke credentials after 24 hours (one day sandbox duration)
# gcloud auth application-default revoke
# gcloud auth revoke --all