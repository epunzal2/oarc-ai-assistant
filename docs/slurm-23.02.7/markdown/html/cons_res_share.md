# <span id="top">Sharing Consumable Resources</span>

## CPU Management

(Disclaimer: In this "CPU Management" section, the term "consumable resource" does not include
memory. The management of memory as a consumable resource is discussed in its own section below.)

The per-partition `OverSubscribe` setting applies to the <u>entity being selected for
scheduling</u>:

- When the default `select/linear` plugin is enabled, the per-partition `OverSubscribe` setting
  controls whether or not the **nodes** are shared among jobs.

- When the `select/cons_res` or `select/cons_tres` plugins are enabled, the per-partition
  `OverSubscribe` setting controls whether or not the **configured consumable resources** are shared
  among jobs. When a consumable resource such as a core, socket, or CPU is shared, it means that
  more than one job can be assigned to it.

The following table describes this new functionality in more detail:

<table data-border="1" data-cellpadding="3" data-cellspacing="1">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<thead>
<tr>
<th>Selection Setting</th>
<th>Per-partition <code>OverSubscribe</code> Setting</th>
<th>Resulting Behavior</th>
</tr>
</thead>
<tbody>
<tr>
<td rowspan="3">SelectType=<strong>select/linear</strong></td>
<td>OverSubscribe=NO</td>
<td>Whole nodes are allocated to jobs. No node will run more than one job per partition/queue.</td>
</tr>
<tr>
<td>OverSubscribe=YES</td>
<td>By default same as OverSubscribe=NO. Nodes allocated to a job may be shared with other jobs if
each job allows sharing via the <code>srun --oversubscribe</code> option.</td>
</tr>
<tr>
<td>OverSubscribe=FORCE</td>
<td>Each whole node can be allocated to multiple jobs up to the count specified per partition/queue
(default 4 jobs per node)</td>
</tr>
<tr>
<td rowspan="3">SelectType=<strong>select/cons_res</strong> or
<strong>select/cons_tres</strong><br />
Plus one of the following:<br />
SelectTypeParameters=<strong>CR_Core</strong><br />
SelectTypeParameters=<strong>CR_Core_Memory</strong></td>
<td>OverSubscribe=NO</td>
<td>Cores are allocated to jobs. No core will run more than one job per partition/queue.</td>
</tr>
<tr>
<td>OverSubscribe=YES</td>
<td>By default same as OverSubscribe=NO. Cores allocated to a job may be shared with other jobs if
each job allows sharing via the <code>srun --oversubscribe</code> option.</td>
</tr>
<tr>
<td>OverSubscribe=FORCE</td>
<td>Each core can be allocated to multiple jobs up to the count specified per partition/queue
(default 4 jobs per core).</td>
</tr>
<tr>
<td rowspan="3">SelectType=<strong>select/cons_res</strong> or
<strong>select/cons_tres</strong><br />
Plus one of the following:<br />
SelectTypeParameters=<strong>CR_CPU</strong><br />
SelectTypeParameters=<strong>CR_CPU_Memory</strong></td>
<td>OverSubscribe=NO</td>
<td>CPUs are allocated to jobs. No CPU will run more than one job per partition/queue.</td>
</tr>
<tr>
<td>OverSubscribe=YES</td>
<td>By default same as OverSubscribe=NO. CPUs allocated to a job may be shared with other jobs if
each job allows sharing via the <code>srun --oversubscribe</code> option.</td>
</tr>
<tr>
<td>OverSubscribe=FORCE</td>
<td>Each CPU can be allocated to multiple jobs up to the count specified per partition/queue
(default 4 jobs per CPU).</td>
</tr>
<tr>
<td rowspan="3">SelectType=<strong>select/cons_res</strong> or
<strong>select/cons_tres</strong><br />
Plus one of the following:<br />
SelectTypeParameters=<strong>CR_Socket</strong><br />
SelectTypeParameters=<strong>CR_Socket_Memory</strong></td>
<td>OverSubscribe=NO</td>
<td>Sockets are allocated to jobs. No Socket will run more than one job per partition/queue.</td>
</tr>
<tr>
<td>OverSubscribe=YES</td>
<td>By default same as OverSubscribe=NO. Sockets allocated to a job may be shared with other jobs if
each job allows sharing via the <code>srun --oversubscribe</code> option.</td>
</tr>
<tr>
<td>OverSubscribe=FORCE</td>
<td>Each socket can be allocated to multiple jobs up to the count specified per partition/queue
(default 4 jobs per socket).</td>
</tr>
</tbody>
</table>

When `OverSubscribe=FORCE` is configured, the consumable resources are scheduled for jobs using a
**least-loaded** algorithm. Thus, idle CPUs\|cores\|sockets will be allocated to a job before busy
ones, and CPUs\|cores\|sockets running one job will be allocated to a job before ones running two or
more jobs. This is the same approach that the `select/linear` plugin uses when allocating "shared"
nodes.

Note that the **granularity** of the "least-loaded" algorithm is what distinguishes the consumable
resource and linear plugins when `OverSubscribe=FORCE` is configured. With the `select/cons_res` or
`select/cons_tres` plugin enabled, the CPUs of a node are not overcommitted until **all** of the
rest of the CPUs are overcommitted on the other nodes. Thus if one job allocates half of the CPUs on
a node and then a second job is submitted that requires more than half of the CPUs, the consumable
resource plugin will attempt to place this new job on other busy nodes that have more than half of
the CPUs available for use. The `select/linear` plugin simply counts jobs on nodes, and does not
track the CPU usage on each node.

The sharing functionality in the `select/cons_res` and `select/cons_tres` plugins also support the
new `OverSubscribe=FORCE:<num>` syntax. If `OverSubscribe=FORCE:3` is configured with a consumable
resource plugin and `CR_Core` or `CR_Core_Memory`, then the plugin will run up to 3 jobs on each
<u>core</u> of each node in the partition. If `CR_Socket` or `CR_Socket_Memory` is configured, then
the plugin will run up to 3 jobs on each <u>socket</u> of each node in the partition.

## Nodes in Multiple Partitions

Slurm has supported configuring nodes in more than one partition since version 0.7.0. The following
table describes how nodes configured in two partitions with different `OverSubscribe` settings will
be allocated to jobs. Note that "shared" jobs are jobs that are submitted to partitions configured
with `OverSubscribe=FORCE` or with `OverSubscribe=YES` and the job requested sharing with the
`srun --oversubscribe` option. Conversely, "non-shared" jobs are jobs that are submitted to
partitions configured with `OverSubscribe=NO` or `OverSubscribe=YES` and the job did <u>not</u>
request shareable resources.

|   | First job "shareable" | First job not "shareable" |
|----|----|----|
| Second job "shareable" | Both jobs can run on the same nodes and may share resources | Jobs do not run on the same nodes |
| Second job not "shareable" | Jobs do not run on the same nodes | Jobs can run on the same nodes but will not share resources |

The next table contains several scenarios with the `select/cons_res` or `select/cons_tres` plugins
enabled to further clarify how a node is used when it is configured in more than one partition and
the partitions have different "OverSubscribe" policies.

| Slurm configuration | Resulting Behavior |
|----|----|
| Two `OverSubscribe=NO` partitions assigned the same set of nodes | Jobs from either partition will be assigned to all available consumable resources. No consumable resource will be shared. One node could have 2 jobs running on it, and each job could be from a different partition. |
| Two partitions assigned the same set of nodes: one partition is `OverSubscribe=FORCE`, and the other is `OverSubscribe=NO` | A node will only run jobs from one partition at a time. If a node is running jobs from the `OverSubscribe=NO` partition, then none of its consumable resources will be shared. If a node is running jobs from the `OverSubscribe=FORCE` partition, then its consumable resources can be shared. |
| Two `OverSubscribe=FORCE` partitions assigned the same set of nodes | Jobs from either partition will be assigned consumable resources. All consumable resources can be shared. One node could have 2 jobs running on it, and each job could be from a different partition. |
| Two partitions assigned the same set of nodes: one partition is `OverSubscribe=FORCE:3`, and the other is `OverSubscribe=FORCE:5` | Generally the same behavior as above. However no consumable resource will ever run more than 3 jobs from the first partition, and no consumable resource will ever run more than 5 jobs from the second partition. A consumable resource could have up to 8 jobs running on it at one time. |

Note that the "mixed shared setting" configuration (row \#2 above) introduces the possibility of
**starvation** between jobs in each partition. If a set of nodes are running jobs from the
`OverSubscribe=NO` partition, then these nodes will continue to only be available to jobs from that
partition, even if jobs submitted to the `OverSubscribe=FORCE` partition have a higher priority.
This works in reverse also, and in fact it's easier for jobs from the `OverSubscribe=FORCE`
partition to hold onto the nodes longer because the consumable resource "sharing" provides more
resource availability for new jobs to begin running "on top of" the existing jobs. This happens with
the `select/linear` plugin also, so it's not specific to the `select/cons_res` or `select/cons_tres`
plugins.

## Memory Management

The management of memory as a consumable resource remains unchanged and can be used to prevent
oversubscription of memory, which would result in having memory pages swapped out and severely
degraded performance.

<table data-border="1" data-cellpadding="3" data-cellspacing="1">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr>
<th>Selection Setting</th>
<th>Resulting Behavior</th>
</tr>
</thead>
<tbody>
<tr>
<td>SelectType=<strong>select/linear</strong></td>
<td>Memory allocation is not tracked. Jobs are allocated to nodes without considering if there is
enough free memory. Swapping could occur!</td>
</tr>
<tr>
<td>SelectType=<strong>select/linear</strong> plus<br />
SelectTypeParameters=<strong>CR_Memory</strong></td>
<td>Memory allocation is tracked. Nodes that do not have enough available memory to meet the jobs
memory requirement will not be allocated to the job.</td>
</tr>
<tr>
<td>SelectType=<strong>select/cons_res</strong> or <strong>select/cons_tres</strong><br />
Plus one of the following:<br />
SelectTypeParameters=<strong>CR_Core</strong><br />
SelectTypeParameters=<strong>CR_CPU</strong><br />
SelectTypeParameters=<strong>CR_Socket</strong></td>
<td>Memory allocation is not tracked. Jobs are allocated to consumable resources without considering
if there is enough free memory. Swapping could occur!</td>
</tr>
<tr>
<td>SelectType=<strong>select/cons_res</strong> or <strong>select/cons_tres</strong><br />
Plus one of the following:<br />
SelectTypeParameters=<strong>CR_Memory</strong><br />
SelectTypeParameters=<strong>CR_Core_Memory</strong><br />
SelectTypeParameters=<strong>CR_CPU_Memory</strong><br />
SelectTypeParameters=<strong>CR_Socket_Memory</strong></td>
<td>Memory allocation for all jobs are tracked. Nodes that do not have enough available memory to
meet the jobs memory requirement will not be allocated to the job.</td>
</tr>
</tbody>
</table>

Users can specify their job's memory requirements one of two ways. The `srun --mem=<num>` option can
be used to specify the jobs memory requirement on a per allocated node basis. This option is
recommended for use with the `select/linear` plugin, which allocates whole nodes to jobs. The
`srun --mem-per-cpu=<num>` option can be used to specify the jobs memory requirement on a per
allocated CPU basis. This is recommended for use with the `select/cons_res` or `select/cons_tres`
plugins, which can allocate individual CPUs to jobs.

Default and maximum values for memory on a per node or per CPU basis can be configured by the system
administrator using the following `slurm.conf` options: `DefMemPerCPU`, `DefMemPerNode`,
`MaxMemPerCPU` and `MaxMemPerNode`. Users can use the `--mem` or `--mem-per-cpu` option at job
submission time to override the default value, but they cannot exceed the maximum value.

Enforcement of a jobs memory allocation is performed by setting the "maximum data segment size" and
the "maximum virtual memory size" system limits to the appropriate values before launching the
tasks. Enforcement is also managed by the accounting plugin, which periodically gathers data about
running jobs. Set `JobAcctGather` and `JobAcctFrequency` to values suitable for your system.

**NOTE**: The `--oversubscribe` and `--exclusive` options are mutually exclusive when used at job
submission. If both options are set when submitting a job, the job submission command used will
fatal.

Last modified 19 September 2022
