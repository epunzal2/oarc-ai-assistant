# <span id="top">Dynamic Nodes</span>

## Overview

Starting in Slurm 22.05, nodes can be dynamically added and removed from Slurm.

## Dynamic Node Communications

For regular, non-dynamically created nodes, Slurm knows how to communicate with nodes by reading in
the slurm.conf. This is why it is important for a non-dynamic setup that the slurm.conf is
synchronized across the cluster. For dynamically created nodes, other than the slurmctld, the rest
of the Slurm components (e.g. srun, daemons) don't know about the dynamically created nodes. In
order for srun and the slurmds to know how to communicate with the other nodes in a job allocation,
slurmctld passes each node's address information (NodeName, NodeAddr, NodeHostname) -- known as the
alias list -- to the srun and the srun forwards the list to the slurmds. This list is seen in the
job's environment as the **SLURM_NODE_ALIASES** environment variable.

The controller automatically grabs the node's **NodeAddr** and **NodeHostname** for dynamic slurmd
registrations. For cloud nodes created with scontrol, if the nodename is not resolvable, then
either 1) the node's **NodeAddr** and **NodeHostname** need to be updated with the **scontrol
update** command before the node registers or 2) use the
[cloud_reg_addrs](slurm.conf.md#OPT_cloud_reg_addrs) **SlurmctldParameter**.

## Slurm Configuration

**MaxNodeCount=#**  
Set to the number of possible nodes that can be active in a system at a time. See the slurm.conf
[man](slurm.conf.md#OPT_MaxNodeCount) page for more details.

**SelectType=select/cons_tres**  
Dynamic nodes are only supported with cons_tres.

**TreeWidth=65533**  
Fanning out of controller pings and application launches through slurmds are not supported with
dynamic nodes. TreeWidth must be disabled (i.e. set to 65533) for dynamic environments. However, the
reverse fanout of step completions through slurmds does happen due to the job's alias list.

**NOTE**: The **cloud_dns** **SlurmctldParameter** must not be set as this disables the alias list.

### Partition Assignment

Dynamic nodes can be automatically assigned to partitions at creation by using the partition's nodes
[ALL](slurm.conf.md#OPT_Nodes_1) keyword or [NodeSets](slurm.conf.md#SECTION_NODESET-CONFIGURATION)
and specifying a feature on the nodes.

e.g.

    Nodeset=ns1 Feature=f1
    Nodeset=ns2 Feature=f2

    PartitionName=all  Nodes=ALL Default=yes
    PartitionName=dyn1 Nodes=ns1
    PartitionName=dyn2 Nodes=ns2
    PartitionName=dyn3 Nodes=ns1,ns2

## Creating Nodes

Nodes can be created two ways:

1.  **Dynamic slurmd registration**  
    Using the slurmd [-Z](slurmd.md#OPT_-Z) and [--conf](slurmd.md#OPT_conf-%3Cnode-parameters%3E)
    options a slurmd will register with the controller and will automatically be added to the
    system.

    e.g.

        slurmd -Z --conf "RealMemory=80000 Gres=gpu:2 Feature=f1"

2.  **scontrol create NodeName= ...**  
    Create nodes using scontrol by specifying the same **NodeName** line that you would define in
    the slurm.conf. See slurm.conf [man](slurm.conf.md#SECTION_NODE-CONFIGURATION) page for node
    options. Only **State=CLOUD** and **State=FUTURE** are supported. The node configuration should
    match what the slurmd will register with (e.g. slurmd -C) plus any additional attributes.

    e.g.

        scontrol create NodeName=d[1-100] CPUs=16 Boards=1 SocketsPerBoard=1 CoresPerSocket=8 ThreadsPerCore=2 RealMemory=31848 Gres=gpu:2 Feature=f1 State=cloud

## Deleting Nodes

Nodes can be deleted using **scontrol delete nodename=\<nodelist\>**. Nodes can only be deleted if
they have no jobs running on them and aren't part of a reservation.

## Limitations

1.  When dynamic nodes are added to Slurm they will potentially be alphabetically out of order
    internally — leading to suboptimal job allocations if node names represent topology of the nodes
    — until a reconfigure or a restart is performed. If using a [Topology Plugin](topology.md), the
    topology will also be out of date until a reconfigure/restart is performed.
2.  The [route/toplogy](slurm.conf.md#OPT_route/topology) plugin is not supported since dynamic
    nodes require that the Fanout/Treewidth be disabled.

Last modified 10 April 2023
