# Quick Start Administrator Guide

## Contents

- [Overview](#overview)
- [Super Quick Start](#quick_start)
- [Building and Installing Slurm](#build_install)
  - [Installing Prerequisites](#prereqs)
  - [Building Manually](#manual_build)
  - [Building RPMs](#rpmbuild)
  - [Installing RPMs](#rpms)
- [Daemons](#daemons)
- [Infrastructure](#infrastructure)
- [Configuration](#Config)
- [Security](#security)
- [Starting the Daemons](#starting_daemons)
- [Administration Examples](#admin_examples)
- [Upgrades](#upgrade)
- [FreeBSD](#FreeBSD)

## Overview

Please see the [Quick Start User Guide](quickstart.md) for a general overview.

Also see [Platforms](platforms.md) for a list of supported computer platforms.

This document also includes a section specifically describing how to perform [upgrades](#upgrade).

## Super Quick Start

1.  Make sure the clocks, users and groups (UIDs and GIDs) are synchronized across the cluster.
2.  Install [MUNGE](https://dun.github.io/munge/) for authentication. Make sure that all nodes in
    your cluster have the same *munge.key*. Make sure the MUNGE daemon, *munged*, is started before
    you start the Slurm daemons.
3.  bunzip2 the distributed tar-ball and untar the files:  
    *tar --bzip -x -f slurm\*tar.bz2*
4.  *cd* to the directory containing the Slurm source and type *./configure* with appropriate
    options, typically *--prefix=* and *--sysconfdir=*
5.  Type *make* to compile Slurm.
6.  Type *make install* to install the programs, documentation, libraries, header files, etc.
7.  Build a configuration file using your favorite web browser and the [Slurm Configuration
    Tool](configurator.md).  
    **NOTE**: The *SlurmUser* must exist prior to starting Slurm and must exist on all nodes of the
    cluster.  
    **NOTE**: The parent directories for Slurm's log files, process ID files, state save
    directories, etc. are not created by Slurm. They must be created and made writable by
    *SlurmUser* as needed prior to starting Slurm daemons.  
    **NOTE**: If any parent directories are created during the installation process (for the
    executable files, libraries, etc.), those directories will have access rights equal to
    read/write/execute for everyone minus the umask value (e.g. umask=0022 generates directories
    with permissions of "drwxr-r-x" and mask=0000 generates directories with permissions of
    "drwxrwrwx" which is a security problem).
8.  Type *ldconfig -n \<library_location\>* so that the Slurm libraries can be found by applications
    that intend to use Slurm APIs directly.
9.  Install the configuration file in *\<sysconfdir\>/slurm.conf*.  
    **NOTE**: You will need to install this configuration file on all nodes of the cluster.
10. systemd (optional): enable the appropriate services on each system:
    - Controller: `systemctl enable slurmctld`
    - Database: `systemctl enable slurmdbd`
    - Compute Nodes: `systemctl enable slurmd`
11. Start the *slurmctld* and *slurmd* daemons.

**NOTE**: Items 3 through 8 can be replaced with

1.  `rpmbuild -ta slurm*.tar.bz2`
2.  `rpm --install <the rpm files>`

FreeBSD administrators should see the [FreeBSD](#FreeBSD) section below.

## Building and Installing Slurm

### Installing Prerequisites

Before building Slurm, consider which plugins you will need for your installation. Which plugins are
built can vary based on the libraries that are available when running configure. Refer to the below
list of possible plugins and what is required to build them.

- **AMD GPU Support** Autodetection of AMD GPUs will be available if the *ROCm* development library
  is installed.
- **cgroup Task Constraining** The *task/cgroup* plugin will be built if the *hwloc* development
  library is present. cgroup/v2 support also requires the *bpf* and *dbus* development libraries.
- **HDF5 Job Profiling** The *acct_gather_profile/hdf5* job profiling plugin will be built if the
  *hdf5* development library is present.
- **HTML Man Pages** HTML versions of the man pages will be generated if the *man2html* command is
  present.
- **InfiniBand Accounting** The *acct_gather_interconnect/ofed* InfiniBand accounting plugin will be
  built if the *libibmad* and *libibumad* development libraries are present.
- **Intel GPU Support** Autodetection of Intel GPUs will be available if the *libvpl* development
  library is installed.
- **IPMI Energy Consumption** The *acct_gather_energy/ipmi* accounting plugin will be built if the
  *freeipmi* development library is present.
- **Lua Support** The lua API will be available in various plugins if the *lua* development library
  is present.
- **MUNGE** The auth/munge plugin will be built if the MUNGE authentication development library is
  installed. MUNGE is used as the default authentication mechanism.
- **MySQL** MySQL support for accounting will be built if the *MySQL* or *MariaDB* development
  library is present. A currently supported version of MySQL or MariaDB should be used.
- **NUMA Affinity** NUMA support in the task/affinity plugin will be available if the *numa*
  development library is installed.
- **NVIDIA GPU Support** Autodetection of NVIDIA GPUs will be available if the *libnvidia-ml*
  development library is installed.
- **PAM Support** PAM support will be added if the *PAM* development library is installed.
- **PMIx** PMIx support will be added if the *pmix* development library is installed.
- **Readline Support** Readline support in scontrol and sacctmgr's interactive modes will be
  available if the *readline* development library is present.
- **REST API** Support for Slurm's REST API will be built if the *http-parser* and *json-c*
  development libraries are installed. Additional functionality will be included if the optional
  *yaml* and *jwt* development libraries are installed.
- **RRD External Sensor Data Collection** The *ext_sensors/rrd* plugin will be built if the
  *rrdtool* development library is present.
- **sview** The sview command will be built only if *gtk+-2.0* is installed.

Please see the [Download](download.md) page for references to required software to build these
plugins.

If required libraries or header files are in non-standard locations, set `CFLAGS` and `LDFLAGS`
environment variables accordingly.

### Building Manually

Instructions to build and install Slurm manually are shown below. See the README and INSTALL files
in the source distribution for more details.

1.  Unpack the distributed tarball:  
    `tar -xaf slurm*tar.bz2`
2.  `cd` to the directory containing the Slurm source and type `./configure` with appropriate
    options (see below).
3.  Type `make install` to compile and install the programs, documentation, libraries, header files,
    etc.
4.  Type `ldconfig -n <library_location>` so that the Slurm libraries can be found by applications
    that intend to use Slurm APIs directly. The library location will be a subdirectory of PREFIX
    (described below) and depend upon the system type and configuration, typically lib or lib64. For
    example, if PREFIX is "/usr" and the subdirectory is "lib64" then you would find that a file
    named "/usr/lib64/libslurm.so" was installed and the command `ldconfig -n /usr/lib64` should be
    executed.

A full list of `configure` options will be returned by the command `configure --help`. The most
commonly used arguments to the `configure` command include:

`--enable-debug`  
Enable additional debugging logic within Slurm.

`--prefix=`*`PREFIX`*  
Install architecture-independent files in PREFIX; default value is /usr/local.

`--sysconfdir=`*`DIR`*  
Specify location of Slurm configuration file. The default value is PREFIX/etc

### Building RPMs

To build RPMs directly, copy the distributed tarball into a directory and execute (substituting the
appropriate Slurm version number):  
`rpmbuild -ta slurm-23.02.7.tar.bz2`

The rpm files will be installed under the `$(HOME)/rpmbuild` directory of the user building them.

You can control some aspects of the RPM built with a *.rpmmacros* file in your home directory.
**Special macro definitions will likely only be required if files are installed in unconventional
locations.** A full list of *rpmbuild* options can be found near the top of the slurm.spec file.
Some macro definitions that may be used in building Slurm include:

\_enable_debug  
Specify if debugging logic within Slurm is to be enabled

\_prefix  
Pathname of directory to contain the Slurm files

\_slurm_sysconfdir  
Pathname of directory containing the slurm.conf configuration file (default /etc/slurm)

with_munge  
Specifies the MUNGE (authentication library) installation location

An example .rpmmacros file:

    # .rpmmacros
    # Override some RPM macros from /usr/lib/rpm/macros
    # Set Slurm-specific macros for unconventional file locations
    #
    %_enable_debug     "--with-debug"
    %_prefix           /opt/slurm
    %_slurm_sysconfdir %{_prefix}/etc/slurm
    %_defaultdocdir    %{_prefix}/doc
    %with_munge        "--with-munge=/opt/munge"

### RPMs Installed

The RPMs needed on the head node, compute nodes, and slurmdbd node can vary by configuration, but
here is a suggested starting point:

- Head Node (where the slurmctld daemon runs),  
  Compute and Login Nodes
  - slurm
  - slurm-perlapi
  - slurm-slurmctld (only on the head node)
  - slurm-slurmd (only on the compute nodes)
- SlurmDBD Node
  - slurm
  - slurm-slurmdbd

## Daemons

**slurmctld** is sometimes called the "controller". It orchestrates Slurm activities, including
queuing of jobs, monitoring node states, and allocating resources to jobs. There is an optional
backup controller that automatically assumes control in the event the primary controller fails (see
the [High Availability](#HA) section below). The primary controller resumes control whenever it is
restored to service. The controller saves its state to disk whenever there is a change in state (see
"StateSaveLocation" in [Configuration](#Config) section below). This state can be recovered by the
controller at startup time. State changes are saved so that jobs and other state information can be
preserved when the controller moves (to or from a backup controller) or is restarted.

We recommend that you create a Unix user *slurm* for use by **slurmctld**. This user name will also
be specified using the **SlurmUser** in the slurm.conf configuration file. This user must exist on
all nodes of the cluster. Note that files and directories used by **slurmctld** will need to be
readable or writable by the user **SlurmUser** (the Slurm configuration files must be readable; the
log file directory and state save directory must be writable).

The **slurmd** daemon executes on every compute node. It resembles a remote shell daemon to export
control to Slurm. Because slurmd initiates and manages user jobs, it must execute as the user root.

If you want to archive job accounting records to a database, the **slurmdbd** (Slurm DataBase
Daemon) should be used. We recommend that you defer adding accounting support until after basic
Slurm functionality is established on your system. An [Accounting](accounting.md) web page contains
more information.

**slurmctld** and/or **slurmd** should be initiated at node startup time per the Slurm
configuration.

The **slurmrestd** daemon was introduced in version 20.02 and allows clients to communicate with
Slurm via the REST API. This is installed by default, assuming the [prerequisites](rest.md#prereq)
are met. It has two [run modes](slurmrestd.md#SECTION_DESCRIPTION), allowing you to have it run as a
traditional Unix service and always listen for TCP connections, or you can have it run as an Inet
service and only have it active when in use.

### High Availability

Multiple SlurmctldHost entries can be configured, with any entry beyond the first being treated as a
backup host. Any backup hosts configured should be on a different node than the node hosting the
primary slurmctld. However, all hosts should mount a common file system containing the state
information (see "StateSaveLocation" in the [Configuration](#Config) section below).

If more than one host is specified, when the primary fails the second listed SlurmctldHost will take
over for it. When the primary returns to service, it notifies the backup. The backup then saves the
state and returns to backup mode. The primary reads the saved state and resumes normal operation.
Likewise, if both of the first two listed hosts fail the third SlurmctldHost will take over until
the primary returns to service. Other than a brief period of non- responsiveness, the transition
back and forth should go undetected.

Note that with an already running cluster, changing the order of the SlurmctldHost entries via
`scontrol reconfigure` is not supported. The supported method is to drain and restart the cluster
since running jobs may still go the previous primary controller when completing and delay
scheduling.

Prior to 18.08, Slurm used the ["BackupAddr"](slurm.conf.md#OPT_BackupAddr) and
["BackupController"](slurm.conf.md#OPT_BackupController) parameters for High Availability. These
parameters have been deprecated and are replaced by
["SlurmctldHost"](slurm.conf.md#OPT_SlurmctldHost). Also see ["
SlurmctldPrimaryOnProg"](slurm.conf.md#OPT_SlurmctldPrimaryOnProg) and ["
SlurmctldPrimaryOffProg"](slurm.conf.md#OPT_SlurmctldPrimaryOffProg) to adjust the actions taken
when machines transition between being the primary controller.

Any time the slurmctld daemon or hardware fails before state information reaches disk can result in
lost state. Slurmctld writes state frequently (every five seconds by default), but with large
numbers of jobs, the formatting and writing of records can take seconds and recent changes might not
be written to disk. Another example is if the state information is written to file, but that
information is cached in memory rather than written to disk when the node fails. The interval
between state saves being written to disk can be configured at build time by defining SAVE_MAX_WAIT
to a different value than five.

## Infrastructure

### User and Group Identification

There must be a uniform user and group name space (including UIDs and GIDs) across the cluster. It
is not necessary to permit user logins to the control hosts (**SlurmctldHost**), but the users and
groups must be resolvable on those hosts.

### Authentication of Slurm communications

All communications between Slurm components are authenticated. The authentication infrastructure is
provided by a dynamically loaded plugin chosen at runtime via the **AuthType** keyword in the Slurm
configuration file. The only currently supported authentication types is
[munge](https://dun.github.io/munge/), which requires the installation of the MUNGE package. When
using MUNGE, all nodes in the cluster must be configured with the same *munge.key* file. The MUNGE
daemon, *munged*, must also be started before Slurm daemons. Note that MUNGE does require clocks to
be synchronized throughout the cluster, usually done by NTP.

### MPI support

Slurm supports many different MPI implementations. For more information, see
[MPI](quickstart.md#mpi).

### Scheduler support

Slurm can be configured with rather simple or quite sophisticated scheduling algorithms depending
upon your needs and willingness to manage the configuration (much of which requires a database). The
first configuration parameter of interest is **PriorityType** with two options available: *basic*
(first-in-first-out) and *multifactor*. The *multifactor* plugin will assign a priority to jobs
based upon a multitude of configuration parameters (age, size, fair-share allocation, etc.) and its
details are beyond the scope of this document. See the [Multifactor Job Priority
Plugin](priority_multifactor.md) document for details.

The **SchedType** configuration parameter controls how queued jobs are scheduled and several options
are available.

- *builtin* will initiate jobs strictly in their priority order, typically (first-in-first-out)
- *backfill* will initiate a lower-priority job if doing so does not delay the expected initiation
  time of higher priority jobs; essentially using smaller jobs to fill holes in the resource
  allocation plan. Effective backfill scheduling does require users to specify job time limits.
- *gang* time-slices jobs in the same partition/queue and can be used to preempt jobs from
  lower-priority queues in order to execute jobs in higher priority queues.

For more information about scheduling options see [Gang Scheduling](gang_scheduling.md),
[Preemption](preempt.md), [Resource Reservation Guide](reservations.md), [Resource
Limits](resource_limits.md) and [Sharing Consumable Resources](cons_res_share.md).

### Resource selection

The resource selection mechanism used by Slurm is controlled by the **SelectType** configuration
parameter. If you want to execute multiple jobs per node, but track and manage allocation of the
processors, memory and other resources, the *cons_res* (consumable resources) or *cons_tres*
(consumable trackable resources) plugins are recommended. For more information, please see
[Consumable Resources in Slurm](cons_res.md).

### Logging

Slurm uses syslog to record events if the `SlurmctldLogFile` and `SlurmdLogFile` locations are not
set.

### Accounting

Slurm supports accounting records being written to a simple text file, directly to a database (MySQL
or MariaDB), or to a daemon securely managing accounting data for multiple clusters. For more
information see [Accounting](accounting.md).

### Compute node access

Slurm does not by itself limit access to allocated compute nodes, but it does provide mechanisms to
accomplish this. There is a Pluggable Authentication Module (PAM) for restricting access to compute
nodes available for download. When installed, the Slurm PAM module will prevent users from logging
into any node that has not be assigned to that user. On job termination, any processes initiated by
the user outside of Slurm's control may be killed using an *Epilog* script configured in
*slurm.conf*.

## Configuration

The Slurm configuration file includes a wide variety of parameters. This configuration file must be
available on each node of the cluster and must have consistent contents. A full description of the
parameters is included in the *slurm.conf* man page. Rather than duplicate that information, a
minimal sample configuration file is shown below. Your slurm.conf file should define at least the
configuration parameters defined in this sample and likely additional ones. Any text following a "#"
is considered a comment. The keywords in the file are not case sensitive, although the argument
typically is (e.g., "SlurmUser=slurm" might be specified as "slurmuser=slurm"). The control machine,
like all other machine specifications, can include both the host name and the name used for
communications. In this case, the host's name is "mcri" and the name "emcri" is used for
communications. In this case "emcri" is the private management network interface for the host
"mcri". Port numbers to be used for communications are specified as well as various timer values.

The *SlurmUser* must be created as needed prior to starting Slurm and must exist on all nodes in
your cluster. The parent directories for Slurm's log files, process ID files, state save
directories, etc. are not created by Slurm. They must be created and made writable by *SlurmUser* as
needed prior to starting Slurm daemons.

A description of the nodes and their grouping into partitions is required. A simple node range
expression may optionally be used to specify ranges of nodes to avoid building a configuration file
with large numbers of entries. The node range expression can contain one pair of square brackets
with a sequence of comma separated numbers and/or ranges of numbers separated by a "-" (e.g.
"linux\[0-64,128\]", or "lx\[15,18,32-33\]"). Up to two numeric ranges can be included in the
expression (e.g. "rack\[0-63\]\_blade\[0-41\]"). If one or more numeric expressions are included,
one of them must be at the end of the name (e.g. "unit\[0-31\]rack" is invalid), but arbitrary names
can always be used in a comma separated list.

Node names can have up to three name specifications: **NodeName** is the name used by all Slurm
tools when referring to the node, **NodeAddr** is the name or IP address Slurm uses to communicate
with the node, and **NodeHostname** is the name returned by the command */bin/hostname -s*. Only
**NodeName** is required (the others default to the same name), although supporting all three
parameters provides complete control over naming and addressing the nodes. See the *slurm.conf* man
page for details on all configuration parameters.

Nodes can be in more than one partition and each partition can have different constraints (permitted
users, time limits, job size limits, etc.). Each partition can thus be considered a separate queue.
Partition and node specifications use node range expressions to identify nodes in a concise fashion.
This configuration file defines a 1154-node cluster for Slurm, but it might be used for a much
larger cluster by just changing a few node range expressions. Specify the minimum processor count
(CPUs), real memory space (RealMemory, megabytes), and temporary disk space (TmpDisk, megabytes)
that a node should have to be considered available for use. Any node lacking these minimum
configuration values will be considered DOWN and not scheduled. Note that a more extensive sample
configuration file is provided in **etc/slurm.conf.example**. We also have a web-based
[configuration tool](configurator.md) which can be used to build a simple configuration file, which
can then be manually edited for more complex configurations.

    #
    # Sample /etc/slurm.conf for mcr.llnl.gov
    #
    SlurmctldHost=mcri(12.34.56.78)
    SlurmctldHost=mcrj(12.34.56.79)
    #
    AuthType=auth/munge
    Epilog=/usr/local/slurm/etc/epilog
    JobCompLoc=/var/tmp/jette/slurm.job.log
    JobCompType=jobcomp/filetxt
    PluginDir=/usr/local/slurm/lib/slurm
    Prolog=/usr/local/slurm/etc/prolog
    SchedulerType=sched/backfill
    SelectType=select/linear
    SlurmUser=slurm
    SlurmctldPort=7002
    SlurmctldTimeout=300
    SlurmdPort=7003
    SlurmdSpoolDir=/var/spool/slurmd.spool
    SlurmdTimeout=300
    StateSaveLocation=/var/spool/slurm.state
    SwitchType=switch/none
    TreeWidth=50
    #
    # Node Configurations
    #
    NodeName=DEFAULT CPUs=2 RealMemory=2000 TmpDisk=64000 State=UNKNOWN
    NodeName=mcr[0-1151] NodeAddr=emcr[0-1151]
    #
    # Partition Configurations
    #
    PartitionName=DEFAULT State=UP
    PartitionName=pdebug Nodes=mcr[0-191] MaxTime=30 MaxNodes=32 Default=YES
    PartitionName=pbatch Nodes=mcr[192-1151]

## Security

Besides authentication of Slurm communications based upon the value of the **AuthType**, digital
signatures are used in job step credentials. This signature is used by *slurmctld* to construct a
job step credential, which is sent to *srun* and then forwarded to *slurmd* to initiate job steps.
This design offers improved performance by removing much of the job step initiation overhead from
the *slurmctld* daemon. The digital signature mechanism is specified by the **CredType**
configuration parameter and the default mechanism is MUNGE.

### Authentication

Authentication of communications (identifying who generated a particular message) between Slurm
components can use a different security mechanism that is configurable. You must specify one "auth"
plugin for this purpose using the **AuthType** configuration parameter. Currently, only one
authentication plugin is supported: **auth/munge**. [MUNGE](https://dun.github.io/munge/) should be
installed in order to get properly authenticated communications. We recommend the use of MUNGE. The
configure script in the top-level directory of this distribution will determine which authentication
plugins may be built. The configuration file specifies which of the available plugins will be
utilized.

### Pluggable Authentication Module (PAM) support

A PAM module (Pluggable Authentication Module) is available for Slurm that can prevent a user from
accessing a node which he has not been allocated, if that mode of operation is desired.

## Starting the Daemons

For testing purposes you may want to start by just running slurmctld and slurmd on one node. By
default, they execute in the background. Use the <span class="commandline">-D</span> option for each
daemon to execute them in the foreground and logging will be done to your terminal. The
<span class="commandline">-v</span> option will log events in more detail with more v's increasing
the level of detail (e.g. <span class="commandline">-vvvvvv</span>). You can use one window to
execute "*slurmctld -D -vvvvvv*", a second window to execute "*slurmd -D -vvvvv*". You may see
errors such as "Connection refused" or "Node X not responding" while one daemon is operative and the
other is being started, but the daemons can be started in any order and proper communications will
be established once both daemons complete initialization. You can use a third window to execute
commands such as "*srun -N1 /bin/hostname*" to confirm functionality.

Another important option for the daemons is "-c" to clear previous state information. Without the
"-c" option, the daemons will restore any previously saved state information: node state, job state,
etc. With the "-c" option all previously running jobs will be purged and node state will be restored
to the values specified in the configuration file. This means that a node configured down manually
using the <span class="commandline">scontrol</span> command will be returned to service unless noted
as being down in the configuration file. In practice, Slurm consistently restarts with preservation.

## Administration Examples

<span class="commandline">scontrol</span> can be used to print all system information and modify
most of it. Only a few examples are shown below. Please see the scontrol man page for full details.
The commands and options are all case insensitive.

Print detailed state of all jobs in the system.

    adev0: scontrol
    scontrol: show job
    JobId=475 UserId=bob(6885) Name=sleep JobState=COMPLETED
       Priority=4294901286 Partition=batch BatchFlag=0
       AllocNode:Sid=adevi:21432 TimeLimit=UNLIMITED
       StartTime=03/19-12:53:41 EndTime=03/19-12:53:59
       NodeList=adev8 NodeListIndecies=-1
       NumCPUs=0 MinNodes=0 OverSubscribe=0 Contiguous=0
       MinCPUs=0 MinMemory=0 Features=(null) MinTmpDisk=0
       ReqNodeList=(null) ReqNodeListIndecies=-1

    JobId=476 UserId=bob(6885) Name=sleep JobState=RUNNING
       Priority=4294901285 Partition=batch BatchFlag=0
       AllocNode:Sid=adevi:21432 TimeLimit=UNLIMITED
       StartTime=03/19-12:54:01 EndTime=NONE
       NodeList=adev8 NodeListIndecies=8,8,-1
       NumCPUs=0 MinNodes=0 OverSubscribe=0 Contiguous=0
       MinCPUs=0 MinMemory=0 Features=(null) MinTmpDisk=0
       ReqNodeList=(null) ReqNodeListIndecies=-1

Print the detailed state of job 477 and change its priority to zero. A priority of zero prevents a
job from being initiated (it is held in "pending" state).

    adev0: scontrol
    scontrol: show job 477
    JobId=477 UserId=bob(6885) Name=sleep JobState=PENDING
       Priority=4294901286 Partition=batch BatchFlag=0
       more data removed....
    scontrol: update JobId=477 Priority=0

Print the state of node adev13 and drain it. To drain a node, specify a new state of DRAIN, DRAINED,
or DRAINING. Slurm will automatically set it to the appropriate value of either DRAINING or DRAINED
depending on whether the node is allocated or not. Return it to service later.

    adev0: scontrol
    scontrol: show node adev13
    NodeName=adev13 State=ALLOCATED CPUs=2 RealMemory=3448 TmpDisk=32000
       Weight=16 Partition=debug Features=(null)
    scontrol: update NodeName=adev13 State=DRAIN
    scontrol: show node adev13
    NodeName=adev13 State=DRAINING CPUs=2 RealMemory=3448 TmpDisk=32000
       Weight=16 Partition=debug Features=(null)
    scontrol: quit
    Later
    adev0: scontrol
    scontrol: show node adev13
    NodeName=adev13 State=DRAINED CPUs=2 RealMemory=3448 TmpDisk=32000
       Weight=16 Partition=debug Features=(null)
    scontrol: update NodeName=adev13 State=IDLE

Reconfigure all Slurm daemons on all nodes. This should be done after changing the Slurm
configuration file.

    adev0: scontrol reconfig

Print the current Slurm configuration. This also reports if the primary and secondary controllers
(slurmctld daemons) are responding. To just see the state of the controllers, use the command
<span class="commandline">ping</span>.

    adev0: scontrol show config
    Configuration data as of 2019-03-29T12:20:45
    ...
    SlurmctldAddr           = eadevi
    SlurmctldDebug          = info
    SlurmctldHost[0]        = adevi
    SlurmctldHost[1]        = adevj
    SlurmctldLogFile        = /var/log/slurmctld.log
    ...

    Slurmctld(primary) at adevi is UP
    Slurmctld(backup) at adevj is UP

Shutdown all Slurm daemons on all nodes.

    adev0: scontrol shutdown

## Upgrades

Background: The Slurm version number contains three period-separated numbers that represent both the
major Slurm release and maintenance release level. The first two parts combine together to represent
the major release, and match the year and month of that major release. The third number in the
version designates a specific maintenance level: year.month.maintenance-release (e.g. 21.08.2 is
major Slurm release 21.08, and maintenance version 2). Thus version 21.08.x was initially released
in August 2021. Changes in the RPCs (remote procedure calls) and state files will only be made if
the major release number changes, which typically happens about every nine months. A list of most
recent major Slurm releases is shown below.

- 21.08.x (Released August 2021)
- 22.05.x (Released May 2022)
- 23.02.x (Released February 2023)

If the SlurmDBD daemon is used, it must be at the same or higher major release number as the
Slurmctld daemons. In other words, when changing the version to a higher release number (e.g from
21.08.x to 22.05.x) **always upgrade the SlurmDBD daemon first**. Database table changes may be
required for the upgrade, for example adding new fields to existing tables. This must complete
**before** upgrading slurmctld. If the database contains a large number of entries, **the SlurmDBD
daemon may require tens of minutes to update the database and be unresponsive during this time
interval**.

Before upgrading SlurmDBD **it is strongly recommended to make a backup of the database**. We
recommend you only backup the database used by **slurmdbd** to limit the time spent creating the
backup and avoid potential problems when restoring from a file that contains multiple databases. If
using mysqldump, the default behavior is to lock the tables, which can cause issues if **SlurmDBD**
is still trying to send updates to the database. If you must make a backup while the cluster is
still active we recommend you use the *--single-transaction* flag with mysqldump to avoid locking
tables. This will dump a consistent state of the database without blocking any applications. Note
that in order for this flag to have the desired effect you must be using the InnoDB storage engine
(specified by default when Slurm automatically creates any table) (e.g.
<span class="commandline">mysqldump --single-transaction --databases slurm_acct_db \>
backup.sql</span>).

Our recommendation is to first stop the **SlurmDBD** daemon and then backup the database (using a
tool like mysqldump, Percona xtrabackup or other) before proceeding with the upgrade. Note that
requests intended for **SlurmDBD** from **Slurmctld** will be queued while **SlurmDBD** is down, but
the queue size is limited and you should monitor the DBD Agent Queue size with the **sdiag**
command.

**NOTE**: If you have an existing Slurm accounting database and plan to upgrade your database server
to MariaDB 10.2.1 (or newer) from a pre-10.2.1 version or from any version of MySQL, please contact
SchedMD for assistance.

The slurmctld daemon must also be upgraded before or at the same time as the client commands and
slurmd daemons on the compute nodes. Generally, upgrading Slurm on all of the login and compute
nodes is recommended, although rolling upgrades are also possible (i.e. upgrading the head node(s)
first then upgrading the compute and login nodes later at various times). Also see the note above
about reverse compatibility.

Almost every new major release of Slurm (e.g. 22.05.x to 23.02.x) involves changes to the state
files with new data structures, new options, etc. Slurm permits upgrades to a new major release from
the past two major releases, which happen every nine months (e.g. 21.08.x or 22.05.x to 23.02.x)
without loss of jobs or other state information. State information from older versions will not be
recognized and will be discarded, resulting in loss of all running and pending jobs. State files are
**not** recognized when downgrading (e.g. from 23.02.x to 22.05.x) and will be discarded, resulting
in loss of all running and pending jobs. For this reason, creating backup copies of state files (as
described below) can be of value. Therefore when upgrading Slurm (more precisely, the slurmctld
daemon), saving the *StateSaveLocation* (as defined in *slurm.conf*) directory contents with all
state information is recommended. If you need to downgrade, restoring that directory's contents will
let you recover the jobs. Jobs submitted under the new version will not be in those state files, but
it can let you recover most jobs. An exception to this is that jobs may be lost when installing new
pre-release versions (e.g. 22.05.0-pre1 to 22.05.0-pre2). Developers will try to note these cases in
the NEWS file. Contents of major releases are also described in the RELEASE_NOTES file.

A common approach when performing upgrades is to install the new version of Slurm to a unique
directory and use a symbolic link to point the directory in your PATH to the version of Slurm you
would like to use. This allows you to install the new version before you are in a maintenance period
as well as easily switch between versions should you need to roll back for any reason. It also
avoids potential problems with library conflicts that might arise from installing different versions
to the same directory.

Slurm's main public API library (libslurm.so.X.0.0) increases its version number with every major
release, so any application linked against it should be recompiled after an upgrade. This includes
locally developed Slurm plugins.

If you have built your own version of Slurm plugins, besides having to recompile them, they will
likely need modification to support the new version of Slurm. It is common for plugins to add new
functions and function arguments during major updates. See the RELEASE_NOTES file for details about
these changes.

Slurm's PMI-1 (libpmi.so.0.0.0) and PMI-2 (libpmi2.so.0.0.0) public API libraries do not change
between releases and are meant to be permanently fixed. This means that linking against either of
them will not require you to recompile the application after a Slurm upgrade, except in the unlikely
event that one of them changes. It is unlikely because these libraries must be compatible with any
other PMI-1 and PMI-2 implementations. If there was a change, it would be announced in the
RELEASE_NOTES and would only happen on a major release.

As an example, MPI stacks like OpenMPI and MVAPICH2 link against Slurm's PMI-1 and/or PMI-2 API, but
not against our main public API. This means that at the time of writing this documentation, you
don't need to recompile these stacks after a Slurm upgrade. One known exception is MPICH. When MPICH
is compiled with Slurm support and with the Hydra Process Manager, it will use the Slurm API to
obtain job information. This link means you will need to recompile the MPICH stack after an upgrade.

One easy way to know if an application requires a recompile is to inspect all of its ELF files with
'ldd' and grep for 'slurm'. If you see a versioned 'libslurm.so.x.y.z' reference, then the
application will likely need to be recompiled.

Slurm daemons will support RPCs and state files from the two previous major releases (e.g. a version
23.02.x SlurmDBD will support slurmctld daemons and commands with a version of 23.02.x, 22.05.x or
21.08.x). This means that upgrading at least once each year is recommended. Otherwise, intermediate
upgrades will be required to preserve state information. Changes in the maintenance release number
generally only include bug fixes, but may also include other minor enhancements.

**Be mindful of your configured SlurmdTimeout and SlurmctldTimeout values**. If the Slurm daemons
are down for longer than the specified timeout during an upgrade, nodes may be marked DOWN and their
jobs killed. You can either increase the timeout values during an upgrade or ensure that the slurmd
daemons on compute nodes are not down for longer than SlurmdTimeout. The recommended upgrade order
is as follows:

1.  Shutdown the slurmdbd daemon.
2.  Backup the Slurm database using mysqldump (or similar tool), e.g.
    <span class="commandline">mysqldump --databases slurm_acct_db \> backup.sql</span>. You may also
    want to take this opportunity to verify that the innodb_buffer_pool_size in my.cnf is greater
    than the default. See the recommendation in the [accounting
    page](accounting.md#slurm-accounting-configuration-before-build).
3.  Upgrade the slurmdbd daemon.
4.  Restart the slurmdbd daemon.
    - **NOTE**: The first time slurmdbd is started after an upgrade it will take some time to update
      existing records in the database. If slurmdbd is started with systemd, it may think that
      slurmdbd is not responding and kill the process when it reaches its timeout value, which
      causes problems with the upgrade. We recommend starting slurmdbd by calling the command
      directly rather than using systemd when performing an upgrade.
5.  Increase configured SlurmdTimeout and SlurmctldTimeout values and execute "scontrol reconfig"
    for them to take effect.
6.  Shutdown the slurmctld daemon(s).
7.  Shutdown the slurmd daemons on the compute nodes.
8.  Copy the contents of the configured StateSaveLocation directory (in case of any possible
    failure).
9.  Upgrade the slurmctld and slurmd daemons.
10. Restart the slurmd daemons on the compute nodes.
11. Restart the slurmctld daemon(s).
12. Validate proper operation.
13. Restore configured SlurmdTimeout and SlurmctldTimeout values and execute "scontrol reconfig" for
    them to take effect.
14. Destroy backup copies of database and/or state files.

**NOTE**: It is possible to update the slurmd daemons on a node-by-node basis after the slurmctld
daemon(s) are upgraded, but do make sure their down time is below the SlurmdTimeout value.

**NOTE**: In the beginning of 2021, a version of Slurm was added to the EPEL repository. This
version is not supported or maintained by SchedMD, and is not currently recommend for customer use.
Unfortunately, this inclusion could cause Slurm to be updated to a newer version outside of a
planned maintenance period. In order to prevent Slurm from being updated unintentionally, we
recommend you modify the EPEL Repository configuration to exclude all Slurm packages from automatic
updates.

    exclude=slurm*

## FreeBSD

FreeBSD administrators can install the latest stable Slurm as a binary package using:

    pkg install slurm-wlm

Or, it can be built and installed from source using:

    cd /usr/ports/sysutils/slurm-wlm && make install

The binary package installs a minimal Slurm configuration suitable for typical compute nodes.
Installing from source allows the user to enable options such as mysql and gui tools via a
configuration menu.

Last modified 24 October 2023
