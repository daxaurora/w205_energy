# Team Sunshine

# Implementation instructions
### Following these instructions will re-create a runnable instance of this project from scratch.

#### Step 1 - Launch an AWS AMI and set up the EBS
* Launch an AWS EC2 instance of this AMI: __UCB W205 Spring 2016__
    * Instance size: m3.large
    * Security group:
        * Custom TCP Rules for Ports: 4040, 50070, 8888, 8080, 10000, 7180, 8088
        * SSH for Port 22
        * HTTPS for Port 443
        * HTTP for Port 80
        * Source for all rules: 0.0.0.0/0
        * Protocol for all rules:  TCP
        * Storage: Do not attach additional storage when launching the AMI.
* In AWS, attach to this AMI an EBS on which postgres has been installed OR  create a new 100GB EBS and install Postgres on it (instructions below)
* Connect to the instance from the command line of a local machine
* Find the location of the attached EBS (the location will be similar to or identical to /dev/xvdf):
```
fdisk -l
```

* If the attached EBS does not yet have Postgres installed, install it:
```
chmod a+rwx /data
wget https://s3.amazonaws.com/ucbdatasciencew205/setup_ucb_complete_plus_postgres.sh
chmod +x ./setup_ucb_complete_plus_postgres.sh
./setup_ucb_complete_plus_postgres.sh /dev/[ebs_location]
# Where ebs_location is the EBS location listed in the output
# from the fdisk command
# Note that this will re-format the EBS from scratch
```

* If you are unsure what disks are mounted, enter this command:
```
mount
```

* Mount the EBS if necessary:
```
mount -t ext4 /dev/<ebs_location> /data
```
(_Where ebs_location is the EBS location listed in the output from the fdisk command._)

#### Step 2 - Set up the environment
* Start postgres as the root user (this is not necessary if you just now installed Postgres on this EBS):
```
/data/start_postgres.sh
```

* Install Anaconda as the root user:
    * _IMPORTANT_:
        * When prompted change installation location to /data/anaconda2
        * When prompted to prepend Anaconda location in .bashrc, enter yes
```
wget https://repo.continuum.io/archive/Anaconda2-4.2.0-Linux-x86_64.sh
bash Anaconda2-4.2.0-Linux-x86_64.sh
# Enter through and read the license agreement
```

* Switch root user to using anaconda python before proceeding.

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

* Update this user’s path to use new(anaconda) python:

_NOTE: This command must be entered EVERY TIME you switch to the w205 user on the AMI. If you switch to the root user and switch back to the w205 user, you must enter this command again._
```
PATH=/data/anaconda2/bin:$PATH
```

* Confirm the w205 user is using anaconda python using:
```
which python
```
This should print a file path that includes the word anaconda.

#### Step 3 - Download scripts, set up Postgres tables and authentication

 _IMPORTANT:  all code is currently set up to run from inside the repo below, with the repo cloned to the /home/w205 directory. If the files are moved elsewhere, code in following steps will not work._

* Clone the Github repo directly to the /home/w205 directory:
```
git clone https://github.com/superbb/w205_energy.git
```

* From any directory, run this setup script:

```
python /home/w205/w205_energy/setup.py
```

* At the prompt, enter an EIA API key, which is recorded in the Final Project Report.


#### Step 4 - Data ingest, modeling, and storage
* From any directory, run these scripts to complete data ingest, load data into postgres database, and create CSV files for storage on Amazon S3.
    * The data_ingest_eia.py file may take approximately 10 minutes to run.
    * Add `verbose` at the end of each command to see logging.
```
python /home/w205/w205_energy/data_ingest_eia.py
python /home/w205/w205_energy/data_ingest_noaa.py
python /home/w205/w205_energy/postgres_to_csv.py
```


#### Step 5 - Data analysis and serving layers
* From any directory, run these scripts to complete data analysis:
```
python /home/w205/w205_energy/data_linking.py
# [list additional scripts]
```

* From any directory, run these scripts to interact with the serving layer:
```
# [list scripts]
```

## How to set up and use Jupyter Notebooks on the AMI
* First complete all of Steps 1 and 2 above
* At the terminal connection to the instance, navigate to the directory at which you want to open Jupyter Notebooks.
* Then enter:
   ```
   jupyter notebook --no-browser --port=8888
   ```
 * Next, open a new terminal window and switch to the directly with your AMI key.  
    * You will put together some code to port the AMI Jupyter notebook to your local browser.  Essentially, you'll start with the same string you usually use to connect to your AMI, and add the porting code in the middle. The result, to be entered in this new terminal window, looks like this:
    ```
     ssh -i "mykey.pem" -NL 10001:localhost:8888 root@ec2-##-##-###-###.compute-1.amazonaws.com
    ```
    If everything went right, nothing will happen.  :-)

   * Open your browser and navigate to to __localhost:10001__
   The tab should open a Jupyter Notebook connected to the AMI.
