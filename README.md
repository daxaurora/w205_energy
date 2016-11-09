# w205 Final: Solar Energy Data Storage and Retrieval
__TEAM:__ Laura Williams, Geoff Stirling, Maya Miller-Vedam, Boris Kletser.  
__About This Repo:__ _Hey Superheroes! Here's a fresh clean spot where we can drop in all our stuff!_ 

## Quick Links
* [National Solar Radiation Database](https://www.ncdc.noaa.gov/data-access/land-based-station-data/land-based-datasets/solar-radiation)
* [Climate Data Online: Documentation](http://www.ncdc.noaa.gov/cdo-web/webservices/v2#gettingStarted)

## TO DO BEFORE NEXT MEETING ( ):
* look into python package FTP lib & Solar Radiation Database
* identify _what data/variables_ are available and _what files_ contain it and _what schema_ we'll put them into. (Laura - EIA, Geoff & Maya NOAA)
* draft a project proposal (All)
* Send project proposal in & Edit final results (Laura)
* Install Anaconda on Boris' AMI (Maya)
* create set up script & keep comments on logistical set-up (Boris)

## Outstanding Questions & Long Term TODOs
* should our API keys be in our python files? (possiblity to include in email along with other parameters for set up)

## Process Outline:
0. Background Research
  1. get an API key for the data source (DONE)
  2. figure out which file we want, (__this is the biggest outstanding task__)
  3. figure out the right API query to run to get that file (PARTIALLY DONE)
  4. figure out the column names/schema for that data (__depends on item 2__)
  5. figure out if there is a way to use AWS to house the data we pull in a way that is accessible to each of us.(DONE)
  6. set up a private team GitHub repo to share code and notes.(DONE)
1. Start with 1 station:  
  1. grab power and capacity information for it (historic)
    -  choose source(s)
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
