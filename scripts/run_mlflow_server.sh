#!/bin/bash
# Minimal local MLflow server launcher for quick experiments. The macOS
# deployment variant uses a SQLite backend and explicit artifact directory.

mlflow server --host 127.0.0.1 --port 5000
