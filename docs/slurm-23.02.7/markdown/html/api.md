# <span id="top">Slurm APIs</span>

### Overview

All of the Slurm commands utilize a collection of Application Programming Interfaces (APIs). User
and system applications can directly use these APIs as desired to achieve tighter integration with
Slurm. For example, Slurm data structures and error codes can be directly examined rather than
executing Slurm commands and parsing their output. This document describes Slurm APIs. You should
see the man pages for individual APIs to get more details.

### Get Overall Slurm Information

- **slurm_api_version** — Get Slurm API version number.
- **slurm_load_ctl_conf** — Load system-wide configuration specifications. Free with
  *slurm_free_ctl_conf* to avoid memory leak.
- **slurm_print_ctl_conf** — Print system-wide configuration specifications.
- **slurm_free_ctl_conf** — Free storage allocated by *slurm_load_ctl_conf*.

### Get Job Information

- **slurm_pid2jobid** — For a given process ID on a node get the corresponding Slurm job ID.
- **slurm_get_end_time** — For a given Slurm job ID get the expected termination time.
- **slurm_load_jobs** — Load job information. Free with *slurm_free_job_info_msg* to avoid memory
  leak.
- **slurm_print_job_info_msg** — Print information about all jobs.
- **slurm_print_job_info** — Print information about a specific job.
- **slurm_free_job_info_msg** — Free storage allocated by *slurm_load_jobs*.

### Get Job Step Information

- **slurm_get_job_steps** — Load job step information. Free with
  *slurm_free_job_step_info_response_msg* to avoid memory leak.
- **slurm_print_job_step_info_msg** — Print information about all job steps.
- **slurm_print_job_step_info** — Print information about a specific job step.
- **slurm_free_job_step_info_response_msg** — Free storage allocated by *slurm_get_job_steps*.

### Get Node Information

- **slurm_load_node** — Load node information. Free with *slurm_free_node_info* to avoid memory
  leak.
- **slurm_print_node_info_msg** — Print information about all nodes.
- **slurm_print_node_table** — Print information about a specific node.
- **slurm_free_node_info** — Free storage allocated by *slurm_load_node*.

### Get Partition Information

- **slurm_load_partitions** — Load partition (queue) information. Free with
  *slurm_free_partition_info* to avoid memory leak.
- **slurm_print_partition_info_msg** — Print information about all partitions.
- **slurm_print_partition_info** — Print information about a specific partition.
- **slurm_free_partition_info** — Free storage allocated by *slurm_load_partitions*.

### Error Handling

- **slurm_get_errno** — Return the error code set by the last Slurm API function executed.
- **slurm_perror** — Print Slurm error information to standard output.
- **slurm_strerror** — Return a string describing a specific Slurm error code.

### Resource Allocation

- **slurm_init_job_desc_msg** — Initialize the data structure used in resource allocation requests.
  You can then just set the fields of particular interest and let the others use default values.
- **slurm_job_will_run** — Determine if a job would be immediately initiated if submitted now.
- **slurm_allocate_resources** — Allocate resources for a job. Response message must be freed using
  *slurm_free_resource_allocation_response_msg* to avoid a memory leak.
- **slurm_free_resource_allocation_response_msg** — Frees memory allocated by
  *slurm_allocate_resources*.
- **slurm_allocate_resources_and_run** — Allocate resources for a job and spawn a job step. Response
  message must be freed using *slurm_free_resource_allocation_and_run_response_msg* to avoid a
  memory leak.
- **slurm_free_resource_allocation_and_run_response_msg** — Frees memory allocated by
  *slurm_allocate_resources_and_run*.
- **slurm_submit_batch_job** — Submit a script for later execution. Response message must be freed
  using *slurm_free_submit_response_response_msg* to avoid a memory leak.
- **slurm_free_submit_response_response_msg** — Frees memory allocated by *slurm_submit_batch_job*.
- **slurm_confirm_allocation** — Test if a resource allocation has already been made for a given job
  id. Response message must be freed using *slurm_free_resource_allocation_response_msg* to avoid a
  memory leak. This can be used to confirm that an allocation is still active or for error recovery.

### Job Step Creation

Slurm job steps involve numerous interactions with the *slurmd* daemon. The job step creation is
only the first step in the process. We don't advise direct user creation of job steps, but include
the information here for completeness.

- **slurm_job_step_create** — Initiate a job step. Allocated memory must be freed by
  *slurm_free_job_step_create_response_msg* to avoid a memory leak.
- **slurm_free_job_step_create_response_msg** — Free memory allocated by *slurm_job_step_create*.
- **slurm_step_ctx_create** — Create job step context. Destroy using *slurm_step_ctx_destroy*.
- **slurm_step_ctx_destroy** — Destroy a job step context created by *slurm_step_ctx_create*.
- **slurm_step_ctx_get** — Get values from job step context.
- **slurm_step_ctx_set** — Set values in job step context.
- **slurm_jobinfo_ctx_get** — Get values from a *jobinfo* field as returned by *slurm_step_ctx_get*.
- **slurm_spawn** — Spawn tasks and establish communications.
- **slurm_spawn_kill** — Signal spawned tasks.

### Job and Job Step Signaling and Cancelling

- **slurm_kill_job** — Signal or cancel a job.
- **slurm_kill_job_step** — Signal or cancel a job step.

### Job Completion

- **slurm_complete_job** — Note completion of a job. Releases resource allocation for the job.
- **slurm_complete_job_step** — Note completion of a job step.

### Administrative Functions

Most of these functions can only be executed by user *root*.

- **slurm_reconfigure** — Update slurm daemons based upon current *slurm.conf* configuration file.
  Use this after updating the configuration file to ensure that it takes effect.
- **slurm_shutdown** — Terminate slurm daemons.
- **slurm_update_job** — Update state information associated with a given job.
- **slurm_update_node** — Update state information associated with a given node. **NOTE**: Most of a
  node's characteristics can not be modified.
- **slurm_init_part_desc_msg** — Initialize a partition update descriptor. Used this to initialize
  the data structure used in *slurm_update_partition*.
- **slurm_update_partition** — Update state information associated with a given partition.
- **slurm_delete_partition** — Destroy a partition.

### Slurm Host List Support

Slurm uses a condensed format to express node names. For example *linux\[1-3,6\]* represents
*linux1*, *linux2*, *linux3*, and *linux6*. These functions permit you to translate the Slurm
expression into a list of individual node names.

- **slurm_hostlist_create** — Translate a Slurm node name expression into a record used for parsing.
  Use *slurm_hostlist_destroy* to free the allocated storage.
- **slurm_hostlist_shift** — Get the next node name.
- **slurm_hostlist_destroy** — Release storage allocated by *slurm_hostlist_create*.

Last modified 23 November 2019
