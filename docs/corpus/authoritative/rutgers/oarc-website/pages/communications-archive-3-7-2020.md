# ELF is now back in service

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/3-7-2020/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2020-08-31T20:48:44+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## ELF is now back in service

Galen Collier Saturday, March 7, 2020 at 2:05 am

ELF Users,

Maintenance for the ELF cluster is nearly complete and the system has been returned to service.

Account holders can access ELF at elf.oarc.rutgers.edu or elf.rutgers.edu (ssh [NetID]@elf.oarc.rutgers.edu).

Work completed includes:

- All hosted VMs, compute nodes, and login nodes have been upgraded to CentOS 7.7 with GPFS 4.2.3.19, SLURM 18.08.8. - The firmware for all managed and unmanaged InfiniBand switches has been upgraded. - Node Health Check has been setup to help with monitoring of the compute nodes. - Added DNS names such that elf.oarc.rutgers.edu and elf[1-2].oarc.rutgers.edu and elf.rutgers.edu are the names used. - Same list of packages is now installed on each node of each type (improved consistency among the compute nodes). - Switched from nslcd (deprecated) to System Security Services Daemon (SSSD) for authentication services. - The Lmod module system has been upgraded to 8.1.6.

For information about Caliburn, please see our Caliburn System Status page: [https://oarc.rutgers.edu/caliburn-status](https://oarc.rutgers.edu/caliburn-status) We are currently working quickly to have Caliburn ready for production use on March 13.

Please let us know if you have questions or if you encounter any problems: help@oarc.rutgers.edu

Galen

Galen Collier, PhD Director, Research Support Office of Advanced Research Computing (OARC)
