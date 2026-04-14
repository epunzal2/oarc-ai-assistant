## Slurm 20.11.1

## 

### openapi/v0.0.36

#### Correct name for partition field

|               |                                                                        |
|---------------|------------------------------------------------------------------------|
| previous path | .components.schemas."v0.0.36_partition".properties."min nodes per job" |
| new path      | .components.schemas."v0.0.36_partition".properties."min_nodes_per_job" |

#### Add node comment field

|          |                                                       |
|----------|-------------------------------------------------------|
| new path | .components.schemas."v0.0.36_node".properties.comment |
