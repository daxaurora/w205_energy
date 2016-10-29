# w205_energy
w205 group project on renewable energy and weather

# Hey Superheroes! Here's a fresh clean spot where we can drop in all our stuff

### Background Research:
1. get an API key for the data source (I know we have some), 
2. figure out which file we want, 
3. figure out the right API query to run to get that file (or find a resource that would help us figure this out)
4. figure out the column names/schema for that data
5. figure out if there is a way to use AWS to house the data we pull in a way that is accessible to each of us.
6. set up a private team GitHub repo to share code and notes.

### Steps:
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
  2. as a simple web response
  3. as a self updating web response
    - will correspond to setting up something that runs in bg on server
  4. as a pretty web response 
  5. with included visualizations
4. Allow filtering
  1. via terminal
  2. via web
    - lots of front end libraries for filtering sorting tables already, may not have to do anything on back end
5. Expand to larger set
6. Build presentation around it
