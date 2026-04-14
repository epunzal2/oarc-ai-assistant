# NAME

Slurm - Slurm Workload Manager overview.

# DESCRIPTION

The Slurm Workload Manager is an open source, fault-tolerant, and highly scalable cluster management
and job scheduling system for large and small Linux clusters. Slurm requires no kernel modifications
for its operation and is relatively self-contained. As a cluster resource manager, Slurm has three
key functions. First, it allocates exclusive and/or non-exclusive access to resources (compute
nodes) to users for some duration of time so they can perform work. Second, it provides a framework
for starting, executing, and monitoring work (normally a parallel job) on the set of allocated
nodes. Finally, it arbitrates contention for resources by managing a queue of pending work. Optional
plugins can be used for accounting, advanced reservation, gang scheduling (time sharing for parallel
jobs), backfill scheduling, resource limits by user or bank account, and sophisticated multifactor
job prioritization algorithms.

Slurm has a centralized manager, **slurmctld**, to monitor resources and work. There may also be a
backup manager to assume those responsibilities in the event of failure. Each compute server (node)
has a **slurmd** daemon, which can be compared to a remote shell: it waits for work, executes that
work, returns status, and waits for more work. An optional **slurmdbd** (Slurm DataBase Daemon) can
be used for accounting purposes and to maintain resource limit information.

Basic user tools include **srun** to initiate jobs, **scancel** to terminate queued or running jobs,
**sinfo** to report system status, and **squeue** to report the status of jobs. There is also an
administrative tool **scontrol** available to monitor and/or modify configuration and state
information. APIs are available for all functions.

Slurm configuration is maintained in the **slurm.conf** file.

Man pages are available for all Slurm commands, daemons, APIs, plus the **slurm.conf** file.
Extensive documentation is also available on the internet at **\<https://slurm.schedmd.com/\>**.

# COPYING

Copyright (C) 2005-2007 The Regents of the University of California. Produced at Lawrence Livermore
National Laboratory (cf, DISCLAIMER).  
Copyright (C) 2008-2009 Lawrence Livermore National Security.  
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

**sacct**(1), **sacctmgr**(1), **salloc**(1), **sattach**(1), **sbatch**(1), **sbcast**(1),
**scancel**(1), **scontrol**(1), **sinfo**(1), **squeue**(1), **sreport**(1), **srun**(1),
**sshare**(1), **sstat**(1), **strigger**(1), **sview**(1), **slurm.conf**(5), **slurmdbd.conf**(5),
**slurmctld**(8), **slurmd**(8), **slurmdbd**(8), **slurmstepd**(8), **spank**(8)
