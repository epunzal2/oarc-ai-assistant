# UPDATE: HPCC and Hill Center upgrades complete: HPCC available (+ migration of HPCC to new environment)

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/10-23-2016/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2021-09-17T13:27:38+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## UPDATE: HPCC and Hill Center upgrades complete: HPCC available (+ migration of HPCC to new environment)

Ryan Novosielski Sunday, October 23, 2016 at 1:21 am

The Office of Information Technology (OIT) upgrades in the Hill Center Data Center, which required electricity to be shut down on Saturday, October 22nd, have been completed as of about 3:15p. The power shutdown was required to make infrastructure changes that will accommodate greater research computing capacity and to improve reliability.

As of about 1:00a Sunday morning, HPCC is available for use, and jobs that were held before the maintenance period are now running. However, there will be brief periods where HPCC will not be reachable on Monday morning, 10/24, between 9:00a and 10:00a as we make changes to increase network performance and reliability. All running jobs will continue to run, but connections to the HPCC login nodes may be interrupted.

Additionally, during this maintenance window, we migrated the majority of the legacy HPCC compute nodes to our new HPCC environment (accessible now via login node fen2.hpc.rutgers.edu), which is running more modern system and application software, uses the Lmod environment modules software to make it easy to configure your user environment for OARC-installed software packages, and contains 20 new compute nodes with 24-core Intel Haswell-generation processors, among other benefits. You will find additional information in our user guide:

[https://sites.google.com/view/cluster-user-guide](https://sites.google.com/view/cluster-user-guide)

A small number of nodes will remain in the existing/legacy HPCC environment to allow current user jobs to finish and to allow users who are not able to migrate immediately to continue working. OARC staff will be available to assist with the new environment if needed; please contact [help@hpc.rutgers.edu](mailto:help@hpc.rutgers.edu) if you have having any difficulty.

*NOTE: you will need to copy any data you will require from your legacy HPCC /scratch directory to the /scratch directory on the new environment. Please only copy the data that you will need, and keep in mind that this storage location is only for temporary storage during the life of a project and is not backed up. /home directories are shared between the legacy and new environments so you will not need to copy these files. Contact us at [help@hpc.rutgers.edu](mailto:help@hpc.rutgers.edu) if you need any assistance.

We apologize for any inconvenience these changes may cause, but these improvements are necessary in order to support the expansion of our research resources and to improve our computing resources. If you have any questions or need any assistance, please respond to this e-mail.

=The OARC Sysadmin Team
