# Camden Power Outage Complete

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/01-08-2021a/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2021-01-13T22:05:20+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Camden Power Outage Complete

Friday, January 8, 2021 at 7:56 am

Morning,

The scheduled power outage in Camden is complete.

To my knowledge, all Amarel related services should be available. *Any error or access problem encountered is unexpected and should be reported.*

Return to service was a little behind schedule due to problems encountered by PSE&G. The necessary repair work was completed yesterday afternoon around 4pm; however, PSE&G's main electrical switch into the power grid did not come online. We were notified that power was fully restored shortly before 7pm. Equipment was brought online and available by 8pm.

Remaining issues are related to the legacy Golova cluster. The following should be restored this morning. These do NOT affect most users.

CCIB Workstations (Camden labs+owners)

* /lustre/scratch fileset

CIIPRO Website

* VM hosted on server ccib-bsb-170 which did not reboot

We appreciate your patience and understanding during this outage. We were all in the same boat. Copy of last notification of outage provided below.

Monday, January 4, 2021 at 2:04 pm

**REMINDER!**

Electrical work is scheduled by PSE&G for this coming Thursday 1/7/21 which will require power be removed from many buildings on the Camden campus. One affected building is the Business & Science Building (BSB). This building houses the Data Center which supplies compute resources for the Amarel HPC cluster as well as home+data directories for many CCIB Lab workstations using Golova legacy resources.

The outage is scheduled from 1/7/21 @06:00 until around 1/7/21 @18:00. To plan for this outage, services and systems will be taken offline starting Wednesday 1/6/21 at 16:00 (4pm). Some services will return to service the evening of 1/7/21; however, some will not become available until Friday morning 1/8/21. An email will be sent out as services return.

The Amarel cluster in Piscataway will remain available. If your data does not reside in Camden, your jobs and access should continue normally during this outage.

Following is a list of some affected services.

1) Amarel resources **physically in Camden** * amarelc login server * halc* nodes * gpuc* nodes * /projects filesets in Camden

ccib f_grigorie_1 f_hfuchs_1 f_jn322 f_km1243_1 f_rucdr jdb252_1

* job partitions using Camden nodes p_ccib_1 cmain p_grigorie_1 p_jn322 p_jdb252_1 p_rucdr

* /scratch only the Camden-specific scratch normally accessible via amarelc, halc* or gpuc*.

2) Legacy Golova/kestrel data+services * home+data directories /g1 /g2 /g3 /g5

* scratch directory /lustre/scratch

* ciipro website

3) Home directories for CCIB Linux workstations * will contact each affected owner separately

Following is an excerpt of the original announcement to the Camden Campus sent on 12/23/2020.

*To the Campus Community:*

*On Thursday, Jan. 7, the following buildings will be without power due to electrical repair work and will be closed during 6 a.m. to 6 p.m.:*

*Artis Building* *Business and Science Building* *Camden Apartments* *Camden Tower* *Campus Center* *Mail Room Building* *Science Building* *401 Cooper*

*For more information, please contact Mike Fitzgerald in University Facilities at [mike.fitzgerald@rutgers.edu](mailto:mike.fitzgerald@rutgers.edu).*

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Tom Skipper HPC & System Administrator Office of Advanced Research Computing (OARC)

Monday, December 21, 2020 at 11:57 am

Hi Amarel Users,

PSE&G have chosen Thursday 1/7/2021 for the work in Camden that will result in a day long power outage. This will affect ALL compute resources in the Camden Data Center (BSB-114). Therefore, all amarel nodes in Camden will be shutdown.

Anyone using amarelc or halc nodes AND /scratch and /project on that campus will be affected.

Sorry for the inconvenience that may cause an interruption to your work.

- Vlad Kholodovych, PhD Senior Scientist vlad.khol@rutgers.edu

Office of Advanced Research Computing (OARC) Rutgers, The State University of New Jersey
