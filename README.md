# RAG System for OARC Documentation

This project implements a Retrieval-Augmented Generation (RAG) system to answer questions about the Amarel cluster based on the OARC Google Sites guide and ServiceNow data. The architecture of the system, including the data pipeline and deployment on the HPC cluster, is detailed in the flowchart below.

## RAG Architecture Flowchart

This flowchart illustrates the general architecture of the RAG system. The HPC deployment specifically utilizes the FAISS index for storage and the Phi-3-mini model for generation, as depicted in the diagram.

```mermaid
graph TD
    subgraph Data Ingestion
        A[ServiceNow Tickets]
        B[Google Sites Documentation]
    end

    subgraph Processing
        C[run_pipeline.sh: Preprocessing and Chunking]
        D[Embedding Model: all-MiniLM-L6-v2]
    end

    subgraph Storage
        E[FAISS Index: Vector Store]
    end

    subgraph Retrieval
        F[User Query]
        G[Query Embedding]
        H[Retrieve Relevant Documents]
    end

    subgraph Generation
        I[LLM: Phi-3-mini]
        J[Generated Answer]
    end

    A --> C
    B --> C
    C --> D
    D --> E
    F --> G
    G --> H
    E --> H
    H --> I
    F --> I
    I --> J
```

### HPC Installation Notes

If you encounter OS-related errors during the installation of `llama-cpp-python` (such as GLIBC incompatibility), you may need to install it from source. The [`env_check/build_llama_cpp.sbatch`](env_check/build_llama_cpp.sbatch) script provides an example of how to do this.

The specific package requirements for the HPC environment are defined in [`requirements_hpc.txt`](requirements_hpc.txt) and [`constraints_hpc.txt`](constraints_hpc.txt). A complete list of the exact environment libraries can be found in [`env_check/oarc-ai-rag-test.sanitized.yml`](env_check/oarc-ai-rag-test.sanitized.yml).

## Architecture

The system is built with Python, LangChain, and a Hugging Face model. It supports both Qdrant and an in-memory FAISS vector store. For a detailed explanation of the architecture, please see the [`architecture/architecture.md`](./architecture/architecture.md) file.

## RAG Evaluation Test Suite

The evaluation “test suite” (aka Evaluation Agent) runs smoke and full bake‑off jobs on the GPU partition to compare embeddings and measure retrieval/generation quality. The diagram below is also available at `architecture/rag_test_suite.md`.

```mermaid
flowchart TB
  subgraph Inputs
    A["Gold dataset<br/>queries.jsonl<br/>answers.jsonl<br/>qrels.tsv"]
    B["Corpus<br/>docs/google_sites_guide<br/>ServiceNow (optional)"]
    C["Model Registry<br/>Embeddings<br/>(MiniLM, BGE small/large, GTE-large)"]
    D["LLMs<br/>Qwen2.5‑14B‑Instruct (llama.cpp local)"]
  end

  subgraph Config
    E1["configs/evaluation/*.yml<br/>- sweeps (grid): embeddings, chunk_size, overlap, top_k<br/>- generator/judge (n_ctx, max_new_tokens)<br/>- chat_template"]
    E2["scripts/evaluation/*.sbatch"]
  end

  Inputs --> BR
  Config --> BR

  subgraph Runner
    BR["BatchRunner<br/>- build doc_id_map (markdown-first)<br/>- chunk corpus<br/>- build FAISS<br/>- retriever -> generator<br/>- judge -> metrics"]
  end

  BR --> VS["FAISS index + retriever"]
  VS --> RAG["Retriever + LLM (RAG chain)"]
  RAG --> J["LLM Judge"]
  RAG --> RES
  J --> MET

  subgraph Outputs
    RES["Per-run responses<br/>runs/<run_id>/responses.jsonl"]
    MET["Metrics<br/>- runs/<run_id>/metrics.json<br/>- summary_metrics.json<br/>- per_run_metrics.jsonl<br/>- doc_id_map.json"]
  end

  NC(["Token-based context cap<br/>(RAG_MAX_CONTEXT_TOKENS)<br/>to avoid n_ctx overflow"])
  NC -.-> RAG
```

- Smoke run: `sbatch scripts/evaluation/run_evaluation_smoke.sbatch --config configs/evaluation/embedding_bakeoff_smoke.yml`
- Full sweep: `sbatch scripts/evaluation/run_evaluation.sbatch --config configs/evaluation/embedding_bakeoff.yml`
- Results: `results/embedding_bakeoff*/{summary_metrics.json,per_run_metrics.jsonl,runs/*}`; mapping: `doc_id_map.json`
- Tuning knobs:
  - Retrieval: `sweeps.chunk_size`, `sweeps.chunk_overlap`, `sweeps.top_k`
  - LLM: `frozen.generator.{n_ctx,max_new_tokens}`; optional `n_ctx_margin`
  - Safety: override context cap via `RAG_MAX_CONTEXT_TOKENS` (tokens) or `RAG_MAX_CONTEXT_CHARS`

What “sweeps” means

- The `sweeps` section in the YAML defines a grid of runs:
  - `embedding_models`: which embeddings to test (e.g., MiniLM, BGE small/large, GTE-large)
  - `chunk_size`, `chunk_overlap`: splitter params
  - `top_k`: retriever depth
- The runner executes every combination and writes per‑run metrics and a summary selecting the best run.

LLMs used

- Generator/Judge: `Qwen2.5‑14B‑Instruct` via local `llama.cpp` (no HF endpoint in this setup).

Future tasks

- Add LLM sweeps from the model registry (Qwen‑32B, Mixtral‑8x7B‑IT, gpt‑oss‑20b, Llama‑3) for generator and/or judge; mind GPU memory.
- Bring ServiceNow into evaluation after stronger preprocessing (strip quoted threads/footers, dedup), smaller chunks, `source_kind` metadata, and SN‑aware qrels; provide markdown‑only and mixed‑corpus tracks.
- Reproducibility and controls: optional frozen `doc_id_map` in YAML; expose a `max_context_tokens` knob in config; persist seeds and deterministic loaders.
- Results/observability: export raw vs deduped retrieved IDs; add summary tables and optional CI checks; include GPU/throughput telemetry in logs.

## Configuration

The project's settings are centralized in the [`src/rag/config.py`](src/rag/config.py) file. This file defines key parameters such as data paths, model names, and vector store configurations.

Many of these settings can be overridden by environment variables (e.g., `QDRANT_HOST`, `HUGGINGFACE_API_TOKEN`), which are loaded at runtime using `python-dotenv`. This allows for flexible configuration without modifying the source code, which is particularly useful for switching between local and HPC environments.

## Setup and Installation

### 1. Prerequisites

-   Python 3.9+
-   Conda (or Mamba) and Pip for environment management.
-   Docker (Optional, for Qdrant)

### 2. Clone the Repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 3. Set Up the Environment

Create a virtual environment and install the required packages:

```bash
conda create -n oarc-rag python=3.9
conda activate oarc-rag
pip install -r requirements_hpc.txt -c constraints_hpc.txt
```

### 4. Set Up the Hugging Face API Token

Create a `.env` file in the root of the project and add your Hugging Face API token:

```
HUGGINGFACE_API_TOKEN="your-token-here"
```

Then, log in to the Hugging Face Hub:

```bash
huggingface-cli login --token $HUGGINGFACE_API_TOKEN
```

### 5. Start the Qdrant Vector Database (Optional)

This step is only required if you are running the chatbot locally with the Qdrant vector store. The HPC deployment uses a FAISS vector store, which does not require a separate database server.

Run the Qdrant Docker container:

```bash
docker run -p 6333:6333 qdrant/qdrant```

### 6. Create the Vector Store

The vector store for the HPC deployment is created using a data preparation pipeline that processes the raw data and builds a FAISS index. This entire process is automated and can be run on the HPC cluster by submitting a Slurm job.

To create the vector store, run the following command:

```bash
sbatch scripts/rag/run_pipeline.sbatch
```

This script executes [`scripts/rag/run_pipeline.sh`](scripts/rag/run_pipeline.sh), which handles cleaning the data, preparing it for ingestion, and creating the final FAISS vector store in the `vector_index/faiss_amarel` directory.

## Data Preparation Pipeline
 
The `run_pipeline.sh` script automates the data preparation process, which includes cleaning the data, preparing it for ingestion, and creating the vector store.
 
To run the pipeline, execute the following command:
 
```bash
./scripts/rag/run_pipeline.sh
```
 
## Running the Chatbot

The method for running the chatbot differs depending on whether you are in a local environment (like a Mac) or on the HPC cluster.

### Running Locally

For local execution, you can run the Streamlit chatbot interface directly. The script accepts command-line arguments to select the LLM provider and the vector store.

-   `--llm-provider`: Choose between `huggingface` (default) and `ollama`.
-   `--vector-store`: Choose between `qdrant` (default) and `in_memory`.

**Examples:**

**Using Hugging Face and Qdrant (default):**
```bash
streamlit run src/rag/main.py
```

**Using Ollama and Qdrant:**
```bash
streamlit run src/rag/main.py -- --llm-provider ollama
```

**Using Hugging Face and In-Memory FAISS:**
```bash
streamlit run src/rag/main.py -- --vector-store in_memory
```

**Using Ollama and In-Memory FAISS:**
```bash
streamlit run src/rag/main.py -- --llm-provider ollama --vector-store in_memory
```

The app will be available at `http://localhost:8501`.

### Running on the HPC Cluster

To run the chatbot on the HPC cluster, please refer to the **HPC Deployment** section for instructions on submitting the job via `sbatch`.

## Deployment

### Deployment on an HPC Cluster

To deploy the chatbot on an HPC cluster, you can use the provided `sbatch` script. This script sets up the necessary environment, including loading the required modules and activating the virtual environment, and then runs the chatbot application.

**To submit the job, run the following command:**
```bash
sbatch scripts/deployment/hpc/run_chat_hpc.sbatch
```

This will submit the job to the Slurm scheduler, and the chatbot will be accessible through the compute node where the job is running.

This deployment is ideal for running the chatbot in a high-performance environment, enabling it to handle complex queries and large datasets efficiently.

```mermaid
sequenceDiagram
    participant User
    participant Login Node
    participant Slurm Scheduler
    participant GPU Compute Node

    User->>Login Node: Connects via SSH
    User->>Login Node: Submits run_chat_hpc.sbatch
    Login Node->>Slurm Scheduler: Sends job request
    Slurm Scheduler->>GPU Compute Node: Allocates node and sends job
    GPU Compute Node->>GPU Compute Node: Runs sbatch script (setup env, start chat_hpc.py)
    User->>Login Node: Creates SSH tunnel to GPU node
    Login Node->>GPU Compute Node: Forwards user connection
    User->>GPU Compute Node: Interacts with chatbot via local browser
```

To run the chatbot on the HPC cluster, submit a job to the Slurm scheduler using the provided `sbatch` script. This script requests a GPU node and sets up the necessary environment for the application to run.

```bash
sbatch scripts/deployment/hpc/run_chat_hpc.sbatch
```
