# Documentation

**NOTE: This documentation is for Slurm version 23.02.7.  
Documentation for older versions of Slurm are distributed with the source, or may be found in the
[archive](archive).**

Also see [Tutorials](tutorials.md) and [Publications and Presentations](publications.md).

## Slurm Users

- [Quick Start User Guide](quickstart.md)
- [Command/option Summary (two pages)](../pdf/pdfs/summary.md)
- [Man Pages](man_index.md)
- [Rosetta Stone of Workload Managers](rosetta.md)
- [Job Array Support](job_array.md)
- [Heterogeneous Job Support](heterogeneous_jobs.md)
- [CPU Management User and Administrator Guide](cpu_management.md)
- [MPI and UPC Users Guide](mpi_guide.md)
- [Support for Multi-core/Multi-threaded Architectures](mc_support.md)
- [Multi-Cluster Operation](multi_cluster.md)
- [Profiling Using HDF5 User Guide](hdf5_profile_user_guide.md)
- [Job Exit Codes](job_exit_code.md)
- [Resource Binding](resource_binding.md)
- Specific Systems
  - [Cray User and Administrator Guide with Native Slurm](cray.md)
  - [Intel Knights Landing (KNL) User and Administrator Guide](intel_knl.md)

## Slurm Administrators

- [Quick Start Administrator Guide](quickstart_admin.md)
- [Accounting](accounting.md)
- [Advanced Resource Reservation Guide](reservations.md)
- [Burst Buffer Guide](burst_buffer.md)
- [Cgroups Guide](cgroups.md)
- ["Configless" Slurm Operation](configless_slurm.md)
- [Configuration Tool (Full version)](configurator.md)
- [Configuration Tool (Simplified version)](configurator.easy.md)
- [Containers](containers.md)
- [CPU Management User and Administrator Guide](cpu_management.md)
- [Dynamic Nodes](dynamic_nodes.md)
- [Elasticsearch Guide](elasticsearch.md)
- [Job Completion Kafka plugin Guide](jobcomp_kafka.md)
- [job_container/tmpfs - Job Specific Temporary File Management](job_container_tmpfs.md)
- [JSON Web Tokens Authentication](jwt.md)
- [Federated Scheduling Guide](federation.md)
- [Job Containment (SSH Session Control) with pam_slurm_adopt](pam_slurm_adopt.md)
- [Large Cluster Administration Guide](big_sys.md)
- [License Management](licenses.md)
- [Multi-Category Security (MCS) Guide](mcs.md)
- [Name Service Caching Through NSS Slurm](nss_slurm.md)
- [Network Configuration Guide](network.md)
- [OpenAPI Plugin Release Notes](openapi_release_notes.md)
- [Power Management Guide (power capping)](power_mgmt.md)
- [Power Saving Guide (power down idle nodes)](power_save.md)
- [Prolog and Epilog Guide](prolog_epilog.md)
- [Slurm REST API](rest.md)
- [Slurm REST API Reference](rest_api.md)
- [Slurm SELinux Context Management](selinux.md)
- [Troubleshooting Guide](troubleshoot.md)
- [User Permissions](user_permissions.md)
- [WCKey Management](wckey.md)
- Workload Prioritization
  - [Multifactor Job Priority](priority_multifactor.md)
  - [Classic Fairshare Algorithm](classic_fair_share.md)
  - [Depth-Oblivious Fair-share Factor](priority_multifactor3.md)
  - [Fair Tree Fairshare Algorithm](fair_tree.md)
- Slurm Scheduling
  - [Scheduling Configuration Guide](sched_config.md)
  - [Consumable Resources Guide](cons_res.md)
  - [Core Specialization](core_spec.md)
  - [Gang Scheduling](gang_scheduling.md)
  - [Generic Resource (GRES) Scheduling](gres.md)
  - [High Throughput Computing Guide](high_throughput.md)
  - [Preemption](preempt.md)
  - [Quality of Service (QOS)](qos.md)
  - [Resource Limits](resource_limits.md)
  - [Resource Reservation Guide](reservations.md)
  - [Sharing Consumable Resources](cons_res_share.md)
  - [Topology](topology.md)
  - [Trackable Resources (TRES)](tres.md)
- Specific Systems
  - [Cray User and Administrator Guide with Native Slurm](cray.md)
- Cloud
  - [Cloud Scheduling Guide](elastic_computing.md)
  - [Slurm on Google Cloud Platform](https://github.com/schedmd/slurm-gcp)
  - [Deploying Slurm with ParallelCluster on Your AWS
    Cluster](https://www.schedmd.com/downloads/extras/Slurm_ParallelCluster_AWS.pdf)
  - [Slurm on Microsoft Azure and CycleCloud](https://github.com/Azure/cyclecloud-slurm)

## Slurm Developers

- [Contributor Agreement](contributor.md)
- [Programmer Guide](programmer_guide.md)
- [Application Programmer Interface (API) Guide](api.md)
- [Adding Files or Plugins to Slurm](add.md)
- Design Information
  - [Generic Resource (GRES) Design Guide](gres_design.md)
  - [Job Launch Design Guide](job_launch.md)
  - [Select Plugin Design Guide](select_design.md)
- [Plugin Programmer Guide](plugins.md)
- Plugin Interface Details
  - [Command Line Filter Plugin Programmer Guide](cli_filter_plugins.md)
  - [Job Submission Plugin Programmer Guide](job_submit_plugins.md)
  - [PrEp Plugin Programmer Guide](prep_plugins.md)
  - [Site Factor (Priority) Plugin Programmer Guide](site_factor.md)

Last modified 5 October 2022
