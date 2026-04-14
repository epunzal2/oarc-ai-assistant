# <span id="top">Slurm Priority Site Factor Plugin API</span>

## Overview

This document describes Slurm site_factor plugins and the API that defines them. It is intended as a
resource to programmers wishing to write their own Slurm site_factor plugins.

Slurm site_factor plugins are Slurm plugins that implement the Slurm site_factor API described
herein. They are designed to provide the site a way to build a custom multifactor priority factor,
and will only be loaded and operation alongside
<span class="commandline">PriorityType=priority/multifactor</span>.

The plugins are meant to set and update the <span class="commandline">site_factor</span> value in
the <span class="commandline">job_record_t</span> corresponding to a given job. Note that the
<span class="commandline">site_factor</span> itself is an unsigned integer, but uses
<span class="commandline">NICE_OFFSET</span> as an offset to allow the value to be positive or
negative. The plugin itself must add <span class="commandline">NICE_OFFSET</span> to the value
stored to <span class="commandline">site_factor</span> for proper operation, otherwise the value
itself will be extremely negative, and the job priority will likely drop to 1. (The lowest value
that does not correspond to a held job.)

Plugins must conform to the Slurm Plugin API with the following specifications:

<span class="commandline">const char plugin_type\[\]="*major/minor*"</span>  
The major type must be "site_factor" The minor type can be any recognizable abbreviation for the
specific plugin.

<span class="commandline">const char plugin_name\[\]</span>  
Some descriptive name for the plugin. There is no requirement with respect to its format.

<span class="commandline">const uint32_t plugin_version</span>  
If specified, identifies the version of Slurm used to build this plugin and any attempt to load the
plugin from a different version of Slurm will result in an error. If not specified, then the plugin
may be loaded by Slurm commands and daemons from any version, however this may result in difficult
to diagnose failures due to changes in the arguments to plugin functions or changes in other Slurm
functions used by the plugin.

## API Functions

The following functions must appear. Functions which are not implemented must be stubbed, or the
plugin will fail to load.

int init(void)

**Description**:  
Called when the plugin is loaded, before any other functions are called. Put global initialization
here.

**Returns**:  
<span class="commandline">SLURM_SUCCESS</span> on success, or  
<span class="commandline">SLURM_ERROR</span> on failure.

void fini(void)

**Description**:  
Called when the plugin is removed. Clear any allocated storage here.

**Returns**: None.

**Note**: These init and fini functions are not the same as those described in the
<span class="commandline">dlopen (3)</span> system library. The C run-time system co-opts those
symbols for its own initialization. The system <span class="commandline">\_init()</span> is called
before the Slurm <span class="commandline">init()</span>, and the Slurm
<span class="commandline">fini()</span> is called before the system's
<span class="commandline">\_fini()</span>.

void site_factor_p_reconfig(void)

**Description**: Refresh the plugin's configuration. Called whenever slurmctld is reconfigured.

**Returns**: void

void site_factor_p_set(job_record_t \*job_ptr)

**Description**: Sets the site_priority of the job, if desired.

**Arguments**:  
<span class="commandline">job_ptr</span> (input) pointer to the job record.

**Returns**: void

void site_factor_p_update(void)

**Description**: Handle periodic updates to all site_priority values in the job_list. Called every

**Returns**: void

## Parameters

These parameters can be used in the slurm.conf to configure the plugin and the frequency at which to
gather information about running jobs.

<span class="commandline">PrioritySiteFactorParameters</span>  
Optional parameters for the site_factor plugin. Interpretation of any value is left to the
site_factor plugin itself.

<span class="commandline">PrioritySiteFactorPlugin</span>  
Specifies which plugin should be used.

<span class="commandline">PriorityCalcPeriod</span>  
Interval between calls to <span class="commandline">site_factor_p_update()</span>

Last modified 23 October 2019
