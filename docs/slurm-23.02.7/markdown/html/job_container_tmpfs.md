# job_container/tmpfs

## Overview

job_container/tmpfs is an optional plugin that provides job-specific, private temporary file system
space.

When enabled on the cluster, each job will have its own /tmp and /dev/shm directory, separate from
every other job as well as the system. These are mapped in the job as "/tmp" and "/dev/shm". The
directories used to mount in a private name space can be configured with the **Dirs=** option in
job_container.conf

## Installation

This plugin is built and installed as part of the default build, no extra installation steps are
required.

## Setup

Slurm must be configured to load the job container plugin by adding
**JobContainerType=job_container/tmpfs** and **PrologFlags=contain** in slurm.conf. Additional
configuration must be done in the "job_container.conf" file, which should be placed in the same
directory as the slurm.conf.

Job containers can be configured for all nodes, or for a subset of nodes. As an example, if all
nodes will be configured the same way, you would put the following in your job_container.conf:

    AutoBasePath=true
    BasePath=/var/nvme/storage

A full description of the parameters available in the job_container.conf file can be found
[here](job_container.conf.md).

## Initial Testing

An easy way to verify that the container is working is to run a job and ensure that the /tmp
directory is empty (since it normally has some other files) and that "." is owned by the user that
submitted the job.

    tim@slurm-ctld:~$ srun ls -al /tmp
    total 8
    drwx------  2 tim    root 4096 Feb 10 17:14 .
    drwxr-xr-x 21 root   root 4096 Nov 15 08:46 ..

## Spank

This plugin interfaces with the SPANK api, and automatically joins the job's container in the
following functions:

- spank_task_init_privileged()
- spank_task_init()

In addition to the job itself, The TaskProlog will also be executed inside the container.

Last modified 26 July 2022
