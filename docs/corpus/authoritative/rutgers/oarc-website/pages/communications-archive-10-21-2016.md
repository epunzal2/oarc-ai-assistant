# 10/21/2016: HPCC and Hill power upgrades - TODAY - Friday, 10/21/16 at 5:00 pm

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/10-21-2016/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2021-09-16T20:42:19+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## 10/21/2016: HPCC and Hill power upgrades - TODAY - Friday, 10/21/16 at 5:00 pm

Ryan Novosielski Friday, October 21, 2016 at 10:19 am

The Office of Information Technology (OIT) will be performing upgrades in the Hill Center Data Center, which will require electricity to be shut down on Saturday, October 22nd, from 6:30a to 11:00p. This is required to accommodate greater research computing capacity and to improve reliability. As a result of these upgrades, per the previous announcement sent out by OIT, OARC equipment housed in Hill Center will not be available this weekend. We will begin a shutdown for the weekend at 5:00p, -TODAY- Friday, October 21st.

The following systems will not be available:

* HPCC (both legacy fen and new environment fen2) * NIH-funded perceval cluster (all compute nodes and infrastructure)

...and related storage systems. A maintenance reservation has been put into place on all systems that will delay any job that will not complete by 5:00p -TODAY- until after the maintenance has completed.

Additionally, during this maintenance window, we will be migrating the majority of the legacy HPCC compute nodes to our new HPCC environment (accessible now via login node fen2.hpc.rutgers.edu), which is running more modern system and application software, uses the Lmod environment modules software to make it easy to configure your user environment for OARC-installed software packages, and contains 20 new compute nodes with 24-core Intel Haswell-generation processors, among other benefits. You will find additional information in our user guide:

[https://sites.google.com/view/cluster-user-guide/home](https://sites.google.com/view/cluster-user-guide)

As mentioned above, this new environment is already available, so we encourage you to login with your existing credentials at fen2.hpc.rutgers.edu and take a look. A small number of nodes will remain in the existing/legacy HPCC environment to allow current user jobs to finish and to allow users who are not able to migrate immediately to continue working. OARC staff will be available to assist with the new environment if needed; please contact [help@hpc.rutgers.edu](mailto:help@hpc.rutgers.edu) if you have having any difficulty.

*NOTE: you will need to copy any data you will require from your legacy HPCC /scratch directory to the /scratch directory on the new environment. Please only copy the data that you will need, and keep in mind that this storage location is only for temporary storage during the life of a project and is not backed up. /home directories are shared between the legacy and new environments so you will not need to copy these files. Contact us at [help@hpc.rutgers.edu](mailto:help@hpc.rutgers.edu) if you need any assistance.

We will begin to restore all equipment to service as soon as possible after the power upgrades and system changes, and will send out updates as information becomes available. We expect have full service restored by 12:00 noon on Monday, October 24th. We apologize for any inconvenience this may cause, but these improvements are necessary in order to support the expansion of our research resources and to improve our computing resources. If you have any questions or need any assistance, please respond to this e-mail.

=The OARC Sysadmin Team
