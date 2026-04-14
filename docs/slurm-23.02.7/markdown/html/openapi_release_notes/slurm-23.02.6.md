## Slurm 23.02.6

### openapi/v0.0.39

#### Correct path for responses types

|  |  |
|----|----|
| Updated paths | .paths."/slurm/v0.0.39/licenses".get.responses.default .paths."/slurm/v0.0.39/job/{job_id}".get.responses.default |

### openapi/dbv0.0.39

#### Switch integer to have NO_VAL tagging to allow for complex values.

|  |  |
|----|----|
| Field modified | .components.schemas."v0.0.39_assoc".properties.max.properties.jobs.properties.per.properties.count .components.schemas."v0.0.39_assoc".properties.max.properties.jobs.properties.active .components.schemas."v0.0.39_assoc".properties.max.properties.jobs.properties.accruing .components.schemas."v0.0.39_assoc".properties.max.properties.jobs.properties.total .components.schemas."v0.0.39_qos".properties.limits.properties.grace_time .components.schemas."v0.0.39_qos".properties.limits.properties.max.properties.active_jobs.properties.accruing .components.schemas."v0.0.39_qos".properties.limits.properties.max.properties.active_jobs.properties.count .components.schemas."v0.0.39_qos".properties.limits.properties.max.properties.wall_clock.properties.per.properties.qos .components.schemas."v0.0.39_qos".properties.limits.properties.max.properties.wall_clock.properties.per.properties.job .components.schemas."v0.0.39_qos".properties.limits.properties.max.properties.jobs.properties.active_jobs.properties.account .components.schemas."v0.0.39_qos".properties.limits.properties.max.properties.jobs.properties.active_jobs.properties.user .components.schemas."v0.0.39_qos".properties.limits.properties.max.properties.jobs.properties.per.properties.account .components.schemas."v0.0.39_qos".properties.limits.properties.max.properties.accruing.properties.per.properties.account .components.schemas."v0.0.39_qos".properties.limits.properties.max.properties.accruing.properties.per.properties.user .components.schemas."v0.0.39_qos".properties.limits.properties.min.properties.priority_threshold |
