## Slurm 21.08.6

### openapi/dbv0.0.37

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
<li>.components.schemas."dbv0.0.37_association".properties.is_default</li>
<li>.components.schemas."dbv0.0.37_association".properties.max.tres.group.minutes</li>
<li>.components.schemas."dbv0.0.37_association".properties.max.tres.group.active</li>
<li>.components.schemas."dbv0.0.37_association".properties.max.jobs.active</li>
<li>.components.schemas."dbv0.0.37_association".properties.max.jobs.accruing</li>
<li>.components.schemas."dbv0.0.37_association".properties.max.jobs.total</li>
<li>.components.schemas."dbv0.0.37_association".properties.max.tres.minutes.per.job</li>
</ul></td>
</tr>
</tbody>
</table>

#### Move incorrectly named field

|          |                                                                                        |
|----------|----------------------------------------------------------------------------------------|
| old path | .components.schemas."dbv0.0.37_qos".properties.limits.max.jobs.per.account             |
| new path | .components.schemas."dbv0.0.37_qos".properties.limits.max.jobs.active_jobs.per.account |

#### Move incorrectly named field

|  |  |
|----|----|
| old path | .components.schemas."dbv0.0.37_qos".properties.limits.properties.max.properties.jobs.properties.per.properties.user |
| new path | .components.schemas."dbv0.0.37_qos".properties.limits.properties.max.properties.jobs.properties.active_jobs.properties.per.properties.user |

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
<li>.components.schemas."dbv0.0.37_qos".properties.limits.properties.factor</li>
<li>.components.schemas."dbv0.0.37_qos".properties.limits.properties.max.properties.accruing.properties.per.properties.account</li>
<li>.components.schemas."dbv0.0.37_qos".properties.limits.properties.max.properties.accruing.properties.per.properties.user</li>
</ul></td>
</tr>
</tbody>
</table>
