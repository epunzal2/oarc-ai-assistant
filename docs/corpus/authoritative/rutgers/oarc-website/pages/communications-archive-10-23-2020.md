# Amarel Storage Roadmap (Oct 2020)

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/10-23-2020/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2021-09-17T16:32:35+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Amarel Storage Roadmap (Oct 2020)

Rutgers Research Computing Community,

With a variety of storage-related challenges and changes at hand, I'd like to take a moment to provide a status update and some details about our current storage management efforts.

Some background

Hardware added during the past few years has configured Amarel's computing environment with 6 PB of [IBM Spectrum Scale (GPFS)](https://nam02.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwww.ibm.com%2Fsupport%2Fknowledgecenter%2Fen%2FSTXKQY_5.0.0%2Fcom.ibm.spectrum.scale.v5r00.doc%2Fbl1ins_intro.htm&data=04%7C01%7Cklepping%40rutgers.edu%7C54adf0c245264a77dc1e08d87780924c%7Cb92d2b234d35447093ff69aca6632ffe%7C1%7C1%7C637390741393974263%7CUnknown%7CTWFpbGZsb3d8eyJWIjoiMC4wLjAwMDAiLCJQIjoiV2luMzIiLCJBTiI6Ik1haWwiLCJXVCI6Mn0%3D%7C3000&sdata=Hx2pWH2lDZHL%2FgA8zYXLq41VmyHYJSe%2F9E0U8rJY6pU%3D&reserved=0) storage that's divided among 3 key file sets: /home, /projects/, and /scratch. All Amarel users have 100 GB of backed-up storage in their /home directory and 1 TB of space in their /scratch directory to serve as temporary expansion space (not backed-up) for actively running jobs. The standard /home and /scratch allocations are intended to be fixed. Additional storage space is available to Amarel owners (those who invest in our shared infrastructure by purchasing 1 or more compute nodes). Amarel owners purchase TBs of backed-up storage in private /projects directories. See our user guide for details: [https://sites.google.com/view/cluster-user-guide/amarel/owner-guide](https://sites.google.com/view/cluster-user-guide/amarel/owner-guide)

As initially configured, those 6 PB of storage were sufficient for quite a long time, but we now support a much larger user population and we have more detailed information about their current and anticipated storage needs. Our current storage has been fully consumed, but we are quickly adding additional storage where it is most urgently needed. In response to recent equipment provisioning setbacks due to COVID-19-related acquisition delays and workplace/datacenter restrictions, a top priority for us has become rushing to provide ample online storage to support the explosive growth of data-centric computing taking place on the Amarel cluster.

Current state

This week, we are (finally) getting our new Phase IV storage hardware installed. In this round of expansion, we're adding 4 PB of storage. Most of that storage will be used to satisfy existing and anticipated /projects storage purchases.

Managing the very large weekly backups for our /home and /projects file sets has become a significant challenge. We are transitioning to storing our weekly backups off-site using commercial cloud storage services. If that turns out to be a safe and cost-effective approach, we may continue to manage our backups that way.

Next few weeks

As the current storage installations (4 PB) are completed and the newly available space is configured for use, owners waiting for their new /projects storage will have earliest access to that space. There are many tasks and variables that influence the schedule for this storage availability. For example,

- We're waiting for the vendor technicians currently on-site to finish installing the hardware - We must provision the bare metal (OS, boot configuration, network configuration) - We must install and configure the GPFS software - We must upgrade storage nodes to a common version of the GPFS software - We must integrate the newly configured storage into our existing production file sets - All filesystems will have to be moved and rewritten - All of this will be done in a very active production environment

The expected timing for the availability of the new /projects storage is as follows:

Best case = the day after the presidential election (Nov 3) Median case = the day after Thanksgiving Worst case = the first work day after the new year, if we encounter problems with all of the tasks listed above, which would be caused by external factors like a vendor's schedule or performance, etc.

Some of the storage upgrade procedures temporarily use the remaining available space, so we would appreciate users avoiding filling-up their /projects allocations during the next few weeks, if that can be avoided.

Since our user population has grown into the thousands, our /scratch system is undergoing a long overdue restructuring to improve sustainability. Personal /scratch quotas will change to a consistent 1 TB for all users on Nov 17. This transition was scheduled and started before the current /projects storage provisioning delays were realized, but proceeding will help us recover much needed storage space. This transition will also bring our user storage allocations into closer alignment with those of national research computing resources.

Months ahead

Going forward, large storage expansions will be a key part of our annual infrastructure purchase plan: a larger portion of our equipment budget will be dedicated to storage. If you anticipate making a very large /projects storage purchase, let us know as soon as possible so we can integrate your expectations into our storage acquisition planning.

As always, if you have questions or comments, we would very like to hear them.

Galen

Galen Collier, PhD Director, Research Support Office of Advanced Research Computing (OARC)
