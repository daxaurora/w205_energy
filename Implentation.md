# Team Sunshine

# Implementation instructions - DRAFT
### Following these instructions will re-create a runnable instance of this project from scratch.

[Implementation instructions should be in the Final Report document, and emailed to Arash.  But perhaps this document can remain as a markdown document, and we can either refer to it in, or attach it to the Final Report?]
[Also: some of this may instead end up in a bash set up script]

#### Step 1 - Launch an AWS AMI
* Launch an AWS EC2 instance of this AMI: UCB MIDS W205 EX2-FULL
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

* Install the following packages as the root user:
```
pip install psycopg2
pip install pandas
```
Note that the following packages are already installed on this AMI: os requests

* Switch to user w205 _NOTE: I could not figure out how to switch users via a bash script - does anyone else know how to do this? - Laura_
```
su - w205
```
* Clone the Github repo directly to the /home/w205 directory
```
git clone https://github.com/superbb/w205_energy.git
```

_IMPORTANT:  all code is currently set up to run from inside the repo, with the repo cloned to the /home/w205 directory. If the files are moved elsewhere, code in following steps will not work._

#### Step 3 - Setup Postgres tables and authentication
* From any directory, run this setup script:
```
python /home/w205/w205_energy/setup.py
```
* At the prompts, enter an EIA API key and NOAA Token:
[The EIA key and NOAA token can be included in the Final report. The final report will be emailed to Arash and won't be on the Repo, so that seems secure]

#### Step 4 - Data ingest and modeling
* From any directory, run these scripts to complete data ingest and to load data into postgres database:
```
python /home/w205/w205_energy/data_ingest_eia.py
#EIA data ingest script will is not complete:
# still needs code to load data into postgres
#[Maya's scripts for NOAA data]
```

#### Step 5 - Data analysis
* From any directory, run these scripts to complete data analysis:
[list scripts]
