## Slurm 22.05.0

### openapi/dbv0.0.38

#### add plugin

<table class="tchange">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new dbv0.0.38 openapi plugin</td>
<td class="tdchange"><ul>
<li>clone of existing dbv0.0.37 openapi plugin</li>
<li>all paths renamed from dbv0.0.37 to dbv0.0.38</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add POST method for /associations

#### 

|          |                                                       |
|----------|-------------------------------------------------------|
| new path | .paths."/associations/".post                          |
| new path | .components.schemas."dbv0.0.38_response_associations" |

#### Correct placement of step TRES

|               |                                                                          |
|---------------|--------------------------------------------------------------------------|
| previous path | .components.schemas."dbv0.0.38_job_step".properties.step.properties.tres |
| new path      | .components.schemas."dbv0.0.38_job_step".properties.tres                 |

#### Add association fields

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."dbv0.0.38_association".properties.is_default</li>
<li>.components.schemas."dbv0.0.38_association".properties.max.tres.group.minutes</li>
<li>.components.schemas."dbv0.0.38_association".properties.max.tres.group.active</li>
<li>.components.schemas."dbv0.0.38_association".properties.max.jobs.active</li>
<li>.components.schemas."dbv0.0.38_association".properties.max.jobs.accruing</li>
<li>.components.schemas."dbv0.0.38_association".properties.max.jobs.total</li>
<li>.components.schemas."dbv0.0.38_association".properties.max.tres.minutes.per.job</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add error response contents

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.paths."/account/{account_name}"[].responses.default[]</li>
<li>.paths."/accounts/"[].responses.default[]</li>
<li>.paths."/association/"[].responses.default[]</li>
<li>.paths."/associations/"[].responses.default[]</li>
<li>.paths."/cluster/{cluster_name}"[].responses.default[]</li>
<li>.paths."/clusters/"[].responses.default[]</li>
<li>.paths."/config/"[].responses.default[]</li>
<li>.paths."/diag/"[].responses.default[]</li>
<li>.paths."/job/{job_id}"[].responses.default[]</li>
<li>.paths."/jobs/"[].responses.default[]</li>
<li>.paths."/qos/{qos_name}/"[].responses.default[]</li>
<li>.paths."/qos/"[].responses.default[]</li>
<li>.paths."/tres/"[].responses.default[]</li>
<li>.paths."/users/"[].responses.default[]</li>
<li>.paths."/user/{user_name}"[].responses.default[]</li>
<li>.paths."/wckeys/"[].responses.default[]</li>
<li>.paths."/wckey/{wckey}"[].responses.default[]</li>
<li>.components.schemas."dbv0.0.38_meta"</li>
</ul></td>
</tr>
</tbody>
</table>

#### Move incorrectly named field

|          |                                                                                        |
|----------|----------------------------------------------------------------------------------------|
| old path | .components.schemas."dbv0.0.38_qos".properties.limits.max.jobs.per.account             |
| new path | .components.schemas."dbv0.0.38_qos".properties.limits.max.jobs.active_jobs.per.account |

#### Move incorrectly named field

|  |  |
|----|----|
| old path | .components.schemas."dbv0.0.38_qos".properties.limits.properties.max.properties.jobs.properties.per.properties.user |
| new path | .components.schemas."dbv0.0.38_qos".properties.limits.properties.max.properties.jobs.properties.active_jobs.properties.per.properties.user |

#### Add QOS fields

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."dbv0.0.38_qos".properties.limits.properties.factor</li>
<li>.components.schemas."dbv0.0.38_qos".properties.limits.properties.max.properties.accruing.properties.per.properties.account</li>
<li>.components.schemas."dbv0.0.38_qos".properties.limits.properties.max.properties.accruing.properties.per.properties.user</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add diag fields

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."v0.0.38_diag".bf_table_size</li>
<li>.components.schemas."v0.0.38_diag".bf_table_size_mean</li>
</ul></td>
</tr>
</tbody>
</table>

#### Split up token and user

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">change array values</td>
<td colspan="2" class="tdchange"><ul>
<li>.security</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add meta entry

<table class="tchange">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">field added</td>
<td class="tdchange"><ul>
<li>.components.schemas."dbv0.0.38_diag".properties.meta</li>
<li>.components.schemas."dbv0.0.38_account_info".properties.meta</li>
<li>.components.schemas."dbv0.0.38_response_account_delete".properties.meta</li>
<li>.components.schemas."dbv0.0.38_response_wckey_add".properties.meta</li>
<li>.components.schemas."dbv0.0.38_wckey_info".properties.meta</li>
<li>.components.schemas."dbv0.0.38_response_wckey_delete".properties.meta</li>
<li>.components.schemas."dbv0.0.38_response_cluster_add".properties.meta</li>
<li>.components.schemas."dbv0.0.38_response_cluster_delete".properties.meta</li>
<li>.components.schemas."dbv0.0.38_response_user_update".properties.meta</li>
<li>.components.schemas."dbv0.0.38_user_info".properties.meta</li>
<li>.components.schemas."dbv0.0.38_response_user_delete".properties.meta</li>
<li>.components.schemas."dbv0.0.38_response_association_delete".properties.meta</li>
<li>.components.schemas."dbv0.0.38_associations_info".properties.meta</li>
<li>.components.schemas."dbv0.0.38_qos_info".properties.meta</li>
<li>.components.schemas."dbv0.0.38_response_qos_delete".properties.meta</li>
<li>.components.schemas."dbv0.0.38_response_associations".properties.meta</li>
<li>.components.schemas."dbv0.0.38_response_tres".properties.meta</li>
<li>.components.schemas."dbv0.0.38_tres_info".properties.meta</li>
<li>.components.schemas."dbv0.0.38_job_info".properties.meta</li>
<li>.components.schemas."dbv0.0.38_config_info".properties.meta</li>
<li>.components.schemas."dbv0.0.38_account_response".properties.meta</li>
<li>.components.schemas."dbv0.0.38_config_response".properties.meta</li>
<li>.components.schemas."dbv0.0.38_errors"</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add missing response field

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."dbv0.0.38_response_association_delete".properties.removed_associations</li>
<li>.components.schemas."dbv0.0.38_error".properties.error_number</li>
<li>.components.schemas."dbv0.0.38_error".properties.source</li>
<li>.components.schemas."dbv0.0.38_error".properties.description</li>
<li>.components.schemas."/clusters/".properties.post.properties.requestBody</li>
<li>.components.schemas."dbv0.0.38_clusters_properties"</li>
</ul></td>
</tr>
</tbody>
</table>

#### Switch field from object to array

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">modified field</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."dbv0.0.38_user".properties.associations</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add missing field

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new field</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."dbv0.0.38_qos".properties.limits.properties.max.properties.tres.properties.minutes.properties.per.properties.qos</li>
<li>.components.schemas."dbv0.0.38_qos".properties.name</li>
</ul></td>
</tr>
</tbody>
</table>

#### Correct field type to reference

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">modified field</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."dbv0.0.38_config_info".properties.tres</li>
<li>.components.schemas."dbv0.0.38".properties.het.properties.job_id</li>
<li>.components.schemas."dbv0.0.38".properties.het.properties.job_offset</li>
<li>.components.schemas."dbv0.0.38_job_step".properties.task</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add requestBody field and associated schema

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."dbv0.0.38_update_users"</li>
<li>.paths."/users/".post.requestBody'</li>
<li>.components.schemas."dbv0.0.38_update_accounts"</li>
<li>.paths."/accounts/".post.requestBody'</li>
</ul></td>
</tr>
</tbody>
</table>

#### Correct parameter styles to "form"

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">modified fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.paths."/job/{job_id}"[].get.parameters[]|select(.name="job_id)"</li>
</ul></td>
</tr>
</tbody>
</table>

#### Change operationId naming schema to include url path

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">modified fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.paths[][].operationId</li>
</ul></td>
</tr>
</tbody>
</table>

#### Fix issue where association's QOS list consisted of IDs instead of names

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">modified fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."dbv0.0.38_association".properties.qos</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add POST method for /qos

|            |                                              |
|------------|----------------------------------------------|
| new method | .paths."/qos/".post                          |
| new path   | .components.schemas."dbv0.0.38_response_qos" |
| new path   | .components.schemas."dbv0.0.38_update_qos"   |

#### Move response fields in dbv0.0.37_diag under "statistics"

new parent field

- .components.schemas."dbv0.0.38_diag".properties.statistics

subordinated fields

- .components.schemas."dbv0.0.38_diag".properties.time_start
- .components.schemas."dbv0.0.38_diag".properties.rollups
- .components.schemas."dbv0.0.38_diag".properties.RPCs
- .components.schemas."dbv0.0.38_diag".properties.users

#### Allow strings for JobIds instead of only numerical JobIds.

<table class="tchange">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">Change job_id parameter to string</td>
<td class="tdchange"><ul>
<li>.paths."/job/{job_id}".get.parameters[].schema</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add with_deleted input parameter to GET /user, /users

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">New parameter</td>
<td colspan="2" class="tdchange"><ul>
<li>.paths."/user/{user_name}".get.parameters[] | select(.name=="with_deleted")</li>
<li>.paths."/users/".get.parameters[] | select(.name=="with_deleted")</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add deleted flag to /user, /users output

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">New property</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."dbv0.0.38_user".properties.flags</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add with_deleted input parameter to GET /qos

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">New parameter</td>
<td colspan="2" class="tdchange"><ul>
<li>.paths."/qos/".get.parameters[] | select(.name=="with_deleted")</li>
<li>.paths."/qos/{qos_name}".get.parameters[] | select(.name=="with_deleted")</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add with_deleted input parameter to GET /account, /accounts

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">New parameter</td>
<td colspan="2" class="tdchange"><ul>
<li>.paths."/account/{account_name}".get.parameters[] | select(.name=="with_deleted")</li>
<li>.paths."/accounts/".get.parameters[] | select(.name=="with_deleted")</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add container field to job description

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."dbv0.0.38_job".properties.container</li>
</ul></td>
</tr>
</tbody>
</table>

#### Enforce limit to only DELETE or GET a single association instead of using required parameters.

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">changed value</td>
<td colspan="2" class="tdchange"><ul>
<li>.paths."/association/".get.parameters[].required</li>
<li>.paths."/association/".delete.parameters[].required</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add filter parameters to GET /associations

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new method</td>
<td colspan="2" class="tdchange"><ul>
<li>.paths."/associations/".get.parameters</li>
</ul></td>
</tr>
</tbody>
</table>

### openapi/dbv0.0.36

#### Deprecation notice

The dbv0.0.36 plugin has now been marked as deprecated.

### openapi/v0.0.38

#### add plugin

<table class="tchange">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new v0.0.38 openapi plugin</td>
<td class="tdchange"><ul>
<li>clone of existing v0.0.37 openapi plugin</li>
<li>all paths renamed from v0.0.37 to v0.0.38</li>
</ul></td>
</tr>
</tbody>
</table>

#### Allow strings for JobIds instead of only numerical JobIds.

<table class="tchange">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">Change job_id parameter to string</td>
<td class="tdchange"><ul>
<li>.paths."/job/{job_id}".get.parameters[].schema</li>
<li>.paths."/job/{job_id}".post.parameters[].schema</li>
<li>.paths."/job/{job_id}".delete.parameters[].schema</li>
</ul></td>
</tr>
</tbody>
</table>

#### Correct multiple type mistakes

#### 

|  |  |
|----|----|
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.array_job_id |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.array_task_id |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.array_max_tasks |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.association_id |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.billable_tres |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.deadline |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.delay_boot |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.derived_exit_code |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.group_id |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.job_id |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.last_sched_evaluation |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.max_cpus |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.max_nodes |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.nice |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.tasks_per_core |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.tasks_per_socket |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.tasks_per_board |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.cpus |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.node_count |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.tasks |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.het_job_id |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.het_job_offset |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.memory_per_node |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.memory_per_cpu |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.minimum_cpus_per_node |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.minimum_tmp_disk_per_node |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.priority |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.restart_cnt |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.sockets_per_board |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.sockets_per_node |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.time_limit |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.time_minimum |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.threads_per_core |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.user_id |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.allocated_nodes |
| modified entry | .components.schemas."v0.0.38_job_response_properties".properties.cpus |

#### Fix errant space after JOB_CPUS_SET flag.

<table class="tchange">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">Fix response.</td>
<td class="tdchange"><ul>
<li>.components.schemas."v0.0.37_job_response_properties".properties.flags</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add new /licenses endpoint

<table class="tchange">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">add</td>
<td class="tdchange"><ul>
<li>.components.schemas."v0.0.38_license"</li>
<li>.components.schemas."v0.0.38_licenses"</li>
<li>.paths."/slurm/v0.0.38/licenses"</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add meta entry

<table class="tchange">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">field added</td>
<td class="tdchange"><ul>
<li>.components.schemas."v0.0.38_diag".properties.meta</li>
<li>.components.schemas."v0.0.38_pings".properties.meta</li>
<li>.components.schemas."v0.0.38_partitions_response".properties.meta</li>
<li>.components.schemas."v0.0.38_reservations_response".properties.meta</li>
<li>.components.schemas."v0.0.38_job_submission_response".properties.meta</li>
<li>.components.schemas."v0.0.38_jobs_response".properties.meta</li>
<li>.components.schemas."v0.0.38_nodes_response".properties.meta</li>
<li>.components.schemas."v0.0.38_errors"</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add error response contents

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.paths."/diag/"[].responses.default[]</li>
<li>.paths."/ping/"[].responses.default[]</li>
<li>.paths."/jobs/"[].responses.default[]</li>
<li>.paths."/job/{job_id}"[].responses.default[]</li>
<li>.paths."/job/submit"[].responses.default[]</li>
<li>.paths."/nodes/"[].responses.default[]</li>
<li>.paths."/node/{node_name}"[].responses.default[]</li>
<li>.paths."/partitions/"[].responses.default[]</li>
<li>.paths."/partition/{partition_name}"[].responses.default[]</li>
<li>.paths."/reservations/"[].responses.default[]</li>
<li>.paths."/reservation/{reservation_name}"[].responses.default[]</li>
</ul></td>
</tr>
</tbody>
</table>

#### Rename errno to error_number

<table class="tchange">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">rename</td>
<td class="tdchange"><ul>
<li>.components.schemas."dbv0.0.38_error".properties.errnum</li>
<li>.components.schemas."dbv0.0.38_error".properties.error_number</li>
</ul></td>
</tr>
</tbody>
</table>

#### Correct parameter styles to "form"

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">modified fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.paths."/jobs/"[].parameters[]|select(.name="update_type)"</li>
<li>.paths."/job/{job_id}"[].get.parameters[]|select(.name="job_id)"</li>
<li>.paths."/job/{job_id}"[].post.parameters[]|select(.name="job_id)"</li>
<li>.paths."/nodes/"[].get.parameters[]|select(.name="update_time)"</li>
<li>.paths."/node/{node_name}"[].get.parameters[]|select(.name="node_name)"</li>
<li>.paths."/partitions/"[].get.parameters[]|select(.name="update_time)"</li>
<li>.paths."/partition/{partition_name}"[].get.parameters[]|select(.name="partition_name)"</li>
<li>.paths."/partition/{partition_name}"[].get.parameters[]|select(.name="update_time)"</li>
<li>.paths."/reservations/"[].get.parameters[]|select(.name="reservation_name)"</li>
<li>.paths."/reservations/"[].get.parameters[]|select(.name="update_time)"</li>
</ul></td>
</tr>
</tbody>
</table>

#### Change operationId naming schema to include url path

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">modified fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.paths[][].operationId</li>
</ul></td>
</tr>
</tbody>
</table>

#### Response changed to move "cores" into "sockets" to differentiate which cores and sockets are allocated. Changed from named dictionary of node names to array containing objects with nodename set.

<table class="tchange">
<colgroup>
<col style="width: 50%" />
<col style="width: 50%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">Updated response.</td>
<td class="tdchange"><ul>
<li>.components.schemas."v0.0.38_job_resources".properties.allocated_nodes</li>
<li>.components.schemas."v0.0.38_node_allocation"</li>
</ul></td>
</tr>
</tbody>
</table>

#### New fields add to diag endpoint

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."v0.0.38_diag_rpcm".rpcs_by_message_type</li>
<li>.components.schemas."v0.0.38_diag_rpcm".rpcs_by_user</li>
<li>.components.schemas."v0.0.38_diag_rpcm"</li>
<li>.components.schemas."v0.0.38_diag_rpcu"</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add container field to job description

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."v0.0.38_job_response_properties".properties.container</li>
<li>.components.schemas."v0.0.38_job_properties".properties.container</li>
</ul></td>
</tr>
</tbody>
</table>

#### Add method to delete associations using filters

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new method</td>
<td colspan="2" class="tdchange"><ul>
<li>.paths."/associations/".delete</li>
</ul></td>
</tr>
</tbody>
</table>

#### Rename response schema entry

|               |                                                              |
|---------------|--------------------------------------------------------------|
| previous path | .components.schemas."dbv0.0.38_response_association_delete"  |
| new path      | .components.schemas."dbv0.0.38_response_associations_delete" |

### openapi/v0.0.36

#### Deprecation notice

The v0.0.36 plugin has now been marked as deprecated.

### openapi/v0.0.35

#### Removal notice

The v0.0.35 plugin has now been removed.
