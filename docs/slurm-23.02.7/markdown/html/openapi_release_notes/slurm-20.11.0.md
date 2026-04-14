## Slurm 20.11.0

### openapi/dbv0.0.36

#### Initial Implementation of database queries.

### openapi/v0.0.36

#### add plugin

<table class="tchange">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new v0.0.36 openapi plugin</td>
<td class="tdchange"><ul>
<li>clone of existing v0.0.35 openapi plugin.</li>
<li>all paths renamed from v0.0.35 to v0.0.36.</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add error schema

|      |                                     |
|------|-------------------------------------|
| path | .components.schemas."v0.0.36_error" |

#### return array of nodes instead of dictionary

|      |                                              |
|------|----------------------------------------------|
| path | .components.schemas."v0.0.36_nodes_response" |

#### return array of partitions instead of dictionary

|      |                                                   |
|------|---------------------------------------------------|
| path | .components.schemas."v0.0.36_partitions_response" |

#### return array of pings instead of dictionary

|      |                                    |
|------|------------------------------------|
| path | .components.schemas."v0.0.36_ping" |

#### Simplify possible signals for canceling jobs

|      |                                               |
|------|-----------------------------------------------|
| path | .paths."/job/{job_id}".delete.parameters\[1\] |

#### Simplify exclusive for jobs submissions

|      |                                                                   |
|------|-------------------------------------------------------------------|
| path | .components.schemas."v0.0.36_job_properties".properties.exclusive |

#### Simplify nodes for jobs submissions

|      |                                                               |
|------|---------------------------------------------------------------|
| path | .components.schemas."v0.0.36_job_properties".properties.nodes |

#### Change server URL

|          |                                   |
|----------|-----------------------------------|
| previous | .servers\[0\].url=/               |
| new      | .servers\[0\].url=/slurm/v0.0.36/ |

#### Add operationId tag

|             |        |
|-------------|--------|
| parent path | .paths |

#### prepend every schema with v0.0.36\_

|             |                     |
|-------------|---------------------|
| parent path | .components.schemas |

#### add tags openapi and slurm

|          |       |
|----------|-------|
| new path | .tags |

#### add support contact

|          |               |
|----------|---------------|
| new path | .info.contact |

#### populate response from partitions query

|          |                                         |
|----------|-----------------------------------------|
| new path | .components.schemas.partitions_response |

#### rename "node_info" to "nodes_response"

|              |                                    |
|--------------|------------------------------------|
| removed path | .components.schemas.node_info      |
| new path     | .components.schemas.nodes_response |

#### add jobs query response properties

|          |                          |
|----------|--------------------------|
| new path | .components.schemas.diag |

#### define response to diag

|          |                          |
|----------|--------------------------|
| new path | .components.schemas.diag |

#### add job query response properties

|          |                                             |
|----------|---------------------------------------------|
| new path | .components.schemas.job_response_properties |

#### remove "requested_node_by_index"

|              |                                                                                |
|--------------|--------------------------------------------------------------------------------|
| removed path | .components.schemas.job_response_properties.properties.requested_node_by_index |

#### rename "pn_min_tmp_disk" to "minimum_tmp_disk_per_node"

|              |                                                                                  |
|--------------|----------------------------------------------------------------------------------|
| removed path | .components.schemas.job_response_properties.properties.pn_min_tmp_disk           |
| new path     | .components.schemas.job_response_properties.properties.minimum_tmp_disk_per_node |

#### renamed "nodes" to "node_count"

|              |                                                                   |
|--------------|-------------------------------------------------------------------|
| removed path | .components.schemas.job_response_properties.properties.nodes      |
| new path     | .components.schemas.job_response_properties.properties.node_count |

#### add get job responses schema

|          |                                             |
|----------|---------------------------------------------|
| new path | .components.schemas.job_submission_response |

#### use job_submission for job_submit instead of job_properties

|               |                                                               |
|---------------|---------------------------------------------------------------|
| changed field | .paths."/job/submit".requestBody.content."application/json"   |
| changed field | .paths."/job/submit".requestBody.content."application/x-yaml" |
| new path      | .components.schemas.job_submission                            |

#### Set type for "job_properties" schema

|          |                                                            |
|----------|------------------------------------------------------------|
| new path | .components.schemas.v0.0.36_job_properties.properties.type |

#### add security bearer

|          |           |
|----------|-----------|
| new path | .security |
