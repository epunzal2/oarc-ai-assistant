# Re: Intermittent SLURM Controller Issue Impacting Some Jobs

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/12-30-2021b/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2022-01-04T21:58:00+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Re: Intermittent SLURM Controller Issue Impacting Some Jobs

12-30-2021 at 8:20 pm

Following-up:

We found the problem, it's a user job configuration issue, and we're working with users to eliminate that issue.

Please proceed with using the cluster as you normally would.

There appears to be a bug in the Slurm code that's triggered when job arrays are used in conjunction with the -batch option. That option is ignored with job arrays (-constraint is used instead), but the Slurm controller is still spending effort resolving those superfulous -batch options. When this is done with a very large number of jobs submitted simultaneously, the Slurm controller was overwhelmed and had to restart.

Please let me know if you have questions or if you need further details.

Galen

12-30-2021 at 10:24 am

Amarel Users,

We're actively troubleshooting an intermittent issue with the Amarel cluster's SLURM controller (that's the core job scheduling and management system). At first, it wasn't clear if this issue was impacting jobs, but now there is evidence that some users' jobs have been impacted.

The SLURM controller exited (stopped) and was restarted at the following times (ET):

Wednesday at 06:26,
17:15,
17:42,
22:53 and Thursday at
00:47 and
08:07.

Based on what we've seen, it's possible that new or existing jobs could be interrupted by this issue if the controller momentarily stops again at a time when those jobs need to communicate with the controller. However, I recommend proceeding with jobs normally, or restarting interrupted jobs, since the majority of jobs are not encountering issues.

Of course, we'll provide updates as we get more information.

Please let me know if you have questions.

Galen Collier, PhD

Director, Research Support
