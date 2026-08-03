# Federation with Google Cloud

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/resources/federationgooglecloud/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2020-08-28T19:59:16+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Federation with Google Cloud

## **Federation with Google Cloud**

OARC has formed a partnership with Google Cloud and SchedMD, the main developer of an open-source job scheduler called SLURM, to develop a federated hybrid storage environment, where some Amarel user data is stored locally and some is stored in the cloud.

The benefits of this arrangement will be many:

- Allowing many storage resources (including cloud services) to work together seamlessly
- Allowing OARC to offer a one-stop shop for users, regardless of whether they need local or cloud
 storage
- Allowing users to access Amarel compute nodes and storage (either as an owner or a general-access
 user) from any campus (or other location) at any time.

The initial proof of concept saw OARC take a number of steps:

- Setting up a federated environment between Rutgers and Google Cloud
- Setting the Google Cloud instance up in a similar manner as local resources, including how SLURM
 schedules jobs
- Establishing a connection through Internet2 between both environments
- Enabling users to submit jobs directly from Rutgers HPC to Google Cloud using a SLURM submit
 script
- Elasticity/bursting capability within the ERN is now being tested, and, looking forward, OARC will
 extend capabilities to Jetstream and the Open Science Grid (OSG).

[Contact OARC for more information](https://oarc.rutgers.edu/contact-oarc/)
