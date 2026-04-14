# NAME

slurm.conf - Slurm configuration file

# DESCRIPTION

**slurm.conf** is an ASCII file which describes general Slurm configuration information, the nodes
to be managed, information about how those nodes are grouped into partitions, and various scheduling
parameters associated with those partitions. This file should be consistent across all nodes in the
cluster.

The file location can be modified at execution time by setting the SLURM_CONF environment variable.
The Slurm daemons also allow you to override both the built-in and environment-provided location
using the "-f" option on the command line.

The contents of the file are case insensitive except for the names of nodes and partitions. Any text
following a "#" in the configuration file is treated as a comment through the end of that line.
Changes to the configuration file take effect upon restart of Slurm daemons, daemon receipt of the
SIGHUP signal, or execution of the command "scontrol reconfigure" unless otherwise noted.

If a line begins with the word "Include" followed by whitespace and then a file name, that file will
be included inline with the current configuration file. For large or complex systems, multiple
configuration files may prove easier to manage and enable reuse of some files (See INCLUDE MODIFIERS
for more details).

Note on file permissions:

The *slurm.conf* file must be readable by all users of Slurm, since it is used by many of the Slurm
commands. Other files that are defined in the *slurm.conf* file, such as log files and job
accounting files, may need to be created/owned by the user "SlurmUser" to be successfully accessed.
Use the "chown" and "chmod" commands to set the ownership and permissions appropriately. See the
section **FILE AND DIRECTORY PERMISSIONS** for information about the various files and directories
used by Slurm.

# PARAMETERS

The overall configuration parameters available include:

**AccountingStorageBackupHost**  
The name of the backup machine hosting the accounting storage database. If used with the
accounting_storage/slurmdbd plugin, this is where the backup slurmdbd would be running. Only used
with systems using SlurmDBD, ignored otherwise.

<!-- -->

**AccountingStorageEnforce**  
This controls what level of association-based enforcement to impose on job submissions. Valid
options are any combination of *associations*, *limits*, *nojobs*, *nosteps*, *qos*, *safe*, and
*wckeys*, or *all* for all things (except nojobs and nosteps, which must be requested as well).

If *limits*, *qos*, or *wckeys* are set, *associations* will automatically be set.

If *wckeys* is set, **TrackWCKey** will automatically be set.

If *safe* is set, *limits* and *associations* will automatically be set.

If *nojobs* is set, *nosteps* will automatically be set.

By setting *associations*, no new job is allowed to run unless a corresponding association exists in
the system. If *limits* are enforced, users can be limited by association to whatever job size or
run time limits are defined.

If *nojobs* is set, Slurm will not account for any jobs or steps on the system. Likewise, if
*nosteps* is set, Slurm will not account for any steps that have run.

If *safe* is enforced, a job will only be launched against an association or qos that has a
TRES-minutes limit set, if the job will be able to run to completion. Without this option set, jobs
will be launched as long as their usage hasn't reached the TRES-minutes limit. This can lead to jobs
being launched but then killed when the limit is reached. With the 'safe' option set, a job won't be
killed due to limits, even if the limits are changed after the job was started and the association
or qos violates the updated limits.

With *qos* and/or *wckeys* enforced jobs will not be scheduled unless a valid qos and/or workload
characterization key is specified.

A restart of slurmctld is required for changes to this parameter to take effect.

<!-- -->

**AccountingStorageExternalHost**  
A comma-separated list of external slurmdbds (\<host/ip\>\[:port\]\[,...\]) to register with. If no
port is given, the **AccountingStoragePort** will be used.

This allows clusters registered with the external slurmdbd to communicate with each other using the
*--cluster/-M* client command options.

The cluster will add itself to the external slurmdbd if it doesn't exist. If a non-external cluster
already exists on the external slurmdbd, the slurmctld will ignore registering to the external
slurmdbd.

<!-- -->

**AccountingStorageHost**  
The name of the machine hosting the accounting storage database. Only used with systems using
SlurmDBD, ignored otherwise.

<!-- -->

**AccountingStorageParameters**  
Comma-separated list of key-value pair parameters. Currently supported values include options to
establish a secure connection to the database:

> **SSL_CERT**  
> The path name of the client public key certificate file.
>
> <!-- -->
>
> **SSL_CA**  
> The path name of the Certificate Authority (CA) certificate file.
>
> <!-- -->
>
> **SSL_CAPATH**  
> The path name of the directory that contains trusted SSL CA certificate files.
>
> <!-- -->
>
> **SSL_KEY**  
> The path name of the client private key file.
>
> <!-- -->
>
> **SSL_CIPHER**  
> The list of permissible ciphers for SSL encryption.

**AccountingStoragePass**  
The password used to gain access to the database to store the accounting data. Only used for
database type storage plugins, ignored otherwise. In the case of Slurm DBD (Database Daemon) with
MUNGE authentication this can be configured to use a MUNGE daemon specifically configured to provide
authentication between clusters while the default MUNGE daemon provides authentication within a
cluster. In that case, **AccountingStoragePass** should specify the named port to be used for
communications with the alternate MUNGE daemon (e.g. "/var/run/munge/global.socket.2"). The default
value is NULL.

<!-- -->

**AccountingStoragePort**  
The listening port of the accounting storage database server. Only used for database type storage
plugins, ignored otherwise. The default value is SLURMDBD_PORT as established at system build time.
If no value is explicitly specified, it will be set to 6819. This value must be equal to the
**DbdPort** parameter in the slurmdbd.conf file.

<!-- -->

**AccountingStorageTRES**  
Comma-separated list of resources you wish to track on the cluster. These are the resources
requested by the sbatch/srun job when it is submitted. Currently this consists of any GRES, BB
(burst buffer) or license along with CPU, Memory, Node, Energy, FS/\[Disk\|Lustre\], IC/OFED, Pages,
and VMem. By default Billing, CPU, Energy, Memory, Node, FS/Disk, Pages and VMem are tracked. These
default TRES cannot be disabled, but only appended to.
AccountingStorageTRES=gres/craynetwork,license/iop1 will track billing, cpu, energy, memory, nodes,
fs/disk, pages and vmem along with a gres called craynetwork as well as a license called iop1.
Whenever these resources are used on the cluster they are recorded. The TRES are automatically set
up in the database on the start of the slurmctld.

If multiple GRES of different types are tracked (e.g. GPUs of different types), then job requests
with matching type specifications will be recorded. Given a configuration of
"AccountingStorageTRES=gres/gpu,gres/gpu:tesla,gres/gpu:volta" Then "gres/gpu:tesla" and
"gres/gpu:volta" will track only jobs that explicitly request those two GPU types, while "gres/gpu"
will track allocated GPUs of any type ("tesla", "volta" or any other GPU type).

Given a configuration of "AccountingStorageTRES=gres/gpu:tesla,gres/gpu:volta" Then "gres/gpu:tesla"
and "gres/gpu:volta" will track jobs that explicitly request those GPU types. If a job requests
GPUs, but does not explicitly specify the GPU type, then its resource allocation will be accounted
for as either "gres/gpu:tesla" or "gres/gpu:volta", although the accounting may not match the actual
GPU type allocated to the job and the GPUs allocated to the job could be heterogeneous. In an
environment containing various GPU types, use of a job_submit plugin may be desired in order to
force jobs to explicitly specify some GPU type.

**NOTE**: Setting gres/gpu will also set gres/gpumem and gres/gpuutil.

<!-- -->

**AccountingStorageType**  
The accounting storage mechanism type. Acceptable values at present include
"accounting_storage/none" and "accounting_storage/slurmdbd". The "accounting_storage/slurmdbd" value
indicates that accounting records will be written to the Slurm DBD, which manages an underlying
MySQL database. See "man slurmdbd" for more information. The default value is
"accounting_storage/none" and indicates that account records are not maintained.

<!-- -->

**AccountingStorageUser**  
The user account for accessing the accounting storage database. Only used for database type storage
plugins, ignored otherwise.

<!-- -->

**AccountingStoreFlags**  
Comma separated list used to tell the slurmctld to store extra fields that may be more heavy weight
than the normal job information.

> Current options are:  
>
> <!-- -->
>
> **job_comment**  
> Include the job's comment field in the job complete message sent to the Accounting Storage
> database. Note the AdminComment and SystemComment are always recorded in the database.
>
> <!-- -->
>
> **job_env**  
> Include a batch job's environment variables used at job submission in the job start message sent
> to the Accounting Storage database.
>
> <!-- -->
>
> **job_extra**  
> Include the job's extra field in the job complete message sent to the Accounting Storage database.
>
> <!-- -->
>
> **job_script**  
> Include the job's batch script in the job start message sent to the Accounting Storage database.

**AcctGatherNodeFreq**  
The AcctGather plugins sampling interval for node accounting. For AcctGather plugin values of none,
this parameter is ignored. For all other values this parameter is the number of seconds between node
accounting samples. For the acct_gather_energy/rapl plugin, set a value less than 300 because the
counters may overflow beyond this rate. The default value is zero. This value disables accounting
sampling for nodes. Note: The accounting sampling interval for jobs is determined by the value of
**JobAcctGatherFrequency**.

<!-- -->

**AcctGatherEnergyType**  
Identifies the plugin to be used for energy consumption accounting. The jobacct_gather plugin and
slurmd daemon call this plugin to collect energy consumption data for jobs and nodes. The collection
of energy consumption data takes place on the node level, hence only in case of exclusive job
allocation the energy consumption measurements will reflect the job's real consumption. In case of
node sharing between jobs the reported consumed energy per job (through sstat or sacct) will not
reflect the real energy consumed by the jobs.

Configurable values at present are:

> **acct_gather_energy/none**  
> No energy consumption data is collected.
>
> <!-- -->
>
> **acct_gather_energy/ipmi**  
> Energy consumption data is collected from the Baseboard Management Controller (BMC) using the
> Intelligent Platform Management Interface (IPMI).
>
> <!-- -->
>
> **acct_gather_energy/pm_counters**  
> Energy consumption data is collected from the Baseboard Management Controller (BMC) for HPE Cray
> systems.
>
> <!-- -->
>
> **acct_gather_energy/rapl**  
> Energy consumption data is collected from hardware sensors using the Running Average Power Limit
> (RAPL) mechanism. Note that enabling RAPL may require the execution of the command "sudo modprobe
> msr".
>
> <!-- -->
>
> **acct_gather_energy/xcc**  
> Energy consumption data is collected from the Lenovo SD650 XClarity Controller (XCC) using IPMI
> OEM raw commands.

**AcctGatherInterconnectType**  
Identifies the plugin to be used for interconnect network traffic accounting. The jobacct_gather
plugin and slurmd daemon call this plugin to collect network traffic data for jobs and nodes. The
collection of network traffic data takes place on the node level, hence only in case of exclusive
job allocation the collected values will reflect the job's real traffic. In case of node sharing
between jobs the reported network traffic per job (through sstat or sacct) will not reflect the real
network traffic by the jobs.

Configurable values at present are:

> **acct_gather_interconnect/none**  
> No infiniband network data are collected.
>
> <!-- -->
>
> **acct_gather_interconnect/ofed**  
> Infiniband network traffic data are collected from the hardware monitoring counters of Infiniband
> devices through the OFED library. In order to account for per job network traffic, add the
> "ic/ofed" TRES to *AccountingStorageTRES*.
>
> <!-- -->
>
> **acct_gather_interconnect/sysfs**  
> Network traffic statistics are collected from the Linux sysfs pseudo-filesystem for specific
> interfaces defined in **acct_gather.conf**(5). In order to account for per job network traffic,
> add the "ic/sysfs" TRES to *AccountingStorageTRES*.

**AcctGatherFilesystemType**  
Identifies the plugin to be used for filesystem traffic accounting. The jobacct_gather plugin and
slurmd daemon call this plugin to collect filesystem traffic data for jobs and nodes. The collection
of filesystem traffic data takes place on the node level, hence only in case of exclusive job
allocation the collected values will reflect the job's real traffic. In case of node sharing between
jobs the reported filesystem traffic per job (through sstat or sacct) will not reflect the real
filesystem traffic by the jobs.

Configurable values at present are:

> **acct_gather_filesystem/none**  
> No filesystem data are collected.
>
> <!-- -->
>
> **acct_gather_filesystem/lustre**  
> Lustre filesystem traffic data are collected from the counters found in /proc/fs/lustre/. In order
> to account for per job lustre traffic, add the "fs/lustre" TRES to *AccountingStorageTRES*.

**AcctGatherProfileType**  
Identifies the plugin to be used for detailed job profiling. The jobacct_gather plugin and slurmd
daemon call this plugin to collect detailed data such as I/O counts, memory usage, or energy
consumption for jobs and nodes. There are interfaces in this plugin to collect data as step start
and completion, task start and completion, and at the account gather frequency. The data collected
at the node level is related to jobs only in case of exclusive job allocation.

Configurable values at present are:

> **acct_gather_profile/none**  
> No profile data is collected.
>
> <!-- -->
>
> **acct_gather_profile/hdf5**  
> This enables the HDF5 plugin. The directory where the profile files are stored and which values
> are collected are configured in the acct_gather.conf file.
>
> <!-- -->
>
> **acct_gather_profile/influxdb**  
> This enables the influxdb plugin. The influxdb instance host, port, database, retention policy and
> which values are collected are configured in the acct_gather.conf file.

**AllowSpecResourcesUsage**  
If set to "YES", Slurm allows individual jobs to override node's configured CoreSpecCount value. For
a job to take advantage of this feature, a command line option of --core-spec must be specified. The
default value for this option is "YES" for Cray systems and "NO" for other system types.

<!-- -->

**AuthAltTypes**  
Comma-separated list of alternative authentication plugins that the slurmctld will permit for
communication. Acceptable values at present include *auth/jwt*.

**NOTE**: *auth/jwt* requires a jwt_hs256.key to be populated in the **StateSaveLocation** directory
for **slurmctld** only. The jwt_hs256.key should only be visible to the SlurmUser and root. It is
not suggested to place the jwt_hs256.key on any nodes but the controller running **slurmctld**.
*auth/jwt* can be activated by the presence of the *SLURM_JWT* environment variable. When activated,
it will override the default **AuthType**.

<!-- -->

**AuthAltParameters**  
Used to define alternative authentication plugins options. Multiple options may be comma separated.

> **disable_token_creation**  
> Disable "scontrol token" use by non-SlurmUser accounts.
>
> **max_token_lifespan**=\<seconds\>  
> Set max lifespan (in seconds) for any token generated for user accounts. (This limit does not
> apply to SlurmUser.)
>
> <!-- -->
>
> **jwks=**  
> Absolute path to JWKS file. Only RS256 keys are supported, although other key types may be listed
> in the file. If set, no HS256 key will be loaded by default (and token generation is disabled),
> although the jwt_key setting may be used to explicitly re-enable HS256 key use (and token
> generation).
>
> <!-- -->
>
> **jwt_key=**  
> Absolute path to JWT key file. Key must be HS256, and should only be accessible by SlurmUser. If
> not set, the default key file is jwt_hs256.key in *StateSaveLocation*.

**AuthInfo**  
Additional information to be used for authentication of communications between the Slurm daemons
(slurmctld and slurmd) and the Slurm clients. The interpretation of this option is specific to the
configured **AuthType**. Multiple options may be specified in a comma-delimited list. If not
specified, the default authentication information will be used.

> **cred_expire**  
> Default job step credential lifetime, in seconds (e.g. "cred_expire=1200"). It must be
> sufficiently long enough to load user environment, run prolog, deal with the slurmd getting paged
> out of memory, etc. This also controls how long a requeued job must wait before starting again.
> The default value is 120 seconds.
>
> <!-- -->
>
> **socket**  
> Path name to a MUNGE daemon socket to use (e.g. "socket=/var/run/munge/munge.socket.2"). The
> default value is "/var/run/munge/munge.socket.2". Used by *auth/munge* and *cred/munge*.
>
> <!-- -->
>
> **ttl**  
> Credential lifetime, in seconds (e.g. "ttl=300"). The default value is dependent upon the MUNGE
> installation, but is typically 300 seconds.
>
> <!-- -->
>
> **userclaimfield=**  
> Use an alternative claim field for the Slurm UserName **sun** field. This option is designed to
> allow compatibility with tokens generated outside of Slurm. (This field may also be known as a
> grant.)
>
> Default: (disabled)

**AuthType**  
The authentication method for communications between Slurm components. Acceptable values at present
include "auth/munge", which is the default. "auth/munge" indicates that MUNGE is to be used. (See
"https://dun.github.io/munge/" for more information). All Slurm daemons and commands must be
terminated prior to changing the value of **AuthType** and later restarted.

<!-- -->

**BackupAddr**  
Deprecated option, see **SlurmctldHost**.

<!-- -->

**BackupController**  
Deprecated option, see **SlurmctldHost**.

The backup controller recovers state information from the **StateSaveLocation** directory, which
must be readable and writable from both the primary and backup controllers. While not essential, it
is recommended that you specify a backup controller. See the **RELOCATING CONTROLLERS** section if
you change this.

<!-- -->

**BatchStartTimeout**  
The maximum time (in seconds) that a batch job is permitted for launching before being considered
missing and releasing the allocation. The default value is 10 (seconds). Larger values may be
required if more time is required to execute the **Prolog**, load user environment variables, or if
the slurmd daemon gets paged from memory.  
  
**Note**: The test for a job being successfully launched is only performed when the Slurm daemon on
the compute node registers state with the slurmctld daemon on the head node, which happens fairly
rarely. Therefore a job will not necessarily be terminated if its start time exceeds
**BatchStartTimeout**. This configuration parameter is also applied to launch tasks and avoid
aborting **srun** commands due to long running **Prolog** scripts.

<!-- -->

**BcastExclude**  
Comma-separated list of absolute directory paths to be excluded when autodetecting and broadcasting
executable shared object dependencies through **sbcast** or **srun --bcast**. The keyword "*none*"
can be used to indicate that no directory paths should be excluded. The default value is
"*/lib,/usr/lib,/lib64,/usr/lib64*". This option can be overridden by **sbcast --exclude** and
**srun --bcast-exclude**.

<!-- -->

**BcastParameters**  
Controls sbcast and srun --bcast behavior. Multiple options can be specified in a comma separated
list. Supported values include:

> **DestDir=**  
> Destination directory for file being broadcast to allocated compute nodes. Default value is
> current working directory, or --chdir for srun if set.
>
> <!-- -->
>
> **Compression=**  
> Specify default file compression library to be used. Supported values are "lz4" and "none". The
> default value with the sbcast --compress option is "lz4" and "none" otherwise. Some compression
> libraries may be unavailable on some systems.
>
> <!-- -->
>
> **send_libs**  
> If set, attempt to autodetect and broadcast the executable's shared object dependencies to
> allocated compute nodes. The files are placed in a directory alongside the executable. For
> **srun** only, the **LD_LIBRARY_PATH** is automatically updated to include this cache directory as
> well. This can be overridden with either **sbcast** or **srun** **--send-libs** option. By default
> this is disabled.

**BurstBufferType**  
The plugin used to manage burst buffers. Acceptable values at present are:

> **burst_buffer/datawarp**  
> Use Cray DataWarp API to provide burst buffer functionality.
>
> <!-- -->
>
> **burst_buffer/lua**  
> This plugin provides hooks to an API that is defined by a Lua script. This plugin was developed to
> provide system administrators with a way to do any task (not only file staging) at different
> points in a job’s life cycle.
>
> <!-- -->
>
> **burst_buffer/none**  
>
> <!-- -->
>
> **CliFilterPlugins**  
> A comma-delimited list of command line interface option filter/modification plugins. The specified
> plugins will be executed in the order listed. No cli_filter plugins are used by default.
> Acceptable values at present are:
>
> > **cli_filter/lua**  
> > This plugin allows you to write your own implementation of a cli_filter using lua.
> >
> > <!-- -->
> >
> > **cli_filter/syslog**  
> > This plugin enables logging of job submission activities performed. All the salloc/sbatch/srun
> > options are logged to syslog together with environment variables in JSON format. If the plugin
> > is not the last one in the list it may log values different than what was actually sent to
> > slurmctld.
> >
> > <!-- -->
> >
> > **cli_filter/user_defaults**  
> > This plugin looks for the file \$HOME/.slurm/defaults and reads every line of it as a
> > *key*=*value* pair, where *key* is any of the job submission options available to
> > salloc/sbatch/srun and *value* is a default value defined by the user. For instance:
> >
> > <!-- -->
> >
> >     time=1:30
> >     mem=2048
> >
> > The above will result in a user defined default for each of their jobs of "-t 1:30" and
> > "--mem=2048".
>
> **ClusterName**  
> The name by which this Slurm managed cluster is known in the accounting database. This is needed
> distinguish accounting records when multiple clusters report to the same database. Because of
> limitations in some databases, any upper case letters in the name will be silently mapped to lower
> case. In order to avoid confusion, it is recommended that the name be lower case. The cluster name
> must be 40 characters or less in order to comply with the limit on the maximum length for table
> names in MySQL/MariaDB.
>
> <!-- -->
>
> **CommunicationParameters**  
> Comma-separated options identifying communication options.
>
> > **block_null_hash**  
> > Require all Slurm authentication tokens to include a newer (20.11.9 and 21.08.8) payload that
> > provides an additional layer of security against credential replay attacks. This option should
> > only be enabled once all Slurm daemons have been upgraded to 20.11.9/21.08.8 or newer, and all
> > jobs that were started before the upgrade have been completed.
> >
> > **CheckGhalQuiesce**  
> > Used specifically on a Cray using an Aries Ghal interconnect. This will check to see if the
> > system is quiescing when sending a message, and if so, we wait until it is done before sending.
> >
> > <!-- -->
> >
> > **DisableIPv4**  
> > Disable IPv4 only operation for all slurm daemons (except slurmdbd). This should also be set in
> > your **slurmdbd.conf** file.
> >
> > <!-- -->
> >
> > **EnableIPv6**  
> > Enable using IPv6 addresses for all slurm daemons (except slurmdbd). When using both IPv4 and
> > IPv6, address family preferences will be based on your /etc/gai.conf file. This should also be
> > set in your **slurmdbd.conf** file.
> >
> > <!-- -->
> >
> > **getnameinfo_cache_timeout**  
> > When munge is used as AuthType slurmctld makes use of getnameinfo to obtain the hostname from IP
> > address stored in munge credential. This parameter controls the number of seconds slurmctld
> > should keep the IP to hostname resolution. When set to 0 cache is disabled. The default value is
> > 60.
> >
> > <!-- -->
> >
> > **keepaliveinterval=#**  
> > Specifies the interval between keepalive probes on the socket communications between srun and
> > its slurmstepd process.
> >
> > <!-- -->
> >
> > **keepaliveprobes=#**  
> > Specifies the number of keepalive probes sent on the socket communications between srun command
> > and its slurmstepd process before the connection is considered broken.
> >
> > <!-- -->
> >
> > **keepalivetime=#**  
> > Specifies how long sockets communications used between the srun command and its slurmstepd
> > process are kept alive after disconnect. Longer values can be used to improve reliability of
> > communications in the event of network failures.
> >
> > <!-- -->
> >
> > **NoAddrCache**  
> > By default, Slurm will cache a node's network address after successfully establishing the node's
> > network address. This option disables the cache and Slurm will look up the node's network
> > address each time a connection is made. This is useful, for example, in a cloud environment
> > where the node addresses come and go out of DNS.
> >
> > <!-- -->
> >
> > **NoCtldInAddrAny**  
> > Used to directly bind to the address of what the node resolves to running the slurmctld instead
> > of binding messages to any address on the node, which is the default.
> >
> > <!-- -->
> >
> > **NoInAddrAny**  
> > Used to directly bind to the address of what the node resolves to instead of binding messages to
> > any address on the node which is the default. This option is for all daemons/clients except for
> > the slurmctld.
>
> **CompleteWait**  
> The time to wait, in seconds, when any job is in the COMPLETING state before any additional jobs
> are scheduled. This is to attempt to keep jobs on nodes that were recently in use, with the goal
> of preventing fragmentation. If set to zero, pending jobs will be started as soon as possible.
> Since a COMPLETING job's resources are released for use by other jobs as soon as the **Epilog**
> completes on each individual node, this can result in very fragmented resource allocations. To
> provide jobs with the minimum response time, a value of zero is recommended (no waiting). To
> minimize fragmentation of resources, a value equal to **KillWait** plus two is recommended. In
> that case, setting **KillWait** to a small value may be beneficial. The default value of
> **CompleteWait** is zero seconds. The value may not exceed 65533.
>
> **NOTE**: Setting **reduce_completing_frag** affects the behavior of **CompleteWait**.
>
> <!-- -->
>
> **ControlAddr**  
> Deprecated option, see **SlurmctldHost**.
>
> <!-- -->
>
> **ControlMachine**  
> Deprecated option, see **SlurmctldHost**.
>
> <!-- -->
>
> **CoreSpecPlugin**  
> Identifies the plugins to be used for enforcement of core specialization. A restart of the slurmd
> daemons is required for changes to this parameter to take effect. Acceptable values at present
> include:
>
> > **core_spec/cray_aries**  
> > used only for Cray systems
> >
> > <!-- -->
> >
> > **core_spec/none**  
> > used for all other system types
>
> **CpuFreqDef**  
> Default CPU frequency value or frequency governor to use when running a job step if it has not
> been explicitly set with the --cpu-freq option. Acceptable values at present include a numeric
> value (frequency in kilohertz) or one of the following governors:
>
> > **Conservative**  
> > attempts to use the Conservative CPU governor
> >
> > <!-- -->
> >
> > **OnDemand**  
> > attempts to use the OnDemand CPU governor
> >
> > <!-- -->
> >
> > **Performance**  
> > attempts to use the Performance CPU governor
> >
> > <!-- -->
> >
> > **PowerSave**  
> > attempts to use the PowerSave CPU governor
>
> There is no default value. If unset, no attempt to set the governor is made if the --cpu-freq
> option has not been set.
>
> **CpuFreqGovernors**  
> List of CPU frequency governors allowed to be set with the salloc, sbatch, or srun option
> --cpu-freq. Acceptable values at present include:
>
> > **Conservative**  
> > attempts to use the Conservative CPU governor
> >
> > <!-- -->
> >
> > **OnDemand**  
> > attempts to use the OnDemand CPU governor (a default value)
> >
> > <!-- -->
> >
> > **Performance**  
> > attempts to use the Performance CPU governor (a default value)
> >
> > <!-- -->
> >
> > **PowerSave**  
> > attempts to use the PowerSave CPU governor
> >
> > <!-- -->
> >
> > **SchedUtil**  
> > attempts to use the SchedUtil CPU governor
> >
> > <!-- -->
> >
> > **UserSpace**  
> > attempts to use the UserSpace CPU governor (a default value)
>
> The default is OnDemand, Performance and UserSpace.
>
> **CredType**  
> The cryptographic signature tool to be used in the creation of job step credentials. A restart of
> slurmctld is required for changes to this parameter to take effect. The default (and recommended)
> value is "cred/munge".
>
> <!-- -->
>
> **DebugFlags**  
> Defines specific subsystems which should provide more detailed event logging. Multiple subsystems
> can be specified with comma separators. Most DebugFlags will result in verbose-level logging for
> the identified subsystems, and could impact performance.
>
> **NOTE**: You can also set debug flags by having the **SLURM_DEBUG_FLAGS** environment variable
> defined with the desired flags when the process (client command, daemon, etc.) is started. The
> environment variable takes precedence over the setting in the slurm.conf.
>
> Valid subsystems available include:
>
> > **Accrue**  
> > Accrue counters accounting details
> >
> > <!-- -->
> >
> > **Agent**  
> > RPC agents (outgoing RPCs from Slurm daemons)
> >
> > <!-- -->
> >
> > **Backfill**  
> > Backfill scheduler details
> >
> > <!-- -->
> >
> > **BackfillMap**  
> > Backfill scheduler to log a very verbose map of reserved resources through time. Combine with
> > **Backfill** for a verbose and complete view of the backfill scheduler's work.
> >
> > <!-- -->
> >
> > **BurstBuffer**  
> > Burst Buffer plugin
> >
> > <!-- -->
> >
> > **Cgroup**  
> > Cgroup details
> >
> > <!-- -->
> >
> > **CPU_Bind**  
> > CPU binding details for jobs and steps
> >
> > <!-- -->
> >
> > **CpuFrequency**  
> > Cpu frequency details for jobs and steps using the --cpu-freq option.
> >
> > <!-- -->
> >
> > **Data**  
> > Generic data structure details.
> >
> > <!-- -->
> >
> > **Dependency**  
> > Job dependency debug info
> >
> > <!-- -->
> >
> > **Elasticsearch**  
> > Elasticsearch debug info (deprecated). Alias of **JobComp**.
> >
> > <!-- -->
> >
> > **Energy**  
> > AcctGatherEnergy debug info
> >
> > <!-- -->
> >
> > **ExtSensors**  
> > External Sensors debug info
> >
> > <!-- -->
> >
> > **Federation**  
> > Federation scheduling debug info
> >
> > <!-- -->
> >
> > **FrontEnd**  
> > Front end node details
> >
> > <!-- -->
> >
> > **Gres**  
> > Generic resource details
> >
> > <!-- -->
> >
> > **Hetjob**  
> > Heterogeneous job details
> >
> > <!-- -->
> >
> > **Gang**  
> > Gang scheduling details
> >
> > <!-- -->
> >
> > **JobAccountGather**  
> > Common job account gathering details (not plugin specific).
> >
> > <!-- -->
> >
> > **JobComp**  
> > Job Completion plugin details
> >
> > <!-- -->
> >
> > **JobContainer**  
> > Job container plugin details
> >
> > <!-- -->
> >
> > **License**  
> > License management details
> >
> > <!-- -->
> >
> > **Network**  
> > Network details. **Warning**: activating this flag may cause logging of passwords, tokens or
> > other authentication credentials.
> >
> > <!-- -->
> >
> > **NetworkRaw**  
> > Dump raw hex values of key Network communications. **Warning**: This flag will cause very
> > verbose logs and may cause logging of passwords, tokens or other authentication credentials.
> >
> > <!-- -->
> >
> > **NodeFeatures**  
> > Node Features plugin debug info
> >
> > <!-- -->
> >
> > **NO_CONF_HASH**  
> > Do not log when the slurm.conf files differ between Slurm daemons
> >
> > <!-- -->
> >
> > **Power**  
> > Power management plugin and power save (suspend/resume programs) details
> >
> > <!-- -->
> >
> > **Priority**  
> > Job prioritization
> >
> > <!-- -->
> >
> > **Profile**  
> > AcctGatherProfile plugins details
> >
> > <!-- -->
> >
> > **Protocol**  
> > Communication protocol details
> >
> > <!-- -->
> >
> > **Reservation**  
> > Advanced reservations
> >
> > <!-- -->
> >
> > **Route**  
> > Message forwarding debug info
> >
> > <!-- -->
> >
> > **Script**  
> > Debug info regarding the process that runs slurmctld scripts such as PrologSlurmctld and
> > EpilogSlurmctld
> >
> > <!-- -->
> >
> > **SelectType**  
> > Resource selection plugin
> >
> > <!-- -->
> >
> > **Steps**  
> > Slurmctld resource allocation for job steps
> >
> > <!-- -->
> >
> > **Switch**  
> > Switch plugin
> >
> > <!-- -->
> >
> > **TimeCray**  
> > Timing of Cray APIs
> >
> > <!-- -->
> >
> > **TraceJobs**  
> > Trace jobs in slurmctld. It will print detailed job information including state, job ids and
> > allocated nodes counter.
> >
> > <!-- -->
> >
> > **Triggers**  
> > Slurmctld triggers
> >
> > <!-- -->
> >
> > **WorkQueue**  
> > Work Queue details
>
> **DefCpuPerGPU**  
> Default count of CPUs allocated per allocated GPU. This value is used only if the job didn't
> specify --cpus-per-task and --cpus-per-gpu.
>
> <!-- -->
>
> **DefMemPerCPU**  
> Default real memory size available per usable allocated CPU in megabytes. Used to avoid
> over-subscribing memory and causing paging. **DefMemPerCPU** would generally be used if individual
> processors are allocated to jobs (**SelectType=select/cons_res** or
> **SelectType=select/cons_tres**). The default value is 0 (unlimited). Also see **DefMemPerGPU**,
> **DefMemPerNode** and **MaxMemPerCPU**. **DefMemPerCPU**, **DefMemPerGPU** and **DefMemPerNode**
> are mutually exclusive.
>
> **NOTE**: This applies to **usable** allocated CPUs in a job allocation. This is important when
> more than one thread per core is configured. If a job requests --threads-per-core with fewer
> threads on a core than exist on the core (or --hint=nomultithread which implies
> --threads-per-core=1), the job will be unable to use those extra threads on the core and those
> threads will not be included in the memory per CPU calculation. But if the job has access to all
> threads on the core, those threads will be included in the memory per CPU calculation even if the
> job did not explicitly request those threads.
>
> In the following examples, each core has two threads.
>
> In this first example, two tasks can run on separate hyperthreads in the same core because
> --threads-per-core is not used. The third task uses both threads of the second core. The allocated
> memory per cpu includes all threads:
>
>     $ salloc -n3 --mem-per-cpu=100
>     salloc: Granted job allocation 17199
>     $ sacct -j $SLURM_JOB_ID -X -o jobid%7,reqtres%35,alloctres%35
>       JobID                             ReqTRES                           AllocTRES
>     ------- ----------------------------------- -----------------------------------
>       17199     billing=3,cpu=3,mem=300M,node=1     billing=4,cpu=4,mem=400M,node=1
>
> In this second example, because of --threads-per-core=1, each task is allocated an entire core but
> is only able to use one thread per core. Allocated CPUs includes all threads on each core.
> However, allocated memory per cpu includes only the usable thread in each core.
>
>     $ salloc -n3 --mem-per-cpu=100 --threads-per-core=1
>     salloc: Granted job allocation 17200
>     $ sacct -j $SLURM_JOB_ID -X -o jobid%7,reqtres%35,alloctres%35
>       JobID                             ReqTRES                           AllocTRES
>     ------- ----------------------------------- -----------------------------------
>       17200     billing=3,cpu=3,mem=300M,node=1     billing=6,cpu=6,mem=300M,node=1
>
> **DefMemPerGPU**  
> Default real memory size available per allocated GPU in megabytes. The default value is 0
> (unlimited). Also see **DefMemPerCPU** and **DefMemPerNode**. **DefMemPerCPU**, **DefMemPerGPU**
> and **DefMemPerNode** are mutually exclusive.
>
> <!-- -->
>
> **DefMemPerNode**  
> Default real memory size available per allocated node in megabytes. Used to avoid over-subscribing
> memory and causing paging. **DefMemPerNode** would generally be used if whole nodes are allocated
> to jobs (**SelectType=select/linear**) and resources are over-subscribed (**OverSubscribe=yes** or
> **OverSubscribe=force**). The default value is 0 (unlimited). Also see **DefMemPerCPU**,
> **DefMemPerGPU** and **MaxMemPerCPU**. **DefMemPerCPU**, **DefMemPerGPU** and **DefMemPerNode**
> are mutually exclusive.
>
> <!-- -->
>
> **DependencyParameters**  
> Multiple options may be comma separated.
>
> > **disable_remote_singleton**  
> > By default, when a federated job has a singleton dependency, each cluster in the federation must
> > clear the singleton dependency before the job's singleton dependency is considered satisfied.
> > Enabling this option means that only the origin cluster must clear the singleton dependency.
> > This option must be set in every cluster in the federation.
> >
> > <!-- -->
> >
> > **kill_invalid_depend**  
> > If a job has an invalid dependency and it can never run terminate it and set its state to be
> > JOB_CANCELLED. By default the job stays pending with reason DependencyNeverSatisfied.
> >
> > <!-- -->
> >
> > **max_depend_depth=#**  
> > Maximum number of jobs to test for a circular job dependency. Stop testing after this number of
> > job dependencies have been tested. The default value is 10 jobs.
>
> **DisableRootJobs**  
> If set to "YES" then user root will be prevented from running any jobs. The default value is "NO",
> meaning user root will be able to execute jobs. **DisableRootJobs** may also be set by partition.
>
> <!-- -->
>
> **EioTimeout**  
> The number of seconds srun waits for slurmstepd to close the TCP/IP connection used to relay data
> between the user application and srun when the user application terminates. The default value is
> 60 seconds. May not exceed 65533.
>
> <!-- -->
>
> **EnforcePartLimits**  
> If set to "ALL" then jobs which exceed a partition's size and/or time limits will be rejected at
> submission time. If job is submitted to multiple partitions, the job must satisfy the limits on
> all the requested partitions. If set to "NO" then the job will be accepted and remain queued until
> the partition limits are altered(Time and Node Limits). If set to "ANY" a job must satisfy any of
> the requested partitions to be submitted. The default value is "NO". **NOTE**: If set, then a
> job's QOS can not be used to exceed partition limits. **NOTE**: The partition limits being
> considered are its configured MaxMemPerCPU, MaxMemPerNode, MinNodes, MaxNodes, MaxTime,
> AllocNodes, AllowAccounts, AllowGroups, AllowQOS, and QOS usage threshold.
>
> <!-- -->
>
> **Epilog**  
> Fully qualified pathname of a script to execute as user root on every node when a user's job
> completes (e.g. "/usr/local/slurm/epilog"). A glob pattern (See **glob** (7)) may also be used to
> run more than one epilog script (e.g. "/etc/slurm/epilog.d/\*"). When more than one epilog script
> is configured, they are executed in reverse order. The Epilog script or scripts may be used to
> purge files, disable user login, etc. By default there is no epilog. See **Prolog and Epilog
> Scripts** for more information.
>
> <!-- -->
>
> **EpilogMsgTime**  
> The number of microseconds that the slurmctld daemon requires to process an epilog completion
> message from the slurmd daemons. This parameter can be used to prevent a burst of epilog
> completion messages from being sent at the same time which should help prevent lost messages and
> improve throughput for large jobs. The default value is 2000 microseconds. For a 1000 node job,
> this spreads the epilog completion messages out over two seconds.
>
> <!-- -->
>
> **EpilogSlurmctld**  
> Fully qualified pathname of a program for the slurmctld to execute upon termination of a job
> allocation (e.g. "/usr/local/slurm/epilog_controller"). The program executes as SlurmUser, which
> gives it permission to drain nodes and requeue the job if a failure occurs (See scontrol(1)).
> Exactly what the program does and how it accomplishes this is completely at the discretion of the
> system administrator. Information about the job being initiated, its allocated nodes, etc. are
> passed to the program using environment variables. See **Prolog and Epilog Scripts** for more
> information.
>
> <!-- -->
>
> **ExtSensorsFreq**  
> The external sensors plugin sampling interval. If **ExtSensorsType=ext_sensors/none**, this
> parameter is ignored. For all other values of **ExtSensorsType**, this parameter is the number of
> seconds between external sensors samples for hardware components (nodes, switches, etc.) The
> default value is zero. This value disables external sensors sampling. Note: This parameter does
> not affect external sensors data collection for jobs/steps.
>
> <!-- -->
>
> **ExtSensorsType**  
> Identifies the plugin to be used for external sensors data collection. Slurmctld calls this plugin
> to collect external sensors data for jobs/steps and hardware components. In case of node sharing
> between jobs the reported values per job/step (through sstat or sacct) may not be accurate. See
> also "man ext_sensors.conf".
>
> Configurable values at present are:
>
> > **ext_sensors/none**  
> > No external sensors data is collected.
> >
> > <!-- -->
> >
> > **ext_sensors/rrd**  
> > External sensors data is collected from the RRD database.
>
> **FairShareDampeningFactor**  
> Dampen the effect of exceeding a user or group's fair share of allocated resources. Higher values
> will provides greater ability to differentiate between exceeding the fair share at high levels
> (e.g. a value of 1 results in almost no difference between overconsumption by a factor of 10 and
> 100, while a value of 5 will result in a significant difference in priority). The default value is
> 1.
>
> <!-- -->
>
> **FederationParameters**  
> Used to define federation options. Multiple options may be comma separated.
>
> > **fed_display**  
> > If set, then the client status commands (e.g. squeue, sinfo, sprio, etc.) will display
> > information in a federated view by default. This option is functionally equivalent to using the
> > --federation options on each command. Use the client's --local option to override the federated
> > view and get a local view of the given cluster.
>
> **FirstJobId**  
> The job id to be used for the first job submitted to Slurm. Job id values generated will
> incremented by 1 for each subsequent job. Value must be larger than 0. The default value is 1.
> Also see **MaxJobId**
>
> <!-- -->
>
> **GetEnvTimeout**  
> Controls how long the job should wait (in seconds) to load the user's environment before
> attempting to load it from a cache file. Applies when the salloc or sbatch *--get-user-env* option
> is used. If set to 0 then always load the user's environment from the cache file. The default
> value is 2 seconds.
>
> <!-- -->
>
> **GresTypes**  
> A comma-delimited list of generic resources to be managed (e.g. *GresTypes=gpu,mps*). These
> resources may have an associated GRES plugin of the same name providing additional functionality.
> No generic resources are managed by default. Ensure this parameter is consistent across all nodes
> in the cluster for proper operation. A restart of slurmctld and the slurmd daemons is required for
> this to take effect.
>
> <!-- -->
>
> **GroupUpdateForce**  
> If set to a non-zero value, then information about which users are members of groups allowed to
> use a partition will be updated periodically, even when there have been no changes to the
> /etc/group file. If set to zero, group member information will be updated only after the
> /etc/group file is updated. The default value is 1. Also see the **GroupUpdateTime** parameter.
>
> <!-- -->
>
> **GroupUpdateTime**  
> Controls how frequently information about which users are members of groups allowed to use a
> partition will be updated, and how long user group membership lists will be cached. The time
> interval is given in seconds with a default value of 600 seconds. A value of zero will prevent
> periodic updating of group membership information. Also see the **GroupUpdateForce** parameter.
>
> <!-- -->
>
> **GpuFreqDef**=\[\<*type*\]=*value*\>\[,\<*type*=*value*\>\]  
> Default GPU frequency to use when running a job step if it has not been explicitly set using the
> --gpu-freq option. This option can be used to independently configure the GPU and its memory
> frequencies. There is no default value. If unset, no attempt to change the GPU frequency is made
> if the --gpu-freq option has not been set. After the job is completed, the frequencies of all
> affected GPUs will be reset to the highest possible values. In some cases, system power caps may
> override the requested values. The field *type* can be "memory". If *type* is not specified, the
> GPU frequency is implied. The *value* field can either be "low", "medium", "high", "highm1" or a
> numeric value in megahertz (MHz). If the specified numeric value is not possible, a value as close
> as possible will be used. See below for definition of the values. Examples of use include
> "GpuFreqDef=medium,memory=high and "GpuFreqDef=450".
>
> Supported *value* definitions:
>
> > **low**  
> > the lowest available frequency.
> >
> > <!-- -->
> >
> > **medium**  
> > attempts to set a frequency in the middle of the available range.
> >
> > <!-- -->
> >
> > **high**  
> > the highest available frequency.
> >
> > <!-- -->
> >
> > **highm1**  
> > (high minus one) will select the next highest available frequency.
>
> **HealthCheckInterval**  
> The interval in seconds between executions of **HealthCheckProgram**. The default value is zero,
> which disables execution.
>
> <!-- -->
>
> **HealthCheckNodeState**  
> Identify what node states should execute the **HealthCheckProgram**. Multiple state values may be
> specified with a comma separator. The default value is ANY to execute on nodes in any state.
>
> > **ALLOC**  
> > Run on nodes in the ALLOC state (all CPUs allocated).
> >
> > <!-- -->
> >
> > **ANY**  
> > Run on nodes in any state.
> >
> > <!-- -->
> >
> > **CYCLE**  
> > Rather than running the health check program on all nodes at the same time, cycle through
> > running on all compute nodes through the course of the **HealthCheckInterval**. May be combined
> > with the various node state options.
> >
> > <!-- -->
> >
> > **IDLE**  
> > Run on nodes in the IDLE state.
> >
> > <!-- -->
> >
> > **NONDRAINED_IDLE**  
> > Run on nodes that are in the IDLE state and not DRAINED.
> >
> > <!-- -->
> >
> > **MIXED**  
> > Run on nodes in the MIXED state (some CPUs idle and other CPUs allocated).
>
> **HealthCheckProgram**  
> Fully qualified pathname of a script to execute as user root periodically on all compute nodes
> that are **not** in the NOT_RESPONDING state. This program may be used to verify the node is fully
> operational and DRAIN the node or send email if a problem is detected. Any action to be taken must
> be explicitly performed by the program (e.g. execute "scontrol update NodeName=foo State=drain
> Reason=tmp_file_system_full" to drain a node). The execution interval is controlled using the
> **HealthCheckInterval** parameter. Note that the **HealthCheckProgram** will be executed at the
> same time on all nodes to minimize its impact upon parallel programs. This program will be killed
> if it does not terminate normally within 60 seconds. This program will also be executed when the
> slurmd daemon is first started and before it registers with the slurmctld daemon. By default, no
> program will be executed.
>
> <!-- -->
>
> **InactiveLimit**  
> The interval, in seconds, after which a non-responsive job allocation command (e.g. **srun** or
> **salloc**) will result in the job being terminated. If the node on which the command is executed
> fails or the command abnormally terminates, this will terminate its job allocation. This option
> has no effect upon batch jobs. When setting a value, take into consideration that a debugger using
> **srun** to launch an application may leave the **srun** command in a stopped state for extended
> periods of time. This limit is ignored for jobs running in partitions with the **RootOnly** flag
> set (the scheduler running as root will be responsible for the job). The default value is
> unlimited (zero) and may not exceed 65533 seconds.
>
> <!-- -->
>
> **InteractiveStepOptions**  
> When LaunchParameters=use_interactive_step is enabled, launching salloc will automatically start
> an srun process with InteractiveStepOptions to launch a terminal on a node in the job allocation.
> The default value is "--interactive --preserve-env --pty \$SHELL". The "--interactive" option is
> intentionally not documented in the srun man page. It is meant only to be used in
> **InteractiveStepOptions** in order to create an "interactive step" that will not consume
> resources so that other steps may run in parallel with the interactive step.
>
> <!-- -->
>
> **JobAcctGatherType**  
> The JobAcctGather plugin collects memory, cpu, io, interconnect, energy and gpu usage information
> at the task level, depending on which plugins are configured in Slurm. This parameter will control
> how some of these metrics will be collected.
>
> Configurable values at present are:
>
> > **jobacct_gather/cgroup** (recommended)  
> > Collect cpu and memory statistics by reading the task's cgroup directory interfaces (e.g.
> > memory.stat, cpu.stat) by issuing a call to the configured CgroupPlugin (see "man cgroup.conf").
> > This mechanism ignores JobAcctGatherParams=UsePSS or NoShared since these are used only when
> > reading memory usage from the proc filesystem.
> >
> > <!-- -->
> >
> > **jobacct_gather/linux**  
> > Collect cpu and memory statistics by reading procfs. The plugin will take all the pids of the
> > task and for each of them will read /proc/\<pid\>/stats. If UsePSS is set it will also read
> > /proc/\<pid\>/smaps, and if NoShare is set it will also read /proc/\<pid\>/statm (see
> > **JobAcctGatherParams** for more information).
> >
> > This plugin carries a performance penalty on jobs with a large number of spawned processes since
> > it needs to iterate over all the task pids and aggregate the stats into one single metric for
> > the ppid, and then these values need to be aggregated to the task stats.
> >
> > <!-- -->
> >
> > **jobacct_gather/none**  
> > This is the default value. No accounting data is collected. **sstat** will not work.
>
> **NOTE**: Changing the plugin type when jobs are running in the cluster is possible. The already
> running steps will keep using the previous plugin mechanism, while new steps will use the new
> mechanism.
>
> **JobAcctGatherFrequency**  
> The job accounting and profiling sampling intervals. The supported format is follows:
>
> > **JobAcctGatherFrequency=***\<datatype\>***=***\<interval\>*  
> > where *\<datatype\>*=*\<interval\>* specifies the task sampling interval for the jobacct_gather
> > plugin or a sampling interval for a profiling type by the acct_gather_profile plugin. Multiple,
> > comma-separated *\<datatype\>*=*\<interval\>* intervals may be specified. Supported datatypes
> > are as follows:
> >
> > > **task=***\<interval\>*  
> > > where *\<interval\>* is the task sampling interval in seconds for the jobacct_gather plugins
> > > and for task profiling by the acct_gather_profile plugin.
> > >
> > > <!-- -->
> > >
> > > **energy=***\<interval\>*  
> > > where *\<interval\>* is the sampling interval in seconds for energy profiling using the
> > > acct_gather_energy plugin
> > >
> > > <!-- -->
> > >
> > > **network=***\<interval\>*  
> > > where *\<interval\>* is the sampling interval in seconds for infiniband profiling using the
> > > acct_gather_interconnect plugin.
> > >
> > > <!-- -->
> > >
> > > **filesystem=***\<interval\>*  
> > > where *\<interval\>* is the sampling interval in seconds for filesystem profiling using the
> > > acct_gather_filesystem plugin.
> >
> > The default value for task sampling interval is 30 seconds. The default value for all other
> > intervals is 0. An interval of 0 disables sampling of the specified type. If the task sampling
> > interval is 0, accounting information is collected only at job termination, which reduces Slurm
> > interference with the job, but also means that the statistics about a job don't reflect the
> > average or maximum of several samples throughout the life of the job, but just show the
> > information collected in the single sample.  
> >   
> > Smaller (non-zero) values have a greater impact upon job performance, but a value of 30 seconds
> > is not likely to be noticeable for applications having less than 10,000 tasks.  
> >   
> > Users can independently override each interval on a per job basis using the **--acctg-freq**
> > option when submitting the job.
>
> **JobAcctGatherParams**  
> Arbitrary parameters for the job account gather plugin. Acceptable values at present include:
>
> > **NoShared**  
> > Exclude shared memory from RSS. This option cannot be used with UsePSS.
> >
> > <!-- -->
> >
> > **UsePss**  
> > Use PSS value instead of RSS to calculate real usage of memory. The PSS value will be saved as
> > RSS. This option cannot be used with NoShared.
> >
> > <!-- -->
> >
> > **OverMemoryKill**  
> > Kill processes that are being detected to use more memory than requested by steps every time
> > accounting information is gathered by the JobAcctGather plugin. This parameter should be used
> > with caution because a job exceeding its memory allocation may affect other processes and/or
> > machine health.
> >
> > **NOTE**: If available, it is recommended to limit memory by enabling task/cgroup as a
> > TaskPlugin and making use of ConstrainRAMSpace=yes in the cgroup.conf instead of using this
> > JobAcctGather mechanism for memory enforcement. Using JobAcctGather is polling based and there
> > is a delay before a job is killed, which could lead to system Out of Memory events.
> >
> > **NOTE**: When using **OverMemoryKill**, if the combined memory used by all the processes in a
> > step exceeds the memory limit, the entire step will be killed/cancelled by the JobAcctGather
> > plugin. This differs from the behavior when using **ConstrainRAMSpace**, where processes in the
> > step will be killed, but the step will be left active, possibly with other processes left
> > running.
> >
> > <!-- -->
> >
> > **DisableGPUAcct**  
> > Do not do accounting of GPU usage and skip any gpu driver library call. This parameter can help
> > to improve performance if the GPU driver response is slow.
>
> **JobCompHost**  
> The name of the machine hosting the job completion database. Only used for database type storage
> plugins, ignored otherwise.
>
> <!-- -->
>
> **JobCompLoc**  
> This option sets a string which has different meanings depending on **JobCompType**:
>
> > If **jobcomp/elasticsearch**:  
> > Instructs this plugin to send the finished job records information to the Elasticsearch server
> > URL endpoint (including the port number and the target index) configured in this option. This
> > string should typically take the form of *\<host\>:\<port\>/\<target\>/\_doc*.
> >
> > **NOTE**: The default value for this plugin is */var/log/slurm_jobcomp.log*.
> >
> > **NOTE**: Refer to \<https://slurm.schedmd.com/elasticsearch.html\> for more information.
> >
> > If **jobcomp/filetxt**:  
> > Instructs this plugin to send the finished job records information to a file configured in this
> > option. This string should represent an absolute path to a file.
> >
> > **NOTE**: The default value for this plugin is */var/log/slurm_jobcomp.log*.
> >
> > <!-- -->
> >
> > If **jobcomp/kafka**:  
> > When this plugin is configured, finished job records information is sent to a Kafka server. The
> > plugin makes use of **librdkafka**. This string represents an absolute path to a file containing
> > 'key=value' pairs configuring the library behavior. For the plugin to work properly, this file
> > needs to exist and least the *bootstrap.servers* **librdkafka** property needs to be configured
> > in it.
> >
> > **NOTE**: For a full list of **librdkafka** properties, please refer to the library
> > documentation. You can also view the jobcomp_kafka page for more information:
> > \<https://slurm.schedmd.com/jobcomp_kafka.html\>
> >
> > **NOTE**: The target Kafka topic and other plugin parameters can be configured via
> > **JobCompParams**.
> >
> > **NOTE**: There is no default value for JobCompLoc when this plugin is configured, and thus it
> > needs to be explicitly set.
> >
> > **NOTE**: The **librdkafka** parameters configured in the file referenced by this option take
> > effect upon slurmctld restart.
> >
> > <!-- -->
> >
> > If **jobcomp/lua**:  
> > This option is ignored in this plugin. The finished job record is processed by a hardcoded
> > *jobcomp.lua* script expected to be located in the same location of slurm.conf.
> >
> > **NOTE**: There is no default value for this option when this plugin is enabled.
> >
> > <!-- -->
> >
> > If **jobcomp/mysql**:  
> > Instructs this plugin to send the finished job records information to a database name configured
> > in this option. This string should represent a database name.
> >
> > **NOTE**: The default value for this plugin is *slurm_jobcomp_db*.
> >
> > <!-- -->
> >
> > If **jobcomp/script**:  
> > The finished job record information is made available via environment variables and processed by
> > a script with name configured by this option. This string should represent a path to a script.
> >
> > **NOTE**: There's no default JobCompLoc value if this plugin is configured, since JobCompLoc
> > needs to be explicitly configured. Otherwise, the plugin will fail to initialize.
>
> **JobCompParams**  
> Pass arbitrary text string to job completion plugin. Also see **JobCompType**.
>
> Optional comma-separated list for **jobcomp/kafka**:  
> > **flush_timeout**=\<milliseconds\>  
> > Maximum time (in milliseconds) to wait for all outstanding produce requests, et.al, to be
> > completed. This is passed as a timeout argument to the **librdkafka** flush API function, called
> > on plugin termination. This is done prior to destroying the producer instance to make sure all
> > queued and in-flight produce requests are completed before terminating. For non-blocking calls,
> > set to 0. To wait indefinitely for an event, set to -1 (not recommended, since this is called on
> > plugin fini and could block slurmctld graceful termination). Accepted values are
> > \[-1,2147483647\]. Defaults to 500 (milliseconds).
> >
> > <!-- -->
> >
> > **poll_interval**=\<seconds\>  
> > Seconds between calls to **librdkafka** API poll function, which polls the provided Kafka handle
> > for events. The plugin spawns a separate thread to perform this call at the configured interval.
> > Accepted values are \[0,4294967295\]. Defaults to 2 (seconds).
> >
> > <!-- -->
> >
> > **requeue_on_msg_timeout**  
> > Instruct the delivery report callback to requeue messages that failed delivery because their
> > time waiting for successful delivery reached the **librdkafka** property **message.timeout.ms**.
> > Defaults to not set (don't requeue and thus discard these messages).
> >
> > <!-- -->
> >
> > **topic**=\<string\>  
> > Target Kafka topic to send messages to. Defaults to **ClusterName**.
>
> <!-- -->
>
> **JobCompPass**  
> The password used to gain access to the database to store the job completion data. Only used for
> database type storage plugins, ignored otherwise.
>
> <!-- -->
>
> **JobCompPort**  
> The listening port of the job completion database server. Only used for database type storage
> plugins, ignored otherwise.
>
> <!-- -->
>
> **JobCompType**  
> The job completion logging mechanism type. Acceptable values at present include:
>
> > **jobcomp/none**  
> > Upon job completion, a record of the job is purged from the system. If using the accounting
> > infrastructure this plugin may not be of interest since some of the information is redundant.
> >
> > <!-- -->
> >
> > **jobcomp/elasticsearch**  
> > Upon job completion, a record of the job should be written to an Elasticsearch server, specified
> > by the **JobCompLoc** parameter.  
> > **NOTE**: More information is available at the Slurm web site (
> > https://slurm.schedmd.com/elasticsearch.html ).
> >
> > <!-- -->
> >
> > **jobcomp/filetxt**  
> > Upon job completion, a record of the job should be written to a text file, specified by the
> > **JobCompLoc** parameter.
> >
> > <!-- -->
> >
> > **jobcomp/kafka**  
> > Upon job completion, a record of the job should be sent to a Kafka server, specified by the file
> > path referenced in **JobCompLoc** and/or using other **JobCompParams**.
> >
> > <!-- -->
> >
> > **jobcomp/lua**  
> > Upon job completion, a record of the job should be processed by the *jobcomp.lua* script,
> > located in the default script directory (typically the subdirectory *etc* of the installation
> > directory.
> >
> > <!-- -->
> >
> > **jobcomp/mysql**  
> > Upon job completion, a record of the job should be written to a MySQL or MariaDB database,
> > specified by the **JobCompLoc** parameter.
> >
> > <!-- -->
> >
> > **jobcomp/script**  
> > Upon job completion, a script specified by the **JobCompLoc** parameter is to be executed with
> > environment variables providing the job information.
>
> **JobCompUser**  
> The user account for accessing the job completion database. Only used for database type storage
> plugins, ignored otherwise.
>
> <!-- -->
>
> **JobContainerType**  
> Identifies the plugin to be used for job tracking. A restart of slurmctld is required for changes
> to this parameter to take effect. **NOTE**: The **JobContainerType** applies to a job allocation,
> while **ProctrackType** applies to job steps. Acceptable values at present include:
>
> > **job_container/cncu**  
> > Used only for Cray systems (CNCU = Compute Node Clean Up)
> >
> > <!-- -->
> >
> > **job_container/none**  
> > Used for all other system types
> >
> > <!-- -->
> >
> > **job_container/tmpfs**  
> > Used to create a private namespace on the filesystem for jobs, which houses temporary file
> > systems (/tmp and /dev/shm) for each job. 'PrologFlags=Contain' must be set to use this plugin.
>
> **JobFileAppend**  
> This option controls what to do if a job's output or error file exist when the job is started. If
> **JobFileAppend** is set to a value of 1, then append to the existing file. By default, any
> existing file is truncated.
>
> <!-- -->
>
> **JobRequeue**  
> This option controls the default ability for batch jobs to be requeued. Jobs may be requeued
> explicitly by a system administrator, after node failure, or upon preemption by a higher priority
> job. If **JobRequeue** is set to a value of 1, then batch jobs may be requeued unless explicitly
> disabled by the user. If **JobRequeue** is set to a value of 0, then batch jobs will not be
> requeued unless explicitly enabled by the user. Use the **sbatch** *--no-requeue* or *--requeue*
> option to change the default behavior for individual jobs. The default value is 1.
>
> <!-- -->
>
> **JobSubmitPlugins**  
> These are intended to be site-specific plugins which can be used to set default job parameters
> and/or logging events. Slurm can be configured to use multiple job_submit plugins if desired,
> which must be specified as a comma-delimited list and will be executed in the order listed.
>
> <!-- -->
>
>     e.g. for multiple job_submit plugin configuration:
>     JobSubmitPlugins=lua,require_timelimit
>
> Take a look at \<https://slurm.schedmd.com/job_submit_plugins.html\> for further plugin
> implementation details. No job submission plugins are used by default. Currently available plugins
> are:
>
> > **all_partitions**  
> > Set default partition to all partitions on the cluster.
> >
> > <!-- -->
> >
> > **defaults**  
> > Set default values for job submission or modify requests.
> >
> > <!-- -->
> >
> > **logging**  
> > Log select job submission and modification parameters.
> >
> > <!-- -->
> >
> > **lua**  
> > Execute a Lua script implementing site's own job_submit logic. Only one Lua script will be
> > executed. It must be named "job_submit.lua" and must be located in the default configuration
> > directory (typically the subdirectory "etc" of the installation directory). Sample Lua scripts
> > can be found with the Slurm distribution, in the directory contribs/lua. Slurmctld will fatal on
> > startup if the configured lua script is invalid. Slurm will try to load the script for each job
> > submission. If the script is broken or removed while slurmctld is running, Slurm will fallback
> > to the previous working version of the script. **Warning**: slurmctld runs this script while
> > holding internal locks, and only a single copy of this script can run at a time. This blocks
> > most concurrency in slurmctld. Therefore, this script should run to completion as quickly as
> > possible.
> >
> > <!-- -->
> >
> > **partition**  
> > Set a job's default partition based upon job submission parameters and available partitions.
> >
> > <!-- -->
> >
> > **pbs**  
> > Translate PBS job submission options to Slurm equivalent (if possible).
> >
> > <!-- -->
> >
> > **require_timelimit**  
> > Force job submissions to specify a timelimit.
>
> **NOTE**: For examples of use see the Slurm code in "src/plugins/job_submit" and
> "contribs/lua/job_submit\*.lua" then modify the code to satisfy your needs.
>
> **KillOnBadExit**  
> If set to 1, a step will be terminated immediately if any task is crashed or aborted, as indicated
> by a non-zero exit code. With the default value of 0, if one of the processes is crashed or
> aborted the other processes will continue to run while the crashed or aborted process waits. The
> user can override this configuration parameter by using srun's **-K**, **--kill-on-bad-exit**.
>
> <!-- -->
>
> **KillWait**  
> The interval, in seconds, given to a job's processes between the SIGTERM and SIGKILL signals upon
> reaching its time limit. If the job fails to terminate gracefully in the interval specified, it
> will be forcibly terminated. The default value is 30 seconds. The value may not exceed 65533.
>
> <!-- -->
>
> **MaxBatchRequeue**  
> Maximum number of times a batch job may be automatically requeued before being marked as
> JobHeldAdmin. (Mainly useful when the **SchedulerParameters** option **nohold_on_prolog_fail** is
> enabled.) The default value is 5.
>
> <!-- -->
>
> **NodeFeaturesPlugins**  
> Identifies the plugins to be used for support of node features which can change through time. For
> example, a node which might be booted with various BIOS setting. This is supported through the use
> of a node's active_features and available_features information. Acceptable values at present
> include:
>
> > **node_features/knl_cray**  
> > Used only for Intel Knights Landing processors (KNL) on Cray systems. See
> > https://slurm.schedmd.com/intel_knl.html for more information.
> >
> > <!-- -->
> >
> > **node_features/knl_generic**  
> > Used for Intel Knights Landing processors (KNL) on a generic Linux system. See
> > https://slurm.schedmd.com/intel_knl.html for more information.
> >
> > <!-- -->
> >
> > **node_features/helpers**  
> > Used to report and modify features on nodes using arbitrary scripts or programs. See
> > helpers.conf man page for more information: https://slurm.schedmd.com/helpers.conf.html
>
> **LaunchParameters**  
> Identifies options to the job launch plugin. Acceptable values include:
>
> > **batch_step_set_cpu_freq**  
> > Set the cpu frequency for the batch step from given --cpu-freq, or slurm.conf CpuFreqDef,
> > option. By default only steps started with srun will utilize the cpu freq setting options.
> >
> > **NOTE**: If you are using srun to launch your steps inside a batch script (advised) this option
> > will create a situation where you may have multiple agents setting the cpu_freq as the batch
> > step usually runs on the same resources one or more steps the sruns in the script will create.
> >
> > <!-- -->
> >
> > **cray_net_exclusive**  
> > Allow jobs on a Cray XC cluster exclusive access to network resources. This should only be set
> > on clusters providing exclusive access to each node to a single job at once, and not using
> > parallel steps within the job, otherwise resources on the node can be oversubscribed.
> >
> > <!-- -->
> >
> > **enable_nss_slurm**  
> > Permits passwd and group resolution for a job to be serviced by slurmstepd rather than requiring
> > a lookup from a network based service. See https://slurm.schedmd.com/nss_slurm.html for more
> > information.
> >
> > <!-- -->
> >
> > **lustre_no_flush**  
> > If set on a Cray XC cluster, then do not flush the Lustre cache on job step completion. This
> > setting will only take effect after reconfiguring, and will only take effect for newly launched
> > jobs.
> >
> > <!-- -->
> >
> > **mem_sort**  
> > Sort NUMA memory at step start. User can override this default with SLURM_MEM_BIND environment
> > variable or --mem-bind=nosort command line option.
> >
> > <!-- -->
> >
> > **mpir_use_nodeaddr**  
> > When launching tasks Slurm creates entries in MPIR_proctable that are used by parallel
> > debuggers, profilers, and related tools to attach to running process. By default the
> > MPIR_proctable entries contain MPIR_procdesc structures where the host_name is set to NodeName
> > by default. If this option is specified, NodeAddr will be used in this context instead.
> >
> > <!-- -->
> >
> > **disable_send_gids**  
> > By default, the slurmctld will look up and send the user_name and extended gids for a job,
> > rather than independently on each node as part of each task launch. This helps mitigate issues
> > around name service scalability when launching jobs involving many nodes. Using this option will
> > disable this functionality. This option is ignored if enable_nss_slurm is specified.
> >
> > <!-- -->
> >
> > **slurmstepd_memlock**  
> > Lock the slurmstepd process's current memory in RAM.
> >
> > <!-- -->
> >
> > **slurmstepd_memlock_all**  
> > Lock the slurmstepd process's current and future memory in RAM.
> >
> > <!-- -->
> >
> > **test_exec**  
> > Have srun verify existence of the executable program along with user execute permission on the
> > node where srun was called before attempting to launch it on nodes in the step.
> >
> > <!-- -->
> >
> > **use_interactive_step**  
> > Have salloc use the Interactive Step to launch a shell on an allocated compute node rather than
> > locally to wherever salloc was invoked. This is accomplished by launching the srun command with
> > InteractiveStepOptions as options.
> >
> > This does not affect salloc called with a command as an argument. These jobs will continue to be
> > executed as the calling user on the calling host.
> >
> > <!-- -->
> >
> > **ulimit_pam_adopt**  
> > When pam_slurm_adopt is used to join an external process into a job cgroup, RLIMIT_RSS is set,
> > as is done for tasks running in regular steps.
>
> **Licenses**  
> Specification of licenses (or other resources available on all nodes of the cluster) which can be
> allocated to jobs. License names can optionally be followed by a colon and count with a default
> count of one. Multiple license names should be comma separated (e.g. "Licenses=foo:4,bar"). Note
> that Slurm prevents jobs from being scheduled if their required license specification is not
> available. Slurm does not prevent jobs from using licenses that are not explicitly listed in the
> job submission specification.
>
> <!-- -->
>
> **LogTimeFormat**  
> Format of the timestamp in slurmctld and slurmd log files. Accepted values are "iso8601",
> "iso8601_ms", "rfc5424", "rfc5424_ms", "rfc3339", "clock", "short" and "thread_id". The values
> ending in "\_ms" differ from the ones without in that fractional seconds with millisecond
> precision are printed. The default value is "iso8601_ms". The "rfc5424" formats are the same as
> the "iso8601" formats except that the timezone value is also shown. The "clock" format shows a
> timestamp in microseconds retrieved with the C standard clock() function. The "short" format is a
> short date and time format. The "thread_id" format shows the timestamp in the C standard ctime()
> function form without the year but including the microseconds, the daemon's process ID and the
> current thread name and ID.
>
> <!-- -->
>
> **MailDomain**  
> Domain name to qualify usernames if email address is not explicitly given with the "--mail-user"
> option. If unset, the local MTA will need to qualify local address itself. Changes to MailDomain
> will only affect new jobs.
>
> <!-- -->
>
> **MailProg**  
> Fully qualified pathname to the program used to send email per user request. The default value is
> "/bin/mail" (or "/usr/bin/mail" if "/bin/mail" does not exist but "/usr/bin/mail" does exist). The
> program is called with arguments suitable for the default mail command, however additional
> information about the job is passed in the form of environment variables.
>
> Additional variables are the same as those passed to *PrologSlurmctld* and *EpilogSlurmctld* with
> additional variables in the following contexts:
>
> > **ALL**  
> > **SLURM_JOB_STATE**  
> > The base state of the job when the MailProg is called.
> >
> > > **SLURM_JOB_MAIL_TYPE**  
> > > The mail type triggering the mail.
>
> > **BEGIN**  
> > **SLURM_JOB_QEUEUED_TIME**  
> > The amount of time the job was queued.
>
> > **END, FAIL, REQUEUE, TIME_LIMIT\_\***  
> > **SLURM_JOB_RUN_TIME**  
> > The amount of time the job ran for.
>
> > **END, FAIL**  
> > **SLURM_JOB_EXIT_CODE_MAX**  
> > Job's exit code or highest exit code for an array job.
> >
> > > **SLURM_JOB_EXIT_CODE_MIN**  
> > > Job's minimum exit code for an array job.
> >
> > > **SLURM_JOB_TERM_SIGNAL_MAX**  
> > > Job's highest signal for an array job.
>
> > **STAGE_OUT**  
> > **SLURM_JOB_STAGE_OUT_TIME**  
> > Job's staging out time.
>
> **MaxArraySize**  
> The maximum job array task index value will be one less than MaxArraySize to allow for an index
> value of zero. Configure MaxArraySize to 0 in order to disable job array use. The value may not
> exceed 4000001. The value of **MaxJobCount** should be much larger than **MaxArraySize**. The
> default value is 1001. See also **max_array_tasks** in SchedulerParameters.
>
> <!-- -->
>
> **MaxDBDMsgs**  
> When communication to the SlurmDBD is not possible the slurmctld will queue messages meant to
> processed when the SlurmDBD is available again. In order to avoid running out of memory the
> slurmctld will only queue so many messages. The default value is 10000, or **MaxJobCount** \* 2 +
> Node Count \* 4, whichever is greater. The value can not be less than 10000.
>
> <!-- -->
>
> **MaxJobCount**  
> The maximum number of jobs slurmctld can have in memory at one time. Combine with **MinJobAge** to
> ensure the slurmctld daemon does not exhaust its memory or other resources. Once this limit is
> reached, requests to submit additional jobs will fail. The default value is 10000 jobs. **NOTE**:
> Each task of a job array counts as one job even though they will not occupy separate job records
> until modified or initiated. Performance can suffer with more than a few hundred thousand jobs.
> Setting per MaxSubmitJobs per user is generally valuable to prevent a single user from filling the
> system with jobs. This is accomplished using Slurm's database and configuring enforcement of
> resource limits. A restart of slurmctld is required for changes to this parameter to take effect.
>
> <!-- -->
>
> **MaxJobId**  
> The maximum job id to be used for jobs submitted to Slurm without a specific requested value. Job
> ids are unsigned 32bit integers with the first 26 bits reserved for local job ids and the
> remaining 6 bits reserved for a cluster id to identify a federated job's origin. The maximum
> allowed local job id is 67,108,863 (0x3FFFFFF). The default value is 67,043,328 (0x03ff0000).
> **MaxJobId** only applies to the local job id and not the federated job id. Job id values
> generated will be incremented by 1 for each subsequent job. Once **MaxJobId** is reached, the next
> job will be assigned **FirstJobId**. Federated jobs will always have a job ID of 67,108,865 or
> higher. Also see **FirstJobId**.
>
> <!-- -->
>
> **MaxMemPerCPU**  
> Maximum real memory size available per allocated CPU in megabytes. Used to avoid over-subscribing
> memory and causing paging. **MaxMemPerCPU** would generally be used if individual processors are
> allocated to jobs (**SelectType=select/cons_res** or **SelectType=select/cons_tres**). The default
> value is 0 (unlimited). Also see **DefMemPerCPU**, **DefMemPerGPU** and **MaxMemPerNode**.
> **MaxMemPerCPU** and **MaxMemPerNode** are mutually exclusive.
>
> **NOTE**: If a job specifies a memory per CPU limit that exceeds this system limit, that job's
> count of CPUs per task will try to automatically increase. This may result in the job failing due
> to CPU count limits. This auto-adjustment feature is a best-effort one and optimal assignment is
> not guaranteed due to the possibility of having heterogeneous configurations and
> multi-partition/qos jobs. If this is a concern it is advised to use a job submit LUA plugin
> instead to enforce auto-adjustments to your specific needs.
>
> <!-- -->
>
> **MaxMemPerNode**  
> Maximum real memory size available per allocated node in megabytes. Used to avoid over-subscribing
> memory and causing paging. **MaxMemPerNode** would generally be used if whole nodes are allocated
> to jobs (**SelectType=select/linear**) and resources are over-subscribed (**OverSubscribe=yes** or
> **OverSubscribe=force**). The default value is 0 (unlimited). Also see **DefMemPerNode** and
> **MaxMemPerCPU**. **MaxMemPerCPU** and **MaxMemPerNode** are mutually exclusive.
>
> <!-- -->
>
> **MaxNodeCount**  
> Maximum count of nodes which may exist in the controller. By default MaxNodeCount will be set to
> the number of nodes found in the slurm.conf. MaxNodeCount will be ignored if less than the number
> of nodes found in the slurm.conf. Increase MaxNodeCount to accommodate dynamically created nodes
> with dynamic node registrations and nodes created with scontrol. The slurmctld daemon must be
> restarted for changes to this parameter to take effect.
>
> <!-- -->
>
> **MaxStepCount**  
> The maximum number of steps that any job can initiate. This parameter is intended to limit the
> effect of bad batch scripts. The default value is 40000 steps.
>
> <!-- -->
>
> **MaxTasksPerNode**  
> Maximum number of tasks Slurm will allow a job step to spawn on a single node. The default
> **MaxTasksPerNode** is 512. May not exceed 65533.
>
> <!-- -->
>
> **MCSParameters**  
> MCS = Multi-Category Security MCS Plugin Parameters. The supported parameters are specific to the
> **MCSPlugin**. Changes to this value take effect when the Slurm daemons are reconfigured. More
> information about MCS is available here \<https://slurm.schedmd.com/mcs.html\>.
>
> <!-- -->
>
> **MCSPlugin**  
> MCS = Multi-Category Security : associate a security label to jobs and ensure that nodes can only
> be shared among jobs using the same security label. Acceptable values include:
>
> > **mcs/none**  
> > is the default value. No security label associated with jobs, no particular security restriction
> > when sharing nodes among jobs.
> >
> > <!-- -->
> >
> > **mcs/account**  
> > only users with the same account can share the nodes (requires enabling of accounting).
> >
> > <!-- -->
> >
> > **mcs/group**  
> > only users with the same group can share the nodes.
> >
> > <!-- -->
> >
> > **mcs/user**  
> > a node cannot be shared with other users.
>
> **MessageTimeout**  
> Time permitted for a round-trip communication to complete in seconds. Default value is 10 seconds.
> For systems with shared nodes, the slurmd daemon could be paged out and necessitate higher values.
>
> <!-- -->
>
> **MinJobAge**  
> The minimum age of a completed job before its record is cleared from the list of jobs slurmctld
> keeps in memory. Combine with **MaxJobCount** to ensure the slurmctld daemon does not exhaust its
> memory or other resources. The default value is 300 seconds. A value of zero prevents any job
> record purging. Jobs are not purged during a backfill cycle, so it can take longer than MinJobAge
> seconds to purge a job if using the backfill scheduling plugin. In order to eliminate some
> possible race conditions, the minimum non-zero value for **MinJobAge** recommended is 2.
>
> <!-- -->
>
> **MpiDefault**  
> Identifies the default type of MPI to be used. Srun may override this configuration parameter in
> any case. Currently supported versions include: **pmi2**, **pmix**, and **none** (default, which
> works for many other versions of MPI). More information about MPI use is available here
> \<https://slurm.schedmd.com/mpi_guide.html\>.
>
> <!-- -->
>
> **MpiParams**  
> MPI parameters. Used to identify ports used by native Cray's PMI. The format to identify a range
> of communication ports is "ports=12000-12999".
>
> <!-- -->
>
> **OverTimeLimit**  
> Number of minutes by which a job can exceed its time limit before being canceled. Normally a job's
> time limit is treated as a *hard* limit and the job will be killed upon reaching that limit.
> Configuring **OverTimeLimit** will result in the job's time limit being treated like a *soft*
> limit. Adding the **OverTimeLimit** value to the *soft* time limit provides a *hard* time limit,
> at which point the job is canceled. This is particularly useful for backfill scheduling, which
> bases upon each job's soft time limit. The default value is zero. May not exceed 65533 minutes. A
> value of "UNLIMITED" is also supported.
>
> <!-- -->
>
> **PluginDir**  
> Identifies the places in which to look for Slurm plugins. This is a colon-separated list of
> directories, like the PATH environment variable. The default value is the prefix given at
> configure time + "/lib/slurm". A restart of slurmctld and the slurmd daemons is required for
> changes to this parameter to take effect.
>
> <!-- -->
>
> **PlugStackConfig**  
> Location of the config file for Slurm stackable plugins that use the Stackable Plugin Architecture
> for Node job (K)control (SPANK). This provides support for a highly configurable set of plugins to
> be called before and/or after execution of each task spawned as part of a user's job step. Default
> location is "plugstack.conf" in the same directory as the system slurm.conf. For more information
> on SPANK plugins, see the **spank**(8) manual.
>
> <!-- -->
>
> **PowerParameters**  
> System power management parameters. The supported parameters are specific to the **PowerPlugin**.
> Changes to this value take effect when the Slurm daemons are reconfigured. More information about
> system power management is available here \<https://slurm.schedmd.com/power_mgmt.html\>. Options
> current supported by any plugins are listed below.
>
> > **balance_interval=#**  
> > Specifies the time interval, in seconds, between attempts to rebalance power caps across the
> > nodes. This also controls the frequency at which Slurm attempts to collect current power
> > consumption data (old data may be used until new data is available from the underlying
> > infrastructure and values below 10 seconds are not recommended for Cray systems). The default
> > value is 30 seconds. Supported by the power/cray_aries plugin.
> >
> > <!-- -->
> >
> > **capmc_path=**  
> > Specifies the absolute path of the capmc command. The default value is
> > "/opt/cray/capmc/default/bin/capmc". Supported by the power/cray_aries plugin.
> >
> > <!-- -->
> >
> > **cap_watts=#**  
> > Specifies the total power limit to be established across all compute nodes managed by Slurm. A
> > value of 0 sets every compute node to have an unlimited cap. The default value is 0. Supported
> > by the power/cray_aries plugin.
> >
> > <!-- -->
> >
> > **decrease_rate=#**  
> > Specifies the maximum rate of change in the power cap for a node where the actual power usage is
> > below the power cap by an amount greater than **lower_threshold** (see below). Value represents
> > a percentage of the difference between a node's minimum and maximum power consumption. The
> > default value is 50 percent. Supported by the power/cray_aries plugin.
> >
> > <!-- -->
> >
> > **get_timeout=#**  
> > Amount of time allowed to get power state information in milliseconds. The default value is
> > 5,000 milliseconds or 5 seconds. Supported by the power/cray_aries plugin and represents the
> > time allowed for the capmc command to respond to various "get" options.
> >
> > <!-- -->
> >
> > **increase_rate=#**  
> > Specifies the maximum rate of change in the power cap for a node where the actual power usage is
> > within **upper_threshold** (see below) of the power cap. Value represents a percentage of the
> > difference between a node's minimum and maximum power consumption. The default value is 20
> > percent. Supported by the power/cray_aries plugin.
> >
> > <!-- -->
> >
> > **job_level**  
> > All nodes associated with every job will have the same power cap, to the extent possible. Also
> > see the --power=level option on the job submission commands.
> >
> > <!-- -->
> >
> > **job_no_level**  
> > Disable the user's ability to set every node associated with a job to the same power cap. Each
> > node will have its power cap set independently. This disables the --power=level option on the
> > job submission commands.
> >
> > <!-- -->
> >
> > **lower_threshold=#**  
> > Specify a lower power consumption threshold. If a node's current power consumption is below this
> > percentage of its current cap, then its power cap will be reduced. The default value is 90
> > percent. Supported by the power/cray_aries plugin.
> >
> > <!-- -->
> >
> > **recent_job=#**  
> > If a job has started or resumed execution (from suspend) on a compute node within this number of
> > seconds from the current time, the node's power cap will be increased to the maximum. The
> > default value is 300 seconds. Supported by the power/cray_aries plugin.
> >
> > <!-- -->
> >
> > **set_timeout=#**  
> > Amount of time allowed to set power state information in milliseconds. The default value is
> > 30,000 milliseconds or 30 seconds. Supported by the power/cray plugin and represents the time
> > allowed for the capmc command to respond to various "set" options.
> >
> > <!-- -->
> >
> > **set_watts=#**  
> > Specifies the power limit to be set on every compute nodes managed by Slurm. Every node gets
> > this same power cap and there is no variation through time based upon actual power usage on the
> > node. Supported by the power/cray_aries plugin.
> >
> > <!-- -->
> >
> > **upper_threshold=#**  
> > Specify an upper power consumption threshold. If a node's current power consumption is above
> > this percentage of its current cap, then its power cap will be increased to the extent possible.
> > The default value is 95 percent. Supported by the power/cray_aries plugin.
>
> **PowerPlugin**  
> Identifies the plugin used for system power management. Currently supported plugins include:
> **cray_aries** and **none**. A restart of slurmctld is required for changes to this parameter to
> take effect. More information about system power management is available here
> \<https://slurm.schedmd.com/power_mgmt.html\>. By default, no power plugin is loaded.
>
> <!-- -->
>
> **PreemptMode**  
> Mechanism used to preempt jobs or enable gang scheduling. When the **PreemptType** parameter is
> set to enable preemption, the **PreemptMode** selects the default mechanism used to preempt the
> eligible jobs for the cluster.  
> **PreemptMode** may be specified on a per partition basis to override this default value if
> **PreemptType=preempt/partition_prio**. Alternatively, it can be specified on a per QOS basis if
> **PreemptType=preempt/qos**. In either case, a valid default **PreemptMode** value must be
> specified for the cluster as a whole when preemption is enabled.  
> The **GANG** option is used to enable gang scheduling independent of whether preemption is enabled
> (i.e. independent of the **PreemptType** setting). It can be specified in addition to a
> **PreemptMode** setting with the two options comma separated (e.g.
> **PreemptMode=SUSPEND,GANG**).  
> See \<https://slurm.schedmd.com/preempt.html\> and
> \<https://slurm.schedmd.com/gang_scheduling.html\> for more details.
>
> **NOTE**: For performance reasons, the backfill scheduler reserves whole nodes for jobs, not
> partial nodes. If during backfill scheduling a job preempts one or more other jobs, the whole
> nodes for those preempted jobs are reserved for the preemptor job, even if the preemptor job
> requested fewer resources than that. These reserved nodes aren't available to other jobs during
> that backfill cycle, even if the other jobs could fit on the nodes. Therefore, jobs may preempt
> more resources during a single backfill iteration than they requested.  
> **NOTE**: For heterogeneous job to be considered for preemption all components must be eligible
> for preemption. When a heterogeneous job is to be preempted the first identified component of the
> job with the highest order PreemptMode (**SUSPEND** (highest), **REQUEUE**, **CANCEL** (lowest))
> will be used to set the PreemptMode for all components. The **GraceTime** and user warning signal
> for each component of the heterogeneous job remain unique. Heterogeneous jobs are excluded from
> GANG scheduling operations.
>
> > **OFF**  
> > Is the default value and disables job preemption and gang scheduling. It is only compatible with
> > **PreemptType=preempt/none** at a global level. A common use case for this parameter is to set
> > it on a partition to disable preemption for that partition.
> >
> > <!-- -->
> >
> > **CANCEL**  
> > The preempted job will be cancelled.
> >
> > <!-- -->
> >
> > **GANG**  
> > Enables gang scheduling (time slicing) of jobs in the same partition, and allows the resuming of
> > suspended jobs. In order to use gang scheduling, the **GANG** option must be specified at the
> > cluster level.
> >
> > **NOTE**: Gang scheduling is performed independently for each partition, so if you only want
> > time-slicing by **OverSubscribe**, without any preemption, then configuring partitions with
> > overlapping nodes is not recommended. On the other hand, if you want to use
> > **PreemptType=preempt/partition_prio** to allow jobs from higher PriorityTier partitions to
> > Suspend jobs from lower PriorityTier partitions you will need overlapping partitions, and
> > **PreemptMode=SUSPEND,GANG** to use the Gang scheduler to resume the suspended jobs(s). You must
> > configure the partition's *OverSubscribe* setting to *FORCE* for all partitions in which
> > time-slicing is to take place. In any case, time-slicing won't happen between jobs on different
> > partitions.
> >
> > **NOTE**: Heterogeneous jobs are excluded from GANG scheduling operations.
> >
> > <!-- -->
> >
> > **REQUEUE**  
> > Preempts jobs by requeuing them (if possible) or canceling them. For jobs to be requeued they
> > must have the --requeue sbatch option set or the cluster wide JobRequeue parameter in slurm.conf
> > must be set to **1**.
> >
> > <!-- -->
> >
> > **SUSPEND**  
> > The preempted jobs will be suspended, and later the Gang scheduler will resume them. Therefore
> > the **SUSPEND** preemption mode always needs the **GANG** option to be specified at the cluster
> > level. Also, because the suspended jobs will still use memory on the allocated nodes, Slurm
> > needs to be able to track memory resources to be able to suspend jobs.  
> > If **PreemptType=preempt/qos** is configured and if the preempted job(s) and the preemptor job
> > are on the same partition, then they will share resources with the Gang scheduler
> > (time-slicing). If not (i.e. if the preemptees and preemptor are on different partitions) then
> > the preempted jobs will remain suspended until the preemptor ends.
> >
> > **NOTE**: Because gang scheduling is performed independently for each partition, if using
> > **PreemptType=preempt/partition_prio** then jobs in higher PriorityTier partitions will suspend
> > jobs in lower PriorityTier partitions to run on the released resources. Only when the preemptor
> > job ends will the suspended jobs will be resumed by the Gang scheduler.  
> > **NOTE**: Suspended jobs will not release GRES. Higher priority jobs will not be able to preempt
> > to gain access to GRES.
> >
> > <!-- -->
> >
> > **WITHIN**  
> > For **PreemptType=preempt/qos**, allow jobs within the same qos to preempt one another. While
> > this can be set globally here, it is recommend that this only be set directly on a relevant
> > subset of the system qos values instead.
>
> **PreemptParameters**  
> Multiple options may be comma separated.
>
> **min_exempt_priority=#**  
> Threshold value for the job's global priority. Only those jobs with priority lower than this value
> will be marked as preemptable.
>
> **reclaim_licenses**  
> If set, jobs may be preempted to reclaim licenses. Otherwise jobs requesting busy licenses will
> have to wait even if they have preemption priority. The logic to support this option is only
> available in the select/cons_res and select/cons_tres plugins.
>
> **reorder_count=#**  
> Specify how many attempts should be made in reordering preemptable jobs to minimize the count of
> jobs preempted. The default value is 1. High values may adversely impact performance. The logic to
> support this option is only available in the select/cons_res and select/cons_tres plugins.
>
> **send_user_signal**  
> Send the user signal (e.g. --signal=\<sig_num\>) at preemption time even if the signal time hasn't
> been reached. In the case of a gracetime preemption the user signal will be sent if the user
> signal has been specified and not sent, otherwise a SIGTERM will be sent to the tasks.
>
> **strict_order**  
> If set, then execute extra logic in an attempt to preempt only the lowest priority jobs. It may be
> desirable to set this configuration parameter when there are multiple priorities of preemptable
> jobs. The logic to support this option is only available in the select/cons_res and
> select/cons_tres plugins.
>
> **youngest_first**  
> If set, then the preemption sorting algorithm will be changed to sort by the job start times to
> favor preempting younger jobs over older. (Requires preempt/partition_prio or preempt/qos
> plugins.)
>
> <!-- -->
>
> **PreemptType**  
> Specifies the plugin used to identify which jobs can be preempted in order to start a pending job.
>
> > **preempt/none**  
> > Job preemption is disabled. This is the default.
> >
> > <!-- -->
> >
> > **preempt/partition_prio**  
> > Job preemption is based upon partition **PriorityTier**. Jobs in higher **PriorityTier**
> > partitions may preempt jobs from lower **PriorityTier** partitions. This is not compatible with
> > **PreemptMode=OFF**.
> >
> > <!-- -->
> >
> > **preempt/qos**  
> > Job preemption rules are specified by Quality Of Service (QOS) specifications in the Slurm
> > database. In the case of **PreemptMode=SUSPEND**, a preempting job has to be submitted to a
> > partition with a higher PriorityTier or to the same partition. Submission to the same partition
> > is also supported, which results in the preemptor QoS to gang schedule the preemptee QoS. This
> > option is not compatible with **PreemptMode=OFF**. A configuration of **PreemptMode=SUSPEND** is
> > only supported by the **SelectType=select/cons_res** and **SelectType=select/cons_tres**
> > plugins. See the **sacctmgr** man page to configure the options for **preempt/qos**.
>
> **PreemptExemptTime**  
> Global option for minimum run time for all jobs before they can be considered for preemption. Any
> QOS PreemptExemptTime takes precedence over the global option. This is only honored for
> **PreemptMode=REQUEUE** and **PreemptMode=CANCEL**.  
> A time of -1 disables the option, equivalent to 0. Acceptable time formats include "minutes",
> "minutes:seconds", "hours:minutes:seconds", "days-hours", "days-hours:minutes", and
> "days-hours:minutes:seconds".
>
> <!-- -->
>
> **PrEpParameters**  
> Parameters to be passed to the **PrEpPlugins**.
>
> <!-- -->
>
> **PrEpPlugins**  
> A resource for programmers wishing to write their own plugins for the Prolog and Epilog (PrEp)
> scripts. The default, and currently the only implemented plugin is *prep/script*. Additional
> plugins can be specified in a comma-separated list. For more information please see the PrEp
> Plugin API documentation page: \<https://slurm.schedmd.com/prep_plugins.html\>
>
> <!-- -->
>
> **PriorityCalcPeriod**  
> The period of time in minutes in which the half-life decay will be re-calculated. Applicable only
> if PriorityType=priority/multifactor. The default value is 5 (minutes).
>
> <!-- -->
>
> **PriorityDecayHalfLife**  
> This controls how long prior resource use is considered in determining how over- or under-serviced
> an association is (user, bank account and cluster) in determining job priority. The record of
> usage will be decayed over time, with half of the original value cleared at age
> **PriorityDecayHalfLife**. If set to 0 no decay will be applied. This is helpful if you want to
> enforce hard time limits per association. If set to 0 **PriorityUsageResetPeriod** must be set to
> some interval. Applicable only if PriorityType=priority/multifactor. The unit is a time string
> (i.e. min, hr:min:00, days-hr:min:00, or days-hr). The default value is 7-0 (7 days).
>
> <!-- -->
>
> **PriorityFavorSmall**  
> Specifies that small jobs should be given preferential scheduling priority. Applicable only if
> PriorityType=priority/multifactor. Supported values are "YES" and "NO". The default value is "NO".
>
> <!-- -->
>
> **PriorityFlags**  
> Flags to modify priority behavior. Applicable only if PriorityType=priority/multifactor. The
> keywords below have no associated value (e.g.
> "PriorityFlags=ACCRUE_ALWAYS,SMALL_RELATIVE_TO_TIME").
>
> > **ACCRUE_ALWAYS**  
> > If set, priority age factor will be increased despite job ineligibility due to either
> > dependencies, holds or begin time in the future. Accrue limits are ignored.
> >
> > <!-- -->
> >
> > **CALCULATE_RUNNING**  
> > If set, priorities will be recalculated not only for pending jobs, but also running and
> > suspended jobs.
> >
> > <!-- -->
> >
> > **DEPTH_OBLIVIOUS**  
> > If set, priority will be calculated based similar to the normal multifactor calculation, but
> > depth of the associations in the tree does not adversely affect their priority. This option
> > automatically enables NO_FAIR_TREE.
> >
> > <!-- -->
> >
> > **NO_FAIR_TREE**  
> > Disables the "fair tree" algorithm, and reverts to "classic" fair share priority scheduling.
> >
> > <!-- -->
> >
> > **INCR_ONLY**  
> > If set, priority values will only increase in value. Job priority will never decrease in value.
> >
> > <!-- -->
> >
> > **MAX_TRES**  
> > If set, the weighted TRES value (e.g. TRESBillingWeights) is calculated as the MAX of individual
> > TRESs on a node (e.g. cpus, mem, gres) plus the sum of all global TRESs (e.g. licenses).
> >
> > <!-- -->
> >
> > **NO_NORMAL_ALL**  
> > If set, all NO_NORMAL\_\* flags are set.
> >
> > <!-- -->
> >
> > **NO_NORMAL_ASSOC**  
> > If set, the association factor is not normalized against the highest association priority.
> >
> > <!-- -->
> >
> > **NO_NORMAL_PART**  
> > If set, the partition factor is not normalized against the highest partition
> > **PriorityJobFactor**.
> >
> > <!-- -->
> >
> > **NO_NORMAL_QOS**  
> > If set, the QOS factor is not normalized against the highest qos priority.
> >
> > <!-- -->
> >
> > **NO_NORMAL_TRES**  
> > If set, the TRES factor is not normalized against the job's partition TRES counts.
> >
> > <!-- -->
> >
> > **SMALL_RELATIVE_TO_TIME**  
> > If set, the job's size component will be based upon not the job size alone, but the job's size
> > divided by its time limit.
>
> **PriorityMaxAge**  
> Specifies the job age which will be given the maximum age factor in computing priority. For
> example, a value of 30 minutes would result in all jobs over 30 minutes old would get the same
> age-based priority. Applicable only if PriorityType=priority/multifactor. The unit is a time
> string (i.e. min, hr:min:00, days-hr:min:00, or days-hr). The default value is 7-0 (7 days).
>
> <!-- -->
>
> **PriorityParameters**  
> Arbitrary string used by the PriorityType plugin.
>
> <!-- -->
>
> **PrioritySiteFactorParameters**  
> Arbitrary string used by the PrioritySiteFactorPlugin plugin.
>
> <!-- -->
>
> **PrioritySiteFactorPlugin**  
> The specifies an optional plugin to be used alongside "priority/multifactor", which is meant to
> initially set and continuously update the SiteFactor priority factor. The default value is
> "site_factor/none".
>
> <!-- -->
>
> **PriorityType**  
> This specifies the plugin to be used in establishing a job's scheduling priority. Also see
> **PriorityFlags** for configuration options. The default value is "priority/basic".
>
> > **priority/basic**  
> > Jobs are evaluated in a First In, First Out (FIFO) manner.
> >
> > <!-- -->
> >
> > **priority/multifactor**  
> > Jobs are assigned a priority based upon a variety of factors that include size, age, Fairshare,
> > etc.
>
> > When not FIFO scheduling, jobs are prioritized in the following order:  
> >
> > 1\. Jobs that can preempt  
> > 2. Jobs with an advanced reservation  
> > 3. Partition PriorityTier  
> > 4. Job priority  
> > 5. Job submit time  
> > 6. Job ID
>
> **PriorityUsageResetPeriod**  
> At this interval the usage of associations will be reset to 0. This is used if you want to enforce
> hard limits of time usage per association. If PriorityDecayHalfLife is set to be 0 no decay will
> happen and this is the only way to reset the usage accumulated by running jobs. By default this is
> turned off and it is advised to use the PriorityDecayHalfLife option to avoid not having anything
> running on your cluster, but if your schema is set up to only allow certain amounts of time on
> your system this is the way to do it. Applicable only if PriorityType=priority/multifactor.
>
> > **NONE**  
> > Never clear historic usage. The default value.
> >
> > <!-- -->
> >
> > **NOW**  
> > Clear the historic usage now. Executed at startup and reconfiguration time.
> >
> > <!-- -->
> >
> > **DAILY**  
> > Cleared every day at midnight.
> >
> > <!-- -->
> >
> > **WEEKLY**  
> > Cleared every week on Sunday at time 00:00.
> >
> > <!-- -->
> >
> > **MONTHLY**  
> > Cleared on the first day of each month at time 00:00.
> >
> > <!-- -->
> >
> > **QUARTERLY**  
> > Cleared on the first day of each quarter at time 00:00.
> >
> > <!-- -->
> >
> > **YEARLY**  
> > Cleared on the first day of each year at time 00:00.
>
> **PriorityWeightAge**  
> An integer value that sets the degree to which the queue wait time component contributes to the
> job's priority. Applicable only if PriorityType=priority/multifactor. Requires
> AccountingStorageType=accounting_storage/slurmdbd. The default value is 0.
>
> <!-- -->
>
> **PriorityWeightAssoc**  
> An integer value that sets the degree to which the association component contributes to the job's
> priority. Applicable only if PriorityType=priority/multifactor. The default value is 0.
>
> <!-- -->
>
> **PriorityWeightFairshare**  
> An integer value that sets the degree to which the fair-share component contributes to the job's
> priority. Applicable only if PriorityType=priority/multifactor. Requires
> AccountingStorageType=accounting_storage/slurmdbd. The default value is 0.
>
> <!-- -->
>
> **PriorityWeightJobSize**  
> An integer value that sets the degree to which the job size component contributes to the job's
> priority. Applicable only if PriorityType=priority/multifactor. The default value is 0.
>
> <!-- -->
>
> **PriorityWeightPartition**  
> Partition factor used by priority/multifactor plugin in calculating job priority. Applicable only
> if PriorityType=priority/multifactor. The default value is 0.
>
> <!-- -->
>
> **PriorityWeightQOS**  
> An integer value that sets the degree to which the Quality Of Service component contributes to the
> job's priority. Applicable only if PriorityType=priority/multifactor. The default value is 0.
>
> <!-- -->
>
> **PriorityWeightTRES**  
> A comma-separated list of TRES Types and weights that sets the degree that each TRES Type
> contributes to the job's priority.
>
>     e.g.
>     PriorityWeightTRES=CPU=1000,Mem=2000,GRES/gpu=3000
>
> Applicable only if PriorityType=priority/multifactor and if AccountingStorageTRES is configured
> with each TRES Type. Negative values are allowed. The default values are 0.
>
> <!-- -->
>
> **PrivateData**  
> This controls what type of information is hidden from regular users. By default, all information
> is visible to all users. User **SlurmUser** and **root** can always view all information. Multiple
> values may be specified with a comma separator. Acceptable values include:
>
> > **accounts**  
> > (NON-SlurmDBD ACCOUNTING ONLY) Prevents users from viewing any account definitions unless they
> > are coordinators of them.
> >
> > <!-- -->
> >
> > **events**  
> > prevents users from viewing event information unless they have operator status or above.
> >
> > <!-- -->
> >
> > **jobs**  
> > Prevents users from viewing jobs or job steps belonging to other users. (NON-SlurmDBD ACCOUNTING
> > ONLY) Prevents users from viewing job records belonging to other users unless they are
> > coordinators of the association running the job when using sacct.
> >
> > <!-- -->
> >
> > **nodes**  
> > Prevents users from viewing node state information.
> >
> > <!-- -->
> >
> > **partitions**  
> > Prevents users from viewing partition state information.
> >
> > <!-- -->
> >
> > **reservations**  
> > Prevents regular users from viewing reservations which they can not use.
> >
> > <!-- -->
> >
> > **usage**  
> > Prevents users from viewing usage of any other user, this applies to sshare. (NON-SlurmDBD
> > ACCOUNTING ONLY) Prevents users from viewing usage of any other user, this applies to sreport.
> >
> > <!-- -->
> >
> > **users**  
> > (NON-SlurmDBD ACCOUNTING ONLY) Prevents users from viewing information of any user other than
> > themselves, this also makes it so users can only see associations they deal with. Coordinators
> > can see associations of all users in the account they are coordinator of, but can only see
> > themselves when listing users.
>
> **ProctrackType**  
> Identifies the plugin to be used for process tracking on a job step basis. The slurmd daemon uses
> this mechanism to identify all processes which are children of processes it spawns for a user job
> step. A restart of slurmctld is required for changes to this parameter to take effect. **NOTE**:
> "proctrack/linuxproc" and "proctrack/pgid" can fail to identify all processes associated with a
> job since processes can become a child of the init process (when the parent process terminates) or
> change their process group. To reliably track all processes, "proctrack/cgroup" is highly
> recommended. **NOTE**: The **JobContainerType** applies to a job allocation, while
> **ProctrackType** applies to job steps. Acceptable values at present include:
>
> > **proctrack/cgroup**  
> > Uses linux cgroups to constrain and track processes, and is the default for systems with cgroup
> > support.  
> > **NOTE**: See "man cgroup.conf" for configuration details.
> >
> > <!-- -->
> >
> > **proctrack/cray_aries**  
> > Uses Cray proprietary process tracking.
> >
> > <!-- -->
> >
> > **proctrack/linuxproc**  
> > Uses linux process tree using parent process IDs.
> >
> > <!-- -->
> >
> > **proctrack/pgid**  
> > Uses Process Group IDs.  
> > **NOTE**: This is the default for the BSD family.
>
> **Prolog**  
> Fully qualified pathname of a program for the slurmd to execute whenever it is asked to run a job
> step from a new job allocation (e.g. "/usr/local/slurm/prolog"). A glob pattern (See **glob** (7))
> may also be used to specify more than one program to run (e.g. "/etc/slurm/prolog.d/\*"). When
> more than one prolog script is configured, they are executed in reverse order. The slurmd executes
> the prolog before starting the first job step. The prolog script or scripts may be used to purge
> files, enable user login, etc. By default there is no prolog. Any configured script is expected to
> complete execution quickly (in less time than **MessageTimeout**). If the prolog fails (returns a
> non-zero exit code), this will result in the node being set to a DRAIN state and the job being
> requeued. The job will be placed in a held state, unless **nohold_on_prolog_fail** is configured
> in **SchedulerParameters**. See **Prolog and Epilog Scripts** for more information.
>
> <!-- -->
>
> **PrologEpilogTimeout**  
> The interval in seconds Slurm waits for Prolog and Epilog before terminating them. The default
> behavior is to wait indefinitely. This interval applies to the Prolog and Epilog run by slurmd
> daemon before and after the job, the PrologSlurmctld and EpilogSlurmctld run by slurmctld daemon,
> and the SPANK plugin prolog/epilog calls: slurm_spank_job_prolog and slurm_spank_job_epilog.  
> If the PrologSlurmctld times out, the job is requeued if possible. If the Prolog or
> slurm_spank_job_prolog time out, the job is requeued if possible and the node is drained. If the
> Epilog or slurm_spank_job_epilog time out, the node is drained. In all cases, errors are logged.
>
> <!-- -->
>
> **PrologFlags**  
> Flags to control the Prolog behavior. By default no flags are set. Multiple flags may be specified
> in a comma-separated list. Currently supported options are:
>
> > **Alloc**  
> > If set, the Prolog script will be executed at job allocation. By default, Prolog is executed
> > just before the task is launched. Therefore, when salloc is started, no Prolog is executed.
> > Alloc is useful for preparing things before a user starts to use any allocated resources. In
> > particular, this flag is needed on a Cray system when cluster compatibility mode is enabled.
> >
> > **NOTE**: Use of the Alloc flag will increase the time required to start jobs.
> >
> > <!-- -->
> >
> > **Contain**  
> > At job allocation time, use the ProcTrack plugin to create a job container on all allocated
> > compute nodes. This container may be used for user processes not launched under Slurm control,
> > for example pam_slurm_adopt may place processes launched through a direct user login into this
> > container. If using pam_slurm_adopt, then ProcTrackType must be set to either
> > **proctrack/cgroup** or **proctrack/cray_aries**. Setting the Contain implicitly sets the Alloc
> > flag.
> >
> > <!-- -->
> >
> > **DeferBatch**  
> > If set, slurmctld will wait until the prolog completes on all allocated nodes before sending the
> > batch job launch request. With just the Alloc flag, slurmctld will launch the batch step as soon
> > as the first node in the job allocation completes the prolog.
> >
> > <!-- -->
> >
> > **NoHold**  
> > If set, the Alloc flag should also be set. This will allow for salloc to not block until the
> > prolog is finished on each node. The blocking will happen when steps reach the slurmd and before
> > any execution has happened in the step. This is a much faster way to work and if using srun to
> > launch your tasks you should use this flag. This flag cannot be combined with the Contain or X11
> > flags.
> >
> > <!-- -->
> >
> > **ForceRequeueOnFail**  
> > When a batch job fails to launch due to a Prolog failure, always requeue it automatically even
> > if the job requested no requeues.
> >
> > **NOTE**: Setting this flag implicitly sets the Alloc flag.
> >
> > <!-- -->
> >
> > **Serial**  
> > By default, the Prolog and Epilog scripts run concurrently on each node. This flag forces those
> > scripts to run serially within each node, but with a significant penalty to job throughput on
> > each node.
> >
> > <!-- -->
> >
> > **X11**  
> > Enable Slurm's built-in X11 forwarding capabilities. This is incompatible with
> > **ProctrackType=proctrack/linuxproc**. Setting the X11 flag implicitly enables both Contain and
> > Alloc flags as well.
>
> **PrologSlurmctld**  
> Fully qualified pathname of a program for the slurmctld daemon to execute before granting a new
> job allocation (e.g. "/usr/local/slurm/prolog_controller"). The program executes as SlurmUser on
> the same node where the slurmctld daemon executes, giving it permission to drain nodes and requeue
> the job if a failure occurs or cancel the job if appropriate. Exactly what the program does and
> how it accomplishes this is completely at the discretion of the system administrator. Information
> about the job being initiated, its allocated nodes, etc. are passed to the program using
> environment variables. While this program is running, the nodes associated with the job will be
> have a POWER_UP/CONFIGURING flag set in their state, which can be readily viewed. The slurmctld
> daemon will wait indefinitely for this program to complete. Once the program completes with an
> exit code of zero, the nodes will be considered ready for use and the program will be started. If
> some node can not be made available for use, the program should drain the node (typically using
> the scontrol command) and terminate with a non-zero exit code. A non-zero exit code will result in
> the job being requeued (where possible) or killed. Note that only batch jobs can be requeued. See
> **Prolog and Epilog Scripts** for more information.
>
> <!-- -->
>
> **PropagatePrioProcess**  
> Controls the scheduling priority (nice value) of user spawned tasks.
>
> > **0**  
> > The tasks will inherit the scheduling priority from the slurm daemon. This is the default value.
> >
> > <!-- -->
> >
> > **1**  
> > The tasks will inherit the scheduling priority of the command used to submit them (e.g. **srun**
> > or **sbatch**). Unless the job is submitted by user root, the tasks will have a scheduling
> > priority no higher than the slurm daemon spawning them.
> >
> > <!-- -->
> >
> > **2**  
> > The tasks will inherit the scheduling priority of the command used to submit them (e.g. **srun**
> > or **sbatch**) with the restriction that their nice value will always be one higher than the
> > slurm daemon (i.e. the tasks scheduling priority will be lower than the slurm daemon).
>
> **PropagateResourceLimits**  
> A comma-separated list of resource limit names. The slurmd daemon uses these names to obtain the
> associated (soft) limit values from the user's process environment on the submit node. These
> limits are then propagated and applied to the jobs that will run on the compute nodes. This
> parameter can be useful when system limits vary among nodes. Any resource limits that do not
> appear in the list are not propagated. However, the user can override this by specifying which
> resource limits to propagate with the sbatch or srun "--propagate" option. If neither
> **PropagateResourceLimits** or **PropagateResourceLimitsExcept** are configured and the
> "--propagate" option is not specified, then the default action is to propagate all limits. Only
> one of the parameters, either PropagateResourceLimits or PropagateResourceLimitsExcept, may be
> specified. The user limits can not exceed hard limits under which the slurmd daemon operates. If
> the user limits are not propagated, the limits from the slurmd daemon will be propagated to the
> user's job. The limits used for the Slurm daemons can be set in the /etc/sysconf/slurm file. For
> more information, see: https://slurm.schedmd.com/faq.html#memlock The following limit names are
> supported by Slurm (although some options may not be supported on some systems):
>
> > **ALL**  
> > All limits listed below (default)
> >
> > <!-- -->
> >
> > **NONE**  
> > No limits listed below
> >
> > <!-- -->
> >
> > **AS**  
> > The maximum address space (virtual memory) for a process.
> >
> > <!-- -->
> >
> > **CORE**  
> > The maximum size of core file
> >
> > <!-- -->
> >
> > **CPU**  
> > The maximum amount of CPU time
> >
> > <!-- -->
> >
> > **DATA**  
> > The maximum size of a process's data segment
> >
> > <!-- -->
> >
> > **FSIZE**  
> > The maximum size of files created. Note that if the user sets FSIZE to less than the current
> > size of the slurmd.log, job launches will fail with a 'File size limit exceeded' error.
> >
> > <!-- -->
> >
> > **MEMLOCK**  
> > The maximum size that may be locked into memory
> >
> > <!-- -->
> >
> > **NOFILE**  
> > The maximum number of open files
> >
> > <!-- -->
> >
> > **NPROC**  
> > The maximum number of processes available
> >
> > <!-- -->
> >
> > **RSS**  
> > The maximum resident set size. Note that this only has effect with Linux kernels 2.4.30 or older
> > or BSD.
> >
> > <!-- -->
> >
> > **STACK**  
> > The maximum stack size
>
> **PropagateResourceLimitsExcept**  
> A comma-separated list of resource limit names. By default, all resource limits will be
> propagated, (as described by the **PropagateResourceLimits** parameter), except for the limits
> appearing in this list. The user can override this by specifying which resource limits to
> propagate with the sbatch or srun "--propagate" option. See **PropagateResourceLimits** above for
> a list of valid limit names.
>
> <!-- -->
>
> **RebootProgram**  
> Program to be executed on each compute node to reboot it. Invoked on each node once it becomes
> idle after the command "scontrol reboot" is executed by an authorized user or a job is submitted
> with the "--reboot" option. After rebooting, the node is returned to normal use. See
> **ResumeTimeout** to configure the time you expect a reboot to finish in. A node will be marked
> DOWN if it doesn't reboot within **ResumeTimeout**.
>
> <!-- -->
>
> **ReconfigFlags**  
> Flags to control various actions that may be taken when an "scontrol reconfig" command is issued.
> Currently the options are:
>
> > **KeepPartInfo**  
> > If set, an "scontrol reconfig" command will maintain the in-memory value of partition "state"
> > and other parameters that may have been dynamically updated by "scontrol update". Partition
> > information in the slurm.conf file will be merged with in-memory data. This flag supersedes the
> > KeepPartState flag.
> >
> > <!-- -->
> >
> > **KeepPartState**  
> > If set, an "scontrol reconfig" command will preserve only the current "state" value of in-memory
> > partitions and will reset all other parameters of the partitions that may have been dynamically
> > updated by "scontrol update" to the values from the slurm.conf file. Partition information in
> > the slurm.conf file will be merged with in-memory data.
> >
> > <!-- -->
> >
> > **KeepPowerSaveSettings**  
> > If set, an "scontrol reconfig" command will preserve the current state of SuspendExcNodes,
> > SuspendExcParts and SuspendExcStates.
>
> > The default for the above flags is not set, and the "scontrol reconfig" will rebuild the
> > partition information using only the definitions in the slurm.conf file.
>
> **RequeueExit**  
> Enables automatic requeue for batch jobs which exit with the specified values. Separate multiple
> exit code by a comma and/or specify numeric ranges using a "-" separator (e.g.
> "RequeueExit=1-9,18") Jobs will be put back in to pending state and later scheduled again.
> Restarted jobs will have the environment variable **SLURM_RESTART_COUNT** set to the number of
> times the job has been restarted.
>
> <!-- -->
>
> **RequeueExitHold**  
> Enables automatic requeue for batch jobs which exit with the specified values, with these jobs
> being held until released manually by the user. Separate multiple exit code by a comma and/or
> specify numeric ranges using a "-" separator (e.g. "RequeueExitHold=10-12,16") These jobs are put
> in the **JOB_SPECIAL_EXIT** exit state. Restarted jobs will have the environment variable
> **SLURM_RESTART_COUNT** set to the number of times the job has been restarted.
>
> <!-- -->
>
> **ResumeFailProgram**  
> The program that will be executed when nodes fail to resume to by **ResumeTimeout**. The argument
> to the program will be the names of the failed nodes (using Slurm's hostlist expression format).
> Programs will be killed if they run longer than the largest configured, global or partition,
> **ResumeTimeout** or **SuspendTimeout**.
>
> <!-- -->
>
> **ResumeProgram**  
> Slurm supports a mechanism to reduce power consumption on nodes that remain idle for an extended
> period of time. This is typically accomplished by reducing voltage and frequency or powering the
> node down. **ResumeProgram** is the program that will be executed when a node in power save mode
> is assigned work to perform. For reasons of reliability, **ResumeProgram** may execute more than
> once for a node when the **slurmctld** daemon crashes and is restarted. If **ResumeProgram** is
> unable to restore a node to service with a responding slurmd and an updated BootTime, it should
> set the node state to DOWN, which will result in a requeue of any job associated with the node -
> this will happen automatically if the node doesn't register within ResumeTimeout. If the node
> isn't actually rebooted (i.e. when multiple-slurmd is configured) starting slurmd with "-b" option
> might be useful. The program executes as **SlurmUser**. The argument to the program will be the
> names of nodes to be removed from power savings mode (using Slurm's hostlist expression format). A
> job to node mapping is available in JSON format by reading the temporary file specified by the
> **SLURM_RESUME_FILE** environment variable. This file is closed once slurmctld shuts down. If
> ResumeProgram is running, slurmctld shutdown is delayed by up to ten seconds to give ResumeProgram
> time to read this file. Therefore, this file should be read at the beginning of ResumeProgram. By
> default no program is run. Programs will be killed if they run longer than the largest configured,
> global or partition, **ResumeTimeout** or **SuspendTimeout**.
>
> <!-- -->
>
> **ResumeRate**  
> The rate at which nodes in power save mode are returned to normal operation by **ResumeProgram**.
> The value is a number of nodes per minute and it can be used to prevent power surges if a large
> number of nodes in power save mode are assigned work at the same time (e.g. a large job starts). A
> value of zero results in no limits being imposed. The default value is 300 nodes per minute.
>
> <!-- -->
>
> **ResumeTimeout**  
> Maximum time permitted (in seconds) between when a node resume request is issued and when the node
> is actually available for use. Nodes which fail to respond in this time frame will be marked DOWN
> and the jobs scheduled on the node requeued. Nodes which reboot after this time frame will be
> marked DOWN with a reason of "Node unexpectedly rebooted." The default value is 60 seconds.
>
> <!-- -->
>
> **ResvEpilog**  
> Fully qualified pathname of a program for the slurmctld to execute when a reservation ends. The
> program can be used to cancel jobs, modify partition configuration, etc. The reservation named
> will be passed as an argument to the program. By default there is no epilog.
>
> <!-- -->
>
> **ResvOverRun**  
> Describes how long a job already running in a reservation should be permitted to execute after the
> end time of the reservation has been reached. The time period is specified in minutes and the
> default value is 0 (kill the job immediately). The value may not exceed 65533 minutes, although a
> value of "UNLIMITED" is supported to permit a job to run indefinitely after its reservation is
> terminated.
>
> <!-- -->
>
> **ResvProlog**  
> Fully qualified pathname of a program for the slurmctld to execute when a reservation begins. The
> program can be used to cancel jobs, modify partition configuration, etc. The reservation named
> will be passed as an argument to the program. By default there is no prolog.
>
> <!-- -->
>
> **ReturnToService**  
> Controls when a DOWN node will be returned to service. The default value is 0. Supported values
> include
>
> > **0**  
> > A node will remain in the DOWN state until a system administrator explicitly changes its state
> > (even if the slurmd daemon registers and resumes communications).
> >
> > <!-- -->
> >
> > **1**  
> > A DOWN node will become available for use upon registration with a valid configuration only if
> > it was set DOWN due to being non-responsive. If the node was set DOWN for any other reason (low
> > memory, unexpected reboot, etc.), its state will not automatically be changed. A node registers
> > with a valid configuration if its memory, GRES, CPU count, etc. are equal to or greater than the
> > values configured in slurm.conf.
> >
> > <!-- -->
> >
> > **2**  
> > A DOWN node will become available for use upon registration with a valid configuration. The node
> > could have been set DOWN for any reason. A node registers with a valid configuration if its
> > memory, GRES, CPU count, etc. are equal to or greater than the values configured in slurm.conf.
>
> **RoutePlugin**  
> Identifies the plugin to be used for defining which nodes will be used for message forwarding.
>
> > **route/default**  
> > default, use TreeWidth.
> >
> > <!-- -->
> >
> > **route/topology**  
> > use the switch hierarchy defined in a *topology.conf* file. TopologyPlugin=topology/tree is
> > required.
>
> **SchedulerParameters**  
> The interpretation of this parameter varies by **SchedulerType**. Multiple options may be comma
> separated.
>
> > **allow_zero_lic**  
> > If set, then job submissions requesting more than configured licenses won't be rejected.
> >
> > <!-- -->
> >
> > **assoc_limit_stop**  
> > If set and a job cannot start due to association limits, then do not attempt to initiate any
> > lower priority jobs in that partition. Setting this can decrease system throughput and
> > utilization, but avoid potentially starving larger jobs by preventing them from launching
> > indefinitely.
> >
> > <!-- -->
> >
> > **batch_sched_delay=#**  
> > How long, in seconds, the scheduling of batch jobs can be delayed. This can be useful in a
> > high-throughput environment in which batch jobs are submitted at a very high rate (i.e. using
> > the sbatch command) and one wishes to reduce the overhead of attempting to schedule each job at
> > submit time. The default value is 3 seconds.
> >
> > <!-- -->
> >
> > **bb_array_stage_cnt=#**  
> > Number of tasks from a job array that should be available for burst buffer resource allocation.
> > Higher values will increase the system overhead as each task from the job array will be moved to
> > its own job record in memory, so relatively small values are generally recommended. The default
> > value is 10.
> >
> > <!-- -->
> >
> > **bf_busy_nodes**  
> > When selecting resources for pending jobs to reserve for future execution (i.e. the job can not
> > be started immediately), then preferentially select nodes that are in use. This will tend to
> > leave currently idle resources available for backfilling longer running jobs, but may result in
> > allocations having less than optimal network topology. This option is currently only supported
> > by the select/cons_res and select/cons_tres plugins (or select/cray_aries with
> > SelectTypeParameters set to "OTHER_CONS_RES" or "OTHER_CONS_TRES", which layers the
> > select/cray_aries plugin over the select/cons_res or select/cons_tres plugin respectively).
> >
> > <!-- -->
> >
> > **bf_continue**  
> > The backfill scheduler periodically releases locks in order to permit other operations to
> > proceed rather than blocking all activity for what could be an extended period of time. Setting
> > this option will cause the backfill scheduler to continue processing pending jobs from its
> > original job list after releasing locks even if job or node state changes.
> >
> > <!-- -->
> >
> > **bf_hetjob_immediate**  
> > Instruct the backfill scheduler to attempt to start a heterogeneous job as soon as all of its
> > components are determined able to do so. Otherwise, the backfill scheduler will delay
> > heterogeneous jobs initiation attempts until after the rest of the queue has been processed.
> > This delay may result in lower priority jobs being allocated resources, which could delay the
> > initiation of the heterogeneous job due to account and/or QOS limits being reached. This option
> > is disabled by default. If enabled and **bf_hetjob_prio=min** is not set, then it would be
> > automatically set.
> >
> > <!-- -->
> >
> > **bf_hetjob_prio=\[min\|avg\|max\]**  
> > At the beginning of each backfill scheduling cycle, a list of pending to be scheduled jobs is
> > sorted according to the precedence order configured in **PriorityType**. This option instructs
> > the scheduler to alter the sorting algorithm to ensure that all components belonging to the same
> > heterogeneous job will be attempted to be scheduled consecutively (thus not fragmented in the
> > resulting list). More specifically, all components from the same heterogeneous job will be
> > treated as if they all have the same priority (minimum, average or maximum depending upon this
> > option's parameter) when compared with other jobs (or other heterogeneous job components). The
> > original order will be preserved within the same heterogeneous job. Note that the operation is
> > calculated for the **PriorityTier** layer and for the **Priority** resulting from the
> > priority/multifactor plugin calculations. When enabled, if any heterogeneous job requested an
> > advanced reservation, then all of that job's components will be treated as if they had requested
> > an advanced reservation (and get preferential treatment in scheduling).
> >
> > Note that this operation does not update the **Priority** values of the heterogeneous job
> > components, only their order within the list, so the output of the sprio command will not be
> > effected.
> >
> > Heterogeneous jobs have special scheduling properties: they are only scheduled by the backfill
> > scheduling plugin, each of their components is considered separately when reserving resources
> > (and might have different **PriorityTier** or different **Priority** values), and no
> > heterogeneous job component is actually allocated resources until all if its components can be
> > initiated. This may imply potential scheduling deadlock scenarios because components from
> > different heterogeneous jobs can start reserving resources in an interleaved fashion (not
> > consecutively), but none of the jobs can reserve resources for all components and start.
> > Enabling this option can help to mitigate this problem. By default, this option is disabled.
> >
> > <!-- -->
> >
> > **bf_interval=#**  
> > The number of seconds between backfill iterations. Higher values result in less overhead and
> > better responsiveness. This option applies only to **SchedulerType=sched/backfill**. Default:
> > 30, Min: 1, Max: 10800 (3h). A setting of -1 will disable the backfill scheduling loop.
> >
> > <!-- -->
> >
> > **bf_job_part_count_reserve=#**  
> > The backfill scheduling logic will reserve resources for the specified count of highest priority
> > jobs in each partition. For example, bf_job_part_count_reserve=10 will cause the backfill
> > scheduler to reserve resources for the ten highest priority jobs in each partition. Any lower
> > priority job that can be started using currently available resources and not adversely impact
> > the expected start time of these higher priority jobs will be started by the backfill scheduler
> > The default value is zero, which will reserve resources for any pending job and delay initiation
> > of lower priority jobs. Also see bf_min_age_reserve and bf_min_prio_reserve. Default: 0, Min: 0,
> > Max: 100000.
> >
> > <!-- -->
> >
> > **bf_licenses**  
> > Require the backfill scheduling logic to track and plan for license availability. By default,
> > any job blocked on license availability will not have resources reserved which can lead to job
> > starvation. This option implicitly enables **bf_running_job_reserve**.
> >
> > <!-- -->
> >
> > **bf_max_job_array_resv=#**  
> > The maximum number of tasks from a job array for which the backfill scheduler will reserve
> > resources in the future. Since job arrays can potentially have millions of tasks, the overhead
> > in reserving resources for all tasks can be prohibitive. In addition various limits may prevent
> > all the jobs from starting at the expected times. This has no impact upon the number of tasks
> > from a job array that can be started immediately, only those tasks expected to start at some
> > future time. Default: 20, Min: 0, Max: 1000. **NOTE**: Jobs submitted to multiple partitions
> > appear in the job queue once per partition. If different copies of a single job array record
> > aren't consecutive in the job queue and another job array record is in between, then
> > bf_max_job_array_resv tasks are considered per partition that the job is submitted to.
> >
> > <!-- -->
> >
> > **bf_max_job_assoc=#**  
> > The maximum number of jobs per user association to attempt starting with the backfill scheduler.
> > This setting is similar to **bf_max_job_user** but is handy if a user has multiple associations
> > equating to basically different users. One can set this limit to prevent users from flooding the
> > backfill queue with jobs that cannot start and that prevent jobs from other users to start. This
> > option applies only to **SchedulerType=sched/backfill**. Also see the **bf_max_job_user**
> > **bf_max_job_part**, **bf_max_job_test** and **bf_max_job_user_part=#** options. Set
> > **bf_max_job_test** to a value much higher than **bf_max_job_assoc**. Default: 0 (no limit),
> > Min: 0, Max: bf_max_job_test.
> >
> > <!-- -->
> >
> > **bf_max_job_part=#**  
> > The maximum number of jobs per partition to attempt starting with the backfill scheduler. This
> > can be especially helpful for systems with large numbers of partitions and jobs. This option
> > applies only to **SchedulerType=sched/backfill**. Also see the **partition_job_depth** and
> > **bf_max_job_test** options. Set **bf_max_job_test** to a value much higher than
> > **bf_max_job_part**. Default: 0 (no limit), Min: 0, Max: bf_max_job_test.
> >
> > <!-- -->
> >
> > **bf_max_job_start=#**  
> > The maximum number of jobs which can be initiated in a single iteration of the backfill
> > scheduler. This option applies only to **SchedulerType=sched/backfill**. Default: 0 (no limit),
> > Min: 0, Max: 10000.
> >
> > <!-- -->
> >
> > **bf_max_job_test=#**  
> > The maximum number of jobs to attempt backfill scheduling for (i.e. the queue depth). Higher
> > values result in more overhead and less responsiveness. Until an attempt is made to backfill
> > schedule a job, its expected initiation time value will not be set. In the case of large
> > clusters, configuring a relatively small value may be desirable. This option applies only to
> > **SchedulerType=sched/backfill**. Default: 500, Min: 1, Max: 1,000,000.
> >
> > <!-- -->
> >
> > **bf_max_job_user=#**  
> > The maximum number of jobs per user to attempt starting with the backfill scheduler for ALL
> > partitions. One can set this limit to prevent users from flooding the backfill queue with jobs
> > that cannot start and that prevent jobs from other users to start. This is similar to the
> > MAXIJOB limit in Maui. This option applies only to **SchedulerType=sched/backfill**. Also see
> > the **bf_max_job_part**, **bf_max_job_test** and **bf_max_job_user_part=#** options. Set
> > **bf_max_job_test** to a value much higher than **bf_max_job_user**. Default: 0 (no limit), Min:
> > 0, Max: bf_max_job_test.
> >
> > <!-- -->
> >
> > **bf_max_job_user_part=#**  
> > The maximum number of jobs per user per partition to attempt starting with the backfill
> > scheduler for any single partition. This option applies only to
> > **SchedulerType=sched/backfill**. Also see the **bf_max_job_part**, **bf_max_job_test** and
> > **bf_max_job_user=#** options. Default: 0 (no limit), Min: 0, Max: bf_max_job_test.
> >
> > <!-- -->
> >
> > **bf_max_time=#**  
> > The maximum time in seconds the backfill scheduler can spend (including time spent sleeping when
> > locks are released) before discontinuing, even if maximum job counts have not been reached. This
> > option applies only to **SchedulerType=sched/backfill**. The default value is the value of
> > bf_interval (which defaults to 30 seconds). Default: bf_interval value (def. 30 sec), Min: 1,
> > Max: 3600 (1h). **NOTE**: If bf_interval is short and bf_max_time is large, this may cause locks
> > to be acquired too frequently and starve out other serviced RPCs. It's advisable if using this
> > parameter to set max_rpc_cnt high enough that scheduling isn't always disabled, and low enough
> > that the interactive workload can get through in a reasonable period of time. max_rpc_cnt needs
> > to be below 256 (the default RPC thread limit). Running around the middle (150) may give you
> > good results. **NOTE**: When increasing the amount of time spent in the backfill scheduling
> > cycle, Slurm can be prevented from responding to client requests in a timely manner. To address
> > this you can use **max_rpc_cnt** to specify a number of queued RPCs before the scheduler stops
> > to respond to these requests.
> >
> > <!-- -->
> >
> > **bf_min_age_reserve=#**  
> > The backfill and main scheduling logic will not reserve resources for pending jobs until they
> > have been pending and runnable for at least the specified number of seconds. In addition, jobs
> > waiting for less than the specified number of seconds will not prevent a newly submitted job
> > from starting immediately, even if the newly submitted job has a lower priority. This can be
> > valuable if jobs lack time limits or all time limits have the same value. The default value is
> > zero, which will reserve resources for any pending job and delay initiation of lower priority
> > jobs. Also see bf_job_part_count_reserve and bf_min_prio_reserve. Default: 0, Min: 0, Max:
> > 2592000 (30 days).
> >
> > <!-- -->
> >
> > **bf_min_prio_reserve=#**  
> > The backfill and main scheduling logic will not reserve resources for pending jobs unless they
> > have a priority equal to or higher than the specified value. In addition, jobs with a lower
> > priority will not prevent a newly submitted job from starting immediately, even if the newly
> > submitted job has a lower priority. This can be valuable if one wished to maximize system
> > utilization without regard for job priority below a certain threshold. The default value is
> > zero, which will reserve resources for any pending job and delay initiation of lower priority
> > jobs. Also see bf_job_part_count_reserve and bf_min_age_reserve. Default: 0, Min: 0, Max: 2^63.
> >
> > <!-- -->
> >
> > **bf_node_space_size=#**  
> > Size of backfill node_space table. Adding a single job to backfill reservations in the worst
> > case can consume two node_space records. In the case of large clusters, configuring a relatively
> > small value may be desirable. This option applies only to **SchedulerType=sched/backfill**. Also
> > see bf_max_job_test and bf_running_job_reserve. Default: bf_max_job_test, Min: 2, Max:
> > 2,000,000.
> >
> > <!-- -->
> >
> > **bf_one_resv_per_job**  
> > Disallow adding more than one backfill reservation per job. The scheduling logic builds a sorted
> > list of job-partition pairs. Jobs submitted to multiple partitions have as many entries in the
> > list as requested partitions. By default, the backfill scheduler may evaluate all the
> > job-partition entries for a single job, potentially reserving resources for each pair, but only
> > starting the job in the reservation offering the earliest start time. Having a single job
> > reserving resources for multiple partitions could impede other jobs (or hetjob components) from
> > reserving resources already reserved for the partitions that don't offer the earliest start
> > time. A single job that requests multiple partitions can also prevent itself from starting
> > earlier in a lower priority partition if the partitions overlap nodes and a backfill reservation
> > in the higher priority partition blocks nodes that are also in the lower priority partition.
> > This option makes it so that a job submitted to multiple partitions will stop reserving
> > resources once the first job-partition pair has booked a backfill reservation. Subsequent pairs
> > from the same job will only be tested to start now. This allows for other jobs to be able to
> > book the other pairs resources at the cost of not guaranteeing that the multi partition job will
> > start in the partition offering the earliest start time (unless it can start immediately). This
> > option is disabled by default.
> >
> > <!-- -->
> >
> > **bf_resolution=#**  
> > The number of seconds in the resolution of data maintained about when jobs begin and end. Higher
> > values result in better responsiveness and quicker backfill cycles by using larger blocks of
> > time to determine node eligibility. However, higher values lead to less efficient system
> > planning, and may miss opportunities to improve system utilization. This option applies only to
> > **SchedulerType=sched/backfill**. Default: 60, Min: 1, Max: 3600 (1 hour).
> >
> > <!-- -->
> >
> > **bf_running_job_reserve**  
> > Add an extra step to backfill logic, which creates backfill reservations for jobs running on
> > whole nodes. This option is disabled by default.
> >
> > <!-- -->
> >
> > **bf_window=#**  
> > The number of minutes into the future to look when considering jobs to schedule. Higher values
> > result in more overhead and less responsiveness. A value at least as long as the highest allowed
> > time limit is generally advisable to prevent job starvation. In order to limit the amount of
> > data managed by the backfill scheduler, if the value of **bf_window** is increased, then it is
> > generally advisable to also increase **bf_resolution**. This option applies only to
> > **SchedulerType=sched/backfill**. Default: 1440 (1 day), Min: 1, Max: 43200 (30 days).
> >
> > <!-- -->
> >
> > **bf_window_linear=#**  
> > For performance reasons, the backfill scheduler will decrease precision in calculation of job
> > expected termination times. By default, the precision starts at 30 seconds and that time
> > interval doubles with each evaluation of currently executing jobs when trying to determine when
> > a pending job can start. This algorithm can support an environment with many thousands of
> > running jobs, but can result in the expected start time of pending jobs being gradually being
> > deferred due to lack of precision. A value for bf_window_linear will cause the time interval to
> > be increased by a constant amount on each iteration. The value is specified in units of seconds.
> > For example, a value of 60 will cause the backfill scheduler on the first iteration to identify
> > the job ending soonest and determine if the pending job can be started after that job plus all
> > other jobs expected to end within 30 seconds (default initial value) of the first job. On the
> > next iteration, the pending job will be evaluated for starting after the next job expected to
> > end plus all jobs ending within 90 seconds of that time (30 second default, plus the 60 second
> > option value). The third iteration will have a 150 second window and the fourth 210 seconds.
> > Without this option, the time windows will double on each iteration and thus be 30, 60, 120, 240
> > seconds, etc. The use of bf_window_linear is not recommended with more than a few hundred
> > simultaneously executing jobs.
> >
> > <!-- -->
> >
> > **bf_yield_interval=#**  
> > The backfill scheduler will periodically relinquish locks in order for other pending operations
> > to take place. This specifies the times when the locks are relinquished in microseconds. Smaller
> > values may be helpful for high throughput computing when used in conjunction with the
> > **bf_continue** option. Also see the **bf_yield_sleep** option. Default: 2,000,000 (2 sec), Min:
> > 1, Max: 10,000,000 (10 sec).
> >
> > <!-- -->
> >
> > **bf_yield_sleep=#**  
> > The backfill scheduler will periodically relinquish locks in order for other pending operations
> > to take place. This specifies the length of time for which the locks are relinquished in
> > microseconds. Also see the **bf_yield_interval** option. Default: 500,000 (0.5 sec), Min: 1,
> > Max: 10,000,000 (10 sec).
> >
> > <!-- -->
> >
> > **build_queue_timeout=#**  
> > Defines the maximum time that can be devoted to building a queue of jobs to be tested for
> > scheduling. If the system has a huge number of jobs with dependencies, just building the job
> > queue can take so much time as to adversely impact overall system performance and this parameter
> > can be adjusted as needed. The default value is 2,000,000 microseconds (2 seconds).
> >
> > <!-- -->
> >
> > **correspond_after_task_cnt=#**  
> > Defines the number of array tasks that get split for potential aftercorr dependency check. Low
> > number may result in dependent task check failures when the job one depends on gets purged
> > before the split. Default: 10.
> >
> > <!-- -->
> >
> > **default_queue_depth=#**  
> > The default number of jobs to attempt scheduling (i.e. the queue depth) when a running job
> > completes or other routine actions occur, however the frequency with which the scheduler is run
> > may be limited by using the **defer** or **sched_min_interval** parameters described below. The
> > full queue will be tested on a less frequent basis as defined by the **sched_interval** option
> > described below. The default value is 100. See the **partition_job_depth** option to limit depth
> > by partition.
> >
> > <!-- -->
> >
> > **defer**  
> > Setting this option will avoid attempting to schedule each job individually at job submit time,
> > but defer it until a later time when scheduling multiple jobs simultaneously may be possible.
> > This option may improve system responsiveness when large numbers of jobs (many hundreds) are
> > submitted at the same time, but it will delay the initiation time of individual jobs. Also see
> > **default_queue_depth** above.
> >
> > <!-- -->
> >
> > **defer_batch**  
> > Like **defer**, but only will defer scheduling for batch jobs. Interactive allocations from
> > salloc/srun will still attempt to schedule immediately upon submission.
> >
> > <!-- -->
> >
> > **delay_boot=#**  
> > Do not reboot nodes in order to satisfied this job's feature specification if the job has been
> > eligible to run for less than this time period. If the job has waited for less than the
> > specified period, it will use only nodes which already have the specified features. The argument
> > is in units of minutes. Individual jobs may override this default value with the
> > **--delay-boot** option.
> >
> > <!-- -->
> >
> > **disable_job_shrink**  
> > Deny user requests to shrink the size of running jobs. (However, running jobs may still shrink
> > due to node failure if the --no-kill option was set.)
> >
> > <!-- -->
> >
> > **disable_hetjob_steps**  
> > Disable job steps that span heterogeneous job allocations.
> >
> > <!-- -->
> >
> > **enable_hetjob_steps**  
> > Enable job steps that span heterogeneous job allocations. The default value.
> >
> > <!-- -->
> >
> > **enable_user_top**  
> > Enable use of the "scontrol top" command by non-privileged users.
> >
> > <!-- -->
> >
> > **Ignore_NUMA**  
> > Some processors (e.g. AMD Opteron 6000 series) contain multiple NUMA nodes per socket. This is a
> > configuration which does not map into the hardware entities that Slurm optimizes resource
> > allocation for (PU/thread, core, socket, baseboard, node and network switch). In order to
> > optimize resource allocations on such hardware, Slurm will consider each NUMA node within the
> > socket as a separate socket by default. Use the Ignore_NUMA option to report the correct socket
> > count, but **not** optimize resource allocations on the NUMA nodes.
> >
> > **NOTE**: Since hwloc 2.0 NUMA Nodes are are not part of the main/CPU topology tree, because of
> > that if Slurm is build with hwloc 2.0 or above Slurm will treat HWLOC_OBJ_PACKAGE as Socket, you
> > can change this behavior using **SlurmdParameters**=l3cache_as_socket.
> >
> > **ignore_prefer_validation**  
> > If set, and a job requests --prefer any features in the request that would create an invalid
> > request with the current system will not generate an error. This is helpful for dynamic systems
> > where nodes with features come and go. Please note using this option will not protect you from
> > typos.
> >
> > <!-- -->
> >
> > **max_array_tasks**  
> > Specify the maximum number of tasks that can be included in a job array. The default limit is
> > MaxArraySize, but this option can be used to set a lower limit. For example,
> > max_array_tasks=1000 and MaxArraySize=100001 would permit a maximum task ID of 100000, but limit
> > the number of tasks in any single job array to 1000.
> >
> > <!-- -->
> >
> > **max_rpc_cnt=#**  
> > If the number of active threads in the slurmctld daemon is equal to or larger than this value,
> > defer scheduling of jobs. The scheduler will check this condition at certain points in code and
> > yield locks if necessary. This can improve Slurm's ability to process requests at a cost of
> > initiating new jobs less frequently. Default: 0 (option disabled), Min: 0, Max: 1000.
> >
> > > **NOTE**: The maximum number of threads (MAX_SERVER_THREADS) is internally set to 256 and
> > > defines the number of served RPCs at a given time. Setting max_rpc_cnt to more than 256 will
> > > be only useful to let backfill continue scheduling work after locks have been yielded (i.e.
> > > each 2 seconds) if there are a maximum of MAX(max_rpc_cnt/10, 20) RPCs in the queue. i.e.
> > > max_rpc_cnt=1000, the scheduler will be allowed to continue after yielding locks only when
> > > there are less than or equal to 100 pending RPCs. If a value is set, then a value of 10 or
> > > higher is recommended. It may require some tuning for each system, but needs to be high enough
> > > that scheduling isn't always disabled, and low enough that requests can get through in a
> > > reasonable period of time.
> >
> > **max_sched_time=#**  
> > How long, in seconds, that the main scheduling loop will execute for before exiting. If a value
> > is configured, be aware that all other Slurm operations will be deferred during this time
> > period. Make certain the value is lower than **MessageTimeout**. If a value is not explicitly
> > configured, the default value is half of **MessageTimeout** with a minimum default value of 1
> > second and a maximum default value of 2 seconds. For example if MessageTimeout=10, the time
> > limit will be 2 seconds (i.e. MIN(10/2, 2) = 2).
> >
> > <!-- -->
> >
> > **max_script_size=#**  
> > Specify the maximum size of a batch script, in bytes. The default value is 4 megabytes. Larger
> > values may adversely impact system performance.
> >
> > <!-- -->
> >
> > **max_switch_wait=#**  
> > Maximum number of seconds that a job can delay execution waiting for the specified desired
> > switch count. The default value is 300 seconds.
> >
> > <!-- -->
> >
> > **no_backup_scheduling**  
> > If used, the backup controller will not schedule jobs when it takes over. The backup controller
> > will allow jobs to be submitted, modified and cancelled but won't schedule new jobs. This is
> > useful in Cray environments when the backup controller resides on an external Cray node. A
> > restart of slurmctld is required for changes to this parameter to take effect.
> >
> > <!-- -->
> >
> > **no_env_cache**  
> > If used, any job started on node that fails to load the env from a node will fail instead of
> > using the cached env. This will also implicitly imply the requeue_setup_env_fail option as well.
> >
> > <!-- -->
> >
> > **nohold_on_prolog_fail**  
> > By default, if the Prolog exits with a non-zero value the job is requeued in a held state. By
> > specifying this parameter the job will be requeued but not held so that the scheduler can
> > dispatch it to another host.
> >
> > <!-- -->
> >
> > **pack_serial_at_end**  
> > If used with the select/cons_res or select/cons_tres plugin, then put serial jobs at the end of
> > the available nodes rather than using a best fit algorithm. This may reduce resource
> > fragmentation for some workloads.
> >
> > <!-- -->
> >
> > **partition_job_depth=#**  
> > The default number of jobs to attempt scheduling (i.e. the queue depth) from each
> > partition/queue in Slurm's main scheduling logic. The functionality is similar to that provided
> > by the **bf_max_job_part** option for the backfill scheduling logic. The default value is 0 (no
> > limit). Job's excluded from attempted scheduling based upon partition will not be counted
> > against the **default_queue_depth** limit. Also see the **bf_max_job_part** option.
> >
> > <!-- -->
> >
> > **reduce_completing_frag**  
> > This option is used to control how scheduling of resources is performed when jobs are in the
> > COMPLETING state, which influences potential fragmentation. If this option is not set then no
> > jobs will be started in any partition when any job is in the COMPLETING state for less than
> > **CompleteWait** seconds. If this option is set then no jobs will be started in any individual
> > partition that has a job in COMPLETING state for less than **CompleteWait** seconds. In
> > addition, no jobs will be started in any partition with nodes that overlap with any nodes in the
> > partition of the completing job. This option is to be used in conjunction with **CompleteWait**.
> >
> > **NOTE**: **CompleteWait** must be set in order for this to work. If **CompleteWait=0** then
> > this option does nothing.
> >
> > **NOTE**: **reduce_completing_frag** only affects the main scheduler, not the backfill
> > scheduler.
> >
> > <!-- -->
> >
> > **requeue_setup_env_fail**  
> > By default if a job environment setup fails the job keeps running with a limited environment. By
> > specifying this parameter the job will be requeued in held state and the execution node drained.
> >
> > <!-- -->
> >
> > **salloc_wait_nodes**  
> > If defined, the salloc command will wait until all allocated nodes are ready for use (i.e.
> > booted) before the command returns. By default, salloc will return as soon as the resource
> > allocation has been made.
> >
> > <!-- -->
> >
> > **sbatch_wait_nodes**  
> > If defined, the sbatch script will wait until all allocated nodes are ready for use (i.e.
> > booted) before the initiation. By default, the sbatch script will be initiated as soon as the
> > first node in the job allocation is ready. The sbatch command can use the --wait-all-nodes
> > option to override this configuration parameter.
> >
> > <!-- -->
> >
> > **sched_interval=#**  
> > How frequently, in seconds, the main scheduling loop will execute and test all pending jobs. The
> > default value is 60 seconds. A setting of -1 will disable the main scheduling loop.
> >
> > <!-- -->
> >
> > **sched_max_job_start=#**  
> > The maximum number of jobs that the main scheduling logic will start in any single execution.
> > The default value is zero, which imposes no limit.
> >
> > <!-- -->
> >
> > **sched_min_interval=#**  
> > How frequently, in microseconds, the main scheduling loop will execute and test any pending
> > jobs. The scheduler runs in a limited fashion every time that any event happens which could
> > enable a job to start (e.g. job submit, job terminate, etc.). If these events happen at a high
> > frequency, the scheduler can run very frequently and consume significant resources if not
> > throttled by this option. This option specifies the minimum time between the end of one
> > scheduling cycle and the beginning of the next scheduling cycle. A value of zero will disable
> > throttling of the scheduling logic interval. The default value is 2 microseconds.
> >
> > <!-- -->
> >
> > **spec_cores_first**  
> > Specialized cores will be selected from the first cores of the first sockets, cycling through
> > the sockets on a round robin basis. By default, specialized cores will be selected from the last
> > cores of the last sockets, cycling through the sockets on a round robin basis.
> >
> > <!-- -->
> >
> > **step_retry_count=#**  
> > When a step completes and there are steps ending resource allocation, then retry step
> > allocations for at least this number of pending steps. Also see **step_retry_time**. The default
> > value is 8 steps.
> >
> > <!-- -->
> >
> > **step_retry_time=#**  
> > When a step completes and there are steps ending resource allocation, then retry step
> > allocations for all steps which have been pending for at least this number of seconds. Also see
> > **step_retry_count**. The default value is 60 seconds.
> >
> > <!-- -->
> >
> > **whole_hetjob**  
> > Requests to cancel, hold or release any component of a heterogeneous job will be applied to all
> > components of the job.
> >
> > **NOTE**: This option was previously named whole_pack and this is still supported for backwards
> > compatibility.
>
> **SchedulerTimeSlice**  
> Number of seconds in each time slice when gang scheduling is enabled
> (**PreemptMode=SUSPEND,GANG**). The value must be between 5 seconds and 65533 seconds. The default
> value is 30 seconds.
>
> <!-- -->
>
> **SchedulerType**  
> Identifies the type of scheduler to be used. A restart of slurmctld is required for changes to
> this parameter to take effect. The **scontrol** command can be used to manually change job
> priorities if desired. Acceptable values include:
>
> > **sched/backfill**  
> > For a backfill scheduling module to augment the default FIFO scheduling. Backfill scheduling
> > will initiate lower-priority jobs if doing so does not delay the expected initiation time of any
> > higher priority job. Effectiveness of backfill scheduling is dependent upon users specifying job
> > time limits, otherwise all jobs will have the same time limit and backfilling is impossible.
> > Note documentation for the **SchedulerParameters** option above. This is the default
> > configuration.
> >
> > <!-- -->
> >
> > **sched/builtin**  
> > This is the FIFO scheduler which initiates jobs in priority order. If any job in the partition
> > can not be scheduled, no lower priority job in that partition will be scheduled. An exception is
> > made for jobs that can not run due to partition constraints (e.g. the time limit) or
> > down/drained nodes. In that case, lower priority jobs can be initiated and not impact the higher
> > priority job.
>
> **ScronParameters**  
> Multiple options may be comma separated.
>
> > **enable**  
> > Enable the use of scrontab to submit and manage periodic repeating jobs.
> >
> > <!-- -->
> >
> > **explicit_scancel**  
> > When cancelling an scrontab job, require the user to explicitly request cancelling the job with
> > the --cron flag in scancel.
>
> **SelectType**  
> Identifies the type of resource selection algorithm to be used. A restart of slurmctld and slurmd
> is required for changes to this parameter to take effect. When changed, all job information
> (running and pending) will be lost, since the job state save format used by each plugin is
> different. The only exception to this is when changing from cons_res to cons_tres or from
> cons_tres to cons_res. However, if a job contains cons_tres-specific features and then SelectType
> is changed to cons_res, the job will be canceled, since there is no way for cons_res to satisfy
> requirements specific to cons_tres.
>
> Acceptable values include
>
> > **select/cons_res**  
> > The resources (cores and memory) within a node are individually allocated as consumable
> > resources. Note that whole nodes can be allocated to jobs for selected partitions by using the
> > *OverSubscribe=Exclusive* option. See the partition **OverSubscribe** parameter for more
> > information.
> >
> > <!-- -->
> >
> > **select/cons_tres**  
> > The resources (cores, memory, GPUs and all other trackable resources) within a node are
> > individually allocated as consumable resources. Note that whole nodes can be allocated to jobs
> > for selected partitions by using the *OverSubscribe=Exclusive* option. See the partition
> > **OverSubscribe** parameter for more information.
> >
> > <!-- -->
> >
> > **select/cray_aries**  
> > for a Cray system. The default value is "select/cray_aries" for all Cray systems.
> >
> > <!-- -->
> >
> > **select/linear**  
> > for allocation of entire nodes assuming a one-dimensional array of nodes in which sequentially
> > ordered nodes are preferable. For a heterogeneous cluster (e.g. different CPU counts on the
> > various nodes), resource allocations will favor nodes with high CPU counts as needed based upon
> > the job's node and CPU specification if **TopologyPlugin=topology/none** is configured. Use of
> > other topology plugins with select/linear and heterogeneous nodes is not recommended and may
> > result in valid job allocation requests being rejected. The linear plugin is not designed to
> > track generic resources on a node. In cases where generic resources (such as GPUs) need to be
> > tracked, the cons_res or cons_tres plugins should be used instead. This is the default value.
>
> **SelectTypeParameters**  
> The permitted values of **SelectTypeParameters** depend upon the configured value of
> **SelectType**. The only supported options for **SelectType=select/linear** are
> **CR_ONE_TASK_PER_CORE** and **CR_Memory**, which treats memory as a consumable resource and
> prevents memory over subscription with job preemption or gang scheduling. By default
> **SelectType=select/linear** allocates whole nodes to jobs without considering their memory
> consumption. By default **SelectType=select/cons_res**, **SelectType=select/cray_aries**, and
> **SelectType=select/cons_tres**, use **CR_Core_Memory**, which allocates Core to jobs with
> considering their memory consumption.
>
> A restart of slurmctld is required for changes to this parameter to take effect.
>
> The following options are supported for **SelectType=select/cray_aries**:
>
> > **OTHER_CONS_RES**  
> > Layer the select/cons_res plugin under the select/cray_aries plugin, the default is to layer on
> > select/linear. This also allows all the options available for **SelectType=select/cons_res**.
> >
> > <!-- -->
> >
> > **OTHER_CONS_TRES**  
> > Layer the select/cons_tres plugin under the select/cray_aries plugin, the default is to layer on
> > select/linear. This also allows all the options available for **SelectType=select/cons_tres**.
>
> The following options are supported by the **SelectType=select/cons_res** and
> **SelectType=select/cons_tres** plugins:
>
> > **CR_CPU**  
> > CPUs are consumable resources. Configure the number of **CPUs** on each node, which may be equal
> > to the count of cores or hyper-threads on the node depending upon the desired minimum resource
> > allocation. The node's **Boards**, **Sockets**, **CoresPerSocket** and **ThreadsPerCore** may
> > optionally be configured and result in job allocations which have improved locality; however
> > doing so will prevent more than one job from being allocated on each core.
> >
> > <!-- -->
> >
> > **CR_CPU_Memory**  
> > CPUs and memory are consumable resources. Configure the number of **CPUs** on each node, which
> > may be equal to the count of cores or hyper-threads on the node depending upon the desired
> > minimum resource allocation. The node's **Boards**, **Sockets**, **CoresPerSocket** and
> > **ThreadsPerCore** may optionally be configured and result in job allocations which have
> > improved locality; however doing so will prevent more than one job from being allocated on each
> > core. Setting a value for **DefMemPerCPU** is strongly recommended.
> >
> > <!-- -->
> >
> > **CR_Core**  
> > Cores are consumable resources. On nodes with hyper-threads, each thread is counted as a CPU to
> > satisfy a job's resource requirement, but multiple jobs are not allocated threads on the same
> > core. The count of CPUs allocated to a job is rounded up to account for every CPU on an
> > allocated core. This will also impact total allocated memory when --mem-per-cpu is used to be
> > multiply of total number of CPUs on allocated cores.
> >
> > <!-- -->
> >
> > **CR_Core_Memory**  
> > Cores and memory are consumable resources. On nodes with hyper-threads, each thread is counted
> > as a CPU to satisfy a job's resource requirement, but multiple jobs are not allocated threads on
> > the same core. The count of CPUs allocated to a job may be rounded up to account for every CPU
> > on an allocated core. Setting a value for **DefMemPerCPU** is strongly recommended.
> >
> > <!-- -->
> >
> > **CR_ONE_TASK_PER_CORE**  
> > Allocate one task per core by default. Without this option, by default one task will be
> > allocated per thread on nodes with more than one **ThreadsPerCore** configured. **NOTE**: This
> > option cannot be used with CR_CPU\*.
> >
> > <!-- -->
> >
> > **CR_CORE_DEFAULT_DIST_BLOCK**  
> > Allocate cores within a node using block distribution by default. This is a pseudo-best-fit
> > algorithm that minimizes the number of boards and minimizes the number of sockets (within
> > minimum boards) used for the allocation. This default behavior can be overridden specifying a
> > particular "-m" parameter with srun/salloc/sbatch. Without this option, cores will be allocated
> > cyclically across the sockets.
> >
> > <!-- -->
> >
> > **CR_LLN**  
> > Schedule resources to jobs on the least loaded nodes (based upon the number of idle CPUs). This
> > is generally only recommended for an environment with serial jobs as idle resources will tend to
> > be highly fragmented, resulting in parallel jobs being distributed across many nodes. Note that
> > node **Weight** takes precedence over how many idle resources are on each node. Also see the
> > partition configuration parameter **LLN** use the least loaded nodes in selected partitions.
> >
> > <!-- -->
> >
> > **CR_Pack_Nodes**  
> > If a job allocation contains more resources than will be used for launching tasks (e.g. if whole
> > nodes are allocated to a job), then rather than distributing a job's tasks evenly across its
> > allocated nodes, pack them as tightly as possible on these nodes. For example, consider a job
> > allocation containing two **entire** nodes with eight CPUs each. If the job starts ten tasks
> > across those two nodes without this option, it will start five tasks on each of the two nodes.
> > With this option, eight tasks will be started on the first node and two tasks on the second
> > node. This can be superseded by "NoPack" in srun's "--distribution" option. CR_Pack_Nodes only
> > applies when the "block" task distribution method is used.
> >
> > <!-- -->
> >
> > **CR_Socket**  
> > Sockets are consumable resources. On nodes with multiple cores, each core or thread is counted
> > as a CPU to satisfy a job's resource requirement, but multiple jobs are not allocated resources
> > on the same socket.
> >
> > <!-- -->
> >
> > **CR_Socket_Memory**  
> > Memory and sockets are consumable resources. On nodes with multiple cores, each core or thread
> > is counted as a CPU to satisfy a job's resource requirement, but multiple jobs are not allocated
> > resources on the same socket. Setting a value for **DefMemPerCPU** is strongly recommended.
> >
> > <!-- -->
> >
> > **CR_Memory**  
> > Memory is a consumable resource. **NOTE**: This implies *OverSubscribe=YES* or
> > *OverSubscribe=FORCE* for all partitions. Setting a value for **DefMemPerCPU** is strongly
> > recommended.
> >
> > **NOTE**: If memory isn't configured as a consumable resource (CR_CPU, CR_Core or CR_Socket
> > without \_Memory) memory can be oversubscribed and will not be constrained by task/cgroup even
> > if it is configured in cgroup.conf. In this case the *--mem* option is only used to filter out
> > nodes with lower configured memory and does not take running jobs into account. For instance,
> > two jobs requesting all the memory of a node can run at the same time.
>
> **SlurmctldAddr**  
> An optional address to be used for communications to the currently active slurmctld daemon,
> normally used with Virtual IP addressing of the currently active server. If this parameter is not
> specified then each primary and backup server will have its own unique address used for
> communications as specified in the **SlurmctldHost** parameter. If this parameter is specified
> then the **SlurmctldHost** parameter will still be used for communications to specific slurmctld
> primary or backup servers, for example to cause all of them to read the current configuration
> files or shutdown. Also see the **SlurmctldPrimaryOffProg** and **SlurmctldPrimaryOnProg**
> configuration parameters to configure programs to manipulate virtual IP address manipulation.
>
> <!-- -->
>
> **SlurmctldDebug**  
> The level of detail to provide **slurmctld** daemon's logs. The default value is **info**. If the
> **slurmctld** daemon is initiated with -v or --verbose options, that debug level will be preserve
> or restored upon reconfiguration.
>
> > **quiet**  
> > Log nothing
> >
> > <!-- -->
> >
> > **fatal**  
> > Log only fatal errors
> >
> > <!-- -->
> >
> > **error**  
> > Log only errors
> >
> > <!-- -->
> >
> > **info**  
> > Log errors and general informational messages
> >
> > <!-- -->
> >
> > **verbose**  
> > Log errors and verbose informational messages
> >
> > <!-- -->
> >
> > **debug**  
> > Log errors and verbose informational messages and debugging messages
> >
> > <!-- -->
> >
> > **debug2**  
> > Log errors and verbose informational messages and more debugging messages
> >
> > <!-- -->
> >
> > **debug3**  
> > Log errors and verbose informational messages and even more debugging messages
> >
> > <!-- -->
> >
> > **debug4**  
> > Log errors and verbose informational messages and even more debugging messages
> >
> > <!-- -->
> >
> > **debug5**  
> > Log errors and verbose informational messages and even more debugging messages
>
> **SlurmctldHost**  
> The short, or long, hostname of the machine where Slurm control daemon is executed (i.e. the name
> returned by the command "hostname -s"). If the host where slurmctld will run may be modified by
> another process, such as pacemaker, then a comma-delimited list with the hostname of every machine
> should be provided. This hostname is optionally followed by the address, either the IP address or
> a name by which the address can be identified, enclosed in parentheses. e.g.
>
> <!-- -->
>
>     SlurmctldHost=slurmctl-primary(12.34.56.78)
>
> or
>
>     SlurmctldHost=slurmctl-primary1,slurmctl-primary2,slurmctl-primary3(slurmctl-primary)
>
> SlurmctldHost must be specified at least once. If specified more than once, the first entry will
> run as the primary and all other entries as backups. If the first specified host fails, the daemon
> will execute on the second host. If both the first and second specified host fails, the daemon
> will execute on the third host. A restart of slurmctld is required for changes to this parameter
> to take effect.
>
> **SlurmctldLogFile**  
> Fully qualified pathname of a file into which the **slurmctld** daemon's logs are written. The
> default value is none (performs logging via syslog).  
> See the section **LOGGING** if a pathname is specified.
>
> <!-- -->
>
> **SlurmctldParameters**  
> Multiple options may be comma separated.
>
> > **allow_user_triggers**  
> > Permit setting triggers from non-root/slurm_user users. SlurmUser must also be set to root to
> > permit these triggers to work. See the **strigger** man page for additional details.
> >
> > <!-- -->
> >
> > **cloud_dns**  
> > By default, Slurm expects that the network address for a cloud node won't be known until the
> > creation of the node and that Slurm will be notified of the node's address (e.g. **scontrol
> > update nodename=\<name\> nodeaddr=\<addr\>**). Since Slurm communications rely on the node
> > configuration found in the slurm.conf, Slurm will tell the client command, after waiting for all
> > nodes to boot, each node's ip address. However, in environments where the nodes are in DNS, this
> > step can be avoided by configuring this option.
> >
> > <!-- -->
> >
> > **cloud_reg_addrs**  
> > When a cloud node registers, the node's NodeAddr and NodeHostName will automatically be set.
> > They will be reset back to the nodename after powering off. Dynamically registered nodes
> > automatically set the node's NodeAddr and NodeHostName on the first registration and won't be
> > updated on subsequent registrations if it changes. Setting **cloud_reg_addrs** will update a
> > dynamically registered node's NodeAddr and NodeHostName if it changes on subsequent
> > registrations.
> >
> > <!-- -->
> >
> > **enable_configless**  
> > Permit "configless" operation by the slurmd, slurmstepd, and user commands. When enabled the
> > slurmd will be permitted to retrieve config files from the slurmctld, and on any 'scontrol
> > reconfigure' command new configs will be automatically pushed out and applied to nodes that are
> > running in this "configless" mode. A restart of slurmctld is required for changes to this
> > parameter to take effect. See https://slurm.schedmd.com/configless_slurm.html for more details.
> >
> > **NOTE**: Included files with the **Include** directive will only be pushed if the filename has
> > no path separators and is located adjacent to slurm.conf.
> >
> > <!-- -->
> >
> > **idle_on_node_suspend**  
> > Mark nodes as idle, regardless of current state, when suspending nodes with **SuspendProgram**
> > so that nodes will be eligible to be resumed at a later time.
> >
> > <!-- -->
> >
> > **node_reg_mem_percent=#**  
> > Percentage of memory a node is allowed to register with without being marked as invalid with low
> > memory. Default is 100. For State=CLOUD nodes, the default is 90. To disable this for cloud
> > nodes set it to 100. *config_overrides* takes precedence over this option.
> >
> > It's recommended that *task/cgroup* with *ConstrainRamSpace* is configured. A memory cgroup
> > limit won't be set more than the actual memory on the node. If needed, configure
> > *AllowedRamSpace* in the cgroup.conf to add a buffer.
> >
> > <!-- -->
> >
> > **power_save_interval**  
> > How often the power_save thread looks to resume and suspend nodes. The power_save thread will do
> > work sooner if there are node state changes. Default is 10 seconds.
> >
> > <!-- -->
> >
> > **power_save_min_interval**  
> > How often the power_save thread, at a minimum, looks to resume and suspend nodes. Default is 0.
> >
> > <!-- -->
> >
> > **max_dbd_msg_action**  
> > Action used once MaxDBDMsgs is reached, options are 'discard' (default) and 'exit'.
> >
> > When 'discard' is specified and MaxDBDMsgs is reached we start by purging pending messages of
> > types Step start and complete, and it reaches MaxDBDMsgs again Job start messages are purged.
> > Job completes and node state changes continue to consume the empty space created from the
> > purgings until MaxDBDMsgs is reached again at which no new message is tracked creating data loss
> > and potentially runaway jobs.
> >
> > When 'exit' is specified and MaxDBDMsgs is reached the slurmctld will exit instead of discarding
> > any messages. It will be impossible to start the slurmctld with this option where the slurmdbd
> > is down and the slurmctld is tracking more than MaxDBDMsgs.
> >
> > <!-- -->
> >
> > **reboot_from_controller**  
> > Run the **RebootProgram** from the controller instead of on the slurmds. The RebootProgram will
> > be passed a comma-separated list of nodes to reboot as the first argument and if applicable the
> > required features needed for reboot as the second argument.
> >
> > <!-- -->
> >
> > **rl_bucket_size=**  
> > Size of the token bucket. This permits a certain amount of RPC burst from a user before the
> > steady-state rate limit takes effect. The default value is 30.
> >
> > <!-- -->
> >
> > **rl_enable**  
> > Enable per-user RPC rate-limiting support. Client-commands will be told to back off and sleep
> > for a second once the limit has been reached. This is implemented as a "token bucket", which
> > permits a certain degree of "bursty" RPC load from an individual user before holding them to a
> > steady-state RPC load established by the refill period and rate.
> >
> > <!-- -->
> >
> > **rl_refill_period=**  
> > How frequently, in seconds, in which additional tokens are added to each user bucket. The
> > default value is 1.
> >
> > <!-- -->
> >
> > **rl_refill_rate=**  
> > How many tokens to add to the bucket on each period. The default value is 2.
> >
> > <!-- -->
> >
> > **rl_table_size=**  
> > Number of entries in the user hash-table. Recommended value should be at least twice the number
> > of active user accounts on the system. The default value is 8192.
> >
> > <!-- -->
> >
> > **user_resv_delete**  
> > Allow any user able to run in a reservation to delete it.
> >
> > <!-- -->
> >
> > **validate_nodeaddr_threads=**  
> > During startup, slurmctld looks up the address for each compute node in the system. On large
> > systems this can cause considerable delay, this option permits the slurmctld to concurrently
> > handle the lookup calls and can reduce system startup time considerably. The default value is 1.
> > Maximum permitted value is 64.
>
> **SlurmctldPidFile**  
> Fully qualified pathname of a file into which the **slurmctld** daemon may write its process id.
> This may be used for automated signal processing. The default value is "/var/run/slurmctld.pid".
>
> <!-- -->
>
> **SlurmctldPort**  
> The port number that the Slurm controller, **slurmctld**, listens to for work. The default value
> is SLURMCTLD_PORT as established at system build time. If none is explicitly specified, it will be
> set to 6817. **SlurmctldPort** may also be configured to support a range of port numbers in order
> to accept larger bursts of incoming messages by specifying two numbers separated by a dash (e.g.
> **SlurmctldPort=6817-6818**). A restart of slurmctld is required for changes to this parameter to
> take effect. **NOTE**: Either **slurmctld** and **slurmd** daemons must not execute on the same
> nodes or the values of **SlurmctldPort** and **SlurmdPort** must be different.
>
> **Note**: On Cray systems, Realm-Specific IP Addressing (RSIP) will automatically try to interact
> with anything opened on ports 8192-60000. Configure SlurmctldPort to use a port outside of the
> configured SrunPortRange and RSIP's port range.
>
> <!-- -->
>
> **SlurmctldPrimaryOffProg**  
> This program is executed when a slurmctld daemon running as the primary server becomes a backup
> server. By default no program is executed. See also the related "SlurmctldPrimaryOnProg"
> parameter.
>
> <!-- -->
>
> **SlurmctldPrimaryOnProg**  
> This program is executed when a slurmctld daemon running as a backup server becomes the primary
> server. By default no program is executed. When using virtual IP addresses to manage High
> Available Slurm services, this program can be used to add the IP address to an interface (and
> optionally try to kill the unresponsive slurmctld daemon and flush the ARP caches on nodes on the
> local Ethernet fabric). See also the related "SlurmctldPrimaryOffProg" parameter.
>
> <!-- -->
>
> **SlurmctldSyslogDebug**  
> The slurmctld daemon will log events to the syslog file at the specified level of detail. If not
> set, the slurmctld daemon will log to syslog at level **fatal**, unless there is no
> **SlurmctldLogFile** and it is running in the background, in which case it will log to syslog at
> the level specified by **SlurmctldDebug** (at **fatal** in the case that **SlurmctldDebug** is set
> to **quiet**) or it is run in the foreground, when it will be set to quiet.
>
> > **quiet**  
> > Log nothing
> >
> > <!-- -->
> >
> > **fatal**  
> > Log only fatal errors
> >
> > <!-- -->
> >
> > **error**  
> > Log only errors
> >
> > <!-- -->
> >
> > **info**  
> > Log errors and general informational messages
> >
> > <!-- -->
> >
> > **verbose**  
> > Log errors and verbose informational messages
> >
> > <!-- -->
> >
> > **debug**  
> > Log errors and verbose informational messages and debugging messages
> >
> > <!-- -->
> >
> > **debug2**  
> > Log errors and verbose informational messages and more debugging messages
> >
> > <!-- -->
> >
> > **debug3**  
> > Log errors and verbose informational messages and even more debugging messages
> >
> > <!-- -->
> >
> > **debug4**  
> > Log errors and verbose informational messages and even more debugging messages
> >
> > <!-- -->
> >
> > **debug5**  
> > Log errors and verbose informational messages and even more debugging messages
>
> > **NOTE**: By default, Slurm's systemd service files start daemons in the foreground with the -D
> > option. This means that systemd will capture stdout/stderr output and print that to syslog,
> > independent of Slurm printing to syslog directly. To prevent systemd from doing this, add
> > "StandardOutput=null" and "StandardError=null" to the respective service files or override
> > files.
>
> **SlurmctldTimeout**  
> The interval, in seconds, that the backup controller waits for the primary controller to respond
> before assuming control. The default value is 120 seconds. May not exceed 65533.
>
> <!-- -->
>
> **SlurmdDebug**  
> The level of detail to provide **slurmd** daemon's logs. The default value is **info**.
>
> > **quiet**  
> > Log nothing
> >
> > <!-- -->
> >
> > **fatal**  
> > Log only fatal errors
> >
> > <!-- -->
> >
> > **error**  
> > Log only errors
> >
> > <!-- -->
> >
> > **info**  
> > Log errors and general informational messages
> >
> > <!-- -->
> >
> > **verbose**  
> > Log errors and verbose informational messages
> >
> > <!-- -->
> >
> > **debug**  
> > Log errors and verbose informational messages and debugging messages
> >
> > <!-- -->
> >
> > **debug2**  
> > Log errors and verbose informational messages and more debugging messages
> >
> > <!-- -->
> >
> > **debug3**  
> > Log errors and verbose informational messages and even more debugging messages
> >
> > <!-- -->
> >
> > **debug4**  
> > Log errors and verbose informational messages and even more debugging messages
> >
> > <!-- -->
> >
> > **debug5**  
> > Log errors and verbose informational messages and even more debugging messages
>
> **SlurmdLogFile**  
> Fully qualified pathname of a file into which the **slurmd** daemon's logs are written. The
> default value is none (performs logging via syslog). The first "%h" within the name is replaced
> with the hostname on which the **slurmd** is running. The first "%n" within the name is replaced
> with the Slurm node name on which the **slurmd** is running.  
> See the section **LOGGING** if a pathname is specified.
>
> <!-- -->
>
> **SlurmdParameters**  
> Parameters specific to the Slurmd. Multiple options may be comma separated.
>
> > **allow_ecores**  
> > If set, and processors on your nodes have E-Cores, allows them to be used in for scheduling and
> > task placement. (By default, E-Cores are ignored.)
> >
> > <!-- -->
> >
> > **config_overrides**  
> > If set, consider the configuration of each node to be that specified in the slurm.conf
> > configuration file and any node with less than the configured resources will **not** be set to
> > INVAL/INVALID_REG. This option is generally only useful for testing purposes. Equivalent to the
> > now deprecated FastSchedule=2 option.
> >
> > <!-- -->
> >
> > **l3cache_as_socket**  
> > Use the hwloc l3cache as the socket count. Can be useful on certain processors where the socket
> > level is too coarse, and the l3cache may provide better task distribution. (E.g., along CCX
> > boundaries instead of socket boundaries.) Mutually exclusive with numa_node_as_socket. Requires
> > hwloc v2.
> >
> > **numa_node_as_socket**  
> > Use the hwloc NUMA Node to determine main hierarchy object to be used as socket. If the option
> > is set Slurm will check the parent object of NUMA Node and use it as socket. This option may be
> > useful for architectures likes AMD Epyc, where number of nodes per socket may be configured.
> > Mutually exclusive with l3cache_as_socket. Requires hwloc v2.
> >
> > <!-- -->
> >
> > **shutdown_on_reboot**  
> > If set, the Slurmd will shut itself down when a reboot request is received.
>
> **SlurmdPidFile**  
> Fully qualified pathname of a file into which the **slurmd** daemon may write its process id. This
> may be used for automated signal processing. The first "%h" within the name is replaced with the
> hostname on which the **slurmd** is running. The first "%n" within the name is replaced with the
> Slurm node name on which the **slurmd** is running. The default value is "/var/run/slurmd.pid".
>
> <!-- -->
>
> **SlurmdPort**  
> The port number that the Slurm compute node daemon, **slurmd**, listens to for work. The default
> value is SLURMD_PORT as established at system build time. If none is explicitly specified, its
> value will be 6818. A restart of slurmctld is required for changes to this parameter to take
> effect. **NOTE**: Either slurmctld and slurmd daemons must not execute on the same nodes or the
> values of **SlurmctldPort** and **SlurmdPort** must be different.
>
> **Note**: On Cray systems, Realm-Specific IP Addressing (RSIP) will automatically try to interact
> with anything opened on ports 8192-60000. Configure SlurmdPort to use a port outside of the
> configured SrunPortRange and RSIP's port range.
>
> <!-- -->
>
> **SlurmdSpoolDir**  
> Fully qualified pathname of a directory into which the **slurmd** daemon's state information and
> batch job script information are written. This must be a common pathname for all nodes, but should
> represent a directory which is local to each node (reference a local file system). The default
> value is "/var/spool/slurmd". The first "%h" within the name is replaced with the hostname on
> which the **slurmd** is running. The first "%n" within the name is replaced with the Slurm node
> name on which the **slurmd** is running.
>
> <!-- -->
>
> **SlurmdSyslogDebug**  
> The slurmd daemon will log events to the syslog file at the specified level of detail. If not set,
> the slurmd daemon will log to syslog at level **fatal**, unless there is no **SlurmdLogFile** and
> it is running in the background, in which case it will log to syslog at the level specified by
> **SlurmdDebug** (at **fatal** in the case that **SlurmdDebug** is set to **quiet**) or it is run
> in the foreground, when it will be set to quiet.
>
> > **quiet**  
> > Log nothing
> >
> > <!-- -->
> >
> > **fatal**  
> > Log only fatal errors
> >
> > <!-- -->
> >
> > **error**  
> > Log only errors
> >
> > <!-- -->
> >
> > **info**  
> > Log errors and general informational messages
> >
> > <!-- -->
> >
> > **verbose**  
> > Log errors and verbose informational messages
> >
> > <!-- -->
> >
> > **debug**  
> > Log errors and verbose informational messages and debugging messages
> >
> > <!-- -->
> >
> > **debug2**  
> > Log errors and verbose informational messages and more debugging messages
> >
> > <!-- -->
> >
> > **debug3**  
> > Log errors and verbose informational messages and even more debugging messages
> >
> > <!-- -->
> >
> > **debug4**  
> > Log errors and verbose informational messages and even more debugging messages
> >
> > <!-- -->
> >
> > **debug5**  
> > Log errors and verbose informational messages and even more debugging messages
>
> > **NOTE**: By default, Slurm's systemd service files start daemons in the foreground with the -D
> > option. This means that systemd will capture stdout/stderr output and print that to syslog,
> > independent of Slurm printing to syslog directly. To prevent systemd from doing this, add
> > "StandardOutput=null" and "StandardError=null" to the respective service files or override
> > files.
>
> **SlurmdTimeout**  
> The interval, in seconds, that the Slurm controller waits for **slurmd** to respond before
> configuring that node's state to DOWN. A value of zero indicates the node will not be tested by
> **slurmctld** to confirm the state of **slurmd**, the node will not be automatically set to a DOWN
> state indicating a non-responsive **slurmd**, and some other tool will take responsibility for
> monitoring the state of each compute node and its **slurmd** daemon. Slurm's hierarchical
> communication mechanism is used to ping the **slurmd** daemons in order to minimize system noise
> and overhead. The default value is 300 seconds. The value may not exceed 65533 seconds.
>
> <!-- -->
>
> **SlurmdUser**  
> The name of the user that the **slurmd** daemon executes as. This user must exist on all nodes of
> the cluster for authentication of communications between Slurm components. The default value is
> "root".
>
> <!-- -->
>
> **SlurmSchedLogFile**  
> Fully qualified pathname of the scheduling event logging file. The syntax of this parameter is the
> same as for **SlurmctldLogFile**. In order to configure scheduler logging, set both the
> **SlurmSchedLogFile** and **SlurmSchedLogLevel** parameters.
>
> <!-- -->
>
> **SlurmSchedLogLevel**  
> The initial level of scheduling event logging, similar to the **SlurmctldDebug** parameter used to
> control the initial level of **slurmctld** logging. Valid values for **SlurmSchedLogLevel** are
> "0" (scheduler logging disabled) and "1" (scheduler logging enabled). If this parameter is
> omitted, the value defaults to "0" (disabled). In order to configure scheduler logging, set both
> the **SlurmSchedLogFile** and **SlurmSchedLogLevel** parameters. The scheduler logging level can
> be changed dynamically using **scontrol**.
>
> <!-- -->
>
> **SlurmUser**  
> The name of the user that the **slurmctld** daemon executes as. For security purposes, a user
> other than "root" is recommended. This user must exist on all nodes of the cluster for
> authentication of communications between Slurm components. The default value is "root".
>
> <!-- -->
>
> **SrunEpilog**  
> Fully qualified pathname of an executable to be run by srun following the completion of a job
> step. The command line arguments for the executable will be the command and arguments of the job
> step. This configuration parameter may be overridden by srun's **--epilog** parameter. Note that
> while the other "Epilog" executables (e.g., TaskEpilog) are run by slurmd on the compute nodes
> where the tasks are executed, the **SrunEpilog** runs on the node where the "srun" is executing.
>
> <!-- -->
>
> **SrunPortRange**  
> The **srun** creates a set of listening ports to communicate with the controller, the slurmstepd
> and to handle the application I/O. By default these ports are ephemeral meaning the port numbers
> are selected by the kernel. Using this parameter allow sites to configure a range of ports from
> which srun ports will be selected. This is useful if sites want to allow only certain port range
> on their network.
>
> **Note**: On Cray systems, Realm-Specific IP Addressing (RSIP) will automatically try to interact
> with anything opened on ports 8192-60000. Configure SrunPortRange to use a range of ports above
> those used by RSIP, ideally 1000 or more ports, for example "SrunPortRange=60001-63000".
>
> **Note**: **SrunPortRange** must be large enough to cover the expected number of srun ports
> created. A single srun opens 4 listening ports plus 2 more for every 48 hosts beyond the first 48.
> Example:
>
> > **srun -N 1** will use 4 listening ports.  
> >
> > <!-- -->
> >
> > **srun -N 48** will use 4 listening ports.  
> >
> > <!-- -->
> >
> > **srun -N 50** will use 6 listening ports.  
> >
> > <!-- -->
> >
> > **srun -N 200** will use 12 listening ports.  
> >
> > <!-- -->
> >
> > **SrunProlog**  
> > Fully qualified pathname of an executable to be run by srun prior to the launch of a job step.
> > The command line arguments for the executable will be the command and arguments of the job step.
> > This configuration parameter may be overridden by srun's **--prolog** parameter. Note that while
> > the other "Prolog" executables (e.g., TaskProlog) are run by slurmd on the compute nodes where
> > the tasks are executed, the **SrunProlog** runs on the node where the "srun" is executing.
> >
> > <!-- -->
> >
> > **StateSaveLocation**  
> > Fully qualified pathname of a directory into which the Slurm controller, **slurmctld**, saves
> > its state (e.g. "/usr/local/slurm/checkpoint"). Slurm state will saved here to recover from
> > system failures. **SlurmUser** must be able to create files in this directory. If you have a
> > secondary **SlurmctldHost** configured, this location should be readable and writable by both
> > systems. Since all running and pending job information is stored here, the use of a reliable
> > file system (e.g. RAID) is recommended. The default value is "/var/spool". A restart of
> > slurmctld is required for changes to this parameter to take effect. If any slurm daemons
> > terminate abnormally, their core files will also be written into this directory.
> >
> > <!-- -->
> >
> > **SuspendExcNodes**  
> > Specifies the nodes which are to not be placed in power save mode, even if the node remains idle
> > for an extended period of time. Use Slurm's hostlist expression to identify nodes with an
> > optional ":" separator and count of nodes to exclude from the preceding range. For example
> > "nid\[10-20\]:4" will prevent 4 usable nodes (i.e IDLE and not DOWN, DRAINING or already powered
> > down) in the set "nid\[10-20\]" from being powered down. Multiple sets of nodes can be specified
> > with or without counts in a comma separated list (e.g "nid\[10-20\]:4,nid\[80-90\]:2"). By
> > default no nodes are excluded. This value may be updated with scontrol. See
> > **ReconfigFlags=KeepPowerSaveSettings** for setting persistence.
> >
> > <!-- -->
> >
> > **SuspendExcParts**  
> > Specifies the partitions whose nodes are to not be placed in power save mode, even if the node
> > remains idle for an extended period of time. Multiple partitions can be identified and separated
> > by commas. By default no nodes are excluded. This value may be updated with scontrol. See
> > **ReconfigFlags=KeepPowerSaveSettings** for setting persistence.
> >
> > <!-- -->
> >
> > **SuspendExcStates**  
> > Specifies node states that are not to be powered down automatically. Valid states include CLOUD,
> > DOWN, DRAIN, DYNAMIC_FUTURE, DYNAMIC_NORM, FAIL, INVALID_REG, MAINTENANCE, NOT_RESPONDING,
> > PERFCTRS, PLANNED, and RESERVED. By default, any of these states, if idle for **SuspendTime**,
> > would be powered down. This value may be updated with scontrol. See
> > **ReconfigFlags=KeepPowerSaveSettings** for setting persistence.
> >
> > <!-- -->
> >
> > **SuspendProgram**  
> > **SuspendProgram** is the program that will be executed when a node remains idle for an extended
> > period of time. This program is expected to place the node into some power save mode. This can
> > be used to reduce the frequency and voltage of a node or completely power the node off. The
> > program executes as **SlurmUser**. The argument to the program will be the names of nodes to be
> > placed into power savings mode (using Slurm's hostlist expression format). By default, no
> > program is run. Programs will be killed if they run longer than the largest configured, global
> > or partition, **ResumeTimeout** or **SuspendTimeout**.
> >
> > <!-- -->
> >
> > **SuspendRate**  
> > The rate at which nodes are placed into power save mode by **SuspendProgram**. The value is
> > number of nodes per minute and it can be used to prevent a large drop in power consumption (e.g.
> > after a large job completes). A value of zero results in no limits being imposed. The default
> > value is 60 nodes per minute.
> >
> > <!-- -->
> >
> > **SuspendTime**  
> > Nodes which remain idle or down for this number of seconds will be placed into power save mode
> > by **SuspendProgram**. Setting **SuspendTime** to anything but INFINITE (or -1) will enable
> > power save mode. INFINITE is the default.
> >
> > <!-- -->
> >
> > **SuspendTimeout**  
> > Maximum time permitted (in seconds) between when a node suspend request is issued and when the
> > node is shutdown. At that time the node must be ready for a resume request to be issued as
> > needed for new work. The default value is 30 seconds.
> >
> > <!-- -->
> >
> > **SwitchParameters**  
> > Optional parameters for the switch plugin.
> >
> > On HPE Slingshot systems configured with SwitchType=switch/hpe_slingshot, the following
> > parameters are supported (separate multiple parameters with a comma):
> >
> > > **vnis**=\<*min*\>-\<*max*\>  
> > > Range of VNIs to allocate for jobs and applications. This parameter is required.
> > >
> > > <!-- -->
> > >
> > > **tcs**=\<*class1*\>\[:\<*class2*\>\]...  
> > > Set of traffic classes to configure for applications. Supported traffic classes are
> > > DEDICATED_ACCESS, LOW_LATENCY, BULK_DATA, and BEST_EFFORT. The traffic classes may also be
> > > specified as TC_DEDICATED_ACCESS, TC_LOW_LATENCY, TC_BULK_DATA, and TC_BEST_EFFORT.
> > >
> > > <!-- -->
> > >
> > > **single_node_vni**=\<*all*\|*user*\|*none*\>  
> > > If set to 'all', allocate a VNI for all job steps (by default, no VNI will be allocated for
> > > single-node job steps). If set to 'user', allocate a VNI for single-node job steps using the
> > > **srun** **--network=single_node_vni** option or **SLURM_NETWORK=single_node_vni** environment
> > > variable. If set to 'none' (or if **single_node_vni** is not set), do not allocate any VNI for
> > > single-node job steps. For backwards compatibility, setting **single_node_vni** with no
> > > argument is equivalent to 'all'.
> > >
> > > <!-- -->
> > >
> > > **job_vni**=\<*all*\|*user*\|*none*\>  
> > > If set to 'all', allocate an additional VNI for jobs, shared among all job steps. If set to
> > > 'user', allocate an additional VNI for any job using the **srun** **--network=job_vni** option
> > > or **SLURM_NETWORK=job_vni** environment variable. If set to 'none' (or if **job_vni** is not
> > > set), do not allocate any additional VNI for jobs. For backwards compatibility, setting
> > > **job_vni** with no argument is equivalent to 'all'.
> > >
> > > <!-- -->
> > >
> > > **adjust_limits**  
> > > If set, slurmd will set an upper bound on network resource reservations by taking the per-NIC
> > > maximum resource quantity and subtracting the reserved or used values (whichever is higher)
> > > for any system network services; this is the default.
> > >
> > > <!-- -->
> > >
> > > **no_adjust_limits**  
> > > If set, slurmd will calculate network resource reservations based only upon the per-resource
> > > configuration default and number of tasks in the application; it will not set an upper bound
> > > on those reservation requests based on resource usage of already-existing system network
> > > services. Setting this will mean more application launches could fail based on network
> > > resource exhaustion, but if the application absolutely needs a certain amount of resources to
> > > function, this option will ensure that.
> > >
> > > <!-- -->
> > >
> > > **jlope_url**=\<*url*\>  
> > > If set, slurmctld will use the configured URL to request Instant On NIC information for each
> > > node in a job step from the HPE jackalope daemon REST API.
> > >
> > > <!-- -->
> > >
> > > **jlope_auth**=\<*BASIC*\|*OAUTH*\>  
> > > HPE jackalope daemon REST API authentication type (BASIC or OAUTH, default OAUTH).
> > >
> > > <!-- -->
> > >
> > > **jlope_authdir**=\<*directory*\>  
> > > Directory containing authentication info files (default /etc/jackaloped for BASIC
> > > authentication, /etc/wlm-client-auth for OAUTH authentication).
> > >
> > > <!-- -->
> > >
> > > **def\_\<rsrc\>**=\<*val*\>  
> > > Per-CPU reserved allocation for this resource.
> > >
> > > <!-- -->
> > >
> > > **res\_\<rsrc\>**=\<*val*\>  
> > > Per-node reserved allocation for this resource. If set, overrides the per-CPU allocation.
> > >
> > > <!-- -->
> > >
> > > **max\_\<rsrc\>**=\<*val*\>  
> > > Maximum per-node application for this resource.
> >
> > The resources that may be configured are:
> >
> > > **txqs**  
> > > Transmit command queues. The default is 2 per-CPU, maximum 1024 per-node.
> > >
> > > <!-- -->
> > >
> > > **tgqs**  
> > > Target command queues. The default is 1 per-CPU, maximum 512 per-node.
> > >
> > > <!-- -->
> > >
> > > **eqs**  
> > > Event queues. The default is 2 per-CPU, maximum 2047 per-node.
> > >
> > > <!-- -->
> > >
> > > **cts**  
> > > Counters. The default is 1 per-CPU, maximum 2047 per-node.
> > >
> > > <!-- -->
> > >
> > > **tles**  
> > > Trigger list entries. The default is 1 per-CPU, maximum 2048 per-node.
> > >
> > > <!-- -->
> > >
> > > **ptes**  
> > > Portable table entries. The default is 6 per-CPU, maximum 2048 per-node.
> > >
> > > <!-- -->
> > >
> > > **les**  
> > > List entries. The default is 16 per-CPU, maximum 16384 per-node.
> > >
> > > <!-- -->
> > >
> > > **acs**  
> > > Addressing contexts. The default is 4 per-CPU, maximum 1022 per-node.
> >
> > **SwitchType**  
> > Identifies the type of switch or interconnect used for application communications. Acceptable
> > values include "switch/cray_aries" for Cray systems, "switch/hpe_slingshot" for HPE Slingshot
> > systems and "switch/none" for switches not requiring special processing for job launch or
> > termination (Ethernet, and InfiniBand). The default value is "switch/none". All Slurm daemons,
> > commands and running jobs must be restarted for a change in **SwitchType** to take effect. If
> > running jobs exist at the time **slurmctld** is restarted with a new value of **SwitchType**,
> > records of all jobs in any state may be lost.
> >
> > <!-- -->
> >
> > **TaskEpilog**  
> > Fully qualified pathname of a program to be executed as the slurm job's owner after termination
> > of each task. See **TaskProlog** for execution order details.
> >
> > <!-- -->
> >
> > **TaskPlugin**  
> > Identifies the type of task launch plugin, typically used to provide resource management within
> > a node (e.g. pinning tasks to specific processors). More than one task plugin can be specified
> > in a comma-separated list. The prefix of "task/" is optional. Acceptable values include:
> >
> > > **task/affinity**  
> > > binds processes to specified resources using sched_setaffinity(). This enables the --cpu-bind
> > > and/or --mem-bind srun options.
> > >
> > > <!-- -->
> > >
> > > **task/cgroup**  
> > > enables process containment to specified resources using Cgroups cpuset interface. This
> > > enables the --cpu-bind and/or --mem-bind srun options. **NOTE**: see "man cgroup.conf" for
> > > configuration details.
> > >
> > > <!-- -->
> > >
> > > **task/none**  
> > > for systems requiring no special handling of user tasks. Lacks support for the --cpu-bind
> > > and/or --mem-bind srun options. The default value is "task/none".
> >
> > > **NOTE**: It is recommended to stack **task/cgroup,task/affinity** together when configuring
> > > TaskPlugin, and setting **ConstrainCores=yes** in **cgroup.conf**. This setup uses the
> > > task/affinity plugin for setting the cpu mask for tasks and uses the task/cgroup plugin to
> > > fence tasks into the allocated cpus.
> > >
> > > **NOTE**: For CRAY systems only: task/cgroup must be used with task/cray_aries in TaskPlugin.
> > > For CRAY systems a configuration like this is recommended:
> > >
> > >     TaskPlugin=task/cray_aries,task/cgroup,task/affinity
> >
> > **TaskPluginParam**  
> > Optional parameters for the task plugin. Multiple options should be comma separated. **None**,
> > **Sockets**, **Cores** and **Threads** are mutually exclusive and treated as a last possible
> > source of --cpu-bind default. See also Node and Partition CpuBind options.
> >
> > > **Cores**  
> > > Bind tasks to cores by default. Overrides automatic binding.
> > >
> > > <!-- -->
> > >
> > > **None**  
> > > Perform no task binding by default. Overrides automatic binding.
> > >
> > > <!-- -->
> > >
> > > **Sockets**  
> > > Bind to sockets by default. Overrides automatic binding.
> > >
> > > <!-- -->
> > >
> > > **Threads**  
> > > Bind to threads by default. Overrides automatic binding.
> > >
> > > <!-- -->
> > >
> > > **SlurmdOffSpec**  
> > > If specialized cores or CPUs are identified for the node (i.e. the **CoreSpecCount** or
> > > **CpuSpecList** are configured for the node), then Slurm daemons running on the compute node
> > > (i.e. slurmd and slurmstepd) should run outside of those resources (i.e. specialized resources
> > > are completely unavailable to Slurm daemons and jobs spawned by Slurm). This option may not be
> > > used with the **task/cray_aries** plugin.
> > >
> > > <!-- -->
> > >
> > > **Verbose**  
> > > Verbosely report binding before tasks run by default.
> > >
> > > <!-- -->
> > >
> > > **Autobind**  
> > > Set a default binding in the event that "auto binding" doesn't find a match. Set to Threads,
> > > Cores or Sockets (E.g. TaskPluginParam=autobind=threads).
> >
> > **TaskProlog**  
> > Fully qualified pathname of a program to be executed as the slurm job's owner prior to
> > initiation of each task. Besides the normal environment variables, this has SLURM_TASK_PID
> > available to identify the process ID of the task being started. Standard output from this
> > program can be used to control the environment variables and output for the user program.
> >
> > > **export NAME=value**  
> > > Will set environment variables for the task being spawned. Everything after the equal sign to
> > > the end of the line will be used as the value for the environment variable. Exporting of
> > > functions is not currently supported.
> > >
> > > <!-- -->
> > >
> > > **print ...**  
> > > Will cause that line (without the leading "print ") to be printed to the job's standard
> > > output.
> > >
> > > <!-- -->
> > >
> > > **unset NAME**  
> > > Will clear environment variables for the task being spawned.
> > >
> > > <!-- -->
> > >
> > > The order of task prolog/epilog execution is as follows:  
> > >
> > > <!-- -->
> > >
> > > **1. pre_launch_priv()**  
> > > Function in TaskPlugin
> > >
> > > <!-- -->
> > >
> > > **1. pre_launch()**  
> > > Function in TaskPlugin
> > >
> > > <!-- -->
> > >
> > > **2. TaskProlog**  
> > > System-wide per task program defined in slurm.conf
> > >
> > > <!-- -->
> > >
> > > **3. User prolog**  
> > > Job-step-specific task program defined using **srun**'s **--task-prolog** option or
> > > **SLURM_TASK_PROLOG** environment variable
> > >
> > > <!-- -->
> > >
> > > **4. Task**  
> > > Execute the job step's task
> > >
> > > <!-- -->
> > >
> > > **5. User epilog**  
> > > Job-step-specific task program defined using **srun**'s **--task-epilog** option or
> > > **SLURM_TASK_EPILOG** environment variable
> > >
> > > <!-- -->
> > >
> > > **6. TaskEpilog**  
> > > System-wide per task program defined in slurm.conf
> > >
> > > <!-- -->
> > >
> > > **7. post_term()**  
> > > Function in TaskPlugin
> >
> > **TCPTimeout**  
> > Time permitted for TCP connection to be established. Default value is 2 seconds.
> >
> > <!-- -->
> >
> > **TmpFS**  
> > Fully qualified pathname of the file system available to user jobs for temporary storage. This
> > parameter is used in establishing a node's **TmpDisk** space. The default value is "/tmp".
> >
> > <!-- -->
> >
> > **TopologyParam**  
> > Comma-separated options identifying network topology options.
> >
> > > **Dragonfly**  
> > > Optimize allocation for Dragonfly network. Valid when TopologyPlugin=topology/tree.
> > >
> > > <!-- -->
> > >
> > > **SwitchAsNodeRank**  
> > > Assign the same node rank to all nodes under one leaf switch. This can be useful if the naming
> > > convention for the nodes does not match the network topology.
> > >
> > > <!-- -->
> > >
> > > **TopoOptional**  
> > > Only optimize allocation for network topology if the job includes a switch option. Since
> > > optimizing resource allocation for topology involves much higher system overhead, this option
> > > can be used to impose the extra overhead only on jobs which can take advantage of it. If most
> > > job allocations are not optimized for network topology, they may fragment resources to the
> > > point that topology optimization for other jobs will be difficult to achieve. **NOTE**: Jobs
> > > may span across nodes without common parent switches with this enabled.
> >
> > **TopologyPlugin**  
> > Identifies the plugin to be used for determining the network topology and optimizing job
> > allocations to minimize network contention. See **NETWORK TOPOLOGY** below for details.
> > Additional plugins may be provided in the future which gather topology information directly from
> > the network. Acceptable values include:
> >
> > > **topology/3d_torus**  
> > > best-fit logic over three-dimensional topology
> > >
> > > <!-- -->
> > >
> > > **topology/none**  
> > > default for other systems, best-fit logic over one-dimensional topology
> > >
> > > <!-- -->
> > >
> > > **topology/tree**  
> > > used for a hierarchical network as described in a *topology.conf* file
> >
> > **TrackWCKey**  
> > Boolean yes or no. Used to set display and track of the Workload Characterization Key. Must be
> > set to track correct wckey usage. **NOTE**: You must also set TrackWCKey in your slurmdbd.conf
> > file to create historical usage reports.
> >
> > <!-- -->
> >
> > **TreeWidth**  
> > **Slurmd** daemons use a virtual tree network for communications. **TreeWidth** specifies the
> > width of the tree (i.e. the fanout). On architectures with a front end node running the slurmd
> > daemon, the value must always be equal to or greater than the number of front end nodes which
> > eliminates the need for message forwarding between the slurmd daemons. On other architectures
> > the default value is 50, meaning each slurmd daemon can communicate with up to 50 other slurmd
> > daemons and over 2500 nodes can be contacted with two message hops. The default value will work
> > well for most clusters. Optimal system performance can typically be achieved if **TreeWidth** is
> > set to the square root of the number of nodes in the cluster for systems having no more than
> > 2500 nodes or the cube root for larger systems. The value may not exceed 65533.
> >
> > <!-- -->
> >
> > **UnkillableStepProgram**  
> > If the processes in a job step are determined to be unkillable for a period of time specified by
> > the **UnkillableStepTimeout** variable, the program specified by **UnkillableStepProgram** will
> > be executed. By default no program is run.
> >
> > See section **UNKILLABLE STEP PROGRAM SCRIPT** for more information.
> >
> > <!-- -->
> >
> > **UnkillableStepTimeout**  
> > The length of time, in seconds, that Slurm will wait before deciding that processes in a job
> > step are unkillable (after they have been signaled with SIGKILL) and execute
> > **UnkillableStepProgram**. The default timeout value is 60 seconds. If exceeded, the compute
> > node will be drained to prevent future jobs from being scheduled on the node.
> >
> > **NOTE**: Ensure that UnkillableStepTimeout is at least 5 times larger than MessageTimeout,
> > otherwise it can lead to unexpected draining of nodes.
> >
> > <!-- -->
> >
> > **UsePAM**  
> > If set to 1, PAM (Pluggable Authentication Modules for Linux) will be enabled. PAM is used to
> > establish the upper bounds for resource limits. With PAM support enabled, local system
> > administrators can dynamically configure system resource limits. Changing the upper bound of a
> > resource limit will not alter the limits of running jobs, only jobs started after a change has
> > been made will pick up the new limits. The default value is 0 (not to enable PAM support).
> > Remember that PAM also needs to be configured to support Slurm as a service. For sites using
> > PAM's directory based configuration option, a configuration file named **slurm** should be
> > created. The module-type, control-flags, and module-path names that should be included in the
> > file are:  
> > auth required pam_localuser.so  
> > auth required pam_shells.so  
> > account required pam_unix.so  
> > account required pam_access.so  
> > session required pam_unix.so  
> > For sites configuring PAM with a general configuration file, the appropriate lines (see above),
> > where **slurm** is the service-name, should be added.
> >
> > **NOTE**: UsePAM option has nothing to do with the **contribs/pam/pam_slurm** and/or
> > **contribs/pam_slurm_adopt** modules. So these two modules can work independently of the value
> > set for UsePAM.
> >
> > <!-- -->
> >
> > **VSizeFactor**  
> > Memory specifications in job requests apply to real memory size (also known as resident set
> > size). It is possible to enforce virtual memory limits for both jobs and job steps by limiting
> > their virtual memory to some percentage of their real memory allocation. The **VSizeFactor**
> > parameter specifies the job's or job step's virtual memory limit as a percentage of its real
> > memory limit. For example, if a job's real memory limit is 500MB and VSizeFactor is set to 101
> > then the job will be killed if its real memory exceeds 500MB or its virtual memory exceeds 505MB
> > (101 percent of the real memory limit). The default value is 0, which disables enforcement of
> > virtual memory limits. The value may not exceed 65533 percent.
> >
> > **NOTE**: This parameter is dependent on **OverMemoryKill** being configured in
> > **JobAcctGatherParams**. It is also possible to configure the **TaskPlugin** to use
> > **task/cgroup** for memory enforcement. **VSizeFactor** will not have an effect on memory
> > enforcement done through cgroups.
> >
> > <!-- -->
> >
> > **WaitTime**  
> > Specifies how many seconds the srun command should by default wait after the first task
> > terminates before terminating all remaining tasks. The "--wait" option on the srun command line
> > overrides this value. The default value is 0, which disables this feature. May not exceed 65533
> > seconds.
> >
> > <!-- -->
> >
> > **X11Parameters**  
> > For use with Slurm's built-in X11 forwarding implementation.
> >
> > > **home_xauthority**  
> > > If set, xauth data on the compute node will be placed in **~/.Xauthority** rather than in a
> > > temporary file under **TmpFS**.

# NODE CONFIGURATION

The configuration of nodes (or machines) to be managed by Slurm is also specified in
**/etc/slurm.conf**. Changes in node configuration (e.g. adding nodes, changing their processor
count, etc.) require restarting both the slurmctld daemon and the slurmd daemons. All slurmd daemons
must know each node in the system to forward messages in support of hierarchical communications.
Only the NodeName must be supplied in the configuration file. All other node configuration
information is optional. It is advisable to establish baseline node configurations, especially if
the cluster is heterogeneous. Nodes which register to the system with less than the configured
resources (e.g. too little memory), will be placed in the "DOWN" state to avoid scheduling jobs on
them. Establishing baseline configurations will also speed Slurm's scheduling process by permitting
it to compare job requirements against these (relatively few) configuration parameters and possibly
avoid having to check job requirements against every individual node's configuration. The resources
checked at node registration time are: CPUs, RealMemory and TmpDisk.

Default values can be specified with a record in which **NodeName** is "DEFAULT". The default entry
values will apply only to lines following it in the configuration file and the default values can be
reset multiple times in the configuration file with multiple entries where "NodeName=DEFAULT". Each
line where **NodeName** is "DEFAULT" will replace or add to previous default values and will not
reinitialize the default values. The "NodeName=" specification must be placed on every line
describing the configuration of nodes. A single node name can not appear as a NodeName value in more
than one line (duplicate node name records will be ignored). In fact, it is generally possible and
desirable to define the configurations of all nodes in only a few lines. This convention permits
significant optimization in the scheduling of larger clusters. In order to support the concept of
jobs requiring consecutive nodes on some architectures, node specifications should be place in this
file in consecutive order. No single node name may be listed more than once in the configuration
file. Use "DownNodes=" to record the state of nodes which are temporarily in a DOWN, DRAIN or
FAILING state without altering permanent configuration information. A job step's tasks are allocated
to nodes in order the nodes appear in the configuration file. There is presently no capability
within Slurm to arbitrarily order a job step's tasks.

Multiple node names may be comma separated (e.g. "alpha,beta,gamma") and/or a simple node range
expression may optionally be used to specify numeric ranges of nodes to avoid building a
configuration file with large numbers of entries. The node range expression can contain one pair of
square brackets with a sequence of comma-separated numbers and/or ranges of numbers separated by a
"-" (e.g. "linux\[0-64,128\]", or "lx\[15,18,32-33\]"). Note that the numeric ranges can include one
or more leading zeros to indicate the numeric portion has a fixed number of digits (e.g.
"linux\[0000-1023\]"). Multiple numeric ranges can be included in the expression (e.g.
"rack\[0-63\]\_blade\[0-41\]"). If one or more numeric expressions are included, one of them must be
at the end of the name (e.g. "unit\[0-31\]rack" is invalid), but arbitrary names can always be used
in a comma-separated list.

The node configuration specified the following information:

**NodeName**  
Name that Slurm uses to refer to a node. Typically this would be the string that "/bin/hostname -s"
returns. It may also be the fully qualified domain name as returned by "/bin/hostname -f" (e.g.
"foo1.bar.com"), or any valid domain name associated with the host through the host database
(/etc/hosts) or DNS, depending on the resolver settings. Note that if the short form of the hostname
is not used, it may prevent use of hostlist expressions (the numeric portion in brackets must be at
the end of the string). It may also be an arbitrary string if **NodeHostname** is specified. If the
**NodeName** is "DEFAULT", the values specified with that record will apply to subsequent node
specifications unless explicitly set to other values in that node record or replaced with a
different set of default values. Each line where **NodeName** is "DEFAULT" will replace or add to
previous default values and not reinitialize the default values. For architectures in which the node
order is significant, nodes will be considered consecutive in the order defined. For example, if the
configuration for "NodeName=charlie" immediately follows the configuration for "NodeName=baker" they
will be considered adjacent in the computer. **NOTE**: If the **NodeName** is "ALL" the process
parsing the configuration will exit immediately as it is an internally reserved word.

<!-- -->

**NodeHostname**  
Typically this would be the string that "/bin/hostname -s" returns. It may also be the fully
qualified domain name as returned by "/bin/hostname -f" (e.g. "foo1.bar.com"), or any valid domain
name associated with the host through the host database (/etc/hosts) or DNS, depending on the
resolver settings. Note that if the short form of the hostname is not used, it may prevent use of
hostlist expressions (the numeric portion in brackets must be at the end of the string). A node
range expression can be used to specify a set of nodes. If an expression is used, the number of
nodes identified by **NodeHostname** on a line in the configuration file must be identical to the
number of nodes identified by **NodeName**. By default, the **NodeHostname** will be identical in
value to **NodeName**.

<!-- -->

**NodeAddr**  
Name that a node should be referred to in establishing a communications path. This name will be used
as an argument to the getaddrinfo() function for identification. If a node range expression is used
to designate multiple nodes, they must exactly match the entries in the **NodeName** (e.g.
"NodeName=lx\[0-7\] NodeAddr=elx\[0-7\]"). **NodeAddr** may also contain IP addresses. By default,
the **NodeAddr** will be identical in value to **NodeHostname**.

<!-- -->

**BcastAddr**  
Alternate network path to be used for sbcast network traffic to a given node. This name will be used
as an argument to the getaddrinfo() function. If a node range expression is used to designate
multiple nodes, they must exactly match the entries in the **NodeName** (e.g. "NodeName=lx\[0-7\]
BcastAddr=elx\[0-7\]"). **BcastAddr** may also contain IP addresses. By default, the **BcastAddr**
is unset, and sbcast traffic will be routed to the **NodeAddr** for a given node. Note: cannot be
used with CommunicationParameters=NoInAddrAny.

<!-- -->

**Boards**  
Number of Baseboards in nodes with a baseboard controller. Note that when Boards is specified,
SocketsPerBoard, CoresPerSocket, and ThreadsPerCore should be specified. The default value is 1.

<!-- -->

**CoreSpecCount**  
Number of cores reserved for system use. Depending upon the **TaskPluginParam** option of
**SlurmdOffSpec**, the Slurm daemon slurmd may either be confined to these resources (the default)
or prevented from using these resources. Isolation of slurmd from user jobs may improve application
performance. A job can use these cores if AllowSpecResourcesUsage=yes and the user explicitly
requests less than the configured CoreSpecCount. If this option and **CpuSpecList** are both
designated for a node, an error is generated. For information on the algorithm used by Slurm to
select the cores refer to the core specialization documentation (
https://slurm.schedmd.com/core_spec.html ).

<!-- -->

**CoresPerSocket**  
Number of cores in a single physical processor socket (e.g. "2"). The CoresPerSocket value describes
physical cores, not the logical number of processors per socket. **NOTE**: If you have multi-core
processors, you will likely need to specify this parameter in order to optimize scheduling. The
default value is 1.

<!-- -->

**CpuBind**  
If a job step request does not specify an option to control how tasks are bound to allocated CPUs
(--cpu-bind) and all nodes allocated to the job have the same **CpuBind** option the node
**CpuBind** option will control how tasks are bound to allocated resources. Supported values for
**CpuBind** are "none", "socket", "ldom" (NUMA), "core" and "thread".

<!-- -->

**CPUs**  
Number of logical processors on the node (e.g. "2"). It can be set to the total number of
sockets(supported only by select/linear), cores or threads. This can be useful when you want to
schedule only the cores on a hyper-threaded node. If **CPUs** is omitted, its default will be set
equal to the product of **Boards**, **Sockets**, **CoresPerSocket**, and **ThreadsPerCore**.

<!-- -->

**CpuSpecList**  
A comma-delimited list of Slurm abstract CPU IDs reserved for system use. The list will be expanded
to include all other CPUs, if any, on the same cores. Depending upon the **TaskPluginParam** option
of **SlurmdOffSpec**, the Slurm daemon slurmd may either be confined to these resources (the
default) or prevented from using these resources. Isolation of slurmd from user jobs may improve
application performance. A job can use these cores if AllowSpecResourcesUsage=yes and the user
explicitly requests less than the number of CPUs in this list. If this option and **CoreSpecCount**
are both designated for a node, an error is generated. This option has no effect unless cgroup job
confinement is also configured (i.e. the *task/cgroup* **TaskPlugin** is enabled and
**ConstrainCores=yes** is set in cgroup.conf).

<!-- -->

**Features**  
A comma-delimited list of arbitrary strings indicative of some characteristic associated with the
node. There is no value or count associated with a feature at this time, a node either has a feature
or it does not. A desired feature may contain a numeric component indicating, for example, processor
speed but this numeric component will be considered to be part of the feature string. Features are
intended to be used to filter nodes eligible to run jobs via the **--constraint** argument. By
default a node has no features. Also see **Gres** for being able to have more control such as types
and count. Using features is faster than scheduling against GRES but is limited to Boolean
operations.

<!-- -->

**Gres**  
A comma-delimited list of generic resources specifications for a node. The format is:
"\<name\>\[:\<type\>\]\[:no_consume\]:\<number\>\[K\|M\|G\]". The first field is the resource name,
which matches the GresType configuration parameter name. The optional type field might be used to
identify a model of that generic resource. It is forbidden to specify both an untyped GRES and a
typed GRES with the same \<name\>. The optional no_consume field allows you to specify that a
generic resource does not have a finite number of that resource that gets consumed as it is
requested. The no_consume field is a GRES specific setting and applies to the GRES, regardless of
the type specified. It should not be used with GRES that has a dedicated plugin, if you're looking
for a way to overcommit GPUs to multiple processes at the time you may be interested in using
"shard" GRES instead. The final field must specify a generic resources count. A suffix of "K", "M",
"G", "T" or "P" may be used to multiply the number by 1024, 1048576, 1073741824, etc. respectively.
(e.g."Gres=gpu:tesla:1,gpu:kepler:1,bandwidth:lustre:no_consume:4G"). By default a node has no
generic resources and its maximum count is that of an unsigned 64bit integer. Also see **Features**
for Boolean flags to filter nodes using job constraints.

<!-- -->

**MemSpecLimit**  
Amount of **RealMemory**, in megabytes, reserved for system use and not available for user
allocations. Must be less than the amount defined for **RealMemory**. If the task/cgroup plugin is
configured and that plugin constrains memory allocations (i.e. the *task/cgroup* **TaskPlugin** is
enabled and **ConstrainRAMSpace=yes** is set in cgroup.conf), then Slurm compute node daemons
(slurmd plus slurmstepd) will be allocated the specified memory limit. Note that having the Memory
set in **SelectTypeParameters** as any of the options that has it as a consumable resource is needed
for this option to work. The daemons will not be killed if they exhaust the memory allocation (i.e.
the Out-Of-Memory Killer is disabled for the daemon's memory cgroup). If the task/cgroup plugin is
not configured, the specified memory will only be unavailable for user allocations.

<!-- -->

**Port**  
The port number that the Slurm compute node daemon, **slurmd**, listens to for work on this
particular node. By default there is a single port number for all **slurmd** daemons on all compute
nodes as defined by the **SlurmdPort** configuration parameter. Use of this option is not generally
recommended except for development or testing purposes. If multiple **slurmd** daemons execute on a
node this can specify a range of ports.

**Note**: On Cray systems, Realm-Specific IP Addressing (RSIP) will automatically try to interact
with anything opened on ports 8192-60000. Configure Port to use a port outside of the configured
SrunPortRange and RSIP's port range.

<!-- -->

**Procs**  
See **CPUs**.

<!-- -->

**RealMemory**  
Size of real memory on the node in megabytes (e.g. "2048"). The default value is 1. Lowering
RealMemory with the goal of setting aside some amount for the OS and not available for job
allocations will not work as intended if Memory is not set as a consumable resource in
**SelectTypeParameters**. So one of the \*\_Memory options need to be enabled for that goal to be
accomplished. Also see **MemSpecLimit**.

<!-- -->

**Reason**  
Identifies the reason for a node being in state "DOWN", "DRAINED" "DRAINING", "FAIL" or "FAILING".
Use quotes to enclose a reason having more than one word.

<!-- -->

**Sockets**  
Number of physical processor sockets/chips on the node (e.g. "2"). If Sockets is omitted, it will be
inferred from **CPUs**, **CoresPerSocket**, and **ThreadsPerCore**. **NOTE**: If you have multi-core
processors, you will likely need to specify these parameters. Sockets and SocketsPerBoard are
mutually exclusive. If Sockets is specified when Boards is also used, Sockets is interpreted as
SocketsPerBoard rather than total sockets. The default value is 1.

<!-- -->

**SocketsPerBoard**  
Number of physical processor sockets/chips on a baseboard. Sockets and SocketsPerBoard are mutually
exclusive. The default value is 1.

<!-- -->

**State**  
State of the node with respect to the initiation of user jobs. Acceptable values are *CLOUD*,
*DOWN*, *DRAIN*, *FAIL*, *FAILING*, *FUTURE* and *UNKNOWN*. Node states of *BUSY* and *IDLE* should
not be specified in the node configuration, but set the node state to *UNKNOWN* instead. Setting the
node state to *UNKNOWN* will result in the node state being set to *BUSY*, *IDLE* or other
appropriate state based upon recovered system state information. The default value is *UNKNOWN*.
Also see the **DownNodes** parameter below.

> **CLOUD**  
> Indicates the node exists in the cloud. Its initial state will be treated as powered down. The
> node will be available for use after its state is recovered from Slurm's state save file or the
> slurmd daemon starts on the compute node.
>
> <!-- -->
>
> **DOWN**  
> Indicates the node failed and is unavailable to be allocated work.
>
> <!-- -->
>
> **DRAIN**  
> Indicates the node is unavailable to be allocated work.
>
> <!-- -->
>
> **FAIL**  
> Indicates the node is expected to fail soon, has no jobs allocated to it, and will not be
> allocated to any new jobs.
>
> <!-- -->
>
> **FAILING**  
> Indicates the node is expected to fail soon, has one or more jobs allocated to it, but will not be
> allocated to any new jobs.
>
> <!-- -->
>
> **FUTURE**  
> Indicates the node is defined for future use and need not exist when the Slurm daemons are
> started. These nodes can be made available for use simply by updating the node state using the
> scontrol command rather than restarting the slurmctld daemon. After these nodes are made
> available, change their State in the slurm.conf file. Until these nodes are made available, they
> will not be seen using any Slurm commands or nor will any attempt be made to contact them.
>
> > **Dynamic Future Nodes**  
> > A **slurmd** started with -F\[\<feature\>\] will be associated with a FUTURE node that matches
> > the same configuration (sockets, cores, threads) as reported by **slurmd** -C. The node's
> > NodeAddr and NodeHostname will automatically be retrieved from the **slurmd** and will be
> > cleared when set back to the FUTURE state. Dynamic FUTURE nodes retain non-FUTURE state on
> > restart. Use scontrol to put node back into FUTURE state.
> >
> > If the mapping of the NodeName to the **slurmd** HostName is not updated in DNS, Dynamic Future
> > nodes won't know how to communicate with each other -- because NodeAddr and NodeHostName are not
> > defined in the slurm.conf -- and the fanout communications need to be disabled by setting
> > TreeWidth to a high number (e.g. 65533). If the DNS mapping is made, then the **cloud_dns**
> > **SlurmctldParameter** can be used.
>
> **UNKNOWN**  
> Indicates the node's state is undefined but will be established (set to *BUSY* or *IDLE*) when the
> **slurmd** daemon on that node registers. *UNKNOWN* is the default state.

**ThreadsPerCore**  
Number of logical threads in a single physical core (e.g. "2"). Note that the Slurm can allocate
resources to jobs down to the resolution of a core. If your system is configured with more than one
thread per core, execution of a different job on each thread is not supported unless you configure
**SelectTypeParameters=CR_CPU** plus **CPUs**; do not configure **Sockets**, **CoresPerSocket** or
**ThreadsPerCore**. A job can execute a one task per thread from within one job step or execute a
distinct job step on each of the threads. Note also if you are running with more than 1 thread per
core and running the select/cons_res or select/cons_tres plugin then you will want to set the
SelectTypeParameters variable to something other than CR_CPU to avoid unexpected results. The
default value is 1.

<!-- -->

**TmpDisk**  
Total size of temporary disk storage in **TmpFS** in megabytes (e.g. "16384"). **TmpFS** (for
"Temporary File System") identifies the location which jobs should use for temporary storage. Note
this does not indicate the amount of free space available to the user on the node, only the total
file system size. The system administration should ensure this file system is purged as needed so
that user jobs have access to most of this space. The Prolog and/or Epilog programs (specified in
the configuration file) might be used to ensure the file system is kept clean. The default value is
0.

<!-- -->

**Weight**  
The priority of the node for scheduling purposes. All things being equal, jobs will be allocated the
nodes with the lowest weight which satisfies their requirements. For example, a heterogeneous
collection of nodes might be placed into a single partition for greater system utilization,
responsiveness and capability. It would be preferable to allocate smaller memory nodes rather than
larger memory nodes if either will satisfy a job's requirements. The units of weight are arbitrary,
but larger weights should be assigned to nodes with more processors, memory, disk space, higher
processor speed, etc. Note that if a job allocation request can not be satisfied using the nodes
with the lowest weight, the set of nodes with the next lowest weight is added to the set of nodes
under consideration for use (repeat as needed for higher weight values). If you absolutely want to
minimize the number of higher weight nodes allocated to a job (at a cost of higher scheduling
overhead), give each node a distinct **Weight** value and they will be added to the pool of nodes
being considered for scheduling individually.

The default value is 1.

**NOTE**: Node weights are first considered among currently available nodes. For example, a
POWERED_DOWN node with a lower weight will not be evaluated before an IDLE node.

# DOWN NODE CONFIGURATION

The **DownNodes=** parameter permits you to mark certain nodes as in a *DOWN*, *DRAIN*, *FAIL*,
*FAILING* or *FUTURE* state without altering the permanent configuration information listed under a
**NodeName=** specification.

**DownNodes**  
Any node name, or list of node names, from the **NodeName=** specifications.

<!-- -->

**Reason**  
Identifies the reason for a node being in state *DOWN*, *DRAIN*, *FAIL*, *FAILING* or *FUTURE*. Use
quotes to enclose a reason having more than one word.

<!-- -->

**State**  
State of the node with respect to the initiation of user jobs. Acceptable values are *DOWN*,
*DRAIN*, *FAIL*, *FAILING* and *FUTURE*. For more information about these states see the
descriptions under **State** in the **NodeName=** section above. The default value is *DOWN*.

# FRONTEND NODE CONFIGURATION

On computers where frontend nodes are used to execute batch scripts rather than compute nodes, one
may configure one or more frontend nodes using the configuration parameters defined below. These
options are very similar to those used in configuring compute nodes. These options may only be used
on systems configured and built with the appropriate parameters (--enable-front-end). The front end
configuration specifies the following information:

**AllowGroups**  
Comma-separated list of group names which may execute jobs on this front end node. By default, all
groups may use this front end node. A user will be permitted to use this front end node if
AllowGroups has **at least one** group associated with the user. May not be used with the
**DenyGroups** option.

<!-- -->

**AllowUsers**  
Comma-separated list of user names which may execute jobs on this front end node. By default, all
users may use this front end node. May not be used with the **DenyUsers** option.

<!-- -->

**DenyGroups**  
Comma-separated list of group names which are prevented from executing jobs on this front end node.
May not be used with the **AllowGroups** option.

<!-- -->

**DenyUsers**  
Comma-separated list of user names which are prevented from executing jobs on this front end node.
May not be used with the **AllowUsers** option.

<!-- -->

**FrontendName**  
Name that Slurm uses to refer to a frontend node. Typically this would be the string that
"/bin/hostname -s" returns. It may also be the fully qualified domain name as returned by
"/bin/hostname -f" (e.g. "foo1.bar.com"), or any valid domain name associated with the host through
the host database (/etc/hosts) or DNS, depending on the resolver settings. Note that if the short
form of the hostname is not used, it may prevent use of hostlist expressions (the numeric portion in
brackets must be at the end of the string). If the **FrontendName** is "DEFAULT", the values
specified with that record will apply to subsequent node specifications unless explicitly set to
other values in that frontend node record or replaced with a different set of default values. Each
line where **FrontendName** is "DEFAULT" will replace or add to previous default values and not
reinitialize the default values.

<!-- -->

**FrontendAddr**  
Name that a frontend node should be referred to in establishing a communications path. This name
will be used as an argument to the getaddrinfo() function for identification. As with
**FrontendName**, list the individual node addresses rather than using a hostlist expression. The
number of **FrontendAddr** records per line must equal the number of **FrontendName** records per
line (i.e. you can't map to node names to one address). **FrontendAddr** may also contain IP
addresses. By default, the **FrontendAddr** will be identical in value to **FrontendName**.

<!-- -->

**Port**  
The port number that the Slurm compute node daemon, **slurmd**, listens to for work on this
particular frontend node. By default there is a single port number for all **slurmd** daemons on all
frontend nodes as defined by the **SlurmdPort** configuration parameter. Use of this option is not
generally recommended except for development or testing purposes.

**Note**: On Cray systems, Realm-Specific IP Addressing (RSIP) will automatically try to interact
with anything opened on ports 8192-60000. Configure Port to use a port outside of the configured
SrunPortRange and RSIP's port range.

<!-- -->

**Reason**  
Identifies the reason for a frontend node being in state *DOWN*, *DRAINED*, *DRAINING*, *FAIL* or
*FAILING*. Use quotes to enclose a reason having more than one word.

<!-- -->

**State**  
State of the frontend node with respect to the initiation of user jobs. Acceptable values are
*DOWN*, *DRAIN*, *FAIL*, *FAILING* and *UNKNOWN*. Node states of *BUSY* and *IDLE* should not be
specified in the node configuration, but set the node state to *UNKNOWN* instead. Setting the node
state to *UNKNOWN* will result in the node state being set to *BUSY*, *IDLE* or other appropriate
state based upon recovered system state information. For more information about these states see the
descriptions under **State** in the **NodeName=** section above. The default value is *UNKNOWN*.

As an example, you can do something similar to the following to define four front end nodes for
running slurmd daemons.

    FrontendName=frontend[00-03] FrontendAddr=efrontend[00-03] State=UNKNOWN

# NODESET CONFIGURATION

The nodeset configuration allows you to define a name for a specific set of nodes which can be used
to simplify the partition configuration section, especially for heterogenous or condo-style systems.
Each nodeset may be defined by an explicit list of nodes, and/or by filtering the nodes by a
particular configured feature. If both **Feature=** and **Nodes=** are used the nodeset shall be the
union of the two subsets. Note that the nodesets are only used to simplify the partition definitions
at present, and are not usable outside of the partition configuration.

**Feature**  
All nodes with this single feature will be included as part of this nodeset.

<!-- -->

**Nodes**  
List of nodes in this set.

<!-- -->

**NodeSet**  
Unique name for a set of nodes. Must not overlap with any NodeName definitions.

# PARTITION CONFIGURATION

The partition configuration permits you to establish different job limits or access controls for
various groups (or partitions) of nodes. Nodes may be in more than one partition, making partitions
serve as general purpose queues. For example one may put the same set of nodes into two different
partitions, each with different constraints (time limit, job sizes, groups allowed to use the
partition, etc.). Jobs are allocated resources within a single partition. Default values can be
specified with a record in which **PartitionName** is "DEFAULT". The default entry values will apply
only to lines following it in the configuration file and the default values can be reset multiple
times in the configuration file with multiple entries where "PartitionName=DEFAULT". The
"PartitionName=" specification must be placed on every line describing the configuration of
partitions. Each line where **PartitionName** is "DEFAULT" will replace or add to previous default
values and not reinitialize the default values. A single partition name can not appear as a
PartitionName value in more than one line (duplicate partition name records will be ignored). If a
partition that is in use is deleted from the configuration and slurm is restarted or reconfigured
(scontrol reconfigure), jobs using the partition are canceled. **NOTE**: Put all parameters for each
partition on a single line. Each line of partition configuration information should represent a
different partition. The partition configuration file contains the following information:

**AllocNodes**  
Comma-separated list of nodes from which users can submit jobs in the partition. Node names may be
specified using the node range expression syntax described above. The default value is "ALL".

<!-- -->

**AllowAccounts**  
Comma-separated list of accounts which may execute jobs in the partition. The default value is
"ALL". This list is also hierarchical, meaning subaccounts are included automatically. **NOTE**: If
AllowAccounts is used then DenyAccounts will not be enforced. Also refer to DenyAccounts.

<!-- -->

**AllowGroups**  
Comma-separated list of group names which may execute jobs in this partition. A user will be
permitted to submit a job to this partition if AllowGroups has **at least one** group associated
with the user. Jobs executed as user root or as user SlurmUser will be allowed to use any partition,
regardless of the value of AllowGroups. In addition, a Slurm Admin or Operator will be able to view
any partition, regardless of the value of AllowGroups. If user root attempts to execute a job as
another user (e.g. using srun's --uid option), then the job will be subject to AllowGroups as if it
were submitted by that user. By default, AllowGroups is unset, meaning all groups are allowed to use
this partition. The special value 'ALL' is equivalent to this. Users who are not members of the
specified group will not see information about this partition by default. However, this should not
be treated as a security mechanism, since job information will be returned if a user requests
details about the partition or a specific job. See the **PrivateData** parameter to restrict access
to job information. **NOTE**: For performance reasons, Slurm maintains a list of user IDs allowed to
use each partition and this is checked at job submission time. This list of user IDs is updated when
the **slurmctld** daemon is restarted, reconfigured (e.g. "scontrol reconfig") or the partition's
**AllowGroups** value is reset, even if is value is unchanged (e.g. "scontrol update
PartitionName=name AllowGroups=group"). For a user's access to a partition to change, both his group
membership must change and Slurm's internal user ID list must change using one of the methods
described above.

<!-- -->

**AllowQos**  
Comma-separated list of Qos which may execute jobs in the partition. Jobs executed as user root can
use any partition without regard to the value of AllowQos. The default value is "ALL". **NOTE**: If
AllowQos is used then DenyQos will not be enforced. Also refer to DenyQos.

<!-- -->

**Alternate**  
Partition name of alternate partition to be used if the state of this partition is "DRAIN" or
"INACTIVE."

<!-- -->

**CpuBind**  
If a job step request does not specify an option to control how tasks are bound to allocated CPUs
(--cpu-bind) and all nodes allocated to the job do not have the same **CpuBind** option the node.
Then the partition's **CpuBind** option will control how tasks are bound to allocated resources.
Supported values for**CpuBind** are "none", "socket", "ldom" (NUMA), "core" and "thread".

<!-- -->

**Default**  
If this keyword is set, jobs submitted without a partition specification will utilize this
partition. Possible values are "YES" and "NO". The default value is "NO".

<!-- -->

**DefaultTime**  
Run time limit used for jobs that don't specify a value. If not set then MaxTime will be used.
Format is the same as for MaxTime.

<!-- -->

**DefCpuPerGPU**  
Default count of CPUs allocated per allocated GPU. This value is used only if the job didn't specify
--cpus-per-task and --cpus-per-gpu.

<!-- -->

**DefMemPerCPU**  
Default real memory size available per allocated CPU in megabytes. Used to avoid over-subscribing
memory and causing paging. **DefMemPerCPU** would generally be used if individual processors are
allocated to jobs (**SelectType=select/cons_res** or **SelectType=select/cons_tres**). If not set,
the **DefMemPerCPU** value for the entire cluster will be used. Also see **DefMemPerGPU**,
**DefMemPerNode** and **MaxMemPerCPU**. **DefMemPerCPU**, **DefMemPerGPU** and **DefMemPerNode** are
mutually exclusive.

<!-- -->

**DefMemPerGPU**  
Default real memory size available per allocated GPU in megabytes. Also see **DefMemPerCPU**,
**DefMemPerNode** and **MaxMemPerCPU**. **DefMemPerCPU**, **DefMemPerGPU** and **DefMemPerNode** are
mutually exclusive.

<!-- -->

**DefMemPerNode**  
Default real memory size available per allocated node in megabytes. Used to avoid over-subscribing
memory and causing paging. **DefMemPerNode** would generally be used if whole nodes are allocated to
jobs (**SelectType=select/linear**) and resources are over-subscribed (**OverSubscribe=yes** or
**OverSubscribe=force**). If not set, the **DefMemPerNode** value for the entire cluster will be
used. Also see **DefMemPerCPU**, **DefMemPerGPU** and **MaxMemPerCPU**. **DefMemPerCPU**,
**DefMemPerGPU** and **DefMemPerNode** are mutually exclusive.

<!-- -->

**DenyAccounts**  
Comma-separated list of accounts which may not execute jobs in the partition. By default, no
accounts are denied access. This list is also hierarchical, meaning subaccounts are included
automatically. **NOTE**: If AllowAccounts is used then DenyAccounts will not be enforced. Also refer
to AllowAccounts.

<!-- -->

**DenyQos**  
Comma-separated list of Qos which may not execute jobs in the partition. By default, no QOS are
denied access **NOTE**: If AllowQos is used then DenyQos will not be enforced. Also refer AllowQos.

<!-- -->

**DisableRootJobs**  
If set to "YES" then user root will be prevented from running any jobs on this partition. The
default value will be the value of **DisableRootJobs** set outside of a partition specification
(which is "NO", allowing user root to execute jobs).

<!-- -->

**ExclusiveUser**  
If set to "YES" then nodes will be exclusively allocated to users. Multiple jobs may be run for the
same user, but only one user can be active at a time. This capability is also available on a per-job
basis by using the **--exclusive=user** option.

<!-- -->

**GraceTime**  
Specifies, in units of seconds, the preemption grace time to be extended to a job which has been
selected for preemption. The default value is zero, no preemption grace time is allowed on this
partition. Once a job has been selected for preemption, its end time is set to the current time plus
GraceTime. The job's tasks are immediately sent SIGCONT and SIGTERM signals in order to provide
notification of its imminent termination. This is followed by the SIGCONT, SIGTERM and SIGKILL
signal sequence upon reaching its new end time. This second set of signals is sent to both the tasks
**and** the containing batch script, if applicable. See also the global **KillWait** configuration
parameter.

<!-- -->

**Hidden**  
Specifies if the partition and its jobs are to be hidden by default. Hidden partitions will by
default not be reported by the Slurm APIs or commands. Possible values are "YES" and "NO". The
default value is "NO". Note that partitions that a user lacks access to by virtue of the
**AllowGroups** parameter will also be hidden by default.

<!-- -->

**LLN**  
Schedule resources to jobs on the least loaded nodes (based upon the number of idle CPUs). This is
generally only recommended for an environment with serial jobs as idle resources will tend to be
highly fragmented, resulting in parallel jobs being distributed across many nodes. Note that node
**Weight** takes precedence over how many idle resources are on each node. Also see the
**SelectTypeParameters** configuration parameter **CR_LLN** to use the least loaded nodes in every
partition.

<!-- -->

**MaxCPUsPerNode**  
Maximum number of CPUs on any node available to all jobs from this partition. This can be especially
useful to schedule GPUs. For example a node can be associated with two Slurm partitions (e.g. "cpu"
and "gpu") and the partition/queue "cpu" could be limited to only a subset of the node's CPUs,
ensuring that one or more CPUs would be available to jobs in the "gpu" partition/queue. Also see
**MaxCPUsPerSocket**.

<!-- -->

**MaxCPUsPerSocket**  
Maximum number of CPUs on any node available on the all jobs from this partition. This can be
especially useful to schedule GPUs. Also see **MaxCPUsPerNode**.

<!-- -->

**MaxMemPerCPU**  
Maximum real memory size available per allocated CPU in megabytes. Used to avoid over-subscribing
memory and causing paging. **MaxMemPerCPU** would generally be used if individual processors are
allocated to jobs (**SelectType=select/cons_res** or **SelectType=select/cons_tres**). If not set,
the **MaxMemPerCPU** value for the entire cluster will be used. Also see **DefMemPerCPU** and
**MaxMemPerNode**. **MaxMemPerCPU** and **MaxMemPerNode** are mutually exclusive.

<!-- -->

**MaxMemPerNode**  
Maximum real memory size available per allocated node in megabytes. Used to avoid over-subscribing
memory and causing paging. **MaxMemPerNode** would generally be used if whole nodes are allocated to
jobs (**SelectType=select/linear**) and resources are over-subscribed (**OverSubscribe=yes** or
**OverSubscribe=force**). If not set, the **MaxMemPerNode** value for the entire cluster will be
used. Also see **DefMemPerNode** and **MaxMemPerCPU**. **MaxMemPerCPU** and **MaxMemPerNode** are
mutually exclusive.

<!-- -->

**MaxNodes**  
Maximum count of nodes which may be allocated to any single job. The default value is "UNLIMITED",
which is represented internally as -1.

<!-- -->

**MaxTime**  
Maximum run time limit for jobs. Format is minutes, minutes:seconds, hours:minutes:seconds,
days-hours, days-hours:minutes, days-hours:minutes:seconds or "UNLIMITED". Time resolution is one
minute and second values are rounded up to the next minute. The job TimeLimit may be updated by
root, SlurmUser or an Operator to a value higher than the configured MaxTime after job submission.

<!-- -->

**MinNodes**  
Minimum count of nodes which may be allocated to any single job. The default value is 0.

<!-- -->

**Nodes**  
Comma-separated list of nodes or nodesets which are associated with this partition. Node names may
be specified using the node range expression syntax described above. A blank list of nodes (i.e.
Nodes="") can be used if one wants a partition to exist, but have no resources (possibly on a
temporary basis). A value of "ALL" is mapped to all nodes configured in the cluster.

<!-- -->

**OverSubscribe**  
Controls the ability of the partition to execute more than one job at a time on each resource (node,
socket or core depending upon the value of **SelectTypeParameters**). If resources are to be
over-subscribed, avoiding memory over-subscription is very important. **SelectTypeParameters**
should be configured to treat memory as a consumable resource and the **--mem** option should be
used for job allocations. Sharing of resources is typically useful only when using gang scheduling
(**PreemptMode=suspend,gang**). Possible values for **OverSubscribe** are "EXCLUSIVE", "FORCE",
"YES", and "NO". Note that a value of "YES" or "FORCE" can negatively impact performance for systems
with many thousands of running jobs. The default value is "NO". For more information see the
following web pages:  

*https://slurm.schedmd.com/cons_res.html*  
*https://slurm.schedmd.com/cons_res_share.html*  
*https://slurm.schedmd.com/gang_scheduling.html*  
*https://slurm.schedmd.com/preempt.html*

> **EXCLUSIVE**  
> Allocates entire nodes to jobs even with **SelectType=select/cons_res** or
> **SelectType=select/cons_tres** configured. Jobs that run in partitions with
> **OverSubscribe=EXCLUSIVE** will have exclusive access to all allocated nodes. These jobs are
> allocated all CPUs and GRES on the nodes, but they are only allocated as much memory as they ask
> for. This is by design to support gang scheduling, because suspended jobs still reside in memory.
> To request all the memory on a node, use **--mem=0** at submit time.
>
> <!-- -->
>
> **FORCE**  
> Makes all resources (except GRES) in the partition available for oversubscription without any
> means for users to disable it. May be followed with a colon and maximum number of jobs in running
> or suspended state. For example **OverSubscribe=FORCE:4** enables each node, socket or core to
> oversubscribe each resource four ways. Recommended only for systems using
> **PreemptMode=suspend,gang**.
>
> **NOTE**: **OverSubscribe=FORCE:1** is a special case that is not exactly equivalent to
> **OverSubscribe=NO**. **OverSubscribe=FORCE:1** disables the regular oversubscription of resources
> in the same partition but it will still allow oversubscription due to preemption or on overlapping
> partitions with the same PriorityTier. Setting **OverSubscribe=NO** will prevent oversubscription
> from happening in all cases.
>
> **NOTE**: If using **PreemptType=preempt/qos** you can specify a value for **FORCE** that is
> greater than 1. For example, **OverSubscribe=FORCE:2** will permit two jobs per resource normally,
> but a third job can be started only if done so through preemption based upon QOS.
>
> **NOTE**: If **OverSubscribe** is configured to **FORCE** or **YES** in your slurm.conf and the
> system is not configured to use preemption (**PreemptMode=OFF**) accounting can easily grow to
> values greater than the actual utilization. It may be common on such systems to get error messages
> in the slurmdbd log stating: "We have more allocated time than is possible."
>
> <!-- -->
>
> **YES**  
> Makes all resources (except GRES) in the partition available for sharing upon request by the job.
> Resources will only be over-subscribed when explicitly requested by the user using the
> "--oversubscribe" option on job submission. May be followed with a colon and maximum number of
> jobs in running or suspended state. For example "OverSubscribe=YES:4" enables each node, socket or
> core to execute up to four jobs at once. Recommended only for systems running with gang scheduling
> (**PreemptMode=suspend,gang**).
>
> <!-- -->
>
> **NO**  
> Selected resources are allocated to a single job. No resource will be allocated to more than one
> job.
>
> **NOTE**: Even if you are using **PreemptMode=suspend,gang**, setting **OverSubscribe=NO** will
> disable preemption on that partition. Use **OverSubscribe=FORCE:1** if you want to disable normal
> oversubscription but still allow suspension due to preemption.

**OverTimeLimit**  
Number of minutes by which a job can exceed its time limit before being canceled. Normally a job's
time limit is treated as a *hard* limit and the job will be killed upon reaching that limit.
Configuring **OverTimeLimit** will result in the job's time limit being treated like a *soft* limit.
Adding the **OverTimeLimit** value to the *soft* time limit provides a *hard* time limit, at which
point the job is canceled. This is particularly useful for backfill scheduling, which bases upon
each job's soft time limit. If not set, the **OverTimeLimit** value for the entire cluster will be
used. May not exceed 65533 minutes. A value of "UNLIMITED" is also supported.

<!-- -->

**PartitionName**  
Name by which the partition may be referenced (e.g. "Interactive"). This name can be specified by
users when submitting jobs. If the **PartitionName** is "DEFAULT", the values specified with that
record will apply to subsequent partition specifications unless explicitly set to other values in
that partition record or replaced with a different set of default values. Each line where
**PartitionName** is "DEFAULT" will replace or add to previous default values and not reinitialize
the default values.

<!-- -->

**PowerDownOnIdle**  
If set to "YES" and power saving is enabled for the partition, then nodes allocated from this
partition will be requested to power down after being allocated at least one job. These nodes will
not power down until they transition from COMPLETING to IDLE. If set to "NO" then power saving will
operate as configured for the partition. The default value is "NO". See
\<https://slurm.schedmd.com/power_save.html\> and
\<https://slurm.schedmd.com/elastic_computing.html\> for more details.

**NOTE**: The following will cause a transition from COMPLETING to IDLE:  
Completing all running jobs without additional jobs being allocated.  
ExclusiveUser=YES and after all running jobs complete but before another user's job is allocated.  
OverSubscribe=EXCLUSIVE and after the running job completes but before another job is allocated.

**NOTE**: Nodes are still subject to powering down when being IDLE for **SuspendTime**.

Also see **SuspendTime**.

<!-- -->

**PreemptMode**  
Mechanism used to preempt jobs or enable gang scheduling for this partition when
**PreemptType=preempt/partition_prio** is configured. This partition-specific **PreemptMode**
configuration parameter will override the cluster-wide **PreemptMode** for this partition. It can be
set to OFF to disable preemption and gang scheduling for this partition. See also **PriorityTier**
and the above description of the cluster-wide **PreemptMode** parameter for further details.  
The **GANG** option is used to enable gang scheduling independent of whether preemption is enabled
(i.e. independent of the **PreemptType** setting). It can be specified in addition to a
**PreemptMode** setting with the two options comma separated (e.g. **PreemptMode=SUSPEND,GANG**).  
See \<https://slurm.schedmd.com/preempt.html\> and
\<https://slurm.schedmd.com/gang_scheduling.html\> for more details.

**NOTE**: For performance reasons, the backfill scheduler reserves whole nodes for jobs, not partial
nodes. If during backfill scheduling a job preempts one or more other jobs, the whole nodes for
those preempted jobs are reserved for the preemptor job, even if the preemptor job requested fewer
resources than that. These reserved nodes aren't available to other jobs during that backfill cycle,
even if the other jobs could fit on the nodes. Therefore, jobs may preempt more resources during a
single backfill iteration than they requested.  
**NOTE**: For heterogeneous job to be considered for preemption all components must be eligible for
preemption. When a heterogeneous job is to be preempted the first identified component of the job
with the highest order PreemptMode (**SUSPEND** (highest), **REQUEUE**, **CANCEL** (lowest)) will be
used to set the PreemptMode for all components. The **GraceTime** and user warning signal for each
component of the heterogeneous job remain unique. Heterogeneous jobs are excluded from GANG
scheduling operations.

> **OFF**  
> Is the default value and disables job preemption and gang scheduling. It is only compatible with
> **PreemptType=preempt/none** at a global level. A common use case for this parameter is to set it
> on a partition to disable preemption for that partition.
>
> <!-- -->
>
> **CANCEL**  
> The preempted job will be cancelled.
>
> <!-- -->
>
> **GANG**  
> Enables gang scheduling (time slicing) of jobs in the same partition, and allows the resuming of
> suspended jobs.
>
> **NOTE**: Gang scheduling is performed independently for each partition, so if you only want
> time-slicing by **OverSubscribe**, without any preemption, then configuring partitions with
> overlapping nodes is not recommended. On the other hand, if you want to use
> **PreemptType=preempt/partition_prio** to allow jobs from higher PriorityTier partitions to
> Suspend jobs from lower PriorityTier partitions you will need overlapping partitions, and
> **PreemptMode=SUSPEND,GANG** to use the Gang scheduler to resume the suspended jobs(s). In any
> case, time-slicing won't happen between jobs on different partitions.  
> **NOTE**: Heterogeneous jobs are excluded from GANG scheduling operations.
>
> <!-- -->
>
> **REQUEUE**  
> Preempts jobs by requeuing them (if possible) or canceling them. For jobs to be requeued they must
> have the --requeue sbatch option set or the cluster wide JobRequeue parameter in slurm.conf must
> be set to **1**.
>
> <!-- -->
>
> **SUSPEND**  
> The preempted jobs will be suspended, and later the Gang scheduler will resume them. Therefore the
> **SUSPEND** preemption mode always needs the **GANG** option to be specified at the cluster level.
> Also, because the suspended jobs will still use memory on the allocated nodes, Slurm needs to be
> able to track memory resources to be able to suspend jobs.
>
> If the preemptees and preemptor are on different partitions then the preempted jobs will remain
> suspended until the preemptor ends.  
> **NOTE**: Because gang scheduling is performed independently for each partition, if using
> **PreemptType=preempt/partition_prio** then jobs in higher PriorityTier partitions will suspend
> jobs in lower PriorityTier partitions to run on the released resources. Only when the preemptor
> job ends will the suspended jobs will be resumed by the Gang scheduler.  
> **NOTE**: Suspended jobs will not release GRES. Higher priority jobs will not be able to preempt
> to gain access to GRES.

**PriorityJobFactor**  
Partition factor used by priority/multifactor plugin in calculating job priority. The value may not
exceed 65533. Also see PriorityTier.

<!-- -->

**PriorityTier**  
Jobs submitted to a partition with a higher **PriorityTier** value will be evaluated by the
scheduler before pending jobs in a partition with a lower **PriorityTier** value. They will also be
considered for preemption of running jobs in partition(s) with lower **PriorityTier** values if
*PreemptType=preempt/partition_prio*. The value may not exceed 65533. Also see PriorityJobFactor.

<!-- -->

**QOS**  
Used to extend the limits available to a QOS on a partition. Jobs will not be associated to this QOS
outside of being associated to the partition. They will still be associated to their requested QOS.
By default, no QOS is used. **NOTE**: If a limit is set in both the Partition's QOS and the Job's
QOS the Partition QOS will be honored unless the Job's QOS has the **OverPartQOS** flag set in which
the Job's QOS will have priority.

<!-- -->

**ReqResv**  
Specifies users of this partition are required to designate a reservation when submitting a job.
This option can be useful in restricting usage of a partition that may have higher priority or
additional resources to be allowed only within a reservation. Possible values are "YES" and "NO".
The default value is "NO".

<!-- -->

**ResumeTimeout**  
Maximum time permitted (in seconds) between when a node resume request is issued and when the node
is actually available for use. Nodes which fail to respond in this time frame will be marked DOWN
and the jobs scheduled on the node requeued. Nodes which reboot after this time frame will be marked
DOWN with a reason of "Node unexpectedly rebooted." For nodes that are in multiple partitions with
this option set, the highest time will take effect. If not set on any partition, the node will use
the **ResumeTimeout** value set for the entire cluster.

<!-- -->

**RootOnly**  
Specifies if only user ID zero (i.e. user *root*) may allocate resources in this partition. User
root may allocate resources for any other user, but the request must be initiated by user root. This
option can be useful for a partition to be managed by some external entity (e.g. a higher-level job
manager) and prevents users from directly using those resources. Possible values are "YES" and "NO".
The default value is "NO".

<!-- -->

**SelectTypeParameters**  
Partition-specific resource allocation type. This option replaces the global
**SelectTypeParameters** value. Supported values are **CR_Core**, **CR_Core_Memory**, **CR_Socket**
and **CR_Socket_Memory**. Use requires the system-wide **SelectTypeParameters** value be set to any
of the four supported values previously listed; otherwise, the partition-specific value will be
ignored.

<!-- -->

**Shared**  
The **Shared** configuration parameter has been replaced by the **OverSubscribe** parameter
described above.

<!-- -->

**State**  
State of partition or availability for use. Possible values are "UP", "DOWN", "DRAIN" and
"INACTIVE". The default value is "UP". See also the related "Alternate" keyword.

> **UP**  
> Designates that new jobs may be queued on the partition, and that jobs may be allocated nodes and
> run from the partition.
>
> <!-- -->
>
> **DOWN**  
> Designates that new jobs may be queued on the partition, but queued jobs may not be allocated
> nodes and run from the partition. Jobs already running on the partition continue to run. The jobs
> must be explicitly canceled to force their termination.
>
> <!-- -->
>
> **DRAIN**  
> Designates that no new jobs may be queued on the partition (job submission requests will be denied
> with an error message), but jobs already queued on the partition may be allocated nodes and run.
> See also the "Alternate" partition specification.
>
> <!-- -->
>
> **INACTIVE**  
> Designates that no new jobs may be queued on the partition, and jobs already queued may not be
> allocated nodes and run. See also the "Alternate" partition specification.

**SuspendTime**  
Nodes which remain idle or down for this number of seconds will be placed into power save mode by
**SuspendProgram**. For nodes that are in multiple partitions with this option set, the highest time
will take effect. If not set on any partition, the node will use the **SuspendTime** value set for
the entire cluster. Setting **SuspendTime** to INFINITE will disable suspending of nodes in this
partition. Setting **SuspendTime** to anything but INFINITE (or -1) will enable power save mode.

<!-- -->

**SuspendTimeout**  
Maximum time permitted (in seconds) between when a node suspend request is issued and when the node
is shutdown. At that time the node must be ready for a resume request to be issued as needed for new
work. For nodes that are in multiple partitions with this option set, the highest time will take
effect. If not set on any partition, the node will use the **SuspendTimeout** value set for the
entire cluster.

<!-- -->

**TRESBillingWeights**  
TRESBillingWeights is used to define the billing weights of each tracked TRES type (see
**AccountingStorageTRES**) that will be used in calculating the usage of a job. The calculated usage
is used when calculating fairshare and when enforcing the TRES billing limit on jobs.

Billing weights are specified as a comma-separated list of *\<TRES Type\>*=*\<TRES Billing Weight\>*
pairs.

Any TRES Type is available for billing. Note that the base unit for memory and burst buffers is
megabytes.

By default the billing of TRES is calculated as the sum of all TRES types multiplied by their
corresponding billing weight.

The weighted amount of a resource can be adjusted by adding a suffix of K,M,G,T or P after the
billing weight. For example, a memory weight of "mem=.25" on a job allocated 8GB will be billed 2048
(8192MB \*.25) units. A memory weight of "mem=.25G" on the same job will be billed 2 (8192MB \*
(.25/1024)) units.

Negative values are allowed.

When a job is allocated 1 CPU and 8 GB of memory on a partition configured with
TRESBillingWeights="CPU=1.0,Mem=0.25G,GRES/gpu=2.0", the billable TRES will be: (1\*1.0) +
(8\*0.25) + (0\*2.0) = 3.0.

If PriorityFlags=MAX_TRES is configured, the billable TRES is calculated as the MAX of individual
TRESs on a node (e.g. cpus, mem, gres) plus the sum of all global TRESs (e.g. licenses). Using the
same example above the billable TRES will be MAX(1\*1.0, 8\*0.25) + (0\*2.0) = 2.0.

If TRESBillingWeights is not defined then the job is billed against the total number of allocated
CPUs.

**NOTE**: TRESBillingWeights doesn't affect job priority directly as it is currently not used for
the size of the job. If you want TRESs to play a role in the job's priority then refer to the
PriorityWeightTRES option.

# PROLOG AND EPILOG SCRIPTS

There are a variety of prolog and epilog program options that execute with various permissions and
at various times. The four options most likely to be used are: **Prolog** and **Epilog** (executed
once on each compute node for each job) plus **PrologSlurmctld** and **EpilogSlurmctld** (executed
once on the **ControlMachine** for each job).

**NOTE**: Standard output and error messages are normally not preserved. Explicitly write output and
error messages to an appropriate location if you wish to preserve that information.

**NOTE**: By default the Prolog script is ONLY run on any individual node when it first sees a job
step from a new allocation. It does not run the Prolog immediately when an allocation is granted. If
no job steps from an allocation are run on a node, it will never run the Prolog for that allocation.
This Prolog behavior can be changed by the **PrologFlags** parameter. The Epilog, on the other hand,
always runs on every node of an allocation when the allocation is released.

If the Epilog fails (returns a non-zero exit code), this will result in the node being set to a
DRAIN state. If the EpilogSlurmctld fails (returns a non-zero exit code), this will only be logged.
If the Prolog fails (returns a non-zero exit code), this will result in the node being set to a
DRAIN state and the job being requeued. The job will be placed in a held state unless
**nohold_on_prolog_fail** is configured in **SchedulerParameters**. If the PrologSlurmctld fails
(returns a non-zero exit code), this will result in the job being requeued to be executed on another
node if possible. Only batch jobs can be requeued. Interactive jobs (salloc and srun) will be
cancelled if the PrologSlurmctld fails. If slurmctld is stopped while either PrologSlurmctld or
EpilogSlurmctld is running, the script will be killed with SIGKILL. The script will restart when
slurmctld restarts.

Information about the job is passed to the script using environment variables. Unless otherwise
specified, these environment variables are available in each of the scripts mentioned above
(**Prolog**, **Epilog**, **PrologSlurmctld** and **EpilogSlurmctld**). For a full list of
environment variables that includes those available in the **SrunProlog**, **SrunEpilog**,
**TaskProlog** and **TaskEpilog** please see the Prolog and Epilog Guide
\<https://slurm.schedmd.com/prolog_epilog.html\>.

**SLURM_ARRAY_JOB_ID**  
If this job is part of a job array, this will be set to the job ID. Otherwise it will not be set. To
reference this specific task of a job array, combine SLURM_ARRAY_JOB_ID with SLURM_ARRAY_TASK_ID
(e.g. "scontrol update \${SLURM_ARRAY_JOB_ID}\_{\$SLURM_ARRAY_TASK_ID} ..."); Available in
**PrologSlurmctld** and **EpilogSlurmctld**.

<!-- -->

**SLURM_ARRAY_TASK_ID**  
If this job is part of a job array, this will be set to the task ID. Otherwise it will not be set.
To reference this specific task of a job array, combine SLURM_ARRAY_JOB_ID with SLURM_ARRAY_TASK_ID
(e.g. "scontrol update \${SLURM_ARRAY_JOB_ID}\_{\$SLURM_ARRAY_TASK_ID} ..."); Available in
**PrologSlurmctld** and **EpilogSlurmctld**.

<!-- -->

**SLURM_ARRAY_TASK_MAX**  
If this job is part of a job array, this will be set to the maximum task ID. Otherwise it will not
be set. Available in **PrologSlurmctld** and **EpilogSlurmctld**.

<!-- -->

**SLURM_ARRAY_TASK_MIN**  
If this job is part of a job array, this will be set to the minimum task ID. Otherwise it will not
be set. Available in **PrologSlurmctld** and **EpilogSlurmctld**.

<!-- -->

**SLURM_ARRAY_TASK_STEP**  
If this job is part of a job array, this will be set to the step size of task IDs. Otherwise it will
not be set. Available in **PrologSlurmctld** and **EpilogSlurmctld**.

<!-- -->

**SLURM_CLUSTER_NAME**  
Name of the cluster executing the job.

<!-- -->

**SLURM_CONF**  
Location of the slurm.conf file. Available in **Prolog** and **Epilog**.

<!-- -->

**SLURMD_NODENAME**  
Name of the node running the task. In the case of a parallel job executing on multiple compute
nodes, the various tasks will have this environment variable set to different values on each compute
node. Available in **Prolog** and **Epilog**.

<!-- -->

**SLURM_JOB_ACCOUNT**  
Account name used for the job.

<!-- -->

**SLURM_JOB_COMMENT**  
Comment added to the job. Available in **Prolog**, **PrologSlurmctld**, **Epilog** and
**EpilogSlurmctld**.

<!-- -->

**SLURM_JOB_CONSTRAINTS**  
Features required to run the job. Available in **Prolog**, **PrologSlurmctld**, **Epilog** and
**EpilogSlurmctld**.

<!-- -->

**SLURM_JOB_DERIVED_EC**  
The highest exit code of all of the job steps. Available in **Epilog** and **EpilogSlurmctld**.

<!-- -->

**SLURM_JOB_END_TIME**  
The UNIX timestamp for a job's end time.

<!-- -->

**SLURM_JOB_EXIT_CODE**  
The exit code of the job script (or salloc). The value is the status as returned by the wait()
system call (See wait(2)) Available in **Epilog** and **EpilogSlurmctld**.

<!-- -->

**SLURM_JOB_EXIT_CODE2**  
The exit code of the job script (or salloc). The value has the format \<exit\>:\<sig\>. The first
number is the exit code, typically as set by the exit() function. The second number of the signal
that caused the process to terminate if it was terminated by a signal. Available in **Epilog** and
**EpilogSlurmctld**.

<!-- -->

**SLURM_JOB_EXTRA**  
Extra field added to the job. Available in **Prolog**, **PrologSlurmctld**, **Epilog** and
**EpilogSlurmctld**.

<!-- -->

**SLURM_JOB_GID**  
Group ID of the job's owner.

<!-- -->

**SLURM_JOB_GPUS**  
The GPU IDs of GPUs in the job allocation (if any). Available in the **Prolog** and **Epilog**.

<!-- -->

**SLURM_JOB_GROUP**  
Group name of the job's owner. Available in **PrologSlurmctld** and **EpilogSlurmctld**.

<!-- -->

**SLURM_JOB_ID**  
Job ID.

<!-- -->

**SLURM_JOBID**  
Job ID.

<!-- -->

**SLURM_JOB_NAME**  
Name of the job. Available in **PrologSlurmctld** and **EpilogSlurmctld**.

<!-- -->

**SLURM_JOB_NODELIST**  
Nodes assigned to job. A Slurm hostlist expression. "scontrol show hostnames" can be used to convert
this to a list of individual host names. Available in **PrologSlurmctld** and **EpilogSlurmctld**.

<!-- -->

**SLURM_JOB_PARTITION**  
Partition that job runs in. Available in **Prolog**, **PrologSlurmctld**, **Epilog** and
**EpilogSlurmctld**.

<!-- -->

**SLURM_JOB_START_TIME**  
The UNIX timestamp of a job's start time.

<!-- -->

**SLURM_JOB_UID**  
User ID of the job's owner.

<!-- -->

**SLURM_JOB_USER**  
User name of the job's owner.

<!-- -->

**SLURM_SCRIPT_CONTEXT**  
Identifies which epilog or prolog program is currently running.

# UNKILLABLE STEP PROGRAM SCRIPT

This program can be used to take special actions to clean up the unkillable processes and/or notify
system administrators. The program will be run as **SlurmdUser** (usually "root") on the compute
node where **UnkillableStepTimeout** was triggered.

Information about the unkillable job step is passed to the script using environment variables.

**SLURM_JOB_ID**  
Job ID.

<!-- -->

**SLURM_STEP_ID**  
Job Step ID.

# NETWORK TOPOLOGY

Slurm is able to optimize job allocations to minimize network contention. Special Slurm logic is
used to optimize allocations on systems with a three-dimensional interconnect. and information about
configuring those systems are available on web pages available here: \<https://slurm.schedmd.com/\>.
For a hierarchical network, Slurm needs to have detailed information about how nodes are configured
on the network switches.

Given network topology information, Slurm allocates all of a job's resources onto a single leaf of
the network (if possible) using a best-fit algorithm. Otherwise it will allocate a job's resources
onto multiple leaf switches so as to minimize the use of higher-level switches. The
**TopologyPlugin** parameter controls which plugin is used to collect network topology information.
The only values presently supported are "topology/3d_torus" (default for Cray XT/XE systems,
performs best-fit logic over three-dimensional topology), "topology/none" (default for other
systems, best-fit logic over one-dimensional topology), "topology/tree" (determine the network
topology based upon information contained in a topology.conf file, see "man topology.conf" for more
information). Future plugins may gather topology information directly from the network. The topology
information is optional. If not provided, Slurm will perform a best-fit algorithm assuming the nodes
are in a one-dimensional array as configured and the communications cost is related to the node
distance in this array.

# RELOCATING CONTROLLERS

If the cluster's computers used for the primary or backup controller will be out of service for an
extended period of time, it may be desirable to relocate them. In order to do so, follow this
procedure:

1\. Stop the Slurm daemons on the old controller and nodes.  
2. Modify the slurm.conf file appropriately.  
3. Copy the files from the StateSaveLocation to the new controller or ensure that they are
accessible to the new controller via a shared drive.  
4. Distribute the updated slurm.conf file to all nodes.  
5. Restart the Slurm daemons on the new controller and nodes.

There should be no loss of any pending jobs but the cluster should be drained of running jobs before
changing hosts for the controller. Ensure that any nodes added to the cluster have the current
slurm.conf file installed.

**CAUTION:** If two nodes are simultaneously configured as the primary controller (two nodes on
which **SlurmctldHost** specify the local host and the **slurmctld** daemon is executing on each),
system behavior will be destructive. If a compute node has an incorrect **SlurmctldHost** parameter,
that node may be rendered unusable, but no other harm will result.

# EXAMPLE

    #
    # Sample /etc/slurm.conf for dev[0-25].llnl.gov
    # Author: John Doe
    # Date: 11/06/2001
    #
    SlurmctldHost=dev0(12.34.56.78)  # Primary server
    SlurmctldHost=dev1(12.34.56.79)  # Backup server
    #
    AuthType=auth/munge
    Epilog=/usr/local/slurm/epilog
    Prolog=/usr/local/slurm/prolog
    FirstJobId=65536
    InactiveLimit=120
    JobCompType=jobcomp/filetxt
    JobCompLoc=/var/log/slurm/jobcomp
    KillWait=30
    MaxJobCount=10000
    MinJobAge=300
    PluginDir=/usr/local/lib:/usr/local/slurm/lib
    ReturnToService=0
    SchedulerType=sched/backfill
    SlurmctldLogFile=/var/log/slurm/slurmctld.log
    SlurmdLogFile=/var/log/slurm/slurmd.log
    SlurmctldPort=7002
    SlurmdPort=7003
    SlurmdSpoolDir=/var/spool/slurmd.spool
    StateSaveLocation=/var/spool/slurm.state
    SwitchType=switch/none
    TmpFS=/tmp
    WaitTime=30
    #
    # Node Configurations
    #
    NodeName=DEFAULT CPUs=2 RealMemory=2000 TmpDisk=64000
    NodeName=DEFAULT State=UNKNOWN
    NodeName=dev[0-25] NodeAddr=edev[0-25] Weight=16
    # Update records for specific DOWN nodes
    DownNodes=dev20 State=DOWN Reason="power,ETA=Dec25"
    #
    # Partition Configurations
    #
    PartitionName=DEFAULT MaxTime=30 MaxNodes=10 State=UP
    PartitionName=debug Nodes=dev[0-8,18-25] Default=YES
    PartitionName=batch Nodes=dev[9-17]  MinNodes=4
    PartitionName=long Nodes=dev[9-17] MaxTime=120 AllowGroups=admin

# INCLUDE MODIFIERS

The "include" key word can be used with modifiers within the specified pathname. These modifiers
would be replaced with cluster name or other information depending on which modifier is specified.
If the included file is not an absolute path name (i.e. it does not start with a slash), it will
searched for in the same directory as the slurm.conf file.

**%c**  
Cluster name specified in the slurm.conf will be used.

**EXAMPLE**

    ClusterName=linux
    include /home/slurm/etc/%c_config
    # Above line interpreted as
    # "include /home/slurm/etc/linux_config"

# FILE AND DIRECTORY PERMISSIONS

There are three classes of files: Files used by **slurmctld** must be accessible by user
**SlurmUser** and accessible by the primary and backup control machines. Files used by **slurmd**
must be accessible by user root and accessible from every compute node. A few files need to be
accessible by normal users on all login and compute nodes. While many files and directories are
listed below, most of them will not be used with most configurations.

**Epilog**  
Must be executable by user root. It is recommended that the file be readable by all users. The file
must exist on every compute node.

<!-- -->

**EpilogSlurmctld**  
Must be executable by user **SlurmUser**. It is recommended that the file be readable by all users.
The file must be accessible by the primary and backup control machines.

<!-- -->

**HealthCheckProgram**  
Must be executable by user root. It is recommended that the file be readable by all users. The file
must exist on every compute node.

<!-- -->

**JobCompLoc**  
If this specifies a file, it must be writable by user **SlurmUser**. The file must be accessible by
the primary and backup control machines.

<!-- -->

**MailProg**  
Must be executable by user **SlurmUser**. Must not be writable by regular users. The file must be
accessible by the primary and backup control machines.

<!-- -->

**Prolog**  
Must be executable by user root. It is recommended that the file be readable by all users. The file
must exist on every compute node.

<!-- -->

**PrologSlurmctld**  
Must be executable by user **SlurmUser**. It is recommended that the file be readable by all users.
The file must be accessible by the primary and backup control machines.

<!-- -->

**ResumeProgram**  
Must be executable by user **SlurmUser**. The file must be accessible by the primary and backup
control machines.

<!-- -->

**slurm.conf**  
Readable to all users on all nodes. Must not be writable by regular users.

<!-- -->

**SlurmctldLogFile**  
Must be writable by user **SlurmUser**. The file must be accessible by the primary and backup
control machines.

<!-- -->

**SlurmctldPidFile**  
Must be writable by user root. Preferably writable and removable by **SlurmUser**. The file must be
accessible by the primary and backup control machines.

<!-- -->

**SlurmdLogFile**  
Must be writable by user root. A distinct file must exist on each compute node.

<!-- -->

**SlurmdPidFile**  
Must be writable by user root. A distinct file must exist on each compute node.

<!-- -->

**SlurmdSpoolDir**  
Must be writable by user root. Permissions must be set to 755 so that job scripts can be executed
from this directory. A distinct file must exist on each compute node.

<!-- -->

**SrunEpilog**  
Must be executable by all users. The file must exist on every login and compute node.

<!-- -->

**SrunProlog**  
Must be executable by all users. The file must exist on every login and compute node.

<!-- -->

**StateSaveLocation**  
Must be writable by user **SlurmUser**. The file must be accessible by the primary and backup
control machines.

<!-- -->

**SuspendProgram**  
Must be executable by user **SlurmUser**. The file must be accessible by the primary and backup
control machines.

<!-- -->

**TaskEpilog**  
Must be executable by all users. The file must exist on every compute node.

<!-- -->

**TaskProlog**  
Must be executable by all users. The file must exist on every compute node.

<!-- -->

**UnkillableStepProgram**  
Must be executable by user **SlurmdUser**. The file must be accessible by the primary and backup
control machines.

# LOGGING

Note that while Slurm daemons create log files and other files as needed, it treats the lack of
parent directories as a fatal error. This prevents the daemons from running if critical file systems
are not mounted and will minimize the risk of cold-starting (starting without preserving jobs).

Log files and job accounting files may need to be created/owned by the "SlurmUser" uid to be
successfully accessed. Use the "chown" and "chmod" commands to set the ownership and permissions
appropriately. See the section **FILE AND DIRECTORY PERMISSIONS** for information about the various
files and directories used by Slurm.

It is recommended that the logrotate utility be used to ensure that various log files do not become
too large. This also applies to text files used for accounting, process tracking, and the slurmdbd
log if they are used.

Here is a sample logrotate configuration. Make appropriate site modifications and save as
/etc/logrotate.d/slurm on all nodes. See the **logrotate** man page for more details.

    ##
    # Slurm Logrotate Configuration
    ##
    /var/log/slurm/*.log {
    	compress
    	missingok
    	nocopytruncate
    	nodelaycompress
    	nomail
    	notifempty
    	noolddir
    	rotate 5
    	sharedscripts
    	size=5M
    	create 640 slurm root
    	postrotate
    		pkill -x --signal SIGUSR2 slurmctld
    		pkill -x --signal SIGUSR2 slurmd
    		pkill -x --signal SIGUSR2 slurmdbd
    		exit 0
    	endscript
    }

# COPYING

Copyright (C) 2002-2007 The Regents of the University of California. Produced at Lawrence Livermore
National Laboratory (cf, DISCLAIMER).  
Copyright (C) 2008-2010 Lawrence Livermore National Security.  
Copyright (C) 2010-2022 SchedMD LLC.

This file is part of Slurm, a resource management program. For details, see
\<https://slurm.schedmd.com/\>.

Slurm is free software; you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

Slurm is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
License for more details.

# FILES

/etc/slurm.conf

# SEE ALSO

**cgroup.conf**(5), **getaddrinfo**(3), **getrlimit**(2), **gres.conf**(5), **group**(5),
**hostname**(1), **scontrol**(1), **slurmctld**(8), **slurmd**(8), **slurmdbd**(8),
**slurmdbd.conf**(5), **srun**(1), **spank**(8), **syslog**(3), **topology.conf**(5)
