# HPC Starter’s Microguide
*July 2025*

Welcome to the Amarel cluster! This guide provides a quick start for new users, focusing on terminal and command-line usage. For a more comprehensive guide, please see the [Amarel Cluster User Guide](https://sites.google.com/view/cluster-user-guide/amarel).

## 1. Logging In

You can log in to the Amarel cluster using your Rutgers NetID and password. Your username is your NetID.

```bash
ssh <NetID>@amarel.rutgers.edu
```

For more details on getting started, please refer to the [Welcome Guide](https://sites.google.com/view/cluster-user-guide/amarel/welcome).

## 2. Navigating Module Usage

Environment modules are used to manage software packages on the cluster. You can load and unload different software versions as needed for your work.

### Searching for Modules

To find available software, you can use the `module spider` or `module avail` commands:

```bash
# Search for a specific package
module spider <package_name>

# List all available modules
module avail
```

### Loading a Module

To load a specific module into your environment, use the `module load` command. For example, to load a version of Apptainer:

```bash
module load apptainer/1.3.6
```

Some software is contributed by the community and requires an extra step to see the modules:
```bash
module use /projects/community/modulefiles
module avail
```
For more detailed information on available applications, see the [Applications Guide](https://sites.google.com/view/cluster-user-guide/amarel/applications) and the [Community Contributed Software Guide](https://sites.google.com/view/cluster-user-guide/amarel/community).

## 3. Submitting a Simple Job

Jobs on the cluster are submitted using the SLURM scheduler. You submit jobs by creating a submission script and using the `sbatch` command.

Here is a simple example of a SLURM script that runs a basic command:

```bash
#!/bin/bash
#SBATCH --job-name=simple_job      # Job name
#SBATCH --nodes=1                    # Number of nodes
#SBATCH --ntasks=1                   # Total number of tasks
#SBATCH --cpus-per-task=1            # Cores per task
#SBATCH --mem=1G                     # Memory per node
#SBATCH --time=00:10:00              # Walltime
#SBATCH --output=simple_job_%j.out   # Standard output and error log

# Your commands go here
echo "Hello, HPC World!"
hostname
date
```

### Key `#SBATCH` Directives:

*   `--job-name`: A name for your job.
*   `--nodes`: The number of compute nodes to request.
*   `--ntasks`: The total number of tasks your job will run.
*   `--cpus-per-task`: The number of CPU cores per task.
*   `--mem`: The amount of memory your job needs.
*   `--time`: The maximum time your job is allowed to run.
*   `--output`: The file where standard output and errors will be written.

To submit this job, save it as a file (e.g., `submit.sh`) and run:
`sbatch submit.sh`

You can find more complex examples in the [Applications Guide](https://sites.google.com/view/cluster-user-guide/amarel/applications).

## 4. Basic HPC Do’s and Don’ts

To ensure the cluster runs smoothly for everyone, please follow these best practices:

*   **Storage:**
    *   Use your `/home/<NetID>` directory (100 GB, backed up) for important files, source code, and small datasets.
    *   Use your `/scratch/<NetID>` directory (1 TB, not backed up) for temporary files and large data needed for actively running jobs. Files in `/scratch` older than 90 days are automatically deleted.
*   **Login Nodes:** Login nodes should be used for file transfers, installing software, editing/compiling code, and submitting jobs. Do **not** run computationally intensive or long-running processes on them.
    *   **File Transfers:** Always use login nodes for transferring files (e.g., with `rclone`, `scp`). They have higher bandwidth for better performance.
    *   **Compute Jobs:** All intensive work must be submitted to the compute nodes via SLURM jobs.
*   **Acceptable Use:** Be sure to read and understand the [Acceptable Use Policies](https://rutgers.app.box.com/v/oarc-systems-mgmt-aup). Misuse of resources can lead to account suspension.

For more details, refer to the [Welcome Guide](https://sites.google.com/view/cluster-user-guide/amarel/welcome), [Owner Guide](https://sites.google.com/view/cluster-user-guide/amarel/owner-guide), and the main [Cluster User Guide](https://sites.google.com/view/cluster-user-guide/amarel).