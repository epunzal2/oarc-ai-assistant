# Prolog and Epilog Guide

Slurm supports a multitude of prolog and epilog programs. Note that for security reasons, these
programs do not have a search path set. Either specify fully qualified path names in the program or
set the <span class="commandline">PATH</span> environment variable. The first table below identifies
what prologs and epilogs are available for job allocations, when and where they run.

|  |  |  |  |  |
|----|----|----|----|----|
| **Parameter** | **Location** | **Invoked by** | **User** | **When executed** |
| Prolog (from slurm.conf) | Compute or front end node | slurmd daemon | SlurmdUser (normally user root) | First job or job step initiation on that node (by default); PrologFlags=Alloc will force the script to be executed at job allocation |
| PrologSlurmctld (from slurm.conf) | Head node (where slurmctld daemon runs) | slurmctld daemon | SlurmctldUser | At job allocation |
| Epilog (from slurm.conf) | Compute or front end node | slurmd daemon | SlurmdUser (normally user root) | At job termination |
| EpilogSlurmctld (from slurm.conf) | Head node (where slurmctld daemon runs) | slurmctld daemon | SlurmctldUser | At job termination |

  

This second table below identifies what prologs and epilogs are available for job step allocations,
when and where they run.

|  |  |  |  |  |
|----|----|----|----|----|
| **Parameter** | **Location** | **Invoked by** | **User** | **When executed** |
| SrunProlog (from slurm.conf) or srun --prolog | srun invocation node | srun command | User invoking srun command | Prior to launching job step |
| TaskProlog (from slurm.conf) | Compute node | slurmstepd daemon | User invoking srun command | Prior to launching job step |
| srun --task-prolog | Compute node | slurmstepd daemon | User invoking srun command | Prior to launching job step |
| TaskEpilog (from slurm.conf) | Compute node | slurmstepd daemon | User invoking srun command | Completion job step |
| srun --task-epilog | Compute node | slurmstepd daemon | User invoking srun command | Completion job step |
| SrunEpilog (from slurm.conf) or srun --epilog | srun invocation node | srun command | User invoking srun command | Completion job step |

By default the Prolog script is only run on any individual node when it first sees a job step from a
new allocation; it does not run the Prolog immediately when an allocation is granted. If no job
steps from an allocation are run on a node, it will never run the Prolog for that allocation. This
Prolog behavior can be changed by the PrologFlags parameter. The Epilog, on the other hand, always
runs on every node of an allocation when the allocation is released.

If multilple prolog and/or epilog scripts are specified, (e.g. "/etc/slurm/prolog.d/\*") they run in
reverse order.

Prolog and Epilog scripts should be designed to be as short as possible and should not call Slurm
commands (e.g. squeue, scontrol, sacctmgr, etc). Long running scripts can cause scheduling problems
when jobs take a long time to start or finish. Slurm commands in these scripts can potentially lead
to performance issues and should not be used.

The task prolog is executed with the same environment as the user tasks to be initiated. The
standard output of that program is read and processed as follows:  
<span class="commandline">export name=value</span> sets an environment variable for the user task  
<span class="commandline">unset name</span> clears an environment variable from the user task  
<span class="commandline">print ...</span> writes to the task's standard output.  
Special treatment is given to the **SLURM_PROLOG_CPU_MASK** variable when set in the task prolog.
The variable is interpreted as a coma separated list of hex maps. It allows you to specify the
CPU(s) that will be bound to a task and is applied using sched_setaffinity. The above functionality
is limited to the task prolog script.

Unless otherwise specified, these environment variables are available to all of the programs.

- **CUDA_MPS_ACTIVE_THREAD_PERCENTAGE** Specifies the percentage of a GPU that should be allocated
  to the job. The value is set only if the gres/mps plugin is configured and the job requests those
  resources. Available in Prolog and Epilog only.
- **CUDA_VISIBLE_DEVICES** Specifies the GPU devices for the job allocation. The value is set only
  if the gres/gpu or gres/mps plugin is configured and the job requests those resources. Note that
  the environment variable set for the job may differ from that set for the Prolog and Epilog if
  Slurm is configured to constrain the device files visible to a job using Linux cgroup. This is
  because the Prolog and Epilog programs run <u>outside</u> of any Linux cgroup while the job runs
  <u>inside</u> of the cgroup and may thus have a different set of visible devices. For example, if
  a job is allocated the device "/dev/nvidia1", then
  <span class="commandline">CUDA_VISIBLE_DEVICES</span> will be set to a value of "1" in the Prolog
  and Epilog while the job's value of <span class="commandline">CUDA_VISIBLE_DEVICES</span> will be
  set to a value of "0" (i.e. the first GPU device visible to the job).
  <span class="commandline">CUDA_VISIBLE_DEVICES</span> will be set unless otherwise excluded via
  the *Flags* or *AutoDetect* options in *gres.conf*. See also
  <span class="commandline">SLURM_JOB_GPUS</span>. Available in Prolog and Epilog only.
- **GPU_DEVICE_ORDINAL** Specifies the GPU devices for the job allocation. The considerations for
  <span class="commandline">CUDA_VISIBLE_DEVICES</span> also apply to
  <span class="commandline">GPU_DEVICE_ORDINAL</span>.
- **ROCR_VISIBLE_DEVICES** Specifies the GPU devices for the job allocation. The considerations for
  <span class="commandline">CUDA_VISIBLE_DEVICES</span> also apply to
  <span class="commandline">ROCR_VISIBLE_DEVICES</span>.
- **SLURM_ARRAY_JOB_ID** If this job is part of a job array, this will be set to the job ID.
  Otherwise it will not be set. To reference this specific task of a job array, combine
  <span class="commandline">SLURM_ARRAY_JOB_ID</span> with
  <span class="commandline">SLURM_ARRAY_TASK_ID</span> (e.g. <span class="commandline">scontrol
  update \${SLURM_ARRAY_JOB_ID}\_{\$SLURM_ARRAY_TASK_ID} ...</span>); Available in PrologSlurmctld,
  SrunProlog, TaskProlog, EpilogSlurmctld, SrunEpilog and TaskEpilog.
- **SLURM_ARRAY_TASK_COUNT** If this job is part of a job array, this will be set to the number of
  tasks in the array. Otherwise it will not be set. Available in PrologSlurmctld, SrunProlog,
  TaskProlog, EpilogSlurmctld, SrunEpilog and TaskEpilog.
- **SLURM_ARRAY_TASK_ID** If this job is part of a job array, this will be set to the task ID.
  Otherwise it will not be set. To reference this specific task of a job array, combine
  <span class="commandline">SLURM_ARRAY_JOB_ID</span> with
  <span class="commandline">SLURM_ARRAY_TASK_ID</span> (e.g. <span class="commandline">scontrol
  update \${SLURM_ARRAY_JOB_ID}\_{\$SLURM_ARRAY_TASK_ID} ...</span>); Available in PrologSlurmctld,
  SrunProlog, TaskProlog, EpilogSlurmctld, SrunEpilog and TaskEpilog.
- **SLURM_ARRAY_TASK_MAX** If this job is part of a job array, this will be set to the maximum task
  ID. Otherwise it will not be set. Available in PrologSlurmctld, SrunProlog, TaskProlog,
  EpilogSlurmctld, SrunEpilog and TaskEpilog.
- **SLURM_ARRAY_TASK_MIN** If this job is part of a job array, this will be set to the minimum task
  ID. Otherwise it will not be set. Available in PrologSlurmctld, SrunProlog, TaskProlog,
  EpilogSlurmctld, SrunEpilog and TaskEpilog.
- **SLURM_ARRAY_TASK_STEP** If this job is part of a job array, this will be set to the step size of
  task IDs. Otherwise it will not be set. Available in PrologSlurmctld, SrunProlog, TaskProlog,
  EpilogSlurmctld, SrunEpilog and TaskEpilog.
- **SLURM_CLUSTER_NAME** Name of the cluster executing the job.
- **SLURM_CONF** Location of the slurm.conf file. Available in Prolog, SrunProlog, TaskProlog,
  Epilog, SrunEpilog and TaskEpilog.
- **SLURM_CPUS_ON_NODE** Count of processors available to the job on current node. Available in
  SrunProlog, TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_DISTRIBUTION** Distribution type for the job. Available in SrunProlog and SrunEpilog.
- **SLURMD_NODENAME** Name of the node running the task. In the case of a parallel job executing on
  multiple compute nodes, the various tasks will have this environment variable set to different
  values on each compute node. Available in Prolog, TaskProlog, Epilog and TaskEpilog.
- **SLURM_GPUS** Count of the GPUs available to the job. Available in SrunProlog, TaskProlog,
  SrunEpilog and TaskEpilog.
- **SLURM_GTID** Global Task IDs running on this node. Zero origin and comma separated. Available in
  SrunProlog, TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_JOB_ACCOUNT** Account name used for the job.
- **SLURM_JOB_COMMENT** Comment added to the job. Available in Prolog, PrologSlurmctld, Epilog and
  EpilogSlurmctld.
- **SLURM_JOB_CONSTRAINTS** Features required to run the job. Available in Prolog, PrologSlurmctld,
  Epilog and EpilogSlurmctld.
- **SLURM_JOB_CPUS_PER_NODE** Count of processors available per node.
- **SLURM_JOB_DERIVED_EC** The highest exit code of all of the job steps. Available in Epilog and
  EpilogSlurmctld.
- **SLURM_JOB_EXIT_CODE** The exit code of the job script (or salloc). The value is the status as
  returned by the <span class="commandline">wait()</span> system call (See
  <span class="commandline">wait(2)</span>). Available in Epilog and EpilogSlurmctld.
- **SLURM_JOB_EXIT_CODE2** The exit code of the job script (or salloc). The value has the format
  <span class="commandline">\<exit\>:\<sig\></span>. The first number is the exit code, typically as
  set by the <span class="commandline">exit()</span> function. The second number is the signal that
  caused the process to terminate if it was terminated by a signal. Available in Epilog and
  EpilogSlurmctld.
- **SLURM_JOB_EXTRA** Extra field added to the job. Available in Prolog, PrologSlurmctld, Epilog,
  EpilogSlurmctld, and ResumeProgram (via SLURM_RESUME_FILE).
- **SLURM_JOB_GID** Group ID of the job's owner.
- **SLURM_JOB_GPUS** The GPU IDs of GPUs in the job allocation (if any). Available in the Prolog and
  Epilog.
- **SLURM_JOB_GROUP** Group name of the job's owner.
- **SLURM_JOB_ID** Job ID.
- **SLURM_JOBID** Job ID.
- **SLURM_JOB_NAME** Name of the job. Available in PrologSlurmctld, SrunProlog, TaskProlog,
  EpilogSlurmctld, SrunEpilog and TaskEpilog.
- **SLURM_JOB_NODELIST** Nodes assigned to job. A Slurm hostlist expression.
  <span class="commandline">scontrol show hostnames</span> can be used to convert this to a list of
  individual host names.
- **SLURM_NTASKS** Number of tasks requested by the job. Available in Prolog, SrunProlog,
  TaskProlog, Epilog, SrunEpilog and TaskEpilog.
- **SLURM_JOB_NUM_NODES** Number of nodes assigned to a job.
- **SLURM_JOB_OVERSUBSCRIBE** Job OverSubscribe status. See the [squeue man
  page](squeue.md#OPT_OverSubscribe) for possible values. Available in Prolog, PrologSlurmctld,
  Epilog and EpilogSlurmctld.
- **SLURM_JOB_PARTITION** Partition that job runs in.
- **SLURM_JOB_QOS** QOS assigned to job. Available in SrunProlog, TaskProlog, SrunEpilog and
  TaskEpilog.
- **SLURM_JOB_RESERVATION** Reservation requested for the job. Available in Prolog, PrologSlurmctld,
  Epilog and EpilogSlurmctld.
- **SLURM_JOB_RESTART_COUNT** Number of times the job has been restarted. Available in Prolog,
  PrologSlurmctld, Epilog and EpilogSlurmctld.
- **SLURM_JOB_STDERR** Job's stderr path. Available in Prolog, PrologSlurmctld, Epilog and
  EpilogSlurmctld.
- **SLURM_JOB_STDIN** Job's stdin path. Available in Prolog, PrologSlurmctld, Epilog and
  EpilogSlurmctld.
- **SLURM_JOB_STDOUT** Job's stdout path. Available in Prolog, PrologSlurmctld, Epilog and
  EpilogSlurmctld.
- **SLURM_JOB_UID** User ID of the job's owner.
- **SLURM_JOB_USER** User name of the job's owner.
- **SLURM_JOB_WORK_DIR** Job's working directory. Available in Prolog, PrologSlurmctld, Epilog,
  EpilogSlurmctld.
- **SLURM_LOCAL_GLOBALS_FILE** Globals file used to set up the environment for the testsuite.
  Available in SrunProlog, TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_LOCALID** Node local task ID for the process within a job. Available in SrunProlog,
  Taskprolog, SrunEpilog and TaskEpilog.
- **SLURM_NNODES** Number of nodes assigned to a job. Available in SrunProlog, TaskProlog,
  SrunEpilog and TaskEpilog.
- **SLURM_NODE_ALIASES** Contains the node name, communication address and hostname of a node. Used
  for cloud environments. Available in Prolog (PrologFlags=alloc only), SrunProlog, TaskProlog,
  SrunEpilog and TaskEpilog.
- **SLURM_NODEID** ID of current node relative to other nodes in a multi-node job. Available in
  TaskProlog and TaskEpilog.
- **SLURM_PRIO_PROCESS** Scheduling priority (nice value) at the time of submission. Available in
  SrunProlog, TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_PROCID** The MPI rank (or relative process ID) of the current process. Available in
  SrunProlog, TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_RESTART_COUNT** Number of times the job has been restarted. This is only set if the job
  has been restarted at least once. Available in SrunProlog, TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_RLIMIT_AS** Resource limit on the job's address space. Available in SrunProlog,
  TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_RLIMIT_CORE** Resource limit on the size of a core file the job is able to produce.
  Available in SrunProlog, TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_RLIMIT_CPU** Resource limit on the amount of CPU time a job is able to use. Available in
  SrunProlog, TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_RLIMIT_DATA** Resource limit on the size of a job's data segment. Available in SrunProlog,
  TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_RLIMIT_FSIZE** Resource limit on the maximum size of files a job may create. Available in
  SrunProlog, TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_RLIMIT_MEMLOCK** Resource limit on the bytes of data that may be locked into RAM.
  Available in SrunProlog, TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_RLIMIT_NOFILE** Resource limit on the number of file descriptors that can be opened by the
  job. Available in SrunProlog, TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_RLIMIT_NPROC** Resource limit on the number of processes that can be opened by the calling
  process. Available in SrunProlog, TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_RLIMIT_RSS** Resource limit on the job's resident set size. Available in SrunProlog,
  TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_RLIMIT_STACK** Resource limit on the job's process stack. Available in SrunProlog,
  TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_SCRIPT_CONTEXT** Identifies which epilog or prolog program is currently running. The value
  is one of the following:
  - <span class="commandline">prolog_slurmctld</span>
  - <span class="commandline">epilog_slurmctld</span>
  - <span class="commandline">prolog_slurmd</span>
  - <span class="commandline">epilog_slurmd</span>
  - <span class="commandline">prolog_task</span>
  - <span class="commandline">epilog_task</span>
  - <span class="commandline">prolog_srun</span>
  - <span class="commandline">epilog_srun</span>
- **SLURM_STEP_ID** Step ID of the current job. Available in SrunProlog and SrunEpilog.
- **SLURM_STEPID** Step ID of the current job. Available in SrunProlog and SrunEpilog.
- **SLURM_SUBMIT_DIR** Directory from which the job was submitted or, if applicable, the directory
  specified by the **-D, --chdir** option. Available in SrunProlog, Taskprolog, SrunEpilog and
  TaskEpilog.
- **SLURM_SUBMIT_HOST** Host from which the job was submitted. Available in SrunProlog, TaskProlog,
  SrunEpilog and TaskEpilog.
- **SLURM_TASK_PID** Process ID of the process started for the task. Available in TaskProlog.
- **SLURM_TASKS_PER_NODE** Number of tasks per node. Available in SrunProlog, TaskProlog, SrunEpilog
  and TaskEpilog.
- **SLURM_TOPOLOGY_ADDR** Set to the names of network switches or nodes that may be involved in the
  job's communications. Starts with the top level switch down to the node name. A period is used to
  separate each hardware component name. Available in SrunProlog, TaskProlog, SrunEpilog and
  TaskEpilog.
- **SLURM_TOPOLOGY_ADDR_PATTERN** Set to the network component types that corresponds with the list
  of names from **SLURM_TOPOLOGY_ADDR**. Each component will be identified as either <u>switch</u>
  or <u>node</u>. A period is used to separate each component type. Available in SrunProlog,
  TaskProlog, SrunEpilog and TaskEpilog.
- **SLURM_WCKEY** User name of the job's wckey (if any). Available in PrologSlurmctld and
  EpilogSlurmctld only.
- **SLURM_WORKING_CLUSTER** For use when using a Federation. Set to the remote sibling cluster's
  name, hostname, port, rpc version and plugin ID. Available in SrunProlog, TaskProlog, SrunEpilog
  and TaskEpilog.

Plugin functions may also be useful to execute logic at various well-defined points.

[SPANK](spank.md) is another mechanism that may be useful to invoke logic in the user commands,
slurmd daemon, and slurmstepd daemon.

## Failure Handling

If the Epilog fails (returns a non-zero exit code), this will result in the node being set to a
DRAIN state. If the EpilogSlurmctld fails (returns a non-zero exit code), this will only be logged.
If the Prolog fails (returns a non-zero exit code), this will result in the node being set to a
DRAIN state and the job requeued. The job will be placed in a held state unless
nohold_on_prolog_fail is configured in SchedulerParameters. If the PrologSlurmctld fails (returns a
non-zero exit code), this will cause the job to be requeued. Only batch jobs can be requeued.
Interactive jobs (salloc and srun) will be cancelled if the PrologSlurmctld fails.

If a task epilog or srun epilog fails (returns a non-zero exit code) this will only be logged. If a
task prolog fails (returns a non-zero exit code), the task will be canceled. If the srun prolog
fails (returns a non-zero exit code), the step will be canceled.

----------------------------------------------------------------------------------------------------

Based upon work by Jason Sollom, Cray Inc. and used by permission.

Last modified 03 May 2023
