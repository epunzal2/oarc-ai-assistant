# NAME

ext_sensors.conf - Slurm configuration file for the external sensors plugin

# DESCRIPTION

**ext_sensors.conf** is an ASCII file which defines parameters used by Slurm's external sensors
plugins. The file will always be located in the same directory as the **slurm.conf**.

Parameter names are case insensitive. Any text following a "#" in the configuration file is treated
as a comment through the end of that line. The size of each line in the file is limited to 1024
characters. Changes to the configuration file take effect upon restart of Slurm daemons, daemon
receipt of the SIGHUP signal, or execution of the command "scontrol reconfigure" unless otherwise
noted.

The following ext_sensors.conf parameters are defined to control data collection by the ext_sensors
plugins. All of these parameters are optional. If a parameter is omitted, data collection of the
omitted type is disabled.

**JobData**=**energy**  
Specify the data types to be collected by the plugin for jobs/steps.

<!-- -->

**NodeData**=**\[energy\|temp\]\[,temp\|energy\]**  
Specify the data types to be collected by the plugin for nodes.

<!-- -->

**SwitchData**=**energy**  
Specify the data types to be collected by the plugin for switches.

<!-- -->

**ColdDoorData**=**temp**  
Specify the data types to be collected by the plugin for cold doors.

<!-- -->

**MinWatt**=**\<number\>**  
Minimum recorded power consumption, in watts.

<!-- -->

**MaxWatt**=**\<number\>**  
Maximum recorded power consumption, in watts.

<!-- -->

**MinTemp**=**\<number\>**  
Minimum recorded temperature, in Celsius.

<!-- -->

**MaxTemp**=**\<number\>**  
Maximum recorded temperature, in Celsius.

<!-- -->

**EnergyRRA**=**\<name\>**  
Energy RRA name.

<!-- -->

**TempRRA**=**\<name\>**  
Temperature RRA name.

<!-- -->

**EnergyPathRRD**=**\<path\>**  
Pathname of energy RRD file.

<!-- -->

**TempPathRRD**=**\<patch\>**  
Pathname of temperature RRD file.

# EXAMPLE

    ###
    # Slurm external sensors plugin configuration file
    ###
    JobData=energy
    NodeData=energy,temp
    SwitchData=energy
    ColdDoorData=temp
    #

# COPYING

Copyright (C) 2013 Bull Copyright (C) 2013-2022 SchedMD LLC. Produced at Bull (cf, DISCLAIMER).

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
