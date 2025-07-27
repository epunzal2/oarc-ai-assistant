You now have an account on the Amarel cluster.

Your cluster username is your NetID and your password is your regular NetID password.

Need help?   Please contact the Amarel support team at help@oarc.rutgers.edu 

Important -- please read
The acceptable use policies can be found HERE.

As an account holder for any of OARC’s systems, you are implying agreement to those policies and guidelines.

Using a shared cluster is quite different from using a single shared server. Please take a moment to learn how to use our system (specifically, using the SLURM system to request compute resources for your jobs). Mis-using resources can result in account suspension. The Amarel user guide is HERE.

About your account
Your personal /home directory is in /home/<NetID>. You have 100 GB of backed-up storage there. 

Your temporary /scratch directory is in /scratch/<NetID>.

You have 1 TB of space there.

/scratch is local storage, so your /scratch directory is not shared among the Amarel compute nodes in Camden, Newark, and Piscataway (each has its own local /scratch filesystem).

The /scratch filesystem is configured for parallel I/O, but it is not backed-up.

Files in /scratch that have not been accessed for 90 days will be deleted automatically.

/scratch is designed to be used only for temporary storage needed by actively running jobs.

Group membership
As a member of member of a department, institute, or research group that owns compute and storage resources on the Amarel cluster, you may also have access to that organization's job partition and private /projects storage space.

To get access to your organization's job partition and /projects storage, your organization's administrative point-of-contact or principal investigator (PI) must send an e-mail to help@oarc.rutgers.edu authorizing your access to their compute and/or storage resources.

Your organization's administrative point-of-contact or principal investigator (PI) can provide you with details about the location and names of their job partition and /projects storage space.

RU-Camden users
As a researcher or student affiliated with RU-Camden, you also have access to the Amarel-C system which comprises Amarel’s Camden-based compute and storage resources. The login node for Amarel-C is amarelc.hpc.rutgers.edu (notice the "c" at the end of "amarel" in that host name).

RU-Newark users
As a researcher or student affiliated with RU-Newark, you also have access to the Amarel-N system which comprises Amarel’s Newark-based compute and storage resources. The login node for Amarel-N is amareln.hpc.rutgers.edu (notice the "n" at the end of "amarel" in that host name).

Guest NetID holders
UPDATE: As of May 12, 2023, we have initiated an experiment that grants guest NetID holders access to all general amarel resources that were previously unavailable to them. Throughout this period, we will diligently monitor cluster usage and system loads to ensure optimal performance. If necessary, we retain the right to revert back to the previously enforced limited access. Meanwhile guest account holders may submit their jobs to general partitions by adding the following line to their scripts:
#SBATCH  -A general

Guests are granted limited access to Amarel. As a guest member of a department, institute, or group that owns compute and storage resources on the Amarel cluster, you may use the job partition(s) or storage resources owned by your host(s), but you will not have access to the University's centrally-funded compute resources (the main, gpu, mem, nonpre job partitions).

Receiving announcements
For information about additional services, training, special events, or our team, be sure to visit the OARC website at https://oarc.rutgers.edu.

Announcements for upcoming events or system maintenance will be sent to all Amarel users using their <NetID>@rutgers.edu account, so there’s no mailing list to join – you’re already on the list. 

