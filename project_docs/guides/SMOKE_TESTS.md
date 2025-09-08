# Smoke Tests

This document outlines the smoke tests to be performed before and after deploying the application to the HPC cluster.

## Local (CPU) Smoke Test

This test should be run on your local machine before deploying to the HPC cluster.

1.  **Prerequisites:**
    *   The FAISS index has been created and is available in the `vector_index/faiss_amarel/` directory.
    *   The required Python packages are installed in your local virtual environment.
    *   A `.gguf` model is available, and the path is correctly set in your environment.

2.  **Execution:**
    *   Run the chat harness in CLI mode:
        ```bash
        python scripts/deployment/hpc/chat_hpc.py --faiss-dir vector_index/faiss_amarel/
        ```

3.  **Verification:**
    *   Ask 2-3 questions from your "golden" Q&A list.
    *   Confirm that the answers are grounded in the document content and are not hallucinations.
    *   Verify that the application logs show the FAISS index being loaded correctly.

## HPC (GPU) Smoke Test

This test should be run after deploying the application to the HPC cluster.

1.  **Prerequisites:**
    *   The deployment bundle has been transferred to the cluster.
    *   The `setup_hpc.sh` script has been run successfully.
    *   The Slurm batch script (`run_chat_hpc.sbatch`) is configured with the correct paths.

2.  **Execution:**
    *   Submit the Slurm job:
        ```bash
        sbatch scripts/deployment/hpc/run_chat_hpc.sbatch
        ```

3.  **Verification:**
    *   Check the job log file (e.g., `logs/rag_chat_hpc_<JOBID>.out`).
    *   Verify that the log contains messages indicating that `llama.cpp` is using CUBLAS and that GPU layers are being offloaded.
    *   Confirm that the FAISS index was loaded from the persisted directory.
    *   Examine the answers to the sample questions in the log to ensure they are still grounded and correct.
    *   Use `nvidia-smi` on the compute node (if possible) to confirm that the application is using GPU memory.

## Gotchas

-   If VRAM is an issue on the HPC, consider using a model with a smaller quantization level or reducing the context length.
-   If the answers are not grounded, double-check that the correct FAISS index is being loaded and that the embedding models match.