# Amarel maintenance is complete + important notes (regarding /scratch, /home, and Lmod)

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/6-10-2019/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2020-08-31T19:55:14+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Amarel maintenance is complete + important notes (regarding /scratch, /home, and Lmod)

Galen Collier Monday, June 10, 2019 at 1:03 pm

OARC Research Computing Users,

The Institutional Planning & Operations team has completed their work in the Hill Data Center, so our maintenance outage is now complete. The compute nodes in Piscataway have been returned to service.

The work completed includes: - Modifications to the data center HVAC cooling water loop - Upgraded power monitoring, diagnostics, and fault detection - Maintenance for the UPS and power distribution systems - Replacement of building power switches and feeder cables - Repairs to the building's domestic water supply

Important notes:

(1) **Files residing in /scratch for 90 days without being accessed (i.e., used or read) will be automatically purged.** Everyone's /scratch directory is considered temporary storage intended only for actively running jobs. Nothing in /scratch is backed-up. We would like to remove limits on /scratch storage to enable researchers to import, use, or generate very large data sets, but doing so will require adherence to this policy of purging of old files. Information about managing or moving data is available in our user guide, here: [https://sites.google.com/view/cluster-user-guide/amarel#h.t618y9lhk7u9](https://sites.google.com/view/cluster-user-guide/amarel#h.t618y9lhk7u9)

(2) Reminder: the quota or limit on storage in /home is 100 GB. If you have more than 100 GB of data in your /home directory, you may be prevented from writing additional data until you remove items stored there.

(3) Lmod (the 'module' command) has been updated to version 8.1.6. Saved modules may need to be updated/refreshed.

Please let us know if you have questions or need help.

Galen
