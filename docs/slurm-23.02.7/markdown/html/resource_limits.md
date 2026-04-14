# Resource Limits

Familiarity with Slurm's [Accounting](accounting.md) web page is strongly recommended before use of
this document.

## Hierarchy

Slurm's hierarchical limits are enforced in the following order with Job QOS and Partition QOS order
being reversible by using the QOS flag 'OverPartQOS':

1.  Partition QOS limit
2.  Job QOS limit
3.  User association
4.  Account association(s), ascending the hierarchy
5.  Root/Cluster association
6.  Partition limit
7.  None

Note: If limits are defined at multiple points in this hierarchy, the point in this list where the
limit is first defined will be used. Consider the following example:

- MaxJobs=20 and MaxSubmitJobs is undefined in the partition QOS
- No limits are set in the job QOS and
- MaxJobs=4 and MaxSubmitJobs=50 in the user association

The limits in effect will be MaxJobs=20 and MaxSubmitJobs=50.

Note: The precedence order specified above is respected except for the following limits:
Max\[Time\|Wall\], \[Min\|Max\]Nodes. For these limits, even if the job is enforced with QOS and/or
Association limits, it can't go over the limit imposed at Partition level, even if it listed at the
bottom. So the default for these 3 types of limits is that they are upper bound by the Partition
one. This Partition level bound can be ignored if the respective QOS PartitionTimeLimit and/or
Partition\[Max\|Min\]Nodes flags are set, then the job would be enforced the limits imposed at QOS
and/or association level respecting the order above.

## Configuration

Scheduling policy information must be stored in a database as specified by the
**AccountingStorageType** configuration parameter in the **slurm.conf** configuration file.
Information can be recorded in a [MySQL](http://www.mysql.com/) or [MariaDB](https://mariadb.org/)
database. For security and performance reasons, the use of SlurmDBD (Slurm Database Daemon) as a
front-end to the database is strongly recommended. SlurmDBD uses a Slurm authentication plugin (e.g.
MUNGE). SlurmDBD also uses an existing Slurm accounting storage plugin to maximize code reuse.
SlurmDBD uses data caching and prioritization of pending requests in order to optimize performance.
While SlurmDBD relies upon existing Slurm plugins for authentication and database use, the other
Slurm commands and daemons are not required on the host where SlurmDBD is installed. Only the
*slurmdbd* and *slurm-plugins* RPMs are required for SlurmDBD execution.

Both accounting and scheduling policies are configured based upon an *association*. An *association*
is a 4-tuple consisting of the cluster name, bank account, user and (optionally) the Slurm
partition. In order to enforce scheduling policy, set the value of **AccountingStorageEnforce**.
This option contains a comma separated list of options you may want to enforce. The valid options
are:

- associations - This will prevent users from running jobs if their *association* is not in the
  database. This option will prevent users from accessing invalid accounts.
- limits - This will enforce limits set to associations. By setting this option, the 'associations'
  option is also set.
- qos - This will require all jobs to specify (either overtly or by default) a valid qos (Quality of
  Service). QOS values are defined for each association in the database. By setting this option, the
  'associations' option is also set.
- safe - This will ensure a job will only be launched when using an association or qos that has a
  TRES-minutes limit set if the job will be able to run to completion. Without this option set, jobs
  will be launched as long as their usage hasn't reached the TRES-minutes limit which can lead to
  jobs being launched but then killed when the limit is reached. With the 'safe' option set, a job
  won't be killed due to limits, even if the limits are changed after the job was started and the
  association or qos violates the updated limits. By setting this option, both the 'associations'
  option and the 'limits' option are set automatically.
- wckeys - This will prevent users from running jobs under a wckey that they don't have access to.
  By using this option, the 'associations' option is also set. The 'TrackWCKey' option is also set
  to true.

**NOTE**: The association is a combination of cluster, account, user names and optional partition
name.  
Without AccountingStorageEnforce being set (the default behavior) jobs will be executed based upon
policies configured in Slurm on each cluster.

## Tools

The tool used to manage accounting policy is *sacctmgr*. It can be used to create and delete
cluster, user, bank account, and partition records plus their combined *association* record. See
*man sacctmgr* for details on this tools and examples of its use.

Changes made to the scheduling policy are uploaded to the Slurm control daemons on the various
clusters and take effect immediately. When an association is deleted, all running or pending jobs
which belong to that association are immediately canceled. When limits are lowered, running jobs
will not be canceled to satisfy the new limits, but the new lower limits will be enforced.

## Association specific limits and scheduling policies

These represent the limits and scheduling policies relevant to Associations. When dealing with
Associations, most of these limits are available not only for the user association, but also for
each cluster and account. Limits and policies are applied in the following order:  
1. The option specified for the user association.  
2. The option specified for the account.  
3. The option specified for the cluster.  
4. If nothing is configured at the above levels, no limit will be applied.

These are just the limits and policies for Associations. For a more complete description of the
columns available to be displayed, see the
[sacctmgr](sacctmgr.md#SECTION_LIST/SHOW-ASSOCIATION-FORMAT-OPTIONS) man page.

**Fairshare**  
Integer value used for determining priority. Essentially this is the amount of claim this
association and its children have to the above system. Can also be the string "parent", when used on
a user this means that the parent association is used for fairshare. If Fairshare=parent is set on
an account, that account's children will be effectively re-parented for fairshare calculations to
the first parent of their parent that is not Fairshare=parent. Limits remain the same, only its
fairshare value is affected.

**GrpJobs**  
The total number of jobs able to run at any given time from an association and its children. If this
limit is reached, new jobs will be queued but only allowed to run after previous jobs complete from
this group.

**GrpJobsAccrue**  
The total number of pending jobs able to accrue age priority at any given time from an association
and its children. If this limit is reached, new jobs will be queued but not accrue age priority
until after previous jobs are removed from pending in this group. This limit does not determine if
the job can run or not, it only limits the age factor of the priority.

**GrpSubmitJobs**  
The total number of jobs able to be submitted to the system at any given time from an association
and its children. If this limit is reached, new submission requests will be denied until previous
jobs complete from this group.

**GrpTRES**  
The total count of TRES able to be used at any given time from jobs running from an association and
its children. If this limit is reached, new jobs will be queued but only allowed to run after
resources have been relinquished from this group.

**GrpTRESMins**  
The total number of TRES minutes that can possibly be used by past, present and future jobs running
from an association and its children. If any limit is reached, all running jobs with that TRES in
this group will be killed, and no new jobs will be allowed to run. This usage is decayed (at a rate
of PriorityDecayHalfLife). It can also be reset (according to PriorityUsageResetPeriod) in order to
allow jobs to run against the association tree. This limit only applies when using the Priority
Multifactor plugin.

**GrpTRESRunMins**  
Used to limit the combined total number of TRES minutes used by all jobs running with an association
and its children. This takes into consideration time limit of running jobs and consumes it. If the
limit is reached, no new jobs are started until other jobs finish to allow time to free up.

**GrpWall**  
The maximum wall clock time running jobs are able to be allocated in aggregate for an association
and its children. If this limit is reached, future jobs in this association will be queued until
they are able to run inside the limit. This usage is decayed (at a rate of PriorityDecayHalfLife).
It can also be reset (according to PriorityUsageResetPeriod) in order to allow jobs to run against
the association tree again.

**MaxJobs**  
The total number of jobs able to run at any given time for the given association. If this limit is
reached, new jobs will be queued but only allowed to run after existing jobs in the association
complete.

**MaxJobsAccrue**  
The maximum number of pending jobs able to accrue age priority at any given time for the given
association. If this limit is reached, new jobs will be queued but will not accrue age priority
until after existing jobs in the association are moved from a pending state. This limit does not
determine if the job can run, it only limits the age factor of the priority.

**MaxSubmitJobs**  
The maximum number of jobs able to be submitted to the system at any given time from the given
association. If this limit is reached, new submission requests will be denied until existing jobs in
this association complete.

**MaxTRESMinsPerJob**  
A limit of TRES minutes to be used by a job. If this limit is reached, the job will be killed if not
running in Safe mode, otherwise the job will pend until enough time is given to complete the job.

**MaxTRESPerJob**  
The maximum size in TRES any given job can have from the association.

**MaxTRESPerNode**  
The maximum size in TRES each node in a job allocation can use.

**MaxWallDurationPerJob**  
The maximum wall clock time any individual job can run for in the given association. If this limit
is reached, the job will be denied at submission.

**MinPrioThreshold**  
Minimum priority required to reserve resources in the given association. Used to override
bf_min_prio_reserve. See [bf_min_prio_reserve](slurm.conf.md#OPT_bf_min_prio_reserve=#) for details.

**QOS**  
comma separated list of QOSs an association is able to run.

**NOTE**: When modifying a TRES field with *sacctmgr*, one must specify which TRES to modify (see
[TRES](tres.md) for complete list) as in the following examples:

    SET:
    sacctmgr modify user bob set GrpTRES=cpu=1500,mem=200,gres/gpu=50
    UNSET:
    sacctmgr modify user bob set GrpTRES=cpu=-1,mem=-1,gres/gpu=-1

## QOS specific limits and scheduling policies

As noted [above](#hierarchy), the default behavior is that a limit set on a Partition QOS will be
applied before a limit on the job's requested QOS. You can change this behavior with the
*OverPartQOS* flag.

Unless noted, if a job request breaches a given limit on its own, the job will pend unless the job's
QOS has the DenyOnLimit flag set, which will cause the job to be denied at submission. When Grp
limits are considered with respect to this flag the Grp limit is treated as a Max limit.

**GraceTime**  
Preemption grace time to be extended to a job which has been selected for preemption in the format
of \<hh\>:\<mm\>:\<ss\>. The default value is zero, meaning no preemption grace time is allowed on
this QOS. This value is only meaningful for QOS PreemptMode=CANCEL and PreemptMode=REQUEUE.

**GrpJobs**  
The total number of jobs able to run at any given time from a QOS. If this limit is reached, new
jobs will be queued but only allowed to run after previous jobs complete from this group.

**GrpJobsAccrue**  
The total number of pending jobs able to accrue age priority at any given time from a QOS. If this
limit is reached, new jobs will be queued but will not accrue age based priority until after
previous jobs are removed from pending in this group. This limit does not determine if the job can
run or not, it only limits the age factor of the priority. This limit only applies to the job's QOS
and not the partition's QOS.

**GrpSubmitJobs**  
The total number of jobs able to be submitted to the system at any given time from a QOS. If this
limit is reached, new submission requests will be denied until previous jobs complete from this
group.

**GrpTRES**  
The total count of TRES able to be used at any given time from jobs running from a QOS. If this
limit is reached, new jobs will be queued but only allowed to run after resources have been
relinquished from this group.

**GrpTRESMins**  
The total number of TRES minutes that can possibly be used by past, present and future jobs running
from a QOS. If any limit is reached, all running jobs with that TRES in this group will be killed,
and no new jobs will be allowed to run. This usage is decayed (at a rate of PriorityDecayHalfLife).
It can also be reset (according to PriorityUsageResetPeriod) in order to allow jobs to run against
the QOS again. QOS that have the NoDecay flag set do not decay GrpTRESMins, see [QOS
Options](qos.md#qos_other) for details. This limit only applies when using the Priority Multifactor
plugin.

**GrpTRESRunMins**  
Used to limit the combined total number of TRES minutes used by all jobs running with a QOS. This
takes into consideration the time limit of running jobs and consumes it. If the limit is reached, no
new jobs are started until other jobs finish to allow time to free up.

**GrpWall**  
The maximum wall clock time running jobs are able to be allocated in aggregate for a QOS. If this
limit is reached, future jobs in this QOS will be queued until they are able to run inside the
limit. This usage is decayed (at a rate of PriorityDecayHalfLife). It can also be reset (according
to PriorityUsageResetPeriod) in order to allow jobs to run against the QOS again. QOS that have the
NoDecay flag set do not decay GrpWall. See [QOS Options](qos.md#qos_other) for details.

**LimitFactor**  
A float that is factored into an associations \[Grp\|Max\]TRES limits. For example, if the
LimitFactor is 2, then an association with a GrpTRES of 30 CPUs would be allowed to allocate 60 CPUs
when running under this QOS. **NOTE**: This factor is only applied to associations running in this
QOS and is not applied to any limits in the QOS itself.

**MaxJobsAccruePerAccount**  
The maximum number of pending jobs an account (or sub-account) can have accruing age priority at any
given time. This limit does not determine if the job can run, it only limits the age factor of the
priority.

**MaxJobsAccruePerUser**  
The maximum number of pending jobs a user can have accruing age priority at any given time. This
limit does not determine if the job can run, it only limits the age factor of the priority.

**MaxJobsPerAccount**  
The maximum number of jobs an account (or sub-account) can have running at a given time.

**MaxJobsPerUser**  
The maximum number of jobs a user can have running at a given time.

**MaxSubmitJobsPerAccount**  
The maximum number of jobs an account (or sub-account) can have running and pending at a given time.

**MaxSubmitJobsPerUser**  
The maximum number of jobs a user can have running and pending at a given time.

**MaxTRESMinsPerJob**  
Maximum number of TRES minutes each job is able to use.

**MaxTRESPerAccount**  
The maximum number of TRES an account can allocate at a given time.

**MaxTRESPerJob**  
The maximum number of TRES each job is able to use.

**MaxTRESPerNode**  
The maximum number of TRES each node in a job allocation can use.

**MaxTRESPerUser**  
The maximum number of TRES a user can allocate at a given time.

**MaxWallDurationPerJob**  
Maximum wall clock time each job is able to use. Format is \<min\> or \<min\>:\<sec\> or
\<hr\>:\<min\>:\<sec\> or \<days\>-\<hr\>:\<min\>:\<sec\> or \<days\>-\<hr\>. The value is recorded
in minutes with rounding as needed.

**MinPrioThreshold**  
Minimum priority required to reserve resources when scheduling.

**MinTRESPerJob**  
The minimum size in TRES any given job can have when using the requested QOS.

**UsageFactor**  
A float that is factored into a job’s TRES usage (e.g. RawUsage, TRESMins, TRESRunMins). For
example, if the usagefactor was 2, for every TRESBillingUnit second a job ran it would count for 2.
If the usagefactor was .5, every second would only count for half of the time. A setting of 0 would
add no timed usage from the job. The usage factor only applies to the job's QOS and not the
partition QOS.  
If the UsageFactorSafe flag is set and AccountingStorageEnforce includes *Safe*, jobs will only be
able to run if the job can run to completion with the UsageFactor applied, and won't be killed due
to limits.  
If the UsageFactorSafe flag is not set and AccountingStorageEnforce includes *Safe*, a job will be
able to be scheduled without the UsageFactor applied and won't be killed due to limits.  
If the UsageFactorSafe flag is not set and AccountingStorageEnforce does not include *Safe*, a job
will be scheduled as long as the limits are not reached, but could be killed due to limits.  
See [AccountingStorageEnforce](slurm.conf.md#OPT_AccountingStorageEnforce) in the slurm.conf man
page.

The **MaxNodes** and **MaxTime** options already exist in Slurm's configuration on a per-partition
basis, but the above options provide the ability to impose limits on a per-user basis. The
**MaxJobs** option provides an entirely new mechanism for Slurm to control the workload any
individual may place on a cluster in order to achieve some balance between users.

When assigning limits to a QOS to use for a Partition QOS, keep in mind that those limits are
enforced at the QOS level, not individually for each partition. For example, if a QOS has a
**GrpTRES=cpu=20** limit defined and the QOS is assigned to two unique partitions, users will be
limited to 20 CPUs for the QOS rather than being allowed 20 CPUs for each partition.

Fair-share scheduling is based upon the hierarchical bank account data maintained in the Slurm
database. More information can be found in the [priority/multifactor](priority_multifactor.md)
plugin description.

### Specific limits over GRES

When a GRES has a type associated with it and a limit is applied over this specific type (e.g.
*MaxTRESPerUser=gres/gpu:tesla=1*) if a user requests a generic gres, the type's limit will not be
enforced. In this situation an additional lua job submit plugin to check the user request may become
useful. For example, if one requests *--gres=gpu:2* having a limit set of
*MaxTRESPerUser=gres/gpu:tesla=1*, the limit won't be enforced so it will still be possible to get
two teslas.

This is due to a design limitation. The only way to enforce such a limit is to combine the
specification of the limit with a job submit plugin that forces the user to always request a
specific type model.

An example of basic lua job submit plugin function could be:

    function slurm_job_submit(job_desc, part_list, submit_uid)
       if (job_desc.gres ~= nil)
       then
          for g in job_desc.gres:gmatch("[^,]+")
          do
         bad = string.match(g,'^gpu[:]*[0-9]*$')
         if (bad ~= nil)
         then
            slurm.log_info("User specified gpu GRES without type: %s", bad)
            slurm.user_msg("You must always specify a type when requesting gpu GRES")
            return slurm.ERROR
         end
          end
       end
    end

Having this script and the limit in place will force the users to always specify a gpu with its
type, thus enforcing the limits for each specific model.

When **TRESBillingWeights** are defined for a partition, both typed and non-typed resources should
be included. For example, if you have 'tesla' GPUs in one partition and you only define the billing
weights for the 'tesla' typed GPU resource, then those weights will not be applied to the generic
GPUs.

It is also advisable to set **AccountingStorageTRES** for both generic and specific gres types,
otherwise requests that ask for the generic instance of a gres won't be accounted for. For example,
to track generic GPUs and Tesla GPUs, you would set this in your slurm.conf:

      AccountingStorageTRES=gres/gpu,gres/gpu:tesla

See [Trackable Resources TRES](tres.md) for details.

## Job Reason Codes

These reason codes can be used to identify why a job is waiting for execution. A job may be waiting
for more than one reason, in which case only one of those reasons is displayed.

**AccountingPolicy** — Fallback reason when others not matched.

**AccountNotAllowed** — Job is in an account not allowed in a partition.

**AssocGrpBB** — The job's association has reached its aggregate Burst Buffer limit.

**AssocGrpBBMinutes** — The job's association has reached the maximum number of minutes allowed in
aggregate for Burst Buffers by past, present and future jobs.

**AssocGrpBBRunMinutes** — The job's association has reached the maximum number of minutes allowed
in aggregate for Burst Buffers by currently running jobs.

**AssocGrpBilling** — The job's association has reached its aggregate Billing limit.

**AssocGrpBillingMinutes** — The job's association has reached the maximum number of minutes allowed
in aggregate for the Billing value of a resource by past, present and future jobs.

**AssocGrpBillingRunMinutes** — The job's association has reached the maximum number of minutes
allowed in aggregate for the Billing value of a resource by currently running jobs.

**AssocGrpCpuLimit** — The job's association has reached its aggregate CPU limit.

**AssocGrpCPUMinutesLimit** — The job's association has reached the maximum number of minutes
allowed in aggregate for CPUs by past, present and future jobs.

**AssocGrpCPURunMinutesLimit** — The job's association has reached the maximum number of minutes
allowed in aggregate for CPUs by currently running jobs.

**AssocGrpEnergy** — The job's association has reached its aggregate Energy limit.

**AssocGrpEnergyMinutes** — The job's association has reached the maximum number of minutes allowed
in aggregate for Energy by past, present and future jobs.

**AssocGrpEnergyRunMinutes** — The job's association has reached the maximum number of minutes
allowed in aggregate for Energy by currently running jobs.

**AssocGrpGRES** — The job's association has reached its aggregate GRES limit.

**AssocGrpGRESMinutes** — The job's association has reached the maximum number of minutes allowed in
aggregate for a GRES by past, present and future jobs.

**AssocGrpGRESRunMinutes** — The job's association has reached the maximum number of minutes allowed
in aggregate for a GRES by currently running jobs.

**AssocGrpJobsLimit** — The job's association has reached the maximum number of allowed jobs in
aggregate.

**AssocGrpLicense** — The job's association has reached its aggregate license limit.

**AssocGrpLicenseMinutes** — The job's association has reached the maximum number of minutes allowed
in aggregate for Licenses by past, present and future jobs.

**AssocGrpLicenseRunMinutes** — The job's association has reached the maximum number of minutes
allowed in aggregate for Licenses by currently running jobs.

**AssocGrpMemLimit** — The job's association has reached its aggregate Memory limit.

**AssocGrpMemMinutes** — The job's association has reached the maximum number of minutes allowed in
aggregate for Memory by past, present and future jobs.

**AssocGrpMemRunMinutes** — The job's association has reached the maximum number of minutes allowed
in aggregate for Memory by currently running jobs.

**AssocGrpNodeLimit** — The job's association has reached its aggregate Node limit.

**AssocGrpNodeMinutes** — The job's association has reached the maximum number of minutes allowed in
aggregate for Nodes by past, present and future jobs.

**AssocGrpNodeRunMinutes** — The job's association has reached the maximum number of minutes allowed
in aggregate for Nodes by currently running jobs.

**AssocGrpSubmitJobsLimit** — The job's association has reached the maximum number of jobs that can
be running or pending in aggregate at a given time.

**AssocGrpUnknown** — The job's association has reached its aggregate limit for an unknown generic
resource.

**AssocGrpUnknownMinutes** — The job's association has reached the maximum number of minutes allowed
in aggregate for an unknown generic resource by past, present and future jobs.

**AssocGrpUnknownRunMinutes** — The job's association has reached the maximum number of minutes
allowed in aggregate for an unknown generic resource by currently running jobs.

**AssocGrpWallLimit** — The job's association has reached its aggregate limit for the amount of
walltime requested by running jobs.

**AssocMaxBBMinutesPerJob** — The Burst Buffer request exceeds the maximum number of minutes each
job is allowed to use for the requested association.

**AssocMaxBBPerJob** — The Burst Buffer request exceeds the maximum each job is allowed to use for
the requested association.

**AssocMaxBBPerNode** — The Burst Buffer request exceeds the maximum number each node in a job
allocation is allowed to use for the requested association.

**AssocMaxBillingMinutesPerJob** — The request exceeds the maximum number of minutes each job is
allowed to use, with Billing taken into account, for the requested association.

**AssocMaxBillingPerJob** — The resource request exceeds the maximum Billing limit each job is
allowed to use for the requested association.

**AssocMaxBillingPerNode** — The request exceeds the maximum Billing limit each node in a job
allocation is allowed to use for the requested association.

**AssocMaxCpuMinutesPerJobLimit** — The CPU request exceeds the maximum number of minutes each job
is allowed to use for the requested association.

**AssocMaxCpuPerJobLimit** — The CPU request exceeds the maximum each job is allowed to use for the
requested association.

**AssocMaxCpuPerNode** — The request exceeds the maximum number of CPUs each node in a job
allocation is allowed to use for the requested association.

**AssocMaxEnergyMinutesPerJob** — The Energy request exceeds the maximum number of minutes each job
is allowed to use for the requested association.

**AssocMaxEnergyPerJob** — The Energy request exceeds the maximum each job is allowed to use for the
requested association.

**AssocMaxEnergyPerNode** — The request exceeds the maximum amount of Energy each node in a job
allocation is allowed to use for the requested association.

**AssocMaxGRESMinutesPerJob** — The GRES request exceeds the maximum number of minutes each job is
allowed to use for the requested association.

**AssocMaxGRESPerJob** — The GRES request exceeds the maximum each job is allowed to use for the
requested association.

**AssocMaxGRESPerNode** — The request exceeds the maximum number of a GRES each node in a job
allocation is allowed to use for the requested association.

**AssocMaxJobsLimit** — The limit on the number of jobs each user is allowed to run at a given time
has been met for the requested association.

**AssocMaxLicenseMinutesPerJob** — The License request exceeds the maximum number of minutes each
job is allowed to use for the requested association.

**AssocMaxLicensePerJob** — The License request exceeds the maximum each job is allowed to use for
the requested association.

**AssocMaxMemMinutesPerJob** — The Memory request exceeds the maximum number of minutes each job is
allowed to use for the requested association.

**AssocMaxMemPerJob** — The Memory request exceeds the maximum each job is allowed to use for the
requested association.

**AssocMaxMemPerNode** — The request exceeds the maximum amount of Memory each node in a job
allocation is allowed to use for the requested association.

**AssocMaxNodeMinutesPerJob** — The number of nodes requested exceeds the maximum number of minutes
each job is allowed to use for the requested association.

**AssocMaxNodePerJobLimit** — The number of nodes requested exceeds the maximum each job is allowed
to use for the requested association.

**AssocMaxSubmitJobLimit** — The limit on the number of jobs each user is allowed to have running or
pending at a given time has been met for the requested association.

**AssocMaxUnknownMinutesPerJob** — The request of an unknown trackable resource exceeds the maximum
number of minutes each job is allowed to use for the requested association.

**AssocMaxUnknownPerJob** — The request of an unknown trackable resource exceeds the maximum each
job is allowed to use for the requested association.

**AssocMaxUnknownPerNode** — The request exceeds the maximum number of an unknown trackable resource
each node in a job allocation is allowed to use for the requested association.

**AssocMaxWallDurationPerJobLimit** — The limit on the amount of wall time a job can request has
been exceeded for the requested association.

**AssociationJobLimit** — The job's association has reached its maximum job count.

**AssociationResourceLimit** — The job's association has reached some resource limit.

**AssociationTimeLimit** — The job's association has reached its time limit.

**BadConstraints** — The job's constraints can not be satisfied.

**BeginTime** — The job's earliest start time has not yet been reached.

**BurstBufferOperation** — Burst Buffer operation for the job failed.

**BurstBufferResources** — There are insufficient resources in a Burst Buffer resource pool.

**BurstBufferStageIn** — The Burst Buffer plugin is in the process of staging the environment for
the job.

**Cleaning** — The job is being requeued and still cleaning up from its previous execution.

**DeadLine** — This job has violated the configured Deadline.

**Dependency** — This job has a dependency on another job that has not been satisfied.

**DependencyNeverSatisfied** — This job has a dependency on another job that will never be
satisfied.

**FedJobLock** — The job is waiting for the clusters in the federation to sync up and issue a lock.

**FrontEndDown** — No front end node is available to execute this job.

**InactiveLimit** — The job reached the system InactiveLimit.

**InvalidAccount** — The job's account is invalid.

**InvalidQOS** — The job's QOS is invalid.

**JobArrayTaskLimit** — The job array's limit on the number of simultaneously running tasks has been
reached.

**JobHeldAdmin** — The job is held by a system administrator.

**JobHeldUser** — The job is held by the user.

**JobHoldMaxRequeue** — Job has been requeued enough times to reach the MAX_BATCH_REQUEUE limit.

**JobLaunchFailure** — The job could not be launched. This may be due to a file system problem,
invalid program name, etc.

**Licenses** — The job is waiting for a license.

**MaxBBPerAccount** — The job's Burst Buffer request exceeds the per-Account limit on the job's QOS.

**MaxBillingPerAccount** — The job's Billing request exceeds the per-Account limit on the job's QOS.

**MaxCpuPerAccount** — The job's CPU request exceeds the per-Account limit on the job's QOS.

**MaxEnergyPerAccount** — The job's Energy request exceeds the per-Account limit on the job's QOS.

**MaxGRESPerAccount** — The job's GRES request exceeds the per-Account limit on the job's QOS.

**MaxJobsPerAccount** — This job exceeds the per-Account limit on the number of jobs for the job's
QOS.

**MaxLicensePerAccount** — The job's License request exceeds the per-Account limit on the job's QOS.

**MaxMemoryPerAccount** — The job's Memory request exceeds the per-Account limit on the job's QOS.

**MaxMemPerLimit** — The job violates the limit on the maximum amount of Memory per-CPU or per-Node.

**MaxNodePerAccount** — The number of nodes requested by the job exceeds the per-Account limit on
the number of nodes for the job's QOS.

**MaxSubmitJobsPerAccount** — This job exceeds the per-Account limit on the number of jobs in a
pending or running state for the job's QOS.

**MaxUnknownPerAccount** — The jobs request of an unknown GRES exceeds the per-Account limit on the
job's QOS.

**NodeDown** — A node required by the job is down.

**NonZeroExitCode** — The job terminated with a non-zero exit code.

**None** — The job hasn't had a reason assigned to it yet.

**OutOfMemory** — The job failed with an Out Of Memory error.

**PartitionConfig** — Fallback reason when the job violates some limit on the partition.

**PartitionDown** — The partition required by this job is in a DOWN state.

**PartitionInactive** — The partition required by this job is in an Inactive state and not able to
start jobs.

**PartitionNodeLimit** — The number of nodes required by this job is outside of its partition's
current limits. Can also indicate that required nodes are DOWN or DRAINED.

**PartitionTimeLimit** — The job's time limit exceeds its partition's current time limit.

**PowerNotAvail** — The job requests more power than is available when using the cray_aries power
management plugin.

**PowerReserved** — The job's power request is for more than what is currently available when using
the cray_aries power management plugin.

**Priority** — One of more higher priority jobs exist for the partition associated with the job or
for the advanced reservation.

**Prolog** — The job's PrologSlurmctld program is still running.

**QOSGrpBB** — The job's QOS has reached its aggregate Burst Buffer limit.

**QOSGrpBBMinutes** — The job's QOS has reached the maximum number of minutes allowed in aggregate
for Burst Buffers by past, present and future jobs.

**QOSGrpBBRunMinutes** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for Burst Buffers by currently running jobs.

**QOSGrpBilling** — The job's QOS has reached its aggregate Billing limit.

**QOSGrpBillingMinutes** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for the Billing value of a resource by past, present and future jobs.

**QOSGrpBillingRunMinutes** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for the Billing value of a resource by currently running jobs.

**QOSGrpCpuLimit** — The job's QOS has reached its aggregate CPU limit.

**QOSGrpCPUMinutesLimit** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for CPUs by past, present and future jobs.

**QOSGrpCPURunMinutesLimit** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for CPUs by currently running jobs.

**QOSGrpEnergy** — The job's QOS has reached its aggregate Energy limit.

**QOSGrpEnergyMinutes** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for Energy by past, present and future jobs.

**QOSGrpEnergyRunMinutes** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for Energy by currently running jobs.

**QOSGrpGRES** — The job's QOS has reached its aggregate GRES limit.

**QOSGrpGRESMinutes** — The job's QOS has reached the maximum number of minutes allowed in aggregate
for a GRES by past, present and future jobs.

**QOSGrpGRESRunMinutes** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for a GRES by currently running jobs.

**QOSGrpJobsLimit** — The job's QOS has reached the maximum number of allowed jobs in aggregate.

**QOSGrpLicense** — The job's QOS has reached its aggregate license limit.

**QOSGrpLicenseMinutes** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for Licenses by past, present and future jobs.

**QOSGrpLicenseRunMinutes** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for Licenses by currently running jobs.

**QOSGrpMemLimit** — The job's QOS has reached its aggregate Memory limit.

**QOSGrpMemoryMinutes** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for Memory by past, present and future jobs.

**QOSGrpMemoryRunMinutes** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for Memory by currently running jobs.

**QOSGrpNodeLimit** — The job's QOS has reached its aggregate Node limit.

**QOSGrpNodeMinutes** — The job's QOS has reached the maximum number of minutes allowed in aggregate
for Nodes by past, present and future jobs.

**QOSGrpNodeRunMinutes** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for Nodes by currently running jobs.

**QOSGrpSubmitJobsLimit** — The job's QOS has reached the maximum number of jobs that can be running
or pending in aggregate at a given time.

**QOSGrpUnknown** — The job's QOS has reached its aggregate limit for an unknown generic resource.

**QOSGrpUnknownMinutes** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for an unknown generic resource by past, present and future jobs.

**QOSGrpUnknownRunMinutes** — The job's QOS has reached the maximum number of minutes allowed in
aggregate for an unknown generic resource by currently running jobs.

**QOSGrpWallLimit** — The job's QOS has reached its aggregate limit for the amount of walltime
requested by running jobs.

**QOSJobLimit** — The job's QOS has reached its maximum job count.

**QOSMaxBBMinutesPerJob** — The Burst Buffer request exceeds the maximum number of minutes each job
is allowed to use for the requested QOS.

**QOSMaxBBPerJob** — The Burst Buffer request exceeds the maximum each job is allowed to use for the
requested QOS.

**QOSMaxBBPerNode** — The Burst Buffer request exceeds the maximum number each node in a job
allocation is allowed to use for the requested QOS.

**QOSMaxBBPerUser** — The Burst Buffer request exceeds the maximum number each user is allowed to
use for the requested QOS.

**QOSMaxBillingMinutesPerJob** — The request exceeds the maximum number of minutes each job is
allowed to use, with Billing taken into account, for the requested QOS.

**QOSMaxBillingPerJob** — The resource request exceeds the maximum Billing limit each job is allowed
to use for the requested QOS.

**QOSMaxBillingPerNode** — The request exceeds the maximum Billing limit each node in a job
allocation is allowed to use for the requested QOS.

**QOSMaxBillingPerUser** — The request exceeds the maximum Billing limit each user is allowed to use
for the requested QOS.

**QOSMaxCpuMinutesPerJobLimit** — The CPU request exceeds the maximum number of minutes each job is
allowed to use for the requested QOS.

**QOSMaxCpuPerJobLimit** — The CPU request exceeds the maximum each job is allowed to use for the
requested QOS.

**QOSMaxCpuPerNode** — The request exceeds the maximum number of CPUs each node in a job allocation
is allowed to use for the requested QOS.

**QOSMaxCpuPerUserLimit** — The CPU request exceeds the maximum each user is allowed to use for the
requested QOS.

**QOSMaxEnergyMinutesPerJob** — The Energy request exceeds the maximum number of minutes each job is
allowed to use for the requested QOS.

**QOSMaxEnergyPerJob** — The Energy request exceeds the maximum each job is allowed to use for the
requested QOS.

**QOSMaxEnergyPerNode** — The request exceeds the maximum amount of Energy each node in a job
allocation is allowed to use for the requested QOS.

**QOSMaxEnergyPerUser** — The request exceeds the maximum amount of Energy each user is allowed to
use for the requested QOS.

**QOSMaxGRESMinutesPerJob** — The GRES request exceeds the maximum number of minutes each job is
allowed to use for the requested QOS.

**QOSMaxGRESPerJob** — The GRES request exceeds the maximum each job is allowed to use for the
requested QOS.

**QOSMaxGRESPerNode** — The request exceeds the maximum number of a GRES each node in a job
allocation is allowed to use for the requested QOS.

**QOSMaxGRESPerUser** — The request exceeds the maximum number of a GRES each user is allowed to use
for the requested QOS.

**QOSMaxJobsPerUserLimit** — The limit on the number of jobs a user is allowed to run at a given
time has been met for the requested QOS.

**QOSMaxLicenseMinutesPerJob** — The License request exceeds the maximum number of minutes each job
is allowed to use for the requested QOS.

**QOSMaxLicensePerJob** — The License request exceeds the maximum each job is allowed to use for the
requested QOS.

**QOSMaxLicensePerUser** — The License request exceeds the maximum each user is allowed to use for
the requested QOS.

**QOSMaxMemoryMinutesPerJob** — The Memory request exceeds the maximum number of minutes each job is
allowed to use for the requested QOS.

**QOSMaxMemoryPerJob** — The Memory request exceeds the maximum each job is allowed to use for the
requested QOS.

**QOSMaxMemoryPerNode** — The request exceeds the maximum amount of Memory each node in a job
allocation is allowed to use for the requested QOS.

**QOSMaxMemoryPerUser** — The request exceeds the maximum amount of Memory each user is allowed to
use for the requested QOS.

**QOSMaxNodeMinutesPerJob** — The number of nodes requested exceeds the maximum number of minutes
each job is allowed to use for the requested QOS.

**QOSMaxNodePerJobLimit** — The number of nodes requested exceeds the maximum each job is allowed to
use for the requested QOS.

**QOSMaxNodePerUserLimit** — The number of nodes requested exceeds the maximum each user is allowed
to use for the requested QOS.

**QOSMaxSubmitJobPerUserLimit** — The limit on the number of jobs each user is allowed to have
running or pending at a given time has been met for the requested QOS.

**QOSMaxUnknownMinutesPerJob** — The request of an unknown trackable resource exceeds the maximum
number of minutes each job is allowed to use for the requested QOS.

**QOSMaxUnknownPerJob** — The request of an unknown trackable resource exceeds the maximum each job
is allowed to use for the requested QOS.

**QOSMaxUnknownPerNode** — The request exceeds the maximum number of an unknown trackable resource
each node in a job allocation is allowed to use for the requested QOS.

**QOSMaxUnknownPerUser** — The request exceeds the maximum number of an unknown trackable resource
each user is allowed to use for the requested QOS.

**QOSMaxWallDurationPerJobLimit** — The limit on the amount of wall time a job can request has been
exceeded for the requested QOS.

**QOSMinBB** — The Burst Buffer request does not meet the minimum each job is required to request
for the requested QOS.

**QOSMinBilling** — The resource request does not meet the minimum Billing limit each job is allowed
to use for the requested QOS.

**QOSMinCpuNotSatisfied** — The CPU request does not meet the minimum each job is allowed to use for
the requested QOS.

**QOSMinEnergy** — The Energy request does not meet the minimum each job is allowed to use for the
requested QOS.

**QOSMinGRES** — The GRES request does not meet the minimum each job is allowed to use for the
requested QOS.

**QOSMinLicense** — The License request does not meet the minimum each job is allowed to use for the
requested QOS.

**QOSMinMemory** — The Memory request does not meet the minimum each job is allowed to use for the
requested QOS.

**QOSMinNode** — The number of nodes requested does not meet the minimum each job is allowed to use
for the requested QOS.

**QOSMinUnknown** — The request of an unknown trackable resource does not meet the minimum each job
is allowed to use for the requested QOS.

**QOSNotAllowed** — The job requests a QOS is not allowed by the requested association or partition.

**ReservationDeleted** — The job requested a reservation that is no longer on the system.

**QOSResourceLimit** — The job's QOS has reached some resource limit.

**QOSTimeLimit** — The job's QOS has reached its time limit.

**QOSUsageThreshold** — Required QOS threshold has been breached.

**ReqNodeNotAvail** — Some node specifically required by the job is not currently available. The
node may currently be in use, reserved for another job, in an advanced reservation, DOWN, DRAINED,
or not responding. Nodes which are DOWN, DRAINED, or not responding will be identified as part of
the job's "reason" field as "UnavailableNodes". Such nodes will typically require the intervention
of a system administrator to make available.

**Reservation** — The job is waiting its advanced reservation to become available.

**Resources** — The QOS resource limit has been reached.

**SchedDefer** — The job requests an immediate allocation but **SchedulerParameters=defer** is
configured in the slurm.conf.

**SystemFailure** — Failure of the Slurm system, a file system, the network, etc.

**TimeLimit** — The job exhausted its time limit.

Last modified 09 June 2023
