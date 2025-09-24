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