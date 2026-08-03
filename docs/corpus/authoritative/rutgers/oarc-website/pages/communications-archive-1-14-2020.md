# Filesystem Access Issue for Open OnDemand Users

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/1-14-2020/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2020-08-31T20:30:56+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Filesystem Access Issue for Open OnDemand Users

Galen Collier Tuesday, January 14, 2020 at 9:36 am

Folks,

We've identified a problem with accessing Amarel and Perceval's storage systems from our browser-based Open OnDemand interface ([https://ondemand.hpc.rutgers.edu](https://ondemand.hpc.rutgers.edu)). The version of the GPFS software running on the OnDemand server is different from that of our storage systems and that difference is preventing OnDemand from accessing the storage servers.

Note: this problem only impacts access to the cluster using OnDemand - regular command-line access is not affected.

Our infrastructure administration team is working with IBM to get this issue resolved ASAP.

In the meantime, if you must have GUI-based access to Amarel or Perceval to proceed with your work, our FastX system may serve as a viable alternative. The desktop interface is very similar to that provided through OnDemand. Here are some basic instructions for getting started:

(1) Use a browser to access [https://amarel.rutgers.edu:3443](https://amarel.rutgers.edu:3443) (2) Confirm/accept the security exception (3) Log-in (4) Choose 'Launch Session' and select an XFCE Desktop, then click the Launch button. You'll be launching a desktop session on login node using FastX. (5) At this point, since you're using a login node, you'll want to get access to a compute node to run your applications. (6) Right-click and choose 'Open Terminal Here' (7) In that terminal window, launch an interactive session on a compute node. For example, 'srun -time=1:00:00 -pty bash' (8) From there, you can load modules and run GUI-based applications.

Please let me know if you have questions or need help.

Galen
