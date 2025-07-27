
Cluster User Guide	
AmarelCaliburn
The Amarel Cluster
Overview
Getting access (requesting an account)
Boilerplate for proposal development
Acknowledging OARC or Amarel
User environment
Login nodes (proper use)
Granting access to files and folders for other users
Applications and libraries
Installing your own software
Available compute hardware
Job partitions (job submission queues)
Connecting to the cluster
Command-line access via SSH
Using the Open OnDemand interface
Using the FastX interface
Storage file sets and how to use them
/home
/scratch
/projects
/mnt/scratch
Home and Projects Snapshots
Best practices
Basics of moving files to/from the cluster
Transferring files with external institute using cloud bucket
With GCP
With AWS
Transferring files using Globus Personal Connect
Transferring files to cloud storage using rclone
Setting-up your rclone configuration on Amarel
Using rclone to move files
Splitting large files
Passwordless access and file transfers using SSH keys
Job scheduler (batch system)
Current configuration
Serial job example
Parallel (multicore MPI) job example
Interactive job example
Parallel interactive job example
Job array example
Some helpful tips
Monitoring job status
Actively running jobs
Completed or terminated jobs
Cancelling jobs
Connecting your lab's systems to Amarel
Checking storage utilization
Snapshots of /home and /projects data
FAQ

Overview
The Amarel cluster is the primary research computing system at Rutgers and it is available for use by all Rutgers faculty, staff, and students at no cost. Amarel is a heterogeneous community-model Linux cluster comprising tens of thousands of Intel Xeon cores, various models and configurations of NVIDIA GPUs, and multiple 1.5 TB RAM large-memory nodes, all sharing a Mellanox InfiniBand fabric and an IBM Spectrum Scale concurrent-access cluster file system.

This system was named in honor of Dr. Saul Amarel, one of the founders of the Rutgers Computer Science Department, who is best known for his pioneering work in artificial intelligence applied to scientific inquiry and engineering practice. 

Getting access (requesting an account)
Rutgers students, staff, and faculty, please use this form to request access to Amarel: 

https://oarc.rutgers.edu/amarel-cluster-access-request/

Who may access and use the Amarel cluster?  The Amarel cluster is funded by Rutgers University and managed by OARC as a research resource available to all current Rutgers students, staff, faculty (including faculty designated by the University as professor emeritus). That means only current Rutgers students, staff, and faculty are authorized to access those University-owned systems: upon graduation or ending employment with the University, a user will automatically lose the ability and authorization to connect to or use the system. Compute and storage resources within the Amarel system can be purchased ("owned") by departments or individual members of the Rutgers research community. That enables them to grant access to their owned compute and storage resources to external users (any non-Rutgers personnel such as visiting scholars or personnel at other institutions) using a Rutgers Guest NetID.

You must be able to access email sent to your NetID@rutgers.edu address. That address is the "Default Personalized Address" setup by OIT when a NetID is generated. OIT provides all Rutgers students, staff, and faculty with a NetID@rutgers.edu account because that enables some automated (system-generated) messages of importance to reach NetID holders, regardless of what other personalized email addresses they may have setup. All communications sent to any of your personalized email addresses will be delivered to all listed delivery account(s) you create. So, the intent is to have messages sent to your NetID@rutgers.edu account also reach your other personalized Rutgers email addresses. Disabling or otherwise circumventing this feature makes it impossible for some OIT units (including OARC) to contact you about system or account related issues.

Boilerplate for proposal development
A Microsoft Word .docx file with a summary of our compute, storage, and networking resources is available here: https://rutgers.box.com/v/oarc-facilities-info

Acknowledging OARC or Amarel
Please reference OARC or the Amarel cluster in any research report, journal, or publication that requires citation of an author's work. Recognizing the OARC resources you used to conduct your research is important for our process of acquiring funding for hardware, support services, and other infrastructure improvements. The minimal content of a reference should include:

Office of Advanced Research Computing (OARC) at Rutgers, The State University of New Jersey

A suggested acknowledgement is:

The authors acknowledge the Office of Advanced Research Computing (OARC) at Rutgers, The State University of New Jersey for providing access to the Amarel cluster and associated research computing resources that have contributed to the results reported here. URL: https://oarc.rutgers.edu

User environment
The default command-line interface shell for all users is Bash, but many other shells are available. In your Bash shell, environment customization can be done using the ~/.bashrc file (preferred method) or the ~/.bash_profile file. 

The Open OnDemand system is available as a graphical interface for some systems. Open OnDemand offers a web browser based graphical Linux desktop for GUI-based applications (no need to use the command-line interface).

Login nodes (proper use)
When you connect to a cluster, the machine or "node" where you start is known as a login node (also called a master node, head node, or user node). Cluster login nodes provide a shared environment where users can transfer data, build software, and prepare their calculations. Sometimes, there can often be over 100 users connected to a login node at one time.

Running applications on a shared login node or doing things that consume significant compute, memory, or network resources can unfairly impact other users. Please do not do that. Do not run your research applications on the login node. Even "small tests" that last more than a few seconds can create problems.

If you're not sure about whether it's okay to do something on a login node, just ask:  help@oarc.rutgers.edu

Your jobs (calculations, simulations, analyses, performance tests, etc.) should only be run on compute nodes and there are many easy ways to quickly get access to a compute node. If you need to quickly run a command, test something, or do a little math, without preparing a job script, use the srun command. Here's an example:

srun python -c 'print(8867*573527)'

That runs a quick calculation using Python on a compute node.

Yes, that may take a moment to start, but thank you for using the job scheduler and doing it right.

[gc563@amarel1 ~]$ srun python -c 'print(8867*573527)'

srun: job 34165665 queued and waiting for resources

srun: job 34165665 has been allocated resources

5085463909

Granting access to files and folders for other users
The commands getfacl and setfacl are useful for understanding permissions and providing read(r), write(w), and execute(x) access to files and folders. 

Running the getfacl command will return the current associated permissions to a file/folder. 

[so398@amarel1 example]$ getfacl examplescript

# file: examplescript

# owner: so398

# group: so398

user::rwx

group::rwx

other::r-x

Using the setfacl command with -m (--modify) will allow assignment of any or all of the following permissions: r (read), w (write), x (execute) to a designated u(ser): <netID>:<permission level> <filename>  or  g(roup):<groupname>:<permission level> <filename>.

Here so398 is providing user gc563 read, write, and execute permissions to ‘examplescript’.

[so398@amarel1 example]$ setfacl -m u:gc563:rwx examplescript              	

 Here so398 is providing group ‘oarc’ read only permissions to ‘examplescript’.

[so398@amarel1 example]$ setfacl -m g:oarc:r examplescript                 

 Running getfacl will show the new permissions.

[so398@amarel1 example]$ getfacl examplescript

# file: examplescript

# owner: so398

# group: so398

user::rwx

user:gc563:rwx

group::rwx

group:oarc:r--

mask::rwx

other::r-x

 All assigned permissions may be removed by using -b (--remove-all).  Otherwise, selectively remove permissions using -x (--remove) u(ser):<NetID> <filename> or -x (--remove) g(roup):<groupname> <filename>.

Here so398 is removing all permissions to ‘examplescript’.

[so398@amarel1 example]$ setfacl -b examplescript

[so398@amarel1 example]$ getfacl examplescript

# file: examplescript

# owner: so398

# group: so398

user::rwx

group::rwx

other::r-x

 Sometimes it is necessary to change permissions on all already existing files in the directory or/and setup a default permissions for newly created files in the future. The following commands can be helpful:

setfacl -R -m u:user2:rwx /scratch/user1/shared.directory 

## gives USER2 read, write, exec permissions for currently existing files and folders, recursively 



setfacl -R -m g:oarc:rwx /scratch/user1/shared.directory 

## gives group OARC read, write, exec permissions for currently existing files and folders, recursively



setfacl -R -m o::x /scratch/user1/shared.directory 

## revokes read and write permission for everyone else in existing folder and subfolders, recursively



setfacl -R -d -m g::rwx /scratch/user1/shared.directory 

## gives group rwx permissions by default, recursively



setfacl -R -d -m o::--- /scratch/user1/shared.directory 

## revokes read, write and execute permissions for everyone else.

Note: "default" ACL settings are separate from regular ACL settings, so both must be set separately. For example, set the ACL for a directory as desired, then add the -d option to your command to make those settings the default settings. 

Also, be aware that simply granting access to a file or directory may not be sufficient if that file or directory resides within another directory that you haven't granted access to. In other words, if you share something with another user, be sure to adjust the access settings for the parent directory or directories to enable them to get to the thing you're sharing.

Applications and libraries
We have multiple collections of software accessible by all users and we use the Lmod module system for managing convenient loading and unloading of software packages and environment configurations. In addition, individuals or research groups can manage their own custom software modules using the Lmod tools available on each cluster.

Many of the commonly-used applications available on Amarel have detailed instructions and examples provided on our Applications page.

A list showing most of the available applications and libraries can be generated with the module spider command.

There are multiple repositories of software on Amarel. For example, we have a large repository of community-contributed software. That is, software installed by users to be shared with others. To access this repository, add it to your MODULEPATH environment variable like this:

module use /projects/community/modulefiles

Now, when you list available software with module spider or module avail, you'll see the community-contributed software also.

The module load <name/version> command is used to configure your user environment for using a particular application or set of libraries.

If you always use the same software modules, your ~/.bashrc file can be configured to load those modules automatically every time you log-in. Just add your desired module load command(s) to the bottom of that file. You can always edit your ~/.bashrc file to change or remove those commands later.

The software that is already available on the cluster and listed with module spider is a very small slice of the broad range of software that researchers using our systems actually use. Users are expected to install and manage their own applications, scripts, and libraries, but OARC staff are available to help with that process.

Software installed cluster-wide is typically configured with default or standard (basic) options, so special performance-enhancing features may not be enabled. This is because our clusters usually include a variety of hardware platforms and cluster-wide software installations must be compatible with all of the available hardware, including older compute nodes. If the performance of the software you use for your research can be enhanced using hardware-specific options (e.g., targeting special CPU core instruction sets), you should consider installing your own customized version of that software in your /home directory.

Installing your own software
Package management tools like yum or apt, which are used to install software in typical Linux systems, are not available to users of shared computing systems like Amarel. So, most packages need to be compiled from their source code and then installed. Further, most packages are generally configured to be installed in /usr or /opt, but these locations are inaccessible to (not writeable for) general users. Special care must be taken by users to ensure that the packages will be installed in their own /home directory (/home/<NetID>).

As an example, here are the steps for installing ZIPPER, a generic example package that doesn’t actually exist:

Download your software package. You can download a software package to your laptop, and then transfer the downloaded package to your /home directory on the cluster for installation. Alternatively, if you have the http or ftp address for the package, you can transfer that package directly to your /home directory while logged-in using the wget utility:   wget http://www.zippersimxl.org/public/zipper/zipper-4.1.5.tar.gz

Unzip and unpack the .tar.gz (or .tgz) file. Most software packages are compressed in a .zip, .tar or .tar.gz file. You can use the tar utility to unpack the contents of these files:  tar -zxf zipper-4.1.5.tar.gz

Read the instructions for installing. Several packages come with an INSTALL or README file with instructions for setting up that package. Many will also explicitly include instructions on how to do so on a system where you do not have root access. Alternatively, the installation instructions may be posted on the website from which you downloaded the software.

Load the required software modules for installation. Software packages generally have dependencies, i.e., they require other software packages in order to be installed. The README or INSTALL file will generally list these dependencies. Often, you can use the available modules to satisfy these dependencies. But sometimes, you may also need to install the dependencies for yourself. Here, we load the dependencies for ZIPPER:
module load intel/19.0.3 mvapich2/2.2

Perform the installation. The next few steps vary widely but instructions almost always come with the downloaded source package. Guidance on the special arguments passed to the configure script is often available by running the ./configure --help command. What you see below is just a typical example of special options that might be specified.

./configure --prefix=$HOME/zipper/4.1.5 --disable-float --enable-mpi --without-x

make -j 4

make install

Several packages are set up in a similar way, i.e., using configure, then make, and make install. Note the options provided to the configure script. These differ from package to package, and are documented as part of the setup instructions, but the prefix option is almost always supported. It specifies where the package will be installed. Unless this special argument is provided, the package will generally be installed to a location such as /usr/local or /opt, but users do not have write-access to those directories. So, here, I'm installing software in my /home/<NetID>/zipper/4.1.5 directory. The following directories are created after installation:

/home/[NetID]/zipper/4.1.5/bin,  where executables will be placed

/home/[NetID]/zipper/4.1.5/lib,  where library files will be placed

/home/[NetID]/zipper/4.1.5/include,  where header files will be placed

/home/[NetID]/zipper/4.1.5/share/man,  where documentation will be placed

Configure environment settings. The above bin, lib, include and share directories are generally not part of the shell environment, i.e., the shell and other programs don’t “know” about these directories. Therefore, the last step in the installation process is to add these directories to the shell environment:

export PATH=/home/<NetID>/zipper/4.1.5/bin:$PATH

export C_INCLUDE_PATH=/home/<NetID>/zipper/4.1.5/include:$C_INCLUDE_PATH

export CPLUS_INCLUDE_PATH=/home/<NetID>/zipper/4.1.5/include:$CPLUS_INCLUDE_PATH

export LIBRARY_PATH=/home/<NetID>/zipper/4.1.5/lib:$LIBRARY_PATH

export LD_LIBRARY_PATH=/home/<NetID>/zipper/4.1.5/lib:$LD_LIBRARY_PATH

export MANPATH=/home/<NetID>/zipper/4.1.5/share/man:$MANPATH

These export commands are standalone commands that change the shell environment, but these new settings are only valid for the current shell session. Rather than executing these commands for every shell session, they can be added to the end of your ~/.bashrc file which will result in those commands being executed every time you log-in to the cluster.

Available compute hardware
Amarel is a heterogeneous computing system with many different node types and hardware features such as NVIDIA GPUs, large memory nodes with Intel Optane DIMMs, and InfiniBand FDR/EDR network interfaces.

Below is a list of the nodes with their specifications and other features. These data can be obtained using the sinfo command, like this:  sinfo --Node --format="%n %f %c %m %G".  The Intel Xeon core models can be identified by their model names (e.g., cascadelake, sandybridge, broadwell) and this information can be used to determine which special instruction sets are supported. For example, the nodes with ivybridge cores support AVX but not AVX2.


Job partitions (job submission queues)
Job partitions are collections of compute nodes that are configured for handling jobs that fall in specific categories of size, duration, location, and access. Below is a summary of the general-access job partitions, but there are many private job partitions such as those belonging to Amarel owners. Guest NetID holders are usually limited to using only Amarel owner job partitions.

Before requesting resources (compute nodes), it can be helpful to see what resources are available and what cluster partitions to use for certain resources.

Example of using the sinfo command:

[gc563@amarel1 ~]$ sinfo -s

PARTITION  AVAIL  TIMELIMIT   NODES(A/I/O/T)  NODELIST

main*         up 3-00:00:00     265/19/6/290  gpu[001-010],hal[0001-0190],mem[001-005],pascal[001-010],slepner[009-048,054-088]

gpu           up 3-00:00:00        14/4/1/19  gpu[001-003,005-010],pascal[001-010]

mem           up 3-00:00:00          5/0/0/5  mem[001-005]

nonpre        up 3-00:00:00          4/0/0/4  slepner[085-088]

graphical     up 1-00:00:00          0/1/0/1  sirius3

cmain         up 3-00:00:00       46/0/21/67  halc[001-067]

Understanding this output:

There are 5 partitions shown here, 

main (traditional compute nodes, CPUs only, jobs running here are preemptible)

The main partition is the default job partition for all general-access (non-guest) users. If you don't specify a partition for your job, it will be directed to the main partition. This is the largest partition and includes most of the compute nodes that comprise the Amarel cluster. This partition should be used for jobs that do no require GPU hardware and that do not require large memory configurations (>248 GB RAM per node).

gpu (nodes with any of our large collection of general-purpose GPU accelerators)

mem (CPU-only nodes with 512 GB to 1.5 TB RAM).

nonpre (a partition where jobs won't be preempted by higher-priority or owner jobs)

graphical (a specialized partition for jobs submitted by the OnDemand system)

cmain (the "main" partition for the Amarel resources located in Camden, note that /scratch for those nodes is within the Amarel-C system)

Note: the upper limit for a job’s run time is 3 days (DD-HH:MM:SS), but only 1 day in the graphical partition.

Connecting to the cluster
If you are connecting from a location outside the Rutgers campus network, you must first connect to the campus network using the Rutgers VPN (virtual private network) service. See here for details and support: https://soc.rutgers.edu/vpn

A video demonstrating various methods of connecting to Amarel is available in our Introduction to Amarel video training series.

Command-line only from OS X (Terminal)

Command-line only from Windows 10 (MobaXterm)

Open OnDemand for a graphical desktop environment (web browser)

FastX for a graphical desktop environment (web browser)


Command-line access via SSH
Accessing the cluster using a command-line interface is done using an SSH (Secure Shell) connection:

ssh <NetID>@amarel.rutgers.edu

The password to use is your standard NetID password. If you're having trouble with your NetID or password, please see https://netid.rutgers.edu for tools and support.

The hostname for the Amarel cluster is amarel.rutgers.edu

The hostname for the Amarel-C cluster (the cluster in Camden) is amarelc.rutgers.edu

The hostname for the Amarel-N cluster (the cluster in Newark) is amareln.rutgers.edu

When you connect to this system, your log-in session (your Linux shell) will begin on one of multiple log-in nodes, named amarel1, amarel2, etc. So, while you are logged-in to Amarel, you will see "amarel1" or "amarel2" as the name of the machine you are using.

Using the Open OnDemand interface
For users who need a graphical desktop environment, there is an option to connect to the cluster via a web browser either from campus or through VPN if connecting from off-campus. Both using the system (submitting jobs) and uploading/downloading files can be achieved through this interface, but there are some performance issues to consider (see here for details). The Open OnDemand system uses a Singularity image to provide the tools and libraries of the Amarel system.

Note: when using the Open OnDemand interface, the Cisco AnyConnect client must be used (not the browser-based VPN connection).

How to access and use it:

Connect to the campus VPN using the Cisco AnyConnect client software. Do not use the browser-based VPN connection.

Go to https://ondemand.hpc.rutgers.edu (when you reach that page, the address in your browser should being with  https://ondemand  and not  https://vpn)

Log-in with your NetID and standard NetID password,

choose ‘Interactive Apps,’

choose ‘Amarel Desktop’ or ‘Sirius3 Desktop’ to launch a desktop environment,

specify the duration and number of cores needed for your job (1 hour and 1 core are defaults, but more time may be needed) and click ‘Launch,’

when your desktop session is ready to start, click on the ‘Launch noVNC in New Tab’ button. Your desktop session will open in a new browser tab. You can add desktop icons for commonly used applications, but at first, all applications must be launched from the command-line/terminal.

To launch an application, click on the little black ‘MATE Terminal’ icon on the menu bar at the top of your desktop,

use the module load command to load an application (e.g., module load MATLAB/R2019a),

with your software module loaded, you can then launch your application (e.g., just type matlab).

Of course, other modules can be loaded instead. For example, SAS/9.4, spss/26, gaussian/16revA03, Mathematica/11.3, and many more.

Moving files using the OnDemand system:

In the main OnDemand window, select the Files drop-down menu and click on Home Directory to open the file transfer tool. You can download and upload files using this tool.

If your session is lost somehow or unrecoverable:

A desktop session provided by FastX or Open OnDemand is not cached, checkpointed, or backed-up. Individual applications used during a session may capture unsaved work (similar to a word processor "autosaving" a file every few minutes), but the desktop session, itself, is not backed-up or saved. So, data not saved to disk can be lost in a variety of circumstances: a node hosting the session crashes or is rebooted, the session exceeds its memory limit, hardware failure, etc.

Using the FastX interface
For users who need a graphical desktop environment that runs natively on the Amarel system (not using a Singularity image), the FastX system provides an additional option for connecting to the cluster via a web browser either from campus or through VPN if connecting from off-campus. Both using the system (submitting jobs) and uploading/downloading files can be achieved through this interface, but there are some performance issues to consider (see here for details).

How to access and use it:

Connect to the campus VPN using the Cisco AnyConnect client software. Do not use the browser-based VPN connection.

Go to https://amarel.hpc.rutgers.edu:3443 (when you reach that page, the address in your browser should being with  https:// and not  https://vpn)

Log-in with your NetID and standard NetID password,

click on the ‘Launch Session’ button,

choose ‘XFCE Desktop’ and then click the 'Launch' button to launch a desktop environment in a new browser tab.

When your deskop environment appears, it's important to note that this session is running on an Amarel login node. That means you must launch an interactive session on a compute node before running applications. To do that, right-click on the Desktop and select 'Open Terminal Here.'

When your Terminal window appears, use the srun command to launch an interactive session. Note: X11 tunneling for GUI-based applications will be enabled by default. For example, here I'll request a session with 2 cores for 45 minutes:

srun --cpus-per-task=2 --time=00:45:00 --pty bash

use the module load command to load an application (e.g., module load MATLAB/R2019a),

with your software module loaded, you can then launch your application (e.g., just type matlab).

Of course, other modules can be loaded instead. For example, SAS/9.4, spss/26, gaussian/16revA03, Mathematica/11.3, and many more.

An alternative to using the web interface is to use the locally-installed FastX client. In some cases, using the client can offer better performance and some helpful features. Downloads for the version of FastX we currently have setup on Amarel are available here: https://www.starnet.com/fastx/current-client?version=2.4.16

Storage file sets and how to use them
/home
Your /home directory at /home/<NetID> is accessible from all login and compute nodes. On most systems, your /home directory is a small space intended for storage of software tools, valuable private files, and environment configuration files. Launching jobs on the cluster from within your /home directory is possible, but you will not experience optimal reading and writing performance there because the /home fileset is not configured for speed. This directory is backed-up in the form of a weekly snapshot and these snapshots are retained for 3 to 4 weeks. 

You have a 100 GB quota for your /home directory (i.e., 100. If you fill-up all of that space, you will no longer be able to write data there and that can cause some applications to stop working or it can cause jobs to fail. See here for details on how to check your 

/scratch
Your /scratch directory at /scratch/<NetID> is accessible from all login and compute nodes on a particular campus. The /scratch filesystem is local to the compute nodes on each campus, so the /scratch directories accessible from compute nodes in Camden are not the same as the /scratch directories accessible from compute nodes in Newark. On most systems, your /scratch directory is a large space intended for temporary storage of input and output files associated actively running jobs. This is the best location for running your jobs because, here, you have more space than in your /home directory and you can have multiple jobs or tasks concurrently reading and writing. The trade-off for performance and extra space in this directory is that nothing in the /scratch directory is backed-up. If you delete files in your /scratch directory, they cannot be recovered. 

Your /scratch space is managed using a quota system. Each user has 1 TB of space in their /scratch directory, but there is also soft/hard limit scheme where 1 TB is the soft limit (subject to a 2-week grace period) and 2 TB is the hard limit. That means, if you place more than 1 TB of data in your /scratch directory, you can keep adding data there for up to 2 weeks, but you must reduce the amount of data there to below the 1 TB quota or you will lose the ability to write any data to your /scratch directory. At no time can you write more than 2 TB of data in your /scratch directory (hard limit). In addition, the /scratch file set uses an automated purge process that deletes files (only files, not directories) that sit unaccessed for 90 days if the /scratch directory owner is over-quota (i.e., if there is more than 1 TB in the /scratch directory). So, be sure to move important data out of your /scratch directory to a backed-up storage space in case you go over-quota and trigger the purge process.

The general approach for using /scratch is to copy your job's files (input files, libraries, etc.) to /scratch, run your job and write output files to /scratch, then move the files you need to save to your /home or /projects directory. There are multiple ways to stage your input files before a job begins and multiple ways to transfer output files to long-term storage after calculations are complete. Below are some examples.

You can manually stage needed files in /scratch before a job. In this example, I'm copying files to my /scratch directory on the Amarel-C system because I plan to use Camden-based compute nodes:

scp my-dir-of-input-files.tar.gz gc563@amarelc.rutgers.edu:/scratch/gc563

ssh gc563@amarelc.rutgers.edu "tar -zxf /scratch/gc563/my-dir-of-input-files.tar.gz"

You can stage needed files in /scratch from within a job (either within your job script for a batch job or on the command line during an interactive job). In this example, I'm not concerned about which Amarel system/site my job will use because the file transfer is done after my job is assigned to any compute node:

mkdir /scratch/$USER/$SLURM_JOB_NAME-$SLURM_JOB_ID

scp my-dir-of-input-files.tar.gz /scratch/$USER/$SLURM_JOB_NAME-$SLURM_JOB_ID

tar -zxf /scratch/$USER/$SLURM_JOB_NAME-$SLURM_JOB_ID/my-dir-of-input-files.tar.gz

Similar commands can be used for moving newly-generated output files back to your /home or /projects directories. This can be done manually,

scp my-dir-of-output-files.tar.gz gc563@amarel.rutgers.edu:/home/gc563

or from within a job script or interactive session:

cp -pru /scratch/$USER/$SLURM_JOB_NAME-$SLURM_JOB_ID/* $SLURM_SUBMIT_DIR

/projects
Compute node owners and former owners may have a shared directory for group/team/department use. These directories are found in the /projects file set at /projects/<storage_ID>. Directories in /projects have characteristics that closely match those of the /home directories: this is not a good place for reading and writing for actively running jobs. Instead, this is where you should store group-shared software, scripts, and data that need to be backed-up on a weekly basis. If you are part of a group that has /projects space, OARC will need confirmation from the owner of that space before you can be granted access.

/mnt/scratch
The local scratch space available on most compute nodes is a storage space unique to each individual node (it's the hard drive installed in that compute node) accessible at /mnt/scratch. There are no preexisting directories there, just stage data or write there, then clean-up when your calculations end. Depending on how you use it, this space can perform very fast, but the space will be limited to just a few hundred GB. You must remove all files from /mnt/scratch before your job on that node ends because, without a job running on a node, you won't be able to access that node to rescue files you leave behind.

Home and Projects Snapshots

We take the snapshots of the home and project directories on a regular basis. The snapshots are found in two different locations. 

/cache/.snapshots is the location of the home snapshot. 

/projects<x>/.snapshots is the location of the projects snapshot where projects<x> refers to projectsp, projectsn, or projectsc.


Note that you will come across projects directory under home snapshot. Please ignore this since it is a symbolic link for the cached file system. The actual projects snapshot is located under /projects<x>/.snapshots. 


More details about the snapshots and their time stamp details can be found  in a separate subsection. 

Best practices
Move files to your /scratch directory and run your job from that location.

Don't leave files sitting unused (unaccessed) for a long time because you may lose them to the 90 day purge process.

Frequently check the utilization or quota for your /home and /scratch directories to ensure that they don't become unusable due to over-filling with files.

Basics of moving files to/from the cluster
Note: Amarel's login nodes use a different network route from that of the compute nodes. Login nodes utilize a bigger "pipe" (greater bandwidth) for faster-performance access to the Internet. The compute nodes do not have external network access of their own (they are not directly connected), so compute nodes have to route network traffic (downloads and uploads) through a gateway that all the compute nodes share. Compute nodes may be shared by multiple jobs, so it is possible for the network bandwidth to/from a compute node to be monopolized by a single user. Therefore, optimal performance in moving files to/from Amarel is achieved using the login nodes.

There are many different ways to move data to/from Amarel: secure copy (scp), remote sync (rsync), an FTP client (FileZilla), the file transfer tool in Open OnDemand, etc. The outward-facing network performance from Amarel's login nodes is generally much better than from compute nodes, so it is recommended that long-running transfers of data be completed on the login nodes.

Let’s assume you’re logged-in to a local workstation or laptop and not connected to Amarel. To send files from your local system to your Amarel /home directory,

scp file-1.txt file-2.txt <NetID>@amarel.rutgers.edu:/home/<NetID>

To pull a file from your Amarel /home directory to your laptop (note the “.” at the end of this command),

scp <NetID>@amarel.rutgers.edu:/home/<NetID>/file-1.txt .

If you want to copy an entire directory and its contents using scp, you’ll need to “package” your directory into a single, compressed file before moving it:

tar -czf my-directory.tar.gz my-directory

After moving it, you can unpack that .tar.gz file to get your original directory and contents:

tar -xzf my-directory.tar.gz

A handy way to synchronize a local file or entire directory between your local workstation and the Amarel cluster is to use the rsync utility. First, let's sync a local (recently updated) directory with the same directory stored on Amarel:

rsync -trlvpz work-dir gc563@amarel.rutgers.edu:/home/gc563/work-dir

In this example, the rsync options I'm using are:

t (preserve modification times)

r (recursive, sync all subdirectories)

l (preserve symbolic links)

v (verbose, show all details)

p (preserve permissions)

z (compress transferred data)

To sync a local directory with updated data from Amarel:

rsync -trlvpz gc563@amarel.rutgers.edu:/home/gc563/work-dir work-dir

Here, we've simply reversed the order of the local and remote locations.

For added security, you can use SSH for the data transfer by adding the e option followed by the protocol name (SSH, in this case):

rsync -trlvpze ssh gc563@amarel.rutgers.edu:/home/gc563/work-dir work-dir

Transferring files with external institute using cloud bucket
For file transfer between institutes, we recommend using cloud buckets. The following is the instructions how to set up, configure and upload/download files with external institutes on Amarel, using AWS S3, and/or gcp bucket, provided that the external institute uses the cloud platform as well.


With GCP
 To download/install gcloud sdk

$ curl https://sdk.cloud.google.com | bash   

$ exec -l $SHELL

        or  

$ module load python 

$ python -m pip install gsutil --user     ## install in user's local directory

To initialize the gcloud 

$ gcloud init   ## you have to initialize the gcloud with your gcp account before using this    

To download the <data> file from gcp bucket with <bucket-name>

$ gsutil cp -r gs://bucket-name/<data>  <local_dir>

$ gustil rsync -r gs://bucket-name/<data>  <local_dir>

To upload <data> to gcp bucket

$ gsutil -m cp -R <data-dir> gs://bucket-name  	

-m to perform copying in parallel (multi-threaded/multi-processing) 

-R  copy files including subdirectories from a local directory named<data_dir>

         For more details on using the utility  :    https://cloud.google.com/sdk/docs


With AWS
 To download/install  awscli

$ module load python/3.5.2

$ pip install awscli --user     ## install in user's local directory

$ aws --version

To configure, input your AWS access key ID and secret access key...  

(How to find your AWS access key ID and secret access key: https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html)

$  aws configure         ##follow screen instructions ...

To download or upload

$aws  s3  sync  s3://my-bucket-name .   ##download the S3 bucket <my-bucket-name >

$aws  s3  sync  .  s3://my-bucket-name   ##upload what the local current directory contains to the AWS S3 bucket <my-bucket-name>

         For more details on using the utility  :      https://docs.aws.amazon.com/cli/latest/userguide/

Transferring files using Globus Personal Connect
If there is a Globus endpoint you'd like to access from Amarel, you can install the Globus Personal Connect client in your /home directory to create a personal endpoint for transferring files. File transfers between Amarel and remote systems should be done using Amarel's login nodes. The compute nodes don't offer the external-facing network bandwidth needed for large transfers, but the login nodes are able to handle that. For very large and long-duration transfers, please notify help@oarc.rutgers.edu of your plans so we can ensure proper load distribution of your transfer operations.

To get started with Globus, create an account at https://www.globus.org
Once your account is ready, download the Globus Personal Connect installer for Linux from https://www.globus.org/globus-connect-personal (you'll be installing this in your Amarel /home directory). The command for downloading that installer may look like this:

wget https://downloads.globus.org/globus-connect-personal/v3/linux/stable/globusconnectpersonal-latest.tgz

Unpack the installer and run the setup script:

tar -zxf globusconnectpersonal-latest.tgz 

cd globusconnectpersonal-3.1.1

./globusconnectpersonal -setup

You will be presented with a website URL where you can log-in using Rutgers authentication and acquire an authorization code. Enter that code to proceed.

Provide a descriptive name for your new Globus endpoint on Amarel. For example, using your NetID, "Amarel endpoint for <NetID>" might be a good choice.

Once your new endpoint is registered successfully, you can start your Globus Connect Personal endpoint from the Amarel login node,

./globusconnectpersonal -start &

and then you can access it while logged-in at https://www.globus.org. When not in use for active transfers, you should stop your endpoint (try not to leave it running when not in use):

./globusconnectpersonal -stop

Transferring files to cloud storage using rclone
There are a few different ways to move files to/from box.rutgers.edu. Most of us use a utility named rclone and below I've detailed how I set it up and use it on Amarel. You'll need to open the Firefox browser on Amarel as part of the setup procedure, so connecting via SSH with the -X or -Y option will be needed. Alternatively, if you can't tunnel a GUI through SSH to your local terminal window, you can complete the setup within an Amarel Desktop session using OnDemand. This setup procedure may seem a bit long and complicated. If it seems like you need help, we'd be happy to have a video chat and walk through it with you.

 Setting-up your rclone configuration on Amarel
First, connect to Amarel with X11 tunneling enabled (i.e., using the -X or -Y option). If you're off-campus, you'll need to connect to the campus VPN first (see https://soc.rutgers.edu/vpn for details)

ssh -Y <NetID>@amarel.rutgers.edu

In your terminal window, load the rclone module by running these commands in your terminal window,

module use /projects/community/modulefiles

module load rclone

 Setup a new remote connection for rclone:

rclone config

Enter the letter "n" for new and provide a name for your connection. For this example, I've named mine "amarel-box"

For the storage type, enter "7" for Box: 
Note: This number may change in  the future  versions of rclone, please check the list of available options  and select an appropriate number.

Storage> 7

 You'll be asked for a Box client ID and secret word as well as a Box configuration file and access_token. You can just press "Enter" to leave these fields blank.

client_id>

client_secret>

box_config_file> 

access_token>

Choose a number indicating operation as a user or a service account (operating as a user is the most common configuration):

box_sub_type> 1 

Edit advanced config? (y/n) Choose "No"

y) Yes

n) No

y/n> n

 Use auto config? Choose "Yes"

y) Yes

n) No

y/n> y

Now, rclone will be waiting for an access code. You'll have to use a web browser (Firefox) window to retrieve it. The http://127.0.0.1:53682/auth?state=xxxxxxx  page should load automatically (just wait for it).

Firefox will open a Box/rclone "Customer Login Page" (see attached). Displaying the Firefox window on your local machine may be slow. Be patient.
If after about 2 minutes you still don't see a new Firefox window, use your mouse and right click on the link in the rlcone output in the terminal. Then select "Open URL" or "Open Link"




When it appears, choose "Use Single Sign On (SSO)" and enter your full e-mail address, then click "Authorize." You'll be redirected to the Rutgers Central Authentication Service page where you'll enter your NetID and password.

If that process is successful, you'll then see a button in that browser window for "Grant access to Box." If you see the "Success!" message,  close that browser window and return to the terminal.

In the terminal, you'll see that an access token has been provided. Enter "y" to accept that token.

At this point, you're done and can enter "q" to quit the connection setup.

Using rclone to move files
Note: data transfer performance when using rclone will likely be best on the Amarel login nodes. Here are some example commands where the name of my remote Box connection is "amarel-box":

List directories in top level of your Box (note the ":" at the end)

rclone lsd amarel-box:

List all the files in your Box (note the ":" at the end)

rclone ls amarel-box:

Copy a local (Amarel) directory to Box and name it "my-work-dir-backup":

rclone copy my-work-dir amarel-box:my-work-dir-backup

There is a full list of rclone commands here:  https://rclone.org/commands

Splitting large files
The 50 GB file size limit imposed by Box can be accommodated by splitting large files with either the split utility or using the "chunker" feature of rclone (https://rclone.org/chunker).

Below is an example of how to use the split utility. Here, I'm splitting a large file into 50 GB chunks:

split -b 50GB --additional-suffix=-foo file.txt

This command creates a series of smaller files named as follows:

xaa-foo  xab-foo  xac-foo  xad-foo  xae-foo  xaf-foo ...

Generate a SHA512 checksum for verifying file integrity later:

sha512sum file.txt > file.txt.sha512

 Move those files (the split files and the checksum file) to Box using rclone for long-term storage. Now, the original can be deleted.

rm file.txt

When ready to use that big file again, move the split files and the checksum back using rclone, then reassemble:

cat xa* > file.txt

Now check that the reassembled file matches the original:

sha512sum --check file.txt.sha512

This approach requires some scripting to make it a tractable procedure for large collections of big files, but it gets the job done reliably.

Passwordless access and file transfers using SSH keys
Generate a public/private RSA key pair on your local computer

This can be done using a variety of different key generation algorithms and key sizes. As an example, I'll use the Elliptic Curve Digital Signature Algorithm (ECDSA) and a 521 bit key:

ssh-keygen -t ecdsa -b 521

When I do this, I'll be asked for a filename and passphrase, but the defaults can be accepted by just pressing "Enter" for each:

Enter file in which to save the key (/Users/stanislem/.ssh/id_ecdsa):

Enter passphrase (empty for no passphrase): 

Enter same passphrase again: 

Upload the generated public key to your /home directory on Amarel:

cat ~/.ssh/id_ecdsa.pub | ssh gc563@amarel.rutgers.edu 'cat >> .ssh/authorized_keys'

Set permissions for the authorized_keys file on Amarel:

ssh gc563@amarel.rutgers.edu "chmod 700 .ssh; chmod 600 .ssh/authorized_keys"

Now, you can login to Amarel or transfer files (one or many) using scp or sftp without having to enter a password:

ssh gc563@amarel.rutgers.edu

scp my-big-file.foo gc563@amarel.rutgers.edu:/home/gc563/uploaded_data

scp {1,2,3,4,5,6,7}.txt gc563@amarel.rutgers.edu:/home/gc563/uploaded_data

sftp gc563@amarel.rutgers.edu

If you have SSHFS (a FUSE-based userspace client) installed on your local computer, you can create a local mount point (i.e., a folder on your laptop or lab workstation) that maps to a directory on Amarel so you can manage your files and directories on Amarel as though they are connected to your local computer. The performance is usually about as fast as an NFS mount. We recommend enabling compression (-C) for your SSHFS connection. Also, be sure the directories you're using already exist:
sshfs gc563@amarel.rutgers.edu:/home/gc563/uploaded_data /some/local/path/data_to_upload -C

Job scheduler (batch system)
The job scheduler used on OARC-managed clusters is SchedMD's SLURM Workload Manager.

Any memory-intensive or compute-intensive process should be run using scheduled resources and not simply run on one of our shared login nodes. In short, do not run applications on the login nodes.

Current configuration
Details of the current SLURM job scheduler configuration (job limits, default settings, etc.) can be viewed by running the scontrol show config command. Some settings of interest may include JobRequeue, MaxArraySize, and MaxJobCount.

Serial job example
Here’s an example of a SLURM job script for a serial job. I’m running a program called “zipper” which is in my /scratch directory. I plan to run my entire job from within my /scratch directory because that offers the best filesystem I/O performance.

#!/bin/bash

#SBATCH --partition=main          # Partition (job queue)

#SBATCH --requeue                 # Return job to the queue if preempted

#SBATCH --job-name=zipx001a       # Assign a short name to your job

#SBATCH --nodes=1                 # Number of nodes you require

#SBATCH --ntasks=1                # Total # of tasks across all nodes

#SBATCH --cpus-per-task=1         # Cores per task (>1 if multithread tasks)

#SBATCH --mem=2000                # Real memory (RAM) required (MB)

#SBATCH --time=02:00:00           # Total run time limit (HH:MM:SS)

#SBATCH --output=slurm.%N.%j.out  # STDOUT output file

#SBATCH --error=slurm.%N.%j.err   # STDERR output file (optional)

cd /scratch/$USER

module purge

module load intel/19.0.3 

srun /scratch/$USER/zipper/4.1.5/bin/zipper < my-input-file.in

Understanding this job script:

A job script contains the instructions for the SLURM workload manager (cluster job scheduler) to manage resource allocation, scheduling, and execution of your job.

The lines beginning with #SBATCH contain commands intended only for the workload manager.

My job will be assigned to the “main” partition (job queue).

If this job is preempted, it will be returned to the job queue and will start again when required resources are available

This job will only use 1 CPU core and should not require much memory, so I have requested only 2 GB of RAM. It’s a good practice to request only about 2 GB per core for any job unless you know that your job will require more than that.

My job will be terminated when the run time limit has been reached, even if the program I’m running is not finished. It is not possible to extend this time after a job starts running.

Any output that would normally go to the command line will be redirected into the output file I have specified, and that file will be named using the compute node name and the job ID number.

Be sure to configure your environment as needed for running your application/executable. This usually means loading any needed modules before the step where you run your application/executable.

Here’s how to run that serial batch job using the sbatch command:

sbatch my-job-script.sh

The sbatch command reads the contents of your job script and forwards those instructions to the SLURM job scheduler. Depending on the level of activity on the cluster, your job may wait in the job queue for minutes or hours before it begins running.

Parallel (multicore MPI) job example
Here’s an example of a SLURM job script for a parallel job. See the previous (serial) example for some important details omitted here.

#!/bin/bash

#SBATCH --partition=main            # Partition (job queue)

#SBATCH --requeue                   # Return job to the queue if preempted

#SBATCH --job-name=zipx001a         # Assign a short name to your job

#SBATCH --nodes=1                   # Number of nodes you require

#SBATCH --ntasks=16                 # Total # of tasks across all nodes

#SBATCH --cpus-per-task=1           # Cores per task (>1 if multithread tasks)

#SBATCH --mem=124000                # Real memory (RAM) required (MB)

#SBATCH --time=02:00:00             # Total run time limit (HH:MM:SS)

#SBATCH --output=slurm.%N.%j.out    # STDOUT output file

#SBATCH --error=slurm.%N.%j.err     # STDERR output file (optional)

cd /scratch/$USER

module purge

module load intel/19.0.3 mvapich2/2.2

srun --mpi=pmi2 /scratch/$USER/zipper/4.1.5/bin/zipper < my-input-file.in

Understanding this job script:

The srun command is used to coordinate communication among the parallel tasks of your job. You must specify how many tasks you will be using, and this number usually matches the –ntasks value in your job’s hardware allocation request.

This job will use 16 CPU cores and nearly 8 GB of RAM per core, so I have requested a total of 124 GB of RAM. It’s a good practice to request only about 2 GB per core for any job unless you know that your job will require more than that.

Note here that I’m also loading the module for the parallel communication libraries (MPI libraries) needed by my parallel executable.

Here’s how to run that parallel batch job using the sbatch command:

sbatch my-job-script.sh

Interactive job example
An interactive job gives you an active connection to a compute node (or collection of compute nodes) where you will have a login shell and you can run commands directly on the command line. This can be useful for testing, short analysis tasks, computational steering, or for development activities.

When submitting an interactive job, you can request resources (single or multiple cores, memory, GPU nodes, etc.) just like you would in a batch job:

[gc563@amarel1 ~]$ srun --partition=main --mem=2000 --time=30:00 --pty bash

srun: job 1365471 queued and waiting for resources srun: job 1365471 has been allocated resources

[gc563@slepner045 ~]$

Notice that, when the interactive job is ready, the command prompt changes from <NetID>@amarel1 to <NetID>@slepner045. This change shows that I’ve been automatically logged-in to slepner045 and I’m now ready to run commands there. To exit this shell and return to the shell running on the amarel1 login node, type the exit command.

Parallel interactive job example
To run a parallel job using MPI in an interactive fashion, use salloc to reserve the resources you'll need, then use srun to send your MPI tasks to those reserved resources. 

Here, I'll request 4 cores for 1 hour:

[gc563@amarel1 ~]$ salloc --time=1:00:00 --ntasks=4

salloc: Pending job allocation 37794854

salloc: job 37794854 queued and waiting for resources

salloc: job 37794854 has been allocated resources

salloc: Granted job allocation 37794854

salloc: Waiting for resource configuration

salloc: Nodes hal0048 are ready for job

Now that my required resources are ready, I'll run my MPI job. In this example, I'm running a program named LAMMPS:

[gc563@amarel1 ~]$ module load intel/17.0.4 mvapich2/2.2

[gc563@amarel1 ~]$ srun --mpi=pmi2 lammps < in.binary

At this point, my interactive job is using my shell (my command prompt is "busy"), so in another shell session I can check on the status of my job and I can see where it's running:

[gc563@amarel2 ~]$ squeue -u gc563

             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)

          37794854      main     bash    gc563  R       1:16      1 hal0048

I'll SSH to that node to verify that my 4 MPI tasks are running there:

[gc563@amarel2 ~]$ ssh hal0048

[gc563@hal0048 ~]$ top -u gc563

top - 14:51:02 up 46 days, 10 min,  1 user,  load average: 5.18, 3.64, 3.48

Tasks: 355 total,   6 running, 349 sleeping,   0 stopped,   0 zombie

%Cpu(s): 23.5 us,  2.0 sy,  0.0 ni, 74.6 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st

KiB Mem : 13131539+total, 11034886+free,  7840860 used, 13125664 buff/cache

KiB Swap:        0 total,        0 free,        0 used. 12027017+avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND              

17716 gc563     20   0  198444  21560  13960 R 100.0  0.0   0:44.27 lammps      

17718 gc563     20   0  197628  20792  13764 R 100.0  0.0   0:44.31 lammps      

17719 gc563     20   0  197628  20956  13932 R 100.0  0.0   0:44.31 lammps      

17717 gc563     20   0  197628  20796  13768 R  93.8  0.0   0:44.31 lammps

Yes, I see 4 instances of my LAMMPS exe running there and each is running at about 100% CPU (each of the 4 CPU cores I've requested are being used efficiently). I'm finished here, so I'll exit this shell session.

Switching back to the shell session where my job is running, when the job is finished, the command prompt will return:

[gc563@amarel1 ~]$

Output from LAMMPS may not be printed to stdout (to my shell) until the job is complete.  

Job array example
A job array is an approach to handle multiple jobs (serial or parallel jobs) with a single job script. Here's an example of submitting 300 jobs:

#!/bin/bash

#SBATCH --partition=main

#SBATCH --job-name=SM-ARR

#SBATCH --array=1-300

#SBATCH --cpus-per-task=4

#SBATCH --mem=1G

#SBATCH --time=00:20:00

module purge

module load intel/19.0.3

mkdir -p $HOME/$SLURM_JOB_ID/$SLURM_ARRAY_TASK_ID

cd $HOME/$SLURM_JOB_ID/$SLURM_ARRAY_TASK_ID

echo "Get a random number from the system:"

export sysrand=$(echo $RANDOM)

echo $sysrand

echo "Running my 4-core OpenMP job:"

srun ./zipper_omp < $SLURM_ARRAY_TASK_ID.input > $SLURM_ARRAY_TASK_ID.output

Understanding this job script:

The --array=1-300 option specifies that 300 instances of this job should be run. As many instances as possible will be launched whenever the requested hardware is available. This process will continue until all 300 instances have been completed.

Each array element (each "job") will have the same hardware and each will have its own 20 minutes of run time, regardless of when it starts.

I'm using the $SLURM_ARRAY_TASK_ID variable to represent each array element (each "job"), so I'm expecting to have input files numbered like 1.input, 2.input, 3.input, ... , 300.input. Correspondingly numbered output files will be created. 

The "%" character can be used to limit the number of jobs in the queue at a time. For example, the following line would send a maximum of 20 jobs to the queue at a time:

#SBATCH --array=1-300%20

Some helpful tips
How many CPU cores should I request? If the application or code you're running in your job has been developed specifically to run in parallel, test basic parallel execution with just 2 or 4 cores. Compare the performance you see with running on just 1 core. If that works and your job is indeed speeding up with multiple cores and the available cores are being used efficiently, run a few benchmarks to see how well your application or code scales (e.g., run the same test job with 2, 4, 8, 16 cores and compare the performance).

How much memory (RAM) should I request? This can be hard to predict and memory utilization can vary as a job proceeds. Some small-scale testing is the best way to start finding the answer. Run a small example job with the default of 4 GB/core to see if that's enough. You may find that's way more memory than you actually need or it might be clear that your job is using all of that memory. Adding this line,

sacct --units=G --format=MaxRSS,MaxDiskRead,MaxDiskWrite,Elapsed,NodeList -j $SLURM_JOBID

to the end of your job script (after all calculations/operations are complete) will capture the peak RAM usage and some other useful info about your job. You can use that info to plan what resources to request for the next job like that one.

Monitoring job status
Actively running jobs
The simplest way to quickly check on the status of active jobs is by using the squeue command:

$ squeue -u <NetID>

  JOBID PARTITION     NAME     USER  ST       TIME  NODES NODELIST(REASON)

1633383      main   zipper    xx345   R       1:15      1 slepner36

Here, the state of each job is typically listed as being either PD (pending), R (running), along with the amount of allocated time that has been used (DD-HH:MM:SS).

For current status details, you can use the sstat command and query specific information:

$ sstat --format=MaxRSS,MaxDiskRead,MaxDiskWrite -j <Job ID>

    MaxRSS  MaxDiskRead MaxDiskWrite 

---------- ------------ ------------ 

    20148K       246863    191234108 

For complete and detailed job info, you can use the scontrol show job <Job ID> command:

scontrol show job 244348

JobId=244348 JobName=XIoT22

   UserId=gc563(148267) GroupId=gc563(148267) MCS_label=N/A

   Priority=5050 Nice=0 Account=oarc QOS=normal

   JobState=RUNNING Reason=None Dependency=(null)

   Requeue=1 Restarts=0 BatchFlag=1 Reboot=0 ExitCode=0:0

   RunTime=1-04:07:40 TimeLimit=2-00:00:00 TimeMin=N/A

   SubmitTime=2020-05-14T07:47:19 EligibleTime=2020-05-14T07:47:19

   StartTime=2020-05-14T07:47:21 EndTime=2020-05-16T07:47:21 Deadline=N/A

   PreemptTime=None SuspendTime=None SecsPreSuspend=0

   Partition=main AllocNode:Sid=amarel1:22391

   ReqNodeList=(null) ExcNodeList=(null)

   NodeList=hal0053

   BatchHost=hal0053

   NumNodes=1 NumCPUs=28 NumTasks=28 CPUs/Task=1 ReqB:S:C:T=0:0:*:*

   TRES=cpu=28,mem=124000M,node=1

   Socks/Node=* NtasksPerN:B:S:C=0:0:*:* CoreSpec=*

   MinCPUsNode=1 MinMemoryNode=124000M MinTmpDiskNode=0

   Features=(null) Gres=(null) Reservation=(null)

   OverSubscribe=OK Contiguous=0 Licenses=(null) Network=(null)

   Command=/scratch/gc563/run.STMV.CPU.slurm

   WorkDir=/scratch/gc563

   StdErr=/scratch/gc563/slurm.%N.244348.out

   StdIn=/dev/null

   StdOut=/scratch/gc563/slurm.%N.244348.out

Completed or terminated jobs
If your jobs have already completed, or have been terminated, you can see details about those jobs using the sacct command. General summary accounting information, including jobs that have recently completed, you can use the sacct command:

$ sacct

JobID        JobName    Partition  Account    AllocCPUS  State      ExitCode

------------ ---------- ---------- ---------- ---------- ---------- --------

63059           archdev               general          1     FAILED    127:0 

63109            ubsing       main    general          1  COMPLETED      0:0 

63109.batch       batch               general          1  COMPLETED      0:0

63153         sys/dashb       main    general          1  CANCELLED      0:0 

63177            extern               general          1  COMPLETED      0:0 

Here, the state of each job is listed as being either PENDING, RUNNING, COMPLETED, or FAILED.

The sacct command can also be used to query detailed information about jobs from within a specific time frame:

sacct --user=<NetID> --starttime=2020-07-03 --endtime=2020-07-13 --format=JobID,Partition,JobName,MaxRSS,NodeList,Elapsed,MaxDiskRead,MaxDiskWrite,State

Cancelling jobs
To cancel, terminate, or kill a job, regardless of whether it is running or just waiting in the job queue, use the scancel command and specify the JobID number of the job you wish to terminate:

scancel 1633383

A job can only be cancelled by the owner of that job. When you terminate a job, a message from the SLURM workload manager will be directed to STDERR and that message will look like this:

slurmstepd: *** JOB 1633383 ON slepner036 CANCELLED AT 2020-05-04T15:38:07 ***

Connecting your lab's systems to Amarel
Many labs have equipment, websites, or other systems that interface directly with the Amarel cluster across the campus network. Typical examples include :

A public-facing website or repository for sharing data with non-Rutgers collaborators or with the general public (note: the Amarel cluster does not have website-hosting capabilities and it is not publicly accessible)

A database management system (DBMS, like MySQL or PostgreSQL) whose tables are populated by data obtained from calculations

A job-spawning workload manager or integrated development environment (IDE)

A visualization system that compiles data from calculations run on Amarel

A geospatial information system (GIS) that compiles data from calculations run on Amarel

For all of these use cases, individual users must manage access to Amarel for their lab's systems. Passwordless access for an application that does a lot of transferring to and from Amarel is common. This involves the use of SSH keys or using a SSHFS client (as described above). When using either approach, SSH keys must be setup and used in accordance with OARC and University policies and they cannot be shared among multiple users (i.e., each user must connect to the Amarel cluster separately).

Checking storage utilization
When you run out of available storage space in /home, /scratch, or /projects, that directory becomes unusable and files must be deleted or moved before you will be able to use that space again.

All Amarel users can use the mmlsquota command to display information about quota limits and current usage for any user, group, or file set. Note: all /home directories are part of the "cache" filesystem, so checking your storage utilization in the "cache" filesystem is equivalent to checking your /home storage utilization.

Checking storage utilization in my /home directory: 

[gc563@amarel1 ~]$ mmlsquota --block-size=auto cache

                         Block Limits                                    |     File Limits

Filesystem type         blocks      quota      limit   in_doubt    grace |    files   quota    limit in_doubt    grace  Remarks

cache      USR          78.18G       100G       110G     561.5M     none |   586773       0        0      239     none DSSP.amarel

I'm using 78.18 GB in my /home directory and I have a quota of 100 GB, so I have only about 21 GB of space remaining to use.

Checking storage utilization in my /scratch directory: 

[gc563@amarel1 ~]$ mmlsquota --block-size=auto scratch

                         Block Limits                                    |     File Limits

Filesystem type         blocks      quota      limit   in_doubt    grace |    files   quota    limit in_doubt    grace  Remarks

scratch    USR          201.6G         1T         2T          0     none |     4729       0        0        0     none redgene.local

I'm using 201.6 GB in my /scratch directory and I have a quota of 1 TB, so I have about 800 GB of space remaining to use. Of course, files in my /scratch directory will be automatically purged if they are not modified or used in 90 days.

To check on utilization for a /projects directory, I must specify the project fileset (using -j) and its location (Camden, Newark, or Piscataway) with projectsc, projectsn, or projectsp:

[gc563@amarel1 ~]$ mmlsquota -j f_bubba_1 --block-size=auto projectsp

                         Block Limits                                    |     File Limits

Filesystem type         blocks      quota      limit   in_doubt    grace |    files   quota    limit in_doubt    grace  Remarks

projects   FILESET      7.145T        10T        10T          0     none |   153237       0        0        0     none DSSP.amarel

The "bubba" research group has a /projects directory at /projects/f_bubba_1 with a 10 TB quota and their storage resides in Piscataway, so I'm querying in projectsp storage system. We're currently using 7.145 TB of that space, so we have about 2.8 GB of space remaining.

Snapshots of /home and /projects data
As we mentioned earlier in the storage section, files stored in the /home and /projects file sets protected against loss using snapshots. Snapshots are not full backups but snapshots do ensure that you can access files that may become damaged or that you accidentally delete. A snapshot includes pointers to unchanged blocks ("chunks" of storage space) and copies of blocks that were subsequently changed. For Amarel, we use a copy-on-write approach to snapshotting: when an I/O request is going to change a block, that block is copied and retained by the snapshot stored separately from the original block. Handling snapshots that way keeps everything consistent for that snapshot and helps us utilize storage space efficiently. Snapshots of the /home and /projects file sets are captured weekly and retained for up to 4 weeks.

If you have damaged or deleted a file in your /home directory, you can look in the recently created snapshots to see if the lost file is available there. Those snapshots are stored in /cache/.snapshots and within a dated cache.<snapshot-date> directory:

[gc563@amarel2 ~]$ ls -l /cache/.snapshots/

drwxr-xr-x 7 root root 4096 May 22 19:35 cache.2020-06-27

drwxr-xr-x 7 root root 4096 May 22 19:35 cache.2020-06-30

drwxr-xr-x 7 root root 4096 May 22 19:35 cache.2020-07-07

drwxr-xr-x 7 root root 4096 May 22 19:35 cache.2020-07-14

Inside each of those dated cache.<snapshot-date> directories, you'll find a snapshot of your /home directory corresponding to the date used in that directory's name. So, a snapshot of your /home directory from 2020-06-30 can be found in /cache/.snapshots/cache.2020-06-30/home/<NetID> and you can simply copy files from that directory back to your current, active /home directory to restore them.

NOTE: If you navigate to /cache/.snapshots/<cache.YYYY-MM-DD>/projects and descend to a projects directory via the symbolic links there, you will be looking at the current production /projects filesystem and not a snapshot because that directory contains symlinks to the current production /projects directories. See below for accessing snapshots of the /projects directories:

Snapshots of the /projects directories are stored on the same campus where a given /projects directory resides. For example, if my /projects directory resides in Camden (within the /projectsc directory), then I can find snapshots for that directory in /projectsc/.snapshots and within a dated projects.<snapshot-date> directory:

[gc563@amarel2 ~]$ ls -l /projectsc/.snapshots/

drwxr-xr-x 10 root root 4096 May 19 16:50 projects.2020-06-23

drwxr-xr-x 10 root root 4096 May 19 16:50 projects.2020-06-30

drwxr-xr-x 10 root root 4096 May 19 16:50 projects.2020-07-07

drwxr-xr-x 10 root root 4096 May 19 16:50 projects.2020-07-14

Likewise, there are snapshots in /projectsn/.snapshots for /projects storage residing in Newark and /projectsp/.snapshots for /projects storage residing in Piscataway.

FAQ
Is the library or utility I need available as part of the OS on Amarel?
Here's an example:  Let's say I'm looking for the Libxml2 library (Libxml2 is the XML C parser and toolkit) which is needed for installing some software I want to use.

Is it installed? Yes.
[gc563@amarel2 ~]$ rpm -qa | grep xml2

libxml2-devel-2.9.1-6.el7.5.x86_64

libxml2-2.9.1-6.el7.5.x86_64

libxml2-python-2.9.1-6.el7.5.x86_64

Where is it located?  In the /lib64 directory.

[gc563@amarel2 ~]$ ldconfig -p | grep xml2

libxml2.so.2 (libc6,x86-64) => /lib64/libxml2.so.2

libxml2.so (libc6,x86-64) => /lib64/libxml2.so



I think there's a maintenance period approaching soon. How can I see the dates and exact start/end times for the next maintenance period?

There must be a maintenance reservation in place, so let's examine that. It probably has the word "maintenance" in some form in the name, but the M could be capitalized, so I'll just search for "aint"

[gc563@amarel2 ~]$ scontrol show res | grep aint

ReservationName=202105-Maint StartTime=2021-05-18T08:00:00 EndTime=2021-05-19T19:00:00 Duration=1-11:00:00

ReservationName=202106-Maint StartTime=2021-06-15T08:00:00 EndTime=2021-06-16T19:00:00 Duration=1-11:00:00



There's a maintenance window approaching soon and I'd like to run a job before the maintenance begins. How can I see how much time I have to run a job?

Here's a way to address that question:

There must be a maintenance reservation in place, so let's examine that. It probably has the word "maintenance" in some form in the name, but the M could be capitalized, so I'll just search for "aint"

[gc563@amarel2 ~]$ scontrol show res | grep aint

ReservationName=202105-Maint StartTime=2021-05-18T08:00:00 EndTime=2021-05-19T19:00:00 Duration=1-11:00:00

ReservationName=202106-Maint StartTime=2021-06-15T08:00:00 EndTime=2021-06-16T19:00:00 Duration=1-11:00:00

Okay, there's the maintenance reservation for 2021-05-18, let's look at the details:

[gc563@amarel2 ~]$ scontrol show res 202105-Maint

ReservationName=202105-Maint StartTime=2021-05-18T08:00:00 EndTime=2021-05-19T19:00:00 Duration=1-11:00:00

   Nodes=cuda[001-008],gpu[001-016],gpuc[001-002],hal[0001-0238],halc[001-067],mem[001-005],memnode001,pascal[001-010],sirius3,slepner[009-048,054-088],volta[001-003] NodeCnt=426 CoreCnt=13964 Features=(null) PartitionName=(null) Flags=MAINT,SPEC_NODES,ALL_NODES

   TRES=cpu=13964

   Users=(null) Accounts=oarc Licenses=(null) State=INACTIVE BurstBuffer=(null) Watts=n/a

Looks like the maintenance window starts at 8am on the 18th. What time is it now?

[gc563@amarel2 ~]$ date

Mon May 17 09:52:44 EDT 2021

So, I could run a job for about 22 hours if I start it now:

[gc563@amarel2 ~]$ srun --time=22:00:00 hostname

slepner014.amarel.rutgers.edu

Yes, that works. As we get closer to the start of the maintenance reservation, that available run time will keep getting shorter, but if I can keep my overall run time within the hours before maintenance begins, I can still get some jobs completed.

