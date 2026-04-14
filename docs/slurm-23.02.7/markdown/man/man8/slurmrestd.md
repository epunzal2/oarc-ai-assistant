# NAME

slurmrestd - Interface to Slurm via REST API.

# SYNOPSIS

**slurmrestd** \[*OPTIONS*...\] \<*\[host\]:port*\|*unix:/path/to/socket*\>...

# DESCRIPTION

**slurmrestd** is REST API interface for Slurm. It can be used in two modes:

**Inetd Mode**: slurmrestd will read and write to STDIO. If STDIN is a socket file descriptor, then
slurmrestd will detect this and use relevant functionality. If a controlling TTY is detected,
interactive mode will automatically activate to provide additional logging information. This mode is
designed to work with piped input, inetd, xinetd or systemd socket activation.

**Listen Mode**: slurmrestd will open a listening socket on each requested *host*:*port* pair or
UNIX socket.

# OPTIONS

**\[host\]:port**  
Hostname and port to listen against. *host* may be an IPv4/IPv6 IP or a resolvable hostname.
Hostnames are only looked up at startup and do not change for the life of the process. *host* is
optional; if not provided, slurmrestd will listen on all network interfaces.

<!-- -->

**unix:/path/to/socket**  
Listen on local UNIX socket. Must have permission to create socket in filesystem.

<!-- -->

**-a \<authentication plugins\>**  
Comma-delimited list of authentication plugins to load. Default behavior is to load all REST
authentication plugins found at load time.

**list**  
Display a list of the possible plugins to load.

**rest_auth/local**  
Allows authentication via UNIX sockets when **auth/munge** is active.  
**NOTE**: slurmrestd and client processes must run under the same UID or the client requests will be
rejected.

**rest_auth/jwt**  
Allows authentication via TCP and UNIX sockets when **AuthAltTypes=auth/jwt** is active. User must
specify the following HTTP cookies with each request:

**X-SLURM-USER-NAME**:\<user name\>  

**X-SLURM-USER-TOKEN**:\<JSON Web Token\>  
**NOTE**: Tokens are usually generated via calling "**scontrol token**".

**-f \<file\>**  
Read Slurm configuration from the specified file. See **NOTES** below.

**-g \<group id\>**  
Change group id (and drop supplemental groups) before processing client request. This should be a
unique group with no write access or special permissions. Do not set this to the group belonging to
to SlurmUser or root or the daemon won't start with the default settings.

**-h**  
Help; print a brief summary of command options.

**--max-connections \<count\>**  
Set the maximum number of connections to process at any one time. This is independent of the number
of connections that can connect to slurmrestd at any one time. The kernel allows any number of
connections to be pending for processing at any one time when SYN cookies are active.

**Caution**:  
Each connection could cause one RPC to the controller daemons, leading to potential overloading of
the controller. Each connection can also hold memory for the duration of the life of the connection.
Having too many connections processing at once could use considerably more memory. Process limits
(**ulimit**(3)) may require adjustment when this value is increased.

Default: 124  

**-s \<OpenAPI plugins to load\>**  
Comma-delimited list of OpenAPI plugins. Set to "list" to dump a list of the possible plugins to
load. Defaults: all builtin supported OpenAPI plugins.

**-t \<THREAD COUNT\>**  
Specify number of threads to use to process client connections. Ignored in inetd mode. Default: 20

**-u \<user id\>**  
Change user id before processing client request. This should be a unique group with no write access
or special permissions. Do not set this user to SlurmUser or root or the daemon won't start with the
default settings.

**-v**  
Verbose operation. Multiple **v**'s can be specified, with each '**v**' beyond the first increasing
verbosity, up to 6 times (i.e. -vvvvvv). Higher verbosity levels will have significant performance
impact.

**-V**  
Print version information and exit.

# ENVIRONMENT VARIABLES

The following environment variables can be used to override settings compiled into slurmctld.

**SLURM_CONF**  
The location of the Slurm configuration file.

<!-- -->

**SLURM_DEBUG_FLAGS**  
Specify debug flags for slurmrestd to use. See DebugFlags in the **slurm.conf**(5) man page for a
full list of flags. The environment variable takes precedence over the setting in the slurm.conf.

<!-- -->

**SLURM_JWT**  
This variable must be set to use JWT token authentication.

<!-- -->

**SLURMRESTD_AUTH_TYPES**  
Set allowed authentication types. See **-a**

<!-- -->

**SLURMRESTD_DEBUG**  
Set debug level explicitly. Valid values are 1-10. See **-v**

<!-- -->

**SLURMRESTD_LISTEN**  
Comma-delimited list of host:port pairs or unix sockets to listen on.

<!-- -->

**SLURMRESTD_MAX_CONNECTIONS**  
Set the maximum number of connections to process at any one time. See **--max-connections**

<!-- -->

**SLURMRESTD_OPENAPI_PLUGINS**  
Comma-delimited list of OpenAPI plugins to load. See **-s**

<!-- -->

**SLURMRESTD_SECURITY**  
Control slurmrestd security functionality using the following comma-delimited values:

> **become_user**  
> Allows **slurmrestd** to be run as root in order to become the requesting user for all requests.
> When combined with **rest_auth/local, when a user** connects via a named UNIX socket,
> **slurmrestd** will setuid()/setgid() into that user/group and then complete all requests as the
> given user. This mode is only intended for inet mode as the user change is permanent for the life
> of the process. This mode is incompatible with **rest_auth/jwt** and it is suggested to start
> **slurmrestd** with "-a **rest_auth/local**" arguments.
>
> <!-- -->
>
> **disable_unshare_files**  
> Disables unsharing file descriptors with parent process.
>
> <!-- -->
>
> **disable_unshare_sysv**  
> Disables unsharing the SYSV namespace.
>
> <!-- -->
>
> **disable_user_check**  
> Disables check that slurmrestd is not running as root or SlurmUser, or with the root or
> SlurmUser's primary group.

# SIGNALS

**SIGINT**  
**slurmrestd** will shutdown cleanly.

<!-- -->

**SIGPIPE**  
This signal is explicitly ignored.

# NOTES

**SPANK** and **clifilter** plugins are not supported in **slurmrestd** due to their lack of thread
safety. Active **SPANK** plugins and **JobSubmitPlugins** in **slurmctld** are independent of
slurmrestd and can be used to enforce site policy on job submissions.

# EXAMPLES

Start **slurmrestd** with a UNIX socket in listen mode:

    $ export SLURMRESTD=/var/spool/slurm/restd/rest
    $ slurmrestd -s dbv0.0.39,v0.0.39 unix:$SLURMRESTD

Verify connectivity with the controller with a ping, with **slurmrestd** running in listen mode:

    $ curl --unix-socket "${SLURMRESTD}" 'http://localhost:8080/slurm/v0.0.39/ping'
    {
      "meta": {
        "plugin": {
          "type": "openapiv0.0.39",
          "name": "Slurm OpenAPI v0.0.39",
          "data_parser": "v0.0.39"
        },
        "client": {
          "source": "tmpslurmrestdrestd->fd:8"
        },
        "Slurm": {
          "version": {
            "major": 23,
            "micro": 3,
            "minor": 2
          },
          "release": "23.02.3"
        }
      },
      "errors": [
      ],
      "warnings": [
      ],
      "pings": [
        {
          "hostname": "kitt",
          "pinged": "UP",
          "latency": 606,
          "mode": "primary"
        }
      ]
    }

Query the status of a node with **slurmrestd** running in INETD mode:

    $ echo -e "GET http://localhost:8080/slurm/v0.0.39/node/node01 HTTP/1.1\r\n" | slurmrestd
    slurmrestd: operations_router: [fd:0->/dev/pts/1] GET /slurm/v0.0.39/node/node01
    slurmrestd: rest_auth/local: slurm_rest_auth_p_authenticate: [fd:0->/dev/pts/1] accepted connection from user: user1[1001]
    HTTP/1.1 200 OK
    Content-Length: 3777
    Content-Type: application/json

    {
      "meta": {
        "plugin": {
          "type": "openapiv0.0.39",
          "name": "Slurm OpenAPI v0.0.39",
          "data_parser": "v0.0.39"
        },
        "client": {
          "source": "fd:0->devpts1"
        },
        "Slurm": {
          "version": {
            "major": 23,
            "micro": 3,
            "minor": 2
          },
          "release": "23.02.3"
        }
      },
      "errors": [
      ],
      "warnings": [
      ],
      "nodes": [
        {
          "architecture": "x86_64",
          "burstbuffer_network_address": "",
          "boards": 1,
          "boot_time": 1688652669,
          "cluster_name": "",
          "cores": 12,
          "specialized_cores": 0,
          "cpu_binding": 0,
          "cpu_load": {
            "set": true,
            "infinite": false,
            "number": 17
          },
          "free_mem": {
            "set": true,
            "infinite": false,
            "number": 187
          },
          "cpus": 24,
          "effective_cpus": 24,
          "specialized_cpus": "",
          "energy": {
            "average_watts": 0,
            "base_consumed_energy": 0,
            "consumed_energy": 0,
            "current_watts": 0,
            "previous_consumed_energy": 0,
            "last_collected": 0
          },
          "external_sensors": {
            "consumed_energy": {
              "set": false,
              "infinite": false,
              "number": 0
            },
            "temperature": {
              "set": false,
              "infinite": false,
              "number": 0
            },
            "energy_update_time": 0,
            "current_watts": 0
          },
          "extra": "",
          "power": {
            "maximum_watts": {
              "set": false,
              "infinite": false,
              "number": 0
            },
            "current_watts": 0,
            "total_energy": 0,
            "new_maximum_watts": 0,
            "peak_watts": 0,
            "lowest_watts": 0,
            "new_job_time": 0,
            "state": 0,
            "time_start_day": 0
          },
          "features": [
            "rhel7",
            "rhel8",
            "rhel76",
            "rhel79",
            "rhel85",
            "rack1"
          ],
          "active_features": [
            "rhel7",
            "rack1"
          ],
          "gres": "cpu:24,gpu:tesla:4(S:0),test:8",
          "gres_drained": "NA",
          "gres_used": "cpu:0,gpu:tesla:0(IDX:NA),tesla:0,test:0",
          "last_busy": 1688671269,
          "mcs_label": "",
          "specialized_memory": 0,
          "name": "node01",
          "next_state_after_reboot": [
            "INVALID",
            "PERFCTRS",
            "RESERVED",
            "UNDRAIN",
            "CLOUD",
            "RESUME",
            "DRAIN",
            "COMPLETING",
            "NOT_RESPONDING",
            "POWERED_DOWN",
            "FAIL",
            "POWERING_UP",
            "MAINTENANCE",
            "REBOOT_REQUESTED",
            "REBOOT_CANCELED",
            "POWERING_DOWN",
            "DYNAMIC_FUTURE",
            "REBOOT_ISSUED",
            "PLANNED",
            "INVALID_REG",
            "POWER_DOWN",
            "POWER_UP",
            "POWER_DRAIN",
            "DYNAMIC_NORM"
          ],
          "address": "kitt",
          "hostname": "kitt",
          "state": [
            "IDLE"
          ],
          "operating_system": "Linux 5.15.0-76-generic #83-Ubuntu SMP Thu Jun 15 19:16:32 UTC 2023",
          "owner": "",
          "partitions": [
            "debug"
          ],
          "port": 18001,
          "real_memory": 15678,
          "comment": "",
          "reason": "",
          "reason_changed_at": 0,
          "reason_set_by_user": "",
          "resume_after": {
            "set": true,
            "infinite": false,
            "number": 0
          },
          "reservation": "",
          "alloc_memory": 0,
          "alloc_cpus": 0,
          "alloc_idle_cpus": 24,
          "tres_used": "",
          "tres_weighted": 0.0,
          "slurmd_start_time": 1688671266,
          "sockets": 1,
          "threads": 2,
          "temporary_disk": 0,
          "weight": 1,
          "tres": "cpu=24,mem=15678M,billing=39,gresgpu=4,gresgpu:tesla=4,grestest=8",
          "version": "23.02.3"
        }
      ]
    }

Submit a job to **slurmrestd** with it running in listen mode:

    $ cat example_job.json
    {"script": "#!/bin/bash\nsleep 30",
      "job": {
        "name": "ExampleJob",
        "account": "sub1",
        "hold": false,
        "environment": {
          "PATH": "/bin"
        },
        "tasks": 12,
        "memory_per_cpu": 100,
        "time_limit": 240
      }
    }

    $ curl -H "Content-Type: application/json" -d @example_job.json --unix-socket "${SLURMRESTD}" 'http://localhost:8080/slurm/v0.0.39/job/submit'
    {
      "meta": {
        "plugin": {
          "type": "openapiv0.0.39",
          "name": "Slurm OpenAPI v0.0.39",
          "data_parser": "v0.0.39"
        },
        "client": {
          "source": "tmpslurmrestdrestd->fd:8"
        },
        "Slurm": {
          "version": {
            "major": 23,
            "micro": 3,
            "minor": 2
          },
          "release": "23.02.3"
        }
      },
      "errors": [
      ],
      "warnings": [
        {
          "description": "Expected OpenAPI type=array (Slurm type=list) but got OpenAPI type=object (Slurm type=dictionary)",
          "source": "#jobenvironment"
        },
        {
          "description": "Expected OpenAPI type=object (Slurm type=dictionary) but got OpenAPI type=integer (Slurm type=int 64bits)",
          "source": "#jobtime_limit"
        },
        {
          "description": "Expected OpenAPI type=object (Slurm type=dictionary) but got OpenAPI type=integer (Slurm type=int 64bits)",
          "source": "#jobmemory_per_cpu"
        }
      ],
      "result": {
        "job_id": 8990,
        "step_id": "batch",
        "error_code": 0,
        "error": "No error",
        "job_submit_user_msg": ""
      },
      "job_id": 8990,
      "step_id": "batch",
      "job_submit_user_msg": ""
    }

# COPYING

Copyright (C) 2019-2022 SchedMD LLC.

This file is part of Slurm, a resource management program. For details, see
\<https://slurm.schedmd.com/\>.

Slurm is free software; you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation; either version 2 of the License, or (at
your option) any later version.

Slurm is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
License for more details.

# SEE ALSO

**slurm.conf**(5), **slurmctld**(8), **slurmdbd**(8)
