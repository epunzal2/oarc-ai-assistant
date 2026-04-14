## Slurm 21.08.0

All of the OpenAPI plugins have moved from "src/slurmrestd/plugins/openapi/" to
"src/plugins/openapi/".

### openapi/v0.0.35

#### Deprecation notice

The v0.0.35 plugin has now been deprecated.

### openapi/dbv0.0.37

#### add plugin

<table class="tchange">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new dbv0.0.37 openapi plugin</td>
<td class="tdchange"><ul>
<li>clone of existing dbv0.0.36 openapi plugin</li>
<li>all paths renamed from v0.0.36 to v0.0.37</li>
</ul></td>
</tr>
</tbody>
</table>

#### rename previous -\> reason

|               |                                                               |
|---------------|---------------------------------------------------------------|
| previous path | .components.schemas."dbv0.0.37_job".properties.state.previous |
| new path      | .components.schemas."dbv0.0.37_job".properties.state.reason   |

### openapi/v0.0.37

#### add plugin

<table class="tchange">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new v0.0.37 openapi plugin</td>
<td class="tdchange"><ul>
<li>clone of existing v0.0.36 openapi plugin</li>
<li>all paths renamed from v0.0.36 to v0.0.37</li>
</ul></td>
</tr>
</tbody>
</table>

#### rename standard_in -\> standard_input

|               |                                                                                 |
|---------------|---------------------------------------------------------------------------------|
| previous path | .components.schemas."v0.0.37_job_response_properties".properties.standard_in    |
| new path      | .components.schemas."v0.0.37_job_response_properties".properties.standard_input |

#### rename standard_out -\> standard_output

|               |                                                                                  |
|---------------|----------------------------------------------------------------------------------|
| previous path | .components.schemas."v0.0.37_job_response_properties".properties.standard_out    |
| new path      | .components.schemas."v0.0.37_job_response_properties".properties.standard_output |

#### Add update_time field to Jobs query to allow clients to only get jobs list based on change timestamp.

|          |                                     |
|----------|-------------------------------------|
| new path | .paths."/jobs/".get.parameters\[0\] |

#### add api to fetch reservation(s) info

|            |                                           |
|------------|-------------------------------------------|
| added path | .paths."/reservations/"                   |
| added path | .paths."/reservation/{reservation_name}"  |
| added path | .components.schemas."v0.0.37_reservation" |

#### Mark job environment as required

|          |                                                       |
|----------|-------------------------------------------------------|
| new path | .components.schemas."v0.0.37_job_properties".required |

#### Correct preemption_mode type to list of strings

|             |                                                                    |
|-------------|--------------------------------------------------------------------|
| modify path | .components.schemas."v0.0.37_partition".properties.preemption_mode |

#### Set UNIX timestamps to int64 instead of string

|             |                                                                                |
|-------------|--------------------------------------------------------------------------------|
| modify path | .components.schemas."v0.0.37_job_response_properties".properties.accrue_time   |
| modify path | .components.schemas."v0.0.37_job_response_properties".properties.eligible_time |
| modify path | .components.schemas."v0.0.37_job_response_properties".properties.end_time      |
| modify path | .components.schemas."v0.0.37_job_response_properties".properties.preempt_time  |
| modify path | .components.schemas."v0.0.37_job_response_properties".properties.pre_sus_time  |
| modify path | .components.schemas."v0.0.37_job_response_properties".properties.resize_time   |

#### Add new fields to node properties

|          |                                                             |
|----------|-------------------------------------------------------------|
| add path | .components.schemas."v0.0.37_node".properties.tres_used     |
| add path | .components.schemas."v0.0.37_node".properties.tres_weighted |
| add path | .components.schemas."v0.0.37_node".properties.alloc_cpus    |
| add path | .components.schemas."v0.0.37_node".properties.idle_cpus     |
| add path | .components.schemas."v0.0.37_node".properties.alloc_memory  |
| add path | .components.schemas."v0.0.37_node".properties.partitions    |

#### replace nodes_online with state in /partitions endpoint

#### 

|              |                                                                |
|--------------|----------------------------------------------------------------|
| removed path | .components.schemas."v0.0.37_partitions_response".nodes_online |
| added path   | .components.schemas."v0.0.37_partitions_response".state        |

#### Add POST method for /associations

#### 

|          |                                                       |
|----------|-------------------------------------------------------|
| new path | .paths."/associations/".post                          |
| new path | .components.schemas."dbv0.0.37_response_associations" |
