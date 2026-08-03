# Upcoming change to /projects/community on Amarel

This Markdown file was generated from the Rutgers OARC website for RAG ingestion.

## Provenance

- Source URL: https://oarc.rutgers.edu/upcoming-change-to-projects-community-on-amarel/
- Source sitemap: https://oarc.rutgers.edu/page-sitemap.xml
- Sitemap type: page-sitemap.xml
- Last modified from sitemap: 2026-05-14T14:54:02+00:00
- Fetched on: 2026-05-22
- HTTP status: 200

## Upcoming change to /projects/community on Amarel

Dear Amarel Users,

As we continue our migration from CentOS to Red Hat Enterprise Linux (RHEL), we are implementing changes to our shared software directories to ensure a stable environment for the new operating system.

During the scheduled maintenance window next week (May 19-20), we will be transitioning the /projects/community path. To help you prepare, we have outlined how this affects your current workflows and where new software will reside.

**New RHEL Environment: /projects/community**

Moving forward, the /projects/community directory will be reserved exclusively for software installations built and supported on Red Hat.

New Standards: For software to be part of the supported community stack, it must include a module file located in /projects/community/modulefiles.

Cleanup Policy: To maintain system health, software installations found without a corresponding module file may be removed during periodic cleanup operations.

**Legacy Environment: /projects/community-old**

The current CentOS-based /projects/community directory will be renamed to /projects/community-old. All your existing files and software will remain accessible, but you must update your access methods.

To continue using modules from the old environment, you must manually add the path by running: module use /projects/community-old/modulefiles

If you have the old path configured in your .bashrc file or other startup scripts, please update those entries to reflect the new -old suffix.

We recommend reviewing any workflows, environment modules, or scripts that may depend on the current path structure.

If you have any questions or concerns regarding these changes, please reach out to our team at [help@oarc.rutgers.edu](mailto:help@oarc.rutgers.edu).

Best regards,

The OARC Team
