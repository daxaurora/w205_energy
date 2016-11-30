# Team Sunshine

# Implementation instructions - DRAFT
### Following these instructions will re-create a runnable instance of this project from scratch.

[From what I understand, implementation instructions should be in the Final Report document, and emailed to Arash.  So maybe all of this should go into the Final Report.  BUT I also like the idea of creating a markdown document in the github repo so that code can be copied and pasted.  So for now I'm making a markdown document, and maybe we can leave this whole thing in the repo, and copy and paste to the Final Report whatever we feel is appropriate once we get to that.]

#### Step 1 - Launch an AWS AMI
* Launch an AWS EC2 instance of this AMI: UCB MIDS W205 EX2-FULL AMI
    * Instance size: m3.large
    * Security group: [I don't know what we need to do for this.]
* Attach to this AMI an EBS on which postgres has been installed
[Assume that we do not need to provide instructions for installing postgres, only for starting it (below)?]
* Connect to the instance from the command line of a local machine
* Find the location of the attached EBS (i.e., xvdf):

```
fdisk -l
```
* Mount that EBS
```mount -t ext4 /dev/<ebs_location> /data
```
Where "<ebs_location>" = the EBS location listed in the output from the fdisk command

#### Step 2 - Set up the AMI
* Start postgres as the root user:
```data/start_postgres.sh
```
* [IMPORTANT:  Do we need to install Python 3?]
* Install the following packages as the root user:
```pip install requests
```
```pip install psycopg2
```
* Switch to user w205 [assuming we are using the UCB AMI]
```su - w205
```
* Clone the Github repo directly to the /home/w205 directory (provide link to repo)
[Assume that we need to make Arash a collaborator for him to have access to a private repo, right?]
[Assume that we do not need to provide code for cloing the repo and that Arash knows how to do that]
* [If we switch the files for this project to a branch, as we did for other assignments before grading, we will need to provide instructions to switch to that branch first - TBD]
```git checkout [branchname]
```
* Copy the files from the repo into another directory:
```cp -r /home/w205/w205_energy/[subdirectory] /home/w205/
```
[Note: sort out some standard procedure about where to put things, so that running all scripts below can be done by copying/pasting text]

#### Step 3 - Setup Postgres tables and authentication
* From any directory, run this setup script:
```/home/w205/[subdirectory]/setup.py[ or setup.sh]
```
[Note: filename in our repo is setup.py, but error statement at end refers to a setup.sh - is this going to be a separate file?]
* At the prompts, enter this authentication information:
[I think this document would work best as a markdown document in the repo, and then we can put the EIA key and NOAA token into the Final report and state clearly in this document where where to look in the final report.  The final report will be emailed to Arash and won't be on the Repo, so that seems secure]

#### Step 4 - Data ingest and modeling
* From any directory, run these scripts to complete data ingest and data modeling
[list scripts, start all with /home/w205/

#### Step 5 - Data analysis
* From any directory, run these scripts to complete data analysis:
[list scripts]
