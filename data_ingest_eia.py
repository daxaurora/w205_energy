"""
This python script loaads EIA data for Project Sunshine (W205 Final Project).
Before running this script please be sure that you have run setup.py to store
your API key in certs/mytokens.py. Alternately, you can manually enter it below.
"""

# Imports
from __future__ import absolute_import, print_function, unicode_literals
import os, requests, psycopg2, numpy as np, pandas as pd
from sqlalchemy import create_engine

# import the EIA API key or comment out this line and add it manually
from certs.mytokens import EIA_API_KEY
# EIA_API_KEY = ''

# First download the list of states
# EIA list of states is here: http://www.eia.gov/opendata/qb.php?category=1017
category_states = '1017'
states_url = 'http://api.eia.gov/category/?api_key=' + EIA_API_KEY + \
             '&category_id=' + category_states
states = requests.get(states_url)

# Create a variable to hold the status code
states_status = states.status_code
# This code will return 200 as an integer if everything downloaded properly
if states_status != 200:
    print("The list of power plants did not download properly. " + \
          " Please run this script again.")
else:
    pass

# Turn the list of states into a dataframe.
states_dict = states.json()
states_json = pd.io.json.json_normalize(states_dict['category'])
states_df = pd.DataFrame(states_json['childcategories'][0],
                         columns = ["name", 'category_id'])

# DOWNLOAD PLANT DATA

# Create empty dataframe to hold the list of all power plants
columns = ["name", 'category_id']
all_plants_df = pd.DataFrame(columns = columns)

# Iterate over the category_id value for each state in the states_df dataframe
for state in states_df.itertuples():
    # Isolate the category_id for each state
    state_id = str(state[2])
    # Download the plant data
    plants_url = 'http://api.eia.gov/category/?api_key=' + EIA_API_KEY + \
                 '&category_id=' + state_id
    plants = requests.get(plants_url)
    # Turn the downloaded data into a dataframe
    plants_dict = plants.json()
    plants_json = pd.io.json.json_normalize(plants_dict['category'])
    plants_df = pd.DataFrame(plants_json['childcategories'][0],
                             columns = ["name", 'category_id'])
    # Append each state's list of plants to the master all plants datagrame
    temp_df = all_plants_df.append(plants_df, ignore_index = True)
    all_plants_df = temp_df

# Fix names to remove the numbers in parentheses in each plant name
plants_name_temp1 = all_plants_df["name"].str.split(')').str.get(1)
plants_name_temp2 = pd.DataFrame(plants_name_temp1.str.split('(').str.get(0),
                                 columns = ["name"])
# Put data together in one dataframe
plants_final_df = pd.concat([plants_name_temp2,
                             all_plants_df["category_id"].astype('int')],
                             axis=1)
# Rename columns to match the ER diagram
col_new = {"name": "name", "category_id": "plant_id"}
plants_final_df.columns = [col_new.get(x, x) for x in plants_final_df.columns]

# Turn column into index
plants_final_df.set_index("plant_id", inplace = True)

# DOWNLOAD SOLAR LOCATION DATA

# Create empty dataframe to hold the list of all solar power locations
columns = ["name", 'series_id']
solar_df = pd.DataFrame(columns = columns)


# Iterate over each category_id value for each plant in the final_plants_df dataframe
for plant in plants_final_df.itertuples():
    # Isolate the category_id for each state
    plant_id = str(plant[0])
    # Download the plant data
    series_url = 'http://api.eia.gov/category/?api_key=' + EIA_API_KEY + '&category_id=' + plant_id
    series = requests.get(series_url)
    # Turn the downloaded data into a dataframe
    series_dict = series.json()
    series_json = pd.io.json.json_normalize(series_dict['category'])
    series_df = pd.DataFrame(series_json['childseries'][0], columns = ["name", 'series_id'])
    solar_filter1 = pd.DataFrame(series_df[series_df["name"].str.contains("solar") == True])
    solar_filter2 = pd.DataFrame(solar_filter1[solar_filter1["name"].str.startswith("Net generation") == True])
    solar_filter3 = pd.DataFrame(solar_filter2[solar_filter2["name"].str.endswith("monthly") == True])
    solar_filter4 = pd.DataFrame(solar_filter3[solar_filter3["name"].str.contains("all primemovers") == True])
    # Append each plant's list of series to the master all series dataframe
    temp_series_df = solar_df.append(solar_filter4, ignore_index = True)
    solar_df = temp_series_df

solar_name_temp1 = solar_df["name"].str.split(':').str.get(1)
solar_name_temp2 = pd.DataFrame(solar_name_temp1.str.split('(').str.get(0), columns = ["name"])
solar_final_df = pd.concat([solar_df["series_id"], solar_name_temp2], axis=1)

# DOWNLOAD ELECTRICITY GENERATION DATA

# Create empty dataframe to hold electricity generation data
columns = ["series_id", "lat", "lon", "latlon", "year", "month", "mwh"]
gen_final_df = pd.DataFrame(columns = columns)

# Iterate over each series in the solar power dataframe
for series in solar_final_df.itertuples():
    series_id = str(series[1])
    # Download the plant data
    gen_url = 'http://api.eia.gov/series/?api_key=' + EIA_API_KEY + '&series_id=' + series_id
    gen = requests.get(gen_url)
    # Put downloaded data into a dataframe
    gen_dict = gen.json()
    gen_json = pd.io.json.json_normalize(gen_dict['series'])
    gen_data_df = pd.DataFrame(gen_json['data'][0], columns = ["date", 'mwh'])
    # Organize data into the right columns in the dataframe
    gen_data_df['year'] = gen_data_df['date'][0][:4]
    gen_data_df['month'] = gen_data_df['date'][0][4:]
    gen_data_df['series_id'] = np.where(gen_data_df["mwh"] == 0, '', gen_json['series_id'])
    gen_data_df['lat'] = np.where(gen_data_df["mwh"] == 0, '', gen_json['lat'])
    gen_data_df['lon'] = np.where(gen_data_df["mwh"] == 0, '', gen_json['lon'])
    gen_data_df['latlon'] = np.where(gen_data_df["mwh"] == 0, '', gen_json['latlon'])
    # Remove all rows with zero electricty generation
    temp1_gen_df = gen_data_df[gen_data_df["mwh"] != 0]
    # Append each series's monthly electricity generation to the generation dataframe
    temp2_gen_df = gen_final_df.append(temp1_gen_df, ignore_index = True)
    gen_final_df = temp2_gen_df

# LOAD DATA INTO POSTGRES

# Set up connection to the post gres database
db_loc = 'postgresql+psycopg2://postgres:pass@localhost:5432/solarenergy'
engine = create_engine(db_loc)

# Load data to plants table
plants_final_df.to_sql("plants", engine, if_exists='append')

# Set up solar locations dataframe to match the ER diagram
# Rename column
col_new = {"name": "plant_name", "series_id": "loc_id"}
solar_final_df.columns = [col_new.get(x, x) for x in solar_final_df.columns]
# Turn column into index
solar_final_df.set_index("loc_id", inplace = True)

# Load data to solar_location table
solar_final_df.to_sql("solar_locations", engine, if_exists='append')

# Set up generation data to match the ER diagram
col_new = {"series_id": "loc_id",
           "lat": "latitude",
           "lon": "longitude",
           "latlon": "lat_lon",
           "date": "full_date",
           "year": "year",
           "month": "month",
           "mwh": "mwh", }

gen_final_df.columns = [col_new.get(x, x) for x in gen_final_df.columns]

# Load data to generation table
gen_final_df.to_sql("generation", engine, if_exists='append')
