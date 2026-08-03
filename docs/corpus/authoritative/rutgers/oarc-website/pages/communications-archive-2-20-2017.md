# Adjustment to Job Scheduling Policy on Perceval

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/2-20-2017/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2020-08-28T20:47:46+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Adjustment to Job Scheduling Policy on Perceval

Les Michelson Monday, February 20, 2017 at 2:57 pm

Dear Perceval user,

We are truly delighted to tell you that the first full year of production on the NIH-funded Perceval cluster has exceeded expectation in the amount of work that has been successfully completed by investigators across the University. In many ways, Perceval has been one of the transformative elements driving the significant progress underway at Rutgers in developing state-of-the-art computational environments for the research community.

As many of you know, Perceval is a high-demand resource, often running at 100% utilization. This a very good thing considering the enormous cost of facilities of this type. At the same time, we are cognizant of the diversity in job size, job number, frequency of submission, or, simply stated, the numerous ways labs use shared, advanced computing to support their particular research needs. A single job scheduler policy, however complex, cannot optimally satisfy all requirements all of the time or, for that matter, predict future patterns of job submission. Consequently, problems regarding the timeliness of job execution have been reported to us, and we are actively taking that feedback into account.

In an effort to provide a better experience for investigators who use Perceval on a less than regular basis or have significant job requirements with lengthy intervening intervals, OARC has introduced a change to scheduler policy which limits any one SLURM (the job scheduler) group to a maximum of 40% of all available standard node cores. A SLURM group is typically the members of a PI/lab. Jobs submitted in excess of this limit will be queued and prevented from running until the resources used by that SLURM group allow a new job to become eligible for dispatch without exceeding the system resource limit. Jobs, once queued by this mechanism, will age and compete with others according to SLURM fairshare policy. We will observe the impact of this change on the accessibility and utilization of Perceval.

It should be remembered that Perceval is a batch machine and that jobs, once dispatched, are allowed to run to completion (no pre-emption). As a result, a job will not run immediately upon submission if currently idled resources cannot support the requested allocation. We encourage users to submit jobs on a regular basis whenever possible. Investigators who will need a significant resource at a pre-determined future time, should contact us with as much lead time as possible to discuss a guaranteed reservation. We also intend to bring the general question of scheduler policy to the attention of the OARC Faculty Advisory Committee at its next scheduled meeting.

Our aim is to make the NIH's investment in this instrument as accessible as possible to the community and insure that it remains an important resource in your research arsenal.

The OARC Technical Administration Team

- [Leslie.Michelson@rutgers.edu](mailto:Leslie.Michelson@rutgers.edu)
