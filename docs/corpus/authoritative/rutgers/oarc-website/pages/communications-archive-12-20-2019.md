# Amarel system-wide maintenance JAN 6 - 10

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/12-20-2019/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2020-08-31T20:17:18+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Amarel system-wide maintenance JAN 6 - 10

Galen Collier Friday, December 20, 2019 at 8:14 am

Hi Folks,

Amarel, Perceval, and Didact will be offline for maintenance January 6-10.

All Amarel resources, including those in Camden and Newark, will be offline.

Items to be addressed during the outage include:

- Lenovo Scalable Infrastructure firmware updates (to match that of the storage systems) - Lenovo Distributed Storage Solution for IBM Spectrum Scale (DSS-G) and Lenovo GPFS Storage Server (GSS) firmware updates - Rewriting of all filesystems with the GPFS 5.0.x format to enable variable sub-block sizing - Add GPFS updates to all compute node images - Implement Spanning Tree Protocol (STP) across Amarel's internal network - Make a range of network interface configuration changes for our non-storage infrastructure - Patching OS images and various service systems - Moving enclosures (i.e., racks, power, cooling, connectivity) to enable a future storage expansion

Please note:

(1) Submitted jobs with a run time that overlaps this maintenance window will be held in a "pending" state and will be resumed when the maintenance is complete. So, for the next couple of weeks, it might be best to set run times that enable your jobs to end before Jan 6. (2) The automated purging of files in /scratch that have not been accessed for 90 days will remain in effect through this maintenance period.

Let me know if you have questions or need help.

Galen
