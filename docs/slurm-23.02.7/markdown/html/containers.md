# Containers Guide

## Contents

- [Overview](#overview)
- [Known limitations](#limitations)
- [Prerequisites](#prereq)
- [Required software](#software)
- [Example configurations for various OCI Runtimes](#example)
- [Testing OCI runtime outside of Slurm](#testing)
- [Requesting container jobs or steps](#request)
- [Integration with Rootless Docker](#docker-scrun)
- [Integration with Podman](#podman-scrun)
- [OCI Container bundle](#bundle)
- [Example OpenMPI v5 + PMIx v4 container](#ex-ompi5-pmix4)
- [Container support via Plugin](#plugin)
- [Container Types](#types)

## Overview

Containers are being adopted in HPC workloads. Containers rely on existing kernel features to allow
greater user control over what applications see and can interact with at any given time. For HPC
Workloads, these are usually restricted to the [mount
namespace](http://man7.org/linux/man-pages/man7/mount_namespaces.7.html). Slurm natively supports
the requesting of unprivileged OCI Containers for jobs and steps.

## Known limitations

The following is a list of known limitations of the Slurm OCI container implementation.

- All containers must run under unprivileged (i.e. rootless) invocation. All commands are called by
  Slurm as the user with no special permissions.
- Custom container networks are not supported. All containers should work with the ["host"
  network](https://docs.docker.com/network/host/).
- Slurm will not transfer the OCI container bundle to the execution nodes. The bundle must already
  exist on the requested path on the execution node.
- Containers are limited by the OCI runtime used. If the runtime does not support a certain feature,
  then that feature will not work for any job using a container.
- oci.conf must be configured on the execution node for the job, otherwise the requested container
  will be ignored by Slurm (but can be used by the job or any given plugin).

## Prerequisites

The host kernel must be configured to allow user land containers:

    $ sudo sysctl -w kernel.unprivileged_userns_clone=1

Docker also provides a tool to verify the kernel configuration:

    $ dockerd-rootless-setuptool.sh check --force
    [INFO] Requirements are satisfied

## Required software:

- Fully functional [OCI
  runtime](https://github.com/opencontainers/runtime-spec/blob/master/runtime.md). It needs to be
  able to run outside of Slurm first.
- Fully functional OCI bundle generation tools. Slurm requires OCI Container compliant bundles for
  jobs.

## Example configurations for various OCI Runtimes

The [OCI Runtime Specification](https://github.com/opencontainers/runtime-spec) provides
requirements for all compliant runtimes but does **not** expressly provide requirements on how
runtimes will use arguments. In order to support as many runtimes as possible, Slurm provides
pattern replacement for commands issued for each OCI runtime operation. This will allow a site to
edit how the OCI runtimes are called as needed to ensure compatibility.

For *runc* and *crun*, there are two sets of examples provided. The OCI runtime specification only
provides the *start* and *create* operations sequence, but these runtimes provides a much more
efficient *run* operation. Sites are strongly encouraged to use the *run* operation (if provided) as
the *start* and *create* operations require that Slurm poll the OCI runtime to know when the
containers have completed execution. While Slurm attempts to be as efficient as possible with
polling, it will result in a thread using CPU time inside of the job and slower response of Slurm to
catch when container execution is complete.

The examples provided have been tested to work but are only suggestions. Sites are expected to
ensure that the resultant root directory used will be secure from cross user viewing and
modifications. The examples provided point to "/run/user/%U" where %U will be replaced with the
numeric user id which should be created and managed by systemd independently of Slurm. Be aware that
the directory in this example will be cleaned up by systemd once the user logs out of the node.

- oci.conf example for runc using create/start:

      EnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeEnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeQuery="runc --rootless=true --root=/run/user/%U/ state %n.%u.%j.%s.%t"
      RunTimeCreate="runc --rootless=true --root=/run/user/%U/ create %n.%u.%j.%s.%t -b %b"
      RunTimeStart="runc --rootless=true --root=/run/user/%U/ start %n.%u.%j.%s.%t"
      RunTimeKill="runc --rootless=true --root=/run/user/%U/ kill -a %n.%u.%j.%s.%t"
      RunTimeDelete="runc --rootless=true --root=/run/user/%U/ delete --force %n.%u.%j.%s.%t"

- oci.conf example for runc using run (suggested):

      EnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeEnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeQuery="runc --rootless=true --root=/run/user/%U/ state %n.%u.%j.%s.%t"
      RunTimeKill="runc --rootless=true --root=/run/user/%U/ kill -a %n.%u.%j.%s.%t"
      RunTimeDelete="runc --rootless=true --root=/run/user/%U/ delete --force %n.%u.%j.%s.%t"
      RunTimeRun="runc --rootless=true --root=/run/user/%U/ run %n.%u.%j.%s.%t -b %b"

- oci.conf example for crun using create/start:

      EnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeEnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeQuery="crun --rootless=true --root=/run/user/%U/ state %n.%u.%j.%s.%t"
      RunTimeKill="crun --rootless=true --root=/run/user/%U/ kill -a %n.%u.%j.%s.%t"
      RunTimeDelete="crun --rootless=true --root=/run/user/%U/ delete --force %n.%u.%j.%s.%t"
      RunTimeCreate="crun --rootless=true --root=/run/user/%U/ create --bundle %b %n.%u.%j.%s.%t"
      RunTimeStart="crun --rootless=true --root=/run/user/%U/ start %n.%u.%j.%s.%t"

- oci.conf example for crun using run (suggested):

      EnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeEnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeQuery="crun --rootless=true --root=/run/user/%U/ state %n.%u.%j.%s.%t"
      RunTimeKill="crun --rootless=true --root=/run/user/%U/ kill -a %n.%u.%j.%s.%t"
      RunTimeDelete="crun --rootless=true --root=/run/user/%U/ delete --force %n.%u.%j.%s.%t"
      RunTimeRun="crun --rootless=true --root=/run/user/%U/ run --bundle %b %n.%u.%j.%s.%t"

- oci.conf example for nvidia-container-runtime using create/start:

      EnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeEnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeQuery="nvidia-container-runtime --rootless=true --root=/run/user/%U/ state %n.%u.%j.%s.%t"
      RunTimeCreate="nvidia-container-runtime --rootless=true --root=/run/user/%U/ create %n.%u.%j.%s.%t -b %b"
      RunTimeStart="nvidia-container-runtime --rootless=true --root=/run/user/%U/ start %n.%u.%j.%s.%t"
      RunTimeKill="nvidia-container-runtime --rootless=true --root=/run/user/%U/ kill -a %n.%u.%j.%s.%t"
      RunTimeDelete="nvidia-container-runtime --rootless=true --root=/run/user/%U/ delete --force %n.%u.%j.%s.%t"

- oci.conf example for nvidia-container-runtime using run (suggested):

      EnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeEnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeQuery="nvidia-container-runtime --rootless=true --root=/run/user/%U/ state %n.%u.%j.%s.%t"
      RunTimeKill="nvidia-container-runtime --rootless=true --root=/run/user/%U/ kill -a %n.%u.%j.%s.%t"
      RunTimeDelete="nvidia-container-runtime --rootless=true --root=/run/user/%U/ delete --force %n.%u.%j.%s.%t"
      RunTimeRun="nvidia-container-runtime --rootless=true --root=/run/user/%U/ run %n.%u.%j.%s.%t -b %b"

- oci.conf example for hpcng singularity v3.8.0:

      EnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeEnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      OCIRunTimeQuery="sudo singularity oci state %n.%u.%j.%s.%t"
      OCIRunTimeCreate="sudo singularity oci create --bundle %b %n.%u.%j.%s.%t"
      OCIRunTimeStart="sudo singularity oci start %n.%u.%j.%s.%t"
      OCIRunTimeKill="sudo singularity oci kill %n.%u.%j.%s.%t"
      OCIRunTimeDelete="sudo singularity oci delete %n.%u.%j.%s.%t

  **WARNING**: Singularity (v3.8.0) requires *sudo* for OCI support, which is a security risk since
  the user is able to modify these calls. This example is only provided for testing purposes.

- oci.conf example for [Charliecloud](https://github.com/hpc/charliecloud) (v0.30)

      IgnoreFileConfigJson=true
      CreateEnvFile=newline
      EnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeEnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeRun="env -i PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin/:/sbin/ USER=$(whoami) HOME=/home/$(whoami)/ ch-run -w --bind /etc/group:/etc/group --bind /etc/passwd:/etc/passwd --bind /etc/slurm:/etc/slurm --bind %m:/var/run/slurm/ --bind /var/run/munge/:/var/run/munge/ --set-env=%e --no-passwd %r -- %@"
      RunTimeKill="kill -s SIGTERM %p"
      RunTimeDelete="kill -s SIGKILL %p"

- oci.conf example for [Enroot](https://github.com/NVIDIA/enroot) (3.3.0)

      IgnoreFileConfigJson=true
      CreateEnvFile=newline
      EnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeEnvExclude="^(SLURM_CONF|SLURM_CONF_SERVER)="
      RunTimeRun="/usr/local/bin/enroot-start-wrapper %b %m %e -- %@"
      RunTimeKill="kill -s SIGINT %p"
      RunTimeDelete="kill -s SIGTERM %p"

  /usr/local/bin/enroot-start-wrapper:

      #!/bin/bash
      BUNDLE="$1"
      SPOOLDIR="$2"
      ENVFILE="$3"
      shift 4
      IMAGE=

      export USER=$(whoami)
      export HOME="$BUNDLE/"
      export TERM
      export ENROOT_SQUASH_OPTIONS='-comp gzip -noD'
      export ENROOT_ALLOW_SUPERUSER=n
      export ENROOT_MOUNT_HOME=y
      export ENROOT_REMAP_ROOT=y
      export ENROOT_ROOTFS_WRITABLE=y
      export ENROOT_LOGIN_SHELL=n
      export ENROOT_TRANSFER_RETRIES=2
      export ENROOT_CACHE_PATH="$SPOOLDIR/"
      export ENROOT_DATA_PATH="$SPOOLDIR/"
      export ENROOT_TEMP_PATH="$SPOOLDIR/"
      export ENROOT_ENVIRON="$ENVFILE"

      if [ ! -f "$BUNDLE" ]
      then
              IMAGE="$SPOOLDIR/container.sqsh"
              enroot import -o "$IMAGE" -- "$BUNDLE" && \
              enroot create "$IMAGE"
              CONTAINER="container"
      else
              CONTAINER="$BUNDLE"
      fi

      enroot start -- "$CONTAINER" "$@"
      rc=$?

      [ $IMAGE ] && unlink $IMAGE

      exit $rc

## Testing OCI runtime outside of Slurm

Slurm calls the OCI runtime directly in the job step. If it fails, then the job will also fail.

- Go to the directory containing the OCI Container bundle:

      cd $ABS_PATH_TO_BUNDLE

- Execute OCI Container runtime (You can find a few examples on how to build a bundle
  [below](#bundle)):

      $OCIRunTime $ARGS create test --bundle $PATH_TO_BUNDLE

      $OCIRunTime $ARGS start test

      $OCIRunTime $ARGS kill test

      $OCIRunTime $ARGS delete test

  If these commands succeed, then the OCI runtime is correctly configured and can be tested in
  Slurm.

## Requesting container jobs or steps

*salloc*, *srun* and *sbatch* (in Slurm 21.08+) have the '--container' argument, which can be used
to request container runtime execution. The requested job container will not be inherited by the
steps called, excluding the batch and interactive steps.

- Batch step inside of container:

      sbatch --container $ABS_PATH_TO_BUNDLE --wrap 'bash -c "cat /etc/*rel*"'

- Batch job with step 0 inside of container:

      sbatch --wrap 'srun bash -c "--container $ABS_PATH_TO_BUNDLE cat /etc/*rel*"'

- Interactive step inside of container:

      salloc --container $ABS_PATH_TO_BUNDLE bash -c "cat /etc/*rel*"

- Interactive job step 0 inside of container:

      salloc srun --container $ABS_PATH_TO_BUNDLE bash -c "cat /etc/*rel*"

- Job with step 0 inside of container:

      srun --container $ABS_PATH_TO_BUNDLE bash -c "cat /etc/*rel*"

- Job with step 1 inside of container:

      srun srun --container $ABS_PATH_TO_BUNDLE bash -c "cat /etc/*rel*"

## Integration with Rootless Docker (Docker Engine v20.10+ & Slurm-23.02+)

Slurm's [scrun](scrun.md) can be directly integrated with [Rootless
Docker](https://docs.docker.com/engine/security/rootless/) to run containers as jobs. No special
user permissions are required and **should not** be granted to use this functionality.

### Prerequisites

1.  [slurm.conf](slurm.conf.md) must be configured to use Munge authentication.

        AuthType=auth/munge

2.  [scrun.lua](scrun.md#SECTION_Example-%3CB%3Escrun.lua%3C/B%3E-scripts) must be configured for
    site storage configuration.

### Limitations

1.  JWT authentication is not supported.

2.  Docker container building is not currently functional pending merge of [Docker pull
    request](https://github.com/moby/moby/pull/41442).

3.  Docker does **not** expose configuration options to disable security options needed to run jobs.
    This requires that all calls to docker provide the following command line arguments. This can be
    done via shell variable, an alias, wrapper function, or wrapper script:

        --security-opt label:disable --security-opt seccomp=unconfined --security-opt apparmor=unconfined --net=none

    Docker's builtin security functionality is not required (or wanted) for containers being run by
    Slurm. Docker is only acting as a container image lifecycle manager. The containers will be
    executed remotely via Slurm following the existing security configuration in Slurm outside of
    unprivileged user control.

4.  All containers must use [host networking](https://docs.docker.com/network/host/)

### Setup procedure

1.  [Install and configure Rootless Docker](https://docs.docker.com/engine/security/rootless/)  
    Rootless Docker must be fully operational and able to run containers before continuing.

2.  Setup environment for all docker calls:

        export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/docker.sock

    All commands following this will expect this environment variable to be set.

3.  Stop rootless docker:

        systemctl --user stop docker

4.  Configure Docker to call scrun instead of the default OCI runtime.

    - To configure for all users:

          /etc/docker/daemon.json

    - To configure per user:

          ~/.config/docker/daemon.json

    Set the following fields to configure Docker:

        {
          "default-runtime": "slurm",
          "runtimes": {
            "slurm": {
              "path": "/usr/local/bin/scrun"
            }
          },
          "experimental": true,
          "iptables": false,
          "bridge": "none",
          "no-new-privileges": true,
          "rootless": true,
          "selinux-enabled": false,
        }

    Correct path to scrun as if installation prefix was configured.

5.  It is strongly suggested that sites consider using inter-node shared filesystems to store
    Docker's containers. While it is possible to have a scrun.lua script to push and pull images for
    each deployment, there can be a massive performance penalty. Using a shared filesystem will
    avoid moving these files around.  
    Possible configuration additions to daemon.json to use a shared filesystem with [vfs storage
    driver](https://docs.docker.com/storage/storagedriver/vfs-driver/):

        {
          "storage-driver": "vfs",
          "data-root": "/path/to/shared/filesystem/user_name/data/",
          "exec-root": "/path/to/shared/filesystem/user_name/exec/",
        }

    Any node expected to be able to run containers from Docker must have ability to atleast read the
    filesystem used. Full write privileges are suggested and will be required if changes to the
    container filesystem are desired.

6.  Start rootless docker:

        systemctl --user start docker

7.  Verify Docker is using scrun:

        export DOCKER_SECURITY="--security-opt label:disable --security-opt seccomp=unconfined  --security-opt apparmor=unconfined --net=none"
        docker run $DOCKER_SECURITY hello-world
        docker run $DOCKER_SECURITY alpine printenv SLURM_JOB_ID
        docker run $DOCKER_SECURITY alpine hostname
        docker run $DOCKER_SECURITY alpine -e SCRUN_JOB_NUM_NODES=10 hostname

## Integration with Podman (Slurm-23.02+)

Slurm's [scrun](scrun.md) can be directly integrated with [Podman](https://podman.io/) to run
containers as jobs. No special user permissions are required and **should not** be granted to use
this functionality.

### Prerequisites

1.  Slurm must be fully configured and running on host running dockerd.

2.  [slurm.conf](slurm.conf.md) must be configured to use Munge authentication.

        AuthType=auth/munge

3.  [scrun.lua](scrun.md) must be configured for site storage configuration.

### Limitations

1.  JWT authentication is not supported.
2.  All containers must use [host
    networking](https://github.com/containers/podman/blob/main/docs/tutorials/basic_networking.md)

### Setup procedure

1.  [Install and configure Podman](https://podman.io/docs/installation)  
    Podman must be fully operational and able to run containers before continuing.

2.  Configure Podman to call scrun instead of the [default OCI
    runtime](https://github.com/opencontainers/runtime-spec).

    - To configure for all users:

          /etc/containers/containers.conf

    - To configure per user:

          ~/.config/containers/containers.conf

    Set the following configuration parameters to configure Podman:

        [containers]
        apparmor_profile = "unconfined"
        cgroupns = "host"
        cgroups = "enabled"
        default_sysctls = []
        label = false
        netns = "host"
        no_hosts = true
        pidns = "host"
        utsns = "host"
        userns = "host"

        [engine]
        cgroup_manager = "systemd"
        runtime = "slurm"
        runtime_supports_nocgroups = [ "slurm" ]
        runtime_supports_json = [ "slurm" ]
        remote = false

        [engine.runtimes]
        slurm = [ "/usr/local/bin/scrun" ]

    Correct path to scrun as if installation prefix was configured.

3.  The "cgroup_manager" field will need to be swapped to "cgroupfs" on systems not running systemd.

4.  It is strongly suggested that sites consider using inter-node shared filesystems to store
    Podman's containers. While it is possible to have a scrun.lua script to push and pull images for
    each deployment, there can be a massive performance penalty. Using a shared filesystem will
    avoid moving these files around.  

    - To configure for all users:

          /etc/containers/storage.conf

    - To configure per user:

          ~/.config/containers/storage.conf

    Possible configuration additions to storage.conf to use a shared filesystem with [vfs storage
    driver](https://docs.podman.io/en/latest/markdown/podman.1.html#storage-driver-value):

        [storage]
        driver = "vfs"
        runroot = "$HOME/containers"
        graphroot = "$HOME/containers"

        [storage.options]
        pull_options = {use_hard_links = "true", enable_partial_images = "true"}


        [storage.options.vfs]
        ignore_chown_errors = "true"

    Any node expected to be able to run containers from Podman must have ability to atleast read the
    filesystem used. Full write privileges are suggested and will be required if changes to the
    container filesystem are desired.

5.  Verify Podman is using scrun:

        podman run hello-world
        podman run alpine printenv SLURM_JOB_ID
        podman run alpine hostname
        podman run alpine -e SCRUN_JOB_NUM_NODES=10 hostname
        salloc podman run --env-host=true alpine hostname
        salloc sh -c 'podman run -e SLURM_JOB_ID=$SLURM_JOB_ID alpine hostname'

## OCI Container bundle

There are multiple ways to generate an OCI Container bundle. The instructions below are the method
we found the easiest. The OCI standard provides the requirements for any given bundle: [Filesystem
Bundle](https://github.com/opencontainers/runtime-spec/blob/master/bundle.md)

Here are instructions on how to generate a container using a few alternative container solutions:

- Create an image and prepare it for use with runc:
  1.  Use an existing tool to create a filesystem image in /image/rootfs:
      - debootstrap:

            sudo debootstrap stable /image/rootfs http://deb.debian.org/debian/

      - yum:

            sudo yum --config /etc/yum.conf --installroot=/image/rootfs/ --nogpgcheck --releasever=${CENTOS_RELEASE} -y

      - docker:

            mkdir -p ~/oci_images/alpine/rootfs
            cd ~/oci_images/
            docker pull alpine
            docker create --name alpine alpine
            docker export alpine | tar -C ~/oci_images/alpine/rootfs -xf -
            docker rm alpine

  2.  Configure a bundle for runtime to execute:

      - Use [runc](https://github.com/opencontainers/runc) to generate a config.json:

            cd ~/oci_images/alpine
            runc --rootless=true spec --rootless

      - Test running image:

      <!-- -->

          srun --container ~/oci_images/alpine/ uptime

Use [umoci](https://github.com/opencontainers/umoci) and skopeo to generate a full image:

    mkdir -p ~/oci_images/
    cd ~/oci_images/
    skopeo copy docker://alpine:latest oci:alpine:latest
    umoci unpack --rootless --image alpine ~/oci_images/alpine
    srun --container ~/oci_images/alpine uptime

Use [singularity](https://sylabs.io/guides/3.1/user-guide/oci_runtime.html) to generate a full
image:

    mkdir -p ~/oci_images/alpine/
    cd ~/oci_images/alpine/
    singularity pull alpine
    sudo singularity oci mount ~/oci_images/alpine/alpine_latest.sif ~/oci_images/alpine
    mv config.json singularity_config.json
    runc spec --rootless
    srun --container ~/oci_images/alpine/ uptime

## Example OpenMPI v5 + PMIx v4 container

Minimalist Dockerfile to generate a image with OpenMPI and PMIx to test basic MPI jobs.

#### Dockerfile

    FROM almalinux:latest
    RUN dnf -y update && dnf -y upgrade && dnf install -y yum-utils && dnf config-manager --set-enabled powertools
    RUN dnf -y install make automake gcc gcc-c++ kernel-devel bzip2 python3 wget libevent-devel hwloc-devel munge-devel

    WORKDIR /usr/local/src/
    RUN wget 'https://github.com/openpmix/openpmix/releases/download/v4.2.2/pmix-4.2.2.tar.bz2' -O - | tar -xvjf -
    WORKDIR /usr/local/src/pmix-4.2.2/
    RUN ./configure && make -j && make install

    WORKDIR /usr/local/src/
    RUN wget --inet4-only 'https://download.open-mpi.org/release/open-mpi/v5.0/openmpi-5.0.0rc9.tar.gz' -O - | tar -xvzf -
    WORKDIR /usr/local/src/openmpi-5.0.0rc9
    RUN ./configure --disable-pty-support --enable-ipv6 --without-slurm --with-pmix --enable-debug && make -j && make install

    WORKDIR /usr/local/src/openmpi-5.0.0rc9/examples
    RUN make && cp -v hello_c ring_c connectivity_c spc_example /usr/local/bin

## Container support via Plugin

Slurm also allows container developers to create [SPANK Plugins](plugins.md) that can be called at
various points of job execution to support containers. Slurm is generally agnostic to SPANK based
containers and can be made to start most, if not all, types. Any site using a plugin to start
containers should not create or configure the "oci.conf" configuration file to deactivate the OCI
container functionality.

Some container developers have chosen a command line interface only which requires users to
explicitly execute the container solution.

Links to several third party container solutions are provided below:

- [Charliecloud](#charliecloud)
- [Docker](#docker)
- [UDOCKER](#udocker)
- [Rootless Docker](#docker-rootless)
- [Kubernetes Pods (k8s)](#k8s)
- [Shifter](#shifter)
- [Singularity](#singularity)
- [ENROOT](#enroot)
- [Podman](#podman)
- [Sarus](#sarus)

Please note this list is not exhaustive as new containers types are being created all the time.

----------------------------------------------------------------------------------------------------

## Container Types

### Charliecloud

[Charliecloud](https://github.com/hpc/charliecloud) is user namespace container system sponsored by
[LANL](https://lanl.gov/) to provide HPC containers. Charliecloud supports the following:

- [Directly called by users](https://hpc.github.io/charliecloud/tutorial.html?highlight=slurm) via
  user namespace support.
- Direct Slurm support currently [in
  development](https://github.com/hpc/charliecloud/tree/slurm-plugin).
- Limited OCI Image support (via wrapper)

### Docker (running as root)

[Docker](https://www.docker.com/) currently has multiple design points that make it unfriendly to
HPC systems. The issue that usually stops most sites from using Docker is the requirement of "only
trusted users should be allowed to control your Docker daemon" [\[Docker
Security\]](https://docs.docker.com/engine/security/security/) which is not acceptable to most HPC
systems.

Sites with trusted users can add them to the docker Unix group and allow them control Docker
directly from inside of jobs. There is currently no direct support for starting or stopping docker
containers in Slurm.

Sites are recommended to extract the container image from docker (procedure above) and then run the
containers using Slurm.

### UDOCKER

[UDOCKER](https://github.com/indigo-dc/udocker) is Docker feature subset clone that is designed to
allow execution of docker commands without increased user privileges.

### Rootless Docker

[Rootless Docker](https://docs.docker.com/engine/security/rootless/) (\>=v20.10) requires no extra
permissions for users and currently (as of January 2021) has no known security issues with users
gaining privileges. Each user will need to run an instance of the dockerd server on each node of the
job in order to use docker. There are currently no helper scripts or plugins for Slurm to automate
the build up or tear down the docker daemons.

Sites are recommended to extract the container image from docker (procedure above) and then run the
containers using Slurm.

### Kubernetes Pods (k8s)

[Kubernetes](https://kubernetes.io/docs/concepts/workloads/pods/pod/) is a container orchestration
system that uses PODs, which are generally a logical grouping of containers for singular purpose.

There is currently no direct support for Kubernetes Pods in Slurm. Sites are encouraged to extract
the OCI image from Kubernetes and then run the containers using Slurm. Users can create jobs that
start together using the "--dependency=" argument in *sbatch* to mirror the functionality of Pods.
Users can also use a larger allocation and then start each pod as a parallel step using *srun*.

### Shifter

[Shifter](https://github.com/NERSC/shifter) is a container project out of
[NERSC](http://www.nersc.gov/) to provide HPC containers with full scheduler integration.

- Shifter provides full [instructions to integrate with
  Slurm](https://github.com/NERSC/shifter/wiki/SLURM-Integration).
- Presentations about Shifter and Slurm:
  - [Never Port Your Code Again - Docker functionality with Shifter using
    SLURM](../pdf/SLUG15/shifter.md)
  - [Shifter: Containers in HPC
    Environments](https://www.slideshare.net/insideHPC/shifter-containers-in-hpc-environments)

### Singularity

[Singularity](https://www.sylabs.io/singularity/) is hybrid container system that supports:

- Slurm integration (for singularity v2.x) via
  [Plugin](https://github.com/sylabs/singularity/blob/master/docs/2.x-slurm/README.md). A full
  description of the plugin was provided in the [SLUG17 Singularity
  Presentation](../pdf/SLUG17/SLUG_Bull_Singularity.md).
- User namespace containers via sandbox mode that require no additional permissions.
- Users directly calling singularity via setuid executable outside of Slurm.

### ENROOT

[Enroot](https://github.com/NVIDIA/enroot) is a user namespace container system sponsored by
[NVIDIA](https://www.nvidia.com) that supports:

- Slurm integration via [pyxis](https://github.com/NVIDIA/pyxis)
- Native support for Nvidia GPUs
- Faster Docker image imports

### Podman

[Podman](https://podman.io/) is a user namespace container system sponsored by
[Redhat/IBM](https://developers.redhat.com/blog/2018/08/29/intro-to-podman/) that supports:

- Drop in replacement of Docker.
- Called directly by users. (Currently lacks direct Slurm support).
- Rootless image building via [buildah](https://buildah.io/)
- Native OCI Image support

### Sarus

[Sarus](https://github.com/eth-cscs/sarus) is a privileged container system sponsored by ETH Zurich
[CSCS](https://user.cscs.ch/tools/containers/sarus/) that supports:

- [Slurm image synchronization via OCI
  hook](https://sarus.readthedocs.io/en/latest/config/slurm-global-sync-hook.html)
- Native OCI Image support
- NVIDIA GPU Support
- Similar design to [Shifter](#shifter)

Overview slides of Sarus are
[here](http://hpcadvisorycouncil.com/events/2019/swiss-workshop/pdf/030419/K_Mariotti_CSCS_SARUS_OCI_ContainerRuntime_04032019.pdf).

----------------------------------------------------------------------------------------------------

Last modified 29 September 2023
