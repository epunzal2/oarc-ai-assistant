## Slurm 23.02.0

### openapi/v0.0.39

#### New plugin

The v0.0.39 plugin forked from the v0.0.38 plugin.

#### New Schema

Plugin has been converted to new data_parser/v0.0.39 plugin for handling parsing and dumping of all
data structures and automatic data structure schema generation. There have been significant changes
to all schemas and care needs to be take to update data sent and expected from requests while
porting to new plugin. Developers are advised to review the generated OpenAPI output directly while
updating.

#### New methods for node queries

DELETE and POST methods are now supported for /slurm/v0.0.39/node/{node_id} paths.

### openapi/v0.0.37

#### Deprecation notice

The v0.0.37 plugin has now been marked as deprecated.

### openapi/v0.0.36

#### Removal notice

The v0.0.36 plugin has now been removed.

### openapi/dbv0.0.39

#### New plugin

The dbv0.0.39 plugin forked from the dbv0.0.38 plugin.

#### New Schema

Plugin has been converted to new data_parser/v0.0.39 plugin for handling parsing and dumping of all
data structures and automatic data structure schema generation. There have been significant changes
to all schemas and care needs to be take to update data sent and expected from requests while
porting to new plugin. Developers are advised to review the generated OpenAPI output directly while
updating.

### openapi/dbv0.0.37

#### Deprecation notice

The dbv0.0.37 plugin has now been marked as deprecated.

### openapi/dbv0.0.36

#### Removal notice

The dbv0.0.36 plugin has now been removed.
