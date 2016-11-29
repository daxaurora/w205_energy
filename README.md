# w205 Final: Solar Energy Data Storage and Retrieval
__TEAM:__ Laura Williams, Geoff Stirling, Maya Miller-Vedam, Boris Kletser.  
__About This Repo:__ _Hey Superheroes! Here's a fresh clean spot where we can drop in all our stuff!_ 

## Quick Links
* [National Solar Radiation Database](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/solar-radiation)
* [Climate Data Online: Documentation](http://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted)

## TO DO BEFORE NEXT MEETING ( ):
* Install Anaconda on Boris' AMI (Maya)


## Outstanding Questions & Long Term TODOs
* Create instructions for the Final Report for implementation

## Process Outline:
1. Data ingest: 
  1. grab power and capacity information for it (historic) (Laura)
  1. Grab all solar radiation weather data (Maya)
  1. Put data into postgres (Laura and Maya)
  1. analysis: linear regression for correlation between solar radiation and net generation for predicting energy output
  1. Optional: may add other analysis
  1. use daily or hourly data to keep a tally of fluctuation of solar radiation
  1. predict monthly energy generation
3. Combine the outcomes of each of the stations into a simple display
  1. first as a response in terminal
  1. as a simple web response
  1. as a self updating web response
    - will correspond to setting up something that runs in bg on server
  1. as a pretty web response 
  1. with included visualizations
4. Allow filtering
  1. via terminal
  1. via web
    - lots of front end libraries for filtering sorting tables already, may not have to do anything on back end
5. Expand to larger set
6. Build presentation around it
