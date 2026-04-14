## Slurm 20.11.5

## 

### openapi/dbv0.0.36

#### Mark job environment as required

|          |                                                       |
|----------|-------------------------------------------------------|
| new path | .components.schemas."v0.0.36_job_properties".required |

#### Add state flags

|          |                                                                             |
|----------|-----------------------------------------------------------------------------|
| new path | .components.schemas."v0.0.37_node".properties.state_flags                   |
| new path | .components.schemas."v0.0.37_node".properties.next_state_after_reboot_flags |

#### Correct description for previous state

|      |                                                                          |
|------|--------------------------------------------------------------------------|
| path | .components.schemas."dbv0.0.36_job".properties.state.properties.previous |
