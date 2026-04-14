## Slurm 22.05.8

### openapi/v0.0.38

#### Fix invalid type for nice

|                |                                                              |
|----------------|--------------------------------------------------------------|
| Field modified | .components.schemas."v0.0.38_job_properties".properties.nice |

### openapi/dbv0.0.38

#### Populate POST /tres/ body

#### 

|           |                                                 |
|-----------|-------------------------------------------------|
| new path  | .paths."/tres/".post.requestBody                |
| new path  | .components.schemas."dbv0.0.38_tres_update"     |
| new field | .components.schemas."dbv0.0.38_update_qos".type |

#### Add missing type field

#### 

|           |                                                     |
|-----------|-----------------------------------------------------|
| new field | .components.schemas."dbv0.0.38_update_account".type |
| new field | .components.schemas."dbv0.0.38_update_users".type   |

#### Add missing requestBody field

#### 

|          |                                          |
|----------|------------------------------------------|
| new path | .paths."/associations/".post.requestBody |
| new path | .paths."/wckeys/".post.requestBody       |

#### Add missing requestBody field

#### 

|           |                                            |
|-----------|--------------------------------------------|
| new field | .paths."/config".post.requestBody          |
| new field | .components.schemas."dbv0.0.38_set_config" |

#### Correct type of field accounts-\>accounting in wckeys

#### 

|               |                                                             |
|---------------|-------------------------------------------------------------|
| new schema    | .components.schemas."dbv0.0.38_accounting"                  |
| new field     | .components.schemas."dbv0.0.38_wckey".properties.accounting |
| removed field | .components.schemas."dbv0.0.38_wckey".properties.accounts   |

#### Use "QOS" in dbv0.0.38_qos_info

#### 

|               |                                                         |
|---------------|---------------------------------------------------------|
| previous path | .components.schemas."dbv0.0.38_qos_info".properties.qos |
| new path      | .components.schemas."dbv0.0.38_qos_info".properties.QOS |

#### Add oversubscribe option to job submission properties

|             |                                                                       |
|-------------|-----------------------------------------------------------------------|
| Field added | .components.schemas."v0.0.38_job_properties".properties.oversubscribe |
