# Slurm User and Administrator Guide for Cray XC Systems

- [User Guide](#user_guide)
- [Cray Specific Features](#features)
- [Administrator Guide](#admin_guide)
- [Cray System Setup](#setup)
- [High Availability](#ha)
- [Cray](http://www.cray.com)

----------------------------------------------------------------------------------------------------

## User Guide

This document describes the unique features of Slurm on Cray XC computers natively, or without the
use of Cray's Application Level Placement Scheduler (ALPS). You should be familiar with the Slurm's
mode of operation on Linux clusters before studying the differences in Cray system operation
described in this document. When running Slurm in native mode a Cray system will function very
similar to a Linux cluster.

Slurm is designed to operate as a workload manager on Cray XC systems (Cascade) without the use of
ALPS. In addition to providing the same look and feel of a regular Linux cluster this also allows
for many functionalities such as:

- Ability to run multiple jobs per node
- Ability to status running jobs with sstat
- Full accounting support for job steps
- Ability to run multiple jobs/steps in background from the same session

## Cray Specific Features

- Network Performance Counters

  To access Cray's Network Performance Counters (NPC) you can use the *--network* option in
  sbatch/salloc/srun to request them. There are 2 different types of counters, system and blade.

  For the system option (--network=system) only one job can use system at a time. Only nodes
  requested will be marked in use for the job allocation. If the job does not fill up the entire
  system the rest of the nodes are not able to be used by other jobs using NPC, if idle their state
  will appear as PerfCnts. These nodes are still available for other jobs not using NPC.

  For the blade option (--network=blade) Only nodes requested will be marked in use for the job
  allocation. If the job does not fill up the entire blade(s) allocated to the job those blade(s)
  are not able to be used by other jobs using NPC, if idle their state will appear as PerfCnts.
  These nodes are still available for other jobs not using NPC.

- Core Specialization

  To use set ***CoreSpecPlugin=core_spec/cray_aries***. Ability to reserve a number of cores
  allocated to the job for system operations and not used by the application. The application will
  not use these cores, but will be charged for their allocation.

## Admin Guide

Many new plugins were added to utilize the Cray system without ALPS. These should be set up in your
slurm.conf outside of your normal configuration.

- AcctGatherEnergyType

  Set ***AcctGatherEnergyType=acct_gather_energy/pm_counters*** to have the Cray XC baseboard
  management controller report energy usage data to Slurm.

- BurstBuffer

  Set ***BurstBufferPlugins=burst_buffer/datawarp*** to use. The burst buffer capability on Cray
  systems is also known by the name *DataWarp*. For more information, see [Slurm Burst Buffer
  Guide](burst_buffer.md).

- CoreSpec

  To use set ***CoreSpecPlugin=core_spec/cray_aries***.

- JobSubmit

  Set ***JobSubmitPlugins=job_submit/cray_aries*** to use. This plugin is primarily used to set a
  gres=craynetwork value which is used to limit the number of applications that can run on a node at
  once. That number can be at most 4. This craynetwork gres needs to be set up in your slurm.conf to
  ensure proper functionality. For example...

<!-- -->

        ...
        Grestypes=craynetwork
        NodeName=nid000[00-10] gres=craynetwork:4
        ...
      

Power

Set ***PowerPlugin=power/cray_aries*** to use. ***PowerParameters*** is also typically configured.
For more information, see [Slurm Power Management Guide](power_mgmt.md).

Proctrack

Set ***ProctrackType=proctrack/cray_aries*** to use.

Select

Set ***SelectType=select/cray_aries*** to use. This plugin is a layered plugin. Which means it
enhances a lower layer select plugin. By default it is layered on top of the *select/linear* plugin.
It can also be layered on top of the *select/cons_res* plugin by using the
***SelectTypeParameters=other_cons_res***, doing this will allow you to run multiple jobs on a Cray
node just like on a normal Linux cluster. Use additional ***SelectTypeParameters*** to identify the
resources to allocate (e.g. cores, sockets, memory, etc.). See the slurm.conf man page for details.

SlurmctldPort, SlurmdPort, SrunPortRange

Realm-Specific IP Addressing (RSIP) will automatically try to interact with anything opened on ports
8192 to 60000. Configure SlurmctldPort, SlurmdPort, and SrunPortRange to use ports above 60000. In
the case of SrunPortRange, making 1000 or more ports available is recommended.

Switch

Set ***SwitchType=switch/cray_aries*** to use.

Task

Set ***TaskPlugin=cray_aries,cgroup*** to use. Use of the ***task/cgroup*** plugin is required
alongside *task/cray_aries*. You may also use the *task/affinity* plugin along with
*task/cray_aries,task/cgroup* if desired (i.e. ***TaskPlugin=cray_aries,affinity,cgroup***). Note
that plugins are used in the order they are defined in the comma separated list, and that
*task/cray_aries* must be listed before *task/cgroup* due to internal dependencies between the two
plugins.

## Cray system setup

Some Slurm plugins (burst_buffer/datawarp and power/cray_aries) plugins parse JSON format data.
These plugins are designed to make use of the JSON-C library for this purpose. See [JSON-C
installation instructions](download.md#json) for details.

Some services on the system need to be set up to run correctly with Slurm. Below is how to restart
the service and the nodes they run on. It is probably a good idea to set this up to happen
automatically.

- boot node
  - WLM_DETECT_ACTIVE=SLURM /etc/init.d/aeld restart
- sdb node
  - WLM_DETECT_ACTIVE=SLURM /etc/init.d/ncmd restart
  - WLM_DETECT_ACTIVE=SLURM /etc/init.d/apptermd restart

As with Linux clusters you will need to start a slurmd on each of your compute nodes. If you choose
to use munge authentication, advised, you will also need munge installed and a munged running on
each of your compute nodes as well. See the [quick start guide](quickstart_admin.md) for more info.
Outside of the differences listed in this file it can be used to set up your Cray system to run
Slurm natively.

On larger systems, you may wish to set the PMI_MMAP_SYNC_WAIT_TIME environment variable in your
users' profiles to a larger value than the default (180 seconds) to prevent PMI from falsely
detecting job launch failures.

## High Availability

A backup controller can be setup in or outside the Cray. However, when the backup is within the
Cray, both the primary and the backup controllers will go down when the Cray is rebooted. It is best
to setup the backup controller on a Cray external node so that the controller can still receive new
jobs when the Cray is down. When the backup is configured on an external node the
***no_backup_scheduling*** ***SchedulerParameter*** should be specified in the slurm.conf. This
allows new jobs to be submitted while the Cray is down and prevents any new jobs from being started.

Last modified 27 July 2023
