# Resource Binding

- [Overview](#overview)
- [Srun --cpu-bind option](#srun)
- [Node CpuBind Configuration](#node)
- [Partition CpuBind Configuration](#partition)
- [TaskPluginParam Configuration](#TaskPluginParam)

## Overview

Slurm has a rich set of options to control the default binding of tasks to resources. For example,
tasks can be bound to individual threads, cores, sockets, NUMA or boards. See the slurm.conf and
srun man pages for more information about how these options work. This document focuses on how
default binding configuration can be configured. Default binding can be configured on a per-node,
per-partition or global basis. The highest priority will be that specified using the srun --cpu-bind
option. The next highest priority binding will be the node-specific binding if any node in the job
allocation has some CpuBind configuration parameter and all other nodes in the job allocation either
have the same or no CpuBind configuration parameter. The next highest priority binding will be the
partition-specific CpuBind configuration parameter (if any). The lowest priority binding will be
that specified by the TaskPluginParam configuration parameter.

1.  Srun --cpu-bind option
2.  Node CpuBind configuration parameter (if all nodes match)
3.  Partition CpuBind configuration parameter
4.  TaskPluginParam configuration parameter

## Srun --cpu-bind option

The srun --cpu-bind option will always be used to control task binding. If the --cpu-bind option
only includes "verbose" rather than identifying the entities to be bound to, then the verbose option
will be used together with the default entity based upon Slurm configuration parameters as described
below.

## Node CpuBind Configuration

The next possible source of the resource binding information is the node's configured CpuBind value,
but only if every node has the same CpuBind value (or no configured CpuBind value). The node's
CpuBind value is configured in the slurm.conf file. Its value may be viewed or modified using the
scontrol command. To clear a node's CpuBind value use the command:

    scontrol update NodeName=... CpuBind=off

If a node_features plugin is configured, typically to support booting Intel KNL nodes into different
NUMA and/or MCDRAM modes, the plugin can be configured to modify the node's CpuBind option based
upon the NUMA mode. This is accomplished by specifying the NumaCpuBind parameter in the knl.conf
configuration file with pairs of NUMA modes and CpuBind options. As soon as the node is booted into
a new NUMA mode, the node's CpuBind option is automatically modified. For example, the following
line in the knl.conf file

    NumaCpuBind=a2a=core;snc2=thread

will set a node's CpuBind field to "core" when booted into "a2a" (all to all) NUMA mode and to
"thread" when booted into "snc2 NUMA mode. Any NUMA mode not specified in the NumaCpuBind
configuration file will result in no change to the node's CpuBind field.

## Partition CpuBind Configuration

The next possible source of the resource binding information is the partition's configured CpuBind
value. The partition's CpuBind value is configured in the slurm.conf file. Its value may be viewed
or modified using the scontrol command.

## TaskPluginParam Configuration

The last possible source of the resource binding information is the TaskPluginParam configuration
parameter from the slurm.conf file.

Last modified 24 June 2020
