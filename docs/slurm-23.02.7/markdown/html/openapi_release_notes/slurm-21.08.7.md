## Slurm 21.08.7

### openapi/v0.0.37

#### Fix misspelling: change account_gather_freqency to account_gather_frequency (only the spec was wrong; the underlying code already worked with the correct spelling).

|               |                                                                                  |
|---------------|----------------------------------------------------------------------------------|
| previous path | .components.schemas."v0.0.37_job_properties".properties.account_gather_freqency  |
| new path      | .components.schemas."v0.0.37_job_properties".properties.account_gather_frequency |

#### Fix misspelling: change cluster_constraints to cluster_constraint (only the spec was wrong; the underlying code already worked with the correct spelling).

|               |                                                                             |
|---------------|-----------------------------------------------------------------------------|
| previous path | .components.schemas."v0.0.37_job_properties".properties.cluster_constraints |
| new path      | .components.schemas."v0.0.37_job_properties".properties.cluster_constraint  |
