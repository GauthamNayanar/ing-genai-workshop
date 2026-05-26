#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

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

echo "All authentication steps completed successfully."

# # 4. Revoke credentials after 24 hours (one day sandbox duration)
# gcloud auth application-default revoke
# gcloud auth revoke --all