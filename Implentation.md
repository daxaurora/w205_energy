# Team Sunshine

# Implementation instructions - DRAFT
### Following these instructions will re-create a runnable instance of this project from scratch.

[Implementation instructions should be in the Final Report document, and emailed to Arash. Also the final version will end up in the Read Me document for this repo.]
[Also: some of this may instead end up in a bash set up script]


#### Step 1 - Launch an AWS AMI
* Launch an AWS EC2 instance of this AMI: UCB MIDS W205 EX2-FULL
    * Instance size: m3.large
    * Attach an additional 100GB EBS to this drive (unless you already have already created an EBS with Postgres installed)
    * Security group:
        * Custom TCP Rules for Ports: 4040, 50070, 8888, 8080, 10000, 7180, 8088
        * SSH for Port 22
        * HTTP for Port 443
        * Source for all rules: 0.0.0.0/0
        * Protocol for all rules:  TCP
* If you have an EBS on which postgres has been installed, attach that to the AMI via the EWS Console
* Connect to the instance from the command line of a local machine
* Find the location of the attached 100GB EBS. The location will be similar to or identical to /dev/xvdf
```
fdisk -l
```
* If the attached EBS does not yet have Postgres installed, install it:
```
chmod a+rwx /data
wget https://s3.amazonaws.com/ucbdatasciencew205/setup_ucb_complete_plus_postgres.sh
chmod +x ./setup_ucb_complete_plus_postgres.sh
./setup_ucb_complete_plus_postgres.sh /dev/ebs_location>
# Where ebs_location is the EBS location listed in the output
# from the fdisk command
# Note that this will re-format the EBS from scratch
```
* If the attached EBS already has Postgres installed, mount that EBS (this is not necessary if you just now installed Postgres on this EBS)

```mount -t ext4 /dev/[ebs_location] /data
```

(Where ebs_location is the EBS location listed in the output from the fdisk command. It may, or may not, be /dev/xvdf)

#### Step 2 - Set up the AMI
* Start postgres as the root user (this is not necessary if you just now installed Postgres on this EBS)
```/data/start_postgres.sh
```

* Install Anaconda as the root user:
```
wget https://repo.continuum.io/archive/Anaconda2-4.2.0-Linux-x86_64.sh
bash Anaconda2-4.2.0-Linux-x86_64.sh
# Enter through and read the license agreement
# when prompted change installation location to /data/anaconda2
# when prompted to prepend Anaconda location in .bashrc, enter yes
```

* Make sure root user is using anaconda python before installing anything else:
```PATH=/data/anaconda2/bin:$PATH
```

* Install the following packages as the root user:
```pip install psycopg2
```
_Note that it is possible to see a list of all installed modules by going to the python prompt and entering help("modules")._


* Switch to user w205:
```su - w205
```
_NOTE: I could not figure out how to switch users via a bash script - does anyone else know how to do this? - Laura_

* Update this user’s path to use new(anaconda) python:
```PATH=/data/anaconda2/bin:$PATH
```

* Confirm this worked using: `which python`
This should print a file path that includes the word anaconda.

* Clone the Github repo directly to the /home/w205 directory:
```git clone https://github.com/superbb/w205_energy.git
```

* Optional:  Start Jupyter Notebooks as the w205 user:
   * From the EC2 instance:
   ```jupyter notebook --no-browser --port=8888
   ```
   * Create another connection to the AMI in a new Terminal window on your local machine:
     ```ssh -i "mykey.pem" -NL 10001:localhost:8888 root@ec2-##-##-###-###.compute-1.amazonaws.com
     ```
   * Open a browser to __localhost:10001__

   _IMPORTANT:  all code is currently set up to run from inside the repo, with the repo cloned to the /home/w205 directory. If the files are moved elsewhere, code in following steps will not work._

#### Step 3 - Setup Postgres tables and authentication
* From any directory, run this setup script:
```python /home/w205/w205_energy/setup.py
```

* At the prompts, enter an EIA API key and NOAA Token: [_The EIA key and NOAA token can be included in the Final report. The final report will be emailed to Arash and won't be on the Repo, so that seems secure_]


#### Step 4 - Data ingest and modeling
* From any directory, run these scripts to complete data ingest and to load data into postgres database:
```
python /home/w205/w205_energy/data_ingest_eia.py
# Note that the data_ingest_eia.py will take several minutes to run
python /home/w205/w205_energy/data_ingest_noaa.py
```

#### Step 5 - Data analysis
* From any directory, run these scripts to complete data analysis:
[list scripts]
