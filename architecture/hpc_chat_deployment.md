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