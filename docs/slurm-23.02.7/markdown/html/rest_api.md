# Slurm Rest API

API to access and control Slurm DB. More information: <https://www.schedmd.com/> Contact Info:
[sales@schedmd.com](sales@schedmd.com) Version: dbv0.0.39 BasePath: Apache 2.0
https://www.apache.org/licenses/LICENSE-2.0.html

## Access

1.  APIKey KeyParamName:X-SLURM-USER-NAME KeyInQuery:false KeyInHeader:true
2.  APIKey KeyParamName:X-SLURM-USER-TOKEN KeyInQuery:false KeyInHeader:true
3.  HTTP Basic Authentication

## <span id="__Methods">Methods</span>

\[ Jump to [Models](#__Models) \]

### Table of Contents

#### [Openapi](#Openapi)

- [<span class="http-method">`get`</span>` /openapi`](#openapiGet)
- [<span class="http-method">`get`</span>` /openapi.json`](#openapiJsonGet)
- [<span class="http-method">`get`</span>` /openapi/v3`](#openapiV3Get)
- [<span class="http-method">`get`</span>` /openapi.yaml`](#openapiYamlGet)

#### [Slurm](#Slurm)

- [<span class="http-method">`delete`</span>` /slurm/v0.0.39/job/{job_id}`](#slurmV0039CancelJob)
- [<span class="http-method">`delete`</span>` /slurm/v0.0.39/node/{node_name}`](#slurmV0039DeleteNode)
- [<span class="http-method">`get`</span>` /slurm/v0.0.39/diag`](#slurmV0039Diag)
- [<span class="http-method">`get`</span>` /slurm/v0.0.39/job/{job_id}`](#slurmV0039GetJob)
- [<span class="http-method">`get`</span>` /slurm/v0.0.39/jobs`](#slurmV0039GetJobs)
- [<span class="http-method">`get`</span>` /slurm/v0.0.39/node/{node_name}`](#slurmV0039GetNode)
- [<span class="http-method">`get`</span>` /slurm/v0.0.39/nodes`](#slurmV0039GetNodes)
- [<span class="http-method">`get`</span>` /slurm/v0.0.39/partition/{partition_name}`](#slurmV0039GetPartition)
- [<span class="http-method">`get`</span>` /slurm/v0.0.39/partitions`](#slurmV0039GetPartitions)
- [<span class="http-method">`get`</span>` /slurm/v0.0.39/reservation/{reservation_name}`](#slurmV0039GetReservation)
- [<span class="http-method">`get`</span>` /slurm/v0.0.39/reservations`](#slurmV0039GetReservations)
- [<span class="http-method">`get`</span>` /slurm/v0.0.39/ping`](#slurmV0039Ping)
- [<span class="http-method">`get`</span>` /slurm/v0.0.39/licenses`](#slurmV0039SlurmctldGetLicenses)
- [<span class="http-method">`post`</span>` /slurm/v0.0.39/job/submit`](#slurmV0039SubmitJob)
- [<span class="http-method">`post`</span>` /slurm/v0.0.39/job/{job_id}`](#slurmV0039UpdateJob)
- [<span class="http-method">`post`</span>` /slurm/v0.0.39/node/{node_name}`](#slurmV0039UpdateNode)
- [<span class="http-method">`post`</span>` /slurmdb/v0.0.39/clusters`](#slurmdbV0039AddClusters)
- [<span class="http-method">`post`</span>` /slurmdb/v0.0.39/wckeys`](#slurmdbV0039AddWckeys)
- [<span class="http-method">`delete`</span>` /slurmdb/v0.0.39/account/{account_name}`](#slurmdbV0039DeleteAccount)
- [<span class="http-method">`delete`</span>` /slurmdb/v0.0.39/association`](#slurmdbV0039DeleteAssociation)
- [<span class="http-method">`delete`</span>` /slurmdb/v0.0.39/associations`](#slurmdbV0039DeleteAssociations)
- [<span class="http-method">`delete`</span>` /slurmdb/v0.0.39/cluster/{cluster_name}`](#slurmdbV0039DeleteCluster)
- [<span class="http-method">`delete`</span>` /slurmdb/v0.0.39/qos/{qos_name}`](#slurmdbV0039DeleteQos)
- [<span class="http-method">`delete`</span>` /slurmdb/v0.0.39/user/{user_name}`](#slurmdbV0039DeleteUser)
- [<span class="http-method">`delete`</span>` /slurmdb/v0.0.39/wckey/{wckey}`](#slurmdbV0039DeleteWckey)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/diag`](#slurmdbV0039Diag)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/account/{account_name}`](#slurmdbV0039GetAccount)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/accounts`](#slurmdbV0039GetAccounts)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/association`](#slurmdbV0039GetAssociation)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/associations`](#slurmdbV0039GetAssociations)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/cluster/{cluster_name}`](#slurmdbV0039GetCluster)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/clusters`](#slurmdbV0039GetClusters)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/config`](#slurmdbV0039GetConfig)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/job/{job_id}`](#slurmdbV0039GetJob)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/jobs`](#slurmdbV0039GetJobs)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/qos`](#slurmdbV0039GetQos)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/qos/{qos_name}`](#slurmdbV0039GetSingleQos)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/tres`](#slurmdbV0039GetTres)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/user/{user_name}`](#slurmdbV0039GetUser)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/users`](#slurmdbV0039GetUsers)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/wckey/{wckey}`](#slurmdbV0039GetWckey)
- [<span class="http-method">`get`</span>` /slurmdb/v0.0.39/wckeys`](#slurmdbV0039GetWckeys)
- [<span class="http-method">`post`</span>` /slurmdb/v0.0.39/config`](#slurmdbV0039SetConfig)
- [<span class="http-method">`post`</span>` /slurmdb/v0.0.39/accounts`](#slurmdbV0039UpdateAccounts)
- [<span class="http-method">`post`</span>` /slurmdb/v0.0.39/associations`](#slurmdbV0039UpdateAssociations)
- [<span class="http-method">`post`</span>` /slurmdb/v0.0.39/qos`](#slurmdbV0039UpdateQos)
- [<span class="http-method">`post`</span>` /slurmdb/v0.0.39/tres`](#slurmdbV0039UpdateTres)
- [<span class="http-method">`post`</span>` /slurmdb/v0.0.39/users`](#slurmdbV0039UpdateUsers)

# <span id="Openapi">Openapi</span>

<span id="openapiGet"></span> <span id="openapiGet"></span> <a href="#__Methods" class="up">Up</a>

``` get
get /openapi
```

Retrieve OpenAPI Specification (<span class="nickname">openapiGet</span>)

### Responses

#### 200

OpenAPI Specification [](rest_api.md)

----------------------------------------------------------------------------------------------------

<span id="openapiJsonGet"></span> <span id="openapiJsonGet"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /openapi.json
```

Retrieve OpenAPI Specification (<span class="nickname">openapiJsonGet</span>)

### Responses

#### 200

OpenAPI Specification [](rest_api.md)

----------------------------------------------------------------------------------------------------

<span id="openapiV3Get"></span> <span id="openapiV3Get"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /openapi/v3
```

Retrieve OpenAPI Specification (<span class="nickname">openapiV3Get</span>)

### Responses

#### 200

OpenAPI Specification [](rest_api.md)

----------------------------------------------------------------------------------------------------

<span id="openapiYamlGet"></span> <span id="openapiYamlGet"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /openapi.yaml
```

Retrieve OpenAPI Specification (<span class="nickname">openapiYamlGet</span>)

### Responses

#### 200

OpenAPI Specification [](rest_api.md)

----------------------------------------------------------------------------------------------------

# <span id="Slurm">Slurm</span>

<span id="slurmV0039CancelJob"></span> <span id="slurmV0039CancelJob"></span>
<a href="#__Methods" class="up">Up</a>

``` delete
delete /slurm/v0.0.39/job/{job_id}
```

cancel or signal job (<span class="nickname">slurmV0039CancelJob</span>)

### Path parameters

job_id (required) <span class="param-type">Path Parameter</span> — Slurm Job ID default: null

### Query parameters

signal (optional) <span class="param-type">Query Parameter</span> — signal to send to job default:
null

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

job cancelled or sent signal [status](#status)

#### default

Job cancel request failed [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039DeleteNode"></span> <span id="slurmV0039DeleteNode"></span>
<a href="#__Methods" class="up">Up</a>

``` delete
delete /slurm/v0.0.39/node/{node_name}
```

delete node (<span class="nickname">slurmV0039DeleteNode</span>)

### Path parameters

node_name (required) <span class="param-type">Path Parameter</span> — Slurm Node Name default: null

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

node deleted [status](#status)

#### default

node delete request failed [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039Diag"></span> <span id="slurmV0039Diag"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurm/v0.0.39/diag
```

get diagnostics (<span class="nickname">slurmV0039Diag</span>)

### Return type

[v0.0.39_diag](#v0.0.39_diag)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ],
  "statistics" : {
    "schedule_cycle_per_minute" : 1,
    "req_time_start" : 1,
    "jobs_running" : 6,
    "bf_last_backfilled_jobs" : 6,
    "rpcs_by_message_type" : [ {
      "average_time" : 3,
      "type_id" : 7,
      "count" : 3,
      "message_type" : "message_type",
      "total_time" : 7
    }, {
      "average_time" : 3,
      "type_id" : 7,
      "count" : 3,
      "message_type" : "message_type",
      "total_time" : 7
    } ],
    "bf_last_depth" : 6,
    "bf_backfilled_het_jobs" : 3,
    "bf_backfilled_jobs" : 9,
    "rpcs_by_user" : [ {
      "average_time" : 4,
      "user_id" : 5,
      "count" : 3,
      "total_time" : 0,
      "user" : "user"
    }, {
      "average_time" : 4,
      "user_id" : 5,
      "count" : 3,
      "total_time" : 0,
      "user" : "user"
    } ],
    "bf_table_size" : 0,
    "bf_depth_sum" : 3,
    "bf_cycle_mean" : 1,
    "job_states_ts" : 8,
    "bf_queue_len" : 0,
    "jobs_started" : 1,
    "schedule_cycle_max" : 2,
    "server_thread_count" : 5,
    "dbd_agent_queue_size" : 9,
    "bf_table_size_mean" : 4,
    "jobs_pending" : 9,
    "agent_count" : 2,
    "bf_queue_len_sum" : 6,
    "bf_cycle_sum" : 6,
    "bf_cycle_last" : 5,
    "parts_packed" : 0,
    "agent_thread_count" : 7,
    "jobs_completed" : 4,
    "bf_depth_mean" : 2,
    "bf_active" : true,
    "bf_depth_mean_try" : 6,
    "bf_depth_try_sum" : 7,
    "schedule_cycle_mean" : 1,
    "agent_queue_size" : 5,
    "jobs_failed" : 9,
    "gettimeofday_latency" : 3,
    "bf_last_depth_try" : 3,
    "req_time" : 6,
    "bf_cycle_counter" : 6,
    "schedule_queue_length" : 6,
    "bf_queue_len_mean" : 7,
    "schedule_cycle_total" : 7,
    "bf_when_last_cycle" : 8,
    "schedule_cycle_last" : 4,
    "jobs_canceled" : 5,
    "jobs_submitted" : 7,
    "schedule_cycle_mean_depth" : 1
  }
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

diagnostic results [v0.0.39_diag](#v0.0.39_diag)

#### default

unable to request ping test [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039GetJob"></span> <span id="slurmV0039GetJob"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurm/v0.0.39/job/{job_id}
```

get job info (<span class="nickname">slurmV0039GetJob</span>)

### Path parameters

job_id (required) <span class="param-type">Path Parameter</span> — Slurm JobID default: null

### Return type

[v0.0.39_jobs_response](#v0.0.39_jobs_response)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "jobs" : [ {
    "container" : "container",
    "cluster" : "cluster",
    "time_minimum" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "memory_per_tres" : "memory_per_tres",
    "scheduled_nodes" : "scheduled_nodes",
    "minimum_switches" : 4,
    "qos" : "qos",
    "resize_time" : 5,
    "eligible_time" : 7,
    "exclusive" : [ "true", "true" ],
    "cpus_per_tres" : "cpus_per_tres",
    "preemptable_time" : 7,
    "tasks" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "system_comment" : "system_comment",
    "federation_siblings_active" : "federation_siblings_active",
    "tasks_per_tres" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "tasks_per_core" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "accrue_time" : 0,
    "dependency" : "dependency",
    "group_name" : "group_name",
    "profile" : [ "NOT_SET", "NOT_SET" ],
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "tres_per_job" : "tres_per_job",
    "failed_node" : "failed_node",
    "derived_exit_code" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "maximum_switch_wait_time" : 3,
    "core_spec" : 1,
    "mcs_label" : "mcs_label",
    "required_nodes" : "required_nodes",
    "tres_bind" : "tres_bind",
    "user_id" : 6,
    "selinux_context" : "selinux_context",
    "exit_code" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "federation_origin" : "federation_origin",
    "container_id" : "container_id",
    "shared" : [ "none", "none" ],
    "tasks_per_board" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "user_name" : "user_name",
    "flags" : [ "KILL_INVALID_DEPENDENCY", "KILL_INVALID_DEPENDENCY" ],
    "standard_input" : "standard_input",
    "admin_comment" : "admin_comment",
    "cores_per_socket" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "job_state" : "job_state",
    "tasks_per_node" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "current_working_directory" : "current_working_directory",
    "standard_error" : "standard_error",
    "array_job_id" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "cluster_features" : "cluster_features",
    "partition" : "partition",
    "threads_per_core" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "tres_alloc_str" : "tres_alloc_str",
    "memory_per_cpu" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "cpu_frequency_minimum" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "node_count" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "power" : {
      "flags" : [ "EQUAL_POWER", "EQUAL_POWER" ]
    },
    "deadline" : 2,
    "mail_type" : [ "BEGIN", "BEGIN" ],
    "memory_per_node" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "state_reason" : "state_reason",
    "het_job_offset" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "end_time" : 9,
    "sockets_per_board" : 9,
    "nice" : 1,
    "last_sched_evaluation" : 1,
    "tres_per_node" : "tres_per_node",
    "burst_buffer" : "burst_buffer",
    "licenses" : "licenses",
    "excluded_nodes" : "excluded_nodes",
    "array_max_tasks" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "het_job_id" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "sockets_per_node" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "prefer" : "prefer",
    "time_limit" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "minimum_cpus_per_node" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "tasks_per_socket" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "batch_host" : "batch_host",
    "max_cpus" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "job_size_str" : [ "job_size_str", "job_size_str" ],
    "hold" : true,
    "cpu_frequency_maximum" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "features" : "features",
    "het_job_id_set" : "het_job_id_set",
    "state_description" : "state_description",
    "show_flags" : [ "ALL", "ALL" ],
    "array_task_id" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "minimum_tmp_disk_per_node" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "tres_req_str" : "tres_req_str",
    "burst_buffer_state" : "burst_buffer_state",
    "cron" : "cron",
    "allocating_node" : "allocating_node",
    "tres_per_socket" : "tres_per_socket",
    "array_task_string" : "array_task_string",
    "submit_time" : 8,
    "oversubscribe" : true,
    "wckey" : "wckey",
    "max_nodes" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "batch_flag" : true,
    "start_time" : 6,
    "name" : "name",
    "preempt_time" : 6,
    "contiguous" : true,
    "job_resources" : {
      "nodes" : "nodes",
      "allocated_nodes" : [ "", "" ],
      "allocated_cpus" : 7,
      "allocated_hosts" : 1,
      "allocated_cores" : 4
    },
    "billable_tres" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "federation_siblings_viable" : "federation_siblings_viable",
    "cpus_per_task" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "batch_features" : "batch_features",
    "thread_spec" : 5,
    "cpu_frequency_governor" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "gres_detail" : [ "gres_detail", "gres_detail" ],
    "network" : "network",
    "restart_cnt" : 9,
    "resv_name" : "resv_name",
    "extra" : "extra",
    "delay_boot" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "reboot" : true,
    "cpus" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "standard_output" : "standard_output",
    "pre_sus_time" : 1,
    "suspend_time" : 9,
    "association_id" : 6,
    "command" : "command",
    "tres_freq" : "tres_freq",
    "requeue" : true,
    "tres_per_task" : "tres_per_task",
    "mail_user" : "mail_user",
    "nodes" : "nodes",
    "group_id" : 3,
    "job_id" : 2,
    "comment" : "comment",
    "account" : "account"
  }, {
    "container" : "container",
    "cluster" : "cluster",
    "time_minimum" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "memory_per_tres" : "memory_per_tres",
    "scheduled_nodes" : "scheduled_nodes",
    "minimum_switches" : 4,
    "qos" : "qos",
    "resize_time" : 5,
    "eligible_time" : 7,
    "exclusive" : [ "true", "true" ],
    "cpus_per_tres" : "cpus_per_tres",
    "preemptable_time" : 7,
    "tasks" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "system_comment" : "system_comment",
    "federation_siblings_active" : "federation_siblings_active",
    "tasks_per_tres" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "tasks_per_core" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "accrue_time" : 0,
    "dependency" : "dependency",
    "group_name" : "group_name",
    "profile" : [ "NOT_SET", "NOT_SET" ],
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "tres_per_job" : "tres_per_job",
    "failed_node" : "failed_node",
    "derived_exit_code" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "maximum_switch_wait_time" : 3,
    "core_spec" : 1,
    "mcs_label" : "mcs_label",
    "required_nodes" : "required_nodes",
    "tres_bind" : "tres_bind",
    "user_id" : 6,
    "selinux_context" : "selinux_context",
    "exit_code" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "federation_origin" : "federation_origin",
    "container_id" : "container_id",
    "shared" : [ "none", "none" ],
    "tasks_per_board" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "user_name" : "user_name",
    "flags" : [ "KILL_INVALID_DEPENDENCY", "KILL_INVALID_DEPENDENCY" ],
    "standard_input" : "standard_input",
    "admin_comment" : "admin_comment",
    "cores_per_socket" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "job_state" : "job_state",
    "tasks_per_node" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "current_working_directory" : "current_working_directory",
    "standard_error" : "standard_error",
    "array_job_id" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "cluster_features" : "cluster_features",
    "partition" : "partition",
    "threads_per_core" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "tres_alloc_str" : "tres_alloc_str",
    "memory_per_cpu" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "cpu_frequency_minimum" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "node_count" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "power" : {
      "flags" : [ "EQUAL_POWER", "EQUAL_POWER" ]
    },
    "deadline" : 2,
    "mail_type" : [ "BEGIN", "BEGIN" ],
    "memory_per_node" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "state_reason" : "state_reason",
    "het_job_offset" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "end_time" : 9,
    "sockets_per_board" : 9,
    "nice" : 1,
    "last_sched_evaluation" : 1,
    "tres_per_node" : "tres_per_node",
    "burst_buffer" : "burst_buffer",
    "licenses" : "licenses",
    "excluded_nodes" : "excluded_nodes",
    "array_max_tasks" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "het_job_id" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "sockets_per_node" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "prefer" : "prefer",
    "time_limit" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "minimum_cpus_per_node" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "tasks_per_socket" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "batch_host" : "batch_host",
    "max_cpus" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "job_size_str" : [ "job_size_str", "job_size_str" ],
    "hold" : true,
    "cpu_frequency_maximum" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "features" : "features",
    "het_job_id_set" : "het_job_id_set",
    "state_description" : "state_description",
    "show_flags" : [ "ALL", "ALL" ],
    "array_task_id" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "minimum_tmp_disk_per_node" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "tres_req_str" : "tres_req_str",
    "burst_buffer_state" : "burst_buffer_state",
    "cron" : "cron",
    "allocating_node" : "allocating_node",
    "tres_per_socket" : "tres_per_socket",
    "array_task_string" : "array_task_string",
    "submit_time" : 8,
    "oversubscribe" : true,
    "wckey" : "wckey",
    "max_nodes" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "batch_flag" : true,
    "start_time" : 6,
    "name" : "name",
    "preempt_time" : 6,
    "contiguous" : true,
    "job_resources" : {
      "nodes" : "nodes",
      "allocated_nodes" : [ "", "" ],
      "allocated_cpus" : 7,
      "allocated_hosts" : 1,
      "allocated_cores" : 4
    },
    "billable_tres" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "federation_siblings_viable" : "federation_siblings_viable",
    "cpus_per_task" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "batch_features" : "batch_features",
    "thread_spec" : 5,
    "cpu_frequency_governor" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "gres_detail" : [ "gres_detail", "gres_detail" ],
    "network" : "network",
    "restart_cnt" : 9,
    "resv_name" : "resv_name",
    "extra" : "extra",
    "delay_boot" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "reboot" : true,
    "cpus" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "standard_output" : "standard_output",
    "pre_sus_time" : 1,
    "suspend_time" : 9,
    "association_id" : 6,
    "command" : "command",
    "tres_freq" : "tres_freq",
    "requeue" : true,
    "tres_per_task" : "tres_per_task",
    "mail_user" : "mail_user",
    "nodes" : "nodes",
    "group_id" : 3,
    "job_id" : 2,
    "comment" : "comment",
    "account" : "account"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

job(s) information [v0.0.39_jobs_response](#v0.0.39_jobs_response)

#### default

job matching JobId not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039GetJobs"></span> <span id="slurmV0039GetJobs"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurm/v0.0.39/jobs
```

get list of jobs (<span class="nickname">slurmV0039GetJobs</span>)

### Query parameters

update_time (optional) <span class="param-type">Query Parameter</span> — Filter if changed since
update_time. Use of this parameter can result in faster replies. default: null format: int64

### Return type

[v0.0.39_jobs_response](#v0.0.39_jobs_response)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "jobs" : [ {
    "container" : "container",
    "cluster" : "cluster",
    "time_minimum" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "memory_per_tres" : "memory_per_tres",
    "scheduled_nodes" : "scheduled_nodes",
    "minimum_switches" : 4,
    "qos" : "qos",
    "resize_time" : 5,
    "eligible_time" : 7,
    "exclusive" : [ "true", "true" ],
    "cpus_per_tres" : "cpus_per_tres",
    "preemptable_time" : 7,
    "tasks" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "system_comment" : "system_comment",
    "federation_siblings_active" : "federation_siblings_active",
    "tasks_per_tres" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "tasks_per_core" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "accrue_time" : 0,
    "dependency" : "dependency",
    "group_name" : "group_name",
    "profile" : [ "NOT_SET", "NOT_SET" ],
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "tres_per_job" : "tres_per_job",
    "failed_node" : "failed_node",
    "derived_exit_code" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "maximum_switch_wait_time" : 3,
    "core_spec" : 1,
    "mcs_label" : "mcs_label",
    "required_nodes" : "required_nodes",
    "tres_bind" : "tres_bind",
    "user_id" : 6,
    "selinux_context" : "selinux_context",
    "exit_code" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "federation_origin" : "federation_origin",
    "container_id" : "container_id",
    "shared" : [ "none", "none" ],
    "tasks_per_board" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "user_name" : "user_name",
    "flags" : [ "KILL_INVALID_DEPENDENCY", "KILL_INVALID_DEPENDENCY" ],
    "standard_input" : "standard_input",
    "admin_comment" : "admin_comment",
    "cores_per_socket" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "job_state" : "job_state",
    "tasks_per_node" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "current_working_directory" : "current_working_directory",
    "standard_error" : "standard_error",
    "array_job_id" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "cluster_features" : "cluster_features",
    "partition" : "partition",
    "threads_per_core" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "tres_alloc_str" : "tres_alloc_str",
    "memory_per_cpu" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "cpu_frequency_minimum" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "node_count" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "power" : {
      "flags" : [ "EQUAL_POWER", "EQUAL_POWER" ]
    },
    "deadline" : 2,
    "mail_type" : [ "BEGIN", "BEGIN" ],
    "memory_per_node" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "state_reason" : "state_reason",
    "het_job_offset" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "end_time" : 9,
    "sockets_per_board" : 9,
    "nice" : 1,
    "last_sched_evaluation" : 1,
    "tres_per_node" : "tres_per_node",
    "burst_buffer" : "burst_buffer",
    "licenses" : "licenses",
    "excluded_nodes" : "excluded_nodes",
    "array_max_tasks" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "het_job_id" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "sockets_per_node" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "prefer" : "prefer",
    "time_limit" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "minimum_cpus_per_node" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "tasks_per_socket" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "batch_host" : "batch_host",
    "max_cpus" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "job_size_str" : [ "job_size_str", "job_size_str" ],
    "hold" : true,
    "cpu_frequency_maximum" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "features" : "features",
    "het_job_id_set" : "het_job_id_set",
    "state_description" : "state_description",
    "show_flags" : [ "ALL", "ALL" ],
    "array_task_id" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "minimum_tmp_disk_per_node" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "tres_req_str" : "tres_req_str",
    "burst_buffer_state" : "burst_buffer_state",
    "cron" : "cron",
    "allocating_node" : "allocating_node",
    "tres_per_socket" : "tres_per_socket",
    "array_task_string" : "array_task_string",
    "submit_time" : 8,
    "oversubscribe" : true,
    "wckey" : "wckey",
    "max_nodes" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "batch_flag" : true,
    "start_time" : 6,
    "name" : "name",
    "preempt_time" : 6,
    "contiguous" : true,
    "job_resources" : {
      "nodes" : "nodes",
      "allocated_nodes" : [ "", "" ],
      "allocated_cpus" : 7,
      "allocated_hosts" : 1,
      "allocated_cores" : 4
    },
    "billable_tres" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "federation_siblings_viable" : "federation_siblings_viable",
    "cpus_per_task" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "batch_features" : "batch_features",
    "thread_spec" : 5,
    "cpu_frequency_governor" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "gres_detail" : [ "gres_detail", "gres_detail" ],
    "network" : "network",
    "restart_cnt" : 9,
    "resv_name" : "resv_name",
    "extra" : "extra",
    "delay_boot" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "reboot" : true,
    "cpus" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "standard_output" : "standard_output",
    "pre_sus_time" : 1,
    "suspend_time" : 9,
    "association_id" : 6,
    "command" : "command",
    "tres_freq" : "tres_freq",
    "requeue" : true,
    "tres_per_task" : "tres_per_task",
    "mail_user" : "mail_user",
    "nodes" : "nodes",
    "group_id" : 3,
    "job_id" : 2,
    "comment" : "comment",
    "account" : "account"
  }, {
    "container" : "container",
    "cluster" : "cluster",
    "time_minimum" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "memory_per_tres" : "memory_per_tres",
    "scheduled_nodes" : "scheduled_nodes",
    "minimum_switches" : 4,
    "qos" : "qos",
    "resize_time" : 5,
    "eligible_time" : 7,
    "exclusive" : [ "true", "true" ],
    "cpus_per_tres" : "cpus_per_tres",
    "preemptable_time" : 7,
    "tasks" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "system_comment" : "system_comment",
    "federation_siblings_active" : "federation_siblings_active",
    "tasks_per_tres" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "tasks_per_core" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "accrue_time" : 0,
    "dependency" : "dependency",
    "group_name" : "group_name",
    "profile" : [ "NOT_SET", "NOT_SET" ],
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "tres_per_job" : "tres_per_job",
    "failed_node" : "failed_node",
    "derived_exit_code" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "maximum_switch_wait_time" : 3,
    "core_spec" : 1,
    "mcs_label" : "mcs_label",
    "required_nodes" : "required_nodes",
    "tres_bind" : "tres_bind",
    "user_id" : 6,
    "selinux_context" : "selinux_context",
    "exit_code" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "federation_origin" : "federation_origin",
    "container_id" : "container_id",
    "shared" : [ "none", "none" ],
    "tasks_per_board" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "user_name" : "user_name",
    "flags" : [ "KILL_INVALID_DEPENDENCY", "KILL_INVALID_DEPENDENCY" ],
    "standard_input" : "standard_input",
    "admin_comment" : "admin_comment",
    "cores_per_socket" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "job_state" : "job_state",
    "tasks_per_node" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "current_working_directory" : "current_working_directory",
    "standard_error" : "standard_error",
    "array_job_id" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "cluster_features" : "cluster_features",
    "partition" : "partition",
    "threads_per_core" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "tres_alloc_str" : "tres_alloc_str",
    "memory_per_cpu" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "cpu_frequency_minimum" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "node_count" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "power" : {
      "flags" : [ "EQUAL_POWER", "EQUAL_POWER" ]
    },
    "deadline" : 2,
    "mail_type" : [ "BEGIN", "BEGIN" ],
    "memory_per_node" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "state_reason" : "state_reason",
    "het_job_offset" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "end_time" : 9,
    "sockets_per_board" : 9,
    "nice" : 1,
    "last_sched_evaluation" : 1,
    "tres_per_node" : "tres_per_node",
    "burst_buffer" : "burst_buffer",
    "licenses" : "licenses",
    "excluded_nodes" : "excluded_nodes",
    "array_max_tasks" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "het_job_id" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "sockets_per_node" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "prefer" : "prefer",
    "time_limit" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "minimum_cpus_per_node" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "tasks_per_socket" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "batch_host" : "batch_host",
    "max_cpus" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "job_size_str" : [ "job_size_str", "job_size_str" ],
    "hold" : true,
    "cpu_frequency_maximum" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "features" : "features",
    "het_job_id_set" : "het_job_id_set",
    "state_description" : "state_description",
    "show_flags" : [ "ALL", "ALL" ],
    "array_task_id" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "minimum_tmp_disk_per_node" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "tres_req_str" : "tres_req_str",
    "burst_buffer_state" : "burst_buffer_state",
    "cron" : "cron",
    "allocating_node" : "allocating_node",
    "tres_per_socket" : "tres_per_socket",
    "array_task_string" : "array_task_string",
    "submit_time" : 8,
    "oversubscribe" : true,
    "wckey" : "wckey",
    "max_nodes" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "batch_flag" : true,
    "start_time" : 6,
    "name" : "name",
    "preempt_time" : 6,
    "contiguous" : true,
    "job_resources" : {
      "nodes" : "nodes",
      "allocated_nodes" : [ "", "" ],
      "allocated_cpus" : 7,
      "allocated_hosts" : 1,
      "allocated_cores" : 4
    },
    "billable_tres" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "federation_siblings_viable" : "federation_siblings_viable",
    "cpus_per_task" : {
      "number" : 5,
      "set" : false,
      "infinite" : true
    },
    "batch_features" : "batch_features",
    "thread_spec" : 5,
    "cpu_frequency_governor" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "gres_detail" : [ "gres_detail", "gres_detail" ],
    "network" : "network",
    "restart_cnt" : 9,
    "resv_name" : "resv_name",
    "extra" : "extra",
    "delay_boot" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "reboot" : true,
    "cpus" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "standard_output" : "standard_output",
    "pre_sus_time" : 1,
    "suspend_time" : 9,
    "association_id" : 6,
    "command" : "command",
    "tres_freq" : "tres_freq",
    "requeue" : true,
    "tres_per_task" : "tres_per_task",
    "mail_user" : "mail_user",
    "nodes" : "nodes",
    "group_id" : 3,
    "job_id" : 2,
    "comment" : "comment",
    "account" : "account"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

job(s) information [v0.0.39_jobs_response](#v0.0.39_jobs_response)

#### default

job not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039GetNode"></span> <span id="slurmV0039GetNode"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurm/v0.0.39/node/{node_name}
```

get node info (<span class="nickname">slurmV0039GetNode</span>)

### Path parameters

node_name (required) <span class="param-type">Path Parameter</span> — Slurm Node Name default: null

### Return type

[v0.0.39_nodes_response](#v0.0.39_nodes_response)

### Example data

Content-Type: application/json

``` example
{
  "nodes" : [ {
    "reason" : "reason",
    "slurmd_start_time" : 6,
    "features" : [ "features", "features" ],
    "hostname" : "hostname",
    "cores" : 1,
    "reason_changed_at" : 3,
    "reservation" : "reservation",
    "tres" : "tres",
    "cpu_binding" : 5,
    "state" : [ "INVALID", "INVALID" ],
    "sockets" : 5,
    "energy" : {
      "current_watts" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "base_consumed_energy" : 3,
      "last_collected" : 7,
      "consumed_energy" : 2,
      "previous_consumed_energy" : 4,
      "average_watts" : 9
    },
    "partitions" : [ "partitions", "partitions" ],
    "gres_drained" : "gres_drained",
    "weight" : 3,
    "version" : "version",
    "gres_used" : "gres_used",
    "mcs_label" : "mcs_label",
    "real_memory" : 6,
    "burstbuffer_network_address" : "burstbuffer_network_address",
    "port" : 9,
    "name" : "name",
    "resume_after" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "temporary_disk" : 3,
    "tres_used" : "tres_used",
    "effective_cpus" : 7,
    "external_sensors" : {
      "current_watts" : 1,
      "temperature" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "energy_update_time" : 1,
      "consumed_energy" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "boards" : 0,
    "alloc_cpus" : 1,
    "active_features" : [ "active_features", "active_features" ],
    "reason_set_by_user" : "reason_set_by_user",
    "free_mem" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "alloc_idle_cpus" : 2,
    "extra" : "extra",
    "operating_system" : "operating_system",
    "power" : {
      "current_watts" : 1,
      "total_energy" : 6,
      "lowest_watts" : 4,
      "new_maximum_watts" : 7,
      "new_job_time" : 5,
      "state" : 9,
      "time_start_day" : 9,
      "peak_watts" : 1,
      "maximum_watts" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "architecture" : "architecture",
    "owner" : "owner",
    "cluster_name" : "cluster_name",
    "address" : "address",
    "cpus" : 2,
    "tres_weighted" : 6.778324963048013,
    "gres" : "gres",
    "threads" : 6,
    "boot_time" : 6,
    "alloc_memory" : 6,
    "specialized_memory" : 8,
    "specialized_cpus" : "specialized_cpus",
    "specialized_cores" : 5,
    "last_busy" : 6,
    "comment" : "comment",
    "next_state_after_reboot" : [ "INVALID", "INVALID" ],
    "cpu_load" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    }
  }, {
    "reason" : "reason",
    "slurmd_start_time" : 6,
    "features" : [ "features", "features" ],
    "hostname" : "hostname",
    "cores" : 1,
    "reason_changed_at" : 3,
    "reservation" : "reservation",
    "tres" : "tres",
    "cpu_binding" : 5,
    "state" : [ "INVALID", "INVALID" ],
    "sockets" : 5,
    "energy" : {
      "current_watts" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "base_consumed_energy" : 3,
      "last_collected" : 7,
      "consumed_energy" : 2,
      "previous_consumed_energy" : 4,
      "average_watts" : 9
    },
    "partitions" : [ "partitions", "partitions" ],
    "gres_drained" : "gres_drained",
    "weight" : 3,
    "version" : "version",
    "gres_used" : "gres_used",
    "mcs_label" : "mcs_label",
    "real_memory" : 6,
    "burstbuffer_network_address" : "burstbuffer_network_address",
    "port" : 9,
    "name" : "name",
    "resume_after" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "temporary_disk" : 3,
    "tres_used" : "tres_used",
    "effective_cpus" : 7,
    "external_sensors" : {
      "current_watts" : 1,
      "temperature" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "energy_update_time" : 1,
      "consumed_energy" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "boards" : 0,
    "alloc_cpus" : 1,
    "active_features" : [ "active_features", "active_features" ],
    "reason_set_by_user" : "reason_set_by_user",
    "free_mem" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "alloc_idle_cpus" : 2,
    "extra" : "extra",
    "operating_system" : "operating_system",
    "power" : {
      "current_watts" : 1,
      "total_energy" : 6,
      "lowest_watts" : 4,
      "new_maximum_watts" : 7,
      "new_job_time" : 5,
      "state" : 9,
      "time_start_day" : 9,
      "peak_watts" : 1,
      "maximum_watts" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "architecture" : "architecture",
    "owner" : "owner",
    "cluster_name" : "cluster_name",
    "address" : "address",
    "cpus" : 2,
    "tres_weighted" : 6.778324963048013,
    "gres" : "gres",
    "threads" : 6,
    "boot_time" : 6,
    "alloc_memory" : 6,
    "specialized_memory" : 8,
    "specialized_cpus" : "specialized_cpus",
    "specialized_cores" : 5,
    "last_busy" : 6,
    "comment" : "comment",
    "next_state_after_reboot" : [ "INVALID", "INVALID" ],
    "cpu_load" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    }
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

node information [v0.0.39_nodes_response](#v0.0.39_nodes_response)

#### default

node not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039GetNodes"></span> <span id="slurmV0039GetNodes"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurm/v0.0.39/nodes
```

get all node info (<span class="nickname">slurmV0039GetNodes</span>)

### Query parameters

update_time (optional) <span class="param-type">Query Parameter</span> — Filter if changed since
update_time. Use of this parameter can result in faster replies. default: null format: int64

### Return type

[v0.0.39_nodes_response](#v0.0.39_nodes_response)

### Example data

Content-Type: application/json

``` example
{
  "nodes" : [ {
    "reason" : "reason",
    "slurmd_start_time" : 6,
    "features" : [ "features", "features" ],
    "hostname" : "hostname",
    "cores" : 1,
    "reason_changed_at" : 3,
    "reservation" : "reservation",
    "tres" : "tres",
    "cpu_binding" : 5,
    "state" : [ "INVALID", "INVALID" ],
    "sockets" : 5,
    "energy" : {
      "current_watts" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "base_consumed_energy" : 3,
      "last_collected" : 7,
      "consumed_energy" : 2,
      "previous_consumed_energy" : 4,
      "average_watts" : 9
    },
    "partitions" : [ "partitions", "partitions" ],
    "gres_drained" : "gres_drained",
    "weight" : 3,
    "version" : "version",
    "gres_used" : "gres_used",
    "mcs_label" : "mcs_label",
    "real_memory" : 6,
    "burstbuffer_network_address" : "burstbuffer_network_address",
    "port" : 9,
    "name" : "name",
    "resume_after" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "temporary_disk" : 3,
    "tres_used" : "tres_used",
    "effective_cpus" : 7,
    "external_sensors" : {
      "current_watts" : 1,
      "temperature" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "energy_update_time" : 1,
      "consumed_energy" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "boards" : 0,
    "alloc_cpus" : 1,
    "active_features" : [ "active_features", "active_features" ],
    "reason_set_by_user" : "reason_set_by_user",
    "free_mem" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "alloc_idle_cpus" : 2,
    "extra" : "extra",
    "operating_system" : "operating_system",
    "power" : {
      "current_watts" : 1,
      "total_energy" : 6,
      "lowest_watts" : 4,
      "new_maximum_watts" : 7,
      "new_job_time" : 5,
      "state" : 9,
      "time_start_day" : 9,
      "peak_watts" : 1,
      "maximum_watts" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "architecture" : "architecture",
    "owner" : "owner",
    "cluster_name" : "cluster_name",
    "address" : "address",
    "cpus" : 2,
    "tres_weighted" : 6.778324963048013,
    "gres" : "gres",
    "threads" : 6,
    "boot_time" : 6,
    "alloc_memory" : 6,
    "specialized_memory" : 8,
    "specialized_cpus" : "specialized_cpus",
    "specialized_cores" : 5,
    "last_busy" : 6,
    "comment" : "comment",
    "next_state_after_reboot" : [ "INVALID", "INVALID" ],
    "cpu_load" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    }
  }, {
    "reason" : "reason",
    "slurmd_start_time" : 6,
    "features" : [ "features", "features" ],
    "hostname" : "hostname",
    "cores" : 1,
    "reason_changed_at" : 3,
    "reservation" : "reservation",
    "tres" : "tres",
    "cpu_binding" : 5,
    "state" : [ "INVALID", "INVALID" ],
    "sockets" : 5,
    "energy" : {
      "current_watts" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "base_consumed_energy" : 3,
      "last_collected" : 7,
      "consumed_energy" : 2,
      "previous_consumed_energy" : 4,
      "average_watts" : 9
    },
    "partitions" : [ "partitions", "partitions" ],
    "gres_drained" : "gres_drained",
    "weight" : 3,
    "version" : "version",
    "gres_used" : "gres_used",
    "mcs_label" : "mcs_label",
    "real_memory" : 6,
    "burstbuffer_network_address" : "burstbuffer_network_address",
    "port" : 9,
    "name" : "name",
    "resume_after" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "temporary_disk" : 3,
    "tres_used" : "tres_used",
    "effective_cpus" : 7,
    "external_sensors" : {
      "current_watts" : 1,
      "temperature" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "energy_update_time" : 1,
      "consumed_energy" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "boards" : 0,
    "alloc_cpus" : 1,
    "active_features" : [ "active_features", "active_features" ],
    "reason_set_by_user" : "reason_set_by_user",
    "free_mem" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "alloc_idle_cpus" : 2,
    "extra" : "extra",
    "operating_system" : "operating_system",
    "power" : {
      "current_watts" : 1,
      "total_energy" : 6,
      "lowest_watts" : 4,
      "new_maximum_watts" : 7,
      "new_job_time" : 5,
      "state" : 9,
      "time_start_day" : 9,
      "peak_watts" : 1,
      "maximum_watts" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "architecture" : "architecture",
    "owner" : "owner",
    "cluster_name" : "cluster_name",
    "address" : "address",
    "cpus" : 2,
    "tres_weighted" : 6.778324963048013,
    "gres" : "gres",
    "threads" : 6,
    "boot_time" : 6,
    "alloc_memory" : 6,
    "specialized_memory" : 8,
    "specialized_cpus" : "specialized_cpus",
    "specialized_cores" : 5,
    "last_busy" : 6,
    "comment" : "comment",
    "next_state_after_reboot" : [ "INVALID", "INVALID" ],
    "cpu_load" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    }
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

node information [v0.0.39_nodes_response](#v0.0.39_nodes_response)

#### default

no nodes in cluster [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039GetPartition"></span> <span id="slurmV0039GetPartition"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurm/v0.0.39/partition/{partition_name}
```

get partition info (<span class="nickname">slurmV0039GetPartition</span>)

### Path parameters

partition_name (required) <span class="param-type">Path Parameter</span> — Slurm Partition Name
default: null

### Query parameters

update_time (optional) <span class="param-type">Query Parameter</span> — Filter if there were no
partition changes (not limited to partition in URL endpoint) since update_time. default: null
format: int64

### Return type

[v0.0.39_partitions_response](#v0.0.39_partitions_response)

### Example data

Content-Type: application/json

``` example
{
  "partitions" : [ {
    "cluster" : "cluster",
    "cpus" : {
      "task_binding" : 6,
      "total" : 1
    },
    "timeouts" : {
      "resume" : {
        "number" : 5,
        "set" : false,
        "infinite" : true
      },
      "suspend" : {
        "number" : 5,
        "set" : false,
        "infinite" : true
      }
    },
    "groups" : {
      "allowed" : "allowed"
    },
    "alternate" : "alternate",
    "suspend_time" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "priority" : {
      "tier" : 2,
      "job_factor" : 3
    },
    "node_sets" : "node_sets",
    "maximums" : {
      "shares" : 7,
      "nodes" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "over_time_limit" : {
        "number" : 5,
        "set" : false,
        "infinite" : true
      },
      "cpus_per_node" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "cpus_per_socket" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "memory_per_cpu" : 2,
      "time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "nodes" : {
      "configured" : "configured",
      "total" : 0,
      "allowed_allocation" : "allowed_allocation"
    },
    "qos" : {
      "deny" : "deny",
      "allowed" : "allowed",
      "assigned" : "assigned"
    },
    "defaults" : {
      "memory_per_cpu" : 5,
      "time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "job" : "job"
    },
    "name" : "name",
    "tres" : {
      "configured" : "configured",
      "billing_weights" : "billing_weights"
    },
    "accounts" : {
      "deny" : "deny",
      "allowed" : "allowed"
    },
    "minimums" : {
      "nodes" : 9
    },
    "grace_time" : 5
  }, {
    "cluster" : "cluster",
    "cpus" : {
      "task_binding" : 6,
      "total" : 1
    },
    "timeouts" : {
      "resume" : {
        "number" : 5,
        "set" : false,
        "infinite" : true
      },
      "suspend" : {
        "number" : 5,
        "set" : false,
        "infinite" : true
      }
    },
    "groups" : {
      "allowed" : "allowed"
    },
    "alternate" : "alternate",
    "suspend_time" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "priority" : {
      "tier" : 2,
      "job_factor" : 3
    },
    "node_sets" : "node_sets",
    "maximums" : {
      "shares" : 7,
      "nodes" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "over_time_limit" : {
        "number" : 5,
        "set" : false,
        "infinite" : true
      },
      "cpus_per_node" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "cpus_per_socket" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "memory_per_cpu" : 2,
      "time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "nodes" : {
      "configured" : "configured",
      "total" : 0,
      "allowed_allocation" : "allowed_allocation"
    },
    "qos" : {
      "deny" : "deny",
      "allowed" : "allowed",
      "assigned" : "assigned"
    },
    "defaults" : {
      "memory_per_cpu" : 5,
      "time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "job" : "job"
    },
    "name" : "name",
    "tres" : {
      "configured" : "configured",
      "billing_weights" : "billing_weights"
    },
    "accounts" : {
      "deny" : "deny",
      "allowed" : "allowed"
    },
    "minimums" : {
      "nodes" : 9
    },
    "grace_time" : 5
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

partition information [v0.0.39_partitions_response](#v0.0.39_partitions_response)

#### default

no partitions found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039GetPartitions"></span> <span id="slurmV0039GetPartitions"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurm/v0.0.39/partitions
```

get all partition info (<span class="nickname">slurmV0039GetPartitions</span>)

### Query parameters

update_time (optional) <span class="param-type">Query Parameter</span> — Filter if changed since
update_time. Use of this parameter can result in faster replies. default: null format: int64

### Return type

[v0.0.39_partitions_response](#v0.0.39_partitions_response)

### Example data

Content-Type: application/json

``` example
{
  "partitions" : [ {
    "cluster" : "cluster",
    "cpus" : {
      "task_binding" : 6,
      "total" : 1
    },
    "timeouts" : {
      "resume" : {
        "number" : 5,
        "set" : false,
        "infinite" : true
      },
      "suspend" : {
        "number" : 5,
        "set" : false,
        "infinite" : true
      }
    },
    "groups" : {
      "allowed" : "allowed"
    },
    "alternate" : "alternate",
    "suspend_time" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "priority" : {
      "tier" : 2,
      "job_factor" : 3
    },
    "node_sets" : "node_sets",
    "maximums" : {
      "shares" : 7,
      "nodes" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "over_time_limit" : {
        "number" : 5,
        "set" : false,
        "infinite" : true
      },
      "cpus_per_node" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "cpus_per_socket" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "memory_per_cpu" : 2,
      "time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "nodes" : {
      "configured" : "configured",
      "total" : 0,
      "allowed_allocation" : "allowed_allocation"
    },
    "qos" : {
      "deny" : "deny",
      "allowed" : "allowed",
      "assigned" : "assigned"
    },
    "defaults" : {
      "memory_per_cpu" : 5,
      "time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "job" : "job"
    },
    "name" : "name",
    "tres" : {
      "configured" : "configured",
      "billing_weights" : "billing_weights"
    },
    "accounts" : {
      "deny" : "deny",
      "allowed" : "allowed"
    },
    "minimums" : {
      "nodes" : 9
    },
    "grace_time" : 5
  }, {
    "cluster" : "cluster",
    "cpus" : {
      "task_binding" : 6,
      "total" : 1
    },
    "timeouts" : {
      "resume" : {
        "number" : 5,
        "set" : false,
        "infinite" : true
      },
      "suspend" : {
        "number" : 5,
        "set" : false,
        "infinite" : true
      }
    },
    "groups" : {
      "allowed" : "allowed"
    },
    "alternate" : "alternate",
    "suspend_time" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "priority" : {
      "tier" : 2,
      "job_factor" : 3
    },
    "node_sets" : "node_sets",
    "maximums" : {
      "shares" : 7,
      "nodes" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "over_time_limit" : {
        "number" : 5,
        "set" : false,
        "infinite" : true
      },
      "cpus_per_node" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "cpus_per_socket" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "memory_per_cpu" : 2,
      "time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "nodes" : {
      "configured" : "configured",
      "total" : 0,
      "allowed_allocation" : "allowed_allocation"
    },
    "qos" : {
      "deny" : "deny",
      "allowed" : "allowed",
      "assigned" : "assigned"
    },
    "defaults" : {
      "memory_per_cpu" : 5,
      "time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "job" : "job"
    },
    "name" : "name",
    "tres" : {
      "configured" : "configured",
      "billing_weights" : "billing_weights"
    },
    "accounts" : {
      "deny" : "deny",
      "allowed" : "allowed"
    },
    "minimums" : {
      "nodes" : 9
    },
    "grace_time" : 5
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

partition information [v0.0.39_partitions_response](#v0.0.39_partitions_response)

#### default

no partitions found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039GetReservation"></span> <span id="slurmV0039GetReservation"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurm/v0.0.39/reservation/{reservation_name}
```

get reservation info (<span class="nickname">slurmV0039GetReservation</span>)

### Path parameters

reservation_name (required) <span class="param-type">Path Parameter</span> — Slurm Reservation Name
default: null

### Query parameters

update_time (optional) <span class="param-type">Query Parameter</span> — Filter if no reservation
(not limited to reservation in URL) changed since update_time. default: null format: int64

### Return type

[v0.0.39_reservations_response](#v0.0.39_reservations_response)

### Example data

Content-Type: application/json

``` example
{
  "reservations" : [ {
    "end_time" : 6,
    "flags" : [ "MAINT", "MAINT" ],
    "groups" : "groups",
    "users" : "users",
    "max_start_delay" : 1,
    "features" : "features",
    "start_time" : 5,
    "burst_buffer" : "burst_buffer",
    "licenses" : "licenses",
    "partition" : "partition",
    "watts" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "core_specializations" : [ {
      "node" : "node",
      "core" : "core"
    }, {
      "node" : "node",
      "core" : "core"
    } ],
    "name" : "name",
    "tres" : "tres",
    "accounts" : "accounts",
    "node_count" : 5,
    "node_list" : "node_list",
    "purge_completed" : {
      "time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "core_count" : 0
  }, {
    "end_time" : 6,
    "flags" : [ "MAINT", "MAINT" ],
    "groups" : "groups",
    "users" : "users",
    "max_start_delay" : 1,
    "features" : "features",
    "start_time" : 5,
    "burst_buffer" : "burst_buffer",
    "licenses" : "licenses",
    "partition" : "partition",
    "watts" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "core_specializations" : [ {
      "node" : "node",
      "core" : "core"
    }, {
      "node" : "node",
      "core" : "core"
    } ],
    "name" : "name",
    "tres" : "tres",
    "accounts" : "accounts",
    "node_count" : 5,
    "node_list" : "node_list",
    "purge_completed" : {
      "time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "core_count" : 0
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

reservation information [v0.0.39_reservations_response](#v0.0.39_reservations_response)

#### default

no reservations found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039GetReservations"></span> <span id="slurmV0039GetReservations"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurm/v0.0.39/reservations
```

get all reservation info (<span class="nickname">slurmV0039GetReservations</span>)

### Query parameters

update_time (optional) <span class="param-type">Query Parameter</span> — Filter if changed since
update_time. Use of this parameter can result in faster replies. default: null format: int64

### Return type

[v0.0.39_reservations_response](#v0.0.39_reservations_response)

### Example data

Content-Type: application/json

``` example
{
  "reservations" : [ {
    "end_time" : 6,
    "flags" : [ "MAINT", "MAINT" ],
    "groups" : "groups",
    "users" : "users",
    "max_start_delay" : 1,
    "features" : "features",
    "start_time" : 5,
    "burst_buffer" : "burst_buffer",
    "licenses" : "licenses",
    "partition" : "partition",
    "watts" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "core_specializations" : [ {
      "node" : "node",
      "core" : "core"
    }, {
      "node" : "node",
      "core" : "core"
    } ],
    "name" : "name",
    "tres" : "tres",
    "accounts" : "accounts",
    "node_count" : 5,
    "node_list" : "node_list",
    "purge_completed" : {
      "time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "core_count" : 0
  }, {
    "end_time" : 6,
    "flags" : [ "MAINT", "MAINT" ],
    "groups" : "groups",
    "users" : "users",
    "max_start_delay" : 1,
    "features" : "features",
    "start_time" : 5,
    "burst_buffer" : "burst_buffer",
    "licenses" : "licenses",
    "partition" : "partition",
    "watts" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "core_specializations" : [ {
      "node" : "node",
      "core" : "core"
    }, {
      "node" : "node",
      "core" : "core"
    } ],
    "name" : "name",
    "tres" : "tres",
    "accounts" : "accounts",
    "node_count" : 5,
    "node_list" : "node_list",
    "purge_completed" : {
      "time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "core_count" : 0
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

reservation information [v0.0.39_reservations_response](#v0.0.39_reservations_response)

#### default

no reservations found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039Ping"></span> <span id="slurmV0039Ping"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurm/v0.0.39/ping
```

ping test (<span class="nickname">slurmV0039Ping</span>)

### Return type

[v0.0.39_pings](#v0.0.39_pings)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "pings" : [ {
    "mode" : "mode",
    "hostname" : "hostname",
    "latency" : 0,
    "pinged" : "pinged"
  }, {
    "mode" : "mode",
    "hostname" : "hostname",
    "latency" : 0,
    "pinged" : "pinged"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

results of ping test [v0.0.39_pings](#v0.0.39_pings)

#### default

unable to request ping test [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039SlurmctldGetLicenses"></span> <span id="slurmV0039SlurmctldGetLicenses"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurm/v0.0.39/licenses
```

get all Slurm tracked license info (<span class="nickname">slurmV0039SlurmctldGetLicenses</span>)

### Return type

[v0.0.39_licenses_info](#v0.0.39_licenses_info)

### Example data

Content-Type: application/json

``` example
{
  "licenses" : [ {
    "Used" : 6,
    "LastUpdate" : 7,
    "Total" : 0,
    "Remote" : true,
    "LastConsumed" : 5,
    "LastDeficit" : 2,
    "LicenseName" : "LicenseName",
    "Free" : 1,
    "Reserved" : 5
  }, {
    "Used" : 6,
    "LastUpdate" : 7,
    "Total" : 0,
    "Remote" : true,
    "LastConsumed" : 5,
    "LastDeficit" : 2,
    "LicenseName" : "LicenseName",
    "Free" : 1,
    "Reserved" : 5
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

results of get all licenses [v0.0.39_licenses_info](#v0.0.39_licenses_info)

#### default

unable to request licenses [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039SubmitJob"></span> <span id="slurmV0039SubmitJob"></span>
<a href="#__Methods" class="up">Up</a>

``` post
post /slurm/v0.0.39/job/submit
```

submit new job (<span class="nickname">slurmV0039SubmitJob</span>)

### Consumes

This API call consumes the following media types via the <span class="header">Content-Type</span>
request header:

- `application/json`
- `application/x-yaml`

### Request body

v0.0.39_job_submission [v0.0.39_job_submission](#v0.0.39_job_submission) (required)
<span class="param-type">Body Parameter</span> —

### Return type

[v0.0.39_job_submission_response](#v0.0.39_job_submission_response)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "job_id" : 0,
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "step_id" : "step_id",
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ],
  "job_submit_user_msg" : "job_submit_user_msg"
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

job submitted [v0.0.39_job_submission_response](#v0.0.39_job_submission_response)

#### default

job rejected [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039UpdateJob"></span> <span id="slurmV0039UpdateJob"></span>
<a href="#__Methods" class="up">Up</a>

``` post
post /slurm/v0.0.39/job/{job_id}
```

update job (<span class="nickname">slurmV0039UpdateJob</span>)

### Path parameters

job_id (required) <span class="param-type">Path Parameter</span> — Slurm Job ID default: null

### Consumes

This API call consumes the following media types via the <span class="header">Content-Type</span>
request header:

- `application/json`
- `application/x-yaml`

### Request body

v0.0.39_job_desc_msg [v0.0.39_job_desc_msg](#v0.0.39_job_desc_msg) (required)
<span class="param-type">Body Parameter</span> —

### Return type

[v0.0.39_job_update_response](#v0.0.39_job_update_response)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "results" : [ {
    "job_id" : 0,
    "why" : "why",
    "error_code" : 6,
    "error" : "error"
  }, {
    "job_id" : 0,
    "why" : "why",
    "error_code" : 6,
    "error" : "error"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

job updated [v0.0.39_job_update_response](#v0.0.39_job_update_response)

#### default

job update failed [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmV0039UpdateNode"></span> <span id="slurmV0039UpdateNode"></span>
<a href="#__Methods" class="up">Up</a>

``` post
post /slurm/v0.0.39/node/{node_name}
```

update node properties (<span class="nickname">slurmV0039UpdateNode</span>)

### Path parameters

node_name (required) <span class="param-type">Path Parameter</span> — Slurm Node Name default: null

### Consumes

This API call consumes the following media types via the <span class="header">Content-Type</span>
request header:

- `application/json`
- `application/x-yaml`

### Request body

v0.0.39_update_node_msg [v0.0.39_update_node_msg](#v0.0.39_update_node_msg) (required)
<span class="param-type">Body Parameter</span> —

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

node information [status](#status)

#### default

node update failed [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039AddClusters"></span> <span id="slurmdbV0039AddClusters"></span>
<a href="#__Methods" class="up">Up</a>

``` post
post /slurmdb/v0.0.39/clusters
```

Add clusters (<span class="nickname">slurmdbV0039AddClusters</span>)

### Consumes

This API call consumes the following media types via the <span class="header">Content-Type</span>
request header:

- `application/json`
- `application/x-yaml`

### Request body

dbv0.0.39_clusters_info [dbv0.0.39_clusters_info](#dbv0.0.39_clusters_info) (required)
<span class="param-type">Body Parameter</span> —

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of clusters [status](#status)

#### default

Unable to add cluster [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039AddWckeys"></span> <span id="slurmdbV0039AddWckeys"></span>
<a href="#__Methods" class="up">Up</a>

``` post
post /slurmdb/v0.0.39/wckeys
```

Add wckeys (<span class="nickname">slurmdbV0039AddWckeys</span>)

### Consumes

This API call consumes the following media types via the <span class="header">Content-Type</span>
request header:

- `application/json`
- `application/x-yaml`

### Request body

dbv0.0.39_wckey_info [dbv0.0.39_wckey_info](#dbv0.0.39_wckey_info) (optional)
<span class="param-type">Body Parameter</span> —

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of wckeys [status](#status)

#### default

Unable to add wckey [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039DeleteAccount"></span> <span id="slurmdbV0039DeleteAccount"></span>
<a href="#__Methods" class="up">Up</a>

``` delete
delete /slurmdb/v0.0.39/account/{account_name}
```

Delete account (<span class="nickname">slurmdbV0039DeleteAccount</span>)

### Path parameters

account_name (required) <span class="param-type">Path Parameter</span> — Slurm Account Name default:
null

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

Delete account [status](#status)

#### default

Unable to delete account [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039DeleteAssociation"></span> <span id="slurmdbV0039DeleteAssociation"></span>
<a href="#__Methods" class="up">Up</a>

``` delete
delete /slurmdb/v0.0.39/association
```

Delete association (<span class="nickname">slurmdbV0039DeleteAssociation</span>)

### Query parameters

cluster (optional) <span class="param-type">Query Parameter</span> — Cluster name default: null
account (optional) <span class="param-type">Query Parameter</span> — Account name default: null user
(optional) <span class="param-type">Query Parameter</span> — User name default: null partition
(optional) <span class="param-type">Query Parameter</span> — Partition Name default: null

### Return type

[dbv0.0.39_response_associations_delete](#dbv0.0.39_response_associations_delete)

### Example data

Content-Type: application/json

``` example
{
  "removed_associations" : [ "removed_associations", "removed_associations" ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

Delete associations
[dbv0.0.39_response_associations_delete](#dbv0.0.39_response_associations_delete)

#### default

Association not found or unable to delete association [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039DeleteAssociations"></span> <span id="slurmdbV0039DeleteAssociations"></span>
<a href="#__Methods" class="up">Up</a>

``` delete
delete /slurmdb/v0.0.39/associations
```

Delete associations (<span class="nickname">slurmdbV0039DeleteAssociations</span>)

### Query parameters

cluster (optional) <span class="param-type">Query Parameter</span> — Cluster name default: null
account (optional) <span class="param-type">Query Parameter</span> — Account name default: null user
(optional) <span class="param-type">Query Parameter</span> — User name default: null partition
(optional) <span class="param-type">Query Parameter</span> — Partition Name default: null

### Return type

[dbv0.0.39_response_associations_delete](#dbv0.0.39_response_associations_delete)

### Example data

Content-Type: application/json

``` example
{
  "removed_associations" : [ "removed_associations", "removed_associations" ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

Delete associations
[dbv0.0.39_response_associations_delete](#dbv0.0.39_response_associations_delete)

#### default

Associations not found or unable to delete association [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039DeleteCluster"></span> <span id="slurmdbV0039DeleteCluster"></span>
<a href="#__Methods" class="up">Up</a>

``` delete
delete /slurmdb/v0.0.39/cluster/{cluster_name}
```

Delete cluster (<span class="nickname">slurmdbV0039DeleteCluster</span>)

### Path parameters

cluster_name (required) <span class="param-type">Path Parameter</span> — Slurm cluster name default:
null

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

Delete cluster [status](#status)

#### default

Cluster not found or unable to delete cluster [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039DeleteQos"></span> <span id="slurmdbV0039DeleteQos"></span>
<a href="#__Methods" class="up">Up</a>

``` delete
delete /slurmdb/v0.0.39/qos/{qos_name}
```

Delete QOS (<span class="nickname">slurmdbV0039DeleteQos</span>)

### Path parameters

qos_name (required) <span class="param-type">Path Parameter</span> — Slurm QOS Name default: null

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

Delete qos [status](#status)

#### default

Unable to delete QOS [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039DeleteUser"></span> <span id="slurmdbV0039DeleteUser"></span>
<a href="#__Methods" class="up">Up</a>

``` delete
delete /slurmdb/v0.0.39/user/{user_name}
```

Delete user (<span class="nickname">slurmdbV0039DeleteUser</span>)

### Path parameters

user_name (required) <span class="param-type">Path Parameter</span> — Slurm User Name default: null

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

User deleted [status](#status)

#### default

User not found or unable to delete user [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039DeleteWckey"></span> <span id="slurmdbV0039DeleteWckey"></span>
<a href="#__Methods" class="up">Up</a>

``` delete
delete /slurmdb/v0.0.39/wckey/{wckey}
```

Delete wckey (<span class="nickname">slurmdbV0039DeleteWckey</span>)

### Path parameters

wckey (required) <span class="param-type">Path Parameter</span> — Slurm wckey name default: null

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

Delete wckey [status](#status)

#### default

wckey not found or unable to delete wckey [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039Diag"></span> <span id="slurmdbV0039Diag"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/diag
```

Get slurmdb diagnostics (<span class="nickname">slurmdbV0039Diag</span>)

### Return type

[dbv0.0.39_diag](#dbv0.0.39_diag)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ],
  "statistics" : {
    "time_start" : 0,
    "RPCs" : [ {
      "rpc" : "rpc",
      "count" : 7,
      "time" : {
        "average" : 9,
        "total" : 3
      }
    }, {
      "rpc" : "rpc",
      "count" : 7,
      "time" : {
        "average" : 9,
        "total" : 3
      }
    } ],
    "rollups" : [ {
      "max_cycle" : 1,
      "mean_cycles" : 2,
      "last run" : 6,
      "type" : "internal",
      "total_time" : 5,
      "total_cycles" : 5
    }, {
      "max_cycle" : 1,
      "mean_cycles" : 2,
      "last run" : 6,
      "type" : "internal",
      "total_time" : 5,
      "total_cycles" : 5
    } ],
    "users" : [ {
      "count" : 2,
      "time" : {
        "average" : 9,
        "total" : 3
      },
      "user" : "user"
    }, {
      "count" : 2,
      "time" : {
        "average" : 9,
        "total" : 3
      },
      "user" : "user"
    } ]
  }
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

Dictionary of statistics [dbv0.0.39_diag](#dbv0.0.39_diag)

#### default

Unable to query diagnostics [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetAccount"></span> <span id="slurmdbV0039GetAccount"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/account/{account_name}
```

Get account info (<span class="nickname">slurmdbV0039GetAccount</span>)

### Path parameters

account_name (required) <span class="param-type">Path Parameter</span> — Slurm Account Name default:
null

### Query parameters

with_deleted (optional) <span class="param-type">Query Parameter</span> — Include deleted accounts.
False by default. default: false

### Return type

[dbv0.0.39_account_info](#dbv0.0.39_account_info)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "accounts" : [ {
    "associations" : [ {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    }, {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    } ],
    "coordinators" : [ {
      "name" : "name",
      "direct" : true
    }, {
      "name" : "name",
      "direct" : true
    } ],
    "organization" : "organization",
    "name" : "name",
    "flags" : [ "DELETED", "DELETED" ],
    "description" : "description"
  }, {
    "associations" : [ {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    }, {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    } ],
    "coordinators" : [ {
      "name" : "name",
      "direct" : true
    }, {
      "name" : "name",
      "direct" : true
    } ],
    "organization" : "organization",
    "name" : "name",
    "flags" : [ "DELETED", "DELETED" ],
    "description" : "description"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of accounts [dbv0.0.39_account_info](#dbv0.0.39_account_info)

#### default

Account not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetAccounts"></span> <span id="slurmdbV0039GetAccounts"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/accounts
```

Get account list (<span class="nickname">slurmdbV0039GetAccounts</span>)

### Query parameters

with_deleted (optional) <span class="param-type">Query Parameter</span> — Include deleted accounts.
False by default. default: false

### Return type

[dbv0.0.39_account_info](#dbv0.0.39_account_info)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "accounts" : [ {
    "associations" : [ {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    }, {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    } ],
    "coordinators" : [ {
      "name" : "name",
      "direct" : true
    }, {
      "name" : "name",
      "direct" : true
    } ],
    "organization" : "organization",
    "name" : "name",
    "flags" : [ "DELETED", "DELETED" ],
    "description" : "description"
  }, {
    "associations" : [ {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    }, {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    } ],
    "coordinators" : [ {
      "name" : "name",
      "direct" : true
    }, {
      "name" : "name",
      "direct" : true
    } ],
    "organization" : "organization",
    "name" : "name",
    "flags" : [ "DELETED", "DELETED" ],
    "description" : "description"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of accounts [dbv0.0.39_account_info](#dbv0.0.39_account_info)

#### default

Account not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetAssociation"></span> <span id="slurmdbV0039GetAssociation"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/association
```

Get association info (<span class="nickname">slurmdbV0039GetAssociation</span>)

### Query parameters

cluster (optional) <span class="param-type">Query Parameter</span> — Cluster name default: null
account (optional) <span class="param-type">Query Parameter</span> — Account name default: null user
(optional) <span class="param-type">Query Parameter</span> — User name default: null partition
(optional) <span class="param-type">Query Parameter</span> — Partition Name default: null

### Return type

[dbv0.0.39_associations_info](#dbv0.0.39_associations_info)

### Example data

Content-Type: application/json

``` example
{
  "associations" : [ {
    "cluster" : "cluster",
    "shares_raw" : 0,
    "max" : {
      "jobs" : {
        "total" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "active" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "accruing" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "per" : {
          "submitted" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "count" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "accruing" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "wall_clock" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "tres" : {
        "total" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ],
        "minutes" : {
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "per" : {
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        },
        "per" : {
          "node" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "job" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "group" : {
          "minutes" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "active" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        }
      },
      "per" : {
        "account" : {
          "wall_clock" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    },
    "usage" : {
      "fairshare_factor" : 5.962133916683182,
      "normalized_shares" : 7.061401241503109,
      "effective_normalized_usage" : 9.301444243932576,
      "job_count" : 7,
      "group_used_wallclock" : 1.4658129805029452,
      "normalized_priority" : 2.3021358869347655,
      "normalized_usage" : 3.616076749251911,
      "accrue_job_count" : 6,
      "fairshare_shares" : 5,
      "fairshare_level" : 1.2315135367772556,
      "raw_usage" : 2.027123023002322,
      "active_jobs" : 4
    },
    "flags" : [ "DELETED", "DELETED" ],
    "is_default" : true,
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "parent_account" : "parent_account",
    "default" : {
      "qos" : "qos"
    },
    "min" : {
      "priority_threshold" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "partition" : "partition",
    "qos" : [ "qos", "qos" ],
    "user" : "user",
    "account" : "account"
  }, {
    "cluster" : "cluster",
    "shares_raw" : 0,
    "max" : {
      "jobs" : {
        "total" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "active" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "accruing" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "per" : {
          "submitted" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "count" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "accruing" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "wall_clock" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "tres" : {
        "total" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ],
        "minutes" : {
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "per" : {
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        },
        "per" : {
          "node" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "job" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "group" : {
          "minutes" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "active" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        }
      },
      "per" : {
        "account" : {
          "wall_clock" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    },
    "usage" : {
      "fairshare_factor" : 5.962133916683182,
      "normalized_shares" : 7.061401241503109,
      "effective_normalized_usage" : 9.301444243932576,
      "job_count" : 7,
      "group_used_wallclock" : 1.4658129805029452,
      "normalized_priority" : 2.3021358869347655,
      "normalized_usage" : 3.616076749251911,
      "accrue_job_count" : 6,
      "fairshare_shares" : 5,
      "fairshare_level" : 1.2315135367772556,
      "raw_usage" : 2.027123023002322,
      "active_jobs" : 4
    },
    "flags" : [ "DELETED", "DELETED" ],
    "is_default" : true,
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "parent_account" : "parent_account",
    "default" : {
      "qos" : "qos"
    },
    "min" : {
      "priority_threshold" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "partition" : "partition",
    "qos" : [ "qos", "qos" ],
    "user" : "user",
    "account" : "account"
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of associations [dbv0.0.39_associations_info](#dbv0.0.39_associations_info)

#### default

Association not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetAssociations"></span> <span id="slurmdbV0039GetAssociations"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/associations
```

Get association list (<span class="nickname">slurmdbV0039GetAssociations</span>)

### Query parameters

cluster (optional) <span class="param-type">Query Parameter</span> — Cluster name default: null
account (optional) <span class="param-type">Query Parameter</span> — Account name default: null user
(optional) <span class="param-type">Query Parameter</span> — User name default: null partition
(optional) <span class="param-type">Query Parameter</span> — Partition Name default: null

### Return type

[dbv0.0.39_associations_info](#dbv0.0.39_associations_info)

### Example data

Content-Type: application/json

``` example
{
  "associations" : [ {
    "cluster" : "cluster",
    "shares_raw" : 0,
    "max" : {
      "jobs" : {
        "total" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "active" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "accruing" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "per" : {
          "submitted" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "count" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "accruing" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "wall_clock" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "tres" : {
        "total" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ],
        "minutes" : {
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "per" : {
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        },
        "per" : {
          "node" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "job" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "group" : {
          "minutes" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "active" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        }
      },
      "per" : {
        "account" : {
          "wall_clock" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    },
    "usage" : {
      "fairshare_factor" : 5.962133916683182,
      "normalized_shares" : 7.061401241503109,
      "effective_normalized_usage" : 9.301444243932576,
      "job_count" : 7,
      "group_used_wallclock" : 1.4658129805029452,
      "normalized_priority" : 2.3021358869347655,
      "normalized_usage" : 3.616076749251911,
      "accrue_job_count" : 6,
      "fairshare_shares" : 5,
      "fairshare_level" : 1.2315135367772556,
      "raw_usage" : 2.027123023002322,
      "active_jobs" : 4
    },
    "flags" : [ "DELETED", "DELETED" ],
    "is_default" : true,
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "parent_account" : "parent_account",
    "default" : {
      "qos" : "qos"
    },
    "min" : {
      "priority_threshold" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "partition" : "partition",
    "qos" : [ "qos", "qos" ],
    "user" : "user",
    "account" : "account"
  }, {
    "cluster" : "cluster",
    "shares_raw" : 0,
    "max" : {
      "jobs" : {
        "total" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "active" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "accruing" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "per" : {
          "submitted" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "count" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "accruing" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "wall_clock" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "tres" : {
        "total" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ],
        "minutes" : {
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "per" : {
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        },
        "per" : {
          "node" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "job" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "group" : {
          "minutes" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "active" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        }
      },
      "per" : {
        "account" : {
          "wall_clock" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    },
    "usage" : {
      "fairshare_factor" : 5.962133916683182,
      "normalized_shares" : 7.061401241503109,
      "effective_normalized_usage" : 9.301444243932576,
      "job_count" : 7,
      "group_used_wallclock" : 1.4658129805029452,
      "normalized_priority" : 2.3021358869347655,
      "normalized_usage" : 3.616076749251911,
      "accrue_job_count" : 6,
      "fairshare_shares" : 5,
      "fairshare_level" : 1.2315135367772556,
      "raw_usage" : 2.027123023002322,
      "active_jobs" : 4
    },
    "flags" : [ "DELETED", "DELETED" ],
    "is_default" : true,
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "parent_account" : "parent_account",
    "default" : {
      "qos" : "qos"
    },
    "min" : {
      "priority_threshold" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "partition" : "partition",
    "qos" : [ "qos", "qos" ],
    "user" : "user",
    "account" : "account"
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of associations [dbv0.0.39_associations_info](#dbv0.0.39_associations_info)

#### default

Association not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetCluster"></span> <span id="slurmdbV0039GetCluster"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/cluster/{cluster_name}
```

Get cluster info (<span class="nickname">slurmdbV0039GetCluster</span>)

### Path parameters

cluster_name (required) <span class="param-type">Path Parameter</span> — Slurm cluster name default:
null

### Return type

[dbv0.0.39_clusters_info](#dbv0.0.39_clusters_info)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ],
  "clusters" : [ {
    "associations" : {
      "root" : {
        "cluster" : "cluster",
        "partition" : "partition",
        "user" : "user",
        "account" : "account"
      }
    },
    "controller" : {
      "port" : 9,
      "host" : "host"
    },
    "nodes" : "nodes",
    "flags" : [ "REGISTERING", "REGISTERING" ],
    "name" : "name",
    "rpc_version" : 9,
    "tres" : [ {
      "name" : "name",
      "count" : 7,
      "id" : 3,
      "type" : "type"
    }, {
      "name" : "name",
      "count" : 7,
      "id" : 3,
      "type" : "type"
    } ],
    "select_plugin" : "select_plugin"
  }, {
    "associations" : {
      "root" : {
        "cluster" : "cluster",
        "partition" : "partition",
        "user" : "user",
        "account" : "account"
      }
    },
    "controller" : {
      "port" : 9,
      "host" : "host"
    },
    "nodes" : "nodes",
    "flags" : [ "REGISTERING", "REGISTERING" ],
    "name" : "name",
    "rpc_version" : 9,
    "tres" : [ {
      "name" : "name",
      "count" : 7,
      "id" : 3,
      "type" : "type"
    }, {
      "name" : "name",
      "count" : 7,
      "id" : 3,
      "type" : "type"
    } ],
    "select_plugin" : "select_plugin"
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

Cluster information [dbv0.0.39_clusters_info](#dbv0.0.39_clusters_info)

#### default

Cluster not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetClusters"></span> <span id="slurmdbV0039GetClusters"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/clusters
```

Get cluster list (<span class="nickname">slurmdbV0039GetClusters</span>)

### Return type

[dbv0.0.39_clusters_info](#dbv0.0.39_clusters_info)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ],
  "clusters" : [ {
    "associations" : {
      "root" : {
        "cluster" : "cluster",
        "partition" : "partition",
        "user" : "user",
        "account" : "account"
      }
    },
    "controller" : {
      "port" : 9,
      "host" : "host"
    },
    "nodes" : "nodes",
    "flags" : [ "REGISTERING", "REGISTERING" ],
    "name" : "name",
    "rpc_version" : 9,
    "tres" : [ {
      "name" : "name",
      "count" : 7,
      "id" : 3,
      "type" : "type"
    }, {
      "name" : "name",
      "count" : 7,
      "id" : 3,
      "type" : "type"
    } ],
    "select_plugin" : "select_plugin"
  }, {
    "associations" : {
      "root" : {
        "cluster" : "cluster",
        "partition" : "partition",
        "user" : "user",
        "account" : "account"
      }
    },
    "controller" : {
      "port" : 9,
      "host" : "host"
    },
    "nodes" : "nodes",
    "flags" : [ "REGISTERING", "REGISTERING" ],
    "name" : "name",
    "rpc_version" : 9,
    "tres" : [ {
      "name" : "name",
      "count" : 7,
      "id" : 3,
      "type" : "type"
    }, {
      "name" : "name",
      "count" : 7,
      "id" : 3,
      "type" : "type"
    } ],
    "select_plugin" : "select_plugin"
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of clusters [dbv0.0.39_clusters_info](#dbv0.0.39_clusters_info)

#### default

Cluster not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetConfig"></span> <span id="slurmdbV0039GetConfig"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/config
```

Dump all configuration information (<span class="nickname">slurmdbV0039GetConfig</span>)

### Return type

[dbv0.0.39_config_info](#dbv0.0.39_config_info)

### Example data

Content-Type: application/json

``` example
{
  "associations" : [ {
    "cluster" : "cluster",
    "shares_raw" : 0,
    "max" : {
      "jobs" : {
        "total" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "active" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "accruing" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "per" : {
          "submitted" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "count" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "accruing" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "wall_clock" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "tres" : {
        "total" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ],
        "minutes" : {
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "per" : {
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        },
        "per" : {
          "node" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "job" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "group" : {
          "minutes" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "active" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        }
      },
      "per" : {
        "account" : {
          "wall_clock" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    },
    "usage" : {
      "fairshare_factor" : 5.962133916683182,
      "normalized_shares" : 7.061401241503109,
      "effective_normalized_usage" : 9.301444243932576,
      "job_count" : 7,
      "group_used_wallclock" : 1.4658129805029452,
      "normalized_priority" : 2.3021358869347655,
      "normalized_usage" : 3.616076749251911,
      "accrue_job_count" : 6,
      "fairshare_shares" : 5,
      "fairshare_level" : 1.2315135367772556,
      "raw_usage" : 2.027123023002322,
      "active_jobs" : 4
    },
    "flags" : [ "DELETED", "DELETED" ],
    "is_default" : true,
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "parent_account" : "parent_account",
    "default" : {
      "qos" : "qos"
    },
    "min" : {
      "priority_threshold" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "partition" : "partition",
    "qos" : [ "qos", "qos" ],
    "user" : "user",
    "account" : "account"
  }, {
    "cluster" : "cluster",
    "shares_raw" : 0,
    "max" : {
      "jobs" : {
        "total" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "active" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "accruing" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "per" : {
          "submitted" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "count" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "accruing" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "wall_clock" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "tres" : {
        "total" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ],
        "minutes" : {
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "per" : {
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        },
        "per" : {
          "node" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "job" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "group" : {
          "minutes" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "active" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        }
      },
      "per" : {
        "account" : {
          "wall_clock" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    },
    "usage" : {
      "fairshare_factor" : 5.962133916683182,
      "normalized_shares" : 7.061401241503109,
      "effective_normalized_usage" : 9.301444243932576,
      "job_count" : 7,
      "group_used_wallclock" : 1.4658129805029452,
      "normalized_priority" : 2.3021358869347655,
      "normalized_usage" : 3.616076749251911,
      "accrue_job_count" : 6,
      "fairshare_shares" : 5,
      "fairshare_level" : 1.2315135367772556,
      "raw_usage" : 2.027123023002322,
      "active_jobs" : 4
    },
    "flags" : [ "DELETED", "DELETED" ],
    "is_default" : true,
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "parent_account" : "parent_account",
    "default" : {
      "qos" : "qos"
    },
    "min" : {
      "priority_threshold" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "partition" : "partition",
    "qos" : [ "qos", "qos" ],
    "user" : "user",
    "account" : "account"
  } ],
  "qos" : [ {
    "flags" : [ "NOT_SET", "NOT_SET" ],
    "name" : "name",
    "usage_threshold" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "description" : "description",
    "usage_factor" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "id" : 1,
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "limits" : {
      "min" : {
        "priority_threshold" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "tres" : {
          "per" : {
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        }
      },
      "max" : {
        "jobs" : {
          "per" : {
            "user" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "account" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          },
          "active_jobs" : {
            "per" : {
              "user" : {
                "number" : 9,
                "set" : false,
                "infinite" : true
              },
              "account" : {
                "number" : 9,
                "set" : false,
                "infinite" : true
              }
            }
          }
        },
        "accruing" : {
          "per" : {
            "user" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "account" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          }
        },
        "tres" : {
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "minutes" : {
            "per" : {
              "qos" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "job" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "user" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "account" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ]
            }
          },
          "per" : {
            "node" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "user" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "account" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        },
        "wall_clock" : {
          "per" : {
            "qos" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "job" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          }
        },
        "active_jobs" : {
          "count" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "accruing" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "factor" : 4.965218492984954,
      "grace_time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "preempt" : {
      "mode" : [ "DISABLED", "DISABLED" ],
      "exempt_time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "list" : [ "list", "list" ]
    }
  }, {
    "flags" : [ "NOT_SET", "NOT_SET" ],
    "name" : "name",
    "usage_threshold" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "description" : "description",
    "usage_factor" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "id" : 1,
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "limits" : {
      "min" : {
        "priority_threshold" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "tres" : {
          "per" : {
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        }
      },
      "max" : {
        "jobs" : {
          "per" : {
            "user" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "account" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          },
          "active_jobs" : {
            "per" : {
              "user" : {
                "number" : 9,
                "set" : false,
                "infinite" : true
              },
              "account" : {
                "number" : 9,
                "set" : false,
                "infinite" : true
              }
            }
          }
        },
        "accruing" : {
          "per" : {
            "user" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "account" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          }
        },
        "tres" : {
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "minutes" : {
            "per" : {
              "qos" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "job" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "user" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "account" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ]
            }
          },
          "per" : {
            "node" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "user" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "account" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        },
        "wall_clock" : {
          "per" : {
            "qos" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "job" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          }
        },
        "active_jobs" : {
          "count" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "accruing" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "factor" : 4.965218492984954,
      "grace_time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "preempt" : {
      "mode" : [ "DISABLED", "DISABLED" ],
      "exempt_time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "list" : [ "list", "list" ]
    }
  } ],
  "wckeys" : [ {
    "cluster" : "cluster",
    "name" : "name",
    "flags" : [ "DELETED", "DELETED" ],
    "accounting" : [ {
      "start" : 6,
      "id" : 1,
      "TRES" : {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      },
      "allocated" : {
        "seconds" : 1
      }
    }, {
      "start" : 6,
      "id" : 1,
      "TRES" : {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      },
      "allocated" : {
        "seconds" : 1
      }
    } ],
    "id" : 7,
    "user" : "user"
  }, {
    "cluster" : "cluster",
    "name" : "name",
    "flags" : [ "DELETED", "DELETED" ],
    "accounting" : [ {
      "start" : 6,
      "id" : 1,
      "TRES" : {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      },
      "allocated" : {
        "seconds" : 1
      }
    }, {
      "start" : 6,
      "id" : 1,
      "TRES" : {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      },
      "allocated" : {
        "seconds" : 1
      }
    } ],
    "id" : 7,
    "user" : "user"
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "tres" : [ {
    "name" : "name",
    "count" : 7,
    "id" : 3,
    "type" : "type"
  }, {
    "name" : "name",
    "count" : 7,
    "id" : 3,
    "type" : "type"
  } ],
  "accounts" : [ {
    "associations" : [ {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    }, {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    } ],
    "coordinators" : [ {
      "name" : "name",
      "direct" : true
    }, {
      "name" : "name",
      "direct" : true
    } ],
    "organization" : "organization",
    "name" : "name",
    "flags" : [ "DELETED", "DELETED" ],
    "description" : "description"
  }, {
    "associations" : [ {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    }, {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    } ],
    "coordinators" : [ {
      "name" : "name",
      "direct" : true
    }, {
      "name" : "name",
      "direct" : true
    } ],
    "organization" : "organization",
    "name" : "name",
    "flags" : [ "DELETED", "DELETED" ],
    "description" : "description"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ],
  "users" : [ {
    "associations" : [ {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    }, {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    } ],
    "default" : {
      "wckey" : "wckey",
      "account" : "account"
    },
    "administrator_level" : [ "Not Set", "Not Set" ],
    "old_name" : "old_name",
    "wckeys" : [ {
      "cluster" : "cluster",
      "name" : "name",
      "flags" : [ "DELETED", "DELETED" ],
      "accounting" : [ {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      }, {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      } ],
      "id" : 7,
      "user" : "user"
    }, {
      "cluster" : "cluster",
      "name" : "name",
      "flags" : [ "DELETED", "DELETED" ],
      "accounting" : [ {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      }, {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      } ],
      "id" : 7,
      "user" : "user"
    } ],
    "coordinators" : [ {
      "name" : "name",
      "direct" : true
    }, {
      "name" : "name",
      "direct" : true
    } ],
    "flags" : [ "NONE", "NONE" ],
    "name" : "name"
  }, {
    "associations" : [ {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    }, {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    } ],
    "default" : {
      "wckey" : "wckey",
      "account" : "account"
    },
    "administrator_level" : [ "Not Set", "Not Set" ],
    "old_name" : "old_name",
    "wckeys" : [ {
      "cluster" : "cluster",
      "name" : "name",
      "flags" : [ "DELETED", "DELETED" ],
      "accounting" : [ {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      }, {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      } ],
      "id" : 7,
      "user" : "user"
    }, {
      "cluster" : "cluster",
      "name" : "name",
      "flags" : [ "DELETED", "DELETED" ],
      "accounting" : [ {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      }, {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      } ],
      "id" : 7,
      "user" : "user"
    } ],
    "coordinators" : [ {
      "name" : "name",
      "direct" : true
    }, {
      "name" : "name",
      "direct" : true
    } ],
    "flags" : [ "NONE", "NONE" ],
    "name" : "name"
  } ],
  "clusters" : [ {
    "associations" : {
      "root" : {
        "cluster" : "cluster",
        "partition" : "partition",
        "user" : "user",
        "account" : "account"
      }
    },
    "controller" : {
      "port" : 9,
      "host" : "host"
    },
    "nodes" : "nodes",
    "flags" : [ "REGISTERING", "REGISTERING" ],
    "name" : "name",
    "rpc_version" : 9,
    "tres" : [ {
      "name" : "name",
      "count" : 7,
      "id" : 3,
      "type" : "type"
    }, {
      "name" : "name",
      "count" : 7,
      "id" : 3,
      "type" : "type"
    } ],
    "select_plugin" : "select_plugin"
  }, {
    "associations" : {
      "root" : {
        "cluster" : "cluster",
        "partition" : "partition",
        "user" : "user",
        "account" : "account"
      }
    },
    "controller" : {
      "port" : 9,
      "host" : "host"
    },
    "nodes" : "nodes",
    "flags" : [ "REGISTERING", "REGISTERING" ],
    "name" : "name",
    "rpc_version" : 9,
    "tres" : [ {
      "name" : "name",
      "count" : 7,
      "id" : 3,
      "type" : "type"
    }, {
      "name" : "name",
      "count" : 7,
      "id" : 3,
      "type" : "type"
    } ],
    "select_plugin" : "select_plugin"
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

slurmdbd configuration [dbv0.0.39_config_info](#dbv0.0.39_config_info)

#### default

Unable to dump config [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetJob"></span> <span id="slurmdbV0039GetJob"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/job/{job_id}
```

Get job info (<span class="nickname">slurmdbV0039GetJob</span>) This endpoint may return multiple
job entries since job_id is not a unique key - only the tuple (cluster, job_id, start_time) is
unique. If the requested job_id is a component of a heterogeneous job all components are returned.

### Path parameters

job_id (required) <span class="param-type">Path Parameter</span> — Slurm JobID default: null

### Return type

[dbv0.0.39_job_info](#dbv0.0.39_job_info)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "jobs" : [ {
    "container" : "container",
    "cluster" : "cluster",
    "flags" : [ "NONE", "NONE" ],
    "used_gres" : "used_gres",
    "association" : {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    },
    "allocation_nodes" : 5,
    "working_directory" : "working_directory",
    "constraints" : "constraints",
    "required" : {
      "memory_per_node" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "memory" : 6,
      "CPUs" : 9,
      "memory_per_cpu" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "hold" : true,
    "partition" : "partition",
    "qos" : "qos",
    "array" : {
      "task" : "task",
      "job_id" : 2,
      "task_id" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "limits" : {
        "max" : {
          "running" : {
            "tasks" : 7
          }
        }
      }
    },
    "het" : {
      "job_id" : 4,
      "job_offset" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "submit_line" : "submit_line",
    "extra" : "extra",
    "reservation" : {
      "name" : "name",
      "id" : 8
    },
    "block" : "block",
    "tres" : {
      "requested" : [ {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      }, {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      } ],
      "allocated" : [ {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      }, {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      } ]
    },
    "state" : {
      "reason" : "reason",
      "current" : "current"
    },
    "mcs" : {
      "label" : "label"
    },
    "group" : "group",
    "wckey" : {
      "wckey" : "wckey",
      "flags" : [ "ASSIGNED_DEFAULT", "ASSIGNED_DEFAULT" ]
    },
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "steps" : [ {
      "nodes" : {
        "count" : 6,
        "range" : "range",
        "list" : [ "list", "list" ]
      },
      "task" : {
        "distribution" : "distribution"
      },
      "exit_code" : {
        "return_code" : 3,
        "signal" : {
          "name" : "name",
          "signal_id" : 2
        },
        "status" : "status"
      },
      "kill_request_user" : "kill_request_user",
      "CPU" : {
        "governor" : "governor",
        "requested_frequency" : {
          "min" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "max" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "pid" : "pid",
      "step" : {
        "name" : "name",
        "id" : {
          "job_id" : 6,
          "step_het_component" : 3,
          "step_id" : "step_id"
        }
      },
      "tres" : {
        "consumed" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "requested" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "allocated" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ]
      },
      "time" : {
        "elapsed" : 9,
        "total" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "system" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "start" : 3,
        "end" : 6,
        "user" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "suspended" : 6
      },
      "state" : "state",
      "tasks" : {
        "count" : 6
      },
      "statistics" : {
        "CPU" : {
          "actual_frequency" : 5
        },
        "energy" : {
          "consumed" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    }, {
      "nodes" : {
        "count" : 6,
        "range" : "range",
        "list" : [ "list", "list" ]
      },
      "task" : {
        "distribution" : "distribution"
      },
      "exit_code" : {
        "return_code" : 3,
        "signal" : {
          "name" : "name",
          "signal_id" : 2
        },
        "status" : "status"
      },
      "kill_request_user" : "kill_request_user",
      "CPU" : {
        "governor" : "governor",
        "requested_frequency" : {
          "min" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "max" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "pid" : "pid",
      "step" : {
        "name" : "name",
        "id" : {
          "job_id" : 6,
          "step_het_component" : 3,
          "step_id" : "step_id"
        }
      },
      "tres" : {
        "consumed" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "requested" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "allocated" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ]
      },
      "time" : {
        "elapsed" : 9,
        "total" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "system" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "start" : 3,
        "end" : 6,
        "user" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "suspended" : 6
      },
      "state" : "state",
      "tasks" : {
        "count" : 6
      },
      "statistics" : {
        "CPU" : {
          "actual_frequency" : 5
        },
        "energy" : {
          "consumed" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    } ],
    "script" : "script",
    "failed_node" : "failed_node",
    "derived_exit_code" : {
      "return_code" : 3,
      "signal" : {
        "name" : "name",
        "signal_id" : 2
      },
      "status" : "status"
    },
    "licenses" : "licenses",
    "nodes" : "nodes",
    "job_id" : 5,
    "exit_code" : {
      "return_code" : 3,
      "signal" : {
        "name" : "name",
        "signal_id" : 2
      },
      "status" : "status"
    },
    "name" : "name",
    "kill_request_user" : "kill_request_user",
    "comment" : {
      "administrator" : "administrator",
      "system" : "system",
      "job" : "job"
    },
    "time" : {
      "elapsed" : 4,
      "total" : {
        "seconds" : 7,
        "microseconds" : 1
      },
      "system" : {
        "seconds" : 7,
        "microseconds" : 1
      },
      "eligible" : 7,
      "start" : 1,
      "limit" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "end" : 1,
      "submission" : 1,
      "user" : {
        "seconds" : 7,
        "microseconds" : 1
      },
      "suspended" : 6
    },
    "user" : "user",
    "account" : "account"
  }, {
    "container" : "container",
    "cluster" : "cluster",
    "flags" : [ "NONE", "NONE" ],
    "used_gres" : "used_gres",
    "association" : {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    },
    "allocation_nodes" : 5,
    "working_directory" : "working_directory",
    "constraints" : "constraints",
    "required" : {
      "memory_per_node" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "memory" : 6,
      "CPUs" : 9,
      "memory_per_cpu" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "hold" : true,
    "partition" : "partition",
    "qos" : "qos",
    "array" : {
      "task" : "task",
      "job_id" : 2,
      "task_id" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "limits" : {
        "max" : {
          "running" : {
            "tasks" : 7
          }
        }
      }
    },
    "het" : {
      "job_id" : 4,
      "job_offset" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "submit_line" : "submit_line",
    "extra" : "extra",
    "reservation" : {
      "name" : "name",
      "id" : 8
    },
    "block" : "block",
    "tres" : {
      "requested" : [ {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      }, {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      } ],
      "allocated" : [ {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      }, {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      } ]
    },
    "state" : {
      "reason" : "reason",
      "current" : "current"
    },
    "mcs" : {
      "label" : "label"
    },
    "group" : "group",
    "wckey" : {
      "wckey" : "wckey",
      "flags" : [ "ASSIGNED_DEFAULT", "ASSIGNED_DEFAULT" ]
    },
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "steps" : [ {
      "nodes" : {
        "count" : 6,
        "range" : "range",
        "list" : [ "list", "list" ]
      },
      "task" : {
        "distribution" : "distribution"
      },
      "exit_code" : {
        "return_code" : 3,
        "signal" : {
          "name" : "name",
          "signal_id" : 2
        },
        "status" : "status"
      },
      "kill_request_user" : "kill_request_user",
      "CPU" : {
        "governor" : "governor",
        "requested_frequency" : {
          "min" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "max" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "pid" : "pid",
      "step" : {
        "name" : "name",
        "id" : {
          "job_id" : 6,
          "step_het_component" : 3,
          "step_id" : "step_id"
        }
      },
      "tres" : {
        "consumed" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "requested" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "allocated" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ]
      },
      "time" : {
        "elapsed" : 9,
        "total" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "system" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "start" : 3,
        "end" : 6,
        "user" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "suspended" : 6
      },
      "state" : "state",
      "tasks" : {
        "count" : 6
      },
      "statistics" : {
        "CPU" : {
          "actual_frequency" : 5
        },
        "energy" : {
          "consumed" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    }, {
      "nodes" : {
        "count" : 6,
        "range" : "range",
        "list" : [ "list", "list" ]
      },
      "task" : {
        "distribution" : "distribution"
      },
      "exit_code" : {
        "return_code" : 3,
        "signal" : {
          "name" : "name",
          "signal_id" : 2
        },
        "status" : "status"
      },
      "kill_request_user" : "kill_request_user",
      "CPU" : {
        "governor" : "governor",
        "requested_frequency" : {
          "min" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "max" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "pid" : "pid",
      "step" : {
        "name" : "name",
        "id" : {
          "job_id" : 6,
          "step_het_component" : 3,
          "step_id" : "step_id"
        }
      },
      "tres" : {
        "consumed" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "requested" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "allocated" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ]
      },
      "time" : {
        "elapsed" : 9,
        "total" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "system" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "start" : 3,
        "end" : 6,
        "user" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "suspended" : 6
      },
      "state" : "state",
      "tasks" : {
        "count" : 6
      },
      "statistics" : {
        "CPU" : {
          "actual_frequency" : 5
        },
        "energy" : {
          "consumed" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    } ],
    "script" : "script",
    "failed_node" : "failed_node",
    "derived_exit_code" : {
      "return_code" : 3,
      "signal" : {
        "name" : "name",
        "signal_id" : 2
      },
      "status" : "status"
    },
    "licenses" : "licenses",
    "nodes" : "nodes",
    "job_id" : 5,
    "exit_code" : {
      "return_code" : 3,
      "signal" : {
        "name" : "name",
        "signal_id" : 2
      },
      "status" : "status"
    },
    "name" : "name",
    "kill_request_user" : "kill_request_user",
    "comment" : {
      "administrator" : "administrator",
      "system" : "system",
      "job" : "job"
    },
    "time" : {
      "elapsed" : 4,
      "total" : {
        "seconds" : 7,
        "microseconds" : 1
      },
      "system" : {
        "seconds" : 7,
        "microseconds" : 1
      },
      "eligible" : 7,
      "start" : 1,
      "limit" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "end" : 1,
      "submission" : 1,
      "user" : {
        "seconds" : 7,
        "microseconds" : 1
      },
      "suspended" : 6
    },
    "user" : "user",
    "account" : "account"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

Job description [dbv0.0.39_job_info](#dbv0.0.39_job_info)

#### default

Unable to find job [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetJobs"></span> <span id="slurmdbV0039GetJobs"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/jobs
```

Get job list (<span class="nickname">slurmdbV0039GetJobs</span>)

### Query parameters

users (optional) <span class="param-type">Query Parameter</span> — Filter by comma delimited list of
user names default: null submit_time (optional) <span class="param-type">Query Parameter</span> —
Filter by submission time Accepted formats: HH:MM\[:SS\] \[AM\|PM\] MMDD\[YY\] or MM/DD\[/YY\] or
MM.DD\[.YY\] MM/DD\[/YY\]-HH:MM\[:SS\] YYYY-MM-DD\[THH:MM\[:SS\]\] default: null start_time
(optional) <span class="param-type">Query Parameter</span> — Filter by start time Accepted formats:
HH:MM\[:SS\] \[AM\|PM\] MMDD\[YY\] or MM/DD\[/YY\] or MM.DD\[.YY\] MM/DD\[/YY\]-HH:MM\[:SS\]
YYYY-MM-DD\[THH:MM\[:SS\]\] default: null end_time (optional) <span class="param-type">Query
Parameter</span> — Filter by end time Accepted formats: HH:MM\[:SS\] \[AM\|PM\] MMDD\[YY\] or
MM/DD\[/YY\] or MM.DD\[.YY\] MM/DD\[/YY\]-HH:MM\[:SS\] YYYY-MM-DD\[THH:MM\[:SS\]\] default: null
account (optional) <span class="param-type">Query Parameter</span> — Comma delimited list of
accounts to match default: null association (optional) <span class="param-type">Query
Parameter</span> — Comma delimited list of associations to match default: null cluster (optional)
<span class="param-type">Query Parameter</span> — Comma delimited list of cluster to match default:
null constraints (optional) <span class="param-type">Query Parameter</span> — Comma delimited list
of constraints to match default: null cpus_max (optional) <span class="param-type">Query
Parameter</span> — Number of CPUs high range default: null cpus_min (optional)
<span class="param-type">Query Parameter</span> — Number of CPUs low range default: null skip_steps
(optional) <span class="param-type">Query Parameter</span> — Report job step information default:
false disable_wait_for_result (optional) <span class="param-type">Query Parameter</span> — Disable
waiting for result from slurmdbd default: false exit_code (optional) <span class="param-type">Query
Parameter</span> — Exit code of job default: null format (optional) <span class="param-type">Query
Parameter</span> — Comma delimited list of formats to match default: null group (optional)
<span class="param-type">Query Parameter</span> — Comma delimited list of groups to match default:
null job_name (optional) <span class="param-type">Query Parameter</span> — Comma delimited list of
job names to match default: null nodes_max (optional) <span class="param-type">Query
Parameter</span> — Number of nodes high range default: null nodes_min (optional)
<span class="param-type">Query Parameter</span> — Number of nodes low range default: null partition
(optional) <span class="param-type">Query Parameter</span> — Comma delimited list of partitions to
match default: null qos (optional) <span class="param-type">Query Parameter</span> — Comma delimited
list of QOS to match default: null reason (optional) <span class="param-type">Query Parameter</span>
— Comma delimited list of job reasons to match default: null reservation (optional)
<span class="param-type">Query Parameter</span> — Comma delimited list of reservations to match
default: null state (optional) <span class="param-type">Query Parameter</span> — Comma delimited
list of states to match default: null step (optional) <span class="param-type">Query
Parameter</span> — Comma delimited list of job steps to match default: null node (optional)
<span class="param-type">Query Parameter</span> — Comma delimited list of used nodes to match
default: null wckey (optional) <span class="param-type">Query Parameter</span> — Comma delimited
list of wckeys to match default: null

### Return type

[dbv0.0.39_job_info](#dbv0.0.39_job_info)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "jobs" : [ {
    "container" : "container",
    "cluster" : "cluster",
    "flags" : [ "NONE", "NONE" ],
    "used_gres" : "used_gres",
    "association" : {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    },
    "allocation_nodes" : 5,
    "working_directory" : "working_directory",
    "constraints" : "constraints",
    "required" : {
      "memory_per_node" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "memory" : 6,
      "CPUs" : 9,
      "memory_per_cpu" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "hold" : true,
    "partition" : "partition",
    "qos" : "qos",
    "array" : {
      "task" : "task",
      "job_id" : 2,
      "task_id" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "limits" : {
        "max" : {
          "running" : {
            "tasks" : 7
          }
        }
      }
    },
    "het" : {
      "job_id" : 4,
      "job_offset" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "submit_line" : "submit_line",
    "extra" : "extra",
    "reservation" : {
      "name" : "name",
      "id" : 8
    },
    "block" : "block",
    "tres" : {
      "requested" : [ {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      }, {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      } ],
      "allocated" : [ {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      }, {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      } ]
    },
    "state" : {
      "reason" : "reason",
      "current" : "current"
    },
    "mcs" : {
      "label" : "label"
    },
    "group" : "group",
    "wckey" : {
      "wckey" : "wckey",
      "flags" : [ "ASSIGNED_DEFAULT", "ASSIGNED_DEFAULT" ]
    },
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "steps" : [ {
      "nodes" : {
        "count" : 6,
        "range" : "range",
        "list" : [ "list", "list" ]
      },
      "task" : {
        "distribution" : "distribution"
      },
      "exit_code" : {
        "return_code" : 3,
        "signal" : {
          "name" : "name",
          "signal_id" : 2
        },
        "status" : "status"
      },
      "kill_request_user" : "kill_request_user",
      "CPU" : {
        "governor" : "governor",
        "requested_frequency" : {
          "min" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "max" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "pid" : "pid",
      "step" : {
        "name" : "name",
        "id" : {
          "job_id" : 6,
          "step_het_component" : 3,
          "step_id" : "step_id"
        }
      },
      "tres" : {
        "consumed" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "requested" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "allocated" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ]
      },
      "time" : {
        "elapsed" : 9,
        "total" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "system" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "start" : 3,
        "end" : 6,
        "user" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "suspended" : 6
      },
      "state" : "state",
      "tasks" : {
        "count" : 6
      },
      "statistics" : {
        "CPU" : {
          "actual_frequency" : 5
        },
        "energy" : {
          "consumed" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    }, {
      "nodes" : {
        "count" : 6,
        "range" : "range",
        "list" : [ "list", "list" ]
      },
      "task" : {
        "distribution" : "distribution"
      },
      "exit_code" : {
        "return_code" : 3,
        "signal" : {
          "name" : "name",
          "signal_id" : 2
        },
        "status" : "status"
      },
      "kill_request_user" : "kill_request_user",
      "CPU" : {
        "governor" : "governor",
        "requested_frequency" : {
          "min" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "max" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "pid" : "pid",
      "step" : {
        "name" : "name",
        "id" : {
          "job_id" : 6,
          "step_het_component" : 3,
          "step_id" : "step_id"
        }
      },
      "tres" : {
        "consumed" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "requested" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "allocated" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ]
      },
      "time" : {
        "elapsed" : 9,
        "total" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "system" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "start" : 3,
        "end" : 6,
        "user" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "suspended" : 6
      },
      "state" : "state",
      "tasks" : {
        "count" : 6
      },
      "statistics" : {
        "CPU" : {
          "actual_frequency" : 5
        },
        "energy" : {
          "consumed" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    } ],
    "script" : "script",
    "failed_node" : "failed_node",
    "derived_exit_code" : {
      "return_code" : 3,
      "signal" : {
        "name" : "name",
        "signal_id" : 2
      },
      "status" : "status"
    },
    "licenses" : "licenses",
    "nodes" : "nodes",
    "job_id" : 5,
    "exit_code" : {
      "return_code" : 3,
      "signal" : {
        "name" : "name",
        "signal_id" : 2
      },
      "status" : "status"
    },
    "name" : "name",
    "kill_request_user" : "kill_request_user",
    "comment" : {
      "administrator" : "administrator",
      "system" : "system",
      "job" : "job"
    },
    "time" : {
      "elapsed" : 4,
      "total" : {
        "seconds" : 7,
        "microseconds" : 1
      },
      "system" : {
        "seconds" : 7,
        "microseconds" : 1
      },
      "eligible" : 7,
      "start" : 1,
      "limit" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "end" : 1,
      "submission" : 1,
      "user" : {
        "seconds" : 7,
        "microseconds" : 1
      },
      "suspended" : 6
    },
    "user" : "user",
    "account" : "account"
  }, {
    "container" : "container",
    "cluster" : "cluster",
    "flags" : [ "NONE", "NONE" ],
    "used_gres" : "used_gres",
    "association" : {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    },
    "allocation_nodes" : 5,
    "working_directory" : "working_directory",
    "constraints" : "constraints",
    "required" : {
      "memory_per_node" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "memory" : 6,
      "CPUs" : 9,
      "memory_per_cpu" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "hold" : true,
    "partition" : "partition",
    "qos" : "qos",
    "array" : {
      "task" : "task",
      "job_id" : 2,
      "task_id" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "limits" : {
        "max" : {
          "running" : {
            "tasks" : 7
          }
        }
      }
    },
    "het" : {
      "job_id" : 4,
      "job_offset" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "submit_line" : "submit_line",
    "extra" : "extra",
    "reservation" : {
      "name" : "name",
      "id" : 8
    },
    "block" : "block",
    "tres" : {
      "requested" : [ {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      }, {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      } ],
      "allocated" : [ {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      }, {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      } ]
    },
    "state" : {
      "reason" : "reason",
      "current" : "current"
    },
    "mcs" : {
      "label" : "label"
    },
    "group" : "group",
    "wckey" : {
      "wckey" : "wckey",
      "flags" : [ "ASSIGNED_DEFAULT", "ASSIGNED_DEFAULT" ]
    },
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "steps" : [ {
      "nodes" : {
        "count" : 6,
        "range" : "range",
        "list" : [ "list", "list" ]
      },
      "task" : {
        "distribution" : "distribution"
      },
      "exit_code" : {
        "return_code" : 3,
        "signal" : {
          "name" : "name",
          "signal_id" : 2
        },
        "status" : "status"
      },
      "kill_request_user" : "kill_request_user",
      "CPU" : {
        "governor" : "governor",
        "requested_frequency" : {
          "min" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "max" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "pid" : "pid",
      "step" : {
        "name" : "name",
        "id" : {
          "job_id" : 6,
          "step_het_component" : 3,
          "step_id" : "step_id"
        }
      },
      "tres" : {
        "consumed" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "requested" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "allocated" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ]
      },
      "time" : {
        "elapsed" : 9,
        "total" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "system" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "start" : 3,
        "end" : 6,
        "user" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "suspended" : 6
      },
      "state" : "state",
      "tasks" : {
        "count" : 6
      },
      "statistics" : {
        "CPU" : {
          "actual_frequency" : 5
        },
        "energy" : {
          "consumed" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    }, {
      "nodes" : {
        "count" : 6,
        "range" : "range",
        "list" : [ "list", "list" ]
      },
      "task" : {
        "distribution" : "distribution"
      },
      "exit_code" : {
        "return_code" : 3,
        "signal" : {
          "name" : "name",
          "signal_id" : 2
        },
        "status" : "status"
      },
      "kill_request_user" : "kill_request_user",
      "CPU" : {
        "governor" : "governor",
        "requested_frequency" : {
          "min" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "max" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "pid" : "pid",
      "step" : {
        "name" : "name",
        "id" : {
          "job_id" : 6,
          "step_het_component" : 3,
          "step_id" : "step_id"
        }
      },
      "tres" : {
        "consumed" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "requested" : {
          "average" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "min" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "max" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ]
        },
        "allocated" : [ {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        }, {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        } ]
      },
      "time" : {
        "elapsed" : 9,
        "total" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "system" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "start" : 3,
        "end" : 6,
        "user" : {
          "seconds" : 1,
          "microseconds" : 2
        },
        "suspended" : 6
      },
      "state" : "state",
      "tasks" : {
        "count" : 6
      },
      "statistics" : {
        "CPU" : {
          "actual_frequency" : 5
        },
        "energy" : {
          "consumed" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      }
    } ],
    "script" : "script",
    "failed_node" : "failed_node",
    "derived_exit_code" : {
      "return_code" : 3,
      "signal" : {
        "name" : "name",
        "signal_id" : 2
      },
      "status" : "status"
    },
    "licenses" : "licenses",
    "nodes" : "nodes",
    "job_id" : 5,
    "exit_code" : {
      "return_code" : 3,
      "signal" : {
        "name" : "name",
        "signal_id" : 2
      },
      "status" : "status"
    },
    "name" : "name",
    "kill_request_user" : "kill_request_user",
    "comment" : {
      "administrator" : "administrator",
      "system" : "system",
      "job" : "job"
    },
    "time" : {
      "elapsed" : 4,
      "total" : {
        "seconds" : 7,
        "microseconds" : 1
      },
      "system" : {
        "seconds" : 7,
        "microseconds" : 1
      },
      "eligible" : 7,
      "start" : 1,
      "limit" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "end" : 1,
      "submission" : 1,
      "user" : {
        "seconds" : 7,
        "microseconds" : 1
      },
      "suspended" : 6
    },
    "user" : "user",
    "account" : "account"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of jobs [dbv0.0.39_job_info](#dbv0.0.39_job_info)

#### default

Unable to query jobs [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetQos"></span> <span id="slurmdbV0039GetQos"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/qos
```

Get QOS list (<span class="nickname">slurmdbV0039GetQos</span>)

### Query parameters

with_deleted (optional) <span class="param-type">Query Parameter</span> — Include deleted QOSs.
False by default. default: false

### Return type

[dbv0.0.39_qos_info](#dbv0.0.39_qos_info)

### Example data

Content-Type: application/json

``` example
{
  "qos" : [ {
    "flags" : [ "NOT_SET", "NOT_SET" ],
    "name" : "name",
    "usage_threshold" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "description" : "description",
    "usage_factor" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "id" : 1,
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "limits" : {
      "min" : {
        "priority_threshold" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "tres" : {
          "per" : {
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        }
      },
      "max" : {
        "jobs" : {
          "per" : {
            "user" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "account" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          },
          "active_jobs" : {
            "per" : {
              "user" : {
                "number" : 9,
                "set" : false,
                "infinite" : true
              },
              "account" : {
                "number" : 9,
                "set" : false,
                "infinite" : true
              }
            }
          }
        },
        "accruing" : {
          "per" : {
            "user" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "account" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          }
        },
        "tres" : {
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "minutes" : {
            "per" : {
              "qos" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "job" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "user" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "account" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ]
            }
          },
          "per" : {
            "node" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "user" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "account" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        },
        "wall_clock" : {
          "per" : {
            "qos" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "job" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          }
        },
        "active_jobs" : {
          "count" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "accruing" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "factor" : 4.965218492984954,
      "grace_time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "preempt" : {
      "mode" : [ "DISABLED", "DISABLED" ],
      "exempt_time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "list" : [ "list", "list" ]
    }
  }, {
    "flags" : [ "NOT_SET", "NOT_SET" ],
    "name" : "name",
    "usage_threshold" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "description" : "description",
    "usage_factor" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "id" : 1,
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "limits" : {
      "min" : {
        "priority_threshold" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "tres" : {
          "per" : {
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        }
      },
      "max" : {
        "jobs" : {
          "per" : {
            "user" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "account" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          },
          "active_jobs" : {
            "per" : {
              "user" : {
                "number" : 9,
                "set" : false,
                "infinite" : true
              },
              "account" : {
                "number" : 9,
                "set" : false,
                "infinite" : true
              }
            }
          }
        },
        "accruing" : {
          "per" : {
            "user" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "account" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          }
        },
        "tres" : {
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "minutes" : {
            "per" : {
              "qos" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "job" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "user" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "account" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ]
            }
          },
          "per" : {
            "node" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "user" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "account" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        },
        "wall_clock" : {
          "per" : {
            "qos" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "job" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          }
        },
        "active_jobs" : {
          "count" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "accruing" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "factor" : 4.965218492984954,
      "grace_time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "preempt" : {
      "mode" : [ "DISABLED", "DISABLED" ],
      "exempt_time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "list" : [ "list", "list" ]
    }
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of QOS' [dbv0.0.39_qos_info](#dbv0.0.39_qos_info)

#### default

QOS not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetSingleQos"></span> <span id="slurmdbV0039GetSingleQos"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/qos/{qos_name}
```

Get QOS info (<span class="nickname">slurmdbV0039GetSingleQos</span>)

### Path parameters

qos_name (required) <span class="param-type">Path Parameter</span> — Slurm QOS Name default: null

### Query parameters

with_deleted (optional) <span class="param-type">Query Parameter</span> — Include deleted QOSs.
False by default. default: false

### Return type

[dbv0.0.39_qos_info](#dbv0.0.39_qos_info)

### Example data

Content-Type: application/json

``` example
{
  "qos" : [ {
    "flags" : [ "NOT_SET", "NOT_SET" ],
    "name" : "name",
    "usage_threshold" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "description" : "description",
    "usage_factor" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "id" : 1,
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "limits" : {
      "min" : {
        "priority_threshold" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "tres" : {
          "per" : {
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        }
      },
      "max" : {
        "jobs" : {
          "per" : {
            "user" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "account" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          },
          "active_jobs" : {
            "per" : {
              "user" : {
                "number" : 9,
                "set" : false,
                "infinite" : true
              },
              "account" : {
                "number" : 9,
                "set" : false,
                "infinite" : true
              }
            }
          }
        },
        "accruing" : {
          "per" : {
            "user" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "account" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          }
        },
        "tres" : {
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "minutes" : {
            "per" : {
              "qos" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "job" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "user" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "account" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ]
            }
          },
          "per" : {
            "node" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "user" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "account" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        },
        "wall_clock" : {
          "per" : {
            "qos" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "job" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          }
        },
        "active_jobs" : {
          "count" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "accruing" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "factor" : 4.965218492984954,
      "grace_time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "preempt" : {
      "mode" : [ "DISABLED", "DISABLED" ],
      "exempt_time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "list" : [ "list", "list" ]
    }
  }, {
    "flags" : [ "NOT_SET", "NOT_SET" ],
    "name" : "name",
    "usage_threshold" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "description" : "description",
    "usage_factor" : {
      "number" : 5.025004791520295,
      "set" : false,
      "infinite" : true
    },
    "id" : 1,
    "priority" : {
      "number" : 9,
      "set" : false,
      "infinite" : true
    },
    "limits" : {
      "min" : {
        "priority_threshold" : {
          "number" : 9,
          "set" : false,
          "infinite" : true
        },
        "tres" : {
          "per" : {
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        }
      },
      "max" : {
        "jobs" : {
          "per" : {
            "user" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "account" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          },
          "active_jobs" : {
            "per" : {
              "user" : {
                "number" : 9,
                "set" : false,
                "infinite" : true
              },
              "account" : {
                "number" : 9,
                "set" : false,
                "infinite" : true
              }
            }
          }
        },
        "accruing" : {
          "per" : {
            "user" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "account" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          }
        },
        "tres" : {
          "total" : [ {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          }, {
            "name" : "name",
            "count" : 7,
            "id" : 3,
            "type" : "type"
          } ],
          "minutes" : {
            "per" : {
              "qos" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "job" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "user" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ],
              "account" : [ {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              }, {
                "name" : "name",
                "count" : 7,
                "id" : 3,
                "type" : "type"
              } ]
            }
          },
          "per" : {
            "node" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "job" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "user" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ],
            "account" : [ {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            }, {
              "name" : "name",
              "count" : 7,
              "id" : 3,
              "type" : "type"
            } ]
          }
        },
        "wall_clock" : {
          "per" : {
            "qos" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            },
            "job" : {
              "number" : 9,
              "set" : false,
              "infinite" : true
            }
          }
        },
        "active_jobs" : {
          "count" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          },
          "accruing" : {
            "number" : 9,
            "set" : false,
            "infinite" : true
          }
        }
      },
      "factor" : 4.965218492984954,
      "grace_time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      }
    },
    "preempt" : {
      "mode" : [ "DISABLED", "DISABLED" ],
      "exempt_time" : {
        "number" : 9,
        "set" : false,
        "infinite" : true
      },
      "list" : [ "list", "list" ]
    }
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

QOS information [dbv0.0.39_qos_info](#dbv0.0.39_qos_info)

#### default

QOS not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetTres"></span> <span id="slurmdbV0039GetTres"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/tres
```

Get TRES info (<span class="nickname">slurmdbV0039GetTres</span>)

### Return type

[dbv0.0.39_tres_info](#dbv0.0.39_tres_info)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "tres" : [ {
    "name" : "name",
    "count" : 7,
    "id" : 3,
    "type" : "type"
  }, {
    "name" : "name",
    "count" : 7,
    "id" : 3,
    "type" : "type"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of TRES [dbv0.0.39_tres_info](#dbv0.0.39_tres_info)

#### default

Unable to retrieve TRES [](rest_api.md)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetUser"></span> <span id="slurmdbV0039GetUser"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/user/{user_name}
```

Get user info (<span class="nickname">slurmdbV0039GetUser</span>)

### Path parameters

user_name (required) <span class="param-type">Path Parameter</span> — Slurm User Name default: null

### Query parameters

with_deleted (optional) <span class="param-type">Query Parameter</span> — Include deleted users.
False by default. default: false

### Return type

[dbv0.0.39_user_info](#dbv0.0.39_user_info)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ],
  "users" : [ {
    "associations" : [ {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    }, {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    } ],
    "default" : {
      "wckey" : "wckey",
      "account" : "account"
    },
    "administrator_level" : [ "Not Set", "Not Set" ],
    "old_name" : "old_name",
    "wckeys" : [ {
      "cluster" : "cluster",
      "name" : "name",
      "flags" : [ "DELETED", "DELETED" ],
      "accounting" : [ {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      }, {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      } ],
      "id" : 7,
      "user" : "user"
    }, {
      "cluster" : "cluster",
      "name" : "name",
      "flags" : [ "DELETED", "DELETED" ],
      "accounting" : [ {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      }, {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      } ],
      "id" : 7,
      "user" : "user"
    } ],
    "coordinators" : [ {
      "name" : "name",
      "direct" : true
    }, {
      "name" : "name",
      "direct" : true
    } ],
    "flags" : [ "NONE", "NONE" ],
    "name" : "name"
  }, {
    "associations" : [ {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    }, {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    } ],
    "default" : {
      "wckey" : "wckey",
      "account" : "account"
    },
    "administrator_level" : [ "Not Set", "Not Set" ],
    "old_name" : "old_name",
    "wckeys" : [ {
      "cluster" : "cluster",
      "name" : "name",
      "flags" : [ "DELETED", "DELETED" ],
      "accounting" : [ {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      }, {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      } ],
      "id" : 7,
      "user" : "user"
    }, {
      "cluster" : "cluster",
      "name" : "name",
      "flags" : [ "DELETED", "DELETED" ],
      "accounting" : [ {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      }, {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      } ],
      "id" : 7,
      "user" : "user"
    } ],
    "coordinators" : [ {
      "name" : "name",
      "direct" : true
    }, {
      "name" : "name",
      "direct" : true
    } ],
    "flags" : [ "NONE", "NONE" ],
    "name" : "name"
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of users [dbv0.0.39_user_info](#dbv0.0.39_user_info)

#### default

User not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetUsers"></span> <span id="slurmdbV0039GetUsers"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/users
```

Get user list (<span class="nickname">slurmdbV0039GetUsers</span>)

### Query parameters

with_deleted (optional) <span class="param-type">Query Parameter</span> — Include deleted users.
False by default. default: false

### Return type

[dbv0.0.39_user_info](#dbv0.0.39_user_info)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ],
  "users" : [ {
    "associations" : [ {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    }, {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    } ],
    "default" : {
      "wckey" : "wckey",
      "account" : "account"
    },
    "administrator_level" : [ "Not Set", "Not Set" ],
    "old_name" : "old_name",
    "wckeys" : [ {
      "cluster" : "cluster",
      "name" : "name",
      "flags" : [ "DELETED", "DELETED" ],
      "accounting" : [ {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      }, {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      } ],
      "id" : 7,
      "user" : "user"
    }, {
      "cluster" : "cluster",
      "name" : "name",
      "flags" : [ "DELETED", "DELETED" ],
      "accounting" : [ {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      }, {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      } ],
      "id" : 7,
      "user" : "user"
    } ],
    "coordinators" : [ {
      "name" : "name",
      "direct" : true
    }, {
      "name" : "name",
      "direct" : true
    } ],
    "flags" : [ "NONE", "NONE" ],
    "name" : "name"
  }, {
    "associations" : [ {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    }, {
      "cluster" : "cluster",
      "partition" : "partition",
      "user" : "user",
      "account" : "account"
    } ],
    "default" : {
      "wckey" : "wckey",
      "account" : "account"
    },
    "administrator_level" : [ "Not Set", "Not Set" ],
    "old_name" : "old_name",
    "wckeys" : [ {
      "cluster" : "cluster",
      "name" : "name",
      "flags" : [ "DELETED", "DELETED" ],
      "accounting" : [ {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      }, {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      } ],
      "id" : 7,
      "user" : "user"
    }, {
      "cluster" : "cluster",
      "name" : "name",
      "flags" : [ "DELETED", "DELETED" ],
      "accounting" : [ {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      }, {
        "start" : 6,
        "id" : 1,
        "TRES" : {
          "name" : "name",
          "count" : 7,
          "id" : 3,
          "type" : "type"
        },
        "allocated" : {
          "seconds" : 1
        }
      } ],
      "id" : 7,
      "user" : "user"
    } ],
    "coordinators" : [ {
      "name" : "name",
      "direct" : true
    }, {
      "name" : "name",
      "direct" : true
    } ],
    "flags" : [ "NONE", "NONE" ],
    "name" : "name"
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of users [dbv0.0.39_user_info](#dbv0.0.39_user_info)

#### default

User not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetWckey"></span> <span id="slurmdbV0039GetWckey"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/wckey/{wckey}
```

Get wckey info (<span class="nickname">slurmdbV0039GetWckey</span>)

### Path parameters

wckey (required) <span class="param-type">Path Parameter</span> — Slurm wckey name default: null

### Return type

[dbv0.0.39_wckey_info](#dbv0.0.39_wckey_info)

### Example data

Content-Type: application/json

``` example
{
  "wckeys" : [ {
    "cluster" : "cluster",
    "name" : "name",
    "flags" : [ "DELETED", "DELETED" ],
    "accounting" : [ {
      "start" : 6,
      "id" : 1,
      "TRES" : {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      },
      "allocated" : {
        "seconds" : 1
      }
    }, {
      "start" : 6,
      "id" : 1,
      "TRES" : {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      },
      "allocated" : {
        "seconds" : 1
      }
    } ],
    "id" : 7,
    "user" : "user"
  }, {
    "cluster" : "cluster",
    "name" : "name",
    "flags" : [ "DELETED", "DELETED" ],
    "accounting" : [ {
      "start" : 6,
      "id" : 1,
      "TRES" : {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      },
      "allocated" : {
        "seconds" : 1
      }
    }, {
      "start" : 6,
      "id" : 1,
      "TRES" : {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      },
      "allocated" : {
        "seconds" : 1
      }
    } ],
    "id" : 7,
    "user" : "user"
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of wckey [dbv0.0.39_wckey_info](#dbv0.0.39_wckey_info)

#### default

wckey not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039GetWckeys"></span> <span id="slurmdbV0039GetWckeys"></span>
<a href="#__Methods" class="up">Up</a>

``` get
get /slurmdb/v0.0.39/wckeys
```

Get wckey list (<span class="nickname">slurmdbV0039GetWckeys</span>)

### Return type

[dbv0.0.39_wckey_info](#dbv0.0.39_wckey_info)

### Example data

Content-Type: application/json

``` example
{
  "wckeys" : [ {
    "cluster" : "cluster",
    "name" : "name",
    "flags" : [ "DELETED", "DELETED" ],
    "accounting" : [ {
      "start" : 6,
      "id" : 1,
      "TRES" : {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      },
      "allocated" : {
        "seconds" : 1
      }
    }, {
      "start" : 6,
      "id" : 1,
      "TRES" : {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      },
      "allocated" : {
        "seconds" : 1
      }
    } ],
    "id" : 7,
    "user" : "user"
  }, {
    "cluster" : "cluster",
    "name" : "name",
    "flags" : [ "DELETED", "DELETED" ],
    "accounting" : [ {
      "start" : 6,
      "id" : 1,
      "TRES" : {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      },
      "allocated" : {
        "seconds" : 1
      }
    }, {
      "start" : 6,
      "id" : 1,
      "TRES" : {
        "name" : "name",
        "count" : 7,
        "id" : 3,
        "type" : "type"
      },
      "allocated" : {
        "seconds" : 1
      }
    } ],
    "id" : 7,
    "user" : "user"
  } ],
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 5
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of wckeys [dbv0.0.39_wckey_info](#dbv0.0.39_wckey_info)

#### default

wckey not found [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039SetConfig"></span> <span id="slurmdbV0039SetConfig"></span>
<a href="#__Methods" class="up">Up</a>

``` post
post /slurmdb/v0.0.39/config
```

Load all configuration information (<span class="nickname">slurmdbV0039SetConfig</span>)

### Consumes

This API call consumes the following media types via the <span class="header">Content-Type</span>
request header:

- `application/json`
- `application/x-yaml`

### Request body

dbv0.0.39_set_config [dbv0.0.39_set_config](#dbv0.0.39_set_config) (optional)
<span class="param-type">Body Parameter</span> —

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

Load config [status](#status)

#### default

Unable to set config [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039UpdateAccounts"></span> <span id="slurmdbV0039UpdateAccounts"></span>
<a href="#__Methods" class="up">Up</a>

``` post
post /slurmdb/v0.0.39/accounts
```

Update accounts (<span class="nickname">slurmdbV0039UpdateAccounts</span>)

### Consumes

This API call consumes the following media types via the <span class="header">Content-Type</span>
request header:

- `application/json`
- `application/x-yaml`

### Request body

dbv0.0.39_account_info [dbv0.0.39_account_info](#dbv0.0.39_account_info) (required)
<span class="param-type">Body Parameter</span> —

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

Add/update list of accounts [status](#status)

#### default

Unable to add or update accounts [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039UpdateAssociations"></span> <span id="slurmdbV0039UpdateAssociations"></span>
<a href="#__Methods" class="up">Up</a>

``` post
post /slurmdb/v0.0.39/associations
```

Set associations info (<span class="nickname">slurmdbV0039UpdateAssociations</span>)

### Consumes

This API call consumes the following media types via the <span class="header">Content-Type</span>
request header:

- `application/json`
- `application/x-yaml`

### Request body

dbv0.0.39_associations_info [dbv0.0.39_associations_info](#dbv0.0.39_associations_info) (required)
<span class="param-type">Body Parameter</span> —

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

status of associations update [status](#status)

#### default

Unable to update associations [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039UpdateQos"></span> <span id="slurmdbV0039UpdateQos"></span>
<a href="#__Methods" class="up">Up</a>

``` post
post /slurmdb/v0.0.39/qos
```

Set QOS info (<span class="nickname">slurmdbV0039UpdateQos</span>)

### Consumes

This API call consumes the following media types via the <span class="header">Content-Type</span>
request header:

- `application/json`
- `application/x-yaml`

### Request body

dbv0.0.39_update_qos [dbv0.0.39_update_qos](#dbv0.0.39_update_qos) (required)
<span class="param-type">Body Parameter</span> —

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

QOS update response [status](#status)

#### default

Unable to update QOSs [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039UpdateTres"></span> <span id="slurmdbV0039UpdateTres"></span>
<a href="#__Methods" class="up">Up</a>

``` post
post /slurmdb/v0.0.39/tres
```

Set TRES info (<span class="nickname">slurmdbV0039UpdateTres</span>)

### Consumes

This API call consumes the following media types via the <span class="header">Content-Type</span>
request header:

- `application/json`
- `application/x-yaml`

### Request body

dbv0.0.39_tres_update [dbv0.0.39_tres_update](#dbv0.0.39_tres_update) (required)
<span class="param-type">Body Parameter</span> —

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

List of TRES [status](#status)

#### default

Unable to update TRES [status](#status)

----------------------------------------------------------------------------------------------------

<span id="slurmdbV0039UpdateUsers"></span> <span id="slurmdbV0039UpdateUsers"></span>
<a href="#__Methods" class="up">Up</a>

``` post
post /slurmdb/v0.0.39/users
```

Update user (<span class="nickname">slurmdbV0039UpdateUsers</span>)

### Consumes

This API call consumes the following media types via the <span class="header">Content-Type</span>
request header:

- `application/json`
- `application/x-yaml`

### Request body

dbv0.0.39_update_users [dbv0.0.39_update_users](#dbv0.0.39_update_users) (required)
<span class="param-type">Body Parameter</span> —

### Return type

[status](#status)

### Example data

Content-Type: application/json

``` example
{
  "meta" : {
    "Slurm" : {
      "release" : "release",
      "version" : {
        "major" : 0,
        "minor" : 1,
        "micro" : 6
      }
    },
    "plugin" : {
      "name" : "name",
      "type" : "type"
    }
  },
  "warnings" : [ {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  }, {
    "warning" : "warning",
    "description" : "description",
    "source" : "source"
  } ],
  "errors" : [ {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  }, {
    "description" : "description",
    "source" : "source",
    "error" : "error",
    "error_number" : 0
  } ]
}
```

### Example data

Content-Type: application/x-yaml

``` example
Custom MIME type example not yet supported: application/x-yaml
```

### Produces

This API call produces the following media types according to the <span class="header">Accept</span>
request header; the media type will be conveyed by the <span class="header">Content-Type</span>
response header.

- `application/json`
- `application/x-yaml`

### Responses

#### 200

Update users [status](#status)

#### default

User not found or not able to update user [status](#status)

----------------------------------------------------------------------------------------------------

## <span id="__Models">Models</span>

\[ Jump to [Methods](#__Methods) \]

### Table of Contents

1.  [`dbv0.0.39_account_info` -](#dbv0.0.39_account_info)
2.  [`dbv0.0.39_associations_info` -](#dbv0.0.39_associations_info)
3.  [`dbv0.0.39_clusters_info` -](#dbv0.0.39_clusters_info)
4.  [`dbv0.0.39_config_info` -](#dbv0.0.39_config_info)
5.  [`dbv0.0.39_diag` -](#dbv0.0.39_diag)
6.  [`dbv0.0.39_error` -](#dbv0.0.39_error)
7.  [`dbv0.0.39_job_info` -](#dbv0.0.39_job_info)
8.  [`dbv0.0.39_meta` -](#dbv0.0.39_meta)
9.  [`dbv0.0.39_qos_info` -](#dbv0.0.39_qos_info)
10. [`dbv0.0.39_response_associations_delete` -](#dbv0.0.39_response_associations_delete)
11. [`dbv0.0.39_set_config` -](#dbv0.0.39_set_config)
12. [`dbv0.0.39_tres_info` -](#dbv0.0.39_tres_info)
13. [`dbv0.0.39_tres_update` -](#dbv0.0.39_tres_update)
14. [`dbv0.0.39_update_qos` -](#dbv0.0.39_update_qos)
15. [`dbv0.0.39_update_users` -](#dbv0.0.39_update_users)
16. [`dbv0.0.39_user_info` -](#dbv0.0.39_user_info)
17. [`dbv0.0.39_warning` -](#dbv0.0.39_warning)
18. [`dbv0.0.39_wckey_info` -](#dbv0.0.39_wckey_info)
19. [`dbv0_0_39_meta_Slurm` -](#dbv0_0_39_meta_Slurm)
20. [`dbv0_0_39_meta_Slurm_version` -](#dbv0_0_39_meta_Slurm_version)
21. [`dbv0_0_39_meta_plugin` -](#dbv0_0_39_meta_plugin)
22. [`status` -](#status)
23. [`v0.0.39_account` -](#v0.0.39_account)
24. [`v0.0.39_accounting` -](#v0.0.39_accounting)
25. [`v0.0.39_acct_gather_energy` -](#v0.0.39_acct_gather_energy)
26. [`v0.0.39_assoc` -](#v0.0.39_assoc)
27. [`v0.0.39_assoc_short` -](#v0.0.39_assoc_short)
28. [`v0.0.39_assoc_usage` -](#v0.0.39_assoc_usage)
29. [`v0.0.39_cluster_rec` -](#v0.0.39_cluster_rec)
30. [`v0.0.39_controller_ping` -](#v0.0.39_controller_ping)
31. [`v0.0.39_coord` -](#v0.0.39_coord)
32. [`v0.0.39_cron_entry` -](#v0.0.39_cron_entry)
33. [`v0.0.39_diag` -](#v0.0.39_diag)
34. [`v0.0.39_error` -](#v0.0.39_error)
35. [`v0.0.39_ext_sensors_data` -](#v0.0.39_ext_sensors_data)
36. [`v0.0.39_float64_no_val` -](#v0.0.39_float64_no_val)
37. [`v0.0.39_job` -](#v0.0.39_job)
38. [`v0.0.39_job_desc_msg` -](#v0.0.39_job_desc_msg)
39. [`v0.0.39_job_exit_code` -](#v0.0.39_job_exit_code)
40. [`v0.0.39_job_info` -](#v0.0.39_job_info)
41. [`v0.0.39_job_res` -](#v0.0.39_job_res)
42. [`v0.0.39_job_submission` -](#v0.0.39_job_submission)
43. [`v0.0.39_job_submission_response` -](#v0.0.39_job_submission_response)
44. [`v0.0.39_job_update_response` -](#v0.0.39_job_update_response)
45. [`v0.0.39_jobs_response` -](#v0.0.39_jobs_response)
46. [`v0.0.39_license` -](#v0.0.39_license)
47. [`v0.0.39_licenses_info` -](#v0.0.39_licenses_info)
48. [`v0.0.39_meta` -](#v0.0.39_meta)
49. [`v0.0.39_node` -](#v0.0.39_node)
50. [`v0.0.39_nodes_response` -](#v0.0.39_nodes_response)
51. [`v0.0.39_partition_info` -](#v0.0.39_partition_info)
52. [`v0.0.39_partitions_response` -](#v0.0.39_partitions_response)
53. [`v0.0.39_pings` -](#v0.0.39_pings)
54. [`v0.0.39_power_mgmt_data` -](#v0.0.39_power_mgmt_data)
55. [`v0.0.39_qos` -](#v0.0.39_qos)
56. [`v0.0.39_reservation_core_spec` -](#v0.0.39_reservation_core_spec)
57. [`v0.0.39_reservation_info` -](#v0.0.39_reservation_info)
58. [`v0.0.39_reservations_response` -](#v0.0.39_reservations_response)
59. [`v0.0.39_slurm_step_id` -](#v0.0.39_slurm_step_id)
60. [`v0.0.39_stats_msg` -](#v0.0.39_stats_msg)
61. [`v0.0.39_stats_rec` -](#v0.0.39_stats_rec)
62. [`v0.0.39_stats_rpc` -](#v0.0.39_stats_rpc)
63. [`v0.0.39_stats_user` -](#v0.0.39_stats_user)
64. [`v0.0.39_step` -](#v0.0.39_step)
65. [`v0.0.39_tres` -](#v0.0.39_tres)
66. [`v0.0.39_uint16_no_val` -](#v0.0.39_uint16_no_val)
67. [`v0.0.39_uint32_no_val` -](#v0.0.39_uint32_no_val)
68. [`v0.0.39_uint64_no_val` -](#v0.0.39_uint64_no_val)
69. [`v0.0.39_update_node_msg` -](#v0.0.39_update_node_msg)
70. [`v0.0.39_user` -](#v0.0.39_user)
71. [`v0.0.39_warning` -](#v0.0.39_warning)
72. [`v0.0.39_wckey` -](#v0.0.39_wckey)
73. [`v0.0.39_wckey_tag` -](#v0.0.39_wckey_tag)
74. [`v0_0_39_accounting_allocated` -](#v0_0_39_accounting_allocated)
75. [`v0_0_39_assoc_default` -](#v0_0_39_assoc_default)
76. [`v0_0_39_assoc_max` -](#v0_0_39_assoc_max)
77. [`v0_0_39_assoc_max_jobs` -](#v0_0_39_assoc_max_jobs)
78. [`v0_0_39_assoc_max_jobs_per` -](#v0_0_39_assoc_max_jobs_per)
79. [`v0_0_39_assoc_max_per` -](#v0_0_39_assoc_max_per)
80. [`v0_0_39_assoc_max_per_account` -](#v0_0_39_assoc_max_per_account)
81. [`v0_0_39_assoc_max_tres` -](#v0_0_39_assoc_max_tres)
82. [`v0_0_39_assoc_max_tres_group` -](#v0_0_39_assoc_max_tres_group)
83. [`v0_0_39_assoc_max_tres_minutes` -](#v0_0_39_assoc_max_tres_minutes)
84. [`v0_0_39_assoc_max_tres_minutes_per` -](#v0_0_39_assoc_max_tres_minutes_per)
85. [`v0_0_39_assoc_max_tres_per` -](#v0_0_39_assoc_max_tres_per)
86. [`v0_0_39_assoc_min` -](#v0_0_39_assoc_min)
87. [`v0_0_39_cluster_rec_associations` -](#v0_0_39_cluster_rec_associations)
88. [`v0_0_39_cluster_rec_controller` -](#v0_0_39_cluster_rec_controller)
89. [`v0_0_39_cron_entry_line` -](#v0_0_39_cron_entry_line)
90. [`v0_0_39_job_array` -](#v0_0_39_job_array)
91. [`v0_0_39_job_array_limits` -](#v0_0_39_job_array_limits)
92. [`v0_0_39_job_array_limits_max` -](#v0_0_39_job_array_limits_max)
93. [`v0_0_39_job_array_limits_max_running` -](#v0_0_39_job_array_limits_max_running)
94. [`v0_0_39_job_array_response_msg_inner` -](#v0_0_39_job_array_response_msg_inner)
95. [`v0_0_39_job_comment` -](#v0_0_39_job_comment)
96. [`v0_0_39_job_exit_code_signal` -](#v0_0_39_job_exit_code_signal)
97. [`v0_0_39_job_het` -](#v0_0_39_job_het)
98. [`v0_0_39_job_info_power` -](#v0_0_39_job_info_power)
99. [`v0_0_39_job_mcs` -](#v0_0_39_job_mcs)
100. [`v0_0_39_job_required` -](#v0_0_39_job_required)
101. [`v0_0_39_job_reservation` -](#v0_0_39_job_reservation)
102. [`v0_0_39_job_state` -](#v0_0_39_job_state)
103. [`v0_0_39_job_time` -](#v0_0_39_job_time)
104. [`v0_0_39_job_time_system` -](#v0_0_39_job_time_system)
105. [`v0_0_39_job_tres` -](#v0_0_39_job_tres)
106. [`v0_0_39_partition_info_accounts` -](#v0_0_39_partition_info_accounts)
107. [`v0_0_39_partition_info_cpus` -](#v0_0_39_partition_info_cpus)
108. [`v0_0_39_partition_info_defaults` -](#v0_0_39_partition_info_defaults)
109. [`v0_0_39_partition_info_groups` -](#v0_0_39_partition_info_groups)
110. [`v0_0_39_partition_info_maximums` -](#v0_0_39_partition_info_maximums)
111. [`v0_0_39_partition_info_minimums` -](#v0_0_39_partition_info_minimums)
112. [`v0_0_39_partition_info_nodes` -](#v0_0_39_partition_info_nodes)
113. [`v0_0_39_partition_info_priority` -](#v0_0_39_partition_info_priority)
114. [`v0_0_39_partition_info_qos` -](#v0_0_39_partition_info_qos)
115. [`v0_0_39_partition_info_timeouts` -](#v0_0_39_partition_info_timeouts)
116. [`v0_0_39_partition_info_tres` -](#v0_0_39_partition_info_tres)
117. [`v0_0_39_qos_limits` -](#v0_0_39_qos_limits)
118. [`v0_0_39_qos_limits_max` -](#v0_0_39_qos_limits_max)
119. [`v0_0_39_qos_limits_max_active_jobs` -](#v0_0_39_qos_limits_max_active_jobs)
120. [`v0_0_39_qos_limits_max_jobs` -](#v0_0_39_qos_limits_max_jobs)
121. [`v0_0_39_qos_limits_max_jobs_active_jobs` -](#v0_0_39_qos_limits_max_jobs_active_jobs)
122. [`v0_0_39_qos_limits_max_jobs_active_jobs_per` -](#v0_0_39_qos_limits_max_jobs_active_jobs_per)
123. [`v0_0_39_qos_limits_max_tres` -](#v0_0_39_qos_limits_max_tres)
124. [`v0_0_39_qos_limits_max_tres_minutes` -](#v0_0_39_qos_limits_max_tres_minutes)
125. [`v0_0_39_qos_limits_max_tres_minutes_per` -](#v0_0_39_qos_limits_max_tres_minutes_per)
126. [`v0_0_39_qos_limits_max_tres_per` -](#v0_0_39_qos_limits_max_tres_per)
127. [`v0_0_39_qos_limits_max_wall_clock` -](#v0_0_39_qos_limits_max_wall_clock)
128. [`v0_0_39_qos_limits_max_wall_clock_per` -](#v0_0_39_qos_limits_max_wall_clock_per)
129. [`v0_0_39_qos_limits_min` -](#v0_0_39_qos_limits_min)
130. [`v0_0_39_qos_limits_min_tres` -](#v0_0_39_qos_limits_min_tres)
131. [`v0_0_39_qos_preempt` -](#v0_0_39_qos_preempt)
132. [`v0_0_39_reservation_info_purge_completed` -](#v0_0_39_reservation_info_purge_completed)
133. [`v0_0_39_rollup_stats_inner` -](#v0_0_39_rollup_stats_inner)
134. [`v0_0_39_stats_msg_rpcs_by_type_inner` -](#v0_0_39_stats_msg_rpcs_by_type_inner)
135. [`v0_0_39_stats_msg_rpcs_by_user_inner` -](#v0_0_39_stats_msg_rpcs_by_user_inner)
136. [`v0_0_39_stats_rpc_time` -](#v0_0_39_stats_rpc_time)
137. [`v0_0_39_step_CPU` -](#v0_0_39_step_CPU)
138. [`v0_0_39_step_CPU_requested_frequency` -](#v0_0_39_step_CPU_requested_frequency)
139. [`v0_0_39_step_nodes` -](#v0_0_39_step_nodes)
140. [`v0_0_39_step_statistics` -](#v0_0_39_step_statistics)
141. [`v0_0_39_step_statistics_CPU` -](#v0_0_39_step_statistics_CPU)
142. [`v0_0_39_step_statistics_energy` -](#v0_0_39_step_statistics_energy)
143. [`v0_0_39_step_step` -](#v0_0_39_step_step)
144. [`v0_0_39_step_task` -](#v0_0_39_step_task)
145. [`v0_0_39_step_tasks` -](#v0_0_39_step_tasks)
146. [`v0_0_39_step_time` -](#v0_0_39_step_time)
147. [`v0_0_39_step_time_system` -](#v0_0_39_step_time_system)
148. [`v0_0_39_step_tres` -](#v0_0_39_step_tres)
149. [`v0_0_39_step_tres_consumed` -](#v0_0_39_step_tres_consumed)
150. [`v0_0_39_step_tres_requested` -](#v0_0_39_step_tres_requested)
151. [`v0_0_39_user_default` -](#v0_0_39_user_default)

### <span id="dbv0.0.39_account_info">`dbv0.0.39_account_info` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[dbv0.0.39_meta](#dbv0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[dbv0.0.39_error\]](#dbv0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[dbv0.0.39_warning\]](#dbv0.0.39_warning)</span>
Slurm warnings accounts
(optional)<span class="param-type">[array\[v0.0.39_account\]](#v0.0.39_account)</span>

### <span id="dbv0.0.39_associations_info">`dbv0.0.39_associations_info` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[dbv0.0.39_meta](#dbv0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[dbv0.0.39_error\]](#dbv0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[dbv0.0.39_warning\]](#dbv0.0.39_warning)</span>
Slurm warnings associations
(optional)<span class="param-type">[array\[v0.0.39_assoc\]](#v0.0.39_assoc)</span>

### <span id="dbv0.0.39_clusters_info">`dbv0.0.39_clusters_info` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[dbv0.0.39_meta](#dbv0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[dbv0.0.39_error\]](#dbv0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[dbv0.0.39_warning\]](#dbv0.0.39_warning)</span>
Slurm warnings clusters
(optional)<span class="param-type">[array\[v0.0.39_cluster_rec\]](#v0.0.39_cluster_rec)</span>

### <span id="dbv0.0.39_config_info">`dbv0.0.39_config_info` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[dbv0.0.39_meta](#dbv0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[dbv0.0.39_error\]](#dbv0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[dbv0.0.39_warning\]](#dbv0.0.39_warning)</span>
Slurm warnings tres (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>
accounts (optional)<span class="param-type">[array\[v0.0.39_account\]](#v0.0.39_account)</span>
associations (optional)<span class="param-type">[array\[v0.0.39_assoc\]](#v0.0.39_assoc)</span>
users (optional)<span class="param-type">[array\[v0.0.39_user\]](#v0.0.39_user)</span> qos
(optional)<span class="param-type">[array\[v0.0.39_qos\]](#v0.0.39_qos)</span> wckeys
(optional)<span class="param-type">[array\[v0.0.39_wckey\]](#v0.0.39_wckey)</span> clusters
(optional)<span class="param-type">[array\[v0.0.39_cluster_rec\]](#v0.0.39_cluster_rec)</span>

### <span id="dbv0.0.39_diag">`dbv0.0.39_diag` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[dbv0.0.39_meta](#dbv0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[dbv0.0.39_error\]](#dbv0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[dbv0.0.39_warning\]](#dbv0.0.39_warning)</span>
Slurm warnings statistics
(optional)<span class="param-type">[v0.0.39_stats_rec](#v0.0.39_stats_rec)</span>

### <span id="dbv0.0.39_error">`dbv0.0.39_error` -</span> <a href="#__Models" class="up">Up</a>

error_number (optional)<span class="param-type">[Integer](#integer)</span> Slurm internal error
number error (optional)<span class="param-type">[String](#string)</span> Error message source
(optional)<span class="param-type">[String](#string)</span> Where error occurred in the source
description (optional)<span class="param-type">[String](#string)</span> Explanation of cause of
error

### <span id="dbv0.0.39_job_info">`dbv0.0.39_job_info` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[dbv0.0.39_meta](#dbv0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[dbv0.0.39_error\]](#dbv0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[dbv0.0.39_warning\]](#dbv0.0.39_warning)</span>
Slurm warnings jobs (optional)<span class="param-type">[array\[v0.0.39_job\]](#v0.0.39_job)</span>

### <span id="dbv0.0.39_meta">`dbv0.0.39_meta` -</span> <a href="#__Models" class="up">Up</a>

plugin (optional)<span class="param-type">[dbv0_0_39_meta_plugin](#dbv0_0_39_meta_plugin)</span>
Slurm (optional)<span class="param-type">[dbv0_0_39_meta_Slurm](#dbv0_0_39_meta_Slurm)</span>

### <span id="dbv0.0.39_qos_info">`dbv0.0.39_qos_info` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[dbv0.0.39_meta](#dbv0.0.39_meta)</span> warnings
(optional)<span class="param-type">[array\[dbv0.0.39_warning\]](#dbv0.0.39_warning)</span> Slurm
warnings errors
(optional)<span class="param-type">[array\[dbv0.0.39_error\]](#dbv0.0.39_error)</span> Slurm errors
qos (optional)<span class="param-type">[array\[v0.0.39_qos\]](#v0.0.39_qos)</span>

### <span id="dbv0.0.39_response_associations_delete">`dbv0.0.39_response_associations_delete` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[dbv0.0.39_meta](#dbv0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[dbv0.0.39_error\]](#dbv0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[dbv0.0.39_warning\]](#dbv0.0.39_warning)</span>
Slurm warnings removed_associations
(optional)<span class="param-type">[array\[String\]](#string)</span> the associations

### <span id="dbv0.0.39_set_config">`dbv0.0.39_set_config` -</span> <a href="#__Models" class="up">Up</a>

clusters
(optional)<span class="param-type">[array\[v0.0.39_cluster_rec\]](#v0.0.39_cluster_rec)</span> TRES
(optional)<span class="param-type">[array\[List\]](#array)</span> accounts
(optional)<span class="param-type">[array\[v0.0.39_account\]](#v0.0.39_account)</span> users
(optional)<span class="param-type">[array\[v0.0.39_user\]](#v0.0.39_user)</span> qos
(optional)<span class="param-type">[array\[v0.0.39_qos\]](#v0.0.39_qos)</span> wckeys
(optional)<span class="param-type">[array\[v0.0.39_wckey\]](#v0.0.39_wckey)</span> associations
(optional)<span class="param-type">[array\[v0.0.39_assoc\]](#v0.0.39_assoc)</span>

### <span id="dbv0.0.39_tres_info">`dbv0.0.39_tres_info` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[dbv0.0.39_meta](#dbv0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[dbv0.0.39_error\]](#dbv0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[dbv0.0.39_warning\]](#dbv0.0.39_warning)</span>
Slurm warnings tres (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>

### <span id="dbv0.0.39_tres_update">`dbv0.0.39_tres_update` -</span> <a href="#__Models" class="up">Up</a>

tres (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>

### <span id="dbv0.0.39_update_qos">`dbv0.0.39_update_qos` -</span> <a href="#__Models" class="up">Up</a>

qos (optional)<span class="param-type">[array\[v0.0.39_qos\]](#v0.0.39_qos)</span>

### <span id="dbv0.0.39_update_users">`dbv0.0.39_update_users` -</span> <a href="#__Models" class="up">Up</a>

users (optional)<span class="param-type">[array\[v0.0.39_user\]](#v0.0.39_user)</span>

### <span id="dbv0.0.39_user_info">`dbv0.0.39_user_info` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[dbv0.0.39_meta](#dbv0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[dbv0.0.39_error\]](#dbv0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[dbv0.0.39_warning\]](#dbv0.0.39_warning)</span>
Slurm warnings users
(optional)<span class="param-type">[array\[v0.0.39_user\]](#v0.0.39_user)</span>

### <span id="dbv0.0.39_warning">`dbv0.0.39_warning` -</span> <a href="#__Models" class="up">Up</a>

warning (optional)<span class="param-type">[String](#string)</span> Earning message source
(optional)<span class="param-type">[String](#string)</span> Where error occurred in the source
description (optional)<span class="param-type">[String](#string)</span> Explanation of cause of
error

### <span id="dbv0.0.39_wckey_info">`dbv0.0.39_wckey_info` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[dbv0.0.39_meta](#dbv0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[dbv0.0.39_error\]](#dbv0.0.39_error)</span> Slurm errors
wckeys (optional)<span class="param-type">[array\[v0.0.39_wckey\]](#v0.0.39_wckey)</span>

### <span id="dbv0_0_39_meta_Slurm">`dbv0_0_39_meta_Slurm` -</span> <a href="#__Models" class="up">Up</a>

Slurm information version
(optional)<span class="param-type">[dbv0_0_39_meta_Slurm_version](#dbv0_0_39_meta_Slurm_version)</span>
release (optional)<span class="param-type">[String](#string)</span> version specifier

### <span id="dbv0_0_39_meta_Slurm_version">`dbv0_0_39_meta_Slurm_version` -</span> <a href="#__Models" class="up">Up</a>

major (optional)<span class="param-type">[Integer](#integer)</span> micro
(optional)<span class="param-type">[Integer](#integer)</span> minor
(optional)<span class="param-type">[Integer](#integer)</span>

### <span id="dbv0_0_39_meta_plugin">`dbv0_0_39_meta_plugin` -</span> <a href="#__Models" class="up">Up</a>

type (optional)<span class="param-type">[String](#string)</span> name
(optional)<span class="param-type">[String](#string)</span>

### <span id="status">`status` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[v0.0.39_meta](#v0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[v0.0.39_error\]](#v0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[v0.0.39_warning\]](#v0.0.39_warning)</span>
Slurm warnings

### <span id="v0.0.39_account">`v0.0.39_account` -</span> <a href="#__Models" class="up">Up</a>

associations
(optional)<span class="param-type">[array\[v0.0.39_assoc_short\]](#v0.0.39_assoc_short)</span>
coordinators (optional)<span class="param-type">[array\[v0.0.39_coord\]](#v0.0.39_coord)</span>
description <span class="param-type">[String](#string)</span> name
<span class="param-type">[String](#string)</span> organization
<span class="param-type">[String](#string)</span> flags
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum:

### <span id="v0.0.39_accounting">`v0.0.39_accounting` -</span> <a href="#__Models" class="up">Up</a>

allocated
(optional)<span class="param-type">[v0_0_39_accounting_allocated](#v0_0_39_accounting_allocated)</span>
id (optional)<span class="param-type">[Integer](#integer)</span> format: int32 start
(optional)<span class="param-type">[Long](#long)</span> format: int64 TRES
(optional)<span class="param-type">[v0.0.39_tres](#v0.0.39_tres)</span>

### <span id="v0.0.39_acct_gather_energy">`v0.0.39_acct_gather_energy` -</span> <a href="#__Models" class="up">Up</a>

average_watts (optional)<span class="param-type">[Integer](#integer)</span> format: int32
base_consumed_energy (optional)<span class="param-type">[Long](#long)</span> format: int64
consumed_energy (optional)<span class="param-type">[Long](#long)</span> format: int64 current_watts
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
previous_consumed_energy (optional)<span class="param-type">[Long](#long)</span> format: int64
last_collected (optional)<span class="param-type">[Long](#long)</span> format: int64

### <span id="v0.0.39_assoc">`v0.0.39_assoc` -</span> <a href="#__Models" class="up">Up</a>

account (optional)<span class="param-type">[String](#string)</span> cluster
(optional)<span class="param-type">[String](#string)</span> default
(optional)<span class="param-type">[v0_0_39_assoc_default](#v0_0_39_assoc_default)</span> flags
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: max
(optional)<span class="param-type">[v0_0_39_assoc_max](#v0_0_39_assoc_max)</span> is_default
(optional)<span class="param-type">[Boolean](#boolean)</span> min
(optional)<span class="param-type">[v0_0_39_assoc_min](#v0_0_39_assoc_min)</span> parent_account
(optional)<span class="param-type">[String](#string)</span> partition
(optional)<span class="param-type">[String](#string)</span> priority
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> qos
(optional)<span class="param-type">[array\[String\]](#string)</span> List of QOS names shares_raw
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 usage
(optional)<span class="param-type">[v0.0.39_assoc_usage](#v0.0.39_assoc_usage)</span> user
<span class="param-type">[String](#string)</span>

### <span id="v0.0.39_assoc_short">`v0.0.39_assoc_short` -</span> <a href="#__Models" class="up">Up</a>

account (optional)<span class="param-type">[String](#string)</span> cluster
(optional)<span class="param-type">[String](#string)</span> partition
(optional)<span class="param-type">[String](#string)</span> user
<span class="param-type">[String](#string)</span>

### <span id="v0.0.39_assoc_usage">`v0.0.39_assoc_usage` -</span> <a href="#__Models" class="up">Up</a>

accrue_job_count (optional)<span class="param-type">[Integer](#integer)</span> format: int32
group_used_wallclock (optional)<span class="param-type">[Double](#double)</span> format: double
fairshare_factor (optional)<span class="param-type">[Double](#double)</span> format: double
fairshare_shares (optional)<span class="param-type">[Integer](#integer)</span> format: int32
normalized_priority (optional)<span class="param-type">[Double](#double)</span> format: double
normalized_shares (optional)<span class="param-type">[Double](#double)</span> format: double
effective_normalized_usage (optional)<span class="param-type">[BigDecimal](#number)</span>
normalized_usage (optional)<span class="param-type">[BigDecimal](#number)</span> raw_usage
(optional)<span class="param-type">[BigDecimal](#number)</span> active_jobs
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 job_count
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 fairshare_level
(optional)<span class="param-type">[BigDecimal](#number)</span>

### <span id="v0.0.39_cluster_rec">`v0.0.39_cluster_rec` -</span> <a href="#__Models" class="up">Up</a>

controller
(optional)<span class="param-type">[v0_0_39_cluster_rec_controller](#v0_0_39_cluster_rec_controller)</span>
flags (optional)<span class="param-type">[array\[String\]](#string)</span> Enum: name
(optional)<span class="param-type">[String](#string)</span> nodes
(optional)<span class="param-type">[String](#string)</span> select_plugin
(optional)<span class="param-type">[String](#string)</span> associations
(optional)<span class="param-type">[v0_0_39_cluster_rec_associations](#v0_0_39_cluster_rec_associations)</span>
rpc_version (optional)<span class="param-type">[Integer](#integer)</span> format: int32 tres
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>

### <span id="v0.0.39_controller_ping">`v0.0.39_controller_ping` -</span> <a href="#__Models" class="up">Up</a>

hostname (optional)<span class="param-type">[String](#string)</span> pinged
(optional)<span class="param-type">[String](#string)</span> latency
(optional)<span class="param-type">[Long](#long)</span> format: int64 mode
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0.0.39_coord">`v0.0.39_coord` -</span> <a href="#__Models" class="up">Up</a>

name <span class="param-type">[String](#string)</span> direct
(optional)<span class="param-type">[Boolean](#boolean)</span>

### <span id="v0.0.39_cron_entry">`v0.0.39_cron_entry` -</span> <a href="#__Models" class="up">Up</a>

flags (optional)<span class="param-type">[array\[String\]](#string)</span> Enum: minute
(optional)<span class="param-type">[String](#string)</span> hour
(optional)<span class="param-type">[String](#string)</span> day_of_month
(optional)<span class="param-type">[String](#string)</span> month
(optional)<span class="param-type">[String](#string)</span> day_of_week
(optional)<span class="param-type">[String](#string)</span> specification
(optional)<span class="param-type">[String](#string)</span> command
(optional)<span class="param-type">[String](#string)</span> line
(optional)<span class="param-type">[v0_0_39_cron_entry_line](#v0_0_39_cron_entry_line)</span>

### <span id="v0.0.39_diag">`v0.0.39_diag` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[v0.0.39_meta](#v0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[v0.0.39_error\]](#v0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[v0.0.39_warning\]](#v0.0.39_warning)</span>
Slurm warnings statistics
(optional)<span class="param-type">[v0.0.39_stats_msg](#v0.0.39_stats_msg)</span>

### <span id="v0.0.39_error">`v0.0.39_error` -</span> <a href="#__Models" class="up">Up</a>

error_number (optional)<span class="param-type">[Integer](#integer)</span> Slurm internal error
number error (optional)<span class="param-type">[String](#string)</span> Error message source
(optional)<span class="param-type">[String](#string)</span> Where error occurred in the source
description (optional)<span class="param-type">[String](#string)</span> Explanation of cause of
error

### <span id="v0.0.39_ext_sensors_data">`v0.0.39_ext_sensors_data` -</span> <a href="#__Models" class="up">Up</a>

consumed_energy
(optional)<span class="param-type">[v0.0.39_uint64_no_val](#v0.0.39_uint64_no_val)</span>
temperature
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
energy_update_time (optional)<span class="param-type">[Long](#long)</span> format: int64
current_watts (optional)<span class="param-type">[Integer](#integer)</span> format: int32

### <span id="v0.0.39_float64_no_val">`v0.0.39_float64_no_val` -</span> <a href="#__Models" class="up">Up</a>

64 bit floating point number with flags set
(optional)<span class="param-type">[Boolean](#boolean)</span> True if number has been set. False if
number is unset infinite (optional)<span class="param-type">[Boolean](#boolean)</span> True if
number has been set to infinite. "set" and "number" will be ignored. number
(optional)<span class="param-type">[Double](#double)</span> If set is True the number will be set
with value. Otherwise ignore number contents. format: double

### <span id="v0.0.39_job">`v0.0.39_job` -</span> <a href="#__Models" class="up">Up</a>

account (optional)<span class="param-type">[String](#string)</span> comment
(optional)<span class="param-type">[v0_0_39_job_comment](#v0_0_39_job_comment)</span>
allocation_nodes (optional)<span class="param-type">[Integer](#integer)</span> format: int32 array
(optional)<span class="param-type">[v0_0_39_job_array](#v0_0_39_job_array)</span> association
(optional)<span class="param-type">[v0.0.39_assoc_short](#v0.0.39_assoc_short)</span> block
(optional)<span class="param-type">[String](#string)</span> cluster
(optional)<span class="param-type">[String](#string)</span> constraints
(optional)<span class="param-type">[String](#string)</span> container
(optional)<span class="param-type">[String](#string)</span> derived_exit_code
(optional)<span class="param-type">[v0.0.39_job_exit_code](#v0.0.39_job_exit_code)</span> time
(optional)<span class="param-type">[v0_0_39_job_time](#v0_0_39_job_time)</span> exit_code
(optional)<span class="param-type">[v0.0.39_job_exit_code](#v0.0.39_job_exit_code)</span> extra
(optional)<span class="param-type">[String](#string)</span> failed_node
(optional)<span class="param-type">[String](#string)</span> flags
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: group
(optional)<span class="param-type">[String](#string)</span> het
(optional)<span class="param-type">[v0_0_39_job_het](#v0_0_39_job_het)</span> job_id
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 name
(optional)<span class="param-type">[String](#string)</span> licenses
(optional)<span class="param-type">[String](#string)</span> mcs
(optional)<span class="param-type">[v0_0_39_job_mcs](#v0_0_39_job_mcs)</span> nodes
(optional)<span class="param-type">[String](#string)</span> partition
(optional)<span class="param-type">[String](#string)</span> hold
(optional)<span class="param-type">[Boolean](#boolean)</span> Hold (true) or release (false) job
priority (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
qos (optional)<span class="param-type">[String](#string)</span> required
(optional)<span class="param-type">[v0_0_39_job_required](#v0_0_39_job_required)</span>
kill_request_user (optional)<span class="param-type">[String](#string)</span> reservation
(optional)<span class="param-type">[v0_0_39_job_reservation](#v0_0_39_job_reservation)</span> script
(optional)<span class="param-type">[String](#string)</span> state
(optional)<span class="param-type">[v0_0_39_job_state](#v0_0_39_job_state)</span> steps
(optional)<span class="param-type">[array\[v0.0.39_step\]](#v0.0.39_step)</span> submit_line
(optional)<span class="param-type">[String](#string)</span> tres
(optional)<span class="param-type">[v0_0_39_job_tres](#v0_0_39_job_tres)</span> used_gres
(optional)<span class="param-type">[String](#string)</span> user
(optional)<span class="param-type">[String](#string)</span> wckey
(optional)<span class="param-type">[v0.0.39_wckey_tag](#v0.0.39_wckey_tag)</span> working_directory
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0.0.39_job_desc_msg">`v0.0.39_job_desc_msg` -</span> <a href="#__Models" class="up">Up</a>

account (optional)<span class="param-type">[String](#string)</span> account_gather_frequency
(optional)<span class="param-type">[String](#string)</span> admin_comment
(optional)<span class="param-type">[String](#string)</span> allocation_node_list
(optional)<span class="param-type">[String](#string)</span> allocation_node_port
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 argv
(optional)<span class="param-type">[array\[String\]](#string)</span> array
(optional)<span class="param-type">[String](#string)</span> batch_features
(optional)<span class="param-type">[String](#string)</span> begin_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 flags
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: burst_buffer
(optional)<span class="param-type">[String](#string)</span> clusters
(optional)<span class="param-type">[String](#string)</span> cluster_constraint
(optional)<span class="param-type">[String](#string)</span> comment
(optional)<span class="param-type">[String](#string)</span> contiguous
(optional)<span class="param-type">[Boolean](#boolean)</span> container
(optional)<span class="param-type">[String](#string)</span> container_id
(optional)<span class="param-type">[String](#string)</span> core_specification
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 thread_specification
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 cpu_binding
(optional)<span class="param-type">[String](#string)</span> cpu_binding_flags
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: cpu_frequency
(optional)<span class="param-type">[String](#string)</span> cpus_per_tres
(optional)<span class="param-type">[String](#string)</span> crontab
(optional)<span class="param-type">[v0.0.39_cron_entry](#v0.0.39_cron_entry)</span> deadline
(optional)<span class="param-type">[Long](#long)</span> format: int64 delay_boot
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 dependency
(optional)<span class="param-type">[String](#string)</span> end_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 environment
<span class="param-type">[array\[String\]](#string)</span> excluded_nodes
(optional)<span class="param-type">[array\[String\]](#string)</span> extra
(optional)<span class="param-type">[String](#string)</span> constraints
(optional)<span class="param-type">[String](#string)</span> group_id
(optional)<span class="param-type">[String](#string)</span> hetjob_group
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 immediate
(optional)<span class="param-type">[Boolean](#boolean)</span> job_id
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 kill_on_node_fail
(optional)<span class="param-type">[Boolean](#boolean)</span> licenses
(optional)<span class="param-type">[String](#string)</span> mail_type
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: mail_user
(optional)<span class="param-type">[String](#string)</span> mcs_label
(optional)<span class="param-type">[String](#string)</span> memory_binding
(optional)<span class="param-type">[String](#string)</span> memory_binding_type
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: memory_per_tres
(optional)<span class="param-type">[String](#string)</span> name
(optional)<span class="param-type">[String](#string)</span> network
(optional)<span class="param-type">[String](#string)</span> nice
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 tasks
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 open_mode
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: reserve_ports
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 overcommit
(optional)<span class="param-type">[Boolean](#boolean)</span> partition
(optional)<span class="param-type">[String](#string)</span> distribution_plane_size
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 power_flags
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: prefer
(optional)<span class="param-type">[String](#string)</span> hold
(optional)<span class="param-type">[Boolean](#boolean)</span> Hold (true) or release (false) job
priority (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
profile (optional)<span class="param-type">[array\[String\]](#string)</span> Enum: qos
(optional)<span class="param-type">[String](#string)</span> reboot
(optional)<span class="param-type">[Boolean](#boolean)</span> required_nodes
(optional)<span class="param-type">[array\[String\]](#string)</span> requeue
(optional)<span class="param-type">[Boolean](#boolean)</span> reservation
(optional)<span class="param-type">[String](#string)</span> script
(optional)<span class="param-type">[String](#string)</span> shared
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: exclusive
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: oversubscribe
(optional)<span class="param-type">[Boolean](#boolean)</span> site_factor
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 spank_environment
(optional)<span class="param-type">[array\[String\]](#string)</span> distribution
(optional)<span class="param-type">[String](#string)</span> time_limit
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
time_minimum
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> tres_bind
(optional)<span class="param-type">[String](#string)</span> tres_freq
(optional)<span class="param-type">[String](#string)</span> tres_per_job
(optional)<span class="param-type">[String](#string)</span> tres_per_node
(optional)<span class="param-type">[String](#string)</span> tres_per_socket
(optional)<span class="param-type">[String](#string)</span> tres_per_task
(optional)<span class="param-type">[String](#string)</span> user_id
(optional)<span class="param-type">[String](#string)</span> wait_all_nodes
(optional)<span class="param-type">[Boolean](#boolean)</span> kill_warning_flags
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: kill_warning_signal
(optional)<span class="param-type">[String](#string)</span> kill_warning_delay
(optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span>
current_working_directory (optional)<span class="param-type">[String](#string)</span> cpus_per_task
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 minimum_cpus
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 maximum_cpus
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 nodes
(optional)<span class="param-type">[String](#string)</span> minimum_nodes
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 maximum_nodes
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 minimum_boards_per_node
(optional)<span class="param-type">[Integer](#integer)</span> format: int32
minimum_sockets_per_board (optional)<span class="param-type">[Integer](#integer)</span> format:
int32 sockets_per_node (optional)<span class="param-type">[Integer](#integer)</span> format: int32
threads_per_core (optional)<span class="param-type">[Integer](#integer)</span> format: int32
tasks_per_node (optional)<span class="param-type">[Integer](#integer)</span> format: int32
tasks_per_socket (optional)<span class="param-type">[Integer](#integer)</span> format: int32
tasks_per_core (optional)<span class="param-type">[Integer](#integer)</span> format: int32
tasks_per_board (optional)<span class="param-type">[Integer](#integer)</span> format: int32
ntasks_per_tres (optional)<span class="param-type">[Integer](#integer)</span> format: int32
minimum_cpus_per_node (optional)<span class="param-type">[Integer](#integer)</span> format: int32
memory_per_cpu
(optional)<span class="param-type">[v0.0.39_uint64_no_val](#v0.0.39_uint64_no_val)</span>
memory_per_node
(optional)<span class="param-type">[v0.0.39_uint64_no_val](#v0.0.39_uint64_no_val)</span>
temporary_disk_per_node (optional)<span class="param-type">[Integer](#integer)</span> format: int32
selinux_context (optional)<span class="param-type">[String](#string)</span> required_switches
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
standard_error (optional)<span class="param-type">[String](#string)</span> standard_input
(optional)<span class="param-type">[String](#string)</span> standard_output
(optional)<span class="param-type">[String](#string)</span> wait_for_switch
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 wckey
(optional)<span class="param-type">[String](#string)</span> x11
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: x11_magic_cookie
(optional)<span class="param-type">[String](#string)</span> x11_target_host
(optional)<span class="param-type">[String](#string)</span> x11_target_port
(optional)<span class="param-type">[Integer](#integer)</span> format: int32

### <span id="v0.0.39_job_exit_code">`v0.0.39_job_exit_code` -</span> <a href="#__Models" class="up">Up</a>

job exit details status (optional)<span class="param-type">[String](#string)</span> exit status
return_code (optional)<span class="param-type">[Integer](#integer)</span> return code (numeric)
format: int32 signal
(optional)<span class="param-type">[v0_0_39_job_exit_code_signal](#v0_0_39_job_exit_code_signal)</span>

### <span id="v0.0.39_job_info">`v0.0.39_job_info` -</span> <a href="#__Models" class="up">Up</a>

account (optional)<span class="param-type">[String](#string)</span> accrue_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 admin_comment
(optional)<span class="param-type">[String](#string)</span> allocating_node
(optional)<span class="param-type">[String](#string)</span> array_job_id
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
array_task_id
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
array_max_tasks
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
array_task_string (optional)<span class="param-type">[String](#string)</span> association_id
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 batch_features
(optional)<span class="param-type">[String](#string)</span> batch_flag
(optional)<span class="param-type">[Boolean](#boolean)</span> batch_host
(optional)<span class="param-type">[String](#string)</span> flags
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: burst_buffer
(optional)<span class="param-type">[String](#string)</span> burst_buffer_state
(optional)<span class="param-type">[String](#string)</span> cluster
(optional)<span class="param-type">[String](#string)</span> cluster_features
(optional)<span class="param-type">[String](#string)</span> command
(optional)<span class="param-type">[String](#string)</span> comment
(optional)<span class="param-type">[String](#string)</span> container
(optional)<span class="param-type">[String](#string)</span> container_id
(optional)<span class="param-type">[String](#string)</span> contiguous
(optional)<span class="param-type">[Boolean](#boolean)</span> core_spec
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 thread_spec
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 cores_per_socket
(optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span>
billable_tres
(optional)<span class="param-type">[v0.0.39_float64_no_val](#v0.0.39_float64_no_val)</span>
cpus_per_task
(optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span>
cpu_frequency_minimum
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
cpu_frequency_maximum
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
cpu_frequency_governor
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
cpus_per_tres (optional)<span class="param-type">[String](#string)</span> cron
(optional)<span class="param-type">[String](#string)</span> deadline
(optional)<span class="param-type">[Long](#long)</span> format: int64 delay_boot
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> dependency
(optional)<span class="param-type">[String](#string)</span> derived_exit_code
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
eligible_time (optional)<span class="param-type">[Long](#long)</span> format: int64 end_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 excluded_nodes
(optional)<span class="param-type">[String](#string)</span> exit_code
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> extra
(optional)<span class="param-type">[String](#string)</span> failed_node
(optional)<span class="param-type">[String](#string)</span> features
(optional)<span class="param-type">[String](#string)</span> federation_origin
(optional)<span class="param-type">[String](#string)</span> federation_siblings_active
(optional)<span class="param-type">[String](#string)</span> federation_siblings_viable
(optional)<span class="param-type">[String](#string)</span> gres_detail
(optional)<span class="param-type">[array\[String\]](#string)</span> group_id
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 group_name
(optional)<span class="param-type">[String](#string)</span> het_job_id
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
het_job_id_set (optional)<span class="param-type">[String](#string)</span> het_job_offset
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> job_id
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 job_resources
(optional)<span class="param-type">[v0.0.39_job_res](#v0.0.39_job_res)</span> job_size_str
(optional)<span class="param-type">[array\[String\]](#string)</span> job_state
(optional)<span class="param-type">[String](#string)</span> last_sched_evaluation
(optional)<span class="param-type">[Long](#long)</span> format: int64 licenses
(optional)<span class="param-type">[String](#string)</span> mail_type
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: mail_user
(optional)<span class="param-type">[String](#string)</span> max_cpus
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> max_nodes
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> mcs_label
(optional)<span class="param-type">[String](#string)</span> memory_per_tres
(optional)<span class="param-type">[String](#string)</span> name
(optional)<span class="param-type">[String](#string)</span> network
(optional)<span class="param-type">[String](#string)</span> nodes
(optional)<span class="param-type">[String](#string)</span> nice
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 tasks_per_core
(optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span>
tasks_per_tres
(optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span>
tasks_per_node
(optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span>
tasks_per_socket
(optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span>
tasks_per_board
(optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span> cpus
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> node_count
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> tasks
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> partition
(optional)<span class="param-type">[String](#string)</span> prefer
(optional)<span class="param-type">[String](#string)</span> memory_per_cpu
(optional)<span class="param-type">[v0.0.39_uint64_no_val](#v0.0.39_uint64_no_val)</span>
memory_per_node
(optional)<span class="param-type">[v0.0.39_uint64_no_val](#v0.0.39_uint64_no_val)</span>
minimum_cpus_per_node
(optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span>
minimum_tmp_disk_per_node
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> power
(optional)<span class="param-type">[v0_0_39_job_info_power](#v0_0_39_job_info_power)</span>
preempt_time (optional)<span class="param-type">[Long](#long)</span> format: int64 preemptable_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 pre_sus_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 hold
(optional)<span class="param-type">[Boolean](#boolean)</span> Hold (true) or release (false) job
priority (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
profile (optional)<span class="param-type">[array\[String\]](#string)</span> Enum: qos
(optional)<span class="param-type">[String](#string)</span> reboot
(optional)<span class="param-type">[Boolean](#boolean)</span> required_nodes
(optional)<span class="param-type">[String](#string)</span> minimum_switches
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 requeue
(optional)<span class="param-type">[Boolean](#boolean)</span> resize_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 restart_cnt
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 resv_name
(optional)<span class="param-type">[String](#string)</span> scheduled_nodes
(optional)<span class="param-type">[String](#string)</span> selinux_context
(optional)<span class="param-type">[String](#string)</span> shared
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: exclusive
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: oversubscribe
(optional)<span class="param-type">[Boolean](#boolean)</span> show_flags
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: sockets_per_board
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 sockets_per_node
(optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span> start_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 state_description
(optional)<span class="param-type">[String](#string)</span> state_reason
(optional)<span class="param-type">[String](#string)</span> standard_error
(optional)<span class="param-type">[String](#string)</span> standard_input
(optional)<span class="param-type">[String](#string)</span> standard_output
(optional)<span class="param-type">[String](#string)</span> submit_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 suspend_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 system_comment
(optional)<span class="param-type">[String](#string)</span> time_limit
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
time_minimum
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
threads_per_core
(optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span> tres_bind
(optional)<span class="param-type">[String](#string)</span> tres_freq
(optional)<span class="param-type">[String](#string)</span> tres_per_job
(optional)<span class="param-type">[String](#string)</span> tres_per_node
(optional)<span class="param-type">[String](#string)</span> tres_per_socket
(optional)<span class="param-type">[String](#string)</span> tres_per_task
(optional)<span class="param-type">[String](#string)</span> tres_req_str
(optional)<span class="param-type">[String](#string)</span> tres_alloc_str
(optional)<span class="param-type">[String](#string)</span> user_id
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 user_name
(optional)<span class="param-type">[String](#string)</span> maximum_switch_wait_time
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 wckey
(optional)<span class="param-type">[String](#string)</span> current_working_directory
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0.0.39_job_res">`v0.0.39_job_res` -</span> <a href="#__Models" class="up">Up</a>

nodes (optional)<span class="param-type">[String](#string)</span> allocated_cores
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 allocated_cpus
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 allocated_hosts
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 allocated_nodes
(optional)<span class="param-type">[array\[oas_any_type_not_mapped\]](#AnyType)</span> job node
resources

### <span id="v0.0.39_job_submission">`v0.0.39_job_submission` -</span> <a href="#__Models" class="up">Up</a>

script (optional)<span class="param-type">[String](#string)</span> Executable script (full contents)
to run in batch step for all job components job
(optional)<span class="param-type">[v0.0.39_job_desc_msg](#v0.0.39_job_desc_msg)</span> jobs
(optional)<span class="param-type">[array\[v0.0.39_job_desc_msg\]](#v0.0.39_job_desc_msg)</span>

### <span id="v0.0.39_job_submission_response">`v0.0.39_job_submission_response` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[v0.0.39_meta](#v0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[v0.0.39_error\]](#v0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[v0.0.39_warning\]](#v0.0.39_warning)</span>
Slurm warnings job_id (optional)<span class="param-type">[Integer](#integer)</span> new job ID
step_id (optional)<span class="param-type">[String](#string)</span> new job step ID
job_submit_user_msg (optional)<span class="param-type">[String](#string)</span> Message to user from
job_submit plugin

### <span id="v0.0.39_job_update_response">`v0.0.39_job_update_response` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[v0.0.39_meta](#v0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[v0.0.39_error\]](#v0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[v0.0.39_warning\]](#v0.0.39_warning)</span>
Slurm warnings results
(optional)<span class="param-type">[array\[v0_0_39_job_array_response_msg_inner\]](#v0_0_39_job_array_response_msg_inner)</span>
Result per ArrayJob

### <span id="v0.0.39_jobs_response">`v0.0.39_jobs_response` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[v0.0.39_meta](#v0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[v0.0.39_error\]](#v0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[v0.0.39_warning\]](#v0.0.39_warning)</span>
Slurm warnings jobs
(optional)<span class="param-type">[array\[v0.0.39_job_info\]](#v0.0.39_job_info)</span>

### <span id="v0.0.39_license">`v0.0.39_license` -</span> <a href="#__Models" class="up">Up</a>

LicenseName (optional)<span class="param-type">[String](#string)</span> Total
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 Used
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 Free
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 Remote
(optional)<span class="param-type">[Boolean](#boolean)</span> Reserved
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 LastConsumed
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 LastDeficit
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 LastUpdate
(optional)<span class="param-type">[Long](#long)</span> format: int64

### <span id="v0.0.39_licenses_info">`v0.0.39_licenses_info` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[v0.0.39_meta](#v0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[v0.0.39_error\]](#v0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[v0.0.39_warning\]](#v0.0.39_warning)</span>
Slurm warnings licenses
(optional)<span class="param-type">[array\[v0.0.39_license\]](#v0.0.39_license)</span>

### <span id="v0.0.39_meta">`v0.0.39_meta` -</span> <a href="#__Models" class="up">Up</a>

plugin (optional)<span class="param-type">[dbv0_0_39_meta_plugin](#dbv0_0_39_meta_plugin)</span>
Slurm (optional)<span class="param-type">[dbv0_0_39_meta_Slurm](#dbv0_0_39_meta_Slurm)</span>

### <span id="v0.0.39_node">`v0.0.39_node` -</span> <a href="#__Models" class="up">Up</a>

architecture (optional)<span class="param-type">[String](#string)</span> burstbuffer_network_address
(optional)<span class="param-type">[String](#string)</span> boards
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 boot_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 cluster_name
(optional)<span class="param-type">[String](#string)</span> cores
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 specialized_cores
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 cpu_binding
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 cpu_load
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> free_mem
(optional)<span class="param-type">[v0.0.39_uint64_no_val](#v0.0.39_uint64_no_val)</span> cpus
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 effective_cpus
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 specialized_cpus
(optional)<span class="param-type">[String](#string)</span> energy
(optional)<span class="param-type">[v0.0.39_acct_gather_energy](#v0.0.39_acct_gather_energy)</span>
external_sensors
(optional)<span class="param-type">[v0.0.39_ext_sensors_data](#v0.0.39_ext_sensors_data)</span>
extra (optional)<span class="param-type">[String](#string)</span> power
(optional)<span class="param-type">[v0.0.39_power_mgmt_data](#v0.0.39_power_mgmt_data)</span>
features (optional)<span class="param-type">[array\[String\]](#string)</span> active_features
(optional)<span class="param-type">[array\[String\]](#string)</span> gres
(optional)<span class="param-type">[String](#string)</span> gres_drained
(optional)<span class="param-type">[String](#string)</span> gres_used
(optional)<span class="param-type">[String](#string)</span> last_busy
(optional)<span class="param-type">[Long](#long)</span> format: int64 mcs_label
(optional)<span class="param-type">[String](#string)</span> specialized_memory
(optional)<span class="param-type">[Long](#long)</span> format: int64 name
(optional)<span class="param-type">[String](#string)</span> next_state_after_reboot
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: address
(optional)<span class="param-type">[String](#string)</span> hostname
(optional)<span class="param-type">[String](#string)</span> state
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: operating_system
(optional)<span class="param-type">[String](#string)</span> owner
(optional)<span class="param-type">[String](#string)</span> partitions
(optional)<span class="param-type">[array\[String\]](#string)</span> port
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 real_memory
(optional)<span class="param-type">[Long](#long)</span> format: int64 comment
(optional)<span class="param-type">[String](#string)</span> reason
(optional)<span class="param-type">[String](#string)</span> reason_changed_at
(optional)<span class="param-type">[Long](#long)</span> format: int64 reason_set_by_user
(optional)<span class="param-type">[String](#string)</span> resume_after
(optional)<span class="param-type">[v0.0.39_uint64_no_val](#v0.0.39_uint64_no_val)</span>
reservation (optional)<span class="param-type">[String](#string)</span> alloc_memory
(optional)<span class="param-type">[Long](#long)</span> format: int64 alloc_cpus
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 alloc_idle_cpus
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 tres_used
(optional)<span class="param-type">[String](#string)</span> tres_weighted
(optional)<span class="param-type">[Double](#double)</span> format: double slurmd_start_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 sockets
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 threads
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 temporary_disk
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 weight
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 tres
(optional)<span class="param-type">[String](#string)</span> version
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0.0.39_nodes_response">`v0.0.39_nodes_response` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[v0.0.39_meta](#v0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[v0.0.39_error\]](#v0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[v0.0.39_warning\]](#v0.0.39_warning)</span>
Slurm warnings nodes
(optional)<span class="param-type">[array\[v0.0.39_node\]](#v0.0.39_node)</span>

### <span id="v0.0.39_partition_info">`v0.0.39_partition_info` -</span> <a href="#__Models" class="up">Up</a>

nodes
(optional)<span class="param-type">[v0_0_39_partition_info_nodes](#v0_0_39_partition_info_nodes)</span>
accounts
(optional)<span class="param-type">[v0_0_39_partition_info_accounts](#v0_0_39_partition_info_accounts)</span>
groups
(optional)<span class="param-type">[v0_0_39_partition_info_groups](#v0_0_39_partition_info_groups)</span>
qos
(optional)<span class="param-type">[v0_0_39_partition_info_qos](#v0_0_39_partition_info_qos)</span>
alternate (optional)<span class="param-type">[String](#string)</span> tres
(optional)<span class="param-type">[v0_0_39_partition_info_tres](#v0_0_39_partition_info_tres)</span>
cluster (optional)<span class="param-type">[String](#string)</span> cpus
(optional)<span class="param-type">[v0_0_39_partition_info_cpus](#v0_0_39_partition_info_cpus)</span>
defaults
(optional)<span class="param-type">[v0_0_39_partition_info_defaults](#v0_0_39_partition_info_defaults)</span>
grace_time (optional)<span class="param-type">[Integer](#integer)</span> format: int32 maximums
(optional)<span class="param-type">[v0_0_39_partition_info_maximums](#v0_0_39_partition_info_maximums)</span>
minimums
(optional)<span class="param-type">[v0_0_39_partition_info_minimums](#v0_0_39_partition_info_minimums)</span>
name (optional)<span class="param-type">[String](#string)</span> node_sets
(optional)<span class="param-type">[String](#string)</span> priority
(optional)<span class="param-type">[v0_0_39_partition_info_priority](#v0_0_39_partition_info_priority)</span>
timeouts
(optional)<span class="param-type">[v0_0_39_partition_info_timeouts](#v0_0_39_partition_info_timeouts)</span>
suspend_time
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>

### <span id="v0.0.39_partitions_response">`v0.0.39_partitions_response` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[v0.0.39_meta](#v0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[v0.0.39_error\]](#v0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[v0.0.39_warning\]](#v0.0.39_warning)</span>
Slurm warnings partitions
(optional)<span class="param-type">[array\[v0.0.39_partition_info\]](#v0.0.39_partition_info)</span>

### <span id="v0.0.39_pings">`v0.0.39_pings` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[v0.0.39_meta](#v0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[v0.0.39_error\]](#v0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[v0.0.39_warning\]](#v0.0.39_warning)</span>
Slurm warnings pings
(optional)<span class="param-type">[array\[v0.0.39_controller_ping\]](#v0.0.39_controller_ping)</span>

### <span id="v0.0.39_power_mgmt_data">`v0.0.39_power_mgmt_data` -</span> <a href="#__Models" class="up">Up</a>

maximum_watts
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
current_watts (optional)<span class="param-type">[Integer](#integer)</span> format: int32
total_energy (optional)<span class="param-type">[Long](#long)</span> format: int64 new_maximum_watts
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 peak_watts
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 lowest_watts
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 new_job_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 state
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 time_start_day
(optional)<span class="param-type">[Long](#long)</span> format: int64

### <span id="v0.0.39_qos">`v0.0.39_qos` -</span> <a href="#__Models" class="up">Up</a>

description (optional)<span class="param-type">[String](#string)</span> flags
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: id
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 limits
(optional)<span class="param-type">[v0_0_39_qos_limits](#v0_0_39_qos_limits)</span> name
(optional)<span class="param-type">[String](#string)</span> preempt
(optional)<span class="param-type">[v0_0_39_qos_preempt](#v0_0_39_qos_preempt)</span> priority
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
usage_factor
(optional)<span class="param-type">[v0.0.39_float64_no_val](#v0.0.39_float64_no_val)</span>
usage_threshold
(optional)<span class="param-type">[v0.0.39_float64_no_val](#v0.0.39_float64_no_val)</span>

### <span id="v0.0.39_reservation_core_spec">`v0.0.39_reservation_core_spec` -</span> <a href="#__Models" class="up">Up</a>

node (optional)<span class="param-type">[String](#string)</span> core
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0.0.39_reservation_info">`v0.0.39_reservation_info` -</span> <a href="#__Models" class="up">Up</a>

accounts (optional)<span class="param-type">[String](#string)</span> burst_buffer
(optional)<span class="param-type">[String](#string)</span> core_count
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 core_specializations
(optional)<span class="param-type">[array\[v0.0.39_reservation_core_spec\]](#v0.0.39_reservation_core_spec)</span>
end_time (optional)<span class="param-type">[Long](#long)</span> format: int64 features
(optional)<span class="param-type">[String](#string)</span> flags
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: groups
(optional)<span class="param-type">[String](#string)</span> licenses
(optional)<span class="param-type">[String](#string)</span> max_start_delay
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 name
(optional)<span class="param-type">[String](#string)</span> node_count
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 node_list
(optional)<span class="param-type">[String](#string)</span> partition
(optional)<span class="param-type">[String](#string)</span> purge_completed
(optional)<span class="param-type">[v0_0_39_reservation_info_purge_completed](#v0_0_39_reservation_info_purge_completed)</span>
start_time (optional)<span class="param-type">[Long](#long)</span> format: int64 watts
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> tres
(optional)<span class="param-type">[String](#string)</span> users
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0.0.39_reservations_response">`v0.0.39_reservations_response` -</span> <a href="#__Models" class="up">Up</a>

meta (optional)<span class="param-type">[v0.0.39_meta](#v0.0.39_meta)</span> errors
(optional)<span class="param-type">[array\[v0.0.39_error\]](#v0.0.39_error)</span> Slurm errors
warnings (optional)<span class="param-type">[array\[v0.0.39_warning\]](#v0.0.39_warning)</span>
Slurm warnings reservations
(optional)<span class="param-type">[array\[v0.0.39_reservation_info\]](#v0.0.39_reservation_info)</span>

### <span id="v0.0.39_slurm_step_id">`v0.0.39_slurm_step_id` -</span> <a href="#__Models" class="up">Up</a>

step details job_id (optional)<span class="param-type">[Integer](#integer)</span> JobID format:
int32 step_het_component (optional)<span class="param-type">[Integer](#integer)</span> HetStep
format: int32 step_id (optional)<span class="param-type">[String](#string)</span>

### <span id="v0.0.39_stats_msg">`v0.0.39_stats_msg` -</span> <a href="#__Models" class="up">Up</a>

parts_packed (optional)<span class="param-type">[Integer](#integer)</span> format: int32 req_time
(optional)<span class="param-type">[Long](#long)</span> format: int64 req_time_start
(optional)<span class="param-type">[Long](#long)</span> format: int64 server_thread_count
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 agent_queue_size
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 agent_count
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 agent_thread_count
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 dbd_agent_queue_size
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 gettimeofday_latency
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 schedule_cycle_max
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 schedule_cycle_last
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 schedule_cycle_total
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 schedule_cycle_mean
(optional)<span class="param-type">[Long](#long)</span> format: int64 schedule_cycle_mean_depth
(optional)<span class="param-type">[Long](#long)</span> format: int64 schedule_cycle_per_minute
(optional)<span class="param-type">[Long](#long)</span> format: int64 schedule_queue_length
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 jobs_submitted
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 jobs_started
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 jobs_completed
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 jobs_canceled
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 jobs_failed
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 jobs_pending
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 jobs_running
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 job_states_ts
(optional)<span class="param-type">[Long](#long)</span> format: int64 bf_backfilled_jobs
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 bf_last_backfilled_jobs
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 bf_backfilled_het_jobs
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 bf_cycle_counter
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 bf_cycle_mean
(optional)<span class="param-type">[Long](#long)</span> format: int64 bf_depth_mean
(optional)<span class="param-type">[Long](#long)</span> format: int64 bf_depth_mean_try
(optional)<span class="param-type">[Long](#long)</span> format: int64 bf_cycle_sum
(optional)<span class="param-type">[Long](#long)</span> format: int64 bf_cycle_last
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 bf_last_depth
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 bf_last_depth_try
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 bf_depth_sum
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 bf_depth_try_sum
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 bf_queue_len
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 bf_queue_len_mean
(optional)<span class="param-type">[Long](#long)</span> format: int64 bf_queue_len_sum
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 bf_table_size
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 bf_table_size_mean
(optional)<span class="param-type">[Long](#long)</span> format: int64 bf_when_last_cycle
(optional)<span class="param-type">[Long](#long)</span> format: int64 bf_active
(optional)<span class="param-type">[Boolean](#boolean)</span> rpcs_by_message_type
(optional)<span class="param-type">[array\[v0_0_39_stats_msg_rpcs_by_type_inner\]](#v0_0_39_stats_msg_rpcs_by_type_inner)</span>
RPCs by message type rpcs_by_user
(optional)<span class="param-type">[array\[v0_0_39_stats_msg_rpcs_by_user_inner\]](#v0_0_39_stats_msg_rpcs_by_user_inner)</span>
RPCs by user

### <span id="v0.0.39_stats_rec">`v0.0.39_stats_rec` -</span> <a href="#__Models" class="up">Up</a>

time_start (optional)<span class="param-type">[Long](#long)</span> format: int64 rollups
(optional)<span class="param-type">[array\[v0_0_39_rollup_stats_inner\]](#v0_0_39_rollup_stats_inner)</span>
list of recorded rollup statistics RPCs
(optional)<span class="param-type">[array\[v0.0.39_stats_rpc\]](#v0.0.39_stats_rpc)</span> users
(optional)<span class="param-type">[array\[v0.0.39_stats_user\]](#v0.0.39_stats_user)</span>

### <span id="v0.0.39_stats_rpc">`v0.0.39_stats_rpc` -</span> <a href="#__Models" class="up">Up</a>

rpc (optional)<span class="param-type">[String](#string)</span> count
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 time
(optional)<span class="param-type">[v0_0_39_stats_rpc_time](#v0_0_39_stats_rpc_time)</span>

### <span id="v0.0.39_stats_user">`v0.0.39_stats_user` -</span> <a href="#__Models" class="up">Up</a>

user (optional)<span class="param-type">[String](#string)</span> count
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 time
(optional)<span class="param-type">[v0_0_39_stats_rpc_time](#v0_0_39_stats_rpc_time)</span>

### <span id="v0.0.39_step">`v0.0.39_step` -</span> <a href="#__Models" class="up">Up</a>

time (optional)<span class="param-type">[v0_0_39_step_time](#v0_0_39_step_time)</span> exit_code
(optional)<span class="param-type">[v0.0.39_job_exit_code](#v0.0.39_job_exit_code)</span> nodes
(optional)<span class="param-type">[v0_0_39_step_nodes](#v0_0_39_step_nodes)</span> tasks
(optional)<span class="param-type">[v0_0_39_step_tasks](#v0_0_39_step_tasks)</span> pid
(optional)<span class="param-type">[String](#string)</span> CPU
(optional)<span class="param-type">[v0_0_39_step_CPU](#v0_0_39_step_CPU)</span> kill_request_user
(optional)<span class="param-type">[String](#string)</span> state
(optional)<span class="param-type">[String](#string)</span> statistics
(optional)<span class="param-type">[v0_0_39_step_statistics](#v0_0_39_step_statistics)</span> step
(optional)<span class="param-type">[v0_0_39_step_step](#v0_0_39_step_step)</span> task
(optional)<span class="param-type">[v0_0_39_step_task](#v0_0_39_step_task)</span> tres
(optional)<span class="param-type">[v0_0_39_step_tres](#v0_0_39_step_tres)</span>

### <span id="v0.0.39_tres">`v0.0.39_tres` -</span> <a href="#__Models" class="up">Up</a>

type <span class="param-type">[String](#string)</span> name
(optional)<span class="param-type">[String](#string)</span> id
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 count
(optional)<span class="param-type">[Long](#long)</span> format: int64

### <span id="v0.0.39_uint16_no_val">`v0.0.39_uint16_no_val` -</span> <a href="#__Models" class="up">Up</a>

Integer number with flags set (optional)<span class="param-type">[Boolean](#boolean)</span> True if
number has been set. False if number is unset infinite
(optional)<span class="param-type">[Boolean](#boolean)</span> True if number has been set to
infinite. "set" and "number" will be ignored. number
(optional)<span class="param-type">[Long](#long)</span> If set is True the number will be set with
value. Otherwise ignore number contents. format: int64

### <span id="v0.0.39_uint32_no_val">`v0.0.39_uint32_no_val` -</span> <a href="#__Models" class="up">Up</a>

Integer number with flags set (optional)<span class="param-type">[Boolean](#boolean)</span> True if
number has been set. False if number is unset infinite
(optional)<span class="param-type">[Boolean](#boolean)</span> True if number has been set to
infinite. "set" and "number" will be ignored. number
(optional)<span class="param-type">[Long](#long)</span> If set is True the number will be set with
value. Otherwise ignore number contents. format: int64

### <span id="v0.0.39_uint64_no_val">`v0.0.39_uint64_no_val` -</span> <a href="#__Models" class="up">Up</a>

Integer number with flags set (optional)<span class="param-type">[Boolean](#boolean)</span> True if
number has been set. False if number is unset infinite
(optional)<span class="param-type">[Boolean](#boolean)</span> True if number has been set to
infinite. "set" and "number" will be ignored. number
(optional)<span class="param-type">[Long](#long)</span> If set is True the number will be set with
value. Otherwise ignore number contents. format: int64

### <span id="v0.0.39_update_node_msg">`v0.0.39_update_node_msg` -</span> <a href="#__Models" class="up">Up</a>

comment (optional)<span class="param-type">[String](#string)</span> arbitrary comment cpu_bind
(optional)<span class="param-type">[Integer](#integer)</span> default CPU binding type format: int32
extra (optional)<span class="param-type">[String](#string)</span> arbitrary string features
(optional)<span class="param-type">[array\[String\]](#string)</span> features_act
(optional)<span class="param-type">[array\[String\]](#string)</span> gres
(optional)<span class="param-type">[String](#string)</span> new generic resources for node address
(optional)<span class="param-type">[array\[String\]](#string)</span> hostname
(optional)<span class="param-type">[array\[String\]](#string)</span> name
(optional)<span class="param-type">[array\[String\]](#string)</span> state
(optional)<span class="param-type">[array\[String\]](#string)</span> assign new node state Enum:
reason (optional)<span class="param-type">[String](#string)</span> reason for node being DOWN or
DRAINING reason_uid (optional)<span class="param-type">[String](#string)</span> user ID of sending
(needed if user root is sending message) resume_after
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> weight
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>

### <span id="v0.0.39_user">`v0.0.39_user` -</span> <a href="#__Models" class="up">Up</a>

administrator_level (optional)<span class="param-type">[array\[String\]](#string)</span> Enum:
associations
(optional)<span class="param-type">[array\[v0.0.39_assoc_short\]](#v0.0.39_assoc_short)</span>
coordinators (optional)<span class="param-type">[array\[v0.0.39_coord\]](#v0.0.39_coord)</span>
default (optional)<span class="param-type">[v0_0_39_user_default](#v0_0_39_user_default)</span>
flags (optional)<span class="param-type">[array\[String\]](#string)</span> Enum: name
<span class="param-type">[String](#string)</span> old_name
(optional)<span class="param-type">[String](#string)</span> wckeys
(optional)<span class="param-type">[array\[v0.0.39_wckey\]](#v0.0.39_wckey)</span>

### <span id="v0.0.39_warning">`v0.0.39_warning` -</span> <a href="#__Models" class="up">Up</a>

warning (optional)<span class="param-type">[String](#string)</span> Earning message source
(optional)<span class="param-type">[String](#string)</span> Where error occurred in the source
description (optional)<span class="param-type">[String](#string)</span> Explanation of cause of
error

### <span id="v0.0.39_wckey">`v0.0.39_wckey` -</span> <a href="#__Models" class="up">Up</a>

accounting
(optional)<span class="param-type">[array\[v0.0.39_accounting\]](#v0.0.39_accounting)</span> cluster
<span class="param-type">[String](#string)</span> id
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 name
<span class="param-type">[String](#string)</span> user
<span class="param-type">[String](#string)</span> flags
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum:

### <span id="v0.0.39_wckey_tag">`v0.0.39_wckey_tag` -</span> <a href="#__Models" class="up">Up</a>

wckey details wckey (optional)<span class="param-type">[String](#string)</span> wckey flags
(optional)<span class="param-type">[array\[String\]](#string)</span> active flags Enum:

### <span id="v0_0_39_accounting_allocated">`v0_0_39_accounting_allocated` -</span> <a href="#__Models" class="up">Up</a>

seconds (optional)<span class="param-type">[Long](#long)</span> format: int64

### <span id="v0_0_39_assoc_default">`v0_0_39_assoc_default` -</span> <a href="#__Models" class="up">Up</a>

qos (optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_assoc_max">`v0_0_39_assoc_max` -</span> <a href="#__Models" class="up">Up</a>

jobs (optional)<span class="param-type">[v0_0_39_assoc_max_jobs](#v0_0_39_assoc_max_jobs)</span>
tres (optional)<span class="param-type">[v0_0_39_assoc_max_tres](#v0_0_39_assoc_max_tres)</span> per
(optional)<span class="param-type">[v0_0_39_assoc_max_per](#v0_0_39_assoc_max_per)</span>

### <span id="v0_0_39_assoc_max_jobs">`v0_0_39_assoc_max_jobs` -</span> <a href="#__Models" class="up">Up</a>

per
(optional)<span class="param-type">[v0_0_39_assoc_max_jobs_per](#v0_0_39_assoc_max_jobs_per)</span>
active (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
accruing (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
total (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>

### <span id="v0_0_39_assoc_max_jobs_per">`v0_0_39_assoc_max_jobs_per` -</span> <a href="#__Models" class="up">Up</a>

count (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
accruing (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
submitted (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
wall_clock (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>

### <span id="v0_0_39_assoc_max_per">`v0_0_39_assoc_max_per` -</span> <a href="#__Models" class="up">Up</a>

account
(optional)<span class="param-type">[v0_0_39_assoc_max_per_account](#v0_0_39_assoc_max_per_account)</span>

### <span id="v0_0_39_assoc_max_per_account">`v0_0_39_assoc_max_per_account` -</span> <a href="#__Models" class="up">Up</a>

wall_clock (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>

### <span id="v0_0_39_assoc_max_tres">`v0_0_39_assoc_max_tres` -</span> <a href="#__Models" class="up">Up</a>

total (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> minutes
(optional)<span class="param-type">[v0_0_39_assoc_max_tres_minutes](#v0_0_39_assoc_max_tres_minutes)</span>
group
(optional)<span class="param-type">[v0_0_39_assoc_max_tres_group](#v0_0_39_assoc_max_tres_group)</span>
per
(optional)<span class="param-type">[v0_0_39_assoc_max_tres_per](#v0_0_39_assoc_max_tres_per)</span>

### <span id="v0_0_39_assoc_max_tres_group">`v0_0_39_assoc_max_tres_group` -</span> <a href="#__Models" class="up">Up</a>

minutes (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> active
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>

### <span id="v0_0_39_assoc_max_tres_minutes">`v0_0_39_assoc_max_tres_minutes` -</span> <a href="#__Models" class="up">Up</a>

per
(optional)<span class="param-type">[v0_0_39_assoc_max_tres_minutes_per](#v0_0_39_assoc_max_tres_minutes_per)</span>
total (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>

### <span id="v0_0_39_assoc_max_tres_minutes_per">`v0_0_39_assoc_max_tres_minutes_per` -</span> <a href="#__Models" class="up">Up</a>

job (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>

### <span id="v0_0_39_assoc_max_tres_per">`v0_0_39_assoc_max_tres_per` -</span> <a href="#__Models" class="up">Up</a>

job (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> node
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>

### <span id="v0_0_39_assoc_min">`v0_0_39_assoc_min` -</span> <a href="#__Models" class="up">Up</a>

priority_threshold
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>

### <span id="v0_0_39_cluster_rec_associations">`v0_0_39_cluster_rec_associations` -</span> <a href="#__Models" class="up">Up</a>

root (optional)<span class="param-type">[v0.0.39_assoc_short](#v0.0.39_assoc_short)</span>

### <span id="v0_0_39_cluster_rec_controller">`v0_0_39_cluster_rec_controller` -</span> <a href="#__Models" class="up">Up</a>

host (optional)<span class="param-type">[String](#string)</span> port
(optional)<span class="param-type">[Integer](#integer)</span> format: int32

### <span id="v0_0_39_cron_entry_line">`v0_0_39_cron_entry_line` -</span> <a href="#__Models" class="up">Up</a>

start (optional)<span class="param-type">[Integer](#integer)</span> format: int32 end
(optional)<span class="param-type">[Integer](#integer)</span> format: int32

### <span id="v0_0_39_job_array">`v0_0_39_job_array` -</span> <a href="#__Models" class="up">Up</a>

job_id (optional)<span class="param-type">[Integer](#integer)</span> format: int32 limits
(optional)<span class="param-type">[v0_0_39_job_array_limits](#v0_0_39_job_array_limits)</span>
task_id (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
task (optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_job_array_limits">`v0_0_39_job_array_limits` -</span> <a href="#__Models" class="up">Up</a>

max
(optional)<span class="param-type">[v0_0_39_job_array_limits_max](#v0_0_39_job_array_limits_max)</span>

### <span id="v0_0_39_job_array_limits_max">`v0_0_39_job_array_limits_max` -</span> <a href="#__Models" class="up">Up</a>

running
(optional)<span class="param-type">[v0_0_39_job_array_limits_max_running](#v0_0_39_job_array_limits_max_running)</span>

### <span id="v0_0_39_job_array_limits_max_running">`v0_0_39_job_array_limits_max_running` -</span> <a href="#__Models" class="up">Up</a>

tasks (optional)<span class="param-type">[Integer](#integer)</span> format: int32

### <span id="v0_0_39_job_array_response_msg_inner">`v0_0_39_job_array_response_msg_inner` -</span> <a href="#__Models" class="up">Up</a>

ArrayJob job_id (optional)<span class="param-type">[Integer](#integer)</span> JobId format: int32
error_code (optional)<span class="param-type">[Integer](#integer)</span> numeric error code format:
int32 error (optional)<span class="param-type">[String](#string)</span> error code description why
(optional)<span class="param-type">[String](#string)</span> error message

### <span id="v0_0_39_job_comment">`v0_0_39_job_comment` -</span> <a href="#__Models" class="up">Up</a>

administrator (optional)<span class="param-type">[String](#string)</span> job
(optional)<span class="param-type">[String](#string)</span> system
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_job_exit_code_signal">`v0_0_39_job_exit_code_signal` -</span> <a href="#__Models" class="up">Up</a>

Job exited due to signal signal_id (optional)<span class="param-type">[Integer](#integer)</span>
signal numeric ID format: int32 name (optional)<span class="param-type">[String](#string)</span>
signal name

### <span id="v0_0_39_job_het">`v0_0_39_job_het` -</span> <a href="#__Models" class="up">Up</a>

job_id (optional)<span class="param-type">[Integer](#integer)</span> format: int32 job_offset
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>

### <span id="v0_0_39_job_info_power">`v0_0_39_job_info_power` -</span> <a href="#__Models" class="up">Up</a>

flags (optional)<span class="param-type">[array\[String\]](#string)</span> Enum:

### <span id="v0_0_39_job_mcs">`v0_0_39_job_mcs` -</span> <a href="#__Models" class="up">Up</a>

label (optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_job_required">`v0_0_39_job_required` -</span> <a href="#__Models" class="up">Up</a>

CPUs (optional)<span class="param-type">[Integer](#integer)</span> format: int32 memory_per_cpu
(optional)<span class="param-type">[v0.0.39_uint64_no_val](#v0.0.39_uint64_no_val)</span>
memory_per_node
(optional)<span class="param-type">[v0.0.39_uint64_no_val](#v0.0.39_uint64_no_val)</span> memory
(optional)<span class="param-type">[Long](#long)</span> format: int64

### <span id="v0_0_39_job_reservation">`v0_0_39_job_reservation` -</span> <a href="#__Models" class="up">Up</a>

id (optional)<span class="param-type">[Integer](#integer)</span> format: int32 name
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_job_state">`v0_0_39_job_state` -</span> <a href="#__Models" class="up">Up</a>

current (optional)<span class="param-type">[String](#string)</span> reason
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_job_time">`v0_0_39_job_time` -</span> <a href="#__Models" class="up">Up</a>

elapsed (optional)<span class="param-type">[Integer](#integer)</span> format: int32 eligible
(optional)<span class="param-type">[Long](#long)</span> format: int64 end
(optional)<span class="param-type">[Long](#long)</span> format: int64 start
(optional)<span class="param-type">[Long](#long)</span> format: int64 submission
(optional)<span class="param-type">[Long](#long)</span> format: int64 suspended
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 system
(optional)<span class="param-type">[v0_0_39_job_time_system](#v0_0_39_job_time_system)</span> limit
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> total
(optional)<span class="param-type">[v0_0_39_job_time_system](#v0_0_39_job_time_system)</span> user
(optional)<span class="param-type">[v0_0_39_job_time_system](#v0_0_39_job_time_system)</span>

### <span id="v0_0_39_job_time_system">`v0_0_39_job_time_system` -</span> <a href="#__Models" class="up">Up</a>

seconds (optional)<span class="param-type">[Long](#long)</span> format: int64 microseconds
(optional)<span class="param-type">[Long](#long)</span> format: int64

### <span id="v0_0_39_job_tres">`v0_0_39_job_tres` -</span> <a href="#__Models" class="up">Up</a>

allocated (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> requested
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>

### <span id="v0_0_39_partition_info_accounts">`v0_0_39_partition_info_accounts` -</span> <a href="#__Models" class="up">Up</a>

allowed (optional)<span class="param-type">[String](#string)</span> deny
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_partition_info_cpus">`v0_0_39_partition_info_cpus` -</span> <a href="#__Models" class="up">Up</a>

task_binding (optional)<span class="param-type">[Integer](#integer)</span> format: int32 total
(optional)<span class="param-type">[Integer](#integer)</span> format: int32

### <span id="v0_0_39_partition_info_defaults">`v0_0_39_partition_info_defaults` -</span> <a href="#__Models" class="up">Up</a>

memory_per_cpu (optional)<span class="param-type">[Long](#long)</span> format: int64 time
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> job
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_partition_info_groups">`v0_0_39_partition_info_groups` -</span> <a href="#__Models" class="up">Up</a>

allowed (optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_partition_info_maximums">`v0_0_39_partition_info_maximums` -</span> <a href="#__Models" class="up">Up</a>

cpus_per_node
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
cpus_per_socket
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
memory_per_cpu (optional)<span class="param-type">[Long](#long)</span> format: int64 nodes
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> shares
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 time
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
over_time_limit
(optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span>

### <span id="v0_0_39_partition_info_minimums">`v0_0_39_partition_info_minimums` -</span> <a href="#__Models" class="up">Up</a>

nodes (optional)<span class="param-type">[Integer](#integer)</span> format: int32

### <span id="v0_0_39_partition_info_nodes">`v0_0_39_partition_info_nodes` -</span> <a href="#__Models" class="up">Up</a>

allowed_allocation (optional)<span class="param-type">[String](#string)</span> configured
(optional)<span class="param-type">[String](#string)</span> total
(optional)<span class="param-type">[Integer](#integer)</span> format: int32

### <span id="v0_0_39_partition_info_priority">`v0_0_39_partition_info_priority` -</span> <a href="#__Models" class="up">Up</a>

job_factor (optional)<span class="param-type">[Integer](#integer)</span> format: int32 tier
(optional)<span class="param-type">[Integer](#integer)</span> format: int32

### <span id="v0_0_39_partition_info_qos">`v0_0_39_partition_info_qos` -</span> <a href="#__Models" class="up">Up</a>

allowed (optional)<span class="param-type">[String](#string)</span> deny
(optional)<span class="param-type">[String](#string)</span> assigned
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_partition_info_timeouts">`v0_0_39_partition_info_timeouts` -</span> <a href="#__Models" class="up">Up</a>

resume (optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span>
suspend (optional)<span class="param-type">[v0.0.39_uint16_no_val](#v0.0.39_uint16_no_val)</span>

### <span id="v0_0_39_partition_info_tres">`v0_0_39_partition_info_tres` -</span> <a href="#__Models" class="up">Up</a>

billing_weights (optional)<span class="param-type">[String](#string)</span> configured
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_qos_limits">`v0_0_39_qos_limits` -</span> <a href="#__Models" class="up">Up</a>

grace_time (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
max (optional)<span class="param-type">[v0_0_39_qos_limits_max](#v0_0_39_qos_limits_max)</span>
factor (optional)<span class="param-type">[Double](#double)</span> format: double min
(optional)<span class="param-type">[v0_0_39_qos_limits_min](#v0_0_39_qos_limits_min)</span>

### <span id="v0_0_39_qos_limits_max">`v0_0_39_qos_limits_max` -</span> <a href="#__Models" class="up">Up</a>

active_jobs
(optional)<span class="param-type">[v0_0_39_qos_limits_max_active_jobs](#v0_0_39_qos_limits_max_active_jobs)</span>
tres
(optional)<span class="param-type">[v0_0_39_qos_limits_max_tres](#v0_0_39_qos_limits_max_tres)</span>
wall_clock
(optional)<span class="param-type">[v0_0_39_qos_limits_max_wall_clock](#v0_0_39_qos_limits_max_wall_clock)</span>
jobs
(optional)<span class="param-type">[v0_0_39_qos_limits_max_jobs](#v0_0_39_qos_limits_max_jobs)</span>
accruing
(optional)<span class="param-type">[v0_0_39_qos_limits_max_jobs_active_jobs](#v0_0_39_qos_limits_max_jobs_active_jobs)</span>

### <span id="v0_0_39_qos_limits_max_active_jobs">`v0_0_39_qos_limits_max_active_jobs` -</span> <a href="#__Models" class="up">Up</a>

accruing (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
count (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>

### <span id="v0_0_39_qos_limits_max_jobs">`v0_0_39_qos_limits_max_jobs` -</span> <a href="#__Models" class="up">Up</a>

active_jobs
(optional)<span class="param-type">[v0_0_39_qos_limits_max_jobs_active_jobs](#v0_0_39_qos_limits_max_jobs_active_jobs)</span>
per
(optional)<span class="param-type">[v0_0_39_qos_limits_max_jobs_active_jobs_per](#v0_0_39_qos_limits_max_jobs_active_jobs_per)</span>

### <span id="v0_0_39_qos_limits_max_jobs_active_jobs">`v0_0_39_qos_limits_max_jobs_active_jobs` -</span> <a href="#__Models" class="up">Up</a>

per
(optional)<span class="param-type">[v0_0_39_qos_limits_max_jobs_active_jobs_per](#v0_0_39_qos_limits_max_jobs_active_jobs_per)</span>

### <span id="v0_0_39_qos_limits_max_jobs_active_jobs_per">`v0_0_39_qos_limits_max_jobs_active_jobs_per` -</span> <a href="#__Models" class="up">Up</a>

account (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>
user (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>

### <span id="v0_0_39_qos_limits_max_tres">`v0_0_39_qos_limits_max_tres` -</span> <a href="#__Models" class="up">Up</a>

total (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> minutes
(optional)<span class="param-type">[v0_0_39_qos_limits_max_tres_minutes](#v0_0_39_qos_limits_max_tres_minutes)</span>
per
(optional)<span class="param-type">[v0_0_39_qos_limits_max_tres_per](#v0_0_39_qos_limits_max_tres_per)</span>

### <span id="v0_0_39_qos_limits_max_tres_minutes">`v0_0_39_qos_limits_max_tres_minutes` -</span> <a href="#__Models" class="up">Up</a>

per
(optional)<span class="param-type">[v0_0_39_qos_limits_max_tres_minutes_per](#v0_0_39_qos_limits_max_tres_minutes_per)</span>

### <span id="v0_0_39_qos_limits_max_tres_minutes_per">`v0_0_39_qos_limits_max_tres_minutes_per` -</span> <a href="#__Models" class="up">Up</a>

qos (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> job
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> account
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> user
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>

### <span id="v0_0_39_qos_limits_max_tres_per">`v0_0_39_qos_limits_max_tres_per` -</span> <a href="#__Models" class="up">Up</a>

account (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> job
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> node
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> user
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>

### <span id="v0_0_39_qos_limits_max_wall_clock">`v0_0_39_qos_limits_max_wall_clock` -</span> <a href="#__Models" class="up">Up</a>

per
(optional)<span class="param-type">[v0_0_39_qos_limits_max_wall_clock_per](#v0_0_39_qos_limits_max_wall_clock_per)</span>

### <span id="v0_0_39_qos_limits_max_wall_clock_per">`v0_0_39_qos_limits_max_wall_clock_per` -</span> <a href="#__Models" class="up">Up</a>

qos (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> job
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>

### <span id="v0_0_39_qos_limits_min">`v0_0_39_qos_limits_min` -</span> <a href="#__Models" class="up">Up</a>

priority_threshold
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> tres
(optional)<span class="param-type">[v0_0_39_qos_limits_min_tres](#v0_0_39_qos_limits_min_tres)</span>

### <span id="v0_0_39_qos_limits_min_tres">`v0_0_39_qos_limits_min_tres` -</span> <a href="#__Models" class="up">Up</a>

per
(optional)<span class="param-type">[v0_0_39_assoc_max_tres_minutes_per](#v0_0_39_assoc_max_tres_minutes_per)</span>

### <span id="v0_0_39_qos_preempt">`v0_0_39_qos_preempt` -</span> <a href="#__Models" class="up">Up</a>

list (optional)<span class="param-type">[array\[String\]](#string)</span> mode
(optional)<span class="param-type">[array\[String\]](#string)</span> Enum: exempt_time
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>

### <span id="v0_0_39_reservation_info_purge_completed">`v0_0_39_reservation_info_purge_completed` -</span> <a href="#__Models" class="up">Up</a>

time (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>

### <span id="v0_0_39_rollup_stats_inner">`v0_0_39_rollup_stats_inner` -</span> <a href="#__Models" class="up">Up</a>

recorded rollup statistics type (optional)<span class="param-type">[String](#string)</span> type
Enum: internaluserunknown last run (optional)<span class="param-type">[Integer](#integer)</span>
Last time rollup ran (UNIX timestamp) format: int32 max_cycle
(optional)<span class="param-type">[Long](#long)</span> longest rollup time (seconds) format: int64
total_time (optional)<span class="param-type">[Long](#long)</span> total time spent doing rollups
(seconds) format: int64 total_cycles (optional)<span class="param-type">[Long](#long)</span> number
of rollups since last_run format: int64 mean_cycles
(optional)<span class="param-type">[Long](#long)</span> average time for rollup (seconds) format:
int64

### <span id="v0_0_39_stats_msg_rpcs_by_type_inner">`v0_0_39_stats_msg_rpcs_by_type_inner` -</span> <a href="#__Models" class="up">Up</a>

RPC message_type (optional)<span class="param-type">[String](#string)</span> Message type as string
type_id (optional)<span class="param-type">[Integer](#integer)</span> Message type as integer
format: int32 count (optional)<span class="param-type">[Long](#long)</span> Number of RPCs received
format: int64 average_time (optional)<span class="param-type">[Long](#long)</span> Average time
spent processing RPC in seconds format: int64 total_time
(optional)<span class="param-type">[Long](#long)</span> Total time spent processing RPC in seconds
format: int64

### <span id="v0_0_39_stats_msg_rpcs_by_user_inner">`v0_0_39_stats_msg_rpcs_by_user_inner` -</span> <a href="#__Models" class="up">Up</a>

user user (optional)<span class="param-type">[String](#string)</span> user name user_id
(optional)<span class="param-type">[Integer](#integer)</span> user id (numeric) format: int32 count
(optional)<span class="param-type">[Long](#long)</span> Number of RPCs received format: int64
average_time (optional)<span class="param-type">[Long](#long)</span> Average time spent processing
RPC in seconds format: int64 total_time (optional)<span class="param-type">[Long](#long)</span>
Total time spent processing RPC in seconds format: int64

### <span id="v0_0_39_stats_rpc_time">`v0_0_39_stats_rpc_time` -</span> <a href="#__Models" class="up">Up</a>

average (optional)<span class="param-type">[Long](#long)</span> format: int64 total
(optional)<span class="param-type">[Long](#long)</span> format: int64

### <span id="v0_0_39_step_CPU">`v0_0_39_step_CPU` -</span> <a href="#__Models" class="up">Up</a>

requested_frequency
(optional)<span class="param-type">[v0_0_39_step_CPU_requested_frequency](#v0_0_39_step_CPU_requested_frequency)</span>
governor (optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_step_CPU_requested_frequency">`v0_0_39_step_CPU_requested_frequency` -</span> <a href="#__Models" class="up">Up</a>

min (optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span> max
(optional)<span class="param-type">[v0.0.39_uint32_no_val](#v0.0.39_uint32_no_val)</span>

### <span id="v0_0_39_step_nodes">`v0_0_39_step_nodes` -</span> <a href="#__Models" class="up">Up</a>

count (optional)<span class="param-type">[Integer](#integer)</span> format: int32 range
(optional)<span class="param-type">[String](#string)</span> list
(optional)<span class="param-type">[array\[String\]](#string)</span>

### <span id="v0_0_39_step_statistics">`v0_0_39_step_statistics` -</span> <a href="#__Models" class="up">Up</a>

CPU
(optional)<span class="param-type">[v0_0_39_step_statistics_CPU](#v0_0_39_step_statistics_CPU)</span>
energy
(optional)<span class="param-type">[v0_0_39_step_statistics_energy](#v0_0_39_step_statistics_energy)</span>

### <span id="v0_0_39_step_statistics_CPU">`v0_0_39_step_statistics_CPU` -</span> <a href="#__Models" class="up">Up</a>

actual_frequency (optional)<span class="param-type">[Long](#long)</span> format: int64

### <span id="v0_0_39_step_statistics_energy">`v0_0_39_step_statistics_energy` -</span> <a href="#__Models" class="up">Up</a>

consumed (optional)<span class="param-type">[v0.0.39_uint64_no_val](#v0.0.39_uint64_no_val)</span>

### <span id="v0_0_39_step_step">`v0_0_39_step_step` -</span> <a href="#__Models" class="up">Up</a>

id (optional)<span class="param-type">[v0.0.39_slurm_step_id](#v0.0.39_slurm_step_id)</span> name
(optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_step_task">`v0_0_39_step_task` -</span> <a href="#__Models" class="up">Up</a>

distribution (optional)<span class="param-type">[String](#string)</span>

### <span id="v0_0_39_step_tasks">`v0_0_39_step_tasks` -</span> <a href="#__Models" class="up">Up</a>

count (optional)<span class="param-type">[Integer](#integer)</span> format: int32

### <span id="v0_0_39_step_time">`v0_0_39_step_time` -</span> <a href="#__Models" class="up">Up</a>

elapsed (optional)<span class="param-type">[Integer](#integer)</span> format: int32 end
(optional)<span class="param-type">[Long](#long)</span> format: int64 start
(optional)<span class="param-type">[Long](#long)</span> format: int64 suspended
(optional)<span class="param-type">[Integer](#integer)</span> format: int32 system
(optional)<span class="param-type">[v0_0_39_step_time_system](#v0_0_39_step_time_system)</span>
total
(optional)<span class="param-type">[v0_0_39_step_time_system](#v0_0_39_step_time_system)</span> user
(optional)<span class="param-type">[v0_0_39_step_time_system](#v0_0_39_step_time_system)</span>

### <span id="v0_0_39_step_time_system">`v0_0_39_step_time_system` -</span> <a href="#__Models" class="up">Up</a>

seconds (optional)<span class="param-type">[Long](#long)</span> format: int64 microseconds
(optional)<span class="param-type">[Integer](#integer)</span> format: int32

### <span id="v0_0_39_step_tres">`v0_0_39_step_tres` -</span> <a href="#__Models" class="up">Up</a>

requested
(optional)<span class="param-type">[v0_0_39_step_tres_requested](#v0_0_39_step_tres_requested)</span>
consumed
(optional)<span class="param-type">[v0_0_39_step_tres_consumed](#v0_0_39_step_tres_consumed)</span>
allocated (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>

### <span id="v0_0_39_step_tres_consumed">`v0_0_39_step_tres_consumed` -</span> <a href="#__Models" class="up">Up</a>

max (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> min
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> average
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> total
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>

### <span id="v0_0_39_step_tres_requested">`v0_0_39_step_tres_requested` -</span> <a href="#__Models" class="up">Up</a>

max (optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> min
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> average
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span> total
(optional)<span class="param-type">[array\[v0.0.39_tres\]](#v0.0.39_tres)</span>

### <span id="v0_0_39_user_default">`v0_0_39_user_default` -</span> <a href="#__Models" class="up">Up</a>

account (optional)<span class="param-type">[String](#string)</span> wckey
(optional)<span class="param-type">[String](#string)</span>
