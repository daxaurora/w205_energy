"""
This python script loaads EIA data for Project Sunshine (W205 Final Project).
Before running this script please be sure that you have run setup.py to store
your API key in certs/mytokens.py. Alternately, you can manually enter it below.

To run this script from the command line use:
    python data_ingest_eia.py
Or
    python data_ingest_eia.py verbose
"""

# Imports
from __future__ import absolute_import, print_function, unicode_literals
import os, requests, psycopg2, numpy as np, pandas as pd
from sqlalchemy import create_engine

# Import the EIA API key
from certs.mytokens import EIA_API_KEY
# Alternately, comment out the above line, uncomment the line below,
# and manually enter and EIA API key.
# EIA_API_KEY = ''

def get_category(category_id):
    """ Function returns data in json format from a given EIA category ID """
    url = 'http://api.eia.gov/category/?api_key=' + EIA_API_KEY + \
                 '&category_id=' + category_id
    data = requests.get(url)
    data_dict = data.json()
    data_json = pd.io.json.json_normalize(data_dict['category'])
    return data_json

def create_dataframe(data_json):
    data_df = pd.DataFrame(data_json['childcategories'][0],
                             columns = ["name", 'category_id'])
    return data_df

def create_plants(states):
    """ Function iterates over the dataframe of each state and returns
    a dataframe of all power plants in all states."""
    # Create empty dataframe to hold the list of all power plants
    columns = ["name", 'category_id']
    all_plants_df = pd.DataFrame(columns = columns)
    for state in states.itertuples():
        # Isolate the category_id for each state
        state_id = str(state[2])
        # Download power plants for this state using functions
        plants_json = get_category(state_id)
        plants_df = create_dataframe(plants_json)
        # Append each state's list of plants to the master all plants dataframe
        temp_df = all_plants_df.append(plants_df, ignore_index = True)
        all_plants_df = temp_df
    return all_plants_df

def clean_plant_data(all_plants_df):
    """Function cleans up names and data types in plant data"""
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
    plants_final_df.columns = [col_new.get(x, x) for x in
                               plants_final_df.columns]
    # Turn column into index
    plants_final_df.set_index("plant_id", inplace = True)
    return plants_final_df

def create_solar(plants_final_df):
    """ Function iterates over the list of plants and filters out locations
    with solar powered elecriticy generation."""
    # Create empty dataframe to hold the list of all solar power locations
    columns = ["name", 'series_id']
    solar_df = pd.DataFrame(columns = columns)
    for plant in plants_final_df.itertuples():
        # Isolate the category_id for each plant
        plant_id = str(plant[0])
        # Download the data for each plant using get_category function
        series_json = get_category(plant_id)
        # Create dataframe
        series_df = pd.DataFrame(series_json['childseries'][0],
                                 columns = ["name", 'series_id'])
        # Filter solar power data from each plant
        solar_filter1 = pd.DataFrame(series_df[series_df["name"].str.
                                     contains("solar") == True])
        solar_filter2 = pd.DataFrame(solar_filter1[solar_filter1["name"].str.
                                     startswith("Net generation") == True])
        solar_filter3 = pd.DataFrame(solar_filter2[solar_filter2["name"].str.
                                     endswith("monthly") == True])
        solar_filter4 = pd.DataFrame(solar_filter3[solar_filter3["name"].str.
                                     contains("all primemovers") == True])
        # Append solar power locations to the master dataframe
        temp_series_df = solar_df.append(solar_filter4, ignore_index = True)
        solar_df = temp_series_df
    return solar_df

def clean_solar_data(solar_df):
    """ Function cleans up plants names in solar location dataframe."""
    solar_name_temp1 = solar_df["name"].str.split(':').str.get(1)
    solar_name_temp2 = pd.DataFrame(solar_name_temp1.str.
                       split('(').str.get(0), columns = ["name"])
    solar_final_df = pd.concat([solar_df["series_id"],
                                solar_name_temp2], axis=1)
    return solar_final_df

def generation_data(solar_final_df):
    """ Function downloads monthly generation in megawatthours from all
    locations with solar powered electricity and also cleans this data."""
    # Create empty dataframe to hold electricity generation data
    columns = ["series_id", "lat", "lon", "latlon", "year", "month", "mwh"]
    gen_final_df = pd.DataFrame(columns = columns)
    # Iterate over each series in the solar power dataframe
    for series in solar_final_df.itertuples():
        series_id = str(series[1])
        # Download the plant data
        gen_url = 'http://api.eia.gov/series/?api_key=' + EIA_API_KEY + \
                  '&series_id=' + series_id
        gen = requests.get(gen_url)
        # Put downloaded data into a dataframe
        gen_dict = gen.json()
        gen_json = pd.io.json.json_normalize(gen_dict['series'])
        gen_data_df = pd.DataFrame(gen_json['data'][0],
                                   columns = ["date", 'mwh'])
        # Organize data into the right columns in the dataframe
        gen_data_df['year'] = gen_data_df['date'][0][:4]
        gen_data_df['month'] = gen_data_df['date'][0][4:]
        gen_data_df['series_id'] = np.where(gen_data_df["mwh"] == 0, '',
                                            gen_json['series_id'])
        gen_data_df['lat'] = np.where(gen_data_df["mwh"] == 0, '',
                                      gen_json['lat'])
        gen_data_df['lon'] = np.where(gen_data_df["mwh"] == 0, '',
                                      gen_json['lon'])
        gen_data_df['latlon'] = np.where(gen_data_df["mwh"] == 0, '',
                                         gen_json['latlon'])
        # Remove all rows with zero electricty generation
        temp1_gen_df = gen_data_df[gen_data_df["mwh"] != 0]
        # Append each series's monthly electricity generation to the generation dataframe
        temp2_gen_df = gen_final_df.append(temp1_gen_df, ignore_index = True)
        gen_final_df = temp2_gen_df
    return gen_final_df

def to_postgres(plants_final_df, solar_final_df, gen_final_df):
    """Function loads data from dataframes into previously create_dataframe
    Postgress database and tables."""
    # Set up connection to the Postgres database
    db_loc = 'postgresql+psycopg2://postgres:pass@localhost:5432/solarenergy'
    engine = create_engine(db_loc)
    # Load data to plants table
    plants_final_df.to_sql("plants", engine, if_exists='append')
    # Set up solar locations dataframe to match the ER diagram
    col_new = {"name": "plant_name", "series_id": "loc_id"}
    solar_final_df.columns = [col_new.get(x, x) for x in solar_final_df.columns]
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


# Command line instructions
if __name__ == '__main__':

    # Load list of states
    # EIA's list of states is here:
    # http://www.eia.gov/opendata/qb.php?category=1017
    states_json = get_category('1017')
    states_df = create_dataframe(states_json)
    # Load list of power plants using the list of states
    all_plants_df = create_plants(states_df)
    # Clean up plant data
    plants_final_df = clean_plant_data(all_plants_df)
    # Load list of solar power installations
    solar_df = create_solar(plants_final_df)
    # Clean up solar data
    solar_final_df = clean_solar_data(solar_df)
    # Load and clean electricity generation data
    gen_final_df = generation_data(solar_final_df)
    to_postgres(plants_final_df, solar_final_df, gen_final_df )
