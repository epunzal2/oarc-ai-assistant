# Optional Next Steps

This document outlines potential future enhancements and directions for the project once the core GPU and retrieval functionality is validated.

## 1. Streamlit UI Integration

Once the CLI/Flask application is stable and performs well on the HPC cluster, a Streamlit user interface can be developed for a more interactive experience.

-   **Separate sbatch Script:** Create a new Slurm batch script specifically for the Streamlit application. This script will need to handle port forwarding to allow access to the UI from outside the cluster.
-   **Resource Profile:** The Streamlit application may have a different resource profile compared to the CLI harness, so the sbatch script should be adjusted accordingly.
-   **UI Development:** The Streamlit application will need to be designed to interact with the RAG pipeline, allowing users to input questions and view the generated answers.

## 2. Qdrant Integration

As the project scales, using a more robust vector store like Qdrant may become necessary.

-   **When to Consider:** Qdrant should be considered when the size of the FAISS index becomes unmanageable or when concurrent access to the vector store is required.
-   **Implementation:** This will involve adding a new vector store option to the configuration and implementing the necessary logic to connect to a Qdrant instance.
-   **Deployment:** Qdrant can be run as a separate service, either on the HPC cluster or on a dedicated server.

## 3. Model Scaling

After successful tests with a small-to-medium sized model, you can experiment with larger models to improve the quality of the generated responses.

-   **Resource Requirements:** Larger models will require more GPU memory and may need adjustments to the Slurm script to request more resources.
-   **Evaluation:** It is important to evaluate the trade-off between model size, performance, and the quality of the answers.

## 4. Advanced RAG Techniques

-   **Re-ranking:** Implement a re-ranking step after the initial retrieval to improve the relevance of the documents passed to the LLM.
-   **Query Transformations:** Use techniques like query expansion or multi-query retrieval to improve the chances of finding relevant documents.