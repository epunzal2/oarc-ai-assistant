## Slurm 21.08.8

### openapi/dbv0.0.37

#### Move response fields in dbv0.0.37_diag under "statistics"

<table class="tchange">
<colgroup>
<col style="width: 33%" />
<col style="width: 33%" />
<col style="width: 33%" />
</colgroup>
<tbody>
<tr class="trchange">
<td class="tdfield">new parent field</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."dbv0.0.37_diag".properties.statistics</li>
</ul></td>
</tr>
<tr class="trchange">
<td class="tdfield">subordinated fields</td>
<td colspan="2" class="tdchange"><ul>
<li>.components.schemas."dbv0.0.37_diag".properties.time_start</li>
<li>.components.schemas."dbv0.0.37_diag".properties.rollups</li>
<li>.components.schemas."dbv0.0.37_diag".properties.RPCs</li>
<li>.components.schemas."dbv0.0.37_diag".properties.users</li>
</ul></td>
</tr>
</tbody>
</table>
