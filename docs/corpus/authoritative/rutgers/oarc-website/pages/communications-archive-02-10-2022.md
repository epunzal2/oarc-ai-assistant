# Removal of Amarel Phase 1 Nodes and Storage

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/02-10-2022/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2022-02-16T20:39:18+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Removal of Amarel Phase 1 Nodes and Storage

Amarel Phase 1 Owners,

As announced previously, Amarel Phase 1 compute nodes and storage expired in July 2021.

We postponed removal of the Phase 1 hardware, in part, to compensate for delays we've faced in acquiring and provisioning Phase 5A. Now that the Phase 5A equipment is in-production, we need to remove the Phase 1 equipment as soon as possible.

We are planning to remove Phase 1 nodes and storage from owner allocations during next week's maintenance window (Feb 15-16).

How will these changes be implemented?

(Case 1) Owners of later-phase nodes (Phase 2-5) will see Phase 1 nodes removed from their job partitions. Storage quotas for the /projects filesystem will be reduced from current values, accounting for the loss of Phase 1 storage. Note that actively owning any number of Amarel compute nodes (i.e., being an Amarel owner) qualifies one for 1 TB of /projects storage, so there is no situation where an owner of compute nodes does not have any /projects storage.

If your /projects storage utilization is over your quota after a quota adjustment, that renders your /projects storage space read-only (unwriteable) until you can move or delete enough data to get back under quota.

(Case 2) Those who own only Phase 1 nodes and storage will simply lose access to those resources. Please note that loss of /projects storage will result in loss of data stored there. If this case applies to you, I urge you to begin moving your data to an appropriate alternative storage resource immediately. Box.rutgers.edu is a good option, but the data transfer process may be slow.

Of course, let me know what questions or concerns you have.

Galen Collier, PhD Director, Research Support Office of Advanced Research Computing (OARC)
