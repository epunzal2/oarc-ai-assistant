# Merge of HPCC into Amarel

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/10-23-2017/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2020-08-31T18:18:12+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Merge of HPCC into Amarel

Les Michelson Monday, October 23, 2017 at 10:42 pm

Dear HPCC Owner/User:

In April of this year we communicated to you regarding the merger of HPCC into the Amarel environment. This merger will take place during the Amarel maintenance window scheduled for October 25-27 (Wednesday thru Friday of this week). As such HPCC will adopt the Amarel scheduling policy.

The Amarel model and attendant scheduling policy will provide HPCC owners much faster turn-around time for most jobs and access to a far larger number of nodes. There are, however, several salient differences between the way jobs are scheduled on HPCC now and how they will be handled post-merger.

Unit now, HPCC jobs have been scheduled using a fairshare algorithm in which owner job priority is proportional to resource purchased. When HPCC is fully utilized, or busy to an extent in which insufficient resources are available to run new jobs, job submissions are queued. All jobs will eventually run to completion without interruption.

In the Amarel model, jobs requesting resources that do not exceed those purchased, e.g., nodes/cores and memory, are guaranteed to run immediately and will run to completion. This is an important distinction. Jobs requesting physical compute resources in excess of ownership will run as "open access" in a partition called "main" and will be subject to preemption if the resources allocated are needed to satisfy an owner job submission. Jobs submitted to the "main partition" can be optionally flagged to be re-queued if preempted. Each owner has an assigned queue providing access to owned resources.

Amarel users with a requirement for non-preemptible access for an urgent or very large job, can request a reservation for non-preemptible access. Reservations requests will be reviewed internally by OARC staff or referred to the OARC Faculty Advisory Committee for review as appropriate. Such requests will be subject to the availability of sufficient non-owner resources

HPCC members will become owners in the Amarel environment with the same resources they currently own. Ownership will be maintained for no less than two years, predicated on purchased node installation date and useful service life, currently estimated to be four years. At the end of the ownership period, HPCC owners can purchase new nodes at a significantly subsidized cost or become general, open access users, subject to job preemption with optional re-queue. OARC, of course, hopes that HPCC owners will continue to invest in Amarel as their requirements and funding permit.

Access to storage for HPCC owners remains unchanged under the Amarel umbrella and will remain available through at least the service life of the nodes owned and can be renewed at the then current pricing for storage. Currently, parallel, clustered storage w/backup is priced at $150/TB.

HPCC owners are asked to contact us via [help@hpc.rutgers.edu](mailto:help@hpc.rutgers.edu) beginning Monday October 30th, for further information on partition names and additional options for managing storage. Some HPCC owners may not have been migrated to the Amarel environment by October 30, so it is import that the help line be contacted prior to first access.

More details are available at: [https://na01.safelinks.protection.outlook.com/?url=https%3A%2F%2Foarc.rutgers.edu%2Famarel%2F&data=02%7C01%7Cklepping%40rutgers.edu%7C5a6750d62aff4447a63e08d51a88db2e%7Cb92d2b234d35447093ff69aca6632ffe%7C1%7C0%7C636444097448615654&sdata=%2FBYL9Gu1sNKV%2ByTF51Ldq9gh95F%2FeNcnJXtN2AOBGhU%3D&reserved=0](https://na01.safelinks.protection.outlook.com/?url=https%3A%2F%2Foarc.rutgers.edu%2Famarel%2F&data=02%7C01%7Cklepping%40rutgers.edu%7C5a6750d62aff4447a63e08d51a88db2e%7Cb92d2b234d35447093ff69aca6632ffe%7C1%7C0%7C636444097448615654&sdata=%2FBYL9Gu1sNKV%2ByTF51Ldq9gh95F%2FeNcnJXtN2AOBGhU%3D&reserved=0) https:/oarc.rutgers.edu/services/condo-model/ or by emailing [help@hpc.rutgers.edu](mailto:help@hpc.rutgers.edu).

Welcome to Amarel. We are ready to help you optimize the transition to Amarel.

Regards,

Leslie P. Michelson, Ph.D. Director for Technical and Scientific Support Office of Advanced Research Computing
