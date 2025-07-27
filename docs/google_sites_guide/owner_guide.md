
Cluster User Guide	
AmarelCaliburn
Amarel Owner Guide
Overview
Acceptable Use Policies
Access to Owned Resources
Data Storage
Software License Management
Connecting Lab Instruments or Local Storage
Hardware End-of-Life Policy
Overview
Access to the Amarel cluster's compute resources and general research computing support are free for all Rutgers students, staff, and faculty. A lot of productive work can be accomplished using Amarel as a general-access user, but the job queues for general-access users are limited by the number of jobs, duration of jobs, and wait time for some resources. In addition, storage space and data sharing/collaboration capabilities are limited for general-access users. Scaling-up your research computing workflows can be a challenge at the general-access level.

To enable scaling-up, there is an option to buy-into the system and become an owner (i.e., purchase compute nodes and storage) to enable an enhanced level of access and productivity. If your research workflows require

dedicated or long-duration access to compute resources without waiting in a job queue,

regular access to large-scale or specialized compute resources beyond the scope of those provided via the general-access job queues,

large amounts of backed-up storage hosted within the Amarel system,

access to compute and storage resources for a few external, non-Rutgers collaborators,

then ownership should be considered.

Amarel ownership offers dedicated access to purchased resources, no waiting in a job queue, and much higher limits on the number and configuration of jobs. In addition, there is the option to buy private backed-up storage at very low cost plus many other benefits. Ownership begins with the purchase of at least 1 compute node.

The standard (most basic) model compute node OARC offers has most recently (spring 2021) been a Xeon-based 52-core, 192 GB RAM model sold at $7,200 for 4 years of service, but large-memory and GPU-equipped variants of that standard model are also available. These purchases are considered equipment purchases, so there is no associated F&A overhead. See https://oarc.rutgers.edu/resources/amarel/#ownership for details.

OARC typically offers an annual buy-in window near the end of each fiscal year after we've collected and compared optimized pricing and configuration options from multiple vendors. Letting us know as early as possible about your intent to purchase compute nodes and storage is the best way to ensure that we will have enough of the right type of equipment available for you. If you are interested in becoming an Amarel owner, please reach-out to OARC's Business Services Team at business@oarc.rutgers.edu

Acceptable Use Policies
All Amarel users, including owners, are required to review OARC's acceptable use policies: https://rutgers.app.box.com/v/oarc-systems-mgmt-aup

By becoming an owner or account holders for any of OARC’s systems, you are implying agreement to the policies presented there.

Access to Owned Resources
Amarel owners access their purchased compute resources through a dedicated, private job partition (job queue within our SLURM job scheduling system). An Amarel owner may designate any current Amarel users as a member of their group and everyone in that owner's group has access to the group's private job partition and private /projects storage.

Owners and their Rutgers-based group members retain access to the full range of general-access compute resources (e.g., the main, gpu, mem, and nonpre job partitions) in addition to access to their private, high-priority owner job partition.

Data Storage
Amarel's /projects file set is intended to be the primary data storage option for active work on Amarel. The performance characteristics of that file set are comparable to those of the /scratch file set, but the /projects directories are backed-up using weekly snapshots.

Any data stored in an owner’s /projects space belongs to that owner, regardless of the permissions configuration. If data stored in an owner’s /projects space is not owned by that owner or somehow becomes inaccessible to the owner of that /projects space, OARC’s infrastructure support team can adjust that ownership to enable the owner to access it.

There is an automated data purge process that operates within the /scratch filesystem if any user remains over their /scratch storage quota for too long. It's important to note that purging of that kind only occurs in the /scratch filesystem because that storage space is owned by OARC and we have to ensure enough space for all users. There has never been purging data of any kind in the /projects filesystem because that space is privately owned by researchers. So, no automated purging of data takes place in the /projects filesystem.

Software License Management
For commercial or otherwise licensed software packages, Amarel offers an internal license server system that can host a variety of common cluster-aware licensing schemes.

If you wish to install licensed software on Amarel as a site license for all users or exclusively for yourself or your research group, you must let us know so our infrastructure team can complete a feasibility review. Our SLURM scheduler is not fully license-aware: the SLURM system can be configured to hold a job if a required software license is not yet available and then launch the job when the required software license becomes available, but there are some licensing schemes or license use configurations (like having a login node consume one license seat) that do not enable SLURM with an accurate count of available licenses.

For example, licenses that use the FlexLM system typically work without issues. Node-locked licensing (which is generally not appropriate for remote cluster environments) presents problems because nodes that comprise a job partition may be swapped with matching hardware if a node must be offline for maintenance.

Software that requires a license management scheme that is not compatible with Amarel's configuration cannot be used on Amarel.

Connecting Lab Instruments or Local Storage
The most common approach for integrating lab instrumentation or compute/storage resources is through a local workstation or server where user accounts on that local system can be used to connect to the Amarel cluster for data movement across the campus network. 

Using the SSHFS utility (a FUSE-based userspace client) is one approach. SSHFS can be installed on your local system which enables the creation of a local mount point (i.e., a folder on your laptop or lab workstation/server) that maps to a directory on Amarel. That enables a user to manage files and directories on Amarel as though they are part of that local system. The performance is usually about as fast as an NFS mount and it can depend on the network performance of the campus network near your lab.

Hardware End-of-Life Policy
When the term of ownership of a compute node comes to an end, that node joins the pool of general-access resources and becomes, from that point,  property of the University and is subject to repurposing or surplus operations. The desire for researchers to adopt end-of-life (post warranty, post ownership) hardware is well-understood, but that equipment management model is strongly discouraged because it works against the University's intention to achieve cost savings and protect research productivity by centralizing management and operation of dedicated compute resources.

The ownership of Amarel nodes is heavily subsidized by the University and the University provides many infrastructure components that owners may not realize are not included with a compute node (e.g., racks, server blade chassis, power distribution and cabling, network interface devices, network cabling, switching infrastructure, OS software, and in some cases, hard drives and RAM/NVM memory modules). So, a retired compute node outside the Amarel environment comprises little more than a motherboard with CPUs and a partial chassis and will require significant investment in components to enable normal operation.


The administration of Amarel compute nodes includes managing the OS software, keeping that software updated with security patches, managing warranty-based parts replacement, security and operational safety, and providing appropriate power and cooling in an environment designed for that purpose. These can be time-consuming tasks that effectively take away from a focus on productive research or scholarship, so having University staff not formally designated for that role taking responsibility for compute systems administration is strongly discouraged by OIT and OFR leadership.

