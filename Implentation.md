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
* Switch to user w205 _NOTE: I could not figure out how to switch users via a bash script - does anyone else know how to do this? - Laura_
```
su - w205
```
* Clone the Github repo directly to the /home/w205 directory. Repo link:
```
https://github.com/superbb/w205_energy.git
```
[Procedural issues:
1) We need to make Arash a collaborator for him to have access to this private repo.
2) Given that a password is required to clone a private repo, we will either need to keep this step out of a bash file OR collect a password as we did with the EIA key and NOAA token.
3) Presumably we should actually have all this in a branch, as we did for other assignments before grading. In that case, we will need to include this code:
```
# This code not yet necessary, but it will be eventually, assuming Arash wants us to create a separate branch for the project code.
git checkout [branchname]
```
* IMPORTANT:  all code is currently set up to run from inside the repo, with the repo cloned as above to the /home/w205 directory.  If it's necessary to copy the repo to another location, use this code:
```
# This code is not currently necessary, and may not ever be necessary:
cp -r /home/w205/[current location] /home/w205/w205_energy/
```

#### Step 3 - Setup Postgres tables and authentication
* From any directory, run this setup script:
```
python /home/w205/w205_energy/setup.py
```
_ISSUE: The setup.py file is currently giving me errors.  TBD_
* At the prompts, enter an EIA API key and NOAA Token: 
[The EIA key and NOAA token can be included in the Final report. The final report will be emailed to Arash and won't be on the Repo, so that seems secure]

#### Step 4 - Data ingest and modeling
* From any directory, run these scripts to complete data ingest and data modeling
[list scripts, start all with /home/w205/

#### Step 5 - Data analysis
* From any directory, run these scripts to complete data analysis:
[list scripts]
