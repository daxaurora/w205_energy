# w205 Final Project: Solar Energy and Weather Data Storage and Retrieval
__Team Sunshine:__ Laura Williams, Geoff Stirling, Maya Miller-Vedam, Boris Kletser  
__About This Repo:__ _This repo contains all code and instructions necessary to create a runnable instance of a storage and retrieval pipeline analyzing relationships between solar power output and weather data. To create the pipeline, please follow the instructions in the section below titled "How to Deploy this Application"_

## Quick Links
* [National Solar Radiation Database](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/solar-radiation)
* [Climate Data Online: Documentation](http://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted)
* [EIA Plant Level Data](http://www.eia.gov/opendata/qb.php?category=1017)

## How to Deploy this Application:
__STEP 1 - PREREQUISITES__ _The code in this repository requires a few assumptions be met_:
    * This code is intended to be run on the_ __UCB W205 Spring 2016__ AMI.
    * The AMI has an attached EBS volume with at least 100GB of space.
    * The AMI has been lauched and connected to via a local machine.
    * The attached EBS has been mounts at __/data__.
_These steps are all outlined in Step 1 of the Instructions.md file included in this repo. Please refer to that document if these prerequisites are unclear._

Additionally it will be necessary for the user to have an EIA API Key ready to supply for a setup script. A key can be obtained via EIA (http://www.eia.gov/opendata/register.php) and also a key will be provided in the Final Project Report.


__STEP 2 - Set up the Environment__
* Start postgres as the root user on the AMI:
```
/data/start_postgres.sh
```

* Install Anaconda as the root user:
    * _IMPORTANT:
        * When prompted change installation location to /data/anaconda2
        * when prompted to prepend Anaconda location in .bashrc, enter yes_
```
wget https://repo.continuum.io/archive/Anaconda2-4.2.0-Linux-x86_64.sh
bash Anaconda2-4.2.0-Linux-x86_64.sh
# Enter through and read the license agreement
```

* Switch root user so that it is using anaconda python before proceeding.
_NOTE: This command must be entered for every new connection to the root user on the AMI._
```
PATH=/data/anaconda2/bin:$PATH
```
* Confirm the root user is using anaconda python using:
```
which python
```
This should print a file path that includes the word anaconda.

* Install the following packages as the root user:
```
pip install psycopg2 vincenty
```
_Note that it is possible to see a list of all installed modules by going to the python prompt and entering help("modules")._

* Switch to user w205:
```
su - w205
```

* Update this user’s path to use new (anaconda) python:
_NOTE: This command must be entered EVERY TIME you switch to the w205 user on the AMI. If you switch to the root user and switch back to the w205 user, you must enter this command again._
```
PATH=/data/anaconda2/bin:$PATH
```

* Confirm the w205 user is using anaconda python using:
```
which python
```
This should print a file path that includes the word anaconda.

__STEP 3 - Set up architecture__
_IMPORTANT:  all code is currently set up to run from inside the repo below, with the repo cloned to the /home/w205 directory. If the files are moved elsewhere, code in following steps will not work._

* Clone this Github repo directly to the /home/w205 directory on the AMI:
```
git clone https://github.com/superbb/w205_energy.git
```

* From any directory, run this setup script:
_At the prompt, enter an EIA API key, which is recorded in the Final Project Report. For your security, the credentials you provide will be deleted by the clean up scripts in Step 6 below to avoid their getting on to github._
```
python /home/w205/w205_energy/setup.py
```

__STEP 4 - Data ingest, modeling, and storage__

* From any directory, run these scripts to complete data ingest, load data into a postgres database, and create CSV files for storage on Amazon S3.
    * The data_ingest_eia.py file may take approximately 10 minutes to run.
    * Add `verbose` at the end of each command to see logging.
```
python /home/w205/w205_energy/data_ingest_eia.py
python /home/w205/w205_energy/data_ingest_noaa.py
python /home/w205/w205_energy/postgres_to_csv.py
```

__STEP 5 - Analysis and Serving Layers___
* From any directory, run these scripts to complete data analysis:
```
# [list scripts]
```

* From any directory, run these scripts to interact with the serving layer:
```
# [list scripts]
```


__STEP 6 - Clean up__

Run this clean up script to delete your API credentials:
```
python /home/w205/w205_energy/cleanup.py
```
* NOTE: _This script will also give you the option to delete the postgres database and table that were created when you deployed this application._
