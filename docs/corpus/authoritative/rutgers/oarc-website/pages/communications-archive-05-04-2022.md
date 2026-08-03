# Amarel Phase 5A Nodes - Proceed with Full-Use of Resources

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/communications-archive/05-04-2022/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2022-05-04T21:05:27+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Amarel Phase 5A Nodes - Proceed with Full-Use of Resources

Amarel Phase 5A Owners,

In a message from February (see below), I requested that the Phase 5A nodes be loaded carefully, not using all cores.

That concern has been obviated. Please feel free to use the full capacity of those nodes - no need for restrained loading.

Thank you for your patience.

Galen

From: Galen Collier Sent: Tuesday, February 8, 2022 1:59 PM To: Galen Collier <galen.collier@rutgers.edu> Subject: Amarel Phase 5A Nodes Entering Production</galen.collier@rutgers.edu>

Amarel Phase 5A Owners,

Your Phase 5A nodes and storage are nearly ready for release. Each you will be hearing more from me about this within the next 24 hours.

We're facing a power distribution issue in the Hill Data Center that could impact the racks where these new compute nodes reside. Rather than delay release, I want to explain the situation and encourage you to simply be mindful of the issue until it's resolved (hopefully very soon): * The new racks are being fed by a power system that's missing some back-ordered components, so it's currently lacking the capacity we prefer to have for racks of nodes that may reach near-peak power consumption. * Half of the in-rack power distribution equipment is back-ordered due to widespread shipping delays, so the entire electrical load on those racks travels a single path. * This configuration is susceptible to drawing too much current and triggering an automatic shut-off. That means we must run at a slightly lower power draw than usual, which in-turn means that we need to try to limit the load your jobs place on those nodes until this issue is resolved. * Until the needed parts arrive, please try to avoid fully loading your new Phase 5A nodes. This can be done by using less than the full 64 cores onboard. We've been running tests with sample jobs that efficiently use all 64 cores and the system seems stable, but spikes in utilization from poorly-configured jobs could risk an isolated power outage for these racks.

Of course, let me know what questions or concerns you have.

Galen Collier, PhD Director, Research Support Office of Advanced Research Computing (OARC)
