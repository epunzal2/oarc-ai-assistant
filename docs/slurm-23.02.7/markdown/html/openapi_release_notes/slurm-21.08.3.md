## Slurm 21.08.3

### openapi/v0.0.37

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

### openapi/dbv0.0.37

#### Correct placement of step TRES

|               |                                                                          |
|---------------|--------------------------------------------------------------------------|
| previous path | .components.schemas."dbv0.0.37_job_step".properties.step.properties.tres |
| new path      | .components.schemas."dbv0.0.37_job_step".properties.tres                 |

### openapi/dbv0.0.36

#### Correct placement of step TRES

|               |                                                                          |
|---------------|--------------------------------------------------------------------------|
| previous path | .components.schemas."dbv0.0.36_job_step".properties.step.properties.tres |
| new path      | .components.schemas."dbv0.0.36_job_step".properties.tres                 |
