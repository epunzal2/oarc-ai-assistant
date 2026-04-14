# NAME

slurmctld - The central management daemon of Slurm.

# SYNOPSIS

**slurmctld** \[*OPTIONS*...\]

# DESCRIPTION

**slurmctld** is the central management daemon of Slurm. It monitors all other Slurm daemons and
resources, accepts work (jobs), and allocates resources to those jobs. Given the critical
functionality of **slurmctld**, there may be a backup server to assume these functions in the event
that the primary server fails.

# OPTIONS

**-c**  
Clear all previous **slurmctld** state from its last checkpoint. With this option, all jobs,
including both running and queued, and all node states, will be deleted. Without this option,
previously running jobs will be preserved along with node *State* of DOWN, DRAINED and DRAINING
nodes and the associated *Reason* field for those nodes. **NOTE**: It is rare you would ever want to
use this in production as all jobs will be killed.

<!-- -->

**-d**  
Run **slurmctld** in the background.

<!-- -->

**-D**  
Run **slurmctld** in the foreground with logging copied to stdout.

<!-- -->

**-f \<file\>**  
Read configuration from the specified file. See **NOTES** below.

<!-- -->

**-h**  
Help; print a brief summary of command options.

<!-- -->

**-i**  
Ignore errors found while reading in state files on startup. Warning: Use of this option will mean
losing the data that wasn't recovered from the state files.

<!-- -->

**-L \<file\>**  
Write log messages to the specified file.

<!-- -->

**-n \<value\>**  
Set the daemon's nice value to the specified value, typically a negative number.

<!-- -->

**-r**  
Recover partial state from last checkpoint: jobs and node DOWN/DRAIN state and reason information
state. No partition state is recovered. This is the default action.

<!-- -->

**-R**  
Recover full state from last checkpoint: jobs, node, partition state, and power save settings.
Without this option, previously running jobs will be preserved along with node *State* of DOWN,
DRAINED and DRAINING nodes and the associated *Reason* field for those nodes. No other node or
partition state will be preserved.

<!-- -->

**-s**  
Change working directory of slurmctld to SlurmctldLogFile path if possible, or to Slurm's
StateSaveLocation otherwise. If both of them fail it will fallback to /var/tmp.

<!-- -->

**-v**  
Verbose operation. Multiple **v**'s can be specified, with each '**v**' beyond the first increasing
verbosity, up to 6 times (i.e. -vvvvvv).

<!-- -->

**-V**  
Print version information and exit.

# ENVIRONMENT VARIABLES

The following environment variables can be used to override settings compiled into slurmctld.

**SLURM_CONF**  
The location of the Slurm configuration file. This is overridden by explicitly naming a
configuration file on the command line.

<!-- -->

**SLURM_DEBUG_FLAGS**  
Specify debug flags for the scheduler to use. See DebugFlags in the **slurm.conf**(5) man page for a
full list of flags. The environment variable takes precedence over the setting in the slurm.conf.

# CORE FILE LOCATION

If slurmctld is started with the **-D** option then the core file will be written to the current
working directory. Otherwise if **SlurmctldLogFile** is a fully qualified path name (starting with a
slash), the core file will be written to the same directory as the log file, provided SlurmUser has
write permission on the directory. Otherwise the core file will be written to the
**StateSaveLocation**, or "/var/tmp/" as a last resort. If none of the above directories have write
permission for SlurmUser, no core file will be produced. The command "scontrol abort" can be used to
abort the slurmctld daemon and generate a core file.

# SIGNALS

**SIGTERM SIGINT**  
**slurmctld** will shutdown cleanly, saving its current state to the state save directory.

<!-- -->

**SIGABRT**  
**slurmctld** will shutdown cleanly, saving its current state, and perform a core dump.

<!-- -->

**SIGHUP**  
Reloads the slurm configuration files, similar to 'scontrol reconfigure'.

<!-- -->

**SIGUSR2**  
Reread the log level from the configs, and then reopen the log file. This should be used when
setting up **logrotate**(8).

<!-- -->

**SIGCHLD SIGUSR1 SIGTSTP SIGXCPU SIGQUIT SIGPIPE SIGALRM**  
These signals are explicitly ignored.

# NOTES

It may be useful to experiment with different **slurmctld** specific configuration parameters using
a distinct configuration file (e.g. timeouts). However, this special configuration file will not be
used by the **slurmd** daemon or the Slurm programs, unless you specifically tell each of them to
use it. If you desire changing communication ports, the location of the temporary file system, or
other parameters used by other Slurm components, change the common configuration file,
**slurm.conf**.

# COPYING

Copyright (C) 2002-2007 The Regents of the University of California. Copyright (C) 2008-2010
Lawrence Livermore National Security. Copyright (C) 2010-2022 SchedMD LLC. Produced at Lawrence
Livermore National Laboratory (cf, DISCLAIMER). CODE-OCEC-09-009. All rights reserved.

This file is part of Slurm, a resource management program. For details, see
\<https://slurm.schedmd.com/\>.

Slurm is free software; you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

Slurm is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
License for more details.

# SEE ALSO

**slurm.conf**(5), **slurmd**(8)
