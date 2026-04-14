## Slurm 23.02.3

### openapi/v0.0.39

#### Correct invalid reference in status schema

|                |                                              |
|----------------|----------------------------------------------|
| Field modified | .components.schemas.status.properties.errors |

#### Revert removal of Job description "oversubscribe" field

|           |                                                                     |
|-----------|---------------------------------------------------------------------|
| New field | .components.schemas."v0.0.39_job_desc_msg".properties.oversubscribe |
| New field | .components.schemas."v0.0.39_job_info".properties.oversubscribe     |
