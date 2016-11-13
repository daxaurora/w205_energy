# Project Sunshine
## Linking actual data to our ER Diagram

Link to diagram in draw.io:
https://www.draw.io/#G0B5btR0kxRRufZGpuQlNrSGNVSWs

For each table in the ER diagram, below is listed the file and column name from which to populate the table.

The EIA data is organized in a very specific way, and once I looked through it, in a really awesome way. So I followed their lead in how I set up the ER diagram for this data, because that will make data ingest and analysis easier, I think. --Laura

#### Plants
This table includes all electrical power plants listed in the EIA database, regardless of how they produce electrical power.
* ID (PK)
Each plant has a unique category_id that has already been assigned by the EIA.
The category_id is probably most easily extracted from each state's list of plant names and category ids.
* Name
The plant name is also probably most easily extracted from each state's list of plant names and category ids.

A point of possible confusion with this category ID is that each plant has a number in parentheses in its name that is inexplicably different from the category ID.  The category ID is the number used in the API call, and given that I am thinking about writing code that would use the category ids in downloaded data to cycle through a loop of other API calls, I think it's better to use this category ID.  But it's important to point this out re: possible confusion.

Relationship:
Each plant can have multiple solar locations, but it is not necessary for a plant to have any solar locations.
Each solar location must have only one plant.


#### Solar Locations
Each plant has a collection of "series" that document different types of data about electrical power from that plant.  The geographical location is connected with each series, not each plant. I'm guessing this is because a plant can be very large and that there might be multiple power generation locations within each plant.
I think it will be possible to use the API code to filter only solar power generation into this table. But I haven't written the code, so I'm not sure how that will work exactly.
* ID (PK)
ID for this table will be the series_id. I think it makes sense to get this from each plant's list of series.  It is also of course in the data for each series.
* Plant_ID (FK)
Each series should be connected to its parent plant via this ID.
* Latitude
Within the data for each series is a latitude column.
* Longitude
Within the data for each series is a longitude column.
There is also a combined latitude and longitude column, if that turns out to be easier to work with at some point in our analysis.

Each solar location may have multiple pieces or types of generation data, but it is not necessary for a solar location to have any generation data.
All generation data must have only one solar location.

#### Generation
This table will record monthly net electricity generation from solar power.
* Index (PK)
I think this table would benefit from having an index as a unique ID (as much of the EIA data has in all of its tables). But maybe there is a better way.
* Series ID (PK)
All net generation data must be associated with a series ID, and thus a specific latitude and longitude associated with that series ID.
* Year
The data for each series contains a month/year number. I'm guessing it would be useful to extract separately the year and month from that number.
* Month
From the same location as the year, unless it turns out that it makes more sense to keep the month and year together as a single.  I'm not sure what will be easier to work with re: dates.
* MWH
Megawatt hours produced in each month from the facility indicated by the Series ID.

#### Weather
TBD, depending on how the weather data is organized and what works best for connecting it to the plant data.
