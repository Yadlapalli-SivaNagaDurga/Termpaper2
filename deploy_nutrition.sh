#!/bin/bash

IMAGE_NAME="term-paper"
CONTAINER_NAME="determined_mcclintock"

# Verify container is running
if docker ps --format '{{.Names}}' | grep -q "^$CONTAINER_NAME$"; then
  echo "✅ Deployment successful: $CONTAINER_NAME is running."

  # Run Snyk monitor
  snyk monitor --docker $IMAGE_NAME
else
  echo "❌ Deployment failed: container $CONTAINER_NAME is not running."
fi
