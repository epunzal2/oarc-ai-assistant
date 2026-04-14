# NAME

knl.conf - Slurm configuration file for Intel Knights Landing processor.

# DESCRIPTION

This ASCII file which describes configuration information for Intel Knights Landing processors and
its name may depend upon the NodeFeatures plugin configured in Slurm. For example, on Cray systems
NodeFeatures should be configured to "knl_cray" and its configuration file will be read from
"knl_cray.conf". The file will always be located in the same directory as the **slurm.conf**. This
file is optional.

Parameter names are case insensitive. Any text following a "#" in the configuration file is treated
as a comment through the end of that line. Changes to the configuration file take effect upon
restart of Slurm daemons, daemon receipt of the SIGHUP signal, or execution of the command "scontrol
reconfigure" unless otherwise noted.

The overall configuration parameters available include:

**AllowMCDRAM**  
Specify the MCDRAM modes which jobs are allowed to use. This may be a subset of MCDRAM modes
supported by the node. If not specified, all MCDRAM modes supported by the node are available for
use. The comma separated list of allowed MCDRAM modes may include any of the modes listed below.

> **cache**  
> All of MCDRAM to be used as cache.
>
> <!-- -->
>
> **equal**  
> MCDRAM to be used partly as cache and partly combined with primary memory.
>
> <!-- -->
>
> **flat**  
> MCDRAM to be combined with primary memory into a "flat" memory space.

**AllowNUMA**  
Specify the NUMA modes which jobs are allowed to use. This may be a subset of NUMA modes supported
by the node. If not specified, all NUMA modes supported by the node are available for use. The comma
separated list of allowed NUMA modes may include any of the modes listed below. Note that Slurm can
only support homogeneous nodes (e.g. the same number of cores per NUMA node). KNL scn4 and quad
modes are not homogeneous, but each NUMA mode will have either 16 or 18 cores. This will result in
Slurm using the lower core count and finding a total of 256 threads rather than 272 threads and
setting the node to a DOWN state. Therefore it is recommended that snc4 and quad mode not be allowed
at this time.

> **a2a**  
> All to all
>
> <!-- -->
>
> **snc2**  
> Sub-NUMA cluster 2
>
> <!-- -->
>
> **snc4**  
> Sub-NUMA cluster 4
>
> <!-- -->
>
> **hemi**  
> Hemisphere
>
> <!-- -->
>
> **quad**  
> Quadrant

**AllowUserBoot**  
A comma-delimited list of users allowed to modify a node's MCDRAM or NUMA state. If not specified
then any user can change a node's state and reboot it.

<!-- -->

**BootTime**  
Estimated time to reboot a node in seconds. Used as a basis for optimizing scheduling decisions. The
default value is 300 seconds (5 minutes) for the "knl_generic" plugin and 2700 seconds (45 minutes)
for the "knl_cray" plugin.

<!-- -->

**CapmcPath**  
Fully qualified path to the **capmc** program. The default value is
"/opt/cray/capmc/default/bin/capmc". This parameter is used only by the "knl_cray" plugin.

<!-- -->

**CapmcPollFreq**  
Time interval between when the **capmc** program should poll for node state changes, in seconds. The
default value is 45 seconds. This parameter is used only by the "knl_cray" plugin.

<!-- -->

**CapmcRetries**  
Number of times to retry failed operations of the **capmc** program. Default value is 4.

<!-- -->

**CapmcTimeout**  
Time limit for the **capmc** program to return status information milliseconds. The default value is
60000 milliseconds and the minimum value is 1000 milliseconds. This parameter is used by the
"knl_cray" plugin, plus the capmc_suspend and capmc_resume programs used for suspending and resuming
nodes.

<!-- -->

**CnselectPath**  
Fully qualified path to the **cnselect** program. The default value is
"/opt/cray/sdb/default/bin/cnselect". This parameter is used only by the "knl_cray" plugin.

<!-- -->

**DefaultMCDRAM**  
Specify the default MCDRAM modes for job's which do not specify a value. This is only used when a
node is booted and the job which has been allocated the node does not specify a desired MCDRAM mode.
The value can include one of the possible values identified with the **AllowMCDRAM** configuration
parameter above. The default value is "cache".

<!-- -->

**DefaultNUMA**  
Specify the default NUMA modes for job's which do not specify a value. This is only used when a node
is booted and the job which has been allocated the node does not specify a desired NUMA mode. The
value can include one of the possible values identified with the **AllowNUMA** configuration
parameter above. The default value is "a2a".

<!-- -->

**Force**  
If set to a non-zero value then load the node_features/generic plugin even on non-KNL nodes. Used
primarily for testing purposes.

<!-- -->

**LogFile**  
Fully qualified path to a log file. The default value is SlurmctldLogFile from the slurm.conf
configuration file. This is option is used only by the campc_suspend and campc_resume programs
(which power down and reboot nodes in the appropriate configuration).

<!-- -->

**McPath**  
Fully qualified path to memory controller device file directory. Children of this directory with
names of the form "mc#/csrow#/ue_count" (i.e. the count of unrecoverable memory errors) will be
monitored for non-zero values. If such errors are detected, the node will be set to a DOWN state and
the slurmd daemon will shutdown. The default value is "/sys/devices/system/edac/mc". See also
**UmeCheckInterval**.

<!-- -->

**NumaCpuBind**  
Contains pairs of NUMA modes and the CpuBind mode to set a node to for that mode. Any compute node
found with or set to the specified NUMA mode will have that node's CpuBind field set to the
configured value. The NUMA node will be followed by an equal sign the desired CpuBind mode for that
NUMA mode. Multiple NUMA mode and CpuBind modes should be in a semicolon separated list. By default
changes to a node's NUMA mode will not effect that node's CpuBind mode. See the example below.

<!-- -->

**SyscfgPath**  
Fully qualified path to Intel's **syscfg** program, which identifies current KNL configuration by
viewing BIOS settings. If not defined, the current BIOS setting will not be available. The default
value is "/usr/bin/syscfg". This parameter is used only by the "knl_generic" plugin.

<!-- -->

**SyscfgTimeout**  
Timeout for **syscfg** program in milliseconds. Default value is 1000 milliseconds. For Dell KNL
systems, experience has shown that a higher value of 10000 milliseconds is more appropriate.

<!-- -->

**SystemType**  
Used to distinguish the flavor of knl we are dealing with. Possible options are "Dell" and "Intel".
The default value is "Intel". This parameter is used only by the "knl_generic" plugin.

<!-- -->

**UmeCheckInterval**  
Interval, in microseconds, between checks for Uncorrectable Memory Errors (UME). If such errors are
detected, the node will be set to a DOWN state and the slurmd daemon will shutdown. The default
value is 0 (disabled). See also **McPath**.

<!-- -->

**ValidateMode**  
If set to 1 then validate, but do not modify the node's configured MCDRAM and NUMA modes from the
slurm.conf file. If the actual modes do not match configured values the node will be set to a DOWN
state. Every KNL nodes MCDRAM and NUMA states must both be listed in the slurm.conf file. This
parameter is used only by the "knl_cray" plugin.

# EXAMPLE

    ###################################################################
    # knl_cray.conf
    # Slurm configuration file for Intel Knights Landing on Cray system
    ###################################################################
    CapmcPath=/opt/cray/capmc/default/bin/capmc
    CapmcTimeout=6000
    DefaultMCDRAM=flat
    DefaultNUMA=a2a
    NumaCpuBind=a2a=core;snc2=thread;snc4=thread
    LogFile=/var/tmp/slurm_node_feature.log
    SyscfgPath=/usr/sbin/syscfg

# COPYING

Copyright (C) 2015-2022 SchedMD LLC.

This file is part of Slurm, a resource management program. For details, see
\<https://slurm.schedmd.com/\>.

Slurm is free software; you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

Slurm is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
License for more details.

# SEE ALSO

**slurm.conf**(5)
