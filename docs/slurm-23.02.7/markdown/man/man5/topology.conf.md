# NAME

topology.conf - Slurm configuration file for defining the network topology

# PREREQUISITES

Topology.conf can only represent a hierarchical network. All nodes in the network must be connected
to at least one switch. The network must be fully connected to use a RoutePlugin. Jobs can only span
nodes connected by the same switch fabric, even if there are available idle nodes.

# DESCRIPTION

**topology.conf** is an ASCII file which describes the cluster's network topology for optimized job
resource allocation. The file will always be located in the same directory as the **slurm.conf**.

Parameter names are case insensitive. Any text following a "#" in the configuration file is treated
as a comment through the end of that line. Changes to the configuration file take effect upon
restart of Slurm daemons, daemon receipt of the SIGHUP signal, or execution of the command "scontrol
reconfigure" unless otherwise noted.

The network topology configuration one line defining a switch name and its children, either node
names or switch names. Slurm's hostlist expression parser is used, so the node and switch names need
not be consecutive (e.g. "Nodes=tux\[0-3,12,18-20\]" and "Switches=s\[0-2,4-8,12\]" will parse
fine). An optional link speed may also be specified.

The **topology.conf** file for an Infiniband switch can be automatically generated using the
**slurmibtopology** tool found here:
\<https://github.com/OleHolmNielsen/Slurm_tools/tree/master/slurmibtopology\>.

The overall configuration parameters available include:

**SwitchName**  
The name of a switch. This name is internal to Slurm and arbitrary. Each switch should have a unique
name. This field must be specified.

<!-- -->

**Switches**  
Child switches of the named switch. Either this option or the **Nodes** option must be specified.

<!-- -->

**Nodes**  
Child Nodes of the named leaf switch. Either this option or the **Switches** option must be
specified.

<!-- -->

**LinkSpeed**  
An optional value specifying the performance of this communication link. The units used are
arbitrary and this information is currently not used. It may be used in the future to optimize
resource allocations.

# EXAMPLE

    ##################################################################
    # Slurm's network topology configuration file for use with the
    # topology/tree plugin
    ##################################################################
    SwitchName=s0 Nodes=dev[0-5]
    SwitchName=s1 Nodes=dev[6-11]
    SwitchName=s2 Nodes=dev[12-17]
    SwitchName=s3 Switches=s[0-2]

# COPYING

Copyright (C) 2009 Lawrence Livermore National Security. Produced at Lawrence Livermore National
Laboratory (cf, DISCLAIMER).  
Copyright (C) 2010-2022 SchedMD LLC.

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
