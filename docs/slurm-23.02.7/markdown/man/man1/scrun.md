# NAME

**scrun** - an OCI runtime proxy for Slurm.

# SYNOPSIS

# Create Operation

**scrun** \[*GLOBAL OPTIONS*...\] *create* \[*CREATE OPTIONS*\] \<*container-id*\>

> Prepares a new container with container-id in current working directory.

# Start Operation

**scrun** \[*GLOBAL OPTIONS*...\] *start* \<*container-id*\>

> Request to start and run container in job.

# Query State Operation

**scrun** \[*GLOBAL OPTIONS*...\] *state* \<*container-id*\>

> Output OCI defined JSON state of container.

# Kill Operation

**scrun** \[*GLOBAL OPTIONS*...\] *kill* \<*container-id*\> \[*signal*\]

> Send signal (default: SIGTERM) to container.

# Delete Operation

**scrun** \[*GLOBAL OPTIONS*...\] *delete* \[*DELETE OPTIONS*\] \<*container-id*\>

> Release any resources held by container locally and remotely.

Perform OCI runtime operations against *container-id* per:  
https://github.com/opencontainers/runtime-spec/blob/main/runtime.md

**scrun** attempts to mimic the commandline behavior as closely as possible to **crun**(1) and
**runc**(1) in order to maintain in place replacement compatibility with **DOCKER**(1) and
**podman**(1). All commandline arguments for **crun**(1) and **runc**(1) will be accepted for
compatibility but may be ignored depending on their applicability.

# DESCRIPTION

**scrun** is an OCI runtime proxy for Slurm. **scrun** will accept all commands as an OCI compliant
runtime but will instead proxy the container and all STDIO to Slurm for scheduling and execution.
The containers will be executed remotely on Slurm compute nodes according to settings in
**oci.conf**(5).

**scrun** requires all containers to be OCI image compliant per:  
https://github.com/opencontainers/image-spec/blob/main/spec.md

# RETURN VALUE

On successful operation, **scrun** will return 0. For any other condition **scrun** will return any
non-zero number to denote a error.

# GLOBAL OPTIONS

**--cgroup-manager**  
Ignored.

<!-- -->

**--debug**  
Activate debug level logging.

<!-- -->

**-f** \<*slurm_conf_path*\>  
Use specified slurm.conf for configuration.  
Default: sysconfdir from **configure** during compilation

<!-- -->

**--usage**  
Show quick help on how to call **scrun**

<!-- -->

**--log-format**=\<*json\|text*\>  
Optional select format for logging. May be "json" or "text".  
Default: text

<!-- -->

**--root**=\<*root_path*\>  
Path to spool directory to communication sockets and temporary directories and files. This should be
a tmpfs and should be cleared on reboot.  
Default: /run/user/*{user_id}*/scrun/

<!-- -->

**--rootless**  
Ignored. All **scrun** commands are always rootless.

<!-- -->

**--systemd-cgroup**  
Ignored.

<!-- -->

**-v**  
Increase logging verbosity. Multiple -v's increase verbosity.

<!-- -->

**-V**, **--version**  
Print version information and exit.

# CREATE OPTIONS

**-b** \<*bundle_path*\>, **--bundle**=\<*bundle_path*\>  
Path to the root of the bundle directory.  
Default: caller's working directory

<!-- -->

**--console-socket**=\<*console_socket_path*\>  
Optional path to an AF_UNIX socket which will receive a file descriptor referencing the master end
of the console's pseudoterminal.  
Default: *ignored*

<!-- -->

**--no-pivot**  
Ignored.

<!-- -->

**--no-new-keyring**  
Ignored.

<!-- -->

**--pid-file**=\<*pid_file_path*\>  
Specify the file to lock and populate with process ID.  
Default: *ignored*

<!-- -->

**--preserve-fds**  
Ignored.

# DELETE OPTIONS

**--force**  
Ignored. All delete requests are forced and will kill any running jobs.

# INPUT ENVIRONMENT VARIABLES

**SCRUN_DEBUG**=\<quiet\|fatal\|error\|info\|verbose\|debug\|debug2\|debug3\|debug4\|debug5\>  
Set logging level.

<!-- -->

**SCRUN_STDERR_DEBUG**=\<quiet\|fatal\|error\|info\|verbose\|debug\|debug2\|debug3\|debug4\|debug5\>  
Set logging level for standard error output only.

<!-- -->

**SCRUN_SYSLOG_DEBUG**=\<quiet\|fatal\|error\|info\|verbose\|debug\|debug2\|debug3\|debug4\|debug5\>  
Set logging level for syslogging only.

<!-- -->

**SCRUN_FILE_DEBUG**=\<quiet\|fatal\|error\|info\|verbose\|debug\|debug2\|debug3\|debug4\|debug5\>  
Set logging level for log file only.

# JOB INPUT ENVIRONMENT VARIABLES

**SCRUN_ACCOUNT**  
See **SLURM_ACCOUNT** from **srun**(1).

<!-- -->

**SCRUN_ACCTG_FREQ**  
See **SLURM_ACCTG_FREQ** from **srun**(1).

<!-- -->

**SCRUN_BURST_BUFFER**  
See **SLURM_BURST_BUFFER** from **srun**(1).

<!-- -->

**SCRUN_CLUSTER_CONSTRAINT**  
See **SLURM_CLUSTER_CONSTRAINT** from **srun**(1).

<!-- -->

**SCRUN_CLUSTERS**  
See **SLURM_CLUSTERS** from **srun**(1).

<!-- -->

**SCRUN_CONSTRAINT**  
See **SLURM_CONSTRAINT** from **srun**(1).

<!-- -->

**SLURM_CORE_SPEC**  
See **SLURM_ACCOUNT** from **srun**(1).

<!-- -->

**SCRUN_CPU_BIND**  
See **SLURM_CPU_BIND** from **srun**(1).

<!-- -->

**SCRUN_CPU_FREQ_REQ**  
See **SLURM_CPU_FREQ_REQ** from **srun**(1).

<!-- -->

**SCRUN_CPUS_PER_GPU**  
See **SLURM_CPUS_PER_GPU** from **srun**(1).

<!-- -->

**SCRUN_CPUS_PER_TASK**  
See **SRUN_CPUS_PER_TASK** from **srun**(1).

<!-- -->

**SCRUN_DELAY_BOOT**  
See **SLURM_DELAY_BOOT** from **srun**(1).

<!-- -->

**SCRUN_DEPENDENCY**  
See **SLURM_DEPENDENCY** from **srun**(1).

<!-- -->

**SCRUN_DISTRIBUTION**  
See **SLURM_DISTRIBUTION** from **srun**(1).

<!-- -->

**SCRUN_EPILOG**  
See **SLURM_EPILOG** from **srun**(1).

<!-- -->

**SCRUN_EXACT**  
See **SLURM_EXACT** from **srun**(1).

<!-- -->

**SCRUN_EXCLUSIVE**  
See **SLURM_EXCLUSIVE** from **srun**(1).

<!-- -->

**SCRUN_GPU_BIND**  
See **SLURM_GPU_BIND** from **srun**(1).

<!-- -->

**SCRUN_GPU_FREQ**  
See **SLURM_GPU_FREQ** from **srun**(1).

<!-- -->

**SCRUN_GPUS**  
See **SLURM_GPUS** from **srun**(1).

<!-- -->

**SCRUN_GPUS_PER_NODE**  
See **SLURM_GPUS_PER_NODE** from **srun**(1).

<!-- -->

**SCRUN_GPUS_PER_SOCKET**  
See **SLURM_GPUS_PER_SOCKET** from **salloc**(1).

<!-- -->

**SCRUN_GPUS_PER_TASK**  
See **SLURM_GPUS_PER_TASK** from **srun**(1).

<!-- -->

**SCRUN_GRES_FLAGS**  
See **SLURM_GRES_FLAGS** from **srun**(1).

<!-- -->

**SCRUN_GRES**  
See **SLURM_GRES** from **srun**(1).

<!-- -->

**SCRUN_HINT**  
See **SLURM_HIST** from **srun**(1).

<!-- -->

**SCRUN_JOB_NAME**  
See **SLURM_JOB_NAME** from **srun**(1).

<!-- -->

**SCRUN_JOB_NODELIST**  
See **SLURM_JOB_NODELIST** from **srun**(1).

<!-- -->

**SCRUN_JOB_NUM_NODES**  
See **SLURM_JOB_NUM_NODES** from **srun**(1).

<!-- -->

**SCRUN_LABELIO**  
See **SLURM_LABELIO** from **srun**(1).

<!-- -->

**SCRUN_MEM_BIND**  
See **SLURM_MEM_BIND** from **srun**(1).

<!-- -->

**SCRUN_MEM_PER_CPU**  
See **SLURM_MEM_PER_CPU** from **srun**(1).

<!-- -->

**SCRUN_MEM_PER_GPU**  
See **SLURM_MEM_PER_GPU** from **srun**(1).

<!-- -->

**SCRUN_MEM_PER_NODE**  
See **SLURM_MEM_PER_NODE** from **srun**(1).

<!-- -->

**SCRUN_MPI_TYPE**  
See **SLURM_MPI_TYPE** from **srun**(1).

<!-- -->

**SCRUN_NCORES_PER_SOCKET**  
See **SLURM_NCORES_PER_SOCKET** from **srun**(1).

<!-- -->

**SCRUN_NETWORK**  
See **SLURM_NETWORK** from **srun**(1).

<!-- -->

**SCRUN_NSOCKETS_PER_NODE**  
See **SLURM_NSOCKETS_PER_NODE** from **srun**(1).

<!-- -->

**SCRUN_NTASKS**  
See **SLURM_NTASKS** from **srun**(1).

<!-- -->

**SCRUN_NTASKS_PER_CORE**  
See **SLURM_NTASKS_PER_CORE** from **srun**(1).

<!-- -->

**SCRUN_NTASKS_PER_GPU**  
See **SLURM_NTASKS_PER_GPU** from **srun**(1).

<!-- -->

**SCRUN_NTASKS_PER_NODE**  
See **SLURM_NTASKS_PER_NODE** from **srun**(1).

<!-- -->

**SCRUN_NTASKS_PER_TRES**  
See **SLURM_NTASKS_PER_TRES** from **srun**(1).

<!-- -->

**SCRUN_OPEN_MODE**  
See **SLURM_MODE** from **srun**(1).

<!-- -->

**SCRUN_OVERCOMMIT**  
See **SLURM_OVERCOMMIT** from **srun**(1).

<!-- -->

**SCRUN_OVERLAP**  
See **SLURM_OVERLAP** from **srun**(1).

<!-- -->

**SCRUN_PARTITION**  
See **SLURM_PARTITION** from **srun**(1).

<!-- -->

**SCRUN_POWER**  
See **SLURM_POWER** from **srun**(1).

<!-- -->

**SCRUN_PROFILE**  
See **SLURM_PROFILE** from **srun**(1).

<!-- -->

**SCRUN_PROLOG**  
See **SLURM_PROLOG** from **srun**(1).

<!-- -->

**SCRUN_QOS**  
See **SLURM_QOS** from **srun**(1).

<!-- -->

**SCRUN_REMOTE_CWD**  
See **SLURM_REMOTE_CWD** from **srun**(1).

<!-- -->

**SCRUN_REQ_SWITCH**  
See **SLURM_REQ_SWITCH** from **srun**(1).

<!-- -->

**SCRUN_RESERVATION**  
See **SLURM_RESERVATION** from **srun**(1).

<!-- -->

**SCRUN_SIGNAL**  
See **SLURM_SIGNAL** from **srun**(1).

<!-- -->

**SCRUN_SLURMD_DEBUG**  
See **SLURMD_DEBUG** from **srun**(1).

<!-- -->

**SCRUN_SPREAD_JOB**  
See **SLURM_SPREAD_JOB** from **srun**(1).

<!-- -->

**SCRUN_TASK_EPILOG**  
See **SLURM_TASK_EPILOG** from **srun**(1).

<!-- -->

**SCRUN_TASK_PROLOG**  
See **SLURM_TASK_PROLOG** from **srun**(1).

<!-- -->

**SCRUN_THREAD_SPEC**  
See **SLURM_THREAD_SPEC** from **srun**(1).

<!-- -->

**SCRUN_THREADS_PER_CORE**  
See **SLURM_THREADS_PER_CORE** from **srun**(1).

<!-- -->

**SCRUN_THREADS**  
See **SLURM_THREADS** from **srun**(1).

<!-- -->

**SCRUN_TIMELIMIT**  
See **SLURM_TIMELIMIT** from **srun**(1).

<!-- -->

**SCRUN_TRES_PER_TASK**  
See **SLURM_TRES_PER_TASK** from **srun**(1).

<!-- -->

**SCRUN_UNBUFFEREDIO**  
See **SLURM_UNBUFFEREDIO** from **srun**(1).

<!-- -->

**SCRUN_USE_MIN_NODES**  
See **SLURM_USE_MIN_NODES** from **srun**(1).

<!-- -->

**SCRUN_WAIT4SWITCH**  
See **SLURM_WAIT4SWITCH** from **srun**(1).

<!-- -->

**SCRUN_WCKEY**  
See **SLURM_WCKEY** from **srun**(1).

<!-- -->

**SCRUN_WORKING_DIR**  
See **SLURM_WORKING_DIR** from **srun**(1).

# OUTPUT ENVIRONMENT VARIABLES

**SCRUN_OCI_VERSION**  
Advertised version of OCI compliance of container.

<!-- -->

**SCRUN_CONTAINER_ID**  
Value based as *container_id* during create operation.

<!-- -->

**SCRUN_PID**  
PID of process used to monitor and control container on allocation node.

<!-- -->

**SCRUN_BUNDLE**  
Path to container bundle directory.

<!-- -->

**SCRUN_SUBMISSION_BUNDLE**  
Path to container bundle directory before modification by Lua script.

<!-- -->

**SCRUN_ANNOTATION\_\***  
List of annotations from container's config.json.

<!-- -->

**SCRUN_PID_FILE**  
Path to pid file that is locked and populated with PID of scrun.

<!-- -->

**SCRUN_SOCKET**  
Path to control socket for scrun.

<!-- -->

**SCRUN_SPOOL_DIR**  
Path to workspace for all temporary files for current container. Purged by deletion operation.

<!-- -->

**SCRUN_SUBMISSION_CONFIG_FILE**  
Path to container's config.json file at time of submission.

<!-- -->

**SCRUN_USER**  
Name of user that called create operation.

<!-- -->

**SCRUN_USER_ID**  
Numeric ID of user that called create operation.

<!-- -->

**SCRUN_GROUP**  
Name of user's primary group that called create operation.

<!-- -->

**SCRUN_GROUP_ID**  
Numeric ID of user primary group that called create operation.

<!-- -->

**SCRUN_ROOT**  
See **--root**.

<!-- -->

**SCRUN_ROOTFS_PATH**  
Path to container's root directory.

<!-- -->

**SCRUN_SUBMISSION_ROOTFS_PATH**  
Path to container's root directory at submission time.

<!-- -->

**SCRUN_LOG_FILE**  
Path to scrun's log file during create operation.

<!-- -->

**SCRUN_LOG_FORMAT**  
Log format type during create operation.

# JOB OUTPUT ENVIRONMENT VARIABLES

**SLURM\_\*\_HET_GROUP\_#**  
For a heterogeneous job allocation, the environment variables are set separately for each component.

<!-- -->

**SLURM_CLUSTER_NAME**  
Name of the cluster on which the job is executing.

<!-- -->

**SLURM_CONTAINER**  
OCI Bundle for job.

<!-- -->

**SLURM_CONTAINER_ID**  
OCI id for job.

<!-- -->

**SLURM_CPUS_PER_GPU**  
Number of CPUs requested per allocated GPU.

<!-- -->

**SLURM_CPUS_PER_TASK**  
Number of CPUs requested per task.

<!-- -->

**SLURM_DIST_PLANESIZE**  
Plane distribution size. Only set for plane distributions.

<!-- -->

**SLURM_DISTRIBUTION**  
Distribution type for the allocated jobs.

<!-- -->

**SLURM_GPU_BIND**  
Requested binding of tasks to GPU.

<!-- -->

**SLURM_GPU_FREQ**  
Requested GPU frequency.

<!-- -->

**SLURM_GPUS**  
Number of GPUs requested.

<!-- -->

**SLURM_GPUS_PER_NODE**  
Requested GPU count per allocated node.

<!-- -->

**SLURM_GPUS_PER_SOCKET**  
Requested GPU count per allocated socket.

<!-- -->

**SLURM_GPUS_PER_TASK**  
Requested GPU count per allocated task.

<!-- -->

**SLURM_HET_SIZE**  
Set to count of components in heterogeneous job.

<!-- -->

**SLURM_JOB_ACCOUNT**  
Account name associated of the job allocation.

<!-- -->

**SLURM_JOB_CPUS_PER_NODE**  
Count of CPUs available to the job on the nodes in the allocation, using the format
*CPU_count*\[(x*number_of_nodes*)\]\[,*CPU_count* \[(x*number_of_nodes*)\] ...\]. For example:
SLURM_JOB_CPUS_PER_NODE='72(x2),36' indicates that on the first and second nodes (as listed by
SLURM_JOB_NODELIST) the allocation has 72 CPUs, while the third node has 36 CPUs. **NOTE**: The
**select/linear** plugin allocates entire nodes to jobs, so the value indicates the total count of
CPUs on allocated nodes. The **select/cons_res** and **select/cons_tres** plugins allocate
individual CPUs to jobs, so this number indicates the number of CPUs allocated to the job.

<!-- -->

**SLURM_JOB_END_TIME**  
The UNIX timestamp for a job's projected end time.

<!-- -->

**SLURM_JOB_GPUS**  
The global GPU IDs of the GPUs allocated to this job. The GPU IDs are not relative to any device
cgroup, even if devices are constrained with task/cgroup. Only set in batch and interactive jobs.

<!-- -->

**SLURM_JOB_ID**  
The ID of the job allocation.

<!-- -->

**SLURM_JOB_NODELIST**  
List of nodes allocated to the job.

<!-- -->

**SLURM_JOB_NUM_NODES**  
Total number of nodes in the job allocation.

<!-- -->

**SLURM_JOB_PARTITION**  
Name of the partition in which the job is running.

<!-- -->

**SLURM_JOB_QOS**  
Quality Of Service (QOS) of the job allocation.

<!-- -->

**SLURM_JOB_RESERVATION**  
Advanced reservation containing the job allocation, if any.

<!-- -->

**SLURM_JOB_START_TIME**  
UNIX timestamp for a job's start time.

<!-- -->

**SLURM_MEM_BIND**  
Bind tasks to memory.

<!-- -->

**SLURM_MEM_BIND_LIST**  
Set to bit mask used for memory binding.

<!-- -->

**SLURM_MEM_BIND_PREFER**  
Set to "prefer" if the **SLURM_MEM_BIND** option includes the prefer option.

<!-- -->

**SLURM_MEM_BIND_SORT**  
Sort free cache pages (run zonesort on Intel KNL nodes)

<!-- -->

**SLURM_MEM_BIND_TYPE**  
Set to the memory binding type specified with the **SLURM_MEM_BIND** option. Possible values are
"none", "rank", "map_map", "mask_mem" and "local".

<!-- -->

**SLURM_MEM_BIND_VERBOSE**  
Set to "verbose" if the **SLURM_MEM_BIND** option includes the verbose option. Set to "quiet"
otherwise.

<!-- -->

**SLURM_MEM_PER_CPU**  
Minimum memory required per usable allocated CPU.

<!-- -->

**SLURM_MEM_PER_GPU**  
Requested memory per allocated GPU.

<!-- -->

**SLURM_MEM_PER_NODE**  
Specify the real memory required per node.

<!-- -->

**SLURM_NODE_ALIASES**  
Sets of node name, communication address and hostname for nodes allocated to the job from the cloud.
Each element in the set if colon separated and each set is comma separated. For example:
SLURM_NODE_ALIASES=ec0:1.2.3.4:foo,ec1:1.2.3.5:bar

<!-- -->

**SLURM_NTASKS**  
Specify the number of tasks to run.

<!-- -->

**SLURM_NTASKS_PER_CORE**  
Request the maximum *ntasks* be invoked on each core.

<!-- -->

**SLURM_NTASKS_PER_GPU**  
Request that there are *ntasks* tasks invoked for every GPU.

<!-- -->

**SLURM_NTASKS_PER_NODE**  
Request that *ntasks* be invoked on each node.

<!-- -->

**SLURM_NTASKS_PER_SOCKET**  
Request the maximum *ntasks* be invoked on each socket.

<!-- -->

**SLURM_OVERCOMMIT**  
Overcommit resources.

<!-- -->

**SLURM_PROFILE**  
Enables detailed data collection by the acct_gather_profile plugin.

<!-- -->

**SLURM_SHARDS_ON_NODE**  
Number of GPU Shards available to the step on this node.

<!-- -->

**SLURM_SUBMIT_HOST**  
The hostname of the computer from which **scrun** was invoked.

<!-- -->

**SLURM_TASKS_PER_NODE**  
Number of tasks to be initiated on each node. Values are comma separated and in the same order as
SLURM_JOB_NODELIST. If two or more consecutive nodes are to have the same task count, that count is
followed by "(x#)" where "#" is the repetition count. For example, "SLURM_TASKS_PER_NODE=2(x3),1"
indicates that the first three nodes will each execute two tasks and the fourth node will execute
one task.

<!-- -->

**SLURM_THREADS_PER_CORE**  
This is only set if **--threads-per-core** or **SCRUN_THREADS_PER_CORE** were specified. The value
will be set to the value specified by **--threads-per-core** or **SCRUN_THREADS_PER_CORE**. This is
used by subsequent srun calls within the job allocation.

# SCRUN.LUA

/etc/slurm/**scrun.lua** must be present on any node where **scrun** will be invoked. **scrun.lua**
must be a compliant **lua**(1) script.

## Required functions

The following functions must be defined.

· function **slurm_scrun_stage_in**(**id**, **bundle**, **spool_dir**, **config_file**, **job_id**, **user_id**, **group_id**, **job_env**)  
Called right after job allocation to stage container into job node(s). Must return *SLURM.success*
or job will be cancelled. It is required that function will prepare the container for execution on
job node(s) as required to run as configured in **oci.conf**(1). The function may block as long as
required until container has been fully prepared (up to the job's max wall time).

**id**  
Container ID

**bundle**  
OCI bundle path

**spool_dir**  
Temporary working directory for container

**config_file**  
Path to config.json for container

**job_id**  
*jobid* of job allocation

**user_id**  
Resolved numeric user id of job allocation. It is generally expected that the lua script will be
executed inside of a user namespace running under the *root(0)* user.

**group_id**  
Resolved numeric group id of job allocation. It is generally expected that the lua script will be
executed inside of a user namespace running under the *root(0)* group.

**job_env**  
Table with each entry of Key=Value or Value of each environment variable of the job.

<!-- -->

· function **slurm_scrun_stage_out**(**id**, **bundle**, **orig_bundle**, **root_path**, **orig_root_path**, **spool_dir**, **config_file**, **jobid**, **user_id**, **group_id**)  
Called right after container step completes to stage out files from job nodes. Must return
*SLURM.success* or job will be cancelled. It is required that function will pull back any changes
and cleanup the container on job node(s). The function may block as long as required until container
has been fully prepared (up to the job's max wall time).

> **id**  
> Container ID
>
> **bundle**  
> OCI bundle path
>
> **orig_bundle**  
> Originally submitted OCI bundle path before modification by **set_bundle_path**().
>
> **root_path**  
> Path to directory root of container contents.
>
> **orig_root_path**  
> Original path to directory root of container contents before modification by **set_root_path**().
>
> **spool_dir**  
> Temporary working directory for container
>
> **config_file**  
> Path to config.json for container
>
> **job_id**  
> *jobid* of job allocation
>
> **user_id**  
> Resolved numeric user id of job allocation. It is generally expected that the lua script will be
> executed inside of a user namespace running under the *root(0)* user.
>
> **group_id**  
> Resolved numeric group id of job allocation. It is generally expected that the lua script will be
> executed inside of a user namespace running under the *root(0)* group.

## Provided functions

The following functions are provided for any Lua function to call as needed.

· **slurm.set_bundle_path**(*PATH*)  
Called to notify **scrun** to use *PATH* as new OCI container bundle path. Depending on the
filesystem layout, cloning the container bundle may be required to allow execution on job nodes.

<!-- -->

· **slurm.set_root_path**(*PATH*)  
Called to notify **scrun** to use *PATH* as new container root filesystem path. Depending on the
filesystem layout, cloning the container bundle may be required to allow execution on job nodes.
Script must also update \#/root/path in config.json when changing root path.

<!-- -->

· *STATUS*,*OUTPUT* = **slurm.remote_command**(*SCRIPT*)  
Run *SCRIPT* in new job step on all job nodes. Returns numeric job status as *STATUS* and job stdio
as *OUTPUT*. Blocks until *SCRIPT* exits.

<!-- -->

· *STATUS*,*OUTPUT* = **slurm.allocator_command**(*SCRIPT*)  
Run *SCRIPT* as forked child process of **scrun**. Returns numeric job status as *STATUS* and job
stdio as *OUTPUT*. Blocks until *SCRIPT* exits.

<!-- -->

· **slurm.log**(*MSG*, *LEVEL*)  
Log *MSG* at log *LEVEL*. Valid range of values for *LEVEL* is \[0, 4\].

<!-- -->

· **slurm.error**(*MSG*)  
Log error *MSG*.

<!-- -->

· **slurm.log_error**(*MSG*)  
Log error *MSG*.

<!-- -->

· **slurm.log_info**(*MSG*)  
Log *MSG* at log level INFO.

<!-- -->

· **slurm.log_verbose**(*MSG*)  
Log *MSG* at log level VERBOSE.

<!-- -->

· **slurm.log_verbose**(*MSG*)  
Log *MSG* at log level VERBOSE.

<!-- -->

· **slurm.log_debug**(*MSG*)  
Log *MSG* at log level DEBUG.

<!-- -->

· **slurm.log_debug2**(*MSG*)  
Log *MSG* at log level DEBUG2.

<!-- -->

· **slurm.log_debug3**(*MSG*)  
Log *MSG* at log level DEBUG3.

<!-- -->

· **slurm.log_debug4**(*MSG*)  
Log *MSG* at log level DEBUG4.

<!-- -->

· *MINUTES* = **slurm.time_str2mins**(*TIME_STRING*)  
Parse *TIME_STRING* into number of minutes as *MINUTES*. Valid formats:

· days-\[hours\[:minutes\[:seconds\]\]\]  
· hours:minutes:seconds  
· minutes\[:seconds\]  
· -1  
· INFINITE  
· UNLIMITED  

## Example **scrun.lua** scripts

Minimal required for **scrun** operation:  
    function slurm_scrun_stage_in(id, bundle, spool_dir, config_file, job_id, user_id, group_id, job_env)
    	return slurm.SUCCESS
    end

    function slurm_scrun_stage_out(id, bundle, orig_bundle, root_path, orig_root_path, spool_dir, config_file, jobid, user_id, group_id)
    	return slurm.SUCCESS
    end

    return slurm.SUCCESS

<!-- -->

Full Container staging using rsync:  
This is full example that will stage container as given by **docker**(1) or **podman**(1).
Container's config.json is modified to remove unwanted functions that may cause container run to
under **crun**(1) or **crun**(1). Script uses rsync to move container to an shared /home filesystem.

    local json = require 'json'
    local open = io.open

    local function read_file(path)
    	local file = open(path, "rb")
    	if not file then return nil end
    	local content = file:read "*all"
    	file:close()
    	return content
    end

    local function write_file(path, contents)
    	local file = open(path, "wb")
    	if not file then return nil end
    	file:write(contents)
    	file:close()
    	return
    end

    function slurm_scrun_stage_in(id, bundle, spool_dir, config_file, job_id, user_id, group_id, job_env)
    	slurm.log_debug(string.format("stage_in(%s, %s, %s, %s, %d, %d, %d)",
    		       id, bundle, spool_dir, config_file, job_id, user_id, group_id))

    	local status, output, user, rc
    	local config = json.decode(read_file(config_file))
    	local src_rootfs = config["root"]["path"]
    	rc, user = slurm.allocator_command(string.format("id -un %d", user_id))
    	user = string.gsub(user, "%s+", "")
    	local root = "/home/"..user.."/containers/"
    	local dst_bundle = root.."/"..id.."/"
    	local dst_config = root.."/"..id.."/config.json"
    	local dst_rootfs = root.."/"..id.."/rootfs/"

    	if string.sub(src_rootfs, 1, 1) ~= "/"
    	then
    		-- always use absolute path
    		src_rootfs = string.format("%s/%s", bundle, src_rootfs)
    	end

    	status, output = slurm.allocator_command("mkdir -p "..dst_rootfs)
    	if (status ~= 0)
    	then
    		slurm.log_info(string.format("mkdir(%s) failed %u: %s",
    			       dst_rootfs, status, output))
    		return slurm.ERROR
    	end

    	status, output = slurm.allocator_command(string.format("/usr/bin/env rsync --exclude sys --exclude proc --numeric-ids --delete-after --ignore-errors --stats -a -- %s/ %s/", src_rootfs, dst_rootfs))
    	if (status ~= 0)
    	then
    		-- rsync can fail due to permissions which may not matter
    		slurm.log_info(string.format("WARNING: rsync failed: %s", output))
    	end

    	slurm.set_bundle_path(dst_bundle)
    	slurm.set_root_path(dst_rootfs)

    	config["root"]["path"] = dst_rootfs

    	-- Always force user namespace support in container or runc will reject
    	if ((config["process"] ~= nil) and (config["process"]["user"] ~= nil))
    	then
    		-- purge additionalGids as they are not supported in rootless
    		config["process"]["user"]["additionalGids"] = nil
    	end

    	if (config["linux"] ~= nil)
    	then
    		-- force user namespace to always be defined for rootless mode
    		local found = false
    		if (config["linux"]["namespaces"] == nil)
    		then
    			config["linux"]["namespaces"] = {}
    		else
    			for _, namespace in ipairs(config["linux"]["namespaces"]) do
    				if (namespace["type"] == "user")
    				then
    					found=true
    					break
    				end
    			end
    		end
    		if (found == false)
    		then
    			table.insert(config["linux"]["namespaces"], {type= "user"})
    		end

    		-- clear all attempts to map uid/gids
    		config["linux"]["uidMappings"] = nil
    		config["linux"]["gidMappings"] = nil

    		-- disable trying to use a specific cgroup
    		config["linux"]["cgroupsPath"] = nil
    	end

    	if (config["mounts"] ~= nil)
    	then
    		-- Find and remove any user/group settings in mounts
    		for _, mount in ipairs(config["mounts"]) do
    			local opts = {}

    			if (mount["options"] ~= nil)
    			then
    				for _, opt in ipairs(mount["options"]) do
    					if ((string.sub(opt, 1, 4) ~= "gid=") and (string.sub(opt, 1, 4) ~= "uid="))
    					then
    						table.insert(opts, opt)
    					end
    				end
    			end

    			mount["options"] = opts
    		end

    		-- Remove all bind mounts by copying files into rootfs
    		local mounts = {}
    		for i, mount in ipairs(config["mounts"]) do
    			if ((mount["type"] ~= nil) and (mount["type"] == "bind") and (string.sub(mount["source"], 1, 4) ~= "/sys") and (string.sub(mount["source"], 1, 5) ~= "/proc"))
    			then
    				status, output = slurm.allocator_command(string.format("/usr/bin/env rsync --numeric-ids --ignore-errors --stats -a -- %s %s", mount["source"], dst_rootfs..mount["destination"]))
    				if (status ~= 0)
    				then
    					-- rsync can fail due to permissions which may not matter
    					slurm.log_info("rsync failed")
    				end
    			else
    				table.insert(mounts, mount)
    			end
    		end
    		config["mounts"] = mounts
    	end

    	-- Merge in Job environment into container
    	if (config["process"]["env"] == nil)
    	then
    		config["process"]["env"] = {}
    	end
    	for _, env in ipairs(job_env) do
    		table.insert(config["process"]["env"], env)
    	end

    	-- Remove all prestart hooks to squash any networking attempts
    	if ((config["hooks"] ~= nil) and (config["hooks"]["prestart"] ~= nil))
    	then
    		config["hooks"]["prestart"] = nil
    	end

    	-- Remove all rlimits
    	if ((config["process"] ~= nil) and (config["process"]["rlimits"] ~= nil))
    	then
    		config["process"]["rlimits"] = nil
    	end

    	write_file(dst_config, json.encode(config))
    	slurm.log_info("created: "..dst_config)

    	return slurm.SUCCESS
    end

    function slurm_scrun_stage_out(id, bundle, orig_bundle, root_path, orig_root_path, spool_dir, config_file, jobid, user_id, group_id)
    	slurm.log_debug(string.format("stage_out(%s, %s, %s, %s, %s, %s, %s, %d, %d, %d)",
    		       id, bundle, orig_bundle, root_path, orig_root_path, spool_dir, config_file, jobid, user_id, group_id))

    	if (bundle == orig_bundle)
    	then
    		slurm.log_info(string.format("skipping stage_out as bundle=orig_bundle=%s", bundle))
    		return slurm.SUCCESS
    	end

    	status, output = slurm.allocator_command(string.format("/usr/bin/env rsync --numeric-ids --delete-after --ignore-errors --stats -a -- %s/ %s/", root_path, orig_root_path))
    	if (status ~= 0)
    	then
    		-- rsync can fail due to permissions which may not matter
    		slurm.log_info("rsync failed")
    	end

    	return slurm.SUCCESS
    end

    slurm.log_info("initialized scrun.lua")

    return slurm.SUCCESS

# SIGNALS

When **scrun** receives SIGINT, it will attempt to gracefully cancel any related jobs (if any) and
cleanup.

# COPYING

Copyright (C) 2023 SchedMD LLC.

This file is part of Slurm, a resource management program. For details, see
\<https://slurm.schedmd.com/\>.

Slurm is free software; you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

Slurm is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
License for more details.

# SEE ALSO

**Slurm**(1), **oci.conf**(5), **srun**(1), **crun**(1), **runc**(1), **DOCKER**(1) and
**podman**(1)
