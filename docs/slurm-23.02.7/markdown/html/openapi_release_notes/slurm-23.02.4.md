## Slurm 23.02.4

### openapi/v0.0.39

#### Tag job description environment field as required

|           |                                                     |
|-----------|-----------------------------------------------------|
| Field add | .components.schemas."v0.0.39_job_desc_msg".required |

#### Add status schema to default

|             |                                              |
|-------------|----------------------------------------------|
| Field added | .paths."/licenses/".get.responses.default    |
| Field added | .paths."/job/{job_id}".get.responses.default |

#### Tag derived_exit_code and exit_code as UINT32_NO_VAL to avoid 4294967295 on still running jobs.

|               |                                                                     |
|---------------|---------------------------------------------------------------------|
| Field changed | .components.schemas."v0.0.39_job_info".properties.derived_exit_code |
| Field changed | .components.schemas."v0.0.39_job_info".properties.exit_code         |
|               |                                                                     |
