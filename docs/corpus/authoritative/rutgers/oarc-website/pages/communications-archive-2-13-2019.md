# Changes to Perceval partitions

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/2-13-2019/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2020-08-31T19:42:59+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Changes to Perceval partitions

Galen Collier Wednesday, February 13, 2019 at 2:15 pm

Perceval users,

Since some recently experienced the undesirable effect of jobs being preempted, we are making some adjustments to our partitions. As a legitimate (NIH-funded) Perceval user, your job will not be preempted on Perceval if that job is submitted to one of the privileged Perceval partitions. Jobs may be preemptable if they are submitted to general priority partitions.

Please let us know if you encounter problems and we will be happy to revisit and adjust our settings as needed.

**Privileged partitions, only available for Perceval users:**

1. "**perceval**" includes only Perceval compute nodes and is only available for Perceval users; not preemptable 2. "**gpu_p**" includes only Perceval cuda (gpu) nodes and is only available for Perceval users; not preemptable 3. "**mem_p**" includes only Perceval largemem node and is only available for Perceval users; not preemptable

**General partitions, available for federated jobs from different clusters (Amarel)**

4. "**main**" includes all nodes on Perceval and includes federated "main" partitions from other clusters, preemptable by jobs submitted to any of Perceval privileged partitions. 5. "**gpu**" includes Perceval cuda nodes and federated Amarel "gpu" nodes and requires to have a legitimate gpu job request; is preemptable by "**gpu_p**"; it will preempt jobs submitted to "**main**" 6. "**mem**" includes Perceval largemem node and federated Amarel "mem" nodes and requires to have a legit large memory job request; is preemptable by "**mem_p**"; it will preempt jobs submitted to "**main**"
