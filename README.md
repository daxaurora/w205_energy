# w205 Final: Solar Energy Data Storage and Retrieval
__TEAM:__ Laura Williams, Geoff Stirling, Maya Miller-Vedam, Boris Kletser.  
__About This Repo:__ _Hey Superheroes! Here's a fresh clean spot where we can drop in all our stuff!_

## Quick Links
* [National Solar Radiation Database](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/solar-radiation)
* [Climate Data Online: Documentation](http://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted)
* [EIA Plant Level Data](http://www.eia.gov/opendata/qb.php?category=1017)

## TO DO:
* finish data ingest scripts (Maya & Laura)
* write code to analyze weather variability (Geoff)
* explore serving layer options (Boris)
* write an installation script  and store it in S3
* figure out whether the cloning of the repo can be scripted in bash
* (OPTIONAL) write a script to automate the timing of running the scripts
* check it all on a fresh AMI (a few times or, like, 10)

## How to Deploy this Application (DRAFT) :
__PREREQUISITES:__ _The code in this repository is intended to be run on the_ __UCB MIDS W205 EX2-FULL__ _AMI. Prior to following the steps described below it is assumed that the root user has launched the AMI and mounted an EBS volume with at least 100 GB of space at_ __/data__. Note that the set up process for running this application assumes that you are running Python2 and requires that the user have access to EAI (http://www.eia.gov/opendata/register.php) and NOAA API (https://www.ncdc.noaa.gov/cdo-web/token) credentials. Please have those on hand before proceeding.

__STEP 1:__ As the root user, download and run the installation script:
* `wget ...`
* `bash ...`
* this script should include the steps to install packages, start postgres, switch to w205 user, clone the repo, and cd in to that folder.

__STEP 2:__ Setup architecture: `python setup.py`
* NOTE: _this script will prompt you to enter your API credentials, please ensure that you have them on hand. For your security, the credentials you provide will be deleted by the clean up scripts in step 5 to avoid their getting on to github._
* At the prompts, enter this authentication information: [I think this document would work best as a markdown document in the repo, and then we can put the EIA key and NOAA token into the Final report and state clearly in this document where where to look in the final report. The final report will be emailed to Arash and won't be on the Repo, so that seems secure]

__STEP 3:__ Run data ingest and modeling
* From any directory, run these scripts to complete data ingest and data modeling [list scripts, start all with /home/w205/

__STEP 4:___ Serving layer

__STEP 5:__ Run clean up script to delete your API credentials: `python cleanup.py`
* NOTE: _This script will also give you the option to delete the postgres database and table that were created when you deployed this application._


## Development Process Notes:
1. Data ingest:
  1. grab power and capacity information for it (historic) (Laura)
  1. Grab all solar radiation weather data (Maya)
  1. Put data into postgres (Laura and Maya)
  1. analysis: linear regression for correlation between solar radiation and net generation for predicting energy output
  1. Optional: may add other analysis
  1. use daily or hourly data to keep a tally of fluctuation of solar radiation
     - need to compute standard deviations
  1. predict monthly energy generation
2. Combine the outcomes of each of the stations into a simple display
  1. first as a response in terminal
  1. as a simple web response
  1. as a self updating web response
    - will correspond to setting up something that runs in bg on server
  1. as a pretty web response
  1. with included visualizations
3. Allow filtering
  1. via terminal
  1. via web
    - lots of front end libraries for filtering sorting tables already, may not have to do anything on back end
4. Expand to larger set
5. Build presentation around it
