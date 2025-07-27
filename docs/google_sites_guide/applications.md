
Cluster User Guide	
AmarelCaliburn
Applications Guide
Alphafold 3
Submission script explanation
Alphafold 2 (with Multimers)
Submission scripts
Conda
Anaconda
Miniconda
MATLAB
Running in parallel (CPU cores only)
Running on GPUs
Using the Parallel Server
MOE
Python
Quickstart
Using pre-installed Python modules
Building your own Python installation
Q-Chem
R
Running R in an interactive session:
Running R in a batch job (using a job script):
Using packages from BioConductor
Example: Calculate gene length
Installing your own build of R
RStudio
Sage
Singularity
Converting to a Singularity image
Building new Singularity images
Using Singularity containers inside a SLURM job
TensorFlow with a GPU
TensorFlow with a GPU using Singularity
Alphafold 3
AlphaFold 3 differs from earlier releases in that it primarily uses a JSON input file (fold_input.json) to specify the sequences (and, if desired, advanced parameters or special configurations). The script run_alphafold.py in AlphaFold 3 reads this JSON file to produce protein structure predictions.

NB: Example submission script and input files can be found in the Amarel path /projects/community/alphafold/vs3.0.0/pgarias/examples.

Submission script explanation
An example submission script is provided below for use with Alphafold 3 on Amarel:

SLURM flags can be modified according to the suitable resource requirements (--time, --mem, etc.)

Below is an explanation of the SLURM directives  in the submission script:



#SBATCH --partition=gpu                    # Partition name 

#SBATCH --job-name=job_name                # Your alphafold3 job name

#SBATCH --gres=gpu:1                       # Number of gpus needed, keep at 1

#SBATCH --ntasks=1                         # Number of tasks, keep at 1

#SBATCH --cpus-per-task=1                  # Number of gpus needed, keep at 1     

#SBATCH --mem=100G                         # This may need to change based on the number of tokens

#SBATCH --time=03:00:00                    # This may need to change according to the requirements of the job

#SBATCH --constraint=ampere|adalovelace.   # This is needed due to the GPU architecture that alphafold3 has been tested on


You will need to also load modules:

module purge 

module use /projects/community/modulefiles

module load apptainer/1.2.5

module load alphafold/vs3.0.0-pgarias

The Alphafold 3 environments ($ALPHAFOLD_MODELWEIGHTS, $ALPHAFOLD_DATA_PATH, $CONTAINERDIR ) are loaded with the alphafold module. An execution of the singularity image is then added to the script:



apptainer exec \ 

   -B ./af_input:/root/af_input \

   -B ./af_output:/root/af_output \

   -B $ALPHAFOLD_MODELWEIGHTS:/root/models \

   -B $ALPHAFOLD_DATA_PATH:/root/public_databases \

   --pwd /app/alphafold \

   --nv $CONTAINERDIR/alphafold3.sif \

   python run_alphafold.py \

   --json_path=/root/af_input/fold_input.json \

   --db_dir=/root/public_databases \

   --model_dir=/root/models \

   --output_dir=/root/af_output

you will need to create the following directories at the same level as the submission script:

Input Directory: Contains your fold_input.json file (and any additional support files, if needed). For example:

./af_input/fold_input.json

Output Directory: This will store generated prediction files, logs, and model outputs. For example:

./af_output/

Submission script example



#!/bin/bash

#SBATCH --partition=gpu              # Partition (job queue)

#SBATCH --requeue                    # Return job to the queue if preempted

#SBATCH --job-name=my_alphafold3     # Job name

#SBATCH --nodes=1                    # Number of nodes

#SBATCH --ntasks=1                   # Total # of tasks

#SBATCH --cpus-per-task=1            # Cores per task

#SBATCH --gres=gpu:1                 # Number of GPUs

#SBATCH --mem=100G                   # Amount of system RAM

#SBATCH --constraint=ampere|adalovelace

#SBATCH --time=24:00:00              # Max run time (HH:MM:SS)

#SBATCH --output=slurm.%N.%j.out     # STDOUT file

#SBATCH --error=slurm.%N.%j.err      # STDERR file

#SBATCH --export=ALL                 # Export current env to job



module purge

module use /projects/community/modulefiles

module load apptainer/1.2.5

module load alphafold/vs3.0.0-pgarias



# Run AlphaFold 3 inside Apptainer

apptainer exec \

    -B ./af_input:/root/af_input \

    -B ./af_output:/root/af_output \

    -B $ALPHAFOLD_MODELWEIGHTS:/root/models \

    -B $ALPHAFOLD_DATA_PATH:/root/public_databases \

    --pwd /app/alphafold \

    --nv $CONTAINERDIR/alphafold3.sif \

    python run_alphafold.py \

        --json_path=/root/af_input/fold_input.json \

        --db_dir=/root/public_databases \

        --model_dir=/root/models \

        --output_dir=/root/af_output


JSON File

AlphaFold 3 uses a JSON file to define sequences or advanced parameters. Below is a minimal example (from AF3 repo), though your use case may vary:



{

  "job_name": "MyProtein",

  "sequences": [

    {

      "description": "Example protein",

      "sequence": "YOUR_PROTEIN_SEQUENCE_HERE"

    }

  ],

  "num_recycles": 3

}

where:


job_name: Optional descriptive name for the run.

sequences: List of sequences; each can include a description and the raw sequence.

num_recycles: Example of an additional parameter. 


For a full list of available parameters, see the AlphaFold 3  input docs.

Multiple sequences JSON file

Below is an explanation of how to organize multiple protein sequences into a single AlphaFold 3 JSON input file (e.g., fold_input.json).



{

  "name": "Tyrosine-protein phosphatase",

  "sequences": [

    {

      "protein": {

        "id": "A",

        "sequence": "MVDATRVPMDERFRTLKKKLEEGMVFTEYEQIPKKKANGIFSTAALPENAERSRIREVVPYEENRVELIPTKENNTGYINASHIKVVVGGAEWHYIATQGPLPHTCHDFWQMVWEQGVNVIAMVTAEEEGGRTKSHRYWPKLGSKHSSATYGKFKVTTKFRTDSVCYATTGLKVKHLLSGQERTVWHLQYTDWPDHGCPEDVQGFLSYLEEIQSVRRHTNSMLEGTKNRHPPIVVHCSAGVGRTGVLILSELMIYCLEHNEKVEVPMMLRLLREQRMFMIQTIAQYKFVYQVLIQFLQNSRLI"

      }

    },

    {

      "protein": {

        "id": "B",

        "sequence": "GHMAEPQRHTMLCMCCKCEARIELVVESSADDLRAFQQLFLNTLSFVCPWCASQQ"

      }

    }

  ],

  "modelSeeds": [1,2],

  "dialect": "alphafold3",

  "version": 1

}


Alphafold 2 (with Multimers)
A recent update of Alphafold 2.0 allows for predictions of multimer and monomer inputs. In addition, this version can also predict monomers (as well as multimers) with full_dbs  or reduced_dbs.

Submission scripts
An example submission script is provided below. For all 4 cases, the user needs to modify the following flags:

--max_template_date=YYYY-MM-DD 

--fasta_paths=<FASTA FILE PATH> 

--output_dir=<OUTPUT FILE DIRECTORY PATH> 

For further explanations and additional options please see run_alphafold.py.

SLURM flags can be modified according to the suitable resource requirements (--gres=gpu:#, --nodes, --ntasks,--time, --mem, etc.)

Below is the explanation of the singularity flags in the submission script.

The database and models are stored in $ALPHAFOLD_DATA_PATH and loaded when you run module load alphafold after you load module use /projects/community/modulefiles.

A cache file ld.so.cache will be written to /etc, which is not allowed on Amarel. The workaround is to bind-mount e.g. the current working directory to /etc inside the container. [-B .:/etc]

You must launch AlphaFold from /app/alphafold inside the container due to this issue. [--pwd /app/alphafold]

The --nv flag enables GPU support.

Alphafold multimer, reduced database (reduced_dbs):

#!/bin/bash



#SBATCH --partition=gpu              # Partition (job queue)

#SBATCH --requeue                    # Return job to the queue if preempted

#SBATCH --job-name=alphafold         # Assign an short name to your job

#SBATCH --nodes=1                    # Number of nodes you require

#SBATCH --ntasks=8                   # Total # of tasks across all nodes

#SBATCH --cpus-per-task=1            # Cores per task (>1 if multithread tasks)

#SBATCH --gres=gpu:1                 # Number of GPUs

#SBATCH --mem=64G                    # Real memory (RAM) required (MB), 0 is the whole-node memory

#SBATCH --time=03:00:00              # Total run time limit (HH:MM:SS)

#SBATCH --output=slurm.%N.%j.out     # STDOUT output file

#SBATCH --error=slurm.%N.%j.err      # STDERR output file (optional)

#SBATCH --export=ALL                 # Export you current env to the job env



module purge

module use /projects/community/modulefiles

module load singularity/3.6.4

module load alphafold



singularity run -B $ALPHAFOLD_DATA_PATH:/data -B .:/etc --pwd /app/alphafold --nv $CONTAINERDIR/alphafold.sif \

    --data_dir=/data \

    --uniref90_database_path=/data/uniref90/uniref90.fasta \

    --mgnify_database_path=/data/mgnify/mgy_clusters_2018_12.fa \

    --template_mmcif_dir=/data/pdb_mmcif/mmcif_files/ \

    --obsolete_pdbs_path=/data/pdb_mmcif/obsolete.dat \

    --fasta_paths=<FASTA FILE PATH> \

    --output_dir=<OUTPUT FILE DIRECTORY PATH> \

    --model_preset=multimer \

    --db_preset=reduced_dbs \

    --small_bfd_database_path=/data/small_bfd/bfd-first_non_consensus_sequences.fasta \

    --pdb_seqres_database_path=/data/pdb_seqres/pdb_seqres.txt \

    --uniprot_database_path=/data/uniprot/uniprot.fasta \

    --max_template_date=YYYY-MM-DD \

    --use_gpu_relax=True








Alphafold monomer, reduced database (reduced_dbs):

#!/bin/bash



#SBATCH --partition=gpu              # Partition (job queue)

#SBATCH --requeue                    # Return job to the queue if preempted

#SBATCH --job-name=alphafold         # Assign an short name to your job

#SBATCH --nodes=1                    # Number of nodes you require

#SBATCH --ntasks=8                   # Total # of tasks across all nodes

#SBATCH --cpus-per-task=1            # Cores per task (>1 if multithread tasks)

#SBATCH --gres=gpu:1                 # Number of GPUs

#SBATCH --mem=64G                    # Real memory (RAM) required (MB), 0 is the whole-node memory

#SBATCH --time=03:00:00              # Total run time limit (HH:MM:SS)

#SBATCH --output=slurm.%N.%j.out     # STDOUT output file

#SBATCH --error=slurm.%N.%j.err      # STDERR output file (optional)

#SBATCH --export=ALL                 # Export you current env to the job env



module purge

module use /projects/community/modulefiles

module load singularity/3.6.4

module load alphafold



singularity run -B $ALPHAFOLD_DATA_PATH:/data -B .:/etc --pwd /app/alphafold --nv $CONTAINERDIR/alphafold.sif \

    --data_dir=/data \

    --uniref90_database_path=/data/uniref90/uniref90.fasta \

    --mgnify_database_path=/data/mgnify/mgy_clusters_2018_12.fa \

    --template_mmcif_dir=/data/pdb_mmcif/mmcif_files/ \

    --obsolete_pdbs_path=/data/pdb_mmcif/obsolete.dat \

    --fasta_paths=<FASTA FILE PATH> \

    --output_dir=<OUTPUT FILE DIRECTORY PATH> \

    --model_preset=monomer \

    --db_preset=reduced_dbs \

    --small_bfd_database_path=/data/small_bfd/bfd-first_non_consensus_sequences.fasta \

    --pdb70_database_path=/data/pdb70/pdb70 \

    --max_template_date=YYYY-MM-DD \

    --use_gpu_relax=True






Alphafold multimer, full database (full_dbs):

#!/bin/bash



#SBATCH --partition=gpu              # Partition (job queue)

#SBATCH --requeue                    # Return job to the queue if preempted

#SBATCH --job-name=alphafold         # Assign an short name to your job

#SBATCH --nodes=1                    # Number of nodes you require

#SBATCH --ntasks=8                   # Total # of tasks across all nodes

#SBATCH --cpus-per-task=1            # Cores per task (>1 if multithread tasks)

#SBATCH --gres=gpu:1                 # Number of GPUs

#SBATCH --mem=64G                    # Real memory (RAM) required (MB), 0 is the whole-node memory

#SBATCH --time=03:00:00              # Total run time limit (HH:MM:SS)

#SBATCH --output=slurm.%N.%j.out     # STDOUT output file

#SBATCH --error=slurm.%N.%j.err      # STDERR output file (optional)

#SBATCH --export=ALL                 # Export you current env to the job env



module purge

module use /projects/community/modulefiles

module load singularity/3.6.4

module load alphafold



singularity run -B $ALPHAFOLD_DATA_PATH:/data -B .:/etc --pwd /app/alphafold --nv $CONTAINERDIR/alphafold.sif \

    --data_dir=/data \

    --uniref90_database_path=/data/uniref90/uniref90.fasta \

    --mgnify_database_path=/data/mgnify/mgy_clusters_2018_12.fa \

    --template_mmcif_dir=/data/pdb_mmcif/mmcif_files/ \

    --obsolete_pdbs_path=/data/pdb_mmcif/obsolete.dat \

    --fasta_paths=/scratch/pgarias/fastafiles/A2B2heterodimer.fasta \

    --output_dir=/scratch/pgarias/outputdir_mm/full_dbs_multimer \

    --model_preset=multimer \

    --db_preset=full_dbs \

    --bfd_database_path=/data/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \

    --pdb_seqres_database_path=/data/pdb_seqres/pdb_seqres.txt \

    --uniprot_database_path=/data/uniprot/uniprot.fasta \

    --uniclust30_database_path=/data/uniclust30/uniclust30_2018_08/uniclust30_2018_08 \

    --max_template_date=YYYY-MM-DD \

    --use_gpu_relax=True




Alphafold monomer, full database (full_dbs):

#!/bin/bash



#SBATCH --partition=gpu              # Partition (job queue)

#SBATCH --requeue                    # Return job to the queue if preempted

#SBATCH --job-name=alphafold         # Assign an short name to your job

#SBATCH --nodes=1                    # Number of nodes you require

#SBATCH --ntasks=8                   # Total # of tasks across all nodes

#SBATCH --cpus-per-task=1            # Cores per task (>1 if multithread tasks)

#SBATCH --gres=gpu:1                 # Number of GPUs

#SBATCH --mem=64G                    # Real memory (RAM) required (MB), 0 is the whole-node memory

#SBATCH --time=03:00:00              # Total run time limit (HH:MM:SS)

#SBATCH --output=slurm.%N.%j.out     # STDOUT output file

#SBATCH --error=slurm.%N.%j.err      # STDERR output file (optional)

#SBATCH --export=ALL                 # Export you current env to the job env



module purge

module use /projects/community/modulefiles

module load singularity/3.6.4

module load alphafold



singularity run -B $ALPHAFOLD_DATA_PATH:/data -B .:/etc --pwd /app/alphafold --nv $CONTAINERDIR/alphafold.sif \

    --data_dir=/data \

    --uniref90_database_path=/data/uniref90/uniref90.fasta \

    --mgnify_database_path=/data/mgnify/mgy_clusters_2018_12.fa \

    --template_mmcif_dir=/data/pdb_mmcif/mmcif_files/ \

    --obsolete_pdbs_path=/data/pdb_mmcif/obsolete.dat \

    --fasta_paths=/scratch/pgarias/fastafiles/sarscovid2.fasta \

    --output_dir=/scratch/pgarias/outputdir_mm/full_dbs_monomer \

    --model_preset=monomer \

    --db_preset=full_dbs \

    --bfd_database_path=/data/bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt \

    --pdb70_database_path=/data/pdb70/pdb70 \

    --uniclust30_database_path=/data/uniclust30/uniclust30_2018_08/uniclust30_2018_08 \

    --max_template_date=YYYY-MM-DD \

    --use_gpu_relax=True






Conda
Conda is an open-source, cross-platform, language-agnostic package manager and environment management system. Conda packages are binaries. No compilers needed to install them.  It consists of the following components

Anaconda is a Conda package repository that includes many python packages and extensions, such as Conda, numpy, scipy, ipython notebook, etc..

Miniconda is a smaller alternative to Anaconda that includes a much smaller set of core packages along with Conda.

While Conda packages are binary distribution allowing fast installation, other forms of installation are supported inside Conda environments, including pip, or any other source installation.  Each package installs along with a list of dependent packages by default.

Anaconda
You can either install your own version of Anaconda in your home directory, or you can use a version from the community-contributed modules. Here's how to search for packages with 'anaconda' in their description:

module use /projects/community/modulefiles

module keyword anaconda

  anaconda: anaconda/2020.07-gc563

    Sets up Anaconda 2020.07 for your environment



  py-data-science-stack: py-data-science-stack/5.1.0-kp807

    Sets up anaconda 5.1.0 in your environment



  py-image: py-image/2020-bd387

    Sets up anaconda in your environment for tensorflow and keras

To use the above anaconda (2020.07)  module and set up conda environment :

$ module use /projects/community/modulefiles/

$ module load anaconda/2020.07-gc563

$ conda init bash   ##configure your bash shell for conda, auto update your .bashrc file

$ cd

$ source .bashrc

$ mkdir -p .conda/pkgs/cache .conda/envs   ##These are the folders to store your own env you going to build

 To see env already installed in the module:    (you'll see  tensorflow-2.3.0,  pytorch-1.7.0 are installed,  you may activate it and use it)

conda env list

 To install your own anaconda env, for example, your own TensorFlow version 2.3, with python 3.8,  name this env  as "tf2":

conda create --name tf2  tensorflow==2.3 python=3.8

This env will be located at:   /home/<netID>/.conda/envs/tf2

# To activate your  above TensorFlow  environment:

$ conda activate tf2

#  After you are done with the work in that environment,  you shall deactivate it, by:

$ conda deactivate

Miniconda
There is a copy of miniconda installed in the community folder: /projects/community/miniconda3/condabin/conda    

The first time using it, you need to initialize it:

/projects/community/miniconda3/bin/conda init    ##This will set up the conda environment via your .bashrc file

/projects/community/miniconda3/bin/conda config --set auto_activate_base false  ##so it won't automatically activate

source ~/.bashrc    

To create your own environment and save it in your home directory, using the above community miniconda:

$ cd

$ mkdir -p .conda/pkgs/cache .conda/envs       ##These folders will store your env and related files

$ conda create --name mytest python=3.8 numpy  ##create an env called mytest with python 3.8,& numpy

You may check now, your new env "mytest" shall be located at :  /home/<netID>/.conda/envs/mytest

To use the env, you need to activate it:

$conda activate mytest

When you are done, deactivate it:

$conda deactivate

MATLAB
There are a few example MATLAB jobs located here: /projects/oarc/users/examples/matlab

Running in parallel (CPU cores only)
To run just about anything in parallel with MATLAB, you must have MATLAB code that's designed to run in parallel. That's usually accomplished by calling the parpool and parfor functions. Before scaling-up to large numbers of cores, be sure your MATLAB script can efficiently utilize many cores (e.g., run some benchmarking jobs to see how the performance of your calculations scale when increasing the number of cores) because more cores doesn't always mean things will run faster.

Here's an example SLURM job script for running a parallel-enabled MATLAB script across 4 cores (i.e., 4 MATLAB worker processes) on a single compute node:

#!/bin/bash

#SBATCH --job-name=mparfor           # Assign an short name to your job

#SBATCH --cpus-per-task=4            # Cores per task (>1 if multithread tasks)

#SBATCH --mem=16000                  # Real memory (RAM) required (MB)

#SBATCH --time=00:05:00              # Total run time limit (HH:MM:SS)

#SBATCH --output=slurm.%N.%j.out     # STDOUT output file

mkdir -p /scratch/$USER/$SLURM_JOB_ID

cd /scratch/$USER/$SLURM_JOB_ID

module purge

rm -rf ~/.matlab

module load MATLAB/R2020a

srun matlab -nodisplay < MonteCarloPi.m

cd ; rm -rf /scratch/$USER/$SLURM_JOB_ID

Running on GPUs
For MATLAB to take advantage of GPU hardware, the gpuArray function must be used in your MATLAB script.

Here's an example SLURM job script for running a GPU-enabled MATLAB script across 4 cores (i.e., 4 MATLAB worker processes):

#!/bin/bash

#SBATCH --partition=gpu              # Partition (job queue)

#SBATCH --job-name=mtrxmlt           # Assign an short name to your job

#SBATCH --cpus-per-task=1            # Cores per task (>1 if multithread tasks)

#SBATCH --gres=gpu:1                 # Request number of GPUs

#SBATCH --constraint=pascal          # Specify hardware models

#SBATCH --mem=16000                  # Real memory (RAM) required (MB)

#SBATCH --time=00:05:00              # Total run time limit (HH:MM:SS)

#SBATCH --output=slurm.%N.%j.out     # STDOUT output file

mkdir -p /scratch/$USER/$SLURM_JOB_ID

cd /scratch/$USER/$SLURM_JOB_ID

module purge

rm -rf ~/.matlab

module load MATLAB/R2020a

srun matlab -nodisplay -singleCompThread -batch "N=10000;MatrixMultGPU(rand(N),rand(N))"

cd ; rm -rf /scratch/$USER/$SLURM_JOB_ID

Using the Parallel Server
The MATLAB Parallel Server is required for parallel execution across more than 1 compute node. Note: before scaling-up to multiple nodes, be sure your MATLAB script can efficiently utilize cores across multiple nodes (e.g., run some benchmarking jobs to see how the performance of your calculations scale when increasing the number of cores) because more cores doesn't always mean things will run faster.

Documentation for using Parallel Server is available here: https://www.mathworks.com/help/matlab-parallel-server/index.html

There is an example Cluster Configuration for Amarel here: /projects/oarc/users/examples/matlab/Amarel_SLURM_Parallel_Server.mlsettings 

That file can be imported into the Cluster Configuration Manager in MATLAB. When using that example configuration, be sure to edit the JobStorageLocation and the number of workers you wish to use. By default, MATLAB will leave the selection of the number of compute nodes up to SLURM, but you can customize this and many other features of your Parallel Server managed SLURM jobs by adding appropriate options in the SubmitArguments field.

Parallel Server can be utilized exclusively from the command-line (a GUI is not required) and that is the most efficient way to use it. However, if you prefer to use the MATLAB IDE for submitting your job(s), connecting to Amarel using the FastX system and launching MATLAB from a compute node is recommended. Note: the resources you request for running the MATLAB IDE are completely separate from those requested when you submit a job using the Parallel Server. For example, you may only need 1 core and 1 GB RAM for running the MATLAB IDE, regardless of how big your Parallel Server jobs are, because the MATLAB IDE only submits your job when using the Parallel Server, it doesn't actually participate in the computation.

MOE
Molecular Operating Environment (MOE) by Chemical Computing Group (CCG) is a drug discovery platform that integrates visualization, modeling, simulations, and methodology development, in one package.

Download and install:

The MOE installation package for Windows, Linux, or OS X can be downloaded from the Rutgers Software Portal: https://software.rutgers.edu/product/3656

Configure the license file:

Once the installation is complete, edit the license.dat file in the main "moe" directory. For example, on a Windows system, look for the license.dat in C:\moe or C:\Program Files\moe or similar default locations.

When you locate  license.dat file, open it with a text editor (like Notepad) and replace the content with the license details provided on the Rutgers Software Portal.

Save the license.dat file and try to start MOE again.

Remember that running MOE will only work if you are connected to the Rutgers campus network (i.e., actually on campus or connected to the campus network via the Rutgers VPN service).

Python
Generally, there are 2 approaches for using Python and its associated tools:

(1) use one of the pre-installed Python modules (version 2.x.x or 3.x.x) that's already available on Amarel (you can add or update packages if needed) or

(2) install your own custom build of Python in your /home directory or in a shared directory (e.g., /projects/<group> or /projects/community).

Quickstart
Loads the Intel libraries and underlying c/c++/fortran code needed for numpy, then the Python module, itself:

module load intel_mkl/17.0.2 python/3.5.2

Or, load a version of Python, Anaconda, or the Python Data Science Stack:

module use /projects/community/modulefiles

module load py-data-science-stack/5.1.0-kp807

Using pre-installed Python modules
With the pre-installed Python modules, you can add or update Python modules/packages as needed if you do it using the '--user' option for pip. This option will instruct pip to install new software or upgrades in your ~/.local directory. Here's an example where I'm installing the Django package:

module load python/3.5.2

pip install --user Django

Note: if necessary, pip can also be upgraded when using a system-installed build of Python, but be aware that the upgraded version of pip will be installed in ~/.local/bin. Whenever a system-installed Pytyon module is loaded, the PATH location of that module's executables (like pip) will precede your ~/.local/bin directory. To run the upgraded version of pip, you'll need to specify its location because the previous version of pip will no longer work properly:

$ which pip

/opt/sw/packages/gcc-4.8/python/3.5.2/bin/pip

$ pip --version

pip 9.0.3 from /opt/sw/packages/gcc-4.8/python/3.5.2/lib/python3.5/site-packages (python 3.5)

$ pip install -U --user pip

Successfully installed pip-10.0.1

$ which pip

/opt/sw/packages/gcc-4.8/python/3.5.2/bin/pip

$ pip --version

Traceback (most recent call last):

  File "/opt/sw/packages/gcc-4.8/python/3.5.2/bin/pip", line 7, in 

    from pip import main

ImportError: cannot import name 'main'

$ .local/bin/pip --version

pip 10.0.1 from /home/gc563/.local/lib/python3.5/site-packages/pip (python 3.5)

$ .local/bin/pip install --user Django

Building your own Python installation
Using this approach, I must specify that I want Python to be installed in my /home directory. This is done using the '--prefix=' option. Also, I prefer to use a [package]/[version] naming scheme because that enables easy organization of multiple versions of Python (optional, it's just a personal preference).

Note: Newer versions of Python require the Foreign Function Interface library (libffi) to avoid errors about missing _ctypes. You can install your own libffi like this,

wget https://github.com/libffi/libffi/releases/download/v3.4.2/libffi-3.4.2.tar.gz

tar -zxf libffi-3.4.2.tar.gz

cd libffi-3.4.2

./configure --prefix=/home/gc563/libffi/3.4.2

make -j 4

make install

 or you can use the one available in Amarel's Community-Contributed Software Repository:

module use /projects/community/modulefiles/

module load libffi/3.4.2-gc563

With libffi ready in my shell environment, I can proceed with my Python installation.

Note #1:  In the example here, I'm using the libffi available on Amarel, not the one installed in my /home directory (to do that, you must change the path for the LDFLAGS environment variable and you'll need to set the PKG_CONFIG_PATH variable to the lib/pkgconfig directory in your libffi installation.

Note #2:  Using the --enable-optimizations option requires that you build Python with GCC 8.10+ or Intel compilers. I'm just using the system default GCC.

At the end of my install procedure, I remove the downloaded install package and tarball, just to tidy-up.

wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz

tar -zxf Python-3.9.6.tgz

cd Python-3.9.6

./configure --prefix=/home/gc563/python/3.9.6 CXX=g++ --with-ensurepip=install LDFLAGS=-L/projects/community/libffi/3.4.2/gc563/lib64

make -j 8

make install

cd ..

rm -rf Python-3.9.6*

Before using my new Python installation, I'll need to set or edit some environment variables. This can be done from the command line (but the settings won't persist after you log-out) or by adding these commands to the bottom of your ~/.bashrc file (so the settings will persist):

export PATH=/home/gc563/python/3.9.6/bin:$PATH

export LD_LIBRARY_PATH=/home/gc563/python/3.9.6/lib

export MANPATH=/home/gc563/python/3.9.6/share/man

If you're adding these lines to the bottom of your ~/.bashrc file, log-out and log-in again, then verify that the settings are working:

which python3

~/python/3.9.6/bin/python3

Q-Chem
Q-Chem is a comprehensive ab initio quantum chemistry software package that can provide accurate predictions of molecular structures, reactivities, and vibrational, electronic and NMR spectra.

How to load the Q-Chem module:

module load Q-Chem/5.4

Example Q-Chem job:

There is a simple example job in /projects/community/users/training/intro.amarel/qchem.example that runs Q-Chem in parallel using OpenMP (in other words, this parallel job can use the cores on a single compute node, but it cannot span multiple compute nodes. That example includes input for an ADC(2)-s calculation of singlet exited states of methane with D2 symmetry. In total, six excited states are requested corresponding to four (two) electronic transitions with irreducible representation B1 (B2).

sbatch run.qchem.openmp

Notes:

Q-Chem can run in parallel using OpenMP (threaded mode), MPI, or a combination of both (hybrid mode):

OpenMP (threaded):

qchem -nt nthreads infile outfile

MPI (be sure to add --mpi=pmi2 after your srun command):

qchem -np n infile outfile

Hybrid OpenMP+MPI:

qchem -np n -nt nthreads infile outfile

Troubleshooting:

If you encounter a "bus error," you may have run out of memory. In that case, assigning more memory (RAM) for your job may help you avoid that situation.

If you see "License server machine is down or not responding" in your output file, the Q-Chem license server may be busy and simply trying again is appropriate. 

R
Running R in an interactive session:
Here's a simple example of loading and running R in an interactive job. First, start an interactive session with 2 CPU cores that will run for 1 hr 40 min and provide you with a Bash shell on the allocated compute node:

$ srun --ntasks=2 --time=01:40:00 --pty bash

Once your interactive session has started, load the desired R module and launch an R shell:

$ module load intel/17.0.4

$ module load R-Project/3.4.1

$ R

Running R in a batch job (using a job script):
#!/bin/bash

#SBATCH --partition=main             # Partition (job queue)

#SBATCH --no-requeue                 # Do not re-run job  if preempted

#SBATCH --job-name=TF_gpu            # Assign an short name to your job

#SBATCH --nodes=1                    # Number of nodes you require

#SBATCH --ntasks=1                   # Total # of tasks across all nodes

#SBATCH --cpus-per-task=2            # Cores per task (>1 if multithread tasks)

#SBATCH --gres=gpu:1                 # Number of GPUs

#SBATCH --mem=16000                  # Real memory (RAM) required (MB)

#SBATCH --time=00:30:00              # Total run time limit (HH:MM:SS)

#SBATCH --output=slurm.%N.%j.out     # STDOUT output file

#SBATCH --error=slurm.%N.%j.err      # STDERR output file (optional)

module purge

module load singularity/.2.5.1

Rscript myRprogram.r

Using packages from BioConductor
If these packages are not installed, you can install them yourself. On a login node, start R and try the following commands:

source("https://bioconductor.org/biocLite.R") 

biocLite("ape")

biocLite("MKmisc")

biocLite("Heatplus")

biocLite("affycoretools")

biocLite("flashClust")

biocLite("affy")

Example: Calculate gene length
Get some data from ENSEMBLE

wget ftp://ftp.ensembl.org/pub/release-91/gtf/homo_sapiens/Homo_sapiens.GRCh38.91.gtf.gz

In an R shell, you can execute these commands to compute gene lengths:

library(GenomicFeatures)

gtfdb <- makeTxDbFromGFF("Homo_sapiens.GRCh38.78.gtf",format="gtf")

exons.list.per.gene <- exonsBy(gtfdb,by="gene")

exonic.gene.sizes <- lapply(exons.list.per.gene,function(x){sum(width(reduce(x)))})

class(exonic.gene.sizes)

Hg20_geneLength <-do.call(rbind, exonic.gene.sizes)

colnames(Hg20_geneLength) <- paste('geneLength')

Installing your own build of R
Here are the steps some have used to install their own customizable build of R in their /home directory. After the installation of R, the procedures here also show how the Bioconductor package can be installed using the newly-installed build of R. NOTE: be sure to use your NetID instead of the <NetID> placeholder.

Start by downloading and installing PCRE:

wget https://ftp.pcre.org/pub/pcre/pcre2-10.35.tar.gz

tar -zxf pcre2-10.35.tar.gz

cd pcre2-10.35

./configure --prefix=/home/<NetID>/pcre/10.35

make -j 8

make install

Add these lines to the end of your ~/.bashrc file (NOTE: the commands presented here assume you don't already have those environment variables set. If you do have them set already, adjust these lines accordingly):

export PATH=/home/<NetID>/pcre/10.35/bin:$PATH

export C_INCLUDE_PATH=/home/<NetID>/pcre/10.35/include

export CPLUS_INCLUDE_PATH=/home/<NetID>/pcre/10.35/include

export LIBRARY_PATH=/home/<NetID>/pcre/10.35/lib

export LD_LIBRARY_PATH=/home/<NetID>/pcre/10.35/lib

export MANPATH=/home/<NetID>/pcre/10.35/share/man:$MANPATH

Then log-out and log-in again so those settings will take effect.

Next, we can download and install R:

wget https://cran.r-project.org/src/base/R-4/R-4.1.0.tar.gz

tar -zxf R-4.1.0.tar.gz

cd R-4.1.0

./configure --prefix=/home/<NetID>/R/4.1.0

make -j 8

make install

Add these lines to the end of your ~/.bashrc file:

export PATH=/home/<NetID>/R/4.1.0/bin:$PATH

export C_INCLUDE_PATH=/home/<NetID>/R/4.1.0/include:$C_INCLUDE_PATH

export CPLUS_INCLUDE_PATH=/home/<NetID>/R/4.1.0/include:$CPLUS_INCLUDE_PATH

export LIBRARY_PATH=/home/<NetID>/R/4.1.0/lib:$LIBRARY_PATH

export LD_LIBRARY_PATH=/home/<NetID>/R/4.1.0/lib:$LD_LIBRARY_PATH

export MANPATH=/home/<NetID>/R/4.1.0/share/man:$MANPATH

Then log-out and log-in again so those settings will take effect.

Now, we're ready to install additional packages for our new R installation. Here, we'll walk through the process of installing the Bioconductor package.

Start R, then enter these commands:

> if (!requireNamespace("BiocManager", quietly = TRUE))

+     install.packages("BiocManager")

> BiocManager::install()

> BiocManager::install("GenomicFeatures")

This installation can take a long time. You may be asked if you'd like to update the installed packages:

Update all/some/none? [a/s/n]: a
Doing so is probably going to be a good idea for most users.

RStudio
RStudio is available as a pre-built app in Amarel's Open OnDemand interface (see here for details: https://sites.google.com/view/cluster-user-guide/amarel#h.z6biscu53ldl). But some users prefer more flexibility or customizability with their RStudio and underlying R builds. For those users, launching RStudio from a Singularity image (running as a container) may be a good option.


Here's how to run a Singularity image of RStudio on Amarel:
(1) Launch a FastX desktop session (see here for details: https://sites.google.com/view/cluster-user-guide/amarel#h.jsnqsekyy1u6)

Direct your web browser to https://amarel.hpc.rutgers.edu:3443

(2) Access a compute node with the job duration and memory you require and launch a Bash shell:

srun --time=1:00:00 --mem=2G --pty bash

(3) Load a recent version of Singularity (may need to check module --show-hidden avail to find the latest version)

module load singularity/3.6.4

(4) Run our Singularity Image File in /projects/community as a container:

singularity run --app rstudio /projects/community/singularity.images/rstudio/r402rstudio11.sif-gc563



If a newer version of R or RStudio is required, the user can build and customize their own Singularity image as needed using the free, web-based image builder: https://cloud.sylabs.io/builder
An example Singularity definition file for creating a new image can be found here: /projects/community/singularity.images/rstudio/r402rstudio11.def-gc563 (that's the definition file used to build the working image stored in that same directory). The exact commands for building an image with the latest versions of R and RStudio may have changed a bit since this definition file was created: the optimal procedures change all the time. So, a user doing this for themselves may need to do a little research to find the best Docker image or preconfigured OS image with which to start.

Sage
SageMath is a free, open-source mathematics software system licensed under the GPL. It builds on top of many existing open-source packages like NumPy, SciPy, matplotlib, Sympy, Maxima, GAP, FLINT, R and many more. Sage enables access to their combined power through a common, Python-based language or directly via interfaces or wrappers. 

On Amarel, Sage 9.2 can be loaded via the Miniconda3 environment in the Community-Contributed Software Repository.

First, initialize the Miniconda3 environment on Amarel as described here.

(e.g., /projects/community/miniconda3/bin/conda init and then log-out, log-in for that change to take effect)

Then, simply activate the Sage environment within Miniconda3:

conda activate sage

Singularity
Singularity is a Linux containerization tool suitable for HPC environments. It uses its own container format and also has features that enable importing Docker containers.

Docker is a platform that employs features of the Linux kernel to run software in a container. The software housed in a Docker container is not standalone program but an entire OS distribution, or at least enough of the OS to enable the program to work. Docker can be thought of as somewhat like a software distribution mechanism like yum or apt. It also can be thought of as an expanded version of a chroot jail, or a reduced version of a virtual machine.

Important differences between Docker and Singularity:

Docker and Singularity have their own container formats.

Docker containers can be imported and run using Singularity.

Docker containers usually run as root, which means you cannot run Docker on a shared computing system (cluster).

Singularity allows for containers that can be run as a regular user. How? When importing a Docker container, Singularity removes any elements which can only run as root. The resulting containers can be run using a regular user account.

Converting to a Singularity image
You will need to have Singularity installed on your local workstation/laptop to prepare your image. The 'create' and 'import' operations of Singularity require root privileges, which you do not have on Amarel.

Create an empty singularity image, and then import the exported docker image into it,

$ sudo singularity create ubuntu.img

Creating a sparse image with a maximum size of 1024MiB...

Using given image size of 1024

Formatting image (/sbin/mkfs.ext3)

Done. Image can be found at: ubuntu.img

$ sudo singularity import ubuntu.img ubuntu.tar

Building new Singularity images
Singularity 3.0 introduced the ability to build a container in the cloud. When doing this, a Singularity user does not need to prepare an environment or assign permissions. The Remote Builder at https://cloud.sylabs.io/builder can build a container using a provided build definition file and can also be used to edit or develop a definition file, then build the desired image.

Here's an example Singularity 3.5 definition file that tells the Singularity bootstrap agent to pull Ubuntu 18.04 from the Container Library, then it installs basic development tools, Python-3.7, Firefox, R-3.6, and the libraries needed for GUI-based applications:

BootStrap: library

From: ubuntu:18.04

%post

    apt -y update

    apt -y install build-essential

    apt -y install python3.7

    DEBIAN_FRONTEND=noninteractive apt -y install xorg

    apt -y install firefox

    apt -y install apt-transport-https software-properties-common

    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9

    add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/'

    apt -y update

    apt -y install r-recommended=3.6.0-2bionic r-base=3.6.0-2bionic r-base-core=3.6.0-2bionic r-base-dev=3.6.0-2bionic

    apt -y install libpcre2-dev

    apt -y install r-base

Once the image has been successfully built, you can download the image and transfer it to Amarel. 

Using Singularity containers inside a SLURM job
Transfer your new Singularity image to Amarel. The following steps are performed while logged-in to Amarel.

You can run any task/program inside the container by prefacing it with

singularity exec <your image name>

Here is a simple example job script that executes commands inside a container,

#SBATCH --partition=main             # Partition (job queue)

#SBATCH --job-name=sing2me           # Assign an short name to your job

#SBATCH --nodes=1                    # Number of nodes you require

#SBATCH --ntasks=1                   # Total # of tasks across all nodes

#SBATCH --cpus-per-task=1            # Cores per task (>1 if multithread tasks)

#SBATCH --mem=4000                   # Real memory (RAM) required (MB)

#SBATCH --time=00:30:00              # Total run time limit (HH:MM:SS)

#SBATCH --output=slurm.%N.%j.out     # STDOUT output file

module purge

module load singularity/.2.5.1

## Where am I running?

srun singularity exec ubuntu.img hostname

## What is the current time and date?

srun singularity exec ubuntu.img date

If you created directories for any Amarel filesystems, you should find they are mounted inside your container,

mount | grep gpfs

/dev/scratch/gc563 on /scratch/gc563 type gpfs (rw,relatime)

/dev/projects/oarc on /projects/oarc type gpfs (rw,relatime)

NOTE: If your container mounts Amarel directories, software inside the container may be able to destroy data on these filesystems for which you have write permissions. Proceed with caution.

TensorFlow with a GPU
TensorFlow's Python package includes 2 versions: tensorflow and tensorflow-gpu. But the command to use TensorFlow is the same in both cases: import tensorflow as tf (and not import tensorflow-gpu as tf in case of the GPU version). This means that you must be careful about which package is setup in your environment.ou can control your environment using a Singularity image, but that can present a problem if you need a package not included in the prebuilt Singularity image. If you encounter that problem, you likely need to build the image yourself. Alternatively, you can control your environment using Conda environments or virtual-env.

TensorFlow with a GPU using Singularity
To do this, you can use the Singularity container manager and a Docker image containing the TensorFlow software.

Running Singularity can be done in batch mode using a job script. Below is an example job script for this purpose. In this example, we'll name the script TF_gpu.sh:

#!/bin/bash

#SBATCH --partition=main             # Partition (job queue)

#SBATCH --job-name=TF_gpu            # Assign an short name to your job

#SBATCH --nodes=1                    # Number of nodes you require

#SBATCH --ntasks=1                   # Total # of tasks across all nodes

#SBATCH --cpus-per-task=2            # Cores per task (>1 if multithread tasks)

#SBATCH --gres=gpu:1                 # Number of GPUs

#SBATCH --mem=16000                  # Real memory (RAM) required (MB)

#SBATCH --time=00:30:00              # Total run time limit (HH:MM:SS)

#SBATCH --output=slurm.%N.%j.out     # STDOUT output file

#SBATCH --error=slurm.%N.%j.err      # STDERR output file (optional)

module purge

module load singularity/.2.5.1

srun singularity exec --nv docker://tensorflow/tensorflow:1.4.1-gpu python 

Once your job script is ready, submit it using the sbatch command:

$ sbatch TF_gpu.sh

Alternatively, you can run Singularity interactively:

$ srun --pty -p main --gres=gpu:1 --time=15:00 --mem=6G singularity shell --nv docker://tensorflow/tensorflow:1.4.1-gpu

Docker image path: index.docker.io/tensorflow/tensorflow:1.4.1-gpu

Cache folder set to /home/user/.singularity/docker

Creating container runtime...

Importing: /home/user/.singularity/docker/sha256:054be6183d067af1af06196d7123f7dd0b67f7157a0959bd857ad73046c3be9a.tar.gz

Importing: /home/user/.singularity/docker/sha256:779578d7ea6e8cc3934791724d28c56bbfc8b1a99e26236e7bf53350ed839b98.tar.gz

Importing: /home/user/.singularity/docker/sha256:82315138c8bd2f784643520005a8974552aaeaaf9ce365faea4e50554cf1bb44.tar.gz

Importing: /home/user/.singularity/docker/sha256:88dc0000f5c4a5feee72bae2c1998412a4b06a36099da354f4f97bdc8f48d0ed.tar.gz

Importing: /home/user/.singularity/docker/sha256:79f59e52a355a539af4e15ec0241dffaee6400ce5de828b372d06c625285fd77.tar.gz

Importing: /home/user/.singularity/docker/sha256:ecc723991ca554289282618d4e422a29fa96bd2c57d8d9ef16508a549f108316.tar.gz

Importing: /home/user/.singularity/docker/sha256:d0e0931cb377863a3dbadd0328a1f637387057321adecce2c47c2d54affc30f2.tar.gz

Importing: /home/user/.singularity/docker/sha256:f7899094c6d8f09b5ac7735b109d7538f5214f1f98d7ded5756ee1cff6aa23dd.tar.gz

Importing: /home/user/.singularity/docker/sha256:ecba77e23ded968b9b2bed496185bfa29f46c6d85b5ea68e23a54a505acb81a3.tar.gz

Importing: /home/user/.singularity/docker/sha256:037240df6b3d47778a353e74703c6ecddbcca4d4d7198eda77f2024f97fc8c3d.tar.gz

Importing: /home/user/.singularity/docker/sha256:b1330cb3fb4a5fe93317aa70df2d6b98ac3ec1d143d20030c32f56fc49b013a8.tar.gz

Importing: /home/user/.singularity/metadata/sha256:b71a53c1f358230f98f25b41ec62ad5c4ba0b9d986bbb4fb15211f24c386780f.tar.gz

Singularity: Invoking an interactive shell within container...

Singularity tensorflow:latest-gpu:~> 

Now, you're ready to execute commands:

Singularity tensorflow:latest-gpu:~> python -V

Python 2.7.12

Singularity tensorflow:latest-gpu:~> python3 -V

Python 3.5.2

Remember to exit from your interactive job after you are finished with your calculations.

There are several Docker images available on Amarel for use with Singularity. The one used in the example above, tensorflow:1.4.1-gpu, is intended for python 2.7.12. If you want to use Python3, you'll need a different image, docker://tensorflow/tensorflow:1.4.1-gpu-py3, and the Python command will be python3 instead of python in your script.

