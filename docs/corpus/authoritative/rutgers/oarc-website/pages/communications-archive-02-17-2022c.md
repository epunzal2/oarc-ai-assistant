# RESOLVED: Amarel Slurm Controller failure - February 17, 2022

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/02-17-2022c/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2022-02-17T20:00:48+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## RESOLVED: Amarel Slurm Controller failure - February 17, 2022

Amarel Cluster users,

The earlier reported issue with the slurm controller failure is resolved now. You may continue to use Amarel cluster as usual.

As mentioned before, we noticed that not all jobs reported with sacct command as RUNNING at the time of the first announcement ran to the full completion. Please check outputs from your recently submitted jobs. As a precaution we would recommend to re-submit these jobs again.

We apologize for inconvenience and for the delay that affects your research.

Message sent on: Thu Feb 17 14:47:39 EST 2022

Amarel Cluster users,

We continue to experience the slurm controller failure issues. Our tech team successfully identified the cause of the problem and now working on patching it.

Unfortunately though, we noticed that not all jobs reported with sacct command as RUNNING at the time of the first announcement ran to the full completion. Please check outputs from your recently submitted jobs. As a precaution we would recommend to re-submit these jobs again when the normal operation of the cluster resumes.

We apologize for inconvenience and for the delay that affects your research.

Message sent on: Thu Feb 17 12:07:02 EST 2022

Amarel Cluster users,

This morning, February 17, 2022, we experience an unexpected failure of slurm controller that prevents new jobs to be submitted to the cluster. Already submitted and running jobs are not affected.

You can check the status of your currently running jobs by using the following command: sacct -u $USER

Our tech team is aware of the problem and investigating the cause. We are working to resolve the problem as soon as possible. We will update you when the issue is resolved. We apologize for inconvenience that it may cause.

Message sent on: Thu Feb 17 09:11:46 EST 2022
