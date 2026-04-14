# Slurm Power Saving Guide

Slurm provides an integrated power saving mechanism for powering down idle nodes. Nodes that remain
idle for a configurable period of time can be placed in a power saving mode, which can reduce power
consumption or fully power down the node. The nodes will be restored to normal operation once work
is assigned to them. For example, power saving can be accomplished using a *cpufreq* governor that
can change CPU frequency and voltage (note that the *cpufreq* driver must be enabled in the Linux
kernel configuration). Of particular note, Slurm can power nodes up or down at a configurable rate
to prevent rapid changes in power demands. For example, starting a 1000 node job on an idle cluster
could result in an instantaneous surge in power demand of multiple megawatts without Slurm's support
to increase power demands in a gradual fashion.

## Configuration

A great deal of flexibility is offered in terms of when and how idle nodes are put into or removed
from power save mode. Note that the Slurm control daemon, *slurmctld*, must be restarted to
initially enable power saving mode. Changes in the configuration parameters (e.g. *SuspendTime*)
will take effect after modifying the *slurm.conf* configuration file and executing "*scontrol
reconfig*". The following configuration parameters are available:

- **SuspendTime**: Nodes becomes eligible for power saving mode after being idle or down for this
  number of seconds. A negative number disables power saving mode. The default value is -1
  (disabled).
- **SuspendRate**: Maximum number of nodes to be placed into power saving mode per minute. A value
  of zero results in no limits being imposed. The default value is 60. Use this to prevent rapid
  drops in power consumption.
- **ResumeRate**: Maximum number of nodes to be removed from power saving mode per minute. A value
  of zero results in no limits being imposed. The default value is 300. Use this to prevent rapid
  increases in power consumption.
- **SuspendProgram**: Program to be executed to place nodes into power saving mode. The program
  executes as *SlurmUser* (as configured in *slurm.conf*). The argument to the program will be the
  names of nodes to be placed into power savings mode (using Slurm's hostlist expression format).
- **ResumeProgram**: Program to be executed to remove nodes from power saving mode. The program
  executes as *SlurmUser* (as configured in *slurm.conf*). The argument to the program will be the
  names of nodes to be removed from power savings mode (using Slurm's hostlist expression format). A
  job to node mapping is available in JSON format by reading the temporary file specified by the
  **SLURM_RESUME_FILE** environment variable. This file should be used at the beginning of
  **ResumeProgram** - see the [Fault Tolerance](#tolerance) section for more details. This program
  may use the *scontrol show node* command to ensure that a node has booted and the *slurmd* daemon
  started. If the *slurmd* daemon fails to respond within the configured **ResumeTimeout** value
  with an updated BootTime, the node will be placed in a DOWN state and the job requesting the node
  will be requeued. If the node isn't actually rebooted (i.e. when multiple-slurmd is configured)
  you can start slurmd with the "-b" option to report the node boot time as now. **NOTE**: The
  **SLURM_RESUME_FILE** will only exist and be usable if Slurm was compiled with the
  [JSON-C](download.md#json) serializer library.
- **SuspendTimeout**: Maximum time permitted (in second) between when a node suspend request is
  issued and when the node shutdown is complete. At that time the node must ready for a resume
  request to be issued as needed for new workload. The default value is 30 seconds.
- **ReconfigFlags=KeepPowerSaveSettings**: If set, an "scontrol reconfig" command will preserve the
  current state of SuspendExcNodes, SuspendExcParts and SuspendExcStates.
- **ResumeTimeout**: Maximum time permitted (in seconds) between when a node resume request is
  issued and when the node is actually available for use. Nodes which fail to respond in this time
  frame will be marked DOWN and the jobs scheduled on the node requeued. Nodes which reboot after
  this time frame will be marked DOWN with a reason of "Node unexpectedly rebooted." The default
  value is 60 seconds.
- **SuspendExcNodes**: List of nodes to never place in power saving mode. Use Slurm's hostlist
  expression to identify nodes with an optional ":" separator and count of nodes to exclude from the
  preceding range. For example "nid\[10\\20\]:4" will prevent 4 usable nodes (i.e IDLE and not DOWN,
  DRAINING or already powered down) in the set "nid\[10\\20\]" from being powered down. Multiple
  sets of nodes can be specified with or without counts in a comma separated list (e.g
  "nid\[10\\20\]:4,nid\[80\\90\]:2"). By default, no nodes are excluded. This value may be updated
  with scontrol. See **ReconfigFlags=KeepPowerSaveSettings** for setting persistence.
- **SuspendExcParts**: List of partitions with nodes to never place in power saving mode. Multiple
  partitions may be specified using a comma separator. By default, no nodes are excluded.
  This value may be updated with scontrol. See **ReconfigFlags=KeepPowerSaveSettings** for setting
  persistence.
- **SuspendExcStates**: Specifies node states that are not to be powered down automatically. Valid
  states include CLOUD, DOWN, DRAIN, DYNAMIC_FUTURE, DYNAMIC_NORM, FAIL, INVALID_REG, MAINTENANCE,
  NOT_RESPONDING, PERFCTRS, PLANNED, and RESERVED. By default, any of these states, if idle for
  **SuspendTime**, would be powered down. This value may be updated with scontrol. See
  **ReconfigFlags=KeepPowerSaveSettings** for setting persistence.
- **BatchStartTimeout**: Specifies how long to wait after a batch job start request is issued before
  we expect the batch job to be running on the compute node. Depending upon how nodes are returned
  to service, this value may need to be increased above its default value of 10 seconds.
- **PartitionName= ... PowerDownOnIdle=\[YES\|NO\]**: If set to **YES** and power saving is enabled
  for the partition, then nodes allocated from this partition will be requested to power down after
  being allocated at least one job. These nodes will not power down until they transition from
  COMPLETING to IDLE. If set to **NO** then power saving will operate as configured for the
  partition. The default value is **NO**.

Note that *SuspendProgram* and *ResumeProgram* execute as *SlurmUser* on the node where the
*slurmctld* daemon runs (primary and backup server nodes). Use of *sudo* may be required for
*SlurmUser* to power down and restart nodes. If you need to convert Slurm's hostlist expression into
individual node names, the *scontrol show hostnames* command may prove useful. The commands used to
boot or shut down nodes will depend upon your cluster management tools.

Note that *SuspendProgram* and *ResumeProgram* are not subject to any time limits. They should
perform the required action, ideally verify the action (e.g. node boot and start the *slurmd*
daemon, thus the node is no longer non-responsive to *slurmctld*) and terminate. Long running
programs will be logged by *slurmctld*, but not aborted.

Also note that the stderr/out of the suspend and resume programs are not logged. If logging is
desired it should be added to the scripts.

    #!/bin/bash
    # Example SuspendProgram
    echo "`date` Suspend invoked $0 $*" >>/var/log/power_save.log
    hosts=`scontrol show hostnames $1`
    for host in $hosts
    do
       sudo node_shutdown $host
    done

    #!/bin/bash
    # Example ResumeProgram
    echo "`date` Resume invoked $0 $*" >>/var/log/power_save.log
    hosts=`scontrol show hostnames $1`
    for host in $hosts
    do
       sudo node_startup $host
    done

Subject to the various rates, limits and exclusions, the power save code follows this logic:

1.  Identify nodes which have been idle for at least **SuspendTime**.
2.  Execute **SuspendProgram** with an argument of the idle node names.
3.  Identify the nodes which are in power save mode (a flag in the node's state field), but have
    been allocated to jobs.
4.  Execute **ResumeProgram** with an argument of the allocated node names.
5.  Once the *slurmd* responds, initiate the job and/or job steps allocated to it.
6.  If the *slurmd* fails to respond within the value configured for **SlurmdTimeout**, the node
    will be marked DOWN and the job requeued if possible.
7.  Repeat indefinitely.

## Use of Allocations

A resource allocation request will be granted as soon as resources are selected for use, possibly
before the nodes are all available for use. The launching of job steps will be delayed until the
required nodes have been restored to service (it prints a warning about waiting for nodes to become
available and periodically retries until they are available).

In the case of an *sbatch* command, the batch program will start when node zero of the allocation is
ready for use and pre-processing can be performed as needed before using *srun* to launch job steps.
The sbatch *--wait-all-nodes=\<value\>* command can be used to override this behavior on a per-job
basis and a system-wide default can be set with the *SchedulerParameters=sbatch_wait_nodes* option.

In the case of the *salloc* command, once the allocation is made a new shell will be created on the
login node. The salloc *--wait-all-nodes=\<value\>* command can be used to override this behavior on
a per-job basis and a system-wide default can be set with the
*SchedulerParameters=salloc_wait_nodes* option.

## Fault Tolerance

If the *slurmctld* daemon is terminated gracefully, it will wait up to ten seconds (or the maximum
of **SuspendTimeout** or **ResumeTimeout** if less than ten seconds) for any spawned
**SuspendProgram** or **ResumeProgram** to terminate before the daemon terminates. If the spawned
program does not terminate within that time period, the event will be logged and *slurmctld* will
exit in order to permit another *slurmctld* daemon to be initiated. Any spawned **SuspendProgram**
or **ResumeProgram** will continue to run.

When the slurmctld daemon shuts down, any **SLURM_RESUME_FILE** temporary files are no longer
available, even once slurmctld restarts. Therefore, **ResumeProgram** should use
**SLURM_RESUME_FILE** within ten seconds of starting to guarantee that it still exists.

## Booting Different Images

If you want **ResumeProgram** to boot various images according to job specifications, it will need
to be a fairly sophisticated program and perform the following actions:

1.  Determine which jobs are associated with the nodes to be booted
2.  Determine which image is required for each job and
3.  Boot the appropriate image for each node

Last modified 14 November 2023
