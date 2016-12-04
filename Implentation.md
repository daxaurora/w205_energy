# Team Sunshine

# Implementation instructions - DRAFT
### Following these instructions will re-create a runnable instance of this project from scratch.

[Implementation instructions should be in the Final Report document, and emailed to Arash. Also the final version will end up in the Read Me document for this repo.]
[Also: some of this may instead end up in a bash set up script]

#### Step 1 - Launch an AWS AMI
* Launch an AWS EC2 instance of this AMI: UCB MIDS W205 EX2-FULL
    * Instance size: m3.large
    * Security group:
    Custom TCP Rules for Ports: 4040, 50070, 8888, 8080, 10000, 7180, 8088
    SSH for Port 22
    HTTP for Port 443
    Source for all rules: 0.0.0.0/0
    Protocol for all rules:  TCP
* Attach to this AMI an EBS on which postgres has been installed
* Connect to the instance from the command line of a local machine
* Find the location of the attached EBS (i.e., xvdf): 
`fdisk -l`
* Mount that EBS: 
`mount -t ext4 /dev/<ebs_location> /data`
(_Where ebs_location is the EBS location listed in the output from the fdisk command._)

#### Step 2 - Set up the AMI
* Start postgres as the root user:
`/data/start_postgres.sh`

* Install Anaconda as the root user:
```
wget https://repo.continuum.io/archive/Anaconda2-4.2.0-Linux-x86_64.sh
bash Anaconda2-4.2.0-Linux-x86_64.sh
# Enter through and read the license agreement
# when prompted change installation location to /data/anaconda2
# when prompted to prepend Anaconda location in .bashrc, enter yes
```

* Make sure root user is using anaconda python before installing anything else:
`PATH=/data/anaconda2/bin:$PATH`

* Install the following packages as the root user:
`pip install psycopg2`

Note that it is possible to see a list of all installed modules by going to the python prompt and entering help("modules").


* Switch to user w205: 
`su - w205`
_NOTE: I could not figure out how to switch users via a bash script - does anyone else know how to do this? - Laura_

* Update this user’s path to use new(anaconda) python:
`PATH=/data/anaconda2/bin:$PATH`

* Confirm this worked using: `which python`
This should print a file path that includes the word anaconda.

* Optional:  Start Jupyter Notebooks as the w205 user:
   * From the EC2 instance: `jupyter notebook —-no-browser —port=8888`
   * From your local machine: `ssh -i "mykey.pem" -NL 8888:localhost:10001 root@ec2-##-##-###-###.compute-1.amazonaws.com`
   * Open a browser to __localhost:10001__

* Clone the Github repo directly to the /home/w205 directory:
`git clone https://github.com/superbb/w205_energy.git`

_IMPORTANT:  all code is currently set up to run from inside the repo, with the repo cloned to the /home/w205 directory. If the files are moved elsewhere, code in following steps will not work._

#### Step 3 - Setup Postgres tables and authentication
* From any directory, run this setup script:
`python /home/w205/w205_energy/setup.py`

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
