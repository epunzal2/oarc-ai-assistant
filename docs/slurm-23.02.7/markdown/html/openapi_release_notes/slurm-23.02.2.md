## Slurm 23.02.2

### openapi/v0.0.39

#### Revert format change for job updates

|              |                                                 |
|--------------|-------------------------------------------------|
| Modify field | .paths."/job/{job_id}".post.requestBody.content |

#### Revert removal of Job description "exclusive" field

|           |                                                                 |
|-----------|-----------------------------------------------------------------|
| New field | .components.schemas."v0.0.39_job_desc_msg".properties.exclusive |
| New field | .components.schemas."v0.0.39_job_info".properties.exclusive     |

### openapi/dbv0.0.39

#### Revert removal of Job description "exclusive" field

|           |                                                                 |
|-----------|-----------------------------------------------------------------|
| New field | .components.schemas."v0.0.39_job_desc_msg".properties.exclusive |
| New field | .components.schemas."v0.0.39_job_info".properties.exclusive     |
