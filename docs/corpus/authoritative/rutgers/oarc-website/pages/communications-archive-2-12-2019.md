# Amarel & Perceval /home quota adjustments

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/2-12-2019/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2021-09-17T13:35:32+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Amarel & Perceval /home quota adjustments

Galen Collier Tuesday, February 12, 2019

OARC Research Computing Users,

The storage quota for all Amarel and Perceval /home directories has been temporarily set to 200 GB. During our next maintenance outage (when no jobs will be running), the original 100 GB quota will be restored.

When our filesystems underwent maintenance recently, the standard 100 GB quota in-place for all user directories in /home was disabled. This change was not evident upon completion of the maintenance work and it enabled a large number of users to push their /home storage beyond the standard quota. Simply enforcing the standard quota would immediately put that very large number of users over quota and would have impacted a large number of actively running jobs. We certainly never want to see productive work interrupted. A compromise to help maintain the health of our storage system (i.e., performance and snapshot capability) would be to temporarily implement a larger-than-normal quota which would have minimal impact on actively running jobs. Some analytical work showed that a 200 GB quota would be about as close to the original quota as we could get, for now. So, that quota has been implemented.

A date for reverting back to the standard 100 GB quota has not yet been set. Keeping Amarel and Perceval running without interruption is a top priority, so that minor quota change will be postponed until it becomes necessary.

Reminder: there are detailed instructions for transferring files to/from Amarel and Perceval in our user documentation: [https://sites.google.com/view/cluster-user-guide#h.3jyxmx35y8y2](https://sites.google.com/view/cluster-user-guide#h.3jyxmx35y8y2)

Please let us know if you have questions or concerns.

Galen
