# Deployment Bundle

This document outlines the files and directories that should be included in the deployment bundle when transferring the project to the HPC cluster.

## Bundle Contents

-   `src/`: The main source code for the RAG pipeline.
-   `scripts/`: All scripts, including data preparation, vector store creation, and deployment scripts.
-   `docs/`: The input documents used for the RAG system (Google Sites extracts, ServiceNow files, etc.).
-   `vector_index/faiss_amarel/`: The persisted FAISS index directory.
-   `./models/`: A directory containing the `.gguf` model file(s). Start with a small-to-medium sized model (e.g., 8B 4-bit quant).
-   `requirements.txt`: The list of Python dependencies.
-   `.env.example`: An example environment file. Do not include the actual `.env` file with secrets.

## Pre-Deployment Checklist

-   [ ] Ensure the persisted FAISS index in `vector_index/faiss_amarel/` is up-to-date.
-   [ ] Verify that the model file specified in the configuration is present in the `./models/` directory.
-   [ ] Make sure the `scripts/deployment/hpc/setup_hpc.sh` script is executable (`chmod +x scripts/deployment/hpc/setup_hpc.sh`).
-   [ ] Review `requirements.txt` to ensure all necessary packages are listed.

## Notes

-   Do not include the local `.venv` directory in the bundle. The environment will be rebuilt on the cluster.
-   Store large model files on a high-performance filesystem on the cluster (e.g., `$SCRATCH`) rather than in the home directory.