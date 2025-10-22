#!/bin/bash
# Deployment script

# Build and test
echo "Running tests..."
pytest

# If tests pass, deploy
if [ $? -eq 0 ]; then
    echo "Tests passed, deploying..."
    vercel --prod
else
    echo "Tests failed, aborting deployment"
    exit 1
fi
