# Research Data Storage and Compute Environment Finder

RAG source capture of Rutgers Research Data Storage and Compute Environment Finder content,
including visible finder text, filter options, filter-to-service mappings, and full service
comparison details.

## Provenance

- Source page: https://researchdatafinder.rutgers.edu/
- Finder settings endpoint: https://researchdatafinder.rutgers.edu/rest/finder_settings
- Facet tree endpoint: https://researchdatafinder.rutgers.edu/rest/facettree
- Service list endpoint: https://researchdatafinder.rutgers.edu/rest/servicelist
- Fetched on: 2026-05-22
- Source system: Drupal 10 ResearchDataFinder finder app
- Transformation: HTML field values converted to Markdown; source IDs preserved.

## Page Content

- Page title: Research Data Storage and Compute Environment Finder
- Subtitle: This tool assists in identifying the most suitable data storage and computational
  environment for research purposes. The available services can be assessed based on storage
  capacity, capability to handle sensitive data, computational resources, and cost considerations.
- Question header: Select filters below to find the data solution that fits your needs.
  To learn more about each filter, simply click the information button next to the
  question. A description will appear explaining what the filter does and how it affects your
  results.
- Service header: Select tiles to generate a comparison table below.
- Select-all button label: Select All
- Clear-selections button label: Clear Selections
- Footer: The Research Data Storage and Compute Environment Finder tool is managed by OARC.
- Footer contact: https://oarc.rutgers.edu/contact-oarc/
- Attribution: Cornell University Research Data Management Service Group and Cornell Information
  Technologies Custom Development Group (2018), Finder Module, Drupal 8,
  https://github.com/CornellCustomDev/CD-finder
- Powered by: Drupal

## Finder Behavior

- The rendered page presents every finder option as a checkbox input.
- Questions marked `control_type: radio` in the source data are treated as exclusive groups by
  JavaScript: selecting one option deselects the other options in that question.
- Questions marked `control_type: checkbox` allow multiple selected options.
- A service matches selected criteria when its `facet_matches` list contains every selected option ID.
- Service tile checkboxes select matching services for the comparison table.
- Comparison-table checkboxes show or hide selected service columns after services are selected.

## Finder Questions and Options

### What is the classification of your data?

- Question ID: 28
- Source control type: radio
- Rendered input type: checkbox
- Description: **Low-risk data** is information intended for public use, where loss of
  confidentiality, integrity, or availability would have little to no impact. (Basic Research)
  **Moderate-risk data** includes internal or confidential information not meant for public release,
  where unauthorized access could cause mild harm to mission, safety, finances, or reputation.
  **High-risk data** consists of highly sensitive information protected by law or regulation, where
  compromise would cause significant legal, financial, operational, or reputational damage. (PII,
  PHI, HIPAA, FERPA, PCI)
- Options:
  - Checkbox option `34`: Low risk (ex. Basic research, Public)
    - Source option control type: radio
    - Matching storage options: Amarel High-Performance Computing (HPC) Cluster; Cloud Services;
      Data Management Plan Tool; Electronic Laboratory Notebooks; External Data Repositories; Globus
      Connect; Google Drive; OneDrive; Open Science Framework; Qualtrics; REDCap; Rutgers BOX;
      Rutgers Enterprise Virtual Infrastructure; Rutgers Research Data Storage; Rutgers University
      Libraries; Rutgers Virtual Computer Labs
  - Checkbox option `35`: Moderate risk (ex. Sensitive, Internal)
    - Source option control type: radio
    - Matching storage options: Cloud Services; Data Management Plan Tool; Globus Connect; OneDrive;
      REDCap; Rutgers BOX
  - Checkbox option `36`: High risk (ex. PHI, Restricted, Protected)
    - Source option control type: radio
    - Matching storage options: Clinical Research Data Warehouse; Cloud Services; Data Management
      Plan Tool; Globus Connect; OneDrive; Rutgers BOX

### Who needs access to the data?

- Question ID: 30
- Source control type: radio
- Rendered input type: checkbox
- Description: **RU NetIDs** - access requires an active Rutgers NetID/password; includes Rutgers
  guest NetIDs
  **External researchers** - access includes RU NetIDs and those with permissions
  **Public** - general access and includes RU NetIDs; external researchers
- Options:
  - Checkbox option `40`: RU NetIDs
    - Source option control type: radio
    - Matching storage options: Amarel High-Performance Computing (HPC) Cluster; Clinical Research
      Data Warehouse; Cloud Services; Data Management Plan Tool; Electronic Laboratory Notebooks;
      External Data Repositories; Genomics Center; Globus Connect; Google Drive; OneDrive; Open
      Science Framework; Qualtrics; REDCap; Rutgers BOX; Rutgers Enterprise Virtual Infrastructure;
      Rutgers Research Data Storage; Rutgers University Libraries; Rutgers Virtual Computer Labs
  - Checkbox option `41`: External researchers
    - Source option control type: radio
    - Matching storage options: Amarel High-Performance Computing (HPC) Cluster; Cloud Services;
      Data Management Plan Tool; Electronic Laboratory Notebooks; External Data Repositories; Globus
      Connect; Google Drive; OneDrive; Open Science Framework; Rutgers BOX; Rutgers University
      Libraries; Rutgers Virtual Computer Labs
  - Checkbox option `42`: Public
    - Source option control type: radio
    - Matching storage options: Cloud Services; Data Management Plan Tool; External Data
      Repositories; Open Science Framework; Rutgers University Libraries

### What is your primary purpose for data storage

- Question ID: 31
- Source control type: radio
- Rendered input type: checkbox
- Description: **Data processing and analytics** transform raw information into structured,
  meaningful insights by collecting, preparing, analyzing, and interpreting data to support
  research, predictive, and informed decision-making. **Data backup and data sharing** ensure that
  information is protected from loss by creating and storing copies, and can be securely accessed or
  exchanged to support researchers and research reproducibility through continuity, collaboration,
  and transparency.
- Options:
  - Checkbox option `37`: Data processing
    - Source option control type: radio
    - Matching storage options: Amarel High-Performance Computing (HPC) Cluster; Clinical Research
      Data Warehouse; Electronic Laboratory Notebooks; Genomics Center; Open Science Framework;
      Qualtrics; REDCap; Rutgers Enterprise Virtual Infrastructure; Rutgers Research Data Storage;
      Rutgers Virtual Computer Labs
  - Checkbox option `38`: Backup
    - Source option control type: radio
    - Matching storage options: Cloud Services; Google Drive; OneDrive; Rutgers BOX; Rutgers
      Research Data Storage
  - Checkbox option `39`: Open data sharing
    - Source option control type: radio
    - Matching storage options: Cloud Services; Data Management Plan Tool; External Data
      Repositories; Globus Connect; Open Science Framework; Rutgers University Libraries

### How much data storage capacity will you need?

- Question ID: 29
- Source control type: radio
- Rendered input type: checkbox
- Description: n/a
- Options:
  - Checkbox option `43`: Under 100 GB
    - Source option control type: radio
    - Matching storage options: Amarel High-Performance Computing (HPC) Cluster; Cloud Services;
      Google Drive; OneDrive; Rutgers BOX; Rutgers Enterprise Virtual Infrastructure; Rutgers
      Research Data Storage
  - Checkbox option `44`: 100 GB to 1 TB
    - Source option control type: radio
    - Matching storage options: Amarel High-Performance Computing (HPC) Cluster; Cloud Services;
      OneDrive; Rutgers BOX; Rutgers Enterprise Virtual Infrastructure; Rutgers Research Data
      Storage
  - Checkbox option `46`: 1 to 5 TB
    - Source option control type: radio
    - Matching storage options: Cloud Services; OneDrive; Rutgers BOX; Rutgers Research Data Storage
  - Checkbox option `45`: Over 5 TB
    - Source option control type: radio
    - Matching storage options: Cloud Services; Rutgers Research Data Storage
  - Checkbox option `47`: Not applicable
    - Source option control type: checkbox
    - Matching storage options: Clinical Research Data Warehouse; Data Management Plan Tool;
      Electronic Laboratory Notebooks; External Data Repositories; Genomics Center; Globus Connect;
      Open Science Framework; Qualtrics; REDCap; Rutgers University Libraries; Rutgers Virtual
      Computer Labs

### Does your data require protection with backups, snapshots, or replication?

- Question ID: 27
- Source control type: checkbox
- Rendered input type: checkbox
- Description: **Snapshots/Backups** Protect against corruption or unintended user deletion. Captures
  the exact state of data at a specific moment for fast, consistent recovery. Some options retain
  versions of the data as it changes. (see specific service for limitations.)
  **Replication** Does not protect against corruption or unintended user deletion. Continuously
  copies data to another system in real or near-real time to ensure up-to-date redundancy.
- Options:
  - Checkbox option `32`: Snapshots/Backups
    - Source option control type: checkbox
    - Matching storage options: Amarel High-Performance Computing (HPC) Cluster; Cloud Services;
      Google Drive; OneDrive; REDCap; Rutgers BOX; Rutgers Enterprise Virtual Infrastructure;
      Rutgers Research Data Storage
  - Checkbox option `33`: Replication
    - Source option control type: checkbox
    - Matching storage options: Amarel High-Performance Computing (HPC) Cluster; Cloud Services;
      Google Drive; OneDrive; Rutgers BOX; Rutgers Research Data Storage
  - Checkbox option `48`: Not applicable
    - Source option control type: n/a
    - Matching storage options: Clinical Research Data Warehouse; Data Management Plan Tool;
      Electronic Laboratory Notebooks; External Data Repositories; Genomics Center; Globus Connect;
      Open Science Framework; Qualtrics; Rutgers University Libraries; Rutgers Virtual Computer Labs

## Option-to-Storage Alignment

Use this section when a user asks which storage or compute services align with a particular
checkbox/filter option. For multi-option scenarios, intersect the matching service lists for all
selected options.

### What is the classification of your data?

#### Low risk (ex. Basic research, Public) (`34`)

- Amarel High-Performance Computing (HPC) Cluster
- Cloud Services
- Data Management Plan Tool
- Electronic Laboratory Notebooks
- External Data Repositories
- Globus Connect
- Google Drive
- OneDrive
- Open Science Framework
- Qualtrics
- REDCap
- Rutgers BOX
- Rutgers Enterprise Virtual Infrastructure
- Rutgers Research Data Storage
- Rutgers University Libraries
- Rutgers Virtual Computer Labs

#### Moderate risk (ex. Sensitive, Internal) (`35`)

- Cloud Services
- Data Management Plan Tool
- Globus Connect
- OneDrive
- REDCap
- Rutgers BOX

#### High risk (ex. PHI, Restricted, Protected) (`36`)

- Clinical Research Data Warehouse
- Cloud Services
- Data Management Plan Tool
- Globus Connect
- OneDrive
- Rutgers BOX

### Who needs access to the data?

#### RU NetIDs (`40`)

- Amarel High-Performance Computing (HPC) Cluster
- Clinical Research Data Warehouse
- Cloud Services
- Data Management Plan Tool
- Electronic Laboratory Notebooks
- External Data Repositories
- Genomics Center
- Globus Connect
- Google Drive
- OneDrive
- Open Science Framework
- Qualtrics
- REDCap
- Rutgers BOX
- Rutgers Enterprise Virtual Infrastructure
- Rutgers Research Data Storage
- Rutgers University Libraries
- Rutgers Virtual Computer Labs

#### External researchers (`41`)

- Amarel High-Performance Computing (HPC) Cluster
- Cloud Services
- Data Management Plan Tool
- Electronic Laboratory Notebooks
- External Data Repositories
- Globus Connect
- Google Drive
- OneDrive
- Open Science Framework
- Rutgers BOX
- Rutgers University Libraries
- Rutgers Virtual Computer Labs

#### Public (`42`)

- Cloud Services
- Data Management Plan Tool
- External Data Repositories
- Open Science Framework
- Rutgers University Libraries

### What is your primary purpose for data storage

#### Data processing (`37`)

- Amarel High-Performance Computing (HPC) Cluster
- Clinical Research Data Warehouse
- Electronic Laboratory Notebooks
- Genomics Center
- Open Science Framework
- Qualtrics
- REDCap
- Rutgers Enterprise Virtual Infrastructure
- Rutgers Research Data Storage
- Rutgers Virtual Computer Labs

#### Backup (`38`)

- Cloud Services
- Google Drive
- OneDrive
- Rutgers BOX
- Rutgers Research Data Storage

#### Open data sharing (`39`)

- Cloud Services
- Data Management Plan Tool
- External Data Repositories
- Globus Connect
- Open Science Framework
- Rutgers University Libraries

### How much data storage capacity will you need?

#### Under 100 GB (`43`)

- Amarel High-Performance Computing (HPC) Cluster
- Cloud Services
- Google Drive
- OneDrive
- Rutgers BOX
- Rutgers Enterprise Virtual Infrastructure
- Rutgers Research Data Storage

#### 100 GB to 1 TB (`44`)

- Amarel High-Performance Computing (HPC) Cluster
- Cloud Services
- OneDrive
- Rutgers BOX
- Rutgers Enterprise Virtual Infrastructure
- Rutgers Research Data Storage

#### 1 to 5 TB (`46`)

- Cloud Services
- OneDrive
- Rutgers BOX
- Rutgers Research Data Storage

#### Over 5 TB (`45`)

- Cloud Services
- Rutgers Research Data Storage

#### Not applicable (`47`)

- Clinical Research Data Warehouse
- Data Management Plan Tool
- Electronic Laboratory Notebooks
- External Data Repositories
- Genomics Center
- Globus Connect
- Open Science Framework
- Qualtrics
- REDCap
- Rutgers University Libraries
- Rutgers Virtual Computer Labs

### Does your data require protection with backups, snapshots, or replication?

#### Snapshots/Backups (`32`)

- Amarel High-Performance Computing (HPC) Cluster
- Cloud Services
- Google Drive
- OneDrive
- REDCap
- Rutgers BOX
- Rutgers Enterprise Virtual Infrastructure
- Rutgers Research Data Storage

#### Replication (`33`)

- Amarel High-Performance Computing (HPC) Cluster
- Cloud Services
- Google Drive
- OneDrive
- Rutgers BOX
- Rutgers Research Data Storage

#### Not applicable (`48`)

- Clinical Research Data Warehouse
- Data Management Plan Tool
- Electronic Laboratory Notebooks
- External Data Repositories
- Genomics Center
- Globus Connect
- Open Science Framework
- Qualtrics
- Rutgers University Libraries
- Rutgers Virtual Computer Labs

## Service Summary List

- `6` Amarel High-Performance Computing (HPC) Cluster: A shared community-owned advanced computing
  environment.
- `1` Clinical Research Data Warehouse: A HIPAA-compliant and NIST SP 800-171-compliant central
  repository that includes access diverse healthcare data and essential analytical tools.
- `4` Cloud Services: Cloud computing platforms from Amazon, Google, and Microsoft.
- `13` Data Management Plan Tool: A free, community-supported service used to create data management
  and sharing plans.
- `7` Electronic Laboratory Notebooks: A digital version of a traditional paper lab notebook.
- `24` External Data Repositories: NIH-Supported Data Sharing Resources offer flexible platforms for
  sharing a wide range of research outputs.
- `15` Genomics Center: The Genomics Center specializes in Next Generation Sequencing (NGS) and
  provides library preparation and data analysis.
- `14` Globus Connect: Secure, reliable, and efficient data transfer and sharing across different
  storage systems
- `11` Google Drive: Cloud storage a part of Rutgers' ScarletApps suite, available to all Faculty,
  Staff, Students, and Guests.
- `10` OneDrive: OneDrive for Business is a feature of Rutgers Connect where you can store, sync,
  and share your work files in the cloud.
- `22` Open Science Framework: A free, open-access repository and project management platform
  designed to support the entire research lifecycle.
- `3` Qualtrics: A survey software tool to help collect data for educational and organizational
  goals
- `9` REDCap: A web-based application for building and managing online surveys and databases.
- `5` Rutgers BOX: Cloud-based storage available to students, faculty, and staff.
- `8` Rutgers Enterprise Virtual Infrastructure: Virtual infrastructure hosting environment.
- `12` Rutgers Research Data Storage: An on-premise system designed to support short- and long-term
  data storage for researchers.
- `23` Rutgers University Libraries: Provide access to a vast range of resources, services, and
  expertise.
- `19` Rutgers Virtual Computer Labs: Access computer lab PCs from any location at any time.

## Full Service Details

### Amarel High-Performance Computing (HPC) Cluster

- Service ID: 6
- Summary: A shared community-owned advanced computing environment.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public)
  - Who needs access to the data?: RU NetIDs, External researchers
  - What is your primary purpose for data storage: Data processing
  - How much data storage capacity will you need?: Under 100 GB, 100 GB to 1 TB
  - Does your data require protection with backups, snapshots, or replication?: Snapshots/Backups,
    Replication
- Raw facet match IDs: 28, 34, 30, 40, 41, 31, 37, 29, 43, 44, 27, 32, 33
- Comparison fields:
  - Description: **Amarel** is a shared community-owned advanced computing environment available to
  any investigator or student with projects requiring research computing resources. The model is
  distinguished by a set of uniform technical and policy elements that, while sufficiently flexible
  to support the degree of heterogeneity inherent in the Rutgers environment, affords a level of
  standardization that greatly simplifies management procedures, troubleshooting, and provides a
  more seamless user experience.
  - Data Allowed: Sensitive data is not allowed
  - Features: **High-performance compute nodes and accelerators across three campuses:**Piscataway,
  Camden, and Newark
  **Traditional High Performance Computing** **High Throughput Computing (HTC)** **Data Analytics**
  **Large memory systems** **Virtualization** **Accelerators (GPGPUs, XEON PHIs, FPGAs)** **The
  ability to couple with edge devices**
  **Graphical Desktop Environment:**Open On Demand and FastX
  **InfiniBand FDR & EDR fabric**
  - Limits: **Storage:**100 GB home directory, 1 TB soft limit, and 2 TB hard limit scratch
  directory*
  **Number of Files:**5 million
  *HPC Storage is a component of the HPC Cluster, specifically designed to handle high-throughput
  calculations. It is not intended for long-term storage
  - Cost: **Compute:**
  [https://oarc.rutgers.edu/resources/amarel/](https://oarc.rutgers.edu/resources/amarel/)
  **Storage**:
  [https://oarc.rutgers.edu/resources/storage/](https://oarc.rutgers.edu/resources/storage/)
  - Access: All faculty, staff, students, and guests
  - Collaboration: -
  - Website:
  [https://oarc.rutgers.edu/resources/amarel/](https://oarc.rutgers.edu/resources/amarel/)
  - Alternative Website: -
  - Contact: [help@oarc.rutgers.edu](mailto:help@oarc.rutgers.edu)

### Clinical Research Data Warehouse

- Service ID: 1
- Summary: A HIPAA-compliant and NIST SP 800-171-compliant central repository that includes access
  diverse healthcare data and essential analytical tools.
- Finder options matched by this service:
  - What is the classification of your data?: High risk (ex. PHI, Restricted, Protected)
  - Who needs access to the data?: RU NetIDs
  - What is your primary purpose for data storage: Data processing
  - How much data storage capacity will you need?: Not applicable
  - Does your data require protection with backups, snapshots, or replication?: Not applicable
- Raw facet match IDs: 28, 36, 30, 40, 31, 37, 29, 47, 27, 48
- Comparison fields:
  - Description: The **Clinical Research Data Warehouse (CRDW)** is a secure, HIPAA-compliant, and
  NIST SP 800-171-compliant central repository that includes diverse healthcare data and essential
  analytical tools for gaining insights into medical conditions, outcomes, and treatments.
  - Data Allowed: HIPAA-compliant and NIST SP 800-171-compliant
  - Features: **Infrastructure services:**Virtual hosting compute, secure networks, high-performance
  block storage, object storage for unstructured data, Citrix access desktops, Staging server, Bulk
  drive data transfer
  **Data services:** BioFortis, PowerBI
  **Security services:**Network segmentation, End-Point (Cisco AMP)
  **User support services:** Experimental design, data governance council (DGC), Secure data import
  and export, researcher support
  - Limits: **-**
  - Cost: [CDRW Fee Schedule](https://it.rutgers.edu/clinical-and-research-data-warehouse/fee-
  schedule/)
  - Access: -
  - Collaboration: Yes
  - Website: [https://crdw.rutgers.edu](https://crdw.rutgers.edu)
  - Alternative Website: [https://it.rutgers.edu/clinical-and-research-data-
  warehouse](https://it.rutgers.edu/clinical-and-research-data-warehouse/)
  - Contact: [crdw_requests@oarc.rutgers.edu](mailto:crdw_requests@oarc.rutgers.edu)

### Cloud Services

- Service ID: 4
- Summary: Cloud computing platforms from Amazon, Google, and Microsoft.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public), Moderate risk
    (ex. Sensitive, Internal), High risk (ex. PHI, Restricted, Protected)
  - Who needs access to the data?: RU NetIDs, External researchers, Public
  - What is your primary purpose for data storage: Backup, Open data sharing
  - How much data storage capacity will you need?: Under 100 GB, 100 GB to 1 TB, 1 to 5 TB, Over 5
    TB
  - Does your data require protection with backups, snapshots, or replication?: Snapshots/Backups,
    Replication
- Raw facet match IDs: 28, 34, 35, 36, 30, 40, 41, 42, 31, 38, 39, 29, 43, 44, 46, 45, 27, 32, 33
- Comparison fields:
  - Description: The Rutgers **cloud services** team assists Rutgers departments and units seeking
  to use cloud computing platforms from Amazon, Google, and Microsoft. Enterprise agreements and
  business associate agreements are in place and available for use.
  - Data Allowed: Currently, only non-sensitive data
  - Features: **Flexibility:** Cloud computing is immediately responsive to changing needs
  **Scalability:**Unlimited resources and ubiquitous access result in greater productivity
  **Security:**Providers secure the infrastructure, and users secure data in transport and at rest
  **Cost savings:**Pooled cloud resources and pay-per-use minimize capital expenditures
  **Multiple locations** Distant data back-up facilitates disaster recovery and business continuity
  services
  **Cloud providers comparison matrix:**[https://it.rutgers.edu/cloud-services/provider-
  comparison/](https://it.rutgers.edu/cloud-services/provider-comparison/)
  - Limits: Scales with need
  - Cost: [Varies (Pay per use)](https://it.rutgers.edu/cloud-services/)
  - Access: Faculty, and staff
  - Collaboration: Yes
  - Website: [https://it.rutgers.edu/cloud-services/](https://it.rutgers.edu/cloud-services/)
  - Alternative Website: -
  - Contact:
  [https://oitforms.rutgers.edu/cloud_support](https://oitforms.rutgers.edu/cloud_support)

### Data Management Plan Tool

- Service ID: 13
- Summary: A free, community-supported service used to create data management and sharing plans.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public), Moderate risk
    (ex. Sensitive, Internal), High risk (ex. PHI, Restricted, Protected)
  - Who needs access to the data?: RU NetIDs, External researchers, Public
  - What is your primary purpose for data storage: Open data sharing
  - How much data storage capacity will you need?: Not applicable
  - Does your data require protection with backups, snapshots, or replication?: Not applicable
- Raw facet match IDs: 31, 39, 28, 34, 35, 36, 29, 47, 27, 48, 30, 40, 41, 42, 49
- Comparison fields:
  - Description: Rutgers is a participating institution in the data management plan (DMP)
  application called **DMPTool**. It is a free, open-source application recommended by the National
  Science Foundation (NSF), the National Institutes of Health (NIH), and other large funding
  agencies that require such plans to be included in funding proposals.
  - Data Allowed: -
  - Features: **Customization tools:** Creating ready-to-use data-management plans for specific
  agencies (DOE, DOEd, USDA, USGS, NASA, NIH, NSF, NEH)
  **Funders:**Meeting funder requirements for data management plans
  **Assistance:** Resources and services available at Rutgers to help fulfill the data management
  requirements of your grant
  - Limits: -
  - Cost: -
  - Access: -
  - Collaboration: -
  - Website: [https://oarc.rutgers.edu/resources/dmp-tool/](https://oarc.rutgers.edu/resources/dmp-
  tool/)
  - Alternative Website: [https://libguides.rutgers.edu/data-
  management](https://libguides.rutgers.edu/data-management)
  - Contact: [help@oarc.rutgers.edu](mailto:help@oarc.rutgers.edu)

### Electronic Laboratory Notebooks

- Service ID: 7
- Summary: A digital version of a traditional paper lab notebook.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public)
  - Who needs access to the data?: RU NetIDs, External researchers
  - What is your primary purpose for data storage: Data processing
  - How much data storage capacity will you need?: Not applicable
  - Does your data require protection with backups, snapshots, or replication?: Not applicable
- Raw facet match IDs: 31, 37, 28, 34, 29, 47, 27, 48, 30, 40, 41
- Comparison fields:
  - Description: An **Electronic Lab Notebook (ELN)** is a digital tool for documenting research,
  experiments, and procedures, replacing traditional paper notebooks. ELNs offer enhanced data
  management, security, and collaboration features, allowing easy data entry, searchability, and
  integration with scientific instruments. They support good data practices, facilitate team
  collaboration, and often include specialized scientific tools, making them invaluable for
  researchers across various disciplines.
  **LabArchives** is available as a course tool
  **ELNs** for research are still under consideration
  - Data Allowed: -
  - Features: **LabArchives** - a content and data management platform that includes an integrated
  digital lab notebook module. This service allows instructors to add their lab manual, integrate an
  OpenStax textbook, and, in the future, lab manual content from a cross-disciplinary open-source
  lab manual repository.
  - **Easy two-way communication** between faculty, TAs, and students, which improves student
  engagement. - **Integrations with digital systems and platforms:** MS Office, Google, Box,
  ChemDoodle, Chem Sketcher, SnapGene, Canvas, Vernier, Turnitin, GraphPad, FLOWJO, etc., and more
  are coming. - **Integration with Canvas**
  - Limits: -
  - Cost: [More information](https://canvas.rutgers.edu/external-apps/labarchives/)
  - Access: -
  - Collaboration: -
  - Website: [https://canvas.rutgers.edu/external-
  apps/labarchives/](https://canvas.rutgers.edu/external-apps/labarchives/)
  - Alternative Website: -
  - Contact: -

### External Data Repositories

- Service ID: 24
- Summary: NIH-Supported Data Sharing Resources offer flexible platforms for sharing a wide range of
  research outputs.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public)
  - Who needs access to the data?: RU NetIDs, External researchers, Public
  - What is your primary purpose for data storage: Open data sharing
  - How much data storage capacity will you need?: Not applicable
  - Does your data require protection with backups, snapshots, or replication?: Not applicable
- Raw facet match IDs: 31, 39, 28, 34, 29, 47, 27, 48, 30, 40, 41, 42
- Comparison fields:
  - Description: NIH-Supported Data Sharing Resources
  Generalist repositories are open-access platforms that accept a wide variety of research data,
  regardless of discipline or format. They're ideal for sharing datasets that don't fit into a
  specific subject-based repository. By making your data publicly available through these
  repositories, you help increase its visibility, support reproducibility, and contribute to a more
  open and collaborative research environment.
  Framework repositories are structured platforms designed to support the development, sharing, and
  reuse of research tools, models, and workflows. Unlike generalist repositories, which focus on
  storing data, framework repositories often provide infrastructure for collaboration, version
  control, and integration with software or computational environments. These repositories help
  researchers build on existing work, ensure reproducibility, and accelerate innovation across
  disciplines.
  - Data Allowed: -
  - Features: Generalist repositories accept data regardless of data type, format, content, or
  disciplinary focus. Investigators may also have access to an institutional repository that would
  be suitable for sharing data and may consider contacting their institution's library to learn
  more.
  - Dataverse [https://dataverse.org/](https://dataverse.org/) - Dryad
  [https://datadryad.org/](https://datadryad.org/) - Figshare
  [https://figshare.com/](https://figshare.com/) - IEEEDataPort [https://ieee-
  dataport.org/](https://ieee-dataport.org/) - Mendeley
  [https://data.mendeley.com/](https://data.mendeley.com/) - OSF [https://osf.io/](https://osf.io/)
  - Synapse [https://www.synapse.org/](https://www.synapse.org/) - Vivli
  [https://vivli.org/](https://vivli.org/) - Zenodo [https://zenodo.org/](https://zenodo.org/)
  Domain-specific repositories are typically limited to data of a certain type or related to a
  certain discipline. There are over 100 domain-specific repositories described here:
  [https://www.nlm.nih.gov/NIHbmic/domain_specific_repositories.html](https://www.nlm.nih.gov/NIHbmic/domain_specific_repositories.html)
  - Limits: -
  - Cost: -
  - Access: -
  - Collaboration: -
  - Website:
  [https://www.nlm.nih.gov/NIHbmic/generalist_repositories.html#](https://www.nlm.nih.gov/NIHbmic/generalist_repositories.html#)
  - Alternative Website:
  [https://www.nlm.nih.gov/NIHbmic/domain_specific_repositories.html](https://www.nlm.nih.gov/NIHbmic/domain_specific_repositories.html)
  - Contact: -

### Genomics Center

- Service ID: 15
- Summary: The Genomics Center specializes in Next Generation Sequencing (NGS) and provides library
  preparation and data analysis.
- Finder options matched by this service:
  - Who needs access to the data?: RU NetIDs
  - What is your primary purpose for data storage: Data processing
  - How much data storage capacity will you need?: Not applicable
  - Does your data require protection with backups, snapshots, or replication?: Not applicable
- Raw facet match IDs: 31, 37, 28, 29, 47, 27, 48, 30, 40
- Comparison fields:
  - Description: The**Genomics Center** specializes in Next Generation Sequencing (NGS) and provides
  comprehensive services, including library preparation and data analysis. The center routinely
  sequences DNA and RNA samples from various sources, utilizing both established and custom
  protocols.
  It also offers robust data storage solutions, featuring large on-site and cloud storage
  capabilities for data backup, delivery of raw and/or analyzed data at the project's conclusion,
  and long-term storage options.
  - Data Allowed: -
  - Features: **DNA Sequencing:** Genomic DNA, Ultra low input DNA, Targeted , ChIP-Seq, ATAC-Seq,
  Methyl-Seq (RRBS), Methyl-Seq (WGS), 16S/18S ribosomal RNA genes (Bacterial/Fungal), Clinical
  diagnostic panels
  **RNA Sequencing:**RNA w/poly A selection, RNA w/RiboMinus, Ultra low input RNA (RNA
  amplification), 3'READS, Ribo-Seq, Small RNA, RIP-Seq, CLIP-Seq, Single Cell RNA-Seq (All 10X
  Chromium protocols)
  **Custom/New protocols:**Available to help implement or develop new sequencing protocols
  **Data Analysis:**DNASeq, RNASeq, Single Cell Seq, Microarrays, Custom data analysis, and new
  pipelines
  **Data Storage:** Large on-site, and cloud storage capabilities for data backup, and end of the
  project long-term storage available
  - Limits: -
  - Cost: -
  - Access: -
  - Collaboration: -
  - Website: [https://research-office.njms.rutgers.edu/research-genomics-lab](https://research-
  office.njms.rutgers.edu/research-genomics-lab)
  - Alternative Website: -
  - Contact: -

### Globus Connect

- Service ID: 14
- Summary: Secure, reliable, and efficient data transfer and sharing across different storage
  systems
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public), Moderate risk
    (ex. Sensitive, Internal), High risk (ex. PHI, Restricted, Protected)
  - Who needs access to the data?: RU NetIDs, External researchers
  - What is your primary purpose for data storage: Open data sharing
  - How much data storage capacity will you need?: Not applicable
  - Does your data require protection with backups, snapshots, or replication?: Not applicable
- Raw facet match IDs: 31, 39, 28, 34, 35, 36, 29, 47, 27, 48, 30, 40, 41, 49
- Comparison fields:
  - Description: **Globus Connect** is a service designed to simplify research data management by
  enabling secure, reliable, and efficient data transfer and sharing across different storage
  systems.
  Currently, the Globus license can be requested through OARC:
  [oarc.rutgers.edu](https://oarc.rutgers.edu)
  - Data Allowed: HIPAA Compliant, NIST standards, PHI, PII, and CUI
  - Features: **Data transfer:** Securely move large amounts of data between Globus 'endpoints'
  **Cloud:** Transfer data between cloud storage, Amarel, or a laptop from a web browser
  **Control Access:**Manage access to choose which collaborators have access, and to which specific
  data they have access
  **Resumable:** Can automatically resume transfers if there are network or system interruptions
  - Limits: -
  - Cost: -
  - Access: -
  - Collaboration: Yes
  - Website: [https://www.globus.org/globus-connect-personal](https://www.globus.org/globus-connect-
  personal)
  - Alternative Website: -
  - Contact: [help@oarc.rutgers.edu](mailto:help@oarc.rutgers.edu)

### Google Drive

- Service ID: 11
- Summary: Cloud storage a part of Rutgers' ScarletApps suite, available to all Faculty, Staff,
  Students, and Guests.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public)
  - Who needs access to the data?: RU NetIDs, External researchers
  - What is your primary purpose for data storage: Backup
  - How much data storage capacity will you need?: Under 100 GB
  - Does your data require protection with backups, snapshots, or replication?: Snapshots/Backups,
    Replication
- Raw facet match IDs: 28, 34, 30, 40, 41, 31, 38, 29, 43, 27, 32, 33
- Comparison fields:
  - Description: **Google Drive** is part of Rutgers' ScarletApps suite and is available to all
  Faculty, Staff, Students, and Guests.
  - Data Allowed: Google Drive **cannot** be used for the storage of restricted data like files
  containing protected health information (PHI)
  - Features: **Cloud-based file storage**
  **Seamless integration with the**[**ScarletApps**](https://it.rutgers.edu/scarletapps/)**suite**
  **Integrated with Canvas**
  - Limits: **Storage:** 30 GB
  **File Size:** 30 GB
  **Number of Files:** None
  - Cost: No cost
  - Access: All faculty, staff, students, and guests
  - Collaboration: Yes
  - Website: [https://it.rutgers.edu/scarletapps/](https://it.rutgers.edu/scarletapps/)
  - Alternative Website: [Google Drive on
  ScarletApps](https://ithelp.rutgers.edu/sp?id=kb_article&sysparm_article=KB0012529) [Comparison
  Matrix](https://it.rutgers.edu/cloud-storage/knowledgebase/data-classification-and-storage-matrix-
  comparing-box-onedrive-and-google-drive/)
  - Contact: [help@oit.rutgers.edu](mailto:help@oit.rutgers.edu)

### OneDrive

- Service ID: 10
- Summary: OneDrive for Business is a feature of Rutgers Connect where you can store, sync, and
  share your work files in the cloud.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public), Moderate risk
    (ex. Sensitive, Internal), High risk (ex. PHI, Restricted, Protected)
  - Who needs access to the data?: RU NetIDs, External researchers
  - What is your primary purpose for data storage: Backup
  - How much data storage capacity will you need?: Under 100 GB, 100 GB to 1 TB, 1 to 5 TB
  - Does your data require protection with backups, snapshots, or replication?: Snapshots/Backups,
    Replication
- Raw facet match IDs: 28, 34, 35, 36, 30, 40, 41, 31, 38, 29, 43, 44, 46, 27, 32, 33
- Comparison fields:
  - Description: **OneDrive**for Business is a feature of Rutgers Connect (Office 365) where you can
  store, sync, and share your work files in the cloud. With **OneDrive**for Business, you can share
  and collaborate on work documents with co-workers.
  - Data Allowed: ["PHI", and other sensitive data](https://it.rutgers.edu/cloud-
  storage/knowledgebase/data-classification-and-storage-matrix-comparing-box-onedrive-and-google-
  drive/)
  - Features: **Cloud-based file storage**
  **Seamless integration with Microsoft software**
  **Integrated with Canvas**
  - Limits: **Storage:** 5 TB
  **File Size:**250 GB
  **Number of Files:** 30 million documents (300,000 limit recommended for sync performance)
  - Cost: No cost
  - Access: Faculty, and staff
  - Collaboration: Yes
  - Website: [https://it.rutgers.edu/rutgers-connect/](https://it.rutgers.edu/rutgers-connect/)
  - Alternative Website:
  [OneDrive_for_Business](https://ithelp.rutgers.edu/sp?id=kb_article&sysparm_article=KB0012617)
  [Comparison Matrix](https://it.rutgers.edu/cloud-storage/knowledgebase/data-classification-and-
  storage-matrix-comparing-box-onedrive-and-google-drive/)
  - Contact: [help@oit.rutgers.edu](mailto:help@oit.rutgers.edu)

### Open Science Framework

- Service ID: 22
- Summary: A free, open-access repository and project management platform designed to support the
  entire research lifecycle.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public)
  - Who needs access to the data?: RU NetIDs, External researchers, Public
  - What is your primary purpose for data storage: Data processing, Open data sharing
  - How much data storage capacity will you need?: Not applicable
  - Does your data require protection with backups, snapshots, or replication?: Not applicable
- Raw facet match IDs: 28, 34, 30, 40, 41, 42, 31, 37, 39, 29, 47, 27, 48
- Comparison fields:
  - Description: **Open Science Framework (OSF)** is a free, open-access repository and project
  management platform designed to support the entire research lifecycle, from planning and execution
  to reporting, archiving, and discovery. It offers automated versioning, action logging,
  collaboration tools, unlimited file storage, registrations, and integrations with other services.
  Researchers can work privately or share projects publicly for broad dissemination, while its
  workflow system streamlines connections to existing tools, enhancing efficiency and productivity.
  - Data Allowed: -
  - Features: -
  - Limits: -
  - Cost: [Variable tiered system](https://www.cos.io/osf-
  usage?hsCtaTracking=76855c49-086f-4333-8bdc-d3a1f4e1f8ae%7C9e805e14-a511-4399-ab62-09bdf431a223)
  - Access: -
  - Collaboration: Yes
  - Website: [https://osf.io/](https://osf.io/)
  - Alternative Website: -
  - Contact: [support@osf.io](mailto:support@osf.io)

### Qualtrics

- Service ID: 3
- Summary: A survey software tool to help collect data for educational and organizational goals
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public)
  - Who needs access to the data?: RU NetIDs
  - What is your primary purpose for data storage: Data processing
  - How much data storage capacity will you need?: Not applicable
  - Does your data require protection with backups, snapshots, or replication?: Not applicable
- Raw facet match IDs: 31, 37, 28, 34, 29, 47, 27, 48, 30, 40
- Comparison fields:
  - Description: A survey software tool offered by Rutgers to collect data for educational and
  organizational goals.
  - Data Allowed: HIPAA Compliant
  - Features: **Data Collection:**For educational and organizational goals
  **Research and Productivity:**Predicting trends in a wide array of subjects, and enhancing the
  productivity of Rutgers departments and organizations.
  **HIPAA-compliant:** For units that routinely handle HIPAA-protected data
  - Limits: **Emails:**limited to 10,000 per week (see the [software
  portal](https://it.rutgers.edu/qualtrics/) for limits)
  **Use:**Not for personal or commercial gain unless the user agrees to additional spam guidelines
  - Cost: -
  - Access: All faculty, staff, students, and affiliates
  - Collaboration: -
  - Website: [https://it.rutgers.edu/qualtrics/](https://it.rutgers.edu/qualtrics/)
  - Alternative Website: -
  - Contact: [qualtrics_support@oit.rutgers.edu](mailto:qualtrics_support@oit.rutgers.edu)

### REDCap

- Service ID: 9
- Summary: A web-based application for building and managing online surveys and databases.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public), Moderate risk
    (ex. Sensitive, Internal)
  - Who needs access to the data?: RU NetIDs
  - What is your primary purpose for data storage: Data processing
  - How much data storage capacity will you need?: Not applicable
  - Does your data require protection with backups, snapshots, or replication?: Snapshots/Backups
- Raw facet match IDs: 28, 34, 35, 30, 40, 31, 37, 29, 47, 27, 32
- Comparison fields:
  - Description: **REDCap** is a secure, web-based application for building and managing online
  surveys and databases. While REDCap can be used to collect virtually any type of data in any
  environment, it is specifically geared to support online and offline data capture for research
  studies and operations.
  - Data Allowed: -
  - Features: **Build online surveys and databases quickly and securely in your browser**
  **Advanced instrument design features**
  **Data Quality:** Tools to improve and protect data quality during data entry
  **Create custom searches:**For generating reports to view aggregate data
  **Export your data to common analysis packages:** As a PDF or as CSV data for easy analysis in
  SAS, Stata, R, SPSS, or Microsoft Excel
  **Secure storage and sharing:** Upload and share any type of file with anyone in the world through
  the File Repository feature or Send-It tool
  **Data-based Alerts:** Send alerts and notifications to your team or other stakeholders via email,
  text, or phone
  **Connect to other resources:**Build your own custom software development features to connect your
  project to other systems
  - Limits: -
  - Cost: -
  - Access: All faculty, staff, students
  - Collaboration: Yes
  - Website: [https://it.rutgers.edu/redcap/](https://it.rutgers.edu/redcap/)
  - Alternative Website: [redcap.rutgers.edu](https://redcap.rutgers.edu)
  - Contact: [redcap-help@oarc.rutgers.edu](mailto:redcap-help@oarc.rutgers.edu)

### Rutgers BOX

- Service ID: 5
- Summary: Cloud-based storage available to students, faculty, and staff.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public), Moderate risk
    (ex. Sensitive, Internal), High risk (ex. PHI, Restricted, Protected)
  - Who needs access to the data?: RU NetIDs, External researchers
  - What is your primary purpose for data storage: Backup
  - How much data storage capacity will you need?: Under 100 GB, 100 GB to 1 TB, 1 to 5 TB
  - Does your data require protection with backups, snapshots, or replication?: Snapshots/Backups,
    Replication
- Raw facet match IDs: 28, 34, 35, 36, 30, 40, 41, 31, 38, 29, 43, 44, 46, 27, 32, 33
- Comparison fields:
  - Description: Box is a cloud-based file storage application where students, faculty, and staff
  can securely store, manage, and share digital files.
  - Data Allowed: ["PHI" and other sensitive data](https://it.rutgers.edu/cloud-
  storage/knowledgebase/data-classification-and-storage-matrix-comparing-box-onedrive-and-google-
  drive/)
  - Features: **Cloud-based file storage**
  **Seamless integration with Microsoft software**
  **Can be used to store "PHI" information**
  **Integrated with Canvas**
  - Limits: **Storage:**5 TB
  **File Size:** 50 GB
  **Number of Files:**Unlimited (15,000 per limit per folder recommended for performance)
  - Cost: No cost
  - Access: All faculty, staff, students, and guests
  - Collaboration: Yes
  - Website: [https://it.rutgers.edu/box/](https://it.rutgers.edu/box/)
  - Alternative Website: [Box at
  Rutgers](https://ithelp.rutgers.edu/sp?id=kb_article&sysparm_article=KB0012461&sys_kb_id=1b0bb3931b88ae54f2f2fe6e034bcba4&spa=1)
  [Comparison Matrix](https://it.rutgers.edu/cloud-storage/knowledgebase/data-classification-and-
  storage-matrix-comparing-box-onedrive-and-google-drive/)
  - Contact: [help@oit.rutgers.edu](mailto:help@oit.rutgers.edu)

### Rutgers Enterprise Virtual Infrastructure

- Service ID: 8
- Summary: Virtual infrastructure hosting environment.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public)
  - Who needs access to the data?: RU NetIDs
  - What is your primary purpose for data storage: Data processing
  - How much data storage capacity will you need?: Under 100 GB, 100 GB to 1 TB
  - Does your data require protection with backups, snapshots, or replication?: Snapshots/Backups
- Raw facet match IDs: 31, 37, 28, 34, 29, 43, 44, 27, 32, 30, 40
- Comparison fields:
  - Description: A **virtual infrastructure** hosting environment is available for all IT
  departments and the university community.
  - Data Allowed: -
  - Features: **Virtual Machines:**Managed, Self-managed, Private VM Clusters
  **High-performance storage**
  **High-speed networking**
  **Application load balancing**
  **Highly Available (HA) architectures**
  **Secure environments**
  **24/7 monitoring of critical infrastructure**
  - Limits: **Storage Limit:** 50GB for virtual machines
  - Cost: [Varies](https://it.rutgers.edu/research-data-storage/)
  - Access: All departments are eligible
  - Collaboration: Yes
  - Website: [https://it.rutgers.edu/virtual-infrastructure/](https://it.rutgers.edu/virtual-
  infrastructure/)
  - Alternative Website: -
  - Contact: [help@oit.rutgers.edu](mailto:help@oit.rutgers.edu)

### Rutgers Research Data Storage

- Service ID: 12
- Summary: An on-premise system designed to support short- and long-term data storage for
  researchers.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public)
  - Who needs access to the data?: RU NetIDs
  - What is your primary purpose for data storage: Data processing, Backup
  - How much data storage capacity will you need?: Under 100 GB, 100 GB to 1 TB, 1 to 5 TB, Over 5
    TB
  - Does your data require protection with backups, snapshots, or replication?: Snapshots/Backups,
    Replication
- Raw facet match IDs: 31, 37, 38, 28, 34, 29, 43, 44, 46, 45, 27, 32, 33, 30, 40
- Comparison fields:
  - Description: **Research Data Storage** (RDS) is a service provided by the Office of Information
  Technology (OIT), offering research labs and university centers reliable data storage, with 34 PB
  of usable space designed for both short- and long-term needs. Optimized for cost-effectiveness, it
  ensures reliable access to university research data. RDS is a collaborative effort managed and
  maintained by OIT's Office of Advanced Research Computing (OARC) and Enterprise Infrastructure.
  - Data Allowed: Currently, only non-sensitive data
  - Features: **Capacity and scalability**: An on-premise solution that scales to handle large
  research datasets
  **Uninterrupted availability and protection:** A three-site object storage system and two-site
  redundant storage configuration provide high data resilience and availability.
  **User-friendly access and management:** Storage efficiency is optimized via standard protocol
  access, an active-active configuration, and end-user self-management.
  - Limits: -
  - Cost: [See RDS site for pricing structure](https://it.rutgers.edu/research-data-storage/)
  - Access: All departments are eligible
  - Collaboration: No
  - Website: [https://it.rutgers.edu/research-data-storage/](https://it.rutgers.edu/research-data-
  storage/)
  - Alternative Website: -
  - Contact: [research_storage@oarc.rutgers.edu](mailto:research_storage@oarc.rutgers.edu)

### Rutgers University Libraries

- Service ID: 23
- Summary: Provide access to a vast range of resources, services, and expertise.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public)
  - Who needs access to the data?: RU NetIDs, External researchers, Public
  - What is your primary purpose for data storage: Open data sharing
  - How much data storage capacity will you need?: Not applicable
  - Does your data require protection with backups, snapshots, or replication?: Not applicable
- Raw facet match IDs: 31, 39, 28, 34, 29, 47, 27, 48, 30, 40, 41, 42
- Comparison fields:
  - Description: **Scholarly Open Access at Rutgers (SOAR)** provides free, long-term access to
  Rutgers research and creative work. Managed by Rutgers University Libraries, it helps faculty and
  departments archive their scholarship, meet funder requirements, and support the university's Open
  Access Policy.
  **RUCore** is Rutgers University's digital repository for preserving and sharing research and
  educational materials. It supports research, interdisciplinary collaboration, and knowledge
  creation by archiving faculty work and unique library resources, making them accessible for long-
  term use. RUcore no longer accepts data deposits.
  - Data Allowed: -
  - Features: -
  - Limits: -
  - Cost: -
  - Access: Rutgers faculty and researchers
  - Collaboration: -
  - Website: [https://soar.libraries.rutgers.edu/](https://soar.libraries.rutgers.edu/)
  - Alternative Website:
  [https://rucore.libraries.rutgers.edu/](https://rucore.libraries.rutgers.edu/)
  - Contact: [https://soar.libraries.rutgers.edu/contact-
  us](https://soar.libraries.rutgers.edu/contact-us)

### Rutgers Virtual Computer Labs

- Service ID: 19
- Summary: Access computer lab PCs from any location at any time.
- Finder options matched by this service:
  - What is the classification of your data?: Low risk (ex. Basic research, Public)
  - Who needs access to the data?: RU NetIDs, External researchers
  - What is your primary purpose for data storage: Data processing
  - How much data storage capacity will you need?: Not applicable
  - Does your data require protection with backups, snapshots, or replication?: Not applicable
- Raw facet match IDs: 31, 37, 28, 34, 29, 47, 27, 48, 30, 40, 41
- Comparison fields:
  - Description: Students, faculty, staff, and individuals with a guest role can utilize the OIT
  Virtual Computer lab's PCs and all Windows applications provided from any location at any time.
  However, guests will need to have their sponsor request a Rutgers Connect license before they can
  access the Virtual Labs.
  - Data Allowed: -
  - Features: **Azure Virtual Desktop**
  **Capacity for unlimited simultaneous usage**
  **Local storage options**
  **Access to some programs that cannot be licensed for physical labs**
  **Access to the Rutgers Mobility Printer Queue**
  [**Available software
  list**](https://ithelp.rutgers.edu/sp?id=kb_article&sysparm_article=KB0012455&sys_kb_id=65bb2f73db4d01108f550ad4e29619bc&spa=1)
  - Limits: -
  - Cost: [Printing
  rates](https://ithelp.rutgers.edu/sp?id=kb_article&sysparm_article=KB0012627&sys_kb_id=844ab11d1b7e1910b2c9ddb4cc4bcbd9&spa=1)
  - Access: All faculty, staff, students, and guests
  - Collaboration: -
  - Website: [https://it.rutgers.edu/virtual-computer-labs/](https://it.rutgers.edu/virtual-
  computer-labs/)
  - Alternative Website: [Accessing Virtual Computer
  Labs](https://ithelp.rutgers.edu/sp?id=kb_article_view&sysparm_article=KB0012438&sys_kb_id=89ee19c8876dd61064a443f5dabb3555&spa=1)
  - Contact: [oit-wvd-support@oit.rutgers.edu](mailto:oit-wvd-support@oit.rutgers.edu)

## Comparison Field Labels

The service list contains a non-displayed `Help` record used by the app to define comparison-table
field labels and ordering.

- Weight 0: Description
- Weight 1: Data Allowed
- Weight 2: Features
- Weight 3: Limits
- Weight 4: Cost
- Weight 5: Access
- Weight 6: Collaboration
- Weight 7: Website
- Weight 8: Alternative Website
- Weight 9: Contact

## Source Data Integrity Notes

- The following facet IDs appear in service `facet_matches` but are not present in the visible
  facet tree endpoint:
  - `49`: Data Management Plan Tool, Globus Connect
