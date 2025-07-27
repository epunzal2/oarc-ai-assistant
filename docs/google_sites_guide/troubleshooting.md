
Cluster User Guide	
AmarelCaliburn
Troubleshooting
Offline nodes
Offline nodes
Both the Amarel and Caliburn systems comprise many compute nodes and nodes become unavailable (usually only temporarily) for many different reasons. To see a list of all offline nodes: sinfo --list-reasons

Below are some common reasons why nodes may be offline:

When our infrastructure team removes a node from service, they enter a brief explanation. Examples include,

Needs service

Epilog error

Hardware failure

Bad hard drive

IB problem (indicates problem with infiniband network)

Testing

Dead (the node is not repairable and offline permanently)

Reserved: Maintenance (the node is reserved for maintenance)

If SLURM automatically takes a node offline, you may see reasons such as:

not responding (SLURM can't communicate with node)

low RealMemory (the node isn't reporting correct amount of RAM)

gres/gpu count too low (indicates a problem with a GPU node not reporting the correct number of GPUs)

We run a "Node Health Check" (NHC) script that verifies a node's readiness to run jobs. If a node fails any of the tests, the NHC script will set the node offline with reasons that include,

NHC: check_ps_cpu (a runaway process on a node)

NHC: check_fs  (one or more of the network filesystems are not mounted correctly or a directory is near capacity)

NHC: nv_health (a problem with an NVIDIA GPU)

NHC: check_hw_ib (an InfiniBand problem)

NHC: check_ps_daemon (a problem with the authentication service)

NHC: check_hw_physmem (a problem with the amount of RAM being reported)

NHC: check_cmd_output (a problem with output from a test command)

