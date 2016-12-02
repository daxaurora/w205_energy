# Team Sunshine

# Implementation instructions - DRAFT
### Following these instructions will re-create a runnable instance of this project from scratch.

[Implementation instructions should be in the Final Report document, and emailed to Arash.  But perhaps this document can remain as a markdown document, and we can either refer to it in, or attach it to the Final Report?]
[Also: some of this may instead end up in a bash set up script]

#### Step 1 - Launch an AWS AMI
* Launch an AWS EC2 instance of this AMI: UCB W205 Spring 2016
    * Instance size: m3.large
    * Security group: [Do we need the Hadoop Cluster Security Group we have been using for class or not?]
* Attach to this AMI an EBS on which postgres has been installed
[Assume that we do not need to provide instructions for installing postgres, only for starting it (below)?]
* Connect to the instance from the command line of a local machine
* Find the location of the attached EBS (i.e., xvdf):
```
fdisk -l
```
* Mount that EBS
```
mount -t ext4 /dev/<ebs_location> /data
```
Where ebs_location is the EBS location listed in the output from the fdisk command

#### Step 2 - Set up the AMI
* Start postgres as the root user:
```
/data/start_postgres.sh
```
* Install Python 3 as the root user:
```
sudo yum install python34
```
* Install the following packages as the root user:
```
pip install requests
pip install psycopg2
```
* Switch to user w205 [assuming we are using the UCB AMI]
```
su - w205
```
* Clone the Github repo directly to the /home/w205 directory (provide link to repo)
```
https://github.com/superbb/w205_energy.git
```
[Assume that we need to make Arash a collaborator for him to have access to a private repo, right?]
[Assume that we do not need to provide code for cloning the repo and that Arash knows how to do that]
* [If we switch the files for this project to a branch, as we did for other assignments before grading, we will need to provide instructions to switch to that branch first - TBD]
```
git checkout [branchname]
```
* Copy the files from the repo into another directory so the project is not run inside the repo:
[Note: this might work better if there is one folder inside w205_energy that has all the scripts in it, then that folder can be copied out of the repo.  TBD]
[Also note: the setup.py document has a specific path listed for saving the credentials file that we will need to make sure works with whatever file structure is set up here.]
```
cp -r /home/w205/w205_energy/ /home/w205/sunshine/
```
[Note: sort out some standard procedure about where to put things, so that running all scripts below can be done by copying/pasting text]

#### Step 3 - Setup Postgres tables and authentication
* From any directory, run this setup script:
```
/home/w205/[subdirectory]/setup.py[ or setup.sh]
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
