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
  1. grab power and capacity information for it (historic)
  1. Grab all solar radiation weather data
  1. grab weather data at that location (historic)
  1. see if we can combine input from last historic and plant historic to give some kind of insightful metric(s)
    - need to know what info we're grabbing from a and b 
  1. initially can be something super simple, later on make more complex, finally add ml to get this piece (think of it as a little arrow pointing to (send info out, get info back... the info we can fig out later)
  1. change historic weather input to the new hourly one instead
    - figure out how/what to store, cache, throw out
2. Repeat for a few other stations
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
