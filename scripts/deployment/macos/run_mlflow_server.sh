#!/bin/bash
# Launch a local MLflow tracking server with a SQLite backend and local artifact
# directory under `mlflow_store/`.

# Create directories for the backend store and artifacts if they don't exist
mkdir -p mlflow_store/artifacts

mlflow server \
    --backend-store-uri sqlite:///mlflow_store/mlflow.db \
    --default-artifact-root ./mlflow_store/artifacts \
    --host 127.0.0.1 \
    --port 5000
